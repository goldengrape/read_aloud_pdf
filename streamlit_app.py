import streamlit as st
from pdf_to_text_streamlit import main as pdf_to_text
from replace_abbr_streamlit import main as replace_abbr
from text_to_speach import main as tts

choice={
    "PDF to Text":pdf_to_text,
    "Replace Abbrevations":replace_abbr,
    "Text to Speach":tts,
}

side_selection=st.sidebar.radio("Select a tool", list(choice.keys()))
choice[side_selection]()