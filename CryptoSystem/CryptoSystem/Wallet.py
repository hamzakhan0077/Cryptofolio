from Asset import Asset

"""
main goal,
contain assets: cryptocurrencies(dummy data lists, dict, etc)
-create wallet
-create route (import wallet in route.py)
-create wallet route to view a wallet
-create a html template to view the wallet

(wallet)
-to show every asset name and balance -value of the crypto -how much in euro
-encryption key of wallet sha256 (see encoder.py)

Main wallet Page
-to show overall balance
-encryption key
-number of assets

#name of asset
#market value of asset
#wallet has amount of the asset
#wallet has balance

#   withdraw 
#   transfer
#   deposit

"""


class Wallet:

    def __init__(self, encKey):
        self._assets = {}
        self._encKey = encKey
        self._totalAssetVal = 0

    def getEncKey(self):
        return self._encKey

    def fillAssets(self, asset):
        self._assets[asset.getName()] = asset.getMarketVal()
        self._totalAssetVal += asset.getMarketVal()

    def getTotalValue(self):
        return self._totalAssetVal

    def withdraw(self, amount, destinationAddress):  ## check this
        pass

    def transfer(self, amount, destinationWallet):
        pass

    def deposit(self, assetAmount):
        # redirect to quick buy
        pass

    def __str__(self):
        ans = "Encryption Key: " + self.getEncKey() + ",\t Assets:"
        for i in self._assets.items():
            ans += str(i) + ", "
        ans += "\tTotal Value:" + str(self.getTotalValue())
        return ans


wallet = Wallet("#123keyKarim")
print(wallet)
teseter = [Asset("BitCoin", 123), Asset("Doge", 456), Asset("Shiba Inu", 789)]
for i in teseter:
    wallet.fillAssets(i)

print(wallet)
print(wallet.getTotalValue())
