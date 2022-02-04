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

    def fillAssets(self, asset, amountOfCoin):
        self._assets[asset] = amountOfCoin
        self._totalAssetVal += asset.getMarketVal()

    # def reduceAssets(self, asset):
    #     self._assets[asset.getName()] = asset.getMarketVal()
    #     self._totalAssetVal -= asset.getMarketVal()

    def getTotalValue(self):
        return self._totalAssetVal

    def setTotalValue(self, val):
        self._totalAssetVal = val

    def withdraw(self, amount, destinationAddress):  ## check this
        pass

    def transfer(self, currencyName, amount, destinationWallet):
        asset = self.getAssetDetails(currencyName)
        self._assets[asset] -= amount
        self.setTotalValue(self.getTotalValue() - asset.getMarketVal() * amount)

    def deposit(self, assetAmount):
        # redirect to quick buy
        pass

    def getAssetDetails(self, nameofcurrency): #helper function
        for asset in self._assets:
            if nameofcurrency == asset.getName():
                return asset

    def findAssetsMarketValue(self): #helper function
        for asset in self._assets:
            print(asset)


    def __str__(self):
        ans = "Encryption Key: " + self.getEncKey() + ",\t Assets: "
        for i in self._assets.items():
            ans += i[0].getName() + "--" + str(i[1]) + ", "
        ans += "\tTotal Value:" + str(self.getTotalValue())
        return ans


wallet = Wallet("#123keyKarim")
teseter = [Asset("BitCoin", 123), Asset("Doge", 456), Asset("Shiba Inu", 789)]
for i in teseter:
    wallet.fillAssets(i, 1)

print(wallet)
wallet.transfer("BitCoin", 1, "123")
print(wallet)
print(wallet.findAssetsMarketValue())