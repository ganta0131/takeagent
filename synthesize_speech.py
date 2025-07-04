# -*- coding: utf-8 -*-
from google.cloud import texttospeech
import os
import sys
import io
import json
from google.oauth2 import service_account

def synthesize_speech(text, output_file='output.mp3'):
    try:
        print("\n=== Speech synthesis started ===")
        print(f"Input text length: {len(text)} characters")
        print(f"First 100 characters: {text[:100]}")
        
        # サービスアカウント情報を環境変数から取得
        service_account_info = os.getenv('GOOGLE_SERVICE_ACCOUNT_INFO')
        if not service_account_info:
            raise ValueError("GOOGLE_SERVICE_ACCOUNT_INFO environment variable not set")
            
        # JSON文字列を辞書に変換
        credentials_dict = json.loads(service_account_info)
        
        # クレデンシャルを作成
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)
        
        # クライアントをインスタンス化
        client = texttospeech.TextToSpeechClient(credentials=credentials)
        print(f"Client created successfully")
        
        # ボイスを設定（日本語、男性）
        voice = texttospeech.VoiceSelectionParams(
            language_code="ja-JP",
            name="ja-JP-Neural2-D",  # 男性の声
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )
        print(f"Voice parameters set")
        
        # 音声の種類を設定（mp3）
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        print(f"Audio config set")
        
        # テキストを分割（1回あたりの制限は約5000文字）
        max_chars = 1500  # 安全のため1500文字に設定
        parts = []
        while text:
            if len(text) <= max_chars:
                parts.append(text)
                break
            
            # 最後の句点または改行で分割
            split_point = max_chars
            while split_point > 0 and text[split_point] not in ['。', '\n']:
                split_point -= 1
            
            if split_point == 0:  # 適切な分割点が見つからない場合
                split_point = max_chars
                
            parts.append(text[:split_point])
            text = text[split_point:].strip()
        
        # すべての部分を合成し、mp3ファイルに保存
        with open(output_file, "wb") as out:
            for i, part in enumerate(parts):
                print(f"Processing part {i+1}/{len(parts)}: {part[:50]}...")
        
        print("All parts processed successfully.")
        # メモリ上のバイトデータを返す
        return audio_content
        
    except Exception as e:
        print(f"Error details: {str(e)}")
        # エラーをログファイルに記録
        with open('error.log', 'a', encoding='utf-8') as f:
            f.write(f'音声合成エラー: {str(e)}\n')
        return None

def main():
    # test_all.pyを実行してテキストを取得
    import test_all
    text = test_all.generate_text()
    
    # 音声合成を実行
    audio_file = synthesize_speech(text)
    
    if audio_file:
        print(f'音声ファイルが正常に生成されました: {audio_file}')
    else:
        print('音声ファイルの生成に失敗しました')

if __name__ == '__main__':
    main()
