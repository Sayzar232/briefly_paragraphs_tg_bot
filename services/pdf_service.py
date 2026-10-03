import pypdf


class Paragraph:
    def __init__(self, pages: list, start_page: int, end_page: int, paragraph_number: int):
        self.pages = pages
        self.text = "\n".join(pages)
        self.start_page = start_page
        self.end_page = end_page
        self.paragraph_number = paragraph_number


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
        self.pages_content = []
        self.text = self.get_text()

        self.save_text_to_file(f"{self.file_path}.txt")  # Save extracted text to a file
        self.split_by_paragraphs()  # Split the text into paragraphs and save to a file

    def get_text(self) -> str:
        """Extract text from PDF file"""
        text = ""
        for num, page in enumerate(self.pdf_reader.pages):
            text += f"PDFPARSER: Page {num + 1}\n"
            page_text = page.extract_text()
            text += page_text + "\n"
            self.pages_content.append(page_text)
            print(f"Page {num + 1} text extracted")

        return text

    def save_text_to_file(self, output_file: str):
        """Save extracted text to a file"""
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(self.text)
        print(f"Extracted text saved to {output_file}")

    def check_last_paragraph(self, num, start_page, paragraph_number) -> bool:
        if num >= len(self.pages_content) - 1:
            pages_num = num + 1 - start_page
            if pages_num > 10:
                paragraph = Paragraph(
                    pages=self.pages_content[start_page - 1:start_page + 10],
                    start_page=start_page,
                    end_page=start_page + 10,
                    paragraph_number=paragraph_number
                )
            else:
                paragraph = Paragraph(
                    pages=self.pages_content[start_page - 1:num],
                    start_page=start_page,
                    end_page=num + 1,
                    paragraph_number=paragraph_number
                )
            return paragraph
        return None

    def split_by_paragraphs(self) -> list:
        """Split the extracted text into paragraphs"""
        paragraphs = []
        start_page = 1
        paragraph_number = 1
        for num, page in enumerate(self.pages_content):
            for i in page.split("\n"):
                if i.strip().lower() == "вспомните":
                    paragraph = Paragraph(
                        pages=self.pages_content[start_page - 1:num + 1],
                        start_page=start_page,
                        end_page=num + 1,
                        paragraph_number=paragraph_number
                    )
                    paragraphs.append(paragraph)
                    start_page = num + 1
                    paragraph_number += 1
                    break
            if paragraph := self.check_last_paragraph(num, start_page, paragraph_number):
                paragraphs.append(paragraph)
                break

        return paragraphs


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