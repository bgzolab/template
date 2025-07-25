import sqlite3

def init_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def create_table(conn):
    sql = '''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    );'''
    conn.execute(sql)
    conn.commit()

def insert_user(conn, name, age):
    sql = 'INSERT INTO users (name, age) VALUES (?, ?);'
    conn.execute(sql, (name, age))
    conn.commit()

def update_user(conn, user_id, new_age):
    sql = 'UPDATE users SET age = ? WHERE id = ?;'
    conn.execute(sql, (new_age, user_id))
    conn.commit()

def query_users(conn):
    sql = 'SELECT id, name, age FROM users;'
    cursor = conn.execute(sql)
    return cursor.fetchall()

def delete_user(conn, user_id):
    sql = 'DELETE FROM users WHERE id = ?;'
    conn.execute(sql, (user_id,))
    conn.commit()

def main():
    db_name = 'demo.db'
    conn = init_db(db_name)
    create_table(conn)

    print('插入数据...')
    insert_user(conn, 'Alice', 23)
    insert_user(conn, 'Bob', 30)

    print('查询数据:')
    users = query_users(conn)
    for user in users:
        print(user)

    print('更新 Bob 的年龄...')
    # 假设 Bob 的 id 是 2
    update_user(conn, 2, 35)

    print('查询数据:')
    users = query_users(conn)
    for user in users:
        print(user)

    print('删除 Alice...')
    # 假设 Alice 的 id 是 1
    delete_user(conn, 1)

    print('最终数据:')
    users = query_users(conn)
    for user in users:
        print(user)

    conn.close()

if __name__ == '__main__':
    main()
