# -*- coding: utf-8 -*-
from google.cloud import texttospeech
import os
import sys
import io

def synthesize_speech(text, output_file='output.mp3'):
    try:
        # サービスアカウントキーのパス
        credentials_path = 'amplified-ward-457419-g1-d926f1d3100b.json'
        
        # クライアントをインスタンス化
        client = texttospeech.TextToSpeechClient.from_service_account_file(credentials_path)
        
        # ボイスを設定（日本語、男性）
        voice = texttospeech.VoiceSelectionParams(
            language_code="ja-JP",
            name="ja-JP-Neural2-D",  # 男性の声
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )
        
        # 音声の種類を設定（mp3）
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
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
                synthesis_input = texttospeech.SynthesisInput(text=part)
                response = client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice,
                    audio_config=audio_config
                )
                print(f"Response received. Audio length: {len(response.audio_content)} bytes")
                out.write(response.audio_content)
        
        print("All parts processed successfully.")
        return output_file
        
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
