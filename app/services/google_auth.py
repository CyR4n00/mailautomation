import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmailとカレンダー両方のスコープ
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar.events'
]

def get_google_credentials():
    """Google APIの認証情報を取得・作成する"""
    creds = None
    token_path = os.path.join(os.getcwd(), 'token.pickle')
    credentials_path = os.path.join(os.getcwd(), 'credentials.json')

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # 有効な認証情報がない場合、ログインを要求
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError("credentials.jsonが見つかりません。Google Cloud Consoleからダウンロードしてルートディレクトリに配置してください。")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # 認証情報を保存
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_gmail_service():
    creds = get_google_credentials()
    return build('gmail', 'v1', credentials=creds)

def get_calendar_service():
    creds = get_google_credentials()
    return build('calendar', 'v3', credentials=creds)
