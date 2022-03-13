import os
import flask
from flask import Flask, request

"""
Simply logs the given file(param f) into 'post_data.txt'

curl -F "f=@lp.txt" 127.0.0.1:8889/save

"""


app = Flask(__name__)

@app.route('/save', methods=['POST'])
def upload():
    f = request.files['f']
    f.save("post_data.txt")
    return ""

if __name__ == "__main__":

    import sys

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000
    app.run("0.0.0.0",port)

