from CryptoSystem import app,oauth
from CryptoSystem.forms import *
from flask import render_template,url_for,redirect, session
from CryptoSystem.Wallet import *
from CryptoSystem.Asset import *



@app.route('/')
def test():
    return render_template("test.html")

""" ******************** Features  ******************** """
@app.route('/peer2peer')
def p2p():
    pass


""" ******************** Auth  ******************** """



@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    profile = resp.json()
    # do something with the token and profile
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)

    return redirect('/')





""" ******************** Wallet Test ******************** """
@app.route('/wallet')
def showWallet():
    wallet = Wallet("123Test")
    teseter = [Asset("BitCoin", 123), Asset("Doge", 456), Asset("Shiba Inu", 789)]
    for i in teseter:
        wallet.fillAssets(i, 1)


    return render_template("wallet.html", wallet=wallet)



""" ******************** Forms ******************** """

@app.route('/userProfile',methods=['GET', 'POST'])
def userProfile():
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














