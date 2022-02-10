import json
import sys
sys.path.insert(1, '../CryptoSystem/CryptoSystem')
from CryptoSystem.models import Asset, User
from CryptoSystem import db
from datetime import datetime
def add_coins():

    # Load files from coins.json
    json_dat = open("coins.json","r")
    dat = json.load(json_dat)
    #Add the coins
    for ticker, name in dat.items():
        asset = Asset(identifier=ticker, name=name)
        print(asset)
        db.session.add(asset)
    
    

def add_dummy_user():
    identifier = 12345
    bio = "This is a dummy bio"
    first_name = "Liam"
    last_name = "Lenihan"
    date_started = datetime.now()
    owned_coins = Asset.query.limit(10).all()
    fav_crypto = Asset.query.first()
    wallet_hash = "12345"

    user = User(identifier=identifier, bio=bio, first_name=first_name,
     last_name=last_name, date_started=date_started, 
     fav_crypto=fav_crypto, wallet_hash=wallet_hash)
    for coin in owned_coins:
        user.coins.append(coin)
    db.session.add(user)



if __name__ == '__main__':
    add_dummy_user()
    db.session.commit()
