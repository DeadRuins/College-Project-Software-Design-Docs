import os
import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(local_file_path, bucket_name, s3_file_path):
    """
    ローカルのファイルを指定したS3バケットにアップロードする関数
    """
    # S3クライアントの初期化（認証情報は自動で読み込まれます）
    s3 = boto3.client('s3')
    
    try:
        print(f"アップロード中: {local_file_path} -> s3://{bucket_name}/{s3_file_path}")
        s3.upload_file(local_file_path, bucket_name, s3_file_path)
        print("アップロードが成功しました！")
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
BUCKET_NAME = 'pbl2026e'  # ステップ1で作ったバケット名に変更
LOCAL_CSV = '/home/pi/temperature_log.csv'     # ラズパイ上にある送信したいCSVのパス
S3_PATH = 'data/raspberry_pi.csv'  # S3上での保存先パス（フォルダ分けも可能）


