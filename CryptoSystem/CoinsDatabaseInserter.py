import json
import sys
sys.path.insert(1, '../CryptoSystem/CryptoSystem')
from CryptoSystem.models import Asset
from CryptoSystem import db
def run():

    # Load files from coins.json
    json_dat = open("coins.json","r")
    dat = json.load(json_dat)
    #Add the coins
    for ticker, name in dat.items():
        asset = Asset(identifier=ticker, name=name)
        print(asset)
        db.session.add(asset)
    
    db.session.commit()
if __name__ == '__main__':
    run()
