import fitz
import webvtt
import re
from PIL import Image, ImageDraw
import os
from sub_PDF_location import get_time_location


def read_pdf_pages(file_path, start_page, end_page):
    pdf_document = fitz.open(file_path)
    pdf_pages = [pdf_document.load_page(i) for i in range(start_page, end_page + 1)]

    return pdf_pages

def convert_pages_to_html(pdf_pages):
    html_pages = [page.get_text("html") for page in pdf_pages]
    return html_pages

def read_vtt_file(file_path):
    return list(webvtt.read(file_path))

def find_phrases_in_html(html_pages, vtt_data, n):
    phrases_positions = []

    for caption in vtt_data:
        words = caption.text.split()
        for idx, word in enumerate(words):
            context_start = max(0, idx - n)
            context_end = min(idx + n + 1, len(words))
            phrase = ' '.join(words[context_start:context_end])

            for html_page_index, html_page in enumerate(html_pages):
                if phrase in html_page:
                    position = {
                        'phrase': phrase,
                        'page_index': html_page_index,
                        'start_index': html_page.index(phrase),
                        'end_index': html_page.index(phrase) + len(phrase),
                        'start_time': caption.start,
                        'end_time': caption.end
                    }
                    phrases_positions.append(position)
                    break
    return phrases_positions

def render_pdf_pages_with_highlight(pdf_pages, phrases_positions, highlight_color=(0, 255, 0), opacity=0.3):
    highlighted_images = []

    for position in phrases_positions:
        page = pdf_pages[position['page_index']]
        pix = page.get_pixmap()

        # Render the PDF page as an image
        image = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)

        # Create a blank image with the same size as the PDF page
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))

        # Create a highlight rectangle around the phrase
        draw = ImageDraw.Draw(overlay)
        highlight_rect = page.search_for(position['phrase'])[0]  # Get the bounding box of the phrase

        # Draw a rectangle with the highlight color
        x0, y0, x1, y1 = highlight_rect
        draw.rectangle([(x0, y0), (x1, y1)], fill=highlight_color + (int(255 * opacity),))

        # Combine the original image and the overlay
        highlighted_image = Image.alpha_composite(image, overlay)
        highlighted_images.append(highlighted_image)

    return highlighted_images

if __name__=='__main__':
    pdf_file_path = 'test_pdf/test2.pdf'
    vtt_file_path = 'test_pdf/test.vtt'
    output_file_path = 'test_pdf/output.pdf'
    n = 2  # Number of words to include in the context

    pdf_pages = read_pdf_pages(pdf_file_path, 45, 46)
    print(len(pdf_pages))
    html_pages = convert_pages_to_html(pdf_pages)
    # vtt_data = read_vtt_file(vtt_file_path)
    # phrases_positions = find_phrases_in_html(html_pages, vtt_data, n)
    # highlighted_images = render_pdf_pages_with_highlight(pdf_pages, phrases_positions)

    # # Save the highlighted images as a PDF
    # highlighted_images[0].save(output_file_path, save_all=True, append_images=highlighted_images[1:])






