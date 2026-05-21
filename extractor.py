import os
import zipfile
from xml.dom import minidom

def extract_ooxml(docx_path, output_dir):
    """Extracts a .docx file and pretty-prints its internal XML structure."""
    # Ensure output target directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Open the word document as a standard zip archive
    with zipfile.ZipFile(docx_path, 'r') as archive:
        for file_info in archive.infolist():
            # Define destination paths
            extracted_path = os.path.join(output_dir, file_info.filename)

            # If the item is a folder, create it and skip processing
            if file_info.is_dir():
                os.makedirs(extracted_path, exist_ok=True)
                continue

            # Create subdirectories if they do not exist yet
            destination_dir = os.path.dirname(extracted_path)
            if destination_dir:
                os.makedirs(destination_dir, exist_ok=True)

            # Read file raw data
            file_data = archive.read(file_info.filename)

            # Pretty-print XML files for human readability
            if file_info.filename.endswith(('.xml', '.rels')):
                try:
                    parsed_xml = minidom.parseString(file_data)
                    # Convert to indented UTF-8 string format
                    pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="utf-8")

                    with open(extracted_path, 'wb') as xml_file:
                        xml_file.write(pretty_xml)
                    print(f"Extracted & Formatted: {file_info.filename}")
                except Exception as exc:
                    print(f"Warning: could not format {file_info.filename} as XML: {exc}")
                    # Fallback for malformed XML or system quirks
                    with open(extracted_path, 'wb') as raw_file:
                        raw_file.write(file_data)
            else:
                # Direct binary dump for images/media files
                with open(extracted_path, 'wb') as binary_file:
                    binary_file.write(file_data)

if __name__ == '__main__':
    extract_ooxml('Test2.docx', './extracted_word_structure')