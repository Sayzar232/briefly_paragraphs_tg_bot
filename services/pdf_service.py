"""Разбор PDF-учебника на параграфы и сохранение их в базу данных.

Параграф начинается со строки-маркера (для географии — «Вспомните»),
которая стоит в начале первой страницы параграфа. Всё до первого
маркера — титул и предисловие — параграфом не считается.
"""

from typing import Callable

import pypdf

from database import db, Database


class Paragraph:
    """Один параграф учебника: диапазон страниц и их текст."""

    def __init__(
        self,
        pages: list[str],
        start_page: int,
        end_page: int,
        paragraph_number: int,
        book_id: int | None = None,
        title_func: Callable[[str], str | None] | None = None,
    ):
        self.pages = pages
        self.text = "\n".join(pages)
        self.start_page = start_page
        self.end_page = end_page
        self.paragraph_number = paragraph_number
        self.book_id = book_id
        self.title_func = title_func
        self.title = self.get_title()

    def get_title(self) -> str | None:
        """Заголовок параграфа — по его первой странице."""
        if self.title_func is None or not self.pages:
            return None
        return self.title_func(self.pages[0])


class PDFParser:
    """Парсер учебника: извлекает текст и разбивает его на параграфы."""

    # Максимальное число страниц в последнем (хвостовом) параграфе.
    MAX_PAGES = 10

    def __init__(
        self,
        file_path: str,
        grade: int,
        subject: str,
        authors: str,
        edition: str,
        url: str,
        check_paragraph_func: Callable[[str], bool],
        publisher: str = "Просвещение",
        title_func: Callable[[str], str | None] | None = None,
    ):
        self.file_path = file_path
        self.pdf_reader = pypdf.PdfReader(file_path)
        self.grade = grade
        self.subject = subject
        self.authors = authors
        self.publisher = publisher
        self.edition = edition
        self.url = url
        self.check_paragraph_func = check_paragraph_func
        self.title_func = title_func
        self.pages = len(self.pdf_reader.pages)
        self.pages_content: list[str] = []
        self.text: str | None = None

    def get_text(self) -> str:
        """Извлечь текст из PDF; содержимое страниц — в self.pages_content."""
        self.pages_content = []
        parts: list[str] = []

        for page_number, page in enumerate(self.pdf_reader.pages, start=1):
            page_text = page.extract_text() or ""
            self.pages_content.append(page_text)
            parts.append(f"PDFPARSER: Page {page_number}\n{page_text}\n")

        print(f"Extracted text from {len(self.pages_content)} pages")
        return "".join(parts)

    def save_text_to_file(self, output_file: str) -> None:
        """Сохранить извлечённый текст в файл."""
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(self.text or "")
        print(f"Extracted text saved to {output_file}")

    def _has_paragraph_marker(self, page_text: str) -> bool:
        """Есть ли на странице строка-маркер начала нового параграфа."""
        return any(
            self.check_paragraph_func(line)
            for line in page_text.split("\n")
        )

    def _get_tail_paragraph(
        self, page_index: int, start_page: int, paragraph_number: int
    ) -> Paragraph | None:
        """Последний параграф книги: от start_page до конца файла.

        Возвращает None, пока не дошли до последней страницы.
        """
        if page_index < len(self.pages_content) - 1:
            return None

        pages = self.pages_content[start_page - 1 : start_page - 1 + self.MAX_PAGES]
        if not pages:
            return None

        return Paragraph(
            pages=pages,
            start_page=start_page,
            end_page=start_page + len(pages) - 1,
            paragraph_number=paragraph_number,
            title_func=self.title_func,
        )

    def split_by_paragraphs(self) -> list[Paragraph]:
        """Разбить извлечённый текст на параграфы.

        Маркер стоит на первой странице нового параграфа, поэтому страница
        с маркером не входит в предыдущий параграф, а начинает следующий.
        """
        paragraphs: list[Paragraph] = []
        start_page = 1
        paragraph_number = 1
        first_marker_seen = False

        for page_index, page_text in enumerate(self.pages_content):
            if self._has_paragraph_marker(page_text):
                if first_marker_seen:
                    paragraphs.append(
                        Paragraph(
                            pages=self.pages_content[start_page - 1 : page_index],
                            start_page=start_page,
                            end_page=page_index,
                            paragraph_number=paragraph_number,
                            title_func=self.title_func,
                        )
                    )
                    paragraph_number += 1
                else:
                    # Титул и предисловие до первого маркера пропускаем.
                    first_marker_seen = True
                # Страница с маркером начинает следующий параграф.
                start_page = page_index + 1

            if tail := self._get_tail_paragraph(page_index, start_page, paragraph_number):
                paragraphs.append(tail)
                break

        return paragraphs

    async def add_to_database(self, db: Database) -> int:
        """Гарантировать наличие книги в БД и вернуть её id."""
        return await db.ensure_book(
            subject=self.subject,
            grade=self.grade,
            authors=self.authors,
            publisher=self.publisher,
            edition=self.edition,
            pages=self.pages,
            url=self.url,
        )

    async def add_paragraphs_to_database(self, paragraphs) -> int:
        """Сохранить все параграфы одним SQL-запросом. Возвращает их число."""
        return await db.add_paragraphs(paragraphs)

    async def run(self, output_file: str = "paragraphs.txt") -> list[Paragraph]:
        """Полный цикл: извлечь текст, разбить на параграфы, сохранить в БД."""
        self.text = self.get_text()
        paragraphs = self.split_by_paragraphs()

        book_id = await self.add_to_database(db)

        for paragraph in paragraphs:
            paragraph.book_id = book_id

        added = await self.add_paragraphs_to_database(paragraphs)
        print(f"{added} paragraphs added to database")

        return paragraphs