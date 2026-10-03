import pypdf

class PDFParser:
    def __init__(
            self, 
            file_path: str,
            grade: int,
            subject: str,
            authors: str,
            publisher: str,
            edition: str,
            url: str
        ):
        self.file_path = file_path
        self.pdf_reader = pypdf.PdfReader(file_path)
        self.grade = grade
        self.subject = subject
        self.authors = authors
        self.publisher = publisher
        self.edition = edition
        self.url = url
        self.pages = len(self.pdf_reader.pages)
        self.text = self.get_text()

        self.save_text_to_file(f"{self.file_path}.txt")  # Save extracted text to a file

    def get_text(self) -> str:
        """Extract text from PDF file"""
        text = ""
        for num, page in enumerate(self.pdf_reader.pages):
            text += f"PDFPARSER: Page {num + 1}\n"
            text += page.extract_text() + "\n"
            print(f"Page {num + 1} text extracted")

        return text

    def save_text_to_file(self, output_file: str):
        """Save extracted text to a file"""
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(self.text)
        print(f"Extracted text saved to {output_file}")

    def split_by_paragraphs(self) -> list:
        """Split the extracted text into paragraphs"""
        pass

if __name__ == "__main__":
    # Example usage
    pdf_parser = PDFParser(
        file_path="geography.pdf",
        grade=9,
        subject="Geography",
        authors="Author Name",
        publisher="Publisher Name",
        edition="2019",
        url="https://example.com/geography"
    )
    print(f"Extracted text from {pdf_parser.file_path}")