from apscheduler.schedulers.background import BackgroundScheduler
from app.models.client import Client
from app.services.email_service import send_email
from app import db
from datetime import datetime, timedelta

def check_and_send_reminders(app):
    """定期的に実行し、必要なメールを自動送信する"""
    with app.app_context():
        now = datetime.now()

        # 1. アポ終了時の「本日の資料を送る」メール
        # 条件: (アポ開始時間 + duration) が 現在時刻 を過ぎていて、未送信であること。
        clients = Client.query.filter(
            Client.appointment_time != None,
            Client.status == 'アポ確定',
            Client.is_followup_sent == False
        ).all()

        for client in clients:
            duration = client.duration_minutes if client.duration_minutes else 60
            end_time = client.appointment_time + timedelta(minutes=duration)

            if now >= end_time:
                try:
                    materials = client.materials_link if client.materials_link else "(資料リンクは設定されていません)"
                    subject = "【御礼】本日のオンラインミーティングと資料のご案内"
                    body = f"{client.name} 様\n\n本日はお忙しい中、お時間をいただき誠にありがとうございました。\n\n本日のミーティングで使用した資料をお送りいたします。\n{materials}\n\n引き続きよろしくお願いいたします。"
                    send_email(to=client.email, subject=subject, body=body)

                    # 送信済みフラグとステータスを更新
                    client.is_followup_sent = True
                    client.status = '完了(資料送付済み)'
                    db.session.commit()
                    print(f"[{datetime.now()}] {client.name}様へアポ終了メールを送信しました。")
                except Exception as e:
                    print(f"[{datetime.now()}] {client.name}様へのアポ終了メール送信に失敗: {e}")

        # 2. 事前リマインドメール（アポの24時間以内に自動送信）
        tomorrow_start = now
        tomorrow_end = now + timedelta(days=1)

        upcoming_appointments = Client.query.filter(
            Client.appointment_time >= tomorrow_start,
            Client.appointment_time < tomorrow_end,
            Client.status == 'アポ確定',
            Client.is_reminder_sent == False
        ).all()

        for client in upcoming_appointments:
            try:
                subject = "【リマインド】明日のオンラインミーティングについて"
                body = f"{client.name} 様\n\nお世話になっております。\n\n明日のオンラインミーティングのリマインドとなります。\n日時: {client.appointment_time.strftime('%Y年%m月%d日 %H:%M')}〜\n\nよろしくお願いいたします。"
                send_email(to=client.email, subject=subject, body=body)

                # 送信済みフラグを更新
                client.is_reminder_sent = True
                db.session.commit()
                print(f"[{datetime.now()}] {client.name}様へリマインドメールを送信しました。")
            except Exception as e:
                print(f"[{datetime.now()}] {client.name}様へのリマインドメール送信に失敗: {e}")

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_and_send_reminders, args=[app], trigger="interval", minutes=1)
    scheduler.start()
    return scheduler
