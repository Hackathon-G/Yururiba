from flask import Flask, request, redirect, render_template, session, flash, abort, url_for, make_response
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import hashlib
import uuid
import re

from models import User, Post, Hobby, UserHobby

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
    user_id = User.create(name, email, hashed_password)
    print(user_id)

    session['user_id'] = user_id
    print('セッションした')

    return redirect(url_for('syumi_view'))


# 趣味選択ページの表示
@app.route('/hobbies', methods=['GET'])
def syumi_view():
    hobbies = Hobby.get_all()
    print(f'{hobbies}を表示')
    # user_idの登録があれば、timeline_viewへ、なければsyumiページへ
    # if session.get('user_id') is not None:
    #     return redirect(url_for('timeline_view'))
    # return render_template('post/syumi.html', hobbies=hobbies)
    return render_template('post/syumi.html', hobbies=hobbies)

# 趣味選択ページの新規登録処理
@app.route('/hobbies', methods=['POST'])
def syumi_process():
    # 前ページからuser_idの受け渡し
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('register_view'))
    
    user_id = int(user_id)
    print(f'user_idは{user_id}です')
        
    # 1個以上のチェックがついたチェックボックス項目を取得
    selected_hobby_ids = request.form.getlist('hobby')
    if not selected_hobby_ids:
        flash('趣味を選んでね')
        print('趣味を選んでね')
        return redirect(url_for('syumi_view'))
    else:
        for hobby_id in selected_hobby_ids:
            user_hobby = UserHobby.create(user_id,int(hobby_id))
            print(user_hobby)
            session['hobby_id'] = hobby_id


    return redirect(url_for('timeline_view'))


# ログインページの表示
@app.route('/login', methods=['GET'])
def login_view():
    if session.get('user_id') is not None:
        return redirect(url_for('/timeline_view'))
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
        print(posts)
        for post in posts:
            print(post)
            post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
            print(post['created_at'])
            post['user_name'] = User.get_name_by_id(post['user_id'])
            print(post['user_name'])
        return render_template('post/timeline.html', posts=posts, user_id=user_id)

# 投稿処理：create関数→models.py     実装中
@app.route('/posts', methods=['POST'])
def create_post():
    user_id = session.get('user_id')
    print(f'投稿処理のuser_idは{user_id}です')
    if user_id is None:
        return redirect(url_for('login_view'))
    
    hobby_id = session.get('hobby_id')
    print(f'投稿処理のhobby_idは{hobby_id}です')
    if hobby_id is None:
        return redirect(url_for('register_view'))
    

    post_text = request.form.get('text', '').strip() 
    if post_text == '':
        flash('投稿内容が空です','error')
        print('投稿内容が空です','error')
        return redirect(url_for('timeline_view'))
    Post.create(user_id, hobby_id, post_text)
    flash('投稿が完了しました','success')
    print('投稿が完了しました','success')
    return redirect(url_for('timeline_view'))

#投稿タグ一覧選択を表示
# @app.route('/tags', methods=['GET'])
# def tags_view():
#     return render_template('post/timeline.html')

# ホーム画面表示
@app.route('/home', methods=['GET'])
def home_view():
    return render_template('post/home.html')

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
def logout_view():
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