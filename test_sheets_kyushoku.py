# -*- coding: utf-8 -*-
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import sys
import io

# 日本語の文字コードを設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_sheets_kyushoku():
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
        SPREADSHEET_ID = '1VgVASBlOmjK_VLbsbgAGn0wu6Oi5CRiUJXfVZ8zhOpY'
        
        import datetime
        from dateutil.parser import parse
        
        # A列とB列のデータを取得
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='A:B'
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print("\n給食テスト結果:")
            print("=======================================")
            print("- ステータス: 失敗")
            print("- エラー: データが見つかりません")
            return
            
        # 現在の日付を取得（YYYY/MM/DD形式）
        today = datetime.datetime.now().strftime('%Y/%m/%d')
        
        # 現在の日付と一致する行のデータを探す
        found = False
        for row in values:
            if len(row) >= 2:  # 日付と献立が両方ある行のみ
                try:
                    # 日付の形式を調整
                    sheet_date = parse(row[0]).strftime('%Y/%m/%d')
                    if sheet_date == today:
                        date = row[0]
                        menu = row[1]
                        found = True
                        break
                except ValueError:
                    continue
        
        if not found:
            print("\n給食テスト結果:")
            print("=======================================")
            print("- ステータス: 失敗")
            print("- エラー: 今日の給食データが見つかりません")
            return
            
        print("\n給食テスト結果:")
        print("=======================================")
        print("- ステータス: 成功")
        print("- 給食内容:")
        print(f"  日付: {date}")
        print(f"  献立: {menu}")
        
        # 読み上げ用のテキストを作成
        kyushoku_text = f"今日の給食は{menu}です。"
        print("\n読み上げ用テキスト:")
        print("=======================================")
        print(kyushoku_text)
            
    except Exception as e:
        print("\n給食テスト結果:")
        print("=======================================")
        print(f"- ステータス: 失敗")
        print(f"- エラー: {str(e)}")

if __name__ == '__main__':
    test_sheets_kyushoku()
