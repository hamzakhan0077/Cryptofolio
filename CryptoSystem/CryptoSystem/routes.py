from CryptoSystem import app,oauth
from CryptoSystem.forms import *
from flask import render_template,url_for,redirect, session,abort,flash,copy_current_request_context, send_from_directory

from CryptoSystem.Wallet_Handler import *
from CryptoSystem.Asset_Handler import *
from CryptoSystem.models import *
from hashlib import sha256
from datetime import date
from CryptoSystem import db, cg
from pycoingecko import CoinGeckoAPI
from CryptoSystem.helpers import *
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

""" ******************** Features  ******************** """
import sys




chosen_currency = 'usd'
days = 3

cryptos = [{"rank": coin["market_cap_rank"], "image": coin["image"], "name": coin["name"],
            "symbol": coin["symbol"], "price": coin["current_price"], "volume": coin["total_volume"]}
           for coin in cg.get_coins_markets(vs_currency=chosen_currency)]

def coin_info_dict():
    coin_dict = {}
    for coin in cg.get_coins_markets(vs_currency=chosen_currency):
        coin_dict[coin['symbol'].upper()] = {'image':coin["image"],'current_price':coin["current_price"],"name":coin["name"]}

    return coin_dict

# @copy_current_request_context
def user_info_dict():
    user_dict = {}
    user_dict['the_user'] = User.query.filter_by(email=session['email']).first()
    user_dict['wallet_hash'] = user_dict['the_user'].wallet_hash
    user_dict['current_assets'] = Asset.query.filter_by(wallet_encryption_key=user_dict['wallet_hash']).all() # list of Asset objects
    user_dict['all_ids'] = [i.asset_id for i in user_dict['current_assets']]
    return user_dict


@app.route('/')
def index():
    return render_template("index.html",currency = chosen_currency, cryptos = cryptos)

@app.route('/peer2peer')
def p2p():
    coin_dict = coin_info_dict()
    all_ads = Advertisement.query.all() # List of Advertisement Model Objects
    return render_template("peer2peer.html",all_ads = all_ads,coin_dict = coin_dict)


@app.route('/tradeDeal/<int:ad_id>')
def trade_deal(ad_id): # This method makes the deal happen between two peers

    ad = Advertisement.query.filter_by(ad_id = ad_id).first()
    ad_data = Advertisement.query.filter_by(ad_id=ad_id).first()
    user = user_info_dict()
    coin_dict = coin_info_dict()
    transaction = {'advertiser':"",'offered_asset':"",'paid':""}

    if ad.email != user['the_user'].email: # handling the case where Same user tries to make his own deal
        for user_asset in user['current_assets']:
            if user_asset.asset_id == ad.advertiser_accepting:
                # we have record of price in Crypto to USD (NOT CRYPTO TO ANOTHER CRYPTO eg BTC -ETH)
                if user_asset.asset_amount * coin_dict[user_asset.asset_id.upper()]['current_price'] >= locale.atof(ad.sell_price.strip("$")):
                    transaction['paid'] = locale.atof(ad.sell_price.strip("$")) / coin_dict[user_asset.asset_id.upper()]['current_price']
                    user_asset.asset_amount -= transaction['paid']
                    db.session.commit()
                    addToWallet(ad.offering_amount,ad.advertiser_offering) # deal completes here
                    # I don't need to remove from the advertiser's wallet because
                    # when an advertiser uploads a deal their assets are deducted and are on hold
                    # in that deal. If the deal is successful like here. The assets are not needed to be deducted
                    # as they were already on hold.

                    transaction['advertiser'] = ad.email
                    transaction['offered_asset'] = (ad.asset_id,ad.offering_amount)
                    db.session.delete(ad)
                    db.session.commit()
                    return render_template("tradeDeal.html",coin_dict= coin_dict,transaction=transaction,ad=ad_data)

            else:
                flash(f"You do not have sufficient {ad.advertiser_accepting} to make this deal Please Purchase more from the market.")
                break
    else:
        flash(f"Please don't try to self trade.")

    return render_template("tradeDeal.html")

def transfer_assets(wallet,asset_id,asset_amount):pass





@app.route('/dealUpload/<string:asset>',methods=['GET', 'POST'])
def deal_upload(asset):
    checker = True
    form = deal()
    info = user_info_dict()
    date = str(datetime.now())
    email = str(info['the_user'].email)
    crypto_details = [coin for coin in cg.get_coins_markets(vs_currency=chosen_currency) if coin["symbol"] == asset][0]
    if form.validate_on_submit():
        for target_asset in info['current_assets']:
            if target_asset.asset_id == asset.upper():
                if target_asset.asset_amount >= form.amount.data:
                    advert = Advertisement(email = email, asset_id = asset,time_created = date,
                                           advertiser_offering = form.trade_currency.data,offering_amount = form.amount.data,
                                           advertiser_accepting = form.accepted_currency.data,sell_price = form.asset_sell_price.data )
                    target_asset.asset_amount -= form.amount.data
                    db.session.commit()
                    db.session.add(advert)
                    db.session.commit()
                    flash(f"Yor advert for {form.amount.data} {asset.upper()} has been posted in Peer to Peer trade")
                    flash(f"{form.amount.data} {asset.upper()} has been deducted from your balance as they are now on hold in Peer to Peer trade")
                    checker = False
                    break

                else:
                    flash(f"Amount of {asset.upper()} cant be greater than the amount you own. Please view your wallet and try again")
                    checker = False
                    break
        if checker: # Handling the case where IF user messes with the url and Tries to advertise the asset that he dosent own
            flash(f"You don't have sufficient {asset} please purchase from the market")

    offering_asset = asset
    market_price = crypto_details['current_price']
    return render_template("dealUpload.html", form=form,offering_asset = offering_asset,market_price = market_price)



@app.route('/nft')
def nft():
    return render_template("nft.html")



@app.route('/market')
def market():
    return render_template("market.html",currency = chosen_currency, cryptos = cryptos)

@app.route('/coin/<string:crypto>',methods=['GET', 'POST'])
def coinCall(crypto): # come back here and fix the sell part
    sellForm = Sell()
    form = Buy()
    crypto_details = [coin for coin in cg.get_coins_markets(vs_currency=chosen_currency) if coin["name"] == crypto][0]
    current_date = datetime.now().date()
    current_unix_time = datetime_to_unix(current_date.year, current_date.month, current_date.day)
    result = cg.get_coin_market_chart_range_by_id(id=crypto_details["id"], vs_currency=chosen_currency,
                                                  from_timestamp=str(int(current_unix_time) - (86400 * days)),
                                                  to_timestamp=current_unix_time)["prices"]
    # print(result)
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        cc_form = credit_card()
        data['amount'] = form.amount.data
        data['amount_receive'] = form.amount_receive.dataj
        addToWallet(form.amount.data,symbol)
        return render_template('payment.html',data = data,form = cc_form)
    if sellForm.validate_on_submit():
        removeFromWallet(sellForm.amount.data,symbol)
        flash(f"You have successfully sold {sellForm.amount.data},{symbol}")




    return render_template("coin.html",form=form,sellForm=sellForm, currency=chosen_currency, crypto_details=crypto_details)


def addToWallet(amount_in_crypto,asset):
    # make a block chain transaction here
    info = user_info_dict()
    if asset in info['all_ids']:
        for val in info['current_assets']:
            if val.asset_id == asset:
                val.asset_amount+=amount_in_crypto
                db.session.commit()
                break
    else:
        asset_add = Asset(asset_id=asset,asset_amount=amount_in_crypto,wallet_encryption_key=info['wallet_hash'])
        db.session.add(asset_add)
        db.session.commit()

def removeFromWallet(amount_of_asset,target_asset):
    info = user_info_dict()
    if asset in all_ids:

        for tar in info['current_assets']:
            if tar.asset_id == target_asset:
                tar.asset_amount -= amount_of_asset
                addToWallet(amount_to_convert * data['current_price'],'usdt')
                db.session.commit()
                break

    
    
    
    # data = asset_data(asset)
    # amount_to_convert = amount_of_asset
    # amount_of_asset *= -1
    # print(amount_of_asset,"****************")
    # addToWallet(amount_of_asset,asset)
    # value_in_usdt = amount_to_convert * data['current_price']
    # addToWallet(value_in_usdt,'usdt')




def asset_data(asset):
    asset = asset.lower()
    crypto_data = [coin for coin in cg.get_coins_markets(vs_currency=chosen_currency) if coin["symbol"] == asset][0]
    return crypto_data

@app.route('/wallet')
def showWallet():
    owned_cryptos = {}
    overall_value = 0
    the_user = User.query.filter_by(email =session['email']).first()
    wallet_handler = Wallet_Handler(the_user.wallet_hash)

    for asset in  Asset.query.filter_by(wallet_encryption_key=the_user.wallet_hash).all():
        data = asset_data(asset.asset_id)
        owned_cryptos[asset.asset_id.upper()] = {'amount':asset.asset_amount,'value': '${:,.2f}'.format(asset.asset_amount * data['current_price']),'data':data}
        overall_value+= asset.asset_amount * data['current_price']
    overall_value_formatted = '${:,.2f}'.format(overall_value)
    # for val in all_assets:
    #     wallet_handler.fillAssets(val[0],val[1])
    return render_template("wallet.html", wallet=wallet_handler,owned_cryptos = owned_cryptos,overall_value=overall_value_formatted)








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
    if not User.query.filter_by(email = user_info['email']).all(): # if user is not already in DB
        wallet_enc_key = sha256(user_info['email'].encode()).hexdigest()
        wallet = Wallet(encryption_key=wallet_enc_key, wallet_holder_email=user_info['email'])
        cryp_user = User(first_name=user_info['name'], last_name=user_info['family_name'], email=user_info['email'],
                         date_started=date.today(), wallet_hash=wallet_enc_key)
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





""" ******************** Static Files ******************** """

@app.route('/react-static/<path:filename>')
def reactStatic(filename):
    #
    if filename == "config.js":
        return abort(404)
    return send_from_directory(app.config['REACT_COMPONENTS'],
                               filename, as_attachment=True,
                               mimetype='text/javascript'
        )


""" ******************** Forms ******************** """

@app.route('/userProfile',methods=['GET', 'POST'])
def userProfile():
    form = user_profile()
    return render_template("userProfile.html", form=form)



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














