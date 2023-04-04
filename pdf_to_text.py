import sys
import fitz  # PyMuPDF库
from typing import List
from utils import query_gpt, remove_pdf_line_breaks
import openai
import os 
import re 
# from openai import GPT4


def read_pdf_pages(pdf_file: str, start_page: int, end_page: int) -> List[str]:
    # page number are 1-indexed
    start_page-=1
    end_page-=1
    

    doc = fitz.open(pdf_file)
    pages = []

    for page_num in range(start_page, end_page + 1):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        pages.append(text)

    doc.close()

    return pages

def remove_footnotes(text: str) -> str:
    # 匹配脚注，例如 ".5–7" 或 ",3"，确保只在句号或逗号之后匹配数字
    footnote_pattern = r"(?<=[.,])\s?\d+(?:–\d+)?(?:,\s?\d+(?:–\d+)?)*"
    cleaned_text = re.sub(footnote_pattern, "", text)
    return cleaned_text

def remove_hyphens(text: str, inline=True) -> str:
    # 匹配换行时的连字符
    hyphen_pattern = r"-\s*" if inline else r"-\n\s*"
    cleaned_text = re.sub(hyphen_pattern, "", text)
    return cleaned_text

def clean_text(text: str, use_GPT=False) -> str:
    prompt='''
    The following text is from a page of a PDF.
    It may contain hard line break and line break connectors. 
    Please remove them.'''
    # prompt+="And return as markdown format. Note, please do not add any figure or table."
    sample_text = '''
Here is a sample page of a PDF:
---
1. Design and Nomenclature of Contact Lenses
3
Figure 1.2. Reverse geometry lens design.
but contains no water. The general categories of gas permeable mate-
rials are:
1. Cellulose acetate butyrate
2. Pure silicone
3. Silicone acrylate (siloxymethacrylate copolymer)
4. Fluorocarbonate (ﬂuoromethacrylate siloxy copolymer)
3. What is the design of a single-cut lens?
The anterior surface of a single-cut contact lens is a continual curvature,
the front optic zone radius, associated with the anterior optic zone.
The posterior surface of a tricurve lens is formed of three or more
curves:
1. The central posterior curve, or base curve, is designed to ﬁt the cur-
vature of the cornea.
2. The secondary posterior curve provides a transition between the
base curve and the peripheral posterior curve. Multicurve contact
lenses may have more than one intermediate posterior curve in order
to create a gradual transition.
3. A peripheral (tertiary) curve is designed to create a smooth transi-
tion between the base curve and the edge of the lens, facilitating the
exchange of tear ﬁlm under the lens with each blink.
4. What is a ‘‘blend,’’ and what is
its importance?
To smooth the junction between adjacent curves on the back surface of
a lens, blending is performed. A blend does not induce a new curve on
the posterior surface of a lens. Blending is a smoothing of these different
curves at their junctions, removing the rigidly demarcated zones of
transition to permit better exchange of tear ﬁlm under the lens.
5. What are the types of edge design
and what are their purposes?
The shape of the outermost portion (�0.2 mm in from the edge) of the
lens is referred to as the edge contour. It is difﬁcult to quantify, so
---
You should return the following text:
---
but contains no water. The general categories of gas permeable materials are:
1. Cellulose acetate butyrate
2. Pure silicone
3. Silicone acrylate (siloxymethacrylate copolymer)
4. Fluorocarbonate (ﬂuoromethacrylate siloxy copolymer)

3. What is the design of a single-cut lens?

The anterior surface of a single-cut contact lens is a continual curvature,
the front optic zone radius, associated with the anterior optic zone.
The posterior surface of a tricurve lens is formed of three or more
curves:

1. The central posterior curve, or base curve, is designed to ﬁt the cur-
vature of the cornea.
2. The secondary posterior curve provides a transition between the
base curve and the peripheral posterior curve. Multicurve contact
lenses may have more than one intermediate posterior curve in order
to create a gradual transition.
3. A peripheral (tertiary) curve is designed to create a smooth transi-
tion between the base curve and the edge of the lens, facilitating the
exchange of tear ﬁlm under the lens with each blink.

4. What is a "blend," and what is its importance?

To smooth the junction between adjacent curves on the back surface of
a lens, blending is performed. A blend does not induce a new curve on
the posterior surface of a lens. Blending is a smoothing of these different
curves at their junctions, removing the rigidly demarcated zones of
transition to permit better exchange of tear ﬁlm under the lens.

5. What are the types of edge design and what are their purposes?

The shape of the outermost portion (≈0.2 mm in from the edge) of the
lens is referred to as the edge contour. It is difﬁcult to quantify, so
---
'''

    # input_text=prompt+sample_text+f"\nHere are the text to be convert:\n---{text}\n---"
    input_text=prompt+f"\nHere are the text to be convert:\n---{text}\n---"
    if use_GPT:
        cleaned_text = query_gpt(input_text)
        cleaned_text = remove_hyphens(cleaned_text, inline=False)
        cleaned_text = remove_footnotes(cleaned_text)
    else:
        cleaned_text = text
        cleaned_text = remove_pdf_line_breaks(cleaned_text)
        cleaned_text = remove_hyphens(cleaned_text)
        cleaned_text = remove_footnotes(cleaned_text)
    
    return cleaned_text




def save_to_txt(text: str, output_file: str) -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)


def main(pdf_file: str, start_page: int, end_page: int, output_file: str, use_GPT=False) -> None:
    raw_pages = read_pdf_pages(pdf_file, start_page, end_page)
    cleaned_pages = [clean_text(page,use_GPT=use_GPT) for page in raw_pages]
    final_text = "\n".join(cleaned_pages)
    final_raw_text = "\n".join(raw_pages)
    # save_to_txt(final_raw_text, "test_pdf/test_raw.txt")
    save_to_txt(final_text, output_file)


if __name__ == "__main__":
    # pdf_file = sys.argv[1]
    # start_page = int(sys.argv[2])
    # end_page = int(sys.argv[3])
    # output_file = sys.argv[4]
    openai.api_key=os.environ['OPENAI_API_KEY']
    pdf_file="test_pdf/test2.pdf"
    start_page=2
    end_page=3
    output_file="test_pdf/test.txt"

    main(pdf_file, start_page, end_page, output_file)
