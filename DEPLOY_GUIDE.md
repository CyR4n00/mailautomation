# PCを閉じても24時間動かすためのクラウド設定マニュアル

このツールを「Render」という無料のクラウドサーバーにアップロードして、あなたのPCの電源が切れていても、24時間自動でメール送信やリマインドが行われるようにする手順です。

大きく分けて「3つのステップ」で完了します。

---

## ステップ1：プログラムをインターネット上（GitHub）に預ける

Renderにプログラムを渡すために、まずは「GitHub」という世界最大のプログラム保管庫にあなたのツールを預けます。

1. **GitHubアカウントの作成**
   [GitHub (https://github.com/)](https://github.com/) にアクセスし、無料アカウントを作成します。
2. **新しい保管庫（リポジトリ）を作る**
   ログイン後、画面右上の「＋」ボタンから「New repository」をクリックします。
   - Repository name: `email-automation-tool` (好きな名前でOK)
   - Public / Private: **「Private（非公開）」** を必ず選んでください。（※他人にプログラムや顧客リストを見られないため）
   - 「Create repository」ボタンを押します。
3. **ファイルをアップロードする**
   画面の中央あたりにある **「uploading an existing file」** というリンクをクリックします。
   お使いのPCにあるこのツールの「中身のファイルすべて（`app`フォルダや `run.py` など）」をドラッグ＆ドロップしてアップロードし、下にある緑色の「Commit changes」ボタンを押します。
   （※ `.git` や `venv` などの隠しフォルダは不要ですが、普通にドラッグすれば問題ありません。一番重要なのは `requirements.txt` や `Procfile` が入っていることです）

---

## ステップ2：Renderでサーバーを立ち上げる

1. **Renderアカウントの作成**
   [Render (https://render.com/)](https://render.com/) にアクセスし、「Get Started」から無料アカウントを作ります（GitHubアカウントでログインするとスムーズです）。
2. **Web Serviceの作成**
   ダッシュボード画面右上の「New」ボタンから **「Web Service」** をクリックします。
3. **GitHubと連携**
   「Build and deploy from a Git repository」を選択し、右側の「Connect GitHub」を押して連携を許可します。
   すると、ステップ1で作った `email-automation-tool` という名前が出てくるので、**「Connect」** を押します。
4. **設定の入力**
   以下の通りに設定を確認・変更します。
   - Name: `my-auto-tool` (好きな名前でOK)
   - Runtime: **Python 3**
   - Build Command: `pip install -r requirements.txt` (そのままか、入力する)
   - Start Command: `gunicorn run:app` (Procfileがあるため自動で入るはずです)
   - Instance Type: **Free** (無料プラン) を選択。
5. **セキュリティ用パスワードの設定（環境変数）**
   同じ画面を少し下にスクロールして **「Environment Variables (Advanced)」** を開き、「Add Environment Variable」を押して以下の3つを追加します。
   - KEY: `AUTH_USERNAME` / VALUE: `自分の好きなログインID` (例: `taro`)
   - KEY: `AUTH_PASSWORD` / VALUE: `自分の好きなパスワード` (例: `himitsu123`)
   - KEY: `PYTHON_VERSION` / VALUE: `3.10.0`
6. 一番下の **「Create Web Service」** を押します！
   （※ここから数分間、画面上で黒い文字が流れてサーバーの準備が行われます。「Your service is live 🎉」と出たら成功です）

画面左上に表示されているURL（例: `https://my-auto-tool.onrender.com`）をクリックすると、あなたが設定したIDとパスワードの入力画面が出ます。ログインすれば、ツールの画面が開きます！

*(※注意：この段階で、このクラウド上のツールからもGoogleカレンダー操作ができるよう、ツールの画面から再度「Google連携設定」で認証をやり直してください)*

---

## ステップ3：サーバーを「居眠り」させない設定

Renderの無料プランは、「15分間アクセスがないと、サーバーが自動的に居眠り（スリープモード）する」という仕様があります。
居眠りしている間は、時計が止まるため「自動メール送信」が行われません。

これを防ぐため、**「5分に1回、自動であなたのツールにアクセスして起こし続けてくれる」** 別の無料サービスを使います。

1. **cron-job.org に登録**
   [cron-job.org (https://cron-job.org/en/)](https://cron-job.org/en/) にアクセスし、無料アカウントを作ります。
2. **ジョブの作成**
   ログイン後、「CREATE CRONJOB」をクリックします。
3. **URLの入力**
   - Title: `Render スリープ防止` (なんでもOK)
   - URL: 先ほどRenderで作ったあなたのツールのURL（例: `https://my-auto-tool.onrender.com/`）を入力します。
   - Schedule: **「Every 5 minutes (5分ごと)」** を選びます。
4. **Basic認証の設定（重要）**
   URLにパスワードがかかっているため、起こしに行くロボットにもパスワードを教えてあげる必要があります。
   画面下部の **「Advanced」** タブを開き、**「HTTP Authorization (Basic Auth)」** にチェックを入れます。
   - User: ステップ2で決めた `AUTH_USERNAME` (例: `taro`)
   - Password: ステップ2で決めた `AUTH_PASSWORD` (例: `himitsu123`)
5. **「CREATE」** ボタンを押して完了です！

以上で、あなたのPCが電源オフになっていても、24時間365日休まずに働く「完全自動の営業＆アポ管理システム」の完成です。お疲れ様でした！
