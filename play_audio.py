import os
import winsound
from time import sleep

def play_audio():
    try:
        # 音声ファイルのパス
        audio_file = 'output.mp3'
        
        # 音声ファイルの存在確認
        if not os.path.exists(audio_file):
            print(f"音声ファイルが見つかりません: {audio_file}")
            return
            
        # 音声ファイルの再生
        print(f"\n音声ファイルを再生します: {audio_file}")
        
        # winsoundを使用して音声ファイルを再生
        winsound.PlaySound(audio_file, winsound.SND_FILENAME)
        
    except Exception as e:
        print(f"音声再生エラー: {str(e)}")

if __name__ == '__main__':
    play_audio()
