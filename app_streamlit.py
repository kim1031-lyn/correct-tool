import streamlit as st
from text_analyzer import analyze_text
from audio_corrector import correct_audio

st.title('AI英语朗读纠音助手')

st.header('智能备课（文本分析）')
text = st.text_area('输入英文文本')
if st.button('分析文本'):
    result = analyze_text(text)
    st.write(result)

st.header('智能批改（音频/视频分析）')
audio_file = st.file_uploader('上传音频/视频', type=['wav', 'mp3', 'mp4'])
original_text = st.text_area('输入原文')
if st.button('开始批改') and audio_file:
    with open('temp_upload', 'wb') as f:
        f.write(audio_file.read())
    result = correct_audio('temp_upload', original_text)
    st.write(result)