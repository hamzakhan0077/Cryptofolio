from CryptoSystem import db
Model=db.Model
#todo add __repr__
class User(Model):
    identifier = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(200), nullable=False, default='')
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    date_started = db.Column(db.Date, nullable=False)
    fav_crypto = db.Column(db.String(10), db.ForeignKey('asset.identifier'))
    wallets = db.relationship('Wallet', backref='owner', lazy=True)

    def __repr__(self, identifier, first_name, last_name):
        return f"User({identifier}, {first_name}, {last_name})"



contains = db.Table('contains',
    db.Column('wallet_hash', db.String(64), db.ForeignKey('wallet.hash'), primary_key=True, nullable=False),
    db.Column('asset_id', db.String(10), db.ForeignKey('asset.identifier'), primary_key=True, nullable=False),
    db.Column('amount', db.Float(), nullable=False)
)

class Wallet(Model):
    hash = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.identifier'), nullable=False)
    coins = db.relationship('Asset', secondary=contains, lazy='subquery')
    
    def __repr__(self, hash):
        return f"Wallet({hash})"


class Asset(Model):
    identifier = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    comments = db.relationship('Comment', backref='commenter')
    fans = db.relationship('User', backref='fan', lazy=True)
    owners = db.relationship('Wallet', secondary=contains, lazy=True)
    
    def __repr__(self, identifier, name):
        return f"User({identifier}, {name})"


class Comment(Model):
    identifier = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=False)
    time_made = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.identifier'), nullable=False)
    asset = db.Column('asset_id', db.String(10), db.ForeignKey('asset.identifier'))
    
    def __repr__(self, identifier, user, body):
        return f"User({identifier}, {user}, {body})"
