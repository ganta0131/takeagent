from google.cloud import texttospeech
import os

# サービスアカウントキーのパス
SERVICE_ACCOUNT_FILE = 'amplified-ward-457419-g1-d926f1d3100b.json'

# 音声合成のテスト
client = texttospeech.TextToSpeechClient.from_service_account_file(SERVICE_ACCOUNT_FILE)

def test_text_to_speech():
    try:
        # 生成されたテキスト
        text = """たける様、おはようございます！今日は晴れて気持ちの良い一日ですね！

今日の給食はたける様の大好きなカレーライス！おかわり自由ですよ！たくさん食べて、午後からの勉強も頑張ってくださいね。

それから、今日は16時に下校ですね。図書館で借りた本を返すのを忘れないようにしてくださいね。

今日は良いことたくさんの一日です！きっと、たける様なら全部上手くできます！頑張ってください！応援していますよ！"""
        
        # 音声合成設定
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # 音声設定（日本語、男性の声）
        voice = texttospeech.VoiceSelectionParams(
            language_code="ja-JP",
            name="ja-JP-Wavenet-C",  # 男性の声
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )
        
        # オーディオ設定
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        # 音声合成実行
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # 音声ファイルの保存
        with open('output.mp3', 'wb') as out:
            out.write(response.audio_content)
            print("\n音声ファイルが生成されました：output.mp3")
            print("- 音声内容：")
            print(text)
            print("- 音声言語：日本語")
            print("- 音声タイプ：子供向け")
            
    except Exception as e:
        print("\n音声合成テスト結果:")
        print("=======================================")
        print(f"- ステータス: 失敗")
        print(f"- エラー: {str(e)}")

if __name__ == '__main__':
    test_text_to_speech()
