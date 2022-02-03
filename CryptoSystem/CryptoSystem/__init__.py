from flask import Flask
from CryptoSystem import routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CS3305-2022'