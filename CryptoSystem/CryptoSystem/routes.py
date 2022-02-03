from CryptoSystem import app
from CryptoSystem.forms import *
from flask import render_template

@app.route('/')
def test():
    return render_template("test.html")



""" ******************** Forms ******************** """

@app.route('/userProfile',methods=['GET', 'POST'])
def user_profile():
    form = user_profile()
    return render_template("userProfile.html", form=form)



@app.route('/dealUpload',methods=['GET', 'POST'])
def deal_upload_form():
    form = deal()
    return render_template("dealUpload.html", form=form)

@app.route('/buy',methods=['GET', 'POST'])# this just for testing in reality those form will be embedded in coin section
def sell_form():
    form = buy()
    return render_template("buyFormTest.html", form=form)


@app.route('/sell',methods=['GET', 'POST']) # this just for testing in reality those form will be embedded in coin section
def buy_form():
    form = sell()
    return render_template("sellFormTest.html", form=form)



@app.route('/quickBuy',methods=['GET', 'POST'])
def quick_buy():
    form = quick_buy_market()
    return render_template("quickBuy.html", form=form)



@app.route('/postReview',methods=['GET', 'POST'])
def post_review():
    form = review()
    return render_template("postReview.html", form=form)


@app.route('/payment',methods=['GET', 'POST'])
def card():
    form = credit_card()
    return render_template("payment.html", form=form)














