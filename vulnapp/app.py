from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# ---------------------------
# Setup DB (insecure)
# ---------------------------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("INSERT INTO users VALUES ('admin','password')")
    conn.commit()
    conn.close()

init_db()

# ---------------------------
# Home
# ---------------------------
@app.route("/")
def home():
    return """
    <h1>AI Startup Dashboard 🚀</h1>

    <h3>Search</h3>
    <form action="/search">
        <input name="q">
        <input type="submit">
    </form>

    <h3>Login</h3>
    <form action="/login">
        <input name="user">
        <input name="pass">
        <input type="submit">
    </form>

    <h3>Ping Tool</h3>
    <form action="/ping">
        <input name="ip">
        <input type="submit">
    </form>
    """

# ---------------------------
# ❌ XSS (REAL)
# ---------------------------
@app.route("/search")
def search():
    q = request.args.get("q", "")
    return f"<h2>Results for: {q}</h2>"  # no sanitization

# ---------------------------
# ❌ SQL Injection (REAL)
# ---------------------------
@app.route("/login")
def login():
    user = request.args.get("user", "")
    pw = request.args.get("pass", "")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # ❌ vulnerable query
    query = f"SELECT * FROM users WHERE username='{user}' AND password='{pw}'"
    result = c.execute(query).fetchone()

    conn.close()

    if result:
        return "Logged in!"
    return "Invalid credentials"

# ---------------------------
# ❌ Command Injection (REAL)
# ---------------------------
@app.route("/ping")
def ping():
    ip = request.args.get("ip", "")
    output = os.popen(f"ping -c 1 {ip}").read()
    return f"<pre>{output}</pre>"

# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
