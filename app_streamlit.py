import nltk
nltk.download('punkt')
nltk.download('cmudict')

from text_analyzer import analyze_text
from audio_corrector import correct_audio
import streamlit as st
import shutil

st.title('AI英语朗读纠音助手')

st.header('智能备课（文本分析）')
text = st.text_area('输入英文文本')
if st.button('分析文本'):
    result = analyze_text(text)
    st.write(result)

st.header('智能批改（音频/视频分析）')
ffmpeg_exists = shutil.which('ffmpeg') is not None
if not ffmpeg_exists:
    st.warning('⚠️ 当前环境不支持 ffmpeg，音频/视频分析功能仅在本地部署时可用。')
else:
    audio_file = st.file_uploader('上传音频/视频', type=['wav', 'mp3', 'mp4'])
    original_text = st.text_area('输入原文')
    if st.button('开始批改') and audio_file:
        with open('temp_upload', 'wb') as f:
            f.write(audio_file.read())
        result = correct_audio('temp_upload', original_text)
        st.write(result)