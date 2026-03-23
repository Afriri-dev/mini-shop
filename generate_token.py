import datetime, jwt

SECRET_KEY = "supersecretkey"
payload = {
    "user_id": 1,
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # expire dans 1h
}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print(token)