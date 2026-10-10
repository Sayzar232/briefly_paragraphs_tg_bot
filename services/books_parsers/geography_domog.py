from database import db
from ..pdf_service import PDFParser
import re
from pathlib import Path
import asyncio

# Строка, оканчивающаяся на один из этих знаков, — предложение, а не заголовок.
_TITLE_STOP_PUNCTUATION = (".", "!", "?", ";", ":")
# Некоторые заголовки занимают 2–3 строки — собираем не больше этого.
_TITLE_MAX_LINES = 4


def get_title_geography(page_text: str) -> str | None:
    """Заголовок параграфа географии: строки над рубрикой «Вспомните».

    Строки собираются снизу вверх, пока они похожи на заголовок: не
    заканчиваются на знак предложения, не являются колонтитулом (капс),
    номером страницы или пустой строкой.
    """
    lines = page_text.split("\n")
    marker_index = next(
        (i for i, line in enumerate(lines) if line.strip().lower() == "вспомните"),
        None,
    )
    if marker_index is None or marker_index == 0:
        return None

    title_lines: list[str] = []
    for line in reversed(lines[:marker_index]):
        text = line.strip()
        if (
            not any(char.isalnum() for char in text)  # пустая строка или «…»
            or text.isdigit()  # номер страницы
            or text.isupper()  # колонтитул вида «ГЕОГРАФИЯ»
            or text.endswith(_TITLE_STOP_PUNCTUATION)
            or re.match(r"^\d+[.)]", text)  # пункт списка вида «1. ...»
        ):
            break
        title_lines.append(text)
        if len(title_lines) >= _TITLE_MAX_LINES:
            break

    title = " ".join(reversed(title_lines)).strip("… ").strip()
    return title or None


async def main() -> None:
    await db.initialize()

    parser = PDFParser(
        file_path=str(Path(__file__).resolve().parent.parent.parent / "books/geography.pdf"),
        grade=9,
        subject="Geography",
        authors="Домогацких Е.М., Алексеевский Н.И.",
        edition="2019",
        url="https://example.com/geography",
        check_paragraph_func=lambda text: text.strip().lower() == "вспомните",
        title_func=get_title_geography,
    )
    paragraphs = await parser.run()
    print(f"Parsed {len(paragraphs)} paragraphs from {parser.file_path}")


if __name__ == "__main__":
    asyncio.run(main())