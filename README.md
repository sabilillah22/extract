1) OOXML Structure Extractor

A Python utility that unpacks a `.docx` file and pretty-prints its internal XML, making the underlying Office Open XML (OOXML) structure human-readable for inspection, debugging, or learning purposes.


2) Background

`.docx` files are ZIP archives containing a collection of XML files and binary assets (images, fonts, etc.). This tool extracts that structure and formats every `.xml` and `.rels` file with proper indentation, so you can read and explore the internals without a specialised editor.


3) Features

- Extracts the full internal structure of any `.docx` file
- Pretty prints all `.xml` and `.rels` files with 2-space indentation
- Preserves the original folder hierarchy (`word/`, `_rels/`, `docProps/`, etc.)
- Writes binary assets (images, media) as-is without modification
- Falls back gracefully if an XML file is malformed


4) As a script

Place your `.docx` file in the same directory as the script, then run:

```bash
python extract_ooxml.py
```

By default this extracts `File.docx` into a folder called `./extracted_word_structure`. Edit the last two lines of the script to change these:

```python
extract_ooxml('your_file.docx', './your_output_folder')
```

5) As a module

```python
from extract_ooxml import extract_ooxml

extract_ooxml('report.docx', './output')
```



6) Output Structure

After extraction, the output directory mirrors the internal ZIP layout of the `.docx`:

```
extracted_word_structure/
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



7) Key Files to Explore

| File | What it contains |
|------|-----------------|
| `word/document.xml` | All body text, paragraphs, tables, and inline formatting |
| `word/styles.xml` | Style definitions (Heading 1, Normal, etc.) |
| `word/numbering.xml` | List and numbering definitions |
| `word/_rels/document.xml.rels` | Links between the document and its resources |
| `[Content_Types].xml` | Package manifest — lists every file and its MIME type |

