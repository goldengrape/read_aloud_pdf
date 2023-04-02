from pdf_to_text import main as pt 
import streamlit as st
import tempfile
import os
import openai

def main():
    st.title("PDF to Text")
    pdf_file=st.file_uploader("Upload a PDF file", type=["pdf"])

    open_ai_api_key=st.text_input("OpenAI API Key", value="", type="password")
    col1,col2=st.columns(2)
    start_page=col1.number_input("Start Page", value=1, min_value=1, max_value=1000)
    end_page=col2.number_input("End Page", value=1, min_value=1, max_value=1000)
    convert_button=st.button("Convert to Text")

    if open_ai_api_key:
        openai.api_key = open_ai_api_key or os.environ['OPENAI_API_KEY']
    if pdf_file is not None:
        pdf_file_name = tempfile.NamedTemporaryFile(delete=False)
        with open(pdf_file_name.name, "wb") as f:
            f.write(pdf_file.getbuffer())
        output_filename=pdf_file.name.split(".")[0]+".txt"
    if convert_button:
        with st.spinner("Converting to Text..."):
            # main(pdf_file, start_page, end_page, output_file)
            pt(pdf_file_name.name, start_page, end_page, output_filename)
        download_button=st.download_button(
            label="Download Text",
            data=open(output_filename, "rb").read(),
            file_name=output_filename,
        )
        if download_button:
            # 清除临时文件
            os.remove(pdf_file_name.name)
            os.remove(output_filename)
if __name__ == "__main__":
    main()