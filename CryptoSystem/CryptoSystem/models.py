from CryptoSystem import db
Model=db.Model
#todo make changes
class User(Model):
    identifier = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200))
    full_name = db.Column(db.String(50))
    years_trading = db.Column(db.Date)
    Wallets = db.relationship('Wallet', backref='owner', lazy=True)

contains = db.Table('contains',
    db.Column('wallet_hash', db.String(64), db.ForeignKey('wallet.hash'), primary_key=True),
    db.Column('asset_id', db.String(10), db.ForeignKey('asset.identifier'), primary_key=True),
    db.Column('amount', db.Float())
)

class Wallet(Model):
    hash = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.identifier'))
    coins = db.relationship('Asset', secondary=contains, lazy='subquery')

class Asset(Model):
    identifier = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    comments = db.relationship('Comment', backref='commenter')

class Comment(Model):
    identifier = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    time_made = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.identifier'))
    asset = db.Column('asset_id', db.String(10), db.ForeignKey('asset.identifier'), primary_key=True)
   
