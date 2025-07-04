import os
import tempfile
import difflib
import whisper
import ffmpeg

def extract_audio(input_path):
    output_path = tempfile.mktemp(suffix='.wav')
    ffmpeg.input(input_path).output(output_path, acodec='pcm_s16le', ac=1, ar='16000').run(overwrite_output=True, quiet=True)
    return output_path

def transcribe_audio(audio_path):
    model = whisper.load_model('base')
    result = model.transcribe(audio_path)
    return result['text']

def compare_texts(original, recognized):
    diff = list(difflib.ndiff(original.split(), recognized.split()))
    errors = {'错词': [], '漏词': [], '增词': []}
    for d in diff:
        if d.startswith('- '):
            errors['漏词'].append(d[2:])
        elif d.startswith('+ '):
            errors['增词'].append(d[2:])
        elif d.startswith('? '):
            continue
    return errors

def run_mfa(audio_path, transcript, user_id=None):
    import subprocess
    import json
    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.txt') as f:
        f.write(transcript)
        transcript_path = f.name
    output_dir = tempfile.mkdtemp()
    mfa_cmd = [
        'mfa_align', audio_path, transcript_path, 'english', output_dir, '--output_format', 'json'
    ]
    try:
        subprocess.run(mfa_cmd, check=True)
        for file in os.listdir(output_dir):
            if file.endswith('.json'):
                with open(os.path.join(output_dir, file), 'r', encoding='utf-8') as jf:
                    mfa_result = json.load(jf)
                return mfa_result
    except Exception as e:
        return {'mfa_error': str(e)}
    return {'mfa_error': 'MFA未生成结果'}

def correct_audio(file_path, original_text):
    audio_path = extract_audio(file_path)
    recognized_text = transcribe_audio(audio_path)
    errors = compare_texts(original_text, recognized_text)
    mfa_result = run_mfa(audio_path, original_text)
    return {
        'original_text': original_text,
        'recognized_text': recognized_text,
        'errors': errors,
        'mfa': mfa_result
    }