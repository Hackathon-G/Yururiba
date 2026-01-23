from flask import Flask, request, redirect, render_template, session, flash, abort, url_for

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# ルートURL('/')へのGETリクエストを処理する関数を定義
@app.route('/')
def hello_world():
    return 'Hello, Flask!'

# url_forのテスト
# ログインページの表示
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('auth/login.html')

# 新規登録ページの表示
@app.route('/register', methods=['GET'])
def register_view():
    return render_template('auth/register.html')

# タイムラインページの表示
@app.route('/timeline', methods=['GET'])
def timeline_view():
    return render_template('post/timeline.html')

# 趣味選択ページの表示
@app.route('/syumi', methods=['GET'])
def syumi_view():
    return render_template('post/syumi.html')

# テストページの表示
@app.route('/pome', methods=['GET'])
def pome_view():
    return render_template('error/pome.html')

# テストページの表示
@app.route('/pomeJSON', methods=['GET'])
def pomeJSON_view():
    return render_template('error/pomeJSON.html')

# Pythonファイルとして直接実行された場合にサーバーを起動
if __name__ == '__main__':
    # host='0.0.0.0'で外部からのアクセスも可能に（デフォルトは'127.0.0.1'）
    # port=5000はデフォルトポート
    app.run(debug=True, host='0.0.0.0')

