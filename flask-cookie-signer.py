from flask import Flask, session
from flask.sessions import SecureCookieSessionInterface
import os


SECRET_KEY = os.urandom(32)
print(f"[*]Secret key: {SECRET_KEY}")

app = Flask(__name__)
app.secret_key = SECRET_KEY

session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)


@app.route("/")
def index():
    session["admin"] = True
    print(f"[*]Sending session cookie: {session_serializer.dumps(session)}")
    # 2. and this is how I needed to use it
    session_cookie = session_serializer.dumps(dict(session))
    return session_cookie
app.run()