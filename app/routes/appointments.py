from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.client import Client
from app.services.calendar_service import create_appointment_event
from app.services.email_service import send_email
from app import db
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__, url_prefix='/appointments')

@appointments_bp.route('/<int:client_id>', methods=['GET', 'POST'])
def schedule(client_id):
    client = Client.query.get_or_404(client_id)

    if request.method == 'POST':
        appt_time_str = request.form.get('appointment_time')
        duration = int(request.form.get('duration', 60))
        send_confirm_mail = request.form.get('send_confirm_mail') == 'on'
        generate_meet = request.form.get('generate_meet') == 'on'
        materials_link = request.form.get('materials_link', '')

        if not appt_time_str:
            flash('日時を指定してください。', 'danger')
            return redirect(url_for('appointments.schedule', client_id=client.id))

        try:
            # カレンダー登録とMeet自動発行
            event_id, meet_url = create_appointment_event(
                summary=f"【商談】{client.name}様",
                description="オンラインアポ",
                start_time_str=appt_time_str,
                duration_minutes=duration,
                attendee_email=client.email,
                generate_meet_url=generate_meet
            )

            # クライアント情報更新
            client.appointment_time = datetime.strptime(appt_time_str, '%Y-%m-%dT%H:%M')
            client.duration_minutes = duration
            client.calendar_event_id = event_id
            client.status = 'アポ確定'
            client.materials_link = materials_link
            client.is_reminder_sent = False
            client.is_followup_sent = False

            # モデルにはMeetURL保存用のカラムがないため、今回は資料リンク等に依存しない形でメール送信時に直接使う。
            # 必要であればデータベースにカラムを追加しても良いが、ここではメール送信のみに使用する。

            db.session.commit()

            # アポ確定メール送信
            if send_confirm_mail:
                subject = "【アポ確定のお知らせ】オンラインミーティングについて"

                body = f"{client.name} 様\n\nお世話になっております。\n\n以下の日時でオンラインミーティングの手配が完了いたしました。\n\n"
                body += f"■日時: {client.appointment_time.strftime('%Y年%m月%d日 %H:%M')}〜 ({duration}分予定)\n"

                if meet_url:
                    body += f"■参加用URL (Google Meet):\n{meet_url}\n\nお時間になりましたら、上記のリンクよりご参加ください。\n"
                else:
                    body += f"\n"

                body += f"よろしくお願いいたします。"
                send_email(to=client.email, subject=subject, body=body)

            flash('アポをカレンダーに登録し、手配を完了しました。', 'success')
            return redirect(url_for('clients.index'))

        except Exception as e:
            flash(f'エラーが発生しました: {str(e)}', 'danger')

    return render_template('appointments/schedule.html', client=client)
