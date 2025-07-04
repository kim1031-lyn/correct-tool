import nltk
nltk.download('punkt')
nltk.download('cmudict')

from text_analyzer import analyze_text
from audio_corrector import correct_audio
import streamlit as st
import shutil
import requests
import time
import os

def video_to_audio_api(video_path):
    with open(video_path, 'rb') as f:
        files = {'file': f}
        data = {'output_format': 'mp3'}
        r = requests.post('https://api.audio-convert.com/convert', files=files, data=data)
        if r.status_code == 200 and 'result_url' in r.json():
            # 轮询等待API处理完成
            for _ in range(20):
                status = requests.get(r.json()['result_url'] + '/status').json()
                if status.get('status') == 'finished':
                    audio_url = status.get('file_url')
                    audio_data = requests.get(audio_url).content
                    audio_path = video_path + '.mp3'
                    with open(audio_path, 'wb') as af:
                        af.write(audio_data)
                    return audio_path
                time.sleep(2)
    return None

st.title('AI英语朗读纠音助手')

st.header('智能备课（文本分析）')
text = st.text_area('输入英文文本')
if st.button('分析文本'):
    result = analyze_text(text)
    st.write(result)

st.header('智能批改（音频/视频分析）')
ffmpeg_exists = shutil.which('ffmpeg') is not None
if not ffmpeg_exists:
    st.warning('⚠️ 当前环境不支持 ffmpeg，视频将通过免费API自动转音频，速度较慢且有大小限制。')
    audio_file = st.file_uploader('上传音频/视频', type=['wav', 'mp3', 'mp4'])
    original_text = st.text_area('输入原文')
    if st.button('开始批改') and audio_file:
        with open('temp_upload', 'wb') as f:
            f.write(audio_file.read())
        if audio_file.type == 'video/mp4':
            st.info('正在通过免费API转码，请耐心等待...')
            audio_path = video_to_audio_api('temp_upload')
            if audio_path:
                result = correct_audio(audio_path, original_text)
                st.write(result)
                os.remove(audio_path)
            else:
                st.error('转码失败，请重试或更换文件。')
        else:
            result = correct_audio('temp_upload', original_text)
            st.write(result)
else:
    audio_file = st.file_uploader('上传音频/视频', type=['wav', 'mp3', 'mp4'])
    original_text = st.text_area('输入原文')
    if st.button('开始批改') and audio_file:
        with open('temp_upload', 'wb') as f:
            f.write(audio_file.read())
        result = correct_audio('temp_upload', original_text)
        st.write(result)