from flask import Flask, request, redirect, render_template, session, flash, abort, url_for, make_response
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import hashlib
import uuid
import re

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
jst = ZoneInfo("Asia/Tokyo")

from models import User , Post

# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)
app.secret_key = "dev-secret-key"
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

# csrf = CSRFProtect(app)

# ルートページのリダイレクト処理
@app.route('/', methods=['GET'])
def index():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    return redirect(url_for('timeline_view'))


# 新規登録ページの表示
@app.route('/register', methods=['GET'])
def register_view():
    # user_idの登録があれば、timeline_viewへ、なければregisterページへ
    if session.get('user_id') is not None:
        return redirect(url_for('timeline_view'))
    return render_template('auth/register.html')

# 新規登録処理
@app.route('/register', methods=['POST'])
def register_process():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    password_confirmation = request.form.get('password_confirmation', '')
    print(email)

    # 空チェック
    # html側でエラー出して？？？これは反映されず
    if not name or not email or not password or not password_confirmation:
        flash("空欄を埋めてねぇ", 'error')
        print("空欄を埋めてねぇ", 'error')
        return redirect(url_for('register_view'))

    # パスワード一致チェック
    if password != password_confirmation:
        flash("パスワードが一緒じゃないよ", 'error')
        print("パスワードが一緒じゃないよ", 'error')
        return redirect(url_for('register_view'))

    # メール形式チェック
    # html側でエラー出して？？？これは反映されず
    if re.match(EMAIL_PATTERN, email) is None:
        flash("メールアドレスの形式がなんか違うよ", 'error')
        print("メールアドレスの形式がなんか違うよ", 'error')
        return redirect(url_for('register_view'))

    # 既存ユーザーチェック：
    registered_user = User.find_by_email(email)
    if registered_user is not None:
        flash("そのメールアドレスもう登録されてるよ")
        print("そのメールアドレスもう登録されてるよ")
        return redirect(url_for('register_view'))

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # 問題なければ以下
    # user_id = User.create(name, email, hashed_password)
    # print(user_id)

    # session['user_id'] = user_id
    session['email'] = email
    session['hashed_password'] = hashed_password
    session['name'] = name
    print('セッションした')

    return redirect(url_for('syumi_view'))


# 趣味選択ページの表示
@app.route('/hobbies', methods=['GET'])
def syumi_view():
    # user_idの登録があれば、timeline_viewへ、なければsyumiページへ
    if session.get('user_id') is not None:
        return redirect(url_for('timeline_view'))
    return render_template('post/syumi.html')

# 趣味選択ページの新規登録処理
@app.route('/hobbies', methods=['POST'])
def syumi_process():
    # 1個以上のチェックがついたチェックボックス項目を取得
    hobbies = request.form.getlist('hobby')
    # 前ページからのemail, password, nameの取得
    email = session.get('email')
    hashed_password = session.get('hashed_password')
    name = session.get('name')

    # user_idの取得
    user_id = User.create(name, email, hashed_password)
    print(user_id)

    # 趣味の保存
    for hobby in hobbies:
        UserHobby.create(user_id, hobby)


    # user_idを取得
    session['user_id'] = user_id
    session['hobbies'] = hobbies
    print('2ページ目もセッションした')

    return redirect(url_for('timeline_view'))

# url_forのテスト
# ログインページの表示
@app.route('/login', methods=['GET'])
def login_view():
    if session.get('user_id') is not None:
        return redirect(url_for('timeline_view'))
    return render_template('auth/login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    print('login_process start')
    email = request.form.get('email')
    password = request.form.get('password')
    print(email)
    print(password)


    # 空欄チェック
    if email == '' or password == '':
        print('空チェック')
        flash("メールアドレスかパスワードが入ってないよ", 'error')
        print("メールアドレスかパスワードが入ってないよ", 'error')
    else:
        print('db接続前')
        user = User.find_by_email(email)
        print(user)
        if user is None:
            flash("メールアドレスが違うよ", 'error')
            print("メールアドレスが違うよ", 'error')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user['password']:
                flash("パスワードが違うよ", 'error')
                print("パスワードが違うよ", 'error')
            else:
                session['user_id'] = user['id']
                return redirect(url_for('timeline_view'))
    return redirect(url_for('login_view'))
                
# タイムラインページの表示
@app.route('/timeline', methods=['GET'])
def timeline_view():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    else:
        posts = Post.get_all()
        user_name = User.get_name_by_id(user_id)
        # print(posts)
        print(user_name)
        for post in posts:
            utc_time = post['created_at']
            utc_time = utc_time.replace(tzinfo=timezone.utc) # UTCとして明示
            jst_time = utc_time.astimezone(jst) # JSTに変換
            # print(post)
            post['created_at'] = jst_time.strftime('%Y-%m-%d %H:%M')
            # print(post['created_at'])
            post['user_name'] = User.get_name_by_id(post['user_id'])
            # print(post['user_name'])
        return render_template('post/timeline.html', posts=posts, user_id=user_id, login_user_name=user_name)
    # posts = Post.get_all()
    # for post in posts:
    #     post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
    #     post['user_name'] = User.get_name_by_id(post['user_id'])
    # return render_template('post/timeline.html')
    # return render_template('post/timeline.html', posts=posts, user_id=user_id)

# 投稿処理：create関数→models.py
@app.route('/posts', methods=['POST'])
def create_post():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    content = request.form.get('text', '').strip() 
    from_page = request.form.get('from_page') # 投稿した画面へ戻る用
    if content == '':
        # flash('投稿内容が空です','error')
        print('投稿内容が空です','error')
        if from_page == 'mypage':
            return redirect(url_for('home_view'))
        else:
            return redirect(url_for('timeline_view'))
    
    hobby_id = 1  # 仮固定
    Post.create(user_id, content, hobby_id)
    # flash('投稿が完了しました','success')
    print('投稿が完了しました','success')
    if from_page == 'mypage':
        return redirect(url_for('home_view'))
    else:
        return redirect(url_for('timeline_view'))

#投稿タグ一覧選択を表示
# @app.route('/tags', methods=['GET'])
# def tags_view():
#     return render_template('post/timeline.html')

#ホーム画面表示
@app.route('/home', methods=['GET'])
def home_view():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    else:
        posts = Post.get_by_user(user_id)
        user_name = User.get_name_by_id(user_id)
        post_count = Post.count_by_user(user_id)
        user_created = User.find_by_id(user_id)
        user_created = user_created.replace(tzinfo=timezone.utc)
        user_created_jst = user_created.astimezone(jst)
        today = datetime.now(jst)
        days = (today.date() - user_created_jst.date()).days
        for post in posts:
            utc_time = post['created_at']
            utc_time = utc_time.replace(tzinfo=timezone.utc) # UTCとして明示
            jst_time = utc_time.astimezone(jst) # JSTに変換
            post['created_at'] = jst_time.strftime('%Y-%m-%d %H:%M')
            post['user_name'] = User.get_name_by_id(post['user_id'])
            print(post)
        return render_template('post/home.html', my_posts=posts, user_id=user_id, login_user_name=user_name, post_count=post_count, days=days)

# 投稿削除処理
@app.route('/posts/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))

    post = Post.find_by_id(post_id)
    if post is None:
        abort(404)

    # 本人チェック
    if post['user_id'] != user_id:
        abort(403)

    Post.delete(post_id)
    flash('投稿を削除しました', 'success')
    return redirect(url_for('home_view'))


#保存画面表示
@app.route('/list', methods=['GET'])
def list_view():
    return render_template('post/list.html')

# ぽめテストページの表示
@app.route('/pome', methods=['GET'])
def pome_view():
    return render_template('error/pome.html')

# ぽめテストページの表示（JSON版）
@app.route('/pomeJSON', methods=['GET'])
def pomeJSON_view():
    return render_template('error/pomeJSON.html')

# ログアウト
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login_view'))


# 404エラー確認用
@app.route('/test', methods=['GET'])
def error_404_test_view():
    abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404

# Pythonファイルとして直接実行された場合にサーバーを起動
if __name__ == '__main__':
    # host='0.0.0.0'で外部からのアクセスも可能に（デフォルトは'127.0.0.1'）
    # port=5000はデフォルトポート
    app.run(debug=True, host='0.0.0.0')


# ブラウザなしでターミナルでブラウザの内容を確認する
# curl -X POST http://localhost:55002/login \
#     -d "email=test@example.com" \
#     -d "password=secret"