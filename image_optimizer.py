from PIL import Image
import os
import sys

def rotate_image(input_path, output_path=None, degrees=90):
    """
    画像を指定された角度で回転します。
    
    Args:
        input_path (str): 入力画像のパス
        output_path (str, optional): 出力画像のパス。指定しない場合は入力パスと同じディレクトリに保存
        degrees (int, optional): 回転角度（度）。デフォルトは90度
    """
    try:
        # 入力ファイルの存在確認
        if not os.path.exists(input_path):
            print(f"エラー: {input_path} が見つかりません")
            return False
            
        # 出力パスが指定されていない場合は、入力パスと同じディレクトリに保存
        if output_path is None:
            dir_name = os.path.dirname(input_path)
            base_name = os.path.basename(input_path)
            output_path = os.path.join(dir_name, f"rotated_{base_name}")
            
        # 画像を開く
        with Image.open(input_path) as img:
            # 回転
            rotated_img = img.rotate(-degrees, expand=True)
            
            # 透明度を保持したまま保存
            rotated_img.save(output_path, 'PNG', optimize=True)
            
            print(f"画像が {degrees}度回転し、{output_path} に保存されました")
            return True
            
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return False

def optimize_image(input_path, output_path=None, target_width=864):
    """
    画像を指定された幅にリサイズし、最適化します。
    
    Args:
        input_path (str): 入力画像のパス
        output_path (str, optional): 出力画像のパス。指定しない場合は入力パスと同じディレクトリに保存
        target_width (int, optional): 目標の横幅（ピクセル）。デフォルトは864
    """
    try:
        # 入力ファイルの存在確認
        if not os.path.exists(input_path):
            print(f"エラー: {input_path} が見つかりません")
            return False
            
        # 出力パスが指定されていない場合は、入力パスと同じディレクトリに保存
        if output_path is None:
            dir_name = os.path.dirname(input_path)
            base_name = os.path.basename(input_path)
            output_path = os.path.join(dir_name, f"optimized_{base_name}")
            
        # 画像を開く
        with Image.open(input_path) as img:
            # 現在のサイズを取得
            width, height = img.size
            
            # 横864ピクセルにリサイズ（縦横比を維持）
            new_width = target_width
            new_height = int(height * (new_width / width))
            
            # リサイズ
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 透明度を保持したまま保存
            resized_img.save(output_path, 'PNG', optimize=True)
            
            print(f"元のサイズ: {width}x{height}")
            print(f"新しいサイズ: {new_width}x{new_height}")
            print(f"最適化された画像が {output_path} に保存されました")
            
            return True
            
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return False

def rotate_all_pngs(directory='.'):
    """
    指定されたディレクトリ内のすべてのPNG画像を回転します。
    
    Args:
        directory (str, optional): 対象のディレクトリパス。デフォルトは現在のディレクトリ
    """
    try:
        # ディレクトリ内のPNGファイルを検索
        png_files = [f for f in os.listdir(directory) if f.lower().endswith('.png')]
        
        if not png_files:
            print(f"{directory} にPNGファイルが見つかりませんでした")
            return
            
        print(f"{len(png_files)}個のPNGファイルが見つかりました")
        
        # 各PNGファイルを回転
        for png_file in png_files:
            input_path = os.path.join(directory, png_file)
            output_path = os.path.join(directory, f"rotated_{png_file}")
            
            print(f"\n{png_file} を処理中...")
            success = rotate_image(input_path, output_path)
            
            if success:
                print(f"{png_file} の処理が完了しました")
            else:
                print(f"{png_file} の処理に失敗しました")
                
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print("使用方法:")
        print("1. 単一の画像を最適化: python image_optimizer.py 入力ファイルパス [出力ファイルパス]")
        print("2. すべてのPNGを最適化: python image_optimizer.py --all [ディレクトリパス]")
        print("3. 単一の画像を回転: python image_optimizer.py --rotate 入力ファイルパス [出力ファイルパス]")
        print("4. すべてのPNGを回転: python image_optimizer.py --rotate-all [ディレクトリパス]")
        sys.exit(1)
        
    if sys.argv[1] == '--all':
        directory = sys.argv[2] if len(sys.argv) > 2 else '.'
        optimize_all_pngs(directory)
    elif sys.argv[1] == '--rotate':
        input_path = sys.argv[2]
        output_path = sys.argv[3] if len(sys.argv) > 3 else None
        rotate_image(input_path, output_path)
    elif sys.argv[1] == '--rotate-all':
        directory = sys.argv[2] if len(sys.argv) > 2 else '.'
        rotate_all_pngs(directory)
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        optimize_image(input_path, output_path)

if __name__ == "__main__":
    main()
