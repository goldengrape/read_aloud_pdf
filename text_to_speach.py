import edge_tts
import asyncio
import streamlit as st
from utils import LANGUAGES_dict

def main():
    async def tts(text, VOICE) -> None:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(OUTPUT_FILE)
    async def voice_selector(Language='en'):
        voices = await edge_tts.VoicesManager.create()
        voice = voices.find(Language=Language)
        return voice

    st.title("Text to Speech")
    text_file=st.file_uploader("Upload a text file", type=["txt"])
    
    # gender=st.selectbox("Voice Gender",["Male","Female"], index=1)
    language=st.selectbox("Voice Language",LANGUAGES_dict.keys(), index = 0)
    
    voice_list=asyncio.run(voice_selector(Language=LANGUAGES_dict[language]))
    voice_list=[voice['ShortName'] for voice in voice_list]
    
    try:
        voice_index=voice_list.index('en-GB-SoniaNeural')
    except:
        voice_index=0 

    VOICE=st.selectbox("Select a voice", 
                    voice_list,
                    index=voice_index
                    )
    convert_button=st.button("Convert to Speech")
    if text_file is not None:
        text=text_file.read().decode("utf-8")
        OUTPUT_FILE = text_file.name.split(".")[0]+".mp3"
    if convert_button:
        with st.spinner("Converting to Speech..."):
            asyncio.run(tts(text, VOICE))
        download_button=st.download_button(
            label="Download Audio",
            data=open(OUTPUT_FILE, "rb").read(),
            file_name=OUTPUT_FILE,
        )

if __name__ == "__main__":
    main()