import os, sys
sys.path.insert(0, os.path.abspath(".."))

from CryptoSystem import app



if __name__ == "__main__":
    app.run(debug=True)