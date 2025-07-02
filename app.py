from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os
import requests
import json

# Flaskアプリケーションの作成
app = Flask(__name__)

# 環境変数の設定
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# データ保存用ディレクトリ作成
if not os.path.exists('data'):
    os.makedirs('data')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/admin')
def admin():
    return app.send_static_file('admin.html')

@app.route('/api/morning-message')
def get_morning_message():
    try:
        # 天気情報取得
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q=Tokyo&appid={OPENWEATHER_API_KEY}&lang=ja&units=metric"
        
        try:
            weather_response = requests.get(weather_url, timeout=10)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            
            # 天気データの構造を確認
            if 'weather' in weather_data and 'main' in weather_data:
                weather = weather_data['weather'][0].get('description', '情報取得中...')
                temp = round(weather_data['main'].get('temp', 0))
            else:
                print("Invalid weather API response format")
                weather = '情報取得中...'
                temp = 0
        except requests.exceptions.RequestException as e:
            print("Weather API Error:", str(e))
            weather = '情報取得中...'
            temp = 0
            
        # リマインド取得
        try:
            with open('data/reminders.json', 'r', encoding='utf-8') as f:
                reminders = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            reminders = []
        
        # 今日のリマインド
        today_reminders = [r["message"] for r in reminders if r["date"] == datetime.now().strftime("%Y-%m-%d")]
        
        # メッセージ作成
        message = f"こんにちは！たけるくん！\n\n"
        message += f"今日の天気は{weather}で、気温は{temp}度です。\n"
        
        if today_reminders:
            message += "\n今日のリマインド：\n"
            message += "\n".join(today_reminders)
        
        message += "\n今日も頑張ろうね！"
        
        return jsonify({
            "message": message,
            "weather": weather,
            "temperature": temp,
            "reminders": today_reminders
        })
    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            "error": "エラーが発生しました",
            "weather": "情報取得中...",
            "temperature": 0,
            "reminders": []
        }), 500
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
