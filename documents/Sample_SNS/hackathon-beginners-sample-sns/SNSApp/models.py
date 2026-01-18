from flask import abort
import pymysql
from util.DB import DB
# abort：エラー画面（403/404など）表示
# pymysql：pythonでMySQLを使う

# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()

# ユーザークラス
class User:
    @classmethod
    # ユーザー作成
    def create(cls, name, email, password):
        # コネクションプールから、接続を借りる
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s);"
                cur.execute(sql, (name, email, password))
                conn.commit()
                # AUTO_INCREMENT された id を返す
                return cur.lastrowid
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally: # 最後に接続解除（つなぎっぱなし防止）
            db_pool.release(conn)

    @classmethod
    # メールでユーザー検索
    def find_by_email(cls, email):
        # コネクションプールから、接続を借りる
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s;"
                cur.execute(sql, (email,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally: # 最後に接続解除（つなぎっぱなし防止）
            db_pool.release(conn)

    @classmethod
    # IDから名前取得
    def get_name_by_id(cls, user_id):
        # コネクションプールから、接続を借りる
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT name FROM users WHERE id=%s;"
                cur.execute(sql, (user_id,))
                user = cur.fetchone()
            return user['name'] if user else None
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally: # 最後に接続解除（つなぎっぱなし防止）
            db_pool.release(conn)

# Postsクラス
class Post:
    @classmethod
    # 投稿一覧を取得
    def get_all(cls):
        # コネクションプールから、接続を借りる
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM posts WHERE  deleted_at IS NULL ORDER BY created_at DESC;"
                cur.execute(sql)
                posts = cur.fetchall()
            return posts
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally: # 最後に接続解除（つなぎっぱなし防止）
            db_pool.release(conn)

    @classmethod
    # 投稿を作成
    def create(cls, user_id, content):
        # コネクションプールから、接続を借りる
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO posts (user_id, content) VALUES (%s, %s);"
                cur.execute(sql, (user_id, content))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally: # 最後に接続解除（つなぎっぱなし防止）
            db_pool.release(conn)

    @classmethod
    # 投稿を削除
    def delete(cls, post_id):
        # コネクションプールから、接続を借りる
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE posts SET deleted_at = NOW() WHERE id = %s;"
                cur.execute(sql, (post_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally: # 最後に接続解除（つなぎっぱなし防止）
            db_pool.release(conn)

    @classmethod
    # 投稿のidを取得
    def find_by_id(cls, post_id):
        # コネクションプールから、接続を借りる
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM posts WHERE id=%s AND deleted_at IS NULL;"
                cur.execute(sql, (post_id,))
                post = cur.fetchone()
            return post
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally: # 最後に接続解除（つなぎっぱなし防止）
            db_pool.release(conn)

# Commentクラス
class Comment:
    @classmethod
    # コメントを作成
    def create(cls, user_id, post_id, content):
        # コネクションプールから、接続を借りる
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO comments (user_id, post_id, content) VALUES (%s, %s, %s);"
                cur.execute(sql, (user_id, post_id, content))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally: # 最後に接続解除（つなぎっぱなし防止）
            db_pool.release(conn)
    @classmethod
    # 投稿のidを取得（どの投稿に対するコメントなのかを判別）
    def get_by_post_id(cls, post_id):
        # コネクションプールから、接続を借りる
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM comments WHERE post_id=%s ORDER BY created_at DESC;"
                cur.execute(sql, (post_id,))
                comments = cur.fetchall()
            return comments
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally: # 最後に接続解除（つなぎっぱなし防止）
            db_pool.release(conn)