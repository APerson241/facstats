#!/usr/bin/env python3.4
import os
from flask import Flask, render_template, request

DEBUG = True
DEFAULT_PORT = 5000

app = Flask(__name__)

@app.route('/')
def index():
    username = request.args.get('username', '')
    if username:
        return render_template('results.html', username=username)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', DEFAULT_PORT))
    app.run(debug=DEBUG, port=port)