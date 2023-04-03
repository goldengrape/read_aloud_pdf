import edge_tts
import asyncio
import streamlit as st
from utils import LANGUAGES_dict
import os

def main():
    async def tts(text, VOICE,OUTPUT_FILE,WEBVTT_FILE) -> None:
        communicate = edge_tts.Communicate(text, VOICE)
        submaker= edge_tts.SubMaker()
        # await communicate.save(OUTPUT_FILE)
        with open(OUTPUT_FILE, "wb") as file:
            async for chunk in communicate.stream():
                # print(chunk['type'])
                if chunk['type']=='audio':
                    file.write(chunk['data'])
                elif chunk['type']=='WordBoundary':
                    submaker.create_sub(
                        (chunk['offset'], chunk['duration']),
                        chunk['text']
                    )
        with open(WEBVTT_FILE, "w",encoding="utf-8") as file:
            file.write(submaker.generate_subs())
            print("WebVTT file saved to", WEBVTT_FILE)

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
        WEBVTT_FILE = text_file.name.split(".")[0]+".vtt"
    if convert_button:
        with st.spinner("Converting to Speech..."):
            asyncio.run(tts(text, VOICE,OUTPUT_FILE,WEBVTT_FILE))
        download_audio_button=st.download_button(
            label="Download Audio",
            data=open(OUTPUT_FILE, "rb").read(),
            file_name=OUTPUT_FILE,
        )
        download_sub_button=st.download_button(
            label="Download Subtitles",
            data=open(WEBVTT_FILE, "r").read(),
            file_name=WEBVTT_FILE,
        )
        if download_audio_button:
            # 清除临时文件
            os.remove(OUTPUT_FILE)
        if download_sub_button:
            # 清除临时文件
            os.remove(WEBVTT_FILE)
if __name__ == "__main__":
    main()