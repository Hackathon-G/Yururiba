from flask import abort
import pymysql
from util.DB import DB


# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


# ユーザークラス
class User:
    @classmethod
    def create(cls, user_name, email, password):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (user_name, email, password) VALUES (%s, %s, %s);"
                cur.execute(sql, (user_name, email, password))
                conn.commit()
                # AUTO_INCREMENT された id を返す
                return cur.lastrowid
        except pymysql.Error as e:
            print(f'create@Userのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_email(cls, email):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s;"
                cur.execute(sql, (email,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f'find_by_email@Userのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_name_by_id(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT user_name FROM users WHERE id=%s;"
                cur.execute(sql, (user_id,))
                user = cur.fetchone()
            return user['user_name'] if user else None
        except pymysql.Error as e:
            print(f'get_name_by_id@Userのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_id(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT created_at FROM users WHERE id=%s;"
                cur.execute(sql, (user_id,))
                user = cur.fetchone()
            return user['created_at'] if user else None
        except pymysql.Error as e:
            print(f'find_by_id@Userのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

# Hobbyクラス
class Hobby:
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM hobbies ORDER BY hobby_id ASC;"
                cur.execute(sql)
                hobbies = cur.fetchall()
            return hobbies
        except pymysql.Error as e:
            print(f'get_all@Hobbyのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

class UserHobby:
    @classmethod
    def create(cls, user_id, hobby_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO user_hobbies (user_id, hobby_id) VALUES (%s, %s);"
                cur.execute(sql, (user_id, hobby_id))
            conn.commit()
        except pymysql.Error as e:
            print(f'create@UserHobbyのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_hobbies_by_user_id(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                SELECT h.hobby_id, h.hobby_name
                FROM hobbies h
                JOIN user_hobbies uh
                    ON h.hobby_id = uh.hobby_id
                WHERE uh.user_id = %s
                """
                cur.execute(sql, (user_id,))
                hobbies = cur.fetchall()
            return hobbies if hobbies else None
        except pymysql.Error as e:
            print(f'create@UserHobbyのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    
# Postsクラス
class Post:
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                # sql = "SELECT * FROM posts WHERE  deleted_at IS NULL ORDER BY created_at DESC;"
                sql = " SELECT p.id, p.user_id, p.post_text, p.created_at, h.hobby_name, u.user_name FROM posts p JOIN hobbies h ON p.hobby_id = h.hobby_id JOIN users u ON p.user_id = u.id WHERE p.deleted_at IS NULL ORDER BY p.created_at DESC;"
                cur.execute(sql)
                posts = cur.fetchall()
            return posts
        except pymysql.Error as e:
            print(f'get_all@Postのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def create(cls, user_id, hobby_id, post_text):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO posts (user_id, hobby_id, post_text) VALUES (%s, %s, %s);"
                cur.execute(sql, (user_id, hobby_id, post_text))
                conn.commit()
        except pymysql.Error as e:
            print(f'create@Postのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, post_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE posts SET deleted_at = NOW() WHERE id = %s;"
                cur.execute(sql, (post_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'delete@Postのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_id(cls, post_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM posts WHERE id=%s AND deleted_at IS NULL;"
                cur.execute(sql, (post_id,))
                post = cur.fetchone()
            return post
        except pymysql.Error as e:
            print(f'find_by_id@Postのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # ユーザーの投稿を取得
    @classmethod
    def get_by_user(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                # sql = "SELECT * FROM posts WHERE user_id = %s AND deleted_at IS NULL ORDER BY created_at DESC;"
                sql = """
                SELECT
                    p.id,
                    p.user_id,
                    p.post_text,
                    p.created_at,
                    h.hobby_name,
                    u.user_name
                FROM posts p
                JOIN hobbies h
                    ON p.hobby_id = h.hobby_id
                JOIN users u
                    ON p.user_id = u.id
                WHERE p.deleted_at IS NULL
                AND p.user_id = %s
                ORDER BY p.created_at DESC;
                """
                cur.execute(sql, (user_id,))
                posts = cur.fetchall()
            return posts
        except pymysql.Error as e:
            print(f'get_by_user@Postのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # ユーザーの投稿数カウント
    @classmethod
    def count_by_user(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT COUNT(*) FROM posts WHERE user_id = %s AND deleted_at IS NULL ORDER BY created_at DESC;"
                cur.execute(sql, (user_id,))
                result = cur.fetchone()
                posts = result['COUNT(*)']
            return posts
        except pymysql.Error as e:
            print(f'count_by_user@Postのエラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

# Commentクラス
# class Comment:
#     @classmethod
#     def create(cls, user_id, post_id, post_text, post_image):
#         conn = db_pool.get_conn()
#         try:
#             with conn.cursor() as cur:
#                 sql = "INSERT INTO comments (user_id, post_id, post_text, post_image) VALUES (%s, %s, %s);"
#                 cur.execute(sql, (user_id, post_id, post_text, post_image))
#                 conn.commit()
#         except pymysql.Error as e:
#             print(f'エラーが発生しています：{e}')
#             abort(500)
#         finally:
#             db_pool.release(conn)
#     @classmethod
#     def get_by_post_id(cls, post_id):
#         conn = db_pool.get_conn()
#         try:
#             with conn.cursor() as cur:
#                 sql = "SELECT * FROM comments WHERE post_id=%s ORDER BY created_at DESC;"
#                 cur.execute(sql, (post_id,))
#                 comments = cur.fetchall()
#             return comments
#         except pymysql.Error as e:
#             print(f'エラーが発生しています：{e}')
#             abort(500)
#         finally:
#             db_pool.release(conn)