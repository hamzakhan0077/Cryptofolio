from CryptoSystem import db
Model=db.Model
contains = db.Table('contains',
    db.Column('wallet_hash', db.String(64), db.ForeignKey('user.wallet_hash'), primary_key=True, nullable=False),
    db.Column('asset_id', db.String(10), db.ForeignKey('asset.identifier'), primary_key=True, nullable=False),
    db.Column('amount', db.Float(), nullable=False)
)




class User(Model):
    # identifier = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200), nullable=True, default='')
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False,primary_key = True)
    date_started = db.Column(db.Date, nullable=False)
    # coins = db.relationship('Asset', secondary=contains, lazy='subquery') # ?? wallet will have assets
    fav_crypto = db.Column(db.String(10),db.ForeignKey('asset.identifier'),nullable =True)
    wallet_hash = db.Column(db.String(64))

    def __repr__(self):
        return f"User({self.first_name}, {self.last_name},{self.email},{self.wallet_hash},{self.date_started})"




class Wallet(Model):
    encryption_key = db.Column(db.String(500), nullable=False,primary_key = True)
    wallet_holder_email =  db.Column(db.String(20), nullable=False)
    assets = db.relationship('Asset', backref='wallet', lazy=True)
    def __repr__(self):
        return f"Wallet({self.encryption_key}, {self.wallet_holder_email}"

class Asset(Model):
    identifier = db.Column(db.String(50),primary_key = True, nullable=False)
    asset_name =  db.Column(db.String(20), nullable=False)
    asset_amount = db.Column(db.Float(20), nullable=False)
    wallet_encryption_key =  db.Column(db.String, db.ForeignKey('wallet.encryption_key'),
        nullable=False)
    def __repr__(self):
        return f"Asset({self.wallet_encryption_key},{self.identifier}, {self.asset_name}),{self.asset_amount}"



#Liam

# class Asset(Model):
#     identifier = db.Column(db.String(10), primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.String(200))
#     fans = db.relationship('User', backref='fan', lazy=True)
#     #owners = db.relationship('User', secondary=contains, lazy=True)
#
#     def __repr__(self):
#         return f"User({self.identifier}, {self.name})"

class Advertisement(Model):
    identifier = db.Column(db.Integer, primary_key=True)
    advertiser_offering = db.Column(db.String(10), db.ForeignKey('asset.identifier'))
    advertiser_accepting = db.Column(db.String(10), db.ForeignKey('asset.identifier'))
    offering_amount = db.Column(db.Float,nullable=False)
    offering_amount = db.Column(db.Float,nullable=False)
    time_created = db.Column(db.Date())

# class Comment(Model):
#     identifier = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(200), nullable=False)
#     time_made = db.Column(db.DateTime(), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.identifier'), nullable=False)
#     asset = db.Column('asset_id', db.String(10), db.ForeignKey('asset.identifier'))
    
#     def __repr__(self):
#         return f"User({self.identifier}, {self.user}, {self.body})"
