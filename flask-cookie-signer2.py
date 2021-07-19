from flask import sessions
import os

session_interface = sessions.SecureCookieSessionInterface()

class App:
    secret_key = os.urandom(32)
app = App()

cookie = {
    "foo": "bar", 
    'admin': True
}

print(f"[*]Secret key: {app.secret_key}")
print(f"[*]Cookie: {cookie}")

signed_cookie = session_interface.get_signing_serializer(app).dumps(cookie)

print(f"[*]Signed cookie: {signed_cookie}")


unsigned_cookie = session_interface.get_signing_serializer(app).loads(signed_cookie)

print(f"[*]Unsigned cookie: {unsigned_cookie}")
