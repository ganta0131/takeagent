# -*- coding: utf-8 -*-
import google.generativeai as genai
import os
import sys

# 文字コードの設定
sys.stdout.reconfigure(encoding='utf-8')

# APIキーの設定
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAE7IC-TdIYFEWaEfvnP0iLciFBYU_Yfxk'

def test_generative_language():
    try:
        # モデルの初期化
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        model = genai.GenerativeModel('gemini-2.0-flash-001')

        # テスト用のプロンプト
        prompt = """
        あなたは小学三年生のたけるの執事です。
        以下の情報を基に、モチベーションが上がる一言を生成してください。
        
        情報：
        - 天気：晴れ（25.25°C）
        - 給食：カレーライス
        - 下校時間：16:00
        - リマインド：図書館の本を返す
        
        出力は日本語で、親しずきやすい口調でお願いします。
        """
        
        # モデルの実行
        response = model.generate_content(prompt)
        
        # レスポンスの処理
        if response.text:
            print("\nGenerative Language APIテスト結果:")
            print("=======================================")
            print("- ステータス: 成功")
            print("- 生成されたテキスト:")
            print(response.text)
        else:
            print("\nGenerative Language APIテスト結果:")
            print("=======================================")
            print("- ステータス: 失敗")
            print("- エラー: レスポンスが空です")
        
    except Exception as e:
        print("\nGenerative Language APIテスト結果:")
        print("=======================================")
        print(f"- ステータス: 失敗")
        print(f"- エラー: {str(e)}")

if __name__ == '__main__':
    test_generative_language()
