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
    fav_crypto = db.Column(db.String(10), db.ForeignKey('asset.identifier'), nullable =True)
    wallet_hash = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f"User({self.first_name}, {self.last_name},{self.email},{self.wallet_hash},{self.date_started})"


class Coin(Model):
    """
    Associative table (Many-Many helper table) between User and Asset
    -wallet_hash: the cryptographic hash used to identify the wallet
    -asset_id: the id of the asset the user holds
    -asset_amount: the amount of the asset the user holds
    """
    wallet_hash =  db.Column(db.String(64), db.ForeignKey('user.wallet_hash'), nullable=False, primary_key=True)
    asset_id = db.Column(db.String(50), db.ForeignKey('asset.identifier'), nullable=False, primary_key=True)
    asset_amount = db.Column(db.Float(20), nullable=False)

    def __repr__(self):
        return f"Coins({self.wallet_holder_email} owns {self.asset_amount} of {self.asset_id})"

    

class Asset(Model):
    """
    Holds information specific to an asset (e.g. Bitcoin)
    -identifier: the ticker of the asset
    -asset_name: the name of the asset
    """
    identifier = db.Column(db.String(50),primary_key = True, nullable=False)
    asset_name =  db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return f"Asset(id={self.identifier}, name={self.asset_name})"


class Advertisement(Model):
    """
    Holds information pertaining to a specific advertisement
    -identifier: unique key to identify the ad
    -time created: the time it was created
    -advertiser_offering: what the advertiser is trying to sell
    -offering_amount: the amount they are offering
    -advertiser_accepting: what the advertiser is willing to accept
    -accepting_amount: what the advertiser wants to accept
    """
    identifier = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.Date())

    advertiser_offering = db.Column(db.String(10), db.ForeignKey('asset.identifier'))
    offering_amount = db.Column(db.Float,nullable=False)

    advertiser_accepting = db.Column(db.String(10), db.ForeignKey('asset.identifier'))
    accepting_amount = db.Column(db.Float,nullable=False)

    def __repr__(self) -> str:
        return f"Advertisement({self.identifier} selling {self.advertiser_offering})"

# class Comment(Model):
#     identifier = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(200), nullable=False)
#     time_made = db.Column(db.DateTime(), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.identifier'), nullable=False)
#     asset = db.Column('asset_id', db.String(10), db.ForeignKey('asset.identifier'))
    
#     def __repr__(self):
#         return f"User({self.identifier}, {self.user}, {self.body})"
