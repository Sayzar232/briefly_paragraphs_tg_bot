import requests
from bs4 import BeautifulSoup

def get_html_content(url: str) -> str | None:
    """Get html content from url"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None
    return None


def extract_paragraphs(url: str) -> list:
    """Extract paragraphs from url"""
    html_content = get_html_content(url)
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'lxml')
    container = soup.find('div', class_="panel-search-filter")
    if not container:
        return []

    book_pages = container.find("ul", class_="book-pages")
    if not book_pages:
        return []

    paragraphs = book_pages.find_all("a")
    return [i.text.strip() for i in paragraphs if i.text]


def get_paragraphs(paragraph_number, book) -> bytes:
    """Get paragraphs from url"""
    image_url = f"https://gdzbakulin.ru/content/uploads/decision/{book}/{paragraph_number}.jpg"

    return download_image(image_url)


def download_image(url: str) -> bytes | None:
    """Return bytes of downloaded image from url"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
    except requests.RequestException:
        return None
    return None