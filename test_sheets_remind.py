# -*- coding: utf-8 -*-
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import sys
import io

# 日本語の文字コードを設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_sheets_remind():
    try:
        # サービスアカウントキーのパス
        SERVICE_ACCOUNT_FILE = 'amplified-ward-457419-g1-d926f1d3100b.json'
        
        # スコープの設定
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        
        # サービスアカウントの認証
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        # Sheets APIのサービスを構築
        service = build('sheets', 'v4', credentials=credentials)
        
        # スプレッドシートID
        SPREADSHEET_ID = '1QOjCLGUat3G6n3LlaY8iKr9Eu93AEkimNuPUqwFPJoI'
        
        # A2セルの値を取得
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='A2'
        ).execute()
        
        # 値を取得
        values = result.get('values', [])
        
        if not values:
            print("\nリマインドテスト結果:")
            print("=======================================")
            print("- ステータス: 失敗")
            print("- エラー: データが見つかりません")
        else:
            remind = values[0][0] if values[0] else ""
            print("\nリマインドテスト結果:")
            print("=======================================")
            print("- ステータス: 成功")
            print("- リマインド内容:")
            print(f"  {remind}")
            
            # ママからの伝言として読み上げ用のテキストを作成
            remind_text = f"それから、ママからの伝言ですが、{remind}だ、そうです"
            print("\n読み上げ用テキスト:")
            print("=======================================")
            print(remind_text)
            
    except Exception as e:
        print("\nリマインドテスト結果:")
        print("=======================================")
        print(f"- ステータス: 失敗")
        print(f"- エラー: {str(e)}")

if __name__ == '__main__':
    test_sheets_remind()
