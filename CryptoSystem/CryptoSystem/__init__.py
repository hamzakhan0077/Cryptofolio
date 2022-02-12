from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CS3305-2022'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


oauth = OAuth(app)
google_conf = oauth.register(

    name='google',
    client_id="333226036029-u8bbjh1nnq7053bipl6updq2gk6o3psq.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'}

)


#db.create_all()

from CryptoSystem import routes
from CryptoSystem import forms
from CryptoSystem import models