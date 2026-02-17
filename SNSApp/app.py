from flask import Flask, request, redirect, render_template, session, flash, abort, url_for, make_response
from datetime import timedelta
import uuid
from models import Post, Comment, User

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)
app.secret_key = "dev-secret-key"
# ルートURL('/')へのGETリクエストを処理する関数を定義
@app.route('/')
def base_view():
    return render_template('auth/base.html')

# url_forのテスト
# ログインページの表示
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('auth/login.html')

@app.route("/login", methods=["POST"])
def login():
    print(dict(request.form))
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print(f"email: {email}")
        print(f"password: {password}")

        # DB照合（今は省略）

        return redirect(url_for("timeline_view"))

    return render_template("login.html")


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
    dummy_posts = [
        {
            "content": "はじめての投稿です！",
            "user": {"username": "ぽめちゃん"}
        },
        {
            "content": "今日はハッカソン！",
            "user": {"username": "ゆるりば"}
        }
    ]

    return render_template('post/timeline.html', posts=dummy_posts)

@app.route('/post/create', methods=['POST'])
def post_create_view():
    content = request.form.get("content")
    print("受け取った投稿:", content)

    flash("投稿送信(仮)")
    return redirect(url_for("timeline_view"))

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

# ログアウト
@app.route("/logout")
def logout():
    session.clear()
    return login_view()

# 404エラー確認用
@app.route('/test', methods=['GET'])
def error_404_test_view():
    abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404

#リスト表示
# @app.route('/posts', methods=['GET'])
# def posts_list_view(post_id):
#     posts = Post.find_by_id(post_id)
#     posts['created_at'] = posts['created_at'].strftime('%Y-%m-%d %H:$M')
#     posts['user_name'] =  User.get_name_by_id(posts['user_id'])
    
#     comments = Comment.get_by_post_id(post_id)
#     for comment in comments:
#         comment['created_at'] = comment['created_at'].strftime('%Y-%m-%d %H:%M')
#         comment['user_name'] = User.get_name_by_id(comment['user_id'])
#     return render_template('post/timeline.html', post=posts, comments = comments, user_id="ぽめちゃん")


# Pythonファイルとして直接実行された場合にサーバーを起動
if __name__ == '__main__':
    # host='0.0.0.0'で外部からのアクセスも可能に（デフォルトは'127.0.0.1'）
    # port=5000はデフォルトポート
    app.run(debug=True, host='0.0.0.0')

