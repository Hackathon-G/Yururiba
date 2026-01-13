# セットアップ 🚀

## ① リポジトリのクローン

リポジトリをクローンします。

```
git clone git@github.com:Hackathon-G/Yururiba.git
```

ディレクトリに移動します。

```
cd Yururiba
```

## ② 環境変数ファイル（.env）の作成

- Mac、Windows(PowerShell、Git Bash)の場合

```
cp .env.example .env
```

- Windows(コマンドプロンプト)の場合

```
copy .env.example .env
```

## ③Docker コンテナのビルドと起動

### コンテナのビルド

docker-compose.yml を元にコンテナイメージをビルドします。  
初回または依存パッケージを更新したときに実行してください。  
※docker-compose.yml があるディレクトリで実行してください。

```
docker compose build
```

## 現時点

※ 現時点では Flask / app.py は未接続のため、
localhost での確認はできません。
画面構成・遷移イメージ確認用の仮実装です。

HTML の確認は、VSCode の拡張機能等をご利用ください。
（例：Live Preview）

### ディレクトリ構成

````
.
├── Docker
│   ├── Flask
│   │   └── Dockerfile             # Flaskアプリを動かすためのDocker設定ファイル
│   └── MySQL
│       ├── Dockerfile             # MySQL（データベース）を動かすためのDocker設定ファイル
│       ├── init.sql               # MySQL起動時に最初に実行されるSQLファイル
│       └── my.cnf                 # MySQLの細かい設定を書くファイル
├── docker-compose.yml             # FlaskとMySQLをまとめて起動する設定ファイル
├── requirements.txt               # Pythonで使うライブラリ一覧
└── SNSApp                         # サンプルSNSアプリの本体
    ├── app.py                     # アプリのメインファイル
    ├── models.py                  # データベースとやり取りする処理をまとめたファイル
    ├── static                     # CSSや画像など、見た目に関係用ディレクトリ
    │   └── css
    ├── templates                   # HTML用ディレクトリ
    │   ├── auth
    │   │   ├── base.html          # 全画面共通の土台となるHTML
    │   │   ├── login.html          # ログイン画面HTML
    │   │   └── signup.html         # 新規登録画面HTML
    │   ├── common
    │   ├── error
    │   └── post
    │       ├── syumi.html         # 趣味選択画面HTML
    │       └── timeline.html         # タイムライン画面HTML
    └── util
        └── DB.py                   # データベース接続まわりをまとめたファイル
        ```
````

※ Docker 構成について  
Docker でエラーなく起動することを優先し、  
現時点ではサンプルアプリの構成を一部残しています。
