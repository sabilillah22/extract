1) OOXML Structure Extractor

A Python utility that unpacks a `.docx` file and pretty prints its internal XML, making the underlying Office Open XML (OOXML) structure human-readable for inspection, debugging, or learning purposes. It also detects and reports the OOXML version used in the document.



2) Background

`.docx` files are ZIP archives containing a collection of XML files and binary assets (images, fonts, etc.). This tool extracts that structure and formats every `.xml` and `.rels` file with proper indentation, so you can read and explore the internals without a specialised editor.

The tool also analyses the extracted `[Content_Types].xml` and internal folder structure to produce a structured version string (e.g. `5.1.1`) that identifies the ECMA-376 edition, conformance level, and document type of the file.



3) Features

- Extracts the full internal structure of any `.docx` file
- Pretty-prints all `.xml` and `.rels` files with 2-space indentation
- Preserves the original folder hierarchy (`word/`, `_rels/`, `docProps/`, etc.)
- Writes binary assets (images, media) as-is without modification
- Detects and displays a structured OOXML version string (e.g. `5.1.1`)
- Breaks down the version into Edition, Conformance level, and Document type
- Falls back to internal folder structure detection if content type parsing fails
- Falls back gracefully if an XML file is malformed



4) Usage

Run the script and enter the path to your `.docx` file when prompted:

```bash
python extract.py
```

```
==================================================
       OOXML Extractor Tool
==================================================

>
```

Then either:
- **Type** the full path to your file, e.g. `C:\Users\User\Documents\report.docx`
- **Drag and drop** the `.docx` file directly into the terminal window — the path will auto-fill

The output folder is automatically named after your input file and saved in the same directory:

| Input File | Output Folder |
|---|---|
| `C:\Users\User\Desktop\report.docx` | `C:\Users\User\Desktop\report\` |
| `C:\Users\User\Downloads\thesis.docx` | `C:\Users\User\Downloads\thesis\` |

---

5) Output Structure

After extraction, the output directory mirrors the internal ZIP layout of the `.docx`:

```
report/
├── [Content_Types].xml       # Declares all content types in the package
├── _rels/
│   └── .rels                 # Top-level relationships
├── docProps/
│   ├── app.xml               # Application metadata
│   └── core.xml              # Author, title, dates
└── word/
    ├── document.xml          # Main document body (text, paragraphs, tables)
    ├── styles.xml            # Named styles and formatting rules
    ├── settings.xml          # Document-level settings
    ├── theme/
    │   └── theme1.xml        # Colour and font theme
    ├── _rels/
    │   └── document.xml.rels # Relationships (images, headers, footnotes, etc.)
    └── media/
        └── image1.png        # Embedded binary assets (extracted as-is)
```

> The exact contents vary depending on the features used in the document (headers, footnotes, comments, embedded objects, etc.).

---

6) OOXML Version Detection

After extraction, the tool prints a structured version string:

```
==================================================
OOXML Version : 5.1.1
  Edition     : ECMA-376 5th / ISO/IEC 29500:2016
  Conformance : Transitional
  Document    : WordprocessingML (.docx)
==================================================
```

The version string follows the format `Edition.Conformance.DocumentType`:

```
5 . 1 . 1
│   │   └─── Document Type
│   └─────── Conformance Level
└─────────── ECMA-376 Edition
```

