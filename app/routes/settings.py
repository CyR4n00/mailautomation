from flask import Blueprint, render_template, flash, redirect, url_for
from app.services.google_auth import get_google_credentials

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/')
def index():
    return render_template('settings/index.html')

@settings_bp.route('/auth_google')
def auth_google():
    try:
        # 認証フローをトリガーする
        get_google_credentials()
        flash('Google アカウントの連携が完了しました。', 'success')
    except Exception as e:
        flash(f'認証エラー: {str(e)}', 'danger')
    return redirect(url_for('settings.index'))
