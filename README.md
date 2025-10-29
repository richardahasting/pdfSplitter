# PDF Splitter

A simple Python tool to split large PDF files into multiple smaller files. Supports two splitting modes: by number of pages per file or by total number of output files.

## Features

- **Split by pages**: Create files with N pages each (e.g., 10-page chunks)
- **Split by number of files**: Divide PDF equally into N files
- **Flexible output**: Specify custom output directory
- **Smart naming**: Output files named `input_part_001.pdf`, `input_part_002.pdf`, etc.
- **Error handling**: Validates input and provides clear error messages

## Installation

### Option 1: Install as a command-line tool (Recommended)

Install directly from the repository:

```bash
pip install git+https://github.com/richardahasting/pdfSplitter.git
```

Or clone and install locally:

```bash
git clone https://github.com/richardahasting/pdfSplitter.git
cd pdfSplitter
pip install .
```

After installation, you can use `pdfsplitter` command directly:

```bash
pdfsplitter input.pdf --pages 10
```

### Option 2: Development installation

For development or if you want to modify the code:

```bash
git clone https://github.com/richardahasting/pdfSplitter.git
cd pdfSplitter
pip install -e .
```

### Option 3: Manual installation (no pip install)

If you prefer to run the script directly without installing:

```bash
git clone https://github.com/richardahasting/pdfSplitter.git
cd pdfSplitter
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python pdfsplitter.py input.pdf
```

## Usage

**Note**: If you installed using Option 1 or 2, use `pdfsplitter` command. If using Option 3 (manual), use `python pdfsplitter.py`.

### Basic Usage (Default: 10 pages per file)

```bash
pdfsplitter input.pdf
# Or if running manually: python pdfsplitter.py input.pdf
```

This splits `input.pdf` into files with 10 pages each (default).

### Split by Pages Per File

```bash
# Split into 20-page files
pdfsplitter input.pdf --pages 20

# Split into 5-page files
pdfsplitter input.pdf --pages 5
```

### Split into N Files

```bash
# Split into exactly 5 files (pages distributed evenly)
pdfsplitter input.pdf --files 5

# Split into 10 files
pdfsplitter input.pdf --files 10
```

### Specify Output Directory

```bash
# Save output to specific directory
pdfsplitter input.pdf --pages 10 -o output/

# Save to subdirectory
pdfsplitter input.pdf --files 3 -o split_pdfs/
```

## Examples

**Example 1**: Split 100-page PDF into 10-page files
```bash
pdfsplitter document.pdf --pages 10
# Creates: document_part_001.pdf (pages 1-10)
#          document_part_002.pdf (pages 11-20)
#          ...
#          document_part_010.pdf (pages 91-100)
```

**Example 2**: Split 100-page PDF into 5 equal files
```bash
pdfsplitter document.pdf --files 5
# Creates: document_part_001.pdf (pages 1-20)
#          document_part_002.pdf (pages 21-40)
#          document_part_003.pdf (pages 41-60)
#          document_part_004.pdf (pages 61-80)
#          document_part_005.pdf (pages 81-100)
```

**Example 3**: Split with custom output directory
```bash
pdfsplitter large_document.pdf --pages 15 -o output/
# Creates files in the 'output/' directory
```

## Command-Line Options

```
positional arguments:
  input                 Input PDF file path

options:
  -h, --help            Show help message and exit
  -o, --output-dir      Output directory for split files (default: current directory)
  --pages PAGES         Number of pages per output file (default: 10)
  --files FILES         Number of output files to create
```

**Note**: `--pages` and `--files` are mutually exclusive. Use one or the other.

## Output Format

Output files are named using the pattern:
```
<input_filename>_part_<number>.pdf
```

Numbers are zero-padded to 3 digits (001, 002, 003, etc.) for proper sorting.

## Requirements

- Python 3.7+
- pypdf >= 4.0.0

## Error Handling

The tool includes validation for:
- Non-existent input files
- Empty PDF files
- Invalid split parameters (e.g., more files than pages)
- Output directory creation

## License

MIT License - Feel free to use and modify as needed.

## Use Cases

- **Email attachments**: Split large PDFs to meet email size limits
- **Batch processing**: Divide documents into manageable chunks
- **Document organization**: Separate chapters or sections
- **Storage optimization**: Create smaller files for easier handling
- **Printing**: Split into printer-friendly page counts

## Contributing

Contributions welcome! Feel free to submit issues or pull requests.
