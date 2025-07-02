from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os
from dotenv import load_dotenv
import requests
from google.cloud import texttospeech
from google.cloud import vision
import json

# Flaskアプリケーションの作成
app = Flask(__name__)

# 環境変数の読み込み
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    print(".envファイルが見つかりません")

# 環境変数の確認
api_key = os.getenv('OPENWEATHER_API_KEY')
if not api_key:
    print("環境変数が設定されていません。以下のコマンドで設定してください：")
    print("$env:OPENWEATHER_API_KEY='757b8b551ef58f6ed9e8734408438347'")
    raise ValueError("OPENWEATHER_API_KEYが設定されていません")

# データ保存用ディレクトリ作成
if not os.path.exists('data'):
    os.makedirs('data')

# データ保存用ディレクトリ作成
if not os.path.exists('data'):
    os.makedirs('data')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/morning-message')
def get_morning_message():
    try:
        # 天気情報取得
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q=Tokyo&appid={os.getenv('OPENWEATHER_API_KEY')}&lang=ja&units=metric"
        
        try:
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()
            
            # レスポンスの確認
            if weather_response.status_code == 200:
                # 正常なレスポンスの場合
                weather_data = {
                    'weather': [{'description': weather_data['weather'][0]['description']}],
                    'main': {'temp': round(weather_data['main']['temp'])}
                }
            else:
                print("Weather API Error:", weather_data.get('message', 'Unknown error'))
                weather_data = {
                    'weather': [{'description': '情報取得中...'}],
                    'main': {'temp': 0}
                }
        except Exception as e:
            print("Weather API Error:", str(e))
            weather_data = {
                'weather': [{'description': '情報取得中...'}],
                'main': {'temp': 0}
            }
        
        # リマインド取得
        with open('data/reminders.json', 'r', encoding='utf-8') as f:
            reminders = json.load(f)
        
        # 今日のリマインド
        today_reminders = [r["message"] for r in reminders if r["date"] == datetime.now().strftime("%Y-%m-%d")]
        
        # メッセージ作成
        message = f"こんにちは！たけるくん！\n\n"
        message += f"今日の天気は{weather_data['weather'][0]['description']}で、気温は{weather_data['main']['temp']}度です。\n"
        
        if today_reminders:
            message += "\n今日のリマインド：\n"
            message += "\n".join(today_reminders)
        
        message += "\n今日も頑張ろうね！"
        
        return jsonify({
            "message": message,
            "weather": weather_data['weather'][0]['description'],
            "temperature": weather_data['main']['temp'],
            "reminders": today_reminders
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/set-reminder', methods=['POST'])
def set_reminder():
    try:
        data = request.json
        today = datetime.now().strftime("%Y-%m-%d")
        
        # リマインドデータを保存
        if not os.path.exists('data/reminders.json'):
            with open('data/reminders.json', 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
        
        with open('data/reminders.json', 'r', encoding='utf-8') as f:
            reminders = json.load(f)
        
        reminders.append({
            "date": today,
            "message": data['message']
        })
        
        with open('data/reminders.json', 'w', encoding='utf-8') as f:
            json.dump(reminders, f, ensure_ascii=False, indent=4)
        
        return jsonify({"message": "リマインドが設定されました"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload-schedule', methods=['POST'])
def upload_schedule():
    try:
        file = request.files['file']
        if file:
            # PDFを保存
            filename = f"schedule_{datetime.now().strftime('%Y%m')}.pdf"
            file.save(os.path.join('data', filename))
            
            # PDFからテキスト抽出
            client = vision.ImageAnnotatorClient()
            with open(os.path.join('data', filename), 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            response = client.document_text_detection(image=image)
            text = response.full_text_annotation.text
            
            # テキストをJSONに変換して保存
            schedule_data = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "text": text
            }
            with open(f"data/schedule_{datetime.now().strftime('%Y%m')}.json", 'w', encoding='utf-8') as f:
                json.dump(schedule_data, f, ensure_ascii=False, indent=4)
            
            return jsonify({"message": "スケジュールがアップロードされました"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
