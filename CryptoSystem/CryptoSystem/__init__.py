from flask import Flask



app = Flask(__name__)
app.config['SECRET_KEY'] = 'CS3305-2022'



from CryptoSystem import routes