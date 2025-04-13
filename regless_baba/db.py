import sqlite3

DB_NAME = "regless.db"

def init_db():
    """
    アプリ起動時にDBを初期化する。
    テーブルがなければ作成するイメージ。
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # ユーザーテーブル（仮のログイン用カラムなどを含む）
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            birthdate TEXT,
            smoking TEXT,
            drinking TEXT,
            exercise TEXT,
            body_shape TEXT,
            estimated_lifespan INTEGER
        )
    ''')

    # やりたいことテーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS wants (
            want_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            cost INTEGER,
            period TEXT,
            first_step TEXT,
            tag TEXT,
            deadline TEXT,
            is_completed INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    # 他人のやりたいことにLikeを付けるための例示テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            like_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            want_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(want_id) REFERENCES wants(want_id)
        )
    ''')

    conn.commit()
    conn.close()

def insert_user(username, password, birthdate, smoking, drinking, exercise, body_shape, estimated_lifespan):
    """
    ユーザーをDBに登録する処理
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (username, password, birthdate, smoking, drinking, exercise, body_shape, estimated_lifespan)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, password, birthdate, smoking, drinking, exercise, body_shape, estimated_lifespan))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    """
    usernameでユーザーを検索し、そのユーザー情報を返す
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def insert_want(user_id, title, cost, period, first_step, tag, deadline):
    """
    やりたいことをDBに登録する処理
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO wants (user_id, title, cost, period, first_step, tag, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, title, cost, period, first_step, tag, deadline))
    conn.commit()
    conn.close()

def get_wants_by_user(user_id):
    """
    ユーザーのやりたいことをすべて取得
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM wants WHERE user_id=?', (user_id,))
    wants_list = c.fetchall()
    conn.close()
    return wants_list

def complete_want(want_id):
    """
    やりたいことを完了状態に更新
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE wants SET is_completed=1 WHERE want_id=?', (want_id,))
    conn.commit()
    conn.close()

def get_wants_by_tag(tag):
    """
    タグで検索してやりたいことリストを取得する
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # タグを部分一致や完全一致にするかは方針次第。ここでは部分一致
    c.execute('SELECT * FROM wants WHERE tag LIKE ?', ('%' + tag + '%',))
    result = c.fetchall()
    conn.close()
    return result

def add_like(user_id, want_id):
    """
    他人のやりたいことにLikeを追加
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO likes (user_id, want_id) VALUES (?, ?)
    ''', (user_id, want_id))
    conn.commit()
    conn.close()

def get_likes_count(want_id):
    """
    指定のやりたいことに対するLike数を取得
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM likes WHERE want_id=?', (want_id,))
    count = c.fetchone()[0]
    conn.close()
    return count

def get_all_wants():
    query = "SELECT * FROM wants"
    # データベースコネクションやカーソルを利用した処理を実装
    ...
