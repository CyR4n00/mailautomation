import base64
from email.message import EmailMessage
from app.services.google_auth import get_gmail_service

def send_email(to, subject, body, bcc=None):
    """Gmail APIを使用してメールを送信する"""
    try:
        service = get_gmail_service()
        message = EmailMessage()

        message.set_content(body)
        message['To'] = to
        message['From'] = 'me'
        message['Subject'] = subject

        if bcc:
            message['Bcc'] = bcc

        # Base64エンコード
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        # 送信
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        return send_message
    except Exception as e:
        print(f"メール送信エラー: {e}")
        raise e
