from pdf_to_text import main as pt 
import streamlit as st
import tempfile
import os
import openai

def main():
    st.title("PDF to Text")
    pdf_file=st.file_uploader("Upload a PDF file", type=["pdf"])
    col1,col2=st.columns(2)
    use_GPT=col1.radio("Use GPT?", ["Yes", "No"],index=1)=="Yes"
    if use_GPT:
        info_text='''
        GPT can produce text that is cleaner and more organized, requiring fewer manual modifications. 
        However, this may come at the cost of $ and cost of slower processing speed.
        You need to provide an OpenAI API Key to use GPT. You can get one from https://beta.openai.com/.
        '''
        
    else:
        info_text='''
        Regular expressions will be utilized to process the text instead of GPT. Although this method is faster, it may not identify certain formatting or word irregularities and may necessitate manual processing.
        '''
    col2.info(info_text)
    
    if use_GPT:
        open_ai_api_key=st.text_input("OpenAI API Key", value="", type="password")
    col1,col2=st.columns(2)
    start_page=col1.number_input("Start Page", value=1, min_value=1, max_value=1000)
    end_page=col2.number_input("End Page", value=1, min_value=1, max_value=1000)
    convert_button=st.button("Convert to Text")

    if use_GPT and (open_ai_api_key is not None):
        openai.api_key = open_ai_api_key or os.environ['OPENAI_API_KEY']
    if pdf_file is not None:
        pdf_file_name = tempfile.NamedTemporaryFile(delete=False)
        with open(pdf_file_name.name, "wb") as f:
            f.write(pdf_file.getbuffer())
        output_filename=pdf_file.name.split(".")[0]+".txt"
    if convert_button:
        with st.spinner("Converting to Text..."):
            # main(pdf_file, start_page, end_page, output_file)
            pt(pdf_file_name.name, start_page, end_page, output_filename, use_GPT)
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