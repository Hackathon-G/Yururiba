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

# 趣味選択ページの表示
@app.route('/hobbies', methods=['GET'])
def syumi_view():
    return render_template('post/syumi.html')

# タイムラインページの表示
@app.route('/timeline', methods=['GET'])
def timeline_view():
    return render_template('post/timeline.html')

#投稿一覧取得・表示
# @app.route('/posts/{hobby_id}', methods=['GET'])
# def posts_view():
#     return render_template('post/timeline.html')

#投稿タグ一覧選択を表示
# @app.route('/tags', methods=['GET'])
# def tags_view():
#     return render_template('post/timeline.html')

#ホーム画面表示
@app.route('/home', methods=['GET'])
def home_view():
    return render_template('post/home.html')

#保存画面表示
@app.route('/list', methods=['GET'])
def list_view():
    return render_template('post/list.html')



# Pythonファイルとして直接実行された場合にサーバーを起動
if __name__ == '__main__':
    # host='0.0.0.0'で外部からのアクセスも可能に（デフォルトは'127.0.0.1'）
    # port=5000はデフォルトポート
    app.run(debug=True, host='0.0.0.0')

