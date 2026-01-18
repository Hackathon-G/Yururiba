from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import hashlib
import uuid
import re
import os
# Flask：アプリ本体
# request：フォームやURLの入力を受け取る
# redirect：別URLへ移動させる
# render_template：HTMLを返す
# session：ログイン状態を保存
# flash：一時メッセージ表示（成功/失敗）
# abort：エラー画面（403/404など）表示
# url_for：URLを安全に生成
# CSRFProtect：CSRF対策（不正なフォーム送信防止）
# timedelta：「30日」など 期間を表現するため
# hashlib：パスワードのハッシュ化
# uuid：ランダムで安全な値を作る
# re：正規表現（メール判定）
# os：環境変数を読む

from models import User , Post, Comment
# User , Post, Commentをmodels.pyで扱うよ

# 定数定義
# メールアドレス形式チェック用の正規表現
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
# セッションの有効期限
SESSION_DAYS = 30
# このファイルを Flask アプリとして起動
app = Flask(__name__)
# 環境変数にSECRET_KEYがあれば使う（なければランダムなキー）
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
# セッションの有効期限を設定
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)
# CSRF対策をON
csrf = CSRFProtect(app)
# めも：セッション=ログイン状態を覚えておくための仕組み

# ルートページのリダイレクト処理
@app.route('/', methods=['GET'])
def index():
    # セッションにuser_idが残っていればpost画面
    # 残っていなければlogin画面にリダイレクト
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    return redirect(url_for('posts_view'))


# サインアップページの表示
@app.route('/signup', methods=['GET'])
def signup_view():
    # セッションにuser_idが残っていればpost画面
    # 残っていなければlogin画面にリダイレクト
    if session.get('user_id') is not None:
        return redirect(url_for('posts_view'))
    return render_template('auth/signup.html')


# サインアップ処理
@app.route('/signup', methods=['POST'])
def signup_process():
    # フォームの値を受け取る
    # .get()：キーがなくてもエラーにならない（キーはhtmlのname）
    #  例. emailがあれば、その値をgetする、なければNone
    # .strip()：前後の空白除去
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    password_confirmation = request.form.get('password_confirmation', '')

    # 空チェック
    if not name or not email or not password or not password_confirmation:
        flash("空のフォームがあります" , 'error')
        return redirect(url_for('signup_view'))

    # パスワード一致チェック
    if password != password_confirmation: # パスワードが違う場合
        # エラーメッセージを表示+sign_uo画面をリダイレクト
        flash('二つのパスワードの値が違っています','error')
        return redirect(url_for('signup_view'))

    # メール形式チェック
    if re.match(EMAIL_PATTERN, email) is None: # メールアドレスの形式がおかしい場合
        # エラーメッセージを表示+sign_uo画面をリダイレクト
        flash('正しいメールアドレスの形式ではありません','error')
        return redirect(url_for('signup_view'))

    # 既存ユーザーチェック
    registered_user = User.find_by_email(email) # emailがDBに既に登録済みチェック
    if registered_user is not None: # emailが登録済みの場合
        # エラーメッセージを表示+sign_uo画面をリダイレクト
        flash('既に登録されているメールアドレスです','error')
        return redirect(url_for('signup_view'))
    
    # パスワードのハッシュ化（sha256）
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Userテーブルにname,email,password(hash)を保存（登録）←models.pyで処理
    user_id = User.create(name, email, hashed_password)

    # ログイン状態（セッション）
    session['user_id'] = user_id

    # post画面に移動（ログイン状態）
    return redirect(url_for('posts_view'))


# ログインページの表示
@app.route('/login', methods=['GET'])
def login_view():
    # セッションにuser_idが残っていればpost画面
    # 残っていなければlogin画面にリダイレクト
    if session.get('user_id') is not None:
        return redirect(url_for('posts_view'))
    return render_template('auth/login.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    # フォームから情報を受け取る
    email = request.form.get('email')
    password = request.form.get('password')
    # 空チェック
    if email =='' or password == '':
        # エラーメッセージを表示
        flash('メールアドレスorパスワードが空です','error')
    else:
        # 入力されたemailがDBにあるかチェック
        user = User.find_by_email(email)
        if user is None: # DBにないよ～
            # エラーメッセージを表示
            flash('メールアドレスorパスワードが違います','error')
        else: # DBにあったよ
            # パスワードをハッシュ化
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            # ハッシュ化したパスワードがDBにあるかチェック
            if hashPassword != user["password"]: # DBにないよ～
                flash('メールアドレスorパスワードが違います','error')
            else: # あったよ
                session['user_id'] = user["id"]
                return redirect(url_for('posts_view'))
    return redirect(url_for('login_view'))


# ログアウト
@app.route('/logout')
def logout():
    # セッションをクリア
    # login画面にリダイレクト
    session.clear()
    return redirect(url_for('login_view'))


# 投稿一覧ページの表示
@app.route('/posts', methods=['GET'])
def posts_view():
    # セッションにuser_idが残っていなければlogin画面にリダイレクト
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    else: # ログイン状態
        posts = Post.get_all() # madels.pyのpostをすべてget
        for post in posts: # 一つずつ取り出し
            # 投稿の投稿日をを取得し、見やすい表記に変える
            post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
            # 投稿したユーザー名を取得
            post['user_name'] = User.get_name_by_id(post['user_id'])
        # posts画面にpost（投稿日とユーザー名）をHTMLに反映
        return render_template('post/posts.html', posts=posts, user_id=user_id)


# 投稿処理
@app.route('/posts', methods=['POST'])
def create_post():
    # セッションにuser_idが残っていなければlogin画面にリダイレクト
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    # フォームの値を受け取る
    # .get()：キーがなくてもエラーにならない（キーはhtmlのname）
    # .strip()：前後の空白除去
    content = request.form.get('content', '').strip()
    if content == '': # 投稿メッセージが空
        # エラーメッセージを表示+post画面にリダイレクト
        flash('投稿内容が空です','error')
        return redirect(url_for('posts_view'))
    # 投稿メッセージが空でない
    # models.pyのPostへ
    Post.create(user_id, content)
    # メッセージを表示して、post画面へリダイレクト
    flash('投稿が完了しました','success')
    return redirect(url_for('posts_view'))

# 投稿削除処理
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    # セッションにuser_idが残っていなければlogin画面にリダイレクト
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    # DBにpost_idがあるかチェック
    post = Post.find_by_id(post_id)
    if post is None: # DBにないよ～
        abort(404) #404NotFound
    # user_idが投稿者のuser_idと同じかチェック
    if post['user_id'] != user_id: # DBのuser_idと違うよ
        # エラーメッセージを表示9post画面をリダイレクト
        flash('この投稿を削除することはできません', 'error')
        return redirect(url_for('posts_view'))
    # 正常の場合、models.pyでPost削除を実行
    Post.delete(post_id)
    # メッセージを表示してリダイレクト
    flash('投稿が削除されました','success')
    return redirect(url_for('posts_view'))

# 投稿詳細ページの表示
@app.route('/posts/<int:post_id>', methods=['GET'])
def post_detail_view(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    post = Post.find_by_id(post_id)
    if post is None:
        abort(404)
    post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
    post['user_name'] = User.get_name_by_id(post['user_id'])

    comments = Comment.get_by_post_id(post_id)
    for comment in comments:
        comment['created_at'] = comment['created_at'].strftime('%Y-%m-%d %H:%M')
        comment['user_name'] = User.get_name_by_id(comment['user_id'])

    return render_template('post/post_detail.html', post=post, comments = comments, user_id=user_id)

# コメント処理
@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    content = request.form.get('content', '').strip()
    if content == '':
        flash('コメント内容が空です','error')
        return redirect(url_for('post_detail_view', post_id=post_id))
    Comment.create(user_id, post_id, content)
    flash('コメントの投稿が完了しました','success')
    return redirect(url_for('post_detail_view', post_id=post_id))

# 400BadRequest
@app.errorhandler(400)
def bad_request(error):
    return render_template('error/400.html'), 400
# 404NotFound
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404
# 500ServerError
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html'),500
# localhostの設定
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
