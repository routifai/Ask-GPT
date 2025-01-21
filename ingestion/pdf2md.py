from pathlib import Path
from markitdown import MarkItDown

def convert_pdf_to_markdown(pdf_path, output_md_path):
    """Converts a PDF file to a Markdown file."""
    try:
        print(f"Processing PDF: {pdf_path}")
        md_converter = MarkItDown()
        result = md_converter.convert(pdf_path)

        if result is None:
            print(f"Failed to convert PDF: {pdf_path}. MarkItDown returned None.")
            return None

        # Save the Markdown text to a file
        with open(output_md_path, "w") as f:
            f.write(result.text_content)

        print(f"Markdown file created: {output_md_path}")
        return result.text_content
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def main():
    # Define the input PDFs and their corresponding output Markdown files
    pdf_files = [
        {"pdf_path": "./data/taxgpt/raw/i1040gi.pdf", "output_md_path": "./data/taxgpt/processed/i1040gi.md"},
        {"pdf_path": "./data/taxgpt/raw/usc26118-78.pdf", "output_md_path": "./data/taxgpt/processed/usc26118-78.md"}
    ]

    for file_pair in pdf_files:
        pdf_path = file_pair["pdf_path"]
        output_md_path = file_pair["output_md_path"]

        # Convert each PDF and handle errors gracefully
        markdown_text = convert_pdf_to_markdown(pdf_path, output_md_path)
        if markdown_text is None:
            print(f"Skipping file due to conversion failure: {pdf_path}")

if __name__ == "__main__":
    main()
