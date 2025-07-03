from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# サービスアカウントキーのパス
SERVICE_ACCOUNT_FILE = 'amplified-ward-457419-g1-d926f1d3100b.json'

# シートID（後で設定）
SHEET_IDS = {
    'kyushoku': '1VgVASBlOmjK_VLbsbgAGn0wu6Oi5CRiUJXfVZ8zhOpY',
    'geko': '18LOXzRjakazyQ5SB_yLHfZhZOBTIqp2E_am9gNrIJOQ',
    'remind': '1QOjCLGUat3G6n3LlaY8iKr9Eu93AEkimNuPUqwFPJoI'
}

def test_google_sheets():
    try:
        # サービスアカウント認証
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        
        service = build('sheets', 'v4', credentials=credentials)
        
        print("\nGoogle Sheets API接続テスト開始")
        print("=======================================")
        
        # 各シートのテスト
        for sheet_type, sheet_id in SHEET_IDS.items():
            try:
                # シートの最初のセルを取得してテスト
                result = service.spreadsheets().values().get(
                    spreadsheetId=sheet_id,
                    range='A1'
                ).execute()
                
                values = result.get('values', [])
                print(f"\n{sheet_type}シートのテスト結果:")
                print(f"- ステータス: 成功")
                if values:
                    print(f"- 最初のセルの値: {values[0][0]}")
                else:
                    print("- セルの値: 空")
            except Exception as e:
                print(f"\n{sheet_type}シートのテスト結果:")
                print(f"- ステータス: 失敗")
                print(f"- エラー: {str(e)}")
                
    except Exception as e:
        print("\n全体的なテスト結果:")
        print(f"- ステータス: 失敗")
        print(f"- エラー: {str(e)}")

if __name__ == '__main__':
    test_google_sheets()
