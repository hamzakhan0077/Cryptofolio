from CryptoSystem import app,oauth
from CryptoSystem.forms import *

from flask import render_template,url_for,redirect, session,abort,flash,copy_current_request_context,g,request
from flask import send_from_directory
import requests, json


from CryptoSystem.Wallet_Handler import *
from CryptoSystem.Asset_Handler import *
from CryptoSystem.models import *
from hashlib import sha256
from datetime import date
from CryptoSystem import db, cg
from pycoingecko import CoinGeckoAPI
from CryptoSystem.helpers import *

from functools import wraps



import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

""" ******************** Features  ******************** """
import sys




chosen_currency = 'usd'
days = 3

cryptos = [{"rank": coin["market_cap_rank"], "image": coin["image"], "name": coin["name"],
            "symbol": coin["symbol"], "price": coin["current_price"], "volume": coin["total_volume"]}
           for coin in cg.get_coins_markets(vs_currency=chosen_currency)]


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.keys():
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


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
@login_required
def p2p():
    coin_dict = coin_info_dict()
    all_ads = Advertisement.query.all() # List of Advertisement Model Objects
    return render_template("peer2peer.html",all_ads = all_ads,coin_dict = coin_dict)

# @app.route('/search',methods=['GET', 'POST'])
# def search():
#     form = search
#     all_coin_names = [coin["name"].capitalize() for coin in cg.get_coins_markets(vs_currency='usd')]
#     if form.validate_on_submit():
#         if form.search.data.capitalize() in all_coin_names:
#             return redirect(f'coin/{form.search.data}')


@app.route('/tradeDeal/<int:ad_id>')
@login_required
def trade_deal(ad_id): # This method makes the deal happen between two peers

    ad = Advertisement.query.filter_by(ad_id = ad_id).first()
    ad_data = Advertisement.query.filter_by(ad_id=ad_id).first()
    user = user_info_dict()
    coin_dict = coin_info_dict()
    transaction = {'advertiser':"",'offered_asset':"",'paid':""}
    email_for_nav = user['the_user'].email

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
                    return render_template("tradeDeal.html",coin_dict= coin_dict,transaction=transaction,ad=ad_data,email_for_nav = email_for_nav)

                else:
                    flash(f"You do not have sufficient {ad.advertiser_accepting} to make this deal Please Purchase more from the market.")
                    break
    else:
        flash(f"Please don't try to self trade.")

    return render_template("tradeDeal.html",email_for_nav = email_for_nav)

#Healper method that makes  transfer happen
def transferring(wallet_hash,asset_to_transfer,Amount):
    asset_to_transfer = asset_to_transfer.upper()
    current_user_dict = user_info_dict()
    all_target_user_assets = Asset.query.filter_by(wallet_encryption_key = wallet_hash).all()

    if asset_to_transfer in [i.asset_id for i in all_target_user_assets ]:
        for target_asset in all_target_user_assets:
            if target_asset.asset_id == asset_to_transfer:
                target_asset.asset_amount += Amount

                db.session.commit()


                break
    else:
        new_asset = Asset(asset_id = asset_to_transfer,asset_amount=Amount,wallet_encryption_key = wallet_hash)
        db.session.add(new_asset)
        db.session.commit()

    return True

@app.route('/transfer/<string:asset>',methods=['GET', 'POST'])
@login_required
def transfer_assets(asset):
    the_asset = asset
    form = transfer()
    user_info = user_info_dict()
    email_for_nav = user_info['the_user'].email

    if form.validate_on_submit():
        for owned_asset in user_info['current_assets']:
            if owned_asset.asset_id == asset.upper():
                if owned_asset.asset_amount >= form.amount.data: # if this user has sufficient amount to send
                    # check to see if this user is actually registered with Cryptofolio
                    if Wallet.query.filter_by(encryption_key = form.receiver_wallet.data).first():
                        owned_asset.asset_amount-=form.amount.data
                        db.session.commit()
                        transferring(form.receiver_wallet.data, asset, form.amount.data)
                        flash(f"You have successfully transferred {form.amount.data} {asset} to ")
                        flash(f"{form.receiver_wallet.data}")

                        break
                    else:
                        flash("User must be registered with Cryptofolio, Please check the wallet hash and try again")
                        break
                else:
                    flash(f"You don\'t have sufficient {asset} please purchase from the Market")
                    break
            # else:
            #     flash(f"Sorry you cant trade an asset that you dont own")
            #     break



    return render_template("transfer.html",form=form,the_asset = the_asset,email_for_nav = email_for_nav)



@app.route('/dealUpload/<string:asset>',methods=['GET', 'POST'])
@login_required
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
@login_required
def nft():
    return render_template("nft.html")



@app.route('/market')
@login_required
def market():
    return render_template("market.html",currency = chosen_currency, cryptos = cryptos)

@app.route('/coin/<string:crypto>',methods=['GET', 'POST'])
@login_required
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
<<<<<<< HEAD

=======
>>>>>>> ca7da8627412530e52415678251d0fc8ed1310c6

    symbol = crypto_details['symbol'].upper()
    data = {}
    data['asset'] = symbol

<<<<<<< HEAD

=======
>>>>>>> ca7da8627412530e52415678251d0fc8ed1310c6
    if form.validate_on_submit():
        cc_form = credit_card()
        data['amount'] = form.amount.data
        data['amount_receive'] = form.amount_receive.data
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

# def removeFromWallet(amount_of_asset,target_asset):
#     info = user_info_dict()
#     if user_asset in info['current_assets']:
#         for tar in info['current_assets']:
#             if tar.asset_id == target_asset:
#                 tar.asset_amount -= amount_of_asset
#                 db.session.commit()
#                 addToWallet(amount_to_convert * data['current_price'],'usdt')
#                 db.session.commit()
#                 break
#
#
    
    
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
@login_required
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
    return render_template("wallet.html", wallet=wallet_handler,owned_cryptos = owned_cryptos,overall_value=overall_value_formatted,email_for_nav = session['email'])




@app.route('/userProfile',methods=['GET', 'POST'])
@login_required
def userProfile():
    form = user_profile()
    user_info = user_info_dict()
    user_email =  user_info['the_user'].email
    # print(form.validate_on_submit(),"****")
    # print(f, "****")

    if form.validate_on_submit():
        user_info['the_user'].bio = form.bio.data
        db.session.commit()
        user_info['the_user'].fav_crypto = form.fav_crypto.data
        db.session.commit()
        return redirect(f'/viewUserProfile/{user_email}')


    return render_template("userProfile.html", form=form,email_for_nav = user_email)

@app.route('/viewUserProfile/<string:email>',methods=['GET', 'POST'])
@login_required
def viewUserProfile(email):
    coin_dict = coin_info_dict()
    user = User.query.filter_by(email=email).first()
    return render_template("userProfileView.html",user=user,coin_dict = coin_dict)



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
@login_required
def logout():

    for key in list(session.keys()):
        session.pop(key)


    return redirect('/')





""" ******************** NFT ******************** """

@app.route('/react-static/<path:filename>')
def reactStatic(filename):
    return send_from_directory(app.config['REACT_COMPONENTS'],
                            filename, as_attachment=True,
                            mimetype='text/javascript'
        )


@app.route("/nft-api/<string:query>")
def nftApi(query):
    urls = {
        "hot":"https://rarible-data-scraper.p.rapidapi.com/hot_collection",
        "top":"https://rarible-data-scraper.p.rapidapi.com/top_collection/7/25"
    }
    if query in urls.keys():
         url = urls[query]

    response =requests.get(url, headers={
                "x-rapidapi-host": "rarible-data-scraper.p.rapidapi.com",
                "x-rapidapi-key": '956b93970amsh0557a4725a6aec2p1f7630jsnd6516534bfa7'
            })

    return json.loads(response.text)

""" ******************** MISC ******************** """
@app.route('/team')
@login_required
def team():
    return render_template('team.html')



#
# @app.route('/buy',methods=['GET', 'POST'])# this just for testing in reality those form will be embedded in coin section
# def sell_form():
#     form = buy()
#     return render_template("buyFormTest.html", form=form)
#
#
# @app.route('/sell',methods=['GET', 'POST']) # this just for testing in reality those form will be embedded in coin section
# def buy_form():
#     form = sell()
#     return render_template("sellFormTest.html", form=form)
#
#

@app.route('/quickBuy',methods=['GET', 'POST'])
def quick_buy():
    return redirect('market')


#
# @app.route('/postReview',methods=['GET', 'POST'])
# def post_review():
#     form = review()
#     return render_template("postReview.html", form=form)
#

@app.route('/payment',methods=['GET', 'POST'])
def card():
    form = credit_card()
    return render_template("payment.html", form=form)














