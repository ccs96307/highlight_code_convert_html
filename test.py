# -*- coding: utf-8 -*-
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def result():
    if request.method == 'POST':
        user = request.values['user']
        return render_template('result.html', name=user)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
