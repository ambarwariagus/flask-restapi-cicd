from app import get_db


def get_all_users():
    conn = get_db()
    rows = conn.execute("SELECT * FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user_by_id(user_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_user(username, email, full_name):
    conn = get_db()
    try:
        cursor = conn.execute(
            "INSERT INTO users (username, email, full_name) VALUES (?, ?, ?)",
            (username, email, full_name),
        )
        conn.commit()
        user_id = cursor.lastrowid
    finally:
        conn.close()
    return get_user_by_id(user_id)


def update_user(user_id, username, email, full_name):
    conn = get_db()
    try:
        conn.execute(
            "UPDATE users SET username = ?, email = ?, full_name = ? WHERE id = ?",
            (username, email, full_name, user_id),
        )
        conn.commit()
    finally:
        conn.close()
    return get_user_by_id(user_id)


def delete_user(user_id):
    conn = get_db()
    try:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
    finally:
        conn.close()
