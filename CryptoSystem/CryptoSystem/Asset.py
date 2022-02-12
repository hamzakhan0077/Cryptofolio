# name of asset
# market value of asset

# wallet has amount of the asset
# wallet has balance


class Asset_Handler:

    def __init__(self, name, marketVal):
        self._name = name
        self._marketVal = marketVal

    def getName(self):
        return self._name

    def getMarketVal(self):
        return self._marketVal

    def setMarketVal(self, val):
        self._marketVal = val

    def __str__(self):
        ans = self.getName() + "  Market Value: " + str(self.getMarketVal())
        return ans


