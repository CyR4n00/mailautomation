from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.client import Client

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/')
def index():
    clients = Client.query.all()
    return render_template('clients/index.html', clients=clients)

@clients_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # テキストエリアからの複数入力 (名前,メールアドレスの形式を想定)
        bulk_data = request.form.get('bulk_data')
        if bulk_data:
            lines = bulk_data.strip().split('\n')
            added_count = 0
            for line in lines:
                parts = line.split(',')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    email = parts[1].strip()

                    if not Client.query.filter_by(email=email).first():
                        client = Client(name=name, email=email)
                        db.session.add(client)
                        added_count += 1
            db.session.commit()
            flash(f'{added_count}件のクライアントを登録しました。', 'success')
            return redirect(url_for('clients.index'))

        # 単体入力
        name = request.form.get('name')
        email = request.form.get('email')

        if name and email:
            if not Client.query.filter_by(email=email).first():
                client = Client(name=name, email=email)
                db.session.add(client)
                db.session.commit()
                flash('クライアントを登録しました。', 'success')
            else:
                flash('このメールアドレスは既に登録されています。', 'danger')
            return redirect(url_for('clients.index'))

    return render_template('clients/add.html')

@clients_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    flash('クライアントを削除しました。', 'success')
    return redirect(url_for('clients.index'))
