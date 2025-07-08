# -*- coding: utf-8 -*-
import pygame
import sys
import io

# 日本語の文字コードを設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def play_audio(file_path):
    try:
        # pygameの初期化
        pygame.mixer.init()
        
        # 音声ファイルの読み込み
        pygame.mixer.music.load(file_path)
        
        # 音声の再生
        pygame.mixer.music.play()
        
        # 再生が終わるまで待機
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # pygameの終了
        pygame.mixer.quit()
        print('音声の再生が完了しました。')
        
    except Exception as e:
        print(f'音声再生エラー: {str(e)}')

def main():
    # テスト用の音声ファイル
    test_file = 'output.mp3'
    
    # 音声再生を実行
    play_audio(test_file)

if __name__ == '__main__':
    main()
