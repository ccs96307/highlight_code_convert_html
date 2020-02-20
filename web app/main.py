# -*- coding: utf-8 -*-
"""
Using Python to process the pygments
"""
from flask import Flask, render_template, request
from highlight import Highlight

app = Flask(__name__)
highlight = Highlight()
print(highlight)



@app.route('/')
def index():
    return render_template('code2html.html')


@app.route('/', methods=['POST'])
def success():
    if request.method == 'POST':
        code = request.form['source code']
        lang = request.form['lang']
        print(request)
        return render_template('code2html.html', html=code, iframe=lang)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)

