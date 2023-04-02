from replace_abbrevation import main as ra 
import streamlit as st 
import tempfile

st.title("Replace Abbrevations")

text_file=st.file_uploader("Upload a text file", type=["txt"])
if text_file is not None:
    text=text_file.read().decode("utf-8")

sample_abbr_file=st.download_button(
    label="Download Sample Abbreviation Replacement Table",
    data=open("Abbreviation_Replacement_Table.csv", "r").read(),
    file_name="Abbreviation_Replacement_Table.csv",
)

abbreviation_file = st.file_uploader("Upload the Abbreviation Replacement Table file", type=["csv"])
if abbreviation_file is not None:
    abbreviation_file_name = tempfile.NamedTemporaryFile(delete=False)
    with open(abbreviation_file_name.name, "w",encoding='utf-8') as f:
        abbr_content = abbreviation_file.read().decode("utf-8")
        abbr_content = abbr_content.replace('\r\n', '\n').replace('\r', '\n')  # Ensure consistent line endings
        f.write(abbr_content)

convert_button=st.button("Replace Abbrevations")
if convert_button:
    with st.spinner("Replacing Abbrevations"):
        cleaned_text = ra(text, abbreviation_file_name.name)
    download_button=st.download_button(
        label="Download Cleaned Text",
        data=cleaned_text.encode("utf-8"),
        file_name=text_file.name.split(".")[0]+"_cleaned.txt",
    )