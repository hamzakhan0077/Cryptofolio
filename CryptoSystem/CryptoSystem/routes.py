from CryptoSystem import app

from flask import render_template

@app.route('/')
def test():
    return render_template("test.html")