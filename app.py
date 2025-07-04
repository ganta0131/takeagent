from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys
import importlib.util

# 環境変数の読み込み
load_dotenv()



# test_all.pyを直接インポート
spec = importlib.util.spec_from_file_location("test_all", "test_all.py")
test_all = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_all)

def generate_text():
    return test_all.generate_text()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        text = generate_text()
        
        # synthesize_speech.pyから音声合成関数をインポート
        from synthesize_speech import synthesize_speech
        
        # 音声ファイルをstaticディレクトリに保存
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        
        audio_file = os.path.join(static_dir, 'output.mp3')
        synthesize_speech(text, audio_file)
        
        # 音声ファイルのパスを相対パスに変換
        relative_path = os.path.relpath(audio_file, os.path.dirname(os.path.abspath(__file__)))
        
        return jsonify({
            'status': 'success',
            'text': text,
            'audio_file': relative_path
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
