from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.client import Client
from app.services.email_service import send_email
from app import db

mail_bp = Blueprint('mail', __name__, url_prefix='/mail')

@mail_bp.route('/', methods=['GET', 'POST'])
def send_bulk():
    clients = Client.query.all()

    if request.method == 'POST':
        subject = request.form.get('subject')
        body = request.form.get('body')
        selected_client_ids = request.form.getlist('client_ids')

        if not subject or not body:
            flash('件名と本文を入力してください。', 'danger')
            return redirect(url_for('mail.send_bulk'))

        if not selected_client_ids:
            flash('送信先のクライアントを選択してください。', 'danger')
            return redirect(url_for('mail.send_bulk'))

        selected_clients = Client.query.filter(Client.id.in_(selected_client_ids)).all()
        bcc_emails = ", ".join([c.email for c in selected_clients])

        try:
            # 宛先(To)は自分自身などに設定し、クライアントはBCCに設定する
            # ※ここでは便宜上 To を自分自身 (BCCの最初の1人や固定のアドレス) にするか、空にすることが多いですが、Gmailの仕様上Toがあった方がスパム判定されにくいです。
            # 一旦、最初のユーザーをToにして残りをBccにするか、自分自身のメールアドレスをToに入れるなどの工夫が必要です。
            # 今回はシンプルに、ダミーとして 'undisclosed-recipients:;' をToにして、すべてBCCに入れます。
            send_email(
                to='undisclosed-recipients:;',
                subject=subject,
                body=body,
                bcc=bcc_emails
            )

            # ステータスを更新
            for c in selected_clients:
                c.status = '打診済み'
            db.session.commit()

            flash(f'{len(selected_clients)}件の宛先に一斉送信しました。', 'success')

        except Exception as e:
            flash(f'送信中にエラーが発生しました: {str(e)}', 'danger')

        return redirect(url_for('mail.send_bulk'))

    return render_template('mail/send.html', clients=clients)
