# AI英语朗读纠音助手

## 项目简介
本项目是一款面向小学英语教师的AI辅助纠音工具，支持文本智能分析、音视频智能批改、个性化发音报告等功能，极大提升教师工作效率。

## 技术栈
- 前端：HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- 后端：Python 3.9+, Flask, Flask-CORS, NLTK, CMUdict, FFmpeg, Whisper, difflib, SQLite3, Montreal Forced Aligner

## 目录结构
```
/ai_teacher_assistant/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── services/
│   │   ├── text_analyzer.py
│   │   └── audio_corrector.py
│   ├── uploads/
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   └── assets/
│       ├── css/style.css
│       └── js/main.js
└── README.md
```

## 主要功能
- 智能备课：文本分析、难点高亮
- 智能批改：音频/视频转文本、发音纠错
- 个性化报告：错词、漏词、发音建议 