import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import date, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'spendly.db')


def get_db():
    """Get a database connection. Uses Flask's g object if available for
    per-request connection reuse, otherwise creates a standalone connection."""
    try:
        from flask import g
        if 'db' not in g:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.execute("PRAGMA cache_size = -8000")  # 8MB cache
            g.db = conn
        return g.db
    except RuntimeError:
        # Outside Flask request context (e.g. init_db, seed_db)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA synchronous = NORMAL")
        conn.execute("PRAGMA cache_size = -8000")
        return conn


def close_db(exception=None):
    """Close the database connection stored in Flask g at end of request."""
    try:
        from flask import g
        db = g.pop('db', None)
        if db is not None:
            db.close()
    except RuntimeError:
        pass


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        phone TEXT DEFAULT '',
        age INTEGER DEFAULT 0,
        gender TEXT DEFAULT '',
        country TEXT DEFAULT '',
        currency TEXT DEFAULT 'INR',
        language TEXT DEFAULT 'English',
        avatar_url TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL DEFAULT 0,
        period TEXT NOT NULL DEFAULT 'monthly',
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date DATE NOT NULL,
        description TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        platform TEXT NOT NULL,
        cost REAL NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE,
        duration_months INTEGER DEFAULT 1,
        is_active INTEGER DEFAULT 1,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        target_amount REAL NOT NULL,
        saved_amount REAL DEFAULT 0,
        deadline DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )''')

    # Performance indexes
    c.execute('CREATE INDEX IF NOT EXISTS idx_expenses_user_date ON expenses(user_id, date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_expenses_user_cat ON expenses(user_id, category)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_subs_user ON subscriptions(user_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_goals_user ON goals(user_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_budgets_user ON budgets(user_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')

    conn.commit()
    # Only close if outside Flask context
    try:
        from flask import g
    except RuntimeError:
        conn.close()


def seed_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as cnt FROM users")
    if c.fetchone()['cnt'] > 0:
        try:
            from flask import g
        except RuntimeError:
            conn.close()
        return

    pw = generate_password_hash("password123")
    c.execute("""INSERT INTO users (name,email,password_hash,phone,age,gender,country,currency,language)
                 VALUES (?,?,?,?,?,?,?,?,?)""",
              ("Alex Johnson", "demo@spendly.com", pw, "+91-9876543210", 25, "Male", "India", "INR", "English"))
    uid = c.lastrowid
    c.execute("INSERT INTO budgets (user_id,amount,period) VALUES (?,?,?)", (uid, 15000.0, "monthly"))

    today = date.today()
    expenses = [
        (uid, 2500, "Food", (today - timedelta(days=1)).isoformat(), "Weekly groceries"),
        (uid, 350, "Food", (today - timedelta(days=3)).isoformat(), "Restaurant dinner"),
        (uid, 120, "Food", (today - timedelta(days=6)).isoformat(), "Street food"),
        (uid, 800, "Transport", (today - timedelta(days=2)).isoformat(), "Uber rides"),
        (uid, 450, "Transport", (today - timedelta(days=8)).isoformat(), "Metro pass"),
        (uid, 5000, "Housing", (today - timedelta(days=0)).isoformat(), "Monthly rent share"),
        (uid, 999, "Entertainment", (today - timedelta(days=4)).isoformat(), "Concert tickets"),
        (uid, 299, "Entertainment", (today - timedelta(days=7)).isoformat(), "Movie night"),
        (uid, 1500, "Shopping", (today - timedelta(days=5)).isoformat(), "New shoes"),
        (uid, 200, "Healthcare", (today - timedelta(days=9)).isoformat(), "Pharmacy"),
        (uid, 650, "Education", (today - timedelta(days=10)).isoformat(), "Online course"),
        (uid, 180, "Other", (today - timedelta(days=11)).isoformat(), "Miscellaneous"),
    ]
    c.executemany("INSERT INTO expenses (user_id,amount,category,date,description) VALUES (?,?,?,?,?)", expenses)

    subs = [
        (uid, "Netflix", 199, (today - timedelta(days=60)).isoformat(), (today + timedelta(days=300)).isoformat(), 12, 1),
        (uid, "Spotify", 119, (today - timedelta(days=30)).isoformat(), (today + timedelta(days=335)).isoformat(), 12, 1),
        (uid, "Gym Membership", 1500, (today - timedelta(days=90)).isoformat(), (today + timedelta(days=275)).isoformat(), 12, 1),
        (uid, "Adobe Creative Cloud", 1675, (today - timedelta(days=120)).isoformat(), (today - timedelta(days=30)).isoformat(), 3, 0),
    ]
    c.executemany("INSERT INTO subscriptions (user_id,platform,cost,start_date,end_date,duration_months,is_active) VALUES (?,?,?,?,?,?,?)", subs)

    goals = [
        (uid, "Emergency Fund", 100000, 25000, (today + timedelta(days=365)).isoformat()),
        (uid, "New Laptop", 80000, 12000, (today + timedelta(days=180)).isoformat()),
        (uid, "Vacation Trip", 50000, 5000, (today + timedelta(days=270)).isoformat()),
    ]
    c.executemany("INSERT INTO goals (user_id,title,target_amount,saved_amount,deadline) VALUES (?,?,?,?,?)", goals)

    conn.commit()
    try:
        from flask import g
    except RuntimeError:
        conn.close()


if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Seeding demo data...")
    seed_db()
    print("Done!")
