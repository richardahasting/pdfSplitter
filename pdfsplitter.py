#!/usr/bin/env python3
"""
PDF Splitter - Split PDF files into multiple smaller files

Usage:
    python pdfsplitter.py input.pdf --pages 10        # Split into 10-page files (default)
    python pdfsplitter.py input.pdf --files 5         # Split into 5 equal files
    python pdfsplitter.py input.pdf --pages 20 -o output_dir/
"""

import argparse
import math
import os
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def split_by_pages(input_path, pages_per_file, output_dir):
    """
    Split PDF into files with N pages each.

    Args:
        input_path: Path to input PDF file
        pages_per_file: Number of pages per output file
        output_dir: Directory to save output files

    Returns:
        List of created file paths
    """
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    if total_pages == 0:
        raise ValueError("PDF file has no pages")

    num_files = math.ceil(total_pages / pages_per_file)
    output_files = []

    # Get base name without extension
    base_name = Path(input_path).stem

    for i in range(num_files):
        writer = PdfWriter()

        # Calculate page range for this file
        start_page = i * pages_per_file
        end_page = min(start_page + pages_per_file, total_pages)

        # Add pages to this file
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])

        # Create output filename with zero-padded numbering
        output_filename = f"{base_name}_part_{i+1:03d}.pdf"
        output_path = Path(output_dir) / output_filename

        # Write the output file
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        output_files.append(output_path)
        print(f"Created: {output_path} (pages {start_page + 1}-{end_page})")

    return output_files


def split_by_num_files(input_path, num_files, output_dir):
    """
    Split PDF into N equal files.

    Args:
        input_path: Path to input PDF file
        num_files: Number of output files to create
        output_dir: Directory to save output files

    Returns:
        List of created file paths
    """
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    if total_pages == 0:
        raise ValueError("PDF file has no pages")

    if num_files > total_pages:
        raise ValueError(f"Cannot split {total_pages} pages into {num_files} files. "
                        f"Number of files must be <= number of pages.")

    # Calculate pages per file (distribute evenly)
    pages_per_file = total_pages / num_files
    output_files = []

    # Get base name without extension
    base_name = Path(input_path).stem

    for i in range(num_files):
        writer = PdfWriter()

        # Calculate page range for this file (ensures even distribution)
        start_page = int(i * pages_per_file)
        end_page = int((i + 1) * pages_per_file) if i < num_files - 1 else total_pages

        # Add pages to this file
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])

        # Create output filename with zero-padded numbering
        output_filename = f"{base_name}_part_{i+1:03d}.pdf"
        output_path = Path(output_dir) / output_filename

        # Write the output file
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        output_files.append(output_path)
        print(f"Created: {output_path} (pages {start_page + 1}-{end_page})")

    return output_files


def main():
    """Main entry point for the PDF splitter."""
    parser = argparse.ArgumentParser(
        description='Split PDF files into multiple smaller files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.pdf                           # Split into 10-page files (default)
  %(prog)s input.pdf --pages 20                # Split into 20-page files
  %(prog)s input.pdf --files 5                 # Split into 5 equal files
  %(prog)s input.pdf --pages 10 -o output/     # Specify output directory
        """
    )

    parser.add_argument('input', help='Input PDF file path')
    parser.add_argument('-o', '--output-dir', default='.',
                       help='Output directory for split files (default: current directory)')

    # Mutually exclusive group for splitting modes
    split_group = parser.add_mutually_exclusive_group()
    split_group.add_argument('--pages', type=int, default=10,
                            help='Number of pages per output file (default: 10)')
    split_group.add_argument('--files', type=int,
                            help='Number of output files to create')

    args = parser.parse_args()

    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        return 1

    if not input_path.is_file():
        print(f"Error: '{args.input}' is not a file", file=sys.stderr)
        return 1

    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Determine splitting mode and execute
        if args.files:
            print(f"Splitting '{input_path.name}' into {args.files} files...")
            output_files = split_by_num_files(args.input, args.files, output_dir)
        else:
            print(f"Splitting '{input_path.name}' into files with {args.pages} pages each...")
            output_files = split_by_pages(args.input, args.pages, output_dir)

        print(f"\nSuccess! Created {len(output_files)} files in '{output_dir}'")
        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
