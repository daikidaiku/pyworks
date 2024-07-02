from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from dotenv import load_dotenv

# # .envファイルの読み込み
load_dotenv()

def main():
    # Google Drive 認証
    gauth = GoogleAuth()
    
    # 認証情報を保存するファイル名
    credentials_file = "/home/daiki_daiku/Documents/pyworks/uploadApp/mycreds.txt"
    
    # 認証情報を読み込みます
    gauth.LoadCredentialsFile(credentials_file)
    
    if gauth.credentials is None:
        # 認証画面を表示します（ブラウザが開かれます）
        gauth.CommandLineAuth()
    elif gauth.access_token_expired:
        # アクセストークンが期限切れの場合、リフレッシュします
        gauth.Refresh()
    else:
        # 既存の認証情報を使用します
        gauth.Authorize()
    
    # 認証情報を保存します
    gauth.SaveCredentialsFile(credentials_file)
    
    drive = GoogleDrive(gauth)
    
    # 画像ファイルのアップロード
    f = drive.CreateFile({"parents":[{'id':os.getenv('PARENT_ID')}],
                          "id":os.getenv('FOLDER_ID'),
                          "title": "test.jpg",
                          "mimeType": "image/jpeg"})
    f.SetContentFile(os.getenv('IMAGE_PATH'))
    f.Upload()
    
    #print("ファイルがアップロードされました")

if __name__ == "__main__":
    main()
