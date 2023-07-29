
def create_table(conn):
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS chatlog (id INTEGER PRIMARY KEY, userid INTEGER, role TEXT, content TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, userid INTEGER, otp TEXT, verified INTEGER)')
    conn.commit()

def add_chatlog(conn, userid, role, content):
    c = conn.cursor()
    c.execute('INSERT INTO chatlog (userid, role, content) VALUES (?, ?, ?)', (userid, role, content))
    conn.commit()

def get_recent_chatlog(conn, userid, limit=10):
    c = conn.cursor()
    c.execute('SELECT * FROM chatlog WHERE userid=? ORDER BY id ASC LIMIT ? OFFSET (SELECT COUNT(*) FROM chatlog) - ?', (userid, limit, limit))
    return c.fetchall()

def delete_chatlog(conn, userid):
    c = conn.cursor()
    c.execute('DELETE FROM chatlog WHERE userid=?', (userid))

def confirm_user(conn, userid, otp):
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE userid=? AND otp=?', (userid, otp))
    if c.fetchone():
        c.execute('UPDATE users SET verified=1 WHERE userid=?', (userid,))
        conn.commit()
        return True
    return False

def add_user(conn, userid, otp):
    c = conn.cursor()
    c.execute('INSERT INTO users (userid, otp, verified) VALUES (?, ?, ?)', (userid, otp, 0))
    conn.commit()

def get_user(conn, userid):
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE userid=?', (userid,))
    return c.fetchone()

def update_user(conn, userid, otp):
    c = conn.cursor()
    c.execute('UPDATE users SET otp=? WHERE userid=?', (otp, userid))
    conn.commit()