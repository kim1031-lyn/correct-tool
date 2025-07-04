document.getElementById('analyze-btn').onclick = async function() {
    const text = document.getElementById('text-input').value;
    const res = await fetch('/api/text_analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });
    const data = await res.json();
    let html = '<b>难点单词:</b><br>';
    for (const [word, reasons] of Object.entries(data.difficult_words || {})) {
        html += `${word}: ${reasons.join('，')}<br>`;
    }
    html += '<b>知识点:</b><br>';
    for (const [point, words] of Object.entries(data.knowledge_points || {})) {
        html += `${point}: ${words.join('，')}<br>`;
    }
    document.getElementById('text-analysis-result').innerHTML = html;
};

document.getElementById('correct-btn').onclick = async function() {
    const fileInput = document.getElementById('audio-file');
    const originalText = document.getElementById('original-text').value;
    if (!fileInput.files.length) return alert('请上传音频或视频文件');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('original_text', originalText);
    const res = await fetch('/api/audio_correction', {
        method: 'POST',
        body: formData
    });
    const data = await res.json();
    let html = `<b>原文:</b> ${data.original_text}<br><b>识别:</b> ${data.recognized_text}<br><b>批改:</b><br>`;
    for (const [type, words] of Object.entries(data.errors || {})) {
        html += `${type}: ${words.join('，')}<br>`;
    }
    if (data.mfa) {
        html += '<b>MFA发音分析:</b><br>';
        if (data.mfa.mfa_error) {
            html += `MFA错误: ${data.mfa.mfa_error}<br>`;
        } else {
            html += JSON.stringify(data.mfa, null, 2);
        }
    }
    document.getElementById('audio-correction-result').innerHTML = html;
};