from CryptoSystem import db
Model=db.Model

class User(Model):
    email = db.Column(db.String(30), nullable=False, primary_key=True)
    bio = db.Column(db.String(200), nullable=True, default='')
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    date_started = db.Column(db.Date, nullable=False)
    fav_crypto = db.Column(db.String(10), db.ForeignKey('asset.asset_id'), nullable =True)
    wallet_hash = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f"User({self.first_name}, {self.last_name},{self.email},{self.wallet_hash},{self.date_started})"



class Wallet(Model):
    encryption_key = db.Column(db.String(500), nullable=False,primary_key = True)
    wallet_holder_email =  db.Column(db.String(20), nullable=False)
    assets = db.relationship('Asset', backref='wallet', lazy=True)
    def __repr__(self):
        return f"Wallet({self.encryption_key}, {self.wallet_holder_email}"


class Asset(Model):
    asset_id = db.Column(db.String(50), nullable=False, primary_key=True)
    asset_amount = db.Column(db.Float(20), nullable=False)
    wallet_encryption_key = db.Column(db.String(64), db.ForeignKey('wallet.encryption_key'), nullable=False, primary_key=True)

    def __repr__(self):
        return f"Assets(Id = {self.asset_id}, amount= {self.asset_amount})"

class Advertisement(Model):
    ad_id  = db.Column(db.Integer, nullable=False, primary_key=True,autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    asset_id = db.Column(db.String(20))
    time_created = db.Column(db.String(30))

    advertiser_offering = db.Column(db.String(10), nullable=False)
    offering_amount = db.Column(db.Float,nullable=False)

    advertiser_accepting = db.Column(db.String(10),nullable=False)
    sell_price = db.Column(db.String(20),nullable=False) # string because it is formatted as currency

    def __repr__(self) -> str:
        return f"Advertisement(email = {self.email},asset_id = {self.asset_id}, time_created = {self.time_created}, advertiser_offering= {self.advertiser_offering}, offering_amount = {self.offering_amount} , advertiser_accepting = {self.advertiser_accepting},sell_price = {self.sell_price}"
if __name__ == '__main__':
    pass