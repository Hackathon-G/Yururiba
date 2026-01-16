from flask import Flask

# Flaskアプリケーションのインスタンスを作成

app = Flask(__name__)

# ルートURL('/')へのGETリクエストを処理する関数を定義

@app.route('/')

def hello_world():

    return 'Hello, Flask!'

# Pythonファイルとして直接実行された場合にサーバーを起動

if __name__ == '__main__':

    # host='0.0.0.0'で外部からのアクセスも可能に（デフォルトは'127.0.0.1'）

    # port=5000はデフォルトポート

    app.run(debug=True, host='0.0.0.0')