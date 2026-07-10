from flask import Flask, request, render_template_string
from logger import log_event

app = Flask(__name__)

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Router Admin Login</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f2f2f2; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { background: white; padding: 30px 40px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); width: 300px; }
        h2 { text-align: center; color: #333; }
        input { width: 100%; padding: 8px; margin: 8px 0; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #2b4c7e; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .error { color: red; text-align: center; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Admin Login</h2>
        {% if show_error %}<p class="error">Invalid username or password</p>{% endif %}
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>
"""

def get_client_ip():
    # Handles requests that come through a proxy (relevant once deployed to a real server)
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    return request.remote_addr

@app.route("/", methods=["GET"])
def index():
    return render_template_string(LOGIN_PAGE, show_error=False)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    source_ip = get_client_ip()
    user_agent = request.headers.get("User-Agent", "unknown")

    log_event(
        "http_honeypot",
        source_ip,
        username=username,
        password=password,
        extra={"user_agent": user_agent, "path": "/login"},
    )

    # Always reject, regardless of what was entered
    return render_template_string(LOGIN_PAGE, show_error=True)

if __name__ == "__main__":
    print("HTTP honeypot listening on http://0.0.0.0:8080")
    app.run(host="0.0.0.0", port=8080, debug=False)