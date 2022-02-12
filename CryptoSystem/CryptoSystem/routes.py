from CryptoSystem import app,oauth
from CryptoSystem.forms import *
from flask import render_template,url_for,redirect, session,abort
from CryptoSystem.Wallet import *
from CryptoSystem.Asset import *
from CryptoSystem.models import User,Wallet
from hashlib import sha256
from datetime import date
from CryptoSystem import db

@app.route('/')
def index():
    return render_template("index.html")

""" ******************** Features  ******************** """
@app.route('/peer2peer')
def p2p():
    pass


@app.route('/market')
def market():
    return render_template("market.html")



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
    user_info =  oauth.google.userinfo()
    session['email'] = user_info['email']
    if not User.query.filter_by(email =  user_info['email']).all(): # if user is not already in DB
        # wallet = Wallet(sha256(user_info['email'].encode()).hexdigest())
        wallet_enc_key = sha256(user_info['email'].encode()).hexdigest()
        wallet = Wallet(encryption_key= wallet_enc_key,wallet_holder_email =user_info['email'] )
        cryp_user = User(first_name =  user_info['name'],last_name =  user_info['family_name'], email =  user_info['email'],date_started = date.today(),wallet_hash = wallet_enc_key)
        db.session.add(wallet)
        db.session.add(cryp_user)
        db.session.commit()
    else:
        print("this user is already there")





    return redirect('/market')


@app.route('/logout')
def logout():

    for key in list(session.keys()):
        session.pop(key)


    return redirect('/')





""" ******************** Wallet Test ******************** """
@app.route('/wallet')
def showWallet():
    the_user = User.query.filter_by(email =session['email']).first()
    wallet_handler = Wallet_Handler(the_user.wallet_hash)
    all_assets = []
    for asset in  Asset.query.filter_by(wallet_encryption_key=the_user.wallet_hash).all():
        all_assets.append((asset.identifier,asset.asset_amount)) # I am adding as tuple as Market Val Api is not ready yet
    for val in all_assets:
        wallet_handler.fillAssets(val[0],val[1])
    return render_template("wallet.html", wallet=wallet_handler)



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














