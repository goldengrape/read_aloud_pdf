import sys
import fitz  # PyMuPDF库
from typing import List
# from openai import GPT4


def read_pdf_pages(pdf_file: str, start_page: int, end_page: int) -> List[str]:
    doc = fitz.open(pdf_file)
    pages = []

    for page_num in range(start_page, end_page + 1):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        pages.append(text)

    doc.close()

    return pages


def clean_text(text: str) -> str:
    prompt=""
    cleaned_text = GPT4.clean_text(text)
    return cleaned_text


def save_to_txt(text: str, output_file: str) -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)


def main(pdf_file: str, start_page: int, end_page: int, output_file: str) -> None:
    raw_pages = read_pdf_pages(pdf_file, start_page, end_page)
    cleaned_pages = [clean_text(page) for page in raw_pages]
    final_text = "\n".join(cleaned_pages)
    save_to_txt(final_text, output_file)


if __name__ == "__main__":
    pdf_file = sys.argv[1]
    start_page = int(sys.argv[2])
    end_page = int(sys.argv[3])
    output_file = sys.argv[4]

    main(pdf_file, start_page, end_page, output_file)
