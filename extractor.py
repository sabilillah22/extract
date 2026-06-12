import os
import sys
import zipfile
from xml.dom import minidom


def get_ooxml_version(output_dir):
    content_types_path = os.path.join(output_dir, '[Content_Types].xml')
    if not os.path.exists(content_types_path):
        return None

    try:
        with open(content_types_path, 'rb') as f:
            parsed = minidom.parse(f)

        overrides = parsed.getElementsByTagName('Override')
        content_type = ""
        for override in overrides:
            ct = override.getAttribute('ContentType')
            if 'officedocument' in ct:
                content_type = ct
                break

        if not content_type:
            # Fallback: check Default tags too
            defaults = parsed.getElementsByTagName('Default')
            for default in defaults:
                ct = default.getAttribute('ContentType')
                if 'officedocument' in ct:
                    content_type = ct
                    break

        # --- Segment 1: ECMA Edition ---
        if '2006' in content_type:
            edition = 1
        elif '2009' in content_type or '2010' in content_type:
            edition = 3
        elif '2011' in content_type or '2012' in content_type:
            edition = 4
        else:
            edition = 5

        # --- Segment 2: Conformance level ---
        strict = False
        for fname in ['word/settings.xml', 'word/document.xml']:
            fpath = os.path.join(output_dir, fname)
            if os.path.exists(fpath):
                with open(fpath, 'rb') as f:
                    raw = f.read().decode('utf-8', errors='ignore')
                if 'strict' in raw.lower():
                    strict = True
                    break
        conformance = 2 if strict else 1

        # --- Segment 3: Document part (case-insensitive) ---
        ct_lower = content_type.lower()
        if 'wordprocessingml' in ct_lower:
            part = 1
        elif 'spreadsheetml' in ct_lower:
            part = 2
        elif 'presentationml' in ct_lower:
            part = 3
        else:
            # Last resort: check by file extension of docx itself
            word_dir = os.path.join(output_dir, 'word')
            ppt_dir  = os.path.join(output_dir, 'ppt')
            xl_dir   = os.path.join(output_dir, 'xl')
            if os.path.exists(word_dir):
                part = 1
            elif os.path.exists(xl_dir):
                part = 2
            elif os.path.exists(ppt_dir):
                part = 3
            else:
                part = 4

        return f"{edition}.{conformance}.{part}"

    except Exception as e:
        print(f"  [Warning] Version detection error: {e}")
        return None


def extract_ooxml(docx_path, output_dir):
    """Extracts a .docx file and pretty-prints its internal XML structure."""
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(docx_path, 'r') as archive:
        for file_info in archive.infolist():
            extracted_path = os.path.join(output_dir, file_info.filename)

            if file_info.is_dir():
                os.makedirs(extracted_path, exist_ok=True)
                continue

            destination_dir = os.path.dirname(extracted_path)
            if destination_dir:
                os.makedirs(destination_dir, exist_ok=True)

            file_data = archive.read(file_info.filename)

            if file_info.filename.endswith(('.xml', '.rels')):
                try:
                    parsed_xml = minidom.parseString(file_data)
                    pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="utf-8")
                    with open(extracted_path, 'wb') as xml_file:
                        xml_file.write(pretty_xml)
                    print(f"  Extracted & Formatted: {file_info.filename}")
                except Exception as exc:
                    print(f"  Warning: could not format {file_info.filename} as XML: {exc}")
                    with open(extracted_path, 'wb') as raw_file:
                        raw_file.write(file_data)
            else:
                with open(extracted_path, 'wb') as binary_file:
                    binary_file.write(file_data)


if __name__ == '__main__':
    print("=" * 50)
    print("       OOXML Extractor Tool")
    print("=" * 50)

    docx_path = input("\nEnter the path to your .docx file:\n> ").strip().strip('"')

    if not docx_path.endswith('.docx'):
        print("Error: File must be in .docx format.")
        sys.exit(1)

    if not os.path.exists(docx_path):
        print(f"Error: File '{docx_path}' not found.")
        sys.exit(1)

    base_name  = os.path.splitext(os.path.basename(docx_path))[0]
    output_dir = os.path.join(os.path.dirname(docx_path), base_name)

    # Handle edge case where dirname returns empty string (same directory)
    if not output_dir:
        output_dir = base_name

    print(f"\nExtracting : {docx_path}")
    print(f"Output dir : {output_dir}/\n")

    extract_ooxml(docx_path, output_dir)

    version     = get_ooxml_version(output_dir)
    iso_year_map = {1: '2006', 2: '2008', 3: '2011', 4: '2012', 5: '2016'}
    doc_type_map = {1: 'WordprocessingML (.docx)', 2: 'SpreadsheetML (.xlsx)', 3: 'PresentationML (.pptx)', 4: 'Other'}
    suffix_map   = {1: 'st', 2: 'nd', 3: 'rd'}

    print(f"\n{'=' * 50}")
    if version:
        v           = version.split('.')
        edition     = int(v[0])
        conformance = int(v[1])
        part        = int(v[2])

        iso_year       = iso_year_map.get(edition, 'Unknown')
        edition_suffix = suffix_map.get(edition, 'th')

        print(f"OOXML Version : {version}")
        print(f"  Edition     : ECMA-376 {edition}{edition_suffix} / ISO/IEC 29500:{iso_year}")
        print(f"  Conformance : {'Strict' if conformance == 2 else 'Transitional'}")
        print(f"  Document    : {doc_type_map.get(part, 'Unknown')}")
    else:
        print("OOXML version info: not detected.")
    print(f"{'=' * 50}\n")