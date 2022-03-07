from CryptoSystem import db
Model=db.Model

class User(Model):
    '''
    Holds information specific to each user

    -email(<30 chars): the users email
    -bio(<200 chars): brief bio
    -first_name(<30 chars): the users first name
    -last_name(<30 chars): the users last name
    -date_started: the date the user started on the platform
    -fav_crypto (foreign key): the users favorite crypto cryptocurrency
    -wallet_hash (unique): the cryptographic hash used to identify the users wallet
    '''

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
    """
    Associative table (Many-Many helper table) between User and Asset
    -wallet_hash: the cryptographic hash used to identify the wallet
    -asset_id: the id of the asset the user holds

    """

    asset_id = db.Column(db.String(50), nullable=False, primary_key=True)
    asset_amount = db.Column(db.Float(20), nullable=False)
    wallet_encryption_key = db.Column(db.String(64), db.ForeignKey('wallet.encryption_key'), nullable=False, primary_key=True)

    def __repr__(self):
        return f"Assets(Id = {self.asset_id}, amount= {self.asset_amount})"

    

# class Amount(Model):
#     """
#     Holds information specific to an asset (e.g. Bitcoin)
#     -identifier: the ticker of the asset
#     -asset_name: the name of the asset
#       -asset_amount: the amount of the asset the user holds
#     """
#     identifier = db.Column(db.String(50),primary_key = True, nullable=False)
#     asset_name =  db.Column(db.String(20), nullable=False)
#
#     def __repr__(self):
#         return f"Asset(id={self.identifier}, name={self.asset_name})"
#
#
#
#
#


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

# class Comment(Model):
#     identifier = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(200), nullable=False)
#     time_made = db.Column(db.DateTime(), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.identifier'), nullable=False)
#     asset = db.Column('asset_id', db.String(10), db.ForeignKey('asset.identifier'))
    
#     def __repr__(self):
#         return f"User({self.identifier}, {self.user}, {self.body})"
