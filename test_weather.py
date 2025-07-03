import requests
import json
from datetime import datetime

# OpenWeatherMap APIキー
API_KEY = '757b8b551ef58f6ed9e8734408438347'

# 愛知県江南市の緯度経度
LAT = 34.9928
LON = 136.8644

def get_weather_forecast():
    try:
        # 1週間予報APIのエンドポイント
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&lang=ja&units=metric'
        
        # APIリクエスト
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # 朝（6-9時）、昼（12-15時）、夕方（16-19時）の天気を取得
            morning_forecast = []
            afternoon_forecast = []
            evening_forecast = []
            rain_forecast = []  # 雨の予報を追跡
            
            for forecast in data['list']:
                # 時間を取得
                forecast_time = datetime.fromtimestamp(forecast['dt'])
                hour = forecast_time.hour
                
                # 雨の予報を追跡
                if '雨' in forecast['weather'][0]['description']:
                    rain_forecast.append({
                        'time': f"{hour}時",
                        'description': forecast['weather'][0]['description']
                    })
                
                if 6 <= hour < 9:  # 朝
                    morning_forecast.append(forecast)
                elif 12 <= hour < 15:  # 昼
                    afternoon_forecast.append(forecast)
                elif 16 <= hour < 19:  # 夕方
                    evening_forecast.append(forecast)
            
            # 結果を整理して表示
            print("\n天気予報テスト結果:")
            print("=======================================")
            print("- ステータス: 成功")
            
            # 朝の天気
            if morning_forecast:
                morning = morning_forecast[0]
                print("\n朝の天気（6-9時）:")
                print(f"- 天気: {morning['weather'][0]['description']}")
                print(f"- 気温: {morning['main']['temp']}°C")
            
            # 昼の天気
            if afternoon_forecast:
                afternoon = afternoon_forecast[0]
                print("\n昼の天気（12-15時）:")
                print(f"- 天気: {afternoon['weather'][0]['description']}")
                print(f"- 気温: {afternoon['main']['temp']}°C")
            
            # 夕方の天気
            if evening_forecast:
                evening = evening_forecast[0]
                print("\n夕方の天気（16-19時）:")
                print(f"- 天気: {evening['weather'][0]['description']}")
                print(f"- 気温: {evening['main']['temp']}°C")
            
            # 雨の予報があれば表示
            if rain_forecast:
                print("\n雨の予報:")
                print("=======================================")
                for rain in rain_forecast:
                    print(f"- {rain['time']}頃から: {rain['description']}")
            
        else:
            print("\n天気予報テスト結果:")
            print("=======================================")
            print(f"- ステータス: 失敗")
            print(f"- エラーコード: {response.status_code}")
            print(f"- エラーメッセージ: {response.text}")
            
    except Exception as e:
        print("\n天気予報テスト結果:")
        print("=======================================")
        print(f"- ステータス: 失敗")
        print(f"- エラー: {str(e)}")

if __name__ == '__main__':
    get_weather_forecast()
