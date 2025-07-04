from flask import Flask, request, jsonify, session
from flask_cors import CORS
from models import db, User
from text_analyzer import analyze_text
from audio_corrector import correct_audio
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/api/text_analysis', methods=['POST'])
def text_analysis():
    data = request.get_json()
    text = data.get('text', '')
    result = analyze_text(text)
    return jsonify(result)

@app.route('/api/audio_correction', methods=['POST'])
def audio_correction():
    file = request.files['file']
    original_text = request.form.get('original_text', '')
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    result = correct_audio(filepath, original_text)
    return jsonify(result)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': '注册成功'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify({'message': '登录成功'})
    return jsonify({'error': '用户名或密码错误'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': '已登出'})

if __name__ == '__main__':
    app.run(debug=True)