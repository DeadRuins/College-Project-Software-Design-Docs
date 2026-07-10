import os
import mimetypes  # ファイルの種類（csv, jpg, pngなど）を自動判別するライブラリ
import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(local_file_path, bucket_name, s3_file_path):
    """
    ローカルのファイル（CSVや画像など）を指定したS3バケットにアップロードする関数
    """
    s3 = boto3.client('s3')
    
    # ファイルの拡張子から種類（MIMEタイプ）を自動判別
    # 例: .csvなら 'text/csv'、.jpgなら 'image/jpeg' に自動でなります
    content_type, _ = mimetypes.guess_type(local_file_path)
    if content_type is None:
        content_type = 'binary/octet-stream'

    try:
        print(f"アップロード中: {local_file_path} -> s3://{bucket_name}/{s3_file_path}")
        
        # ContentTypeを指定してアップロード（これでAWS上で直接中身が見られます）
        s3.upload_file(
            local_file_path, 
            bucket_name, 
            s3_file_path,
            ExtraArgs={'ContentType': content_type}
        )
        print(f"【成功】{os.path.basename(local_file_path)} のアップロードが完了しました。")
        return True
    except FileNotFoundError:
        print(f"エラー: ローカルファイル {local_file_path} が見つかりません。")
        return False
    except NoCredentialsError:
        print("エラー: AWSの認証情報が見つかりません。'aws configure' を確認してください。")
        return False
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        return False

# --- 設定部分 ---
BUCKET_NAME = 'pbl2026e'  # 指定していただいたバケット名

# 1. CSVファイルの設定
LOCAL_CSV = '/home/pi/temperature_log.csv'  # ラズパイ側のCSVのパス（yokoiに変更）
S3_CSV_PATH = 'data/temperature_log.csv'       # S3側の保存先パス

# 2. 画像ファイルの設定
LOCAL_IMAGE = '/home/pi/photo.jpg'          # ラズパイ側の画像のパス
S3_IMAGE_PATH = 'images/camera_photo.jpg'      # S3側の保存先パス

if __name__ == "__main__":
    print("=== S3一括アップロード処理を開始します ===")
    
    # --- 1. CSVファイルのアップロード ---
    if os.path.exists(LOCAL_CSV):
        upload_to_s3(LOCAL_CSV, BUCKET_NAME, S3_CSV_PATH)
    else:
        print(f"スキップ: CSVファイルが見つかりません ({LOCAL_CSV})")
        
    print("-" * 40)  # 区切り線
        
    # --- 2. 画像ファイルのアップロード ---
    if os.path.exists(LOCAL_IMAGE):
        upload_to_s3(LOCAL_IMAGE, BUCKET_NAME, S3_IMAGE_PATH)
    else:
        print(f"スキップ: 画像ファイルが見つかりません ({LOCAL_IMAGE})")

    print("=== 全ての処理が終了しました ===")
