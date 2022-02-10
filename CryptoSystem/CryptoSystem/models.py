from CryptoSystem import db
Model=db.Model
contains = db.Table('contains',
    db.Column('wallet_hash', db.String(64), db.ForeignKey('user.wallet_hash'), primary_key=True, nullable=False),
    db.Column('asset_id', db.String(10), db.ForeignKey('asset.identifier'), primary_key=True, nullable=False),
    db.Column('amount', db.Float(), nullable=False)
)

class User(Model):
    identifier = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200), nullable=False, default='')
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    date_started = db.Column(db.Date, nullable=False)
    coins = db.relationship('Asset', secondary=contains, lazy='subquery')
    fav_crypto = db.Column(db.String(10), db.ForeignKey('asset.identifier'))
    wallet_hash = db.Column(db.String(64))

    def __repr__(self):
        return f"User({self.identifier}, {self.first_name}, {self.last_name})"



class Asset(Model):
    identifier = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    fans = db.relationship('User', backref='fan', lazy=True)
    #owners = db.relationship('User', secondary=contains, lazy=True)
    
    def __repr__(self):
        return f"User({self.identifier}, {self.name})"

class Advertisement(Model):
    identifier = db.Column(db.Integer, primary_key=True)
    advertiser_offering = db.Column(db.String(10), db.ForeignKey('asset.identifier'))
    advertiser_accepting = db.Column(db.String(10), db.ForeignKey('asset.identifier'))
    offering_amount = db.Column(db.Float)
    offering_amount = db.Column(db.Float)
    time_created = db.Column(db.Date())

# class Comment(Model):
#     identifier = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(200), nullable=False)
#     time_made = db.Column(db.DateTime(), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.identifier'), nullable=False)
#     asset = db.Column('asset_id', db.String(10), db.ForeignKey('asset.identifier'))
    
#     def __repr__(self):
#         return f"User({self.identifier}, {self.user}, {self.body})"
