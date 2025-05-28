<<<<<<< HEAD
from flask import abort  # HTTPステータスコードをクライアント側へ表示させるライブラリ
import pymysql          # SQL操作のライブラリ
from util.DB import DB  # 作成したDBファイルをimport

# 初期起動時にコネクションプールを作成し接続を確立
# envファイルからユーザー名やDB等を取得や同時接続最大数の設定、DB空の戻り値を辞書型に設定などを定義している
db_pool = DB.init_db_pool()

# ユーザークラス


class User:

    # ログイン時に、emailからユーザー情報を検索し、ユーザー情報を辞書型で返している
    @classmethod
    def find_user(cls, email):
        # データベース接続プールからコネクションを取得する（DB.pyファイルのこと）
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s;"
                cur.execute(sql, (email))
                user = cur.fetchone()   # 設定した辞書型で取得
            return user
        except pymysql.Error as e:
            print(f'エラーが発生してます：{e}')
            abort(500)

        finally:
            db_pool.release(conn)

    # サインアップ処理

    @classmethod
    def create_user(cls, user_id, company_id, name, email, password):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (user_id, company_id, user_name, email, pass) VALUES (%s,%s,%s,%s,%s)"
                cur.execute(sql, (user_id, company_id, name, email, password))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生してます：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # 会社情報の取得と登録

    @classmethod
    def find_company(cls, company_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM companies WHERE company_name=%s;"
                cur.execute(sql, (company_name))
                company = cur.fetchone()
                # 会社情報があれば返し、無ければ登録して返す
                if company is None:
                    sql = "INSERT INTO companies (company_name) VALUES (%s);"
                    cur.execute(sql, (company_name))
                    conn.commit()  # 変更をDBに反映

                    # 登録した会社情報を取得
                    sql = "SELECT * FROM companies WHERE company_name=%s"
                    cur.execute(sql, (company_name))
                    company = cur.fetchone()
                return company['company_id']

        except pymysql.Error as e:
            print(f'エラーが発生してます：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


# ルームクラス
class Room:
    # ルーム作成メソッド
    @classmethod
    def create(cls, user_id, room_id, new_room_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO rooms (room_id, room_name) VALUES (%s, %s);"
                cur.execute(sql, (room_id, new_room_name,))
                sql = "INSERT INTO room_members (user_id, room_id, privilege) VALUES (%s, %s, %s)"
                cur.execute(sql, (user_id, room_id, "admin",))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # メンバー追加メソッド

    @classmethod
    def add_member(cls, member_id, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO room_members (user_id, room_id, privilege) VALUES (%s, %s, %s)"
                cur.execute(sql, (member_id, room_id, "member",))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # メンバー削除メソッド

    @classmethod
    def remove_member(cls, member_id, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM room_members WHERE room_id=%s and member_id=%s;"
                cur.execute(sql, (room_id, member_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # 自身が所属するルーム情報全て取得

    @classmethod
    def get_all(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM room_members WHERE user_id=%s"
                sql = """
                    SELECT rm.*,r.*
                    FROM room_members AS rm
                    INNER JOIN rooms AS r ON rm.room_id = r.room_id
                    WHERE rm.user_id=%s 
                    ORDER BY last_accessed_at DESC;
                   """
                cur.execute(sql, (user_id))
                rooms = cur.fetchall()
                return rooms
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # ルームの所属メンバー一覧取得

    @classmethod
    def get_all_members(cls, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM room_members where room_id=%s;"
                cur.execute(sql, (room_id,))
                room_members = cur.fetchall()
                return room_members
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    #

    @classmethod
    def find_by_id(cls, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM rooms WHERE room_id=%s;"
                cur.execute(sql, (room_id,))
                room = cur.fetchone()
                return room
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    #

    @classmethod
    def find_by_name(cls, room_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM rooms WHERE room_name=%s;"
                cur.execute(sql, (room_name,))
                room = cur.fetchone()
                return room
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # ルーム編集

    @classmethod
    def update(cls, new_room_name, new_room_visibility, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE rooms SET name=%s, visibility=%s, updated_at=Now() WHERE room_id=%s;"
                cur.execute(sql, (new_room_name,
                            new_room_visibility, room_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # ルーム削除

    @classmethod
    def delete(cls, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM rooms WHERE room_id=%s;"
                cur.execute(sql, (room_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


# メッセージクラス
class Message:
    # メッセージ作成
    @classmethod
    def create(cls, user_id, room_id, original_message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO messages(room_member_id, room_id, original_message) VALUES(%s, %s, %s)"
                cur.execute(sql, (user_id, room_id, original_message,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # ルームのメッセージ一覧取得

    @classmethod
    def get_all(cls, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                   SELECT m.message_id, u.user_name, m.original_message, m.translated_message 
                   FROM messages AS m 
                   INNER JOIN room_members AS r ON m.room_member_id = r.room_member_id 
                   INNER JOIN users AS u ON u.user_id = r.user_id 
                   WHERE r.room_id = %s 
                   ORDER BY message_id ASC;
               """
                cur.execute(sql, (room_id,))
                messages = cur.fetchall()
                return messages
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # メッセージの編集

    @classmethod
    def update(cls, message_id, new_message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE messages SET original_message=%s, updated_at=Now() WHERE message_id=%s;"
                cur.execute(sql, (new_message, message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # メッセージの翻訳

    @classmethod
    def translate(cls, message_id, translated_message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE messages SET translated_message=%s, updated_at=Now() WHERE message_id=%s;"
                cur.execute(sql, (translated_message, message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # メッセージの削除

    @classmethod
    def delete(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM messages WHERE id=%s;"
                cur.execute(sql, (message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


# ファイルクラス
class File:
    # ファイルの作成
    @classmethod
    def create(cls, message_id, display_name, file_path):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO files(message_id, display_name, file_path) VALUES(%s, %s, %s)"
                cur.execute(sql, (message_id, display_name, file_path,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # ファイルの検索

    @classmethod
    def find_by_id(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM files WHERE message_id=%s;"
                cur.execute(sql, (message_id,))
                room = cur.fetchone()
                return room
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # ファイル情報の編集

    @classmethod
    def update(cls, new_display_name, new_file_path, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE rooms SET display_name=%s, file_path=%s, updated_at=Now() WHERE room_id=%s;"
                cur.execute(sql, (new_display_name,
                            new_file_path, message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # ファイルの削除
    @classmethod
    def delete(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM files WHERE message_id=%s;"
                cur.execute(sql, (message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
=======
from flask import abort
import pymysql
from util.DB import DB


# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


# ユーザークラス
class User:
    @classmethod
    def create(cls, uid, name, email, password):
        # データベース接続プールからコネクションを取得する
        conn = db_pool.get_conn()
        try:
            # コネクションからカーソル（操作用のオブジェクト）を取得する
            with conn.cursor() as cur:
                sql = "INSERT INTO users (uid, user_name, email, password) VALUES (%s, %s, %s, %s);"
                # SQLを実行し、パラメータ（uid, name, email, password）を埋め込む
                cur.execute(sql, (uid, name, email, password,))
                # データベースに変更を反映（保存）する
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
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
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


# ルームクラス
class room:
    @classmethod
    def create(cls, user_id, room_id, new_room_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO rooms (room_id, room_name) VALUES (%s, %s);"
                cur.execute(sql, (room_id, new_room_name,))
                sql = "INSERT INTO room_members (user_id, room_id, privilege) VALUES (%s, %s, %s)"
                cur.execute(sql, (user_id, room_id, "admin",))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def add_member(cls, member_id, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO room_members (user_id, room_id, privilege) VALUES (%s, %s, %s)"
                cur.execute(sql, (member_id, room_id, "member",))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def remove_member(cls, member_id, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM room_members WHERE room_id=%s and member_id=%s;"
                cur.execute(sql, (room_id, member_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM rooms;"
                cur.execute(sql)
                rooms = cur.fetchall()
                return rooms
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_all_members(cls, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM room_members where room_id=%s;"
                cur.execute(sql, (room_id,))
                room_members = cur.fetchall()
                return room_members
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_id(cls, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM rooms WHERE room_id=%s;"
                cur.execute(sql, (room_id,))
                room = cur.fetchone()
                return room
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_name(cls, room_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM rooms WHERE room_name=%s;"
                cur.execute(sql, (room_name,))
                room = cur.fetchone()
                return room
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, new_room_name, new_room_visibility, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE rooms SET name=%s, visibility=%s, updated_at=Now() WHERE room_id=%s;"
                cur.execute(sql, (new_room_name,
                            new_room_visibility, room_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM rooms WHERE room_id=%s;"
                cur.execute(sql, (room_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


# ファイルクラス
class File:
    @classmethod
    def create(cls, message_id, display_name, file_path):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO files(message_id, display_name, file_path) VALUES(%s, %s, %s)"
                cur.execute(sql, (message_id, display_name, file_path,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_id(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM files WHERE message_id=%s;"
                cur.execute(sql, (message_id,))
                room = cur.fetchone()
                return room
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, new_display_name, new_file_path, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE rooms SET display_name=%s, file_path=%s, updated_at=Now() WHERE room_id=%s;"
                cur.execute(sql, (new_display_name,
                            new_file_path, message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM files WHERE message_id=%s;"
                cur.execute(sql, (message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

# メッセージクラス


class Message:
    @classmethod
    def create(cls, cid, original_message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO messages(uid, cid, original_message) VALUES(%s, %s, %s)"
                cur.execute(sql, (cid, original_message,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_all(cls, room_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                   SELECT m.message_id, u.user_name, m.original_message, m.translated_message 
                   FROM messages AS m 
                   INNER JOIN room_members AS r ON m.room_member_id = r.room_member_id 
                   INNER JOIN users AS u ON u.user_id = r.user_id 
                   WHERE r.room_id = %s 
                   ORDER BY message_id ASC;
               """
                cur.execute(sql, (room_id,))
                messages = cur.fetchall()
                return messages
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, message_id, translated_message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE messages SET translated_message=%s, updated_at=Now() WHERE message_id=%s;"
                cur.execute(sql, (translated_message, message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM messages WHERE id=%s;"
                cur.execute(sql, (message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
>>>>>>> c9cd171dfeebc393b6176e2087e8a468560b9994
