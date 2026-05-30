from app import db
from datetime import datetime

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 状態管理（例: '未連絡', '打診済み', 'アポ確定', '完了' など）
    status = db.Column(db.String(50), default='未連絡')

    # アポ情報
    appointment_time = db.Column(db.DateTime, nullable=True)
    duration_minutes = db.Column(db.Integer, default=60)
    calendar_event_id = db.Column(db.String(255), nullable=True)

    # アポ後の送付資料リンクなどを事前に保存しておくフィールド
    materials_link = db.Column(db.Text, nullable=True)

    # 送信済みフラグ (スパム防止用)
    is_reminder_sent = db.Column(db.Boolean, default=False)
    is_followup_sent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Client {self.name} ({self.email})>'
