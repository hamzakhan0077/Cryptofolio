
import json

def run():
    json_dat = open("coins.json","r")
    dat = json.load(json_dat)
    res = [tuple for tuple in dat.items()]
    out =open("coinsSelectField.txt","a")
    out.write(str(res))
if __name__ == "__main__":
    run()