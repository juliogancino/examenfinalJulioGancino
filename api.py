from flask import Flask, render_template
from patiotuerca import get_auto, set_auto, read_auto
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/carga_vehiculo", methods=["POST"])
def get_vehi():
    v = (request.form['marca'])
    n = int((request.form['numero']))
    dic = get_auto(v, n)
    # dic = ["juan","pedro",'jose']
    return render_template('get_vehiculo.html', vehi=v, num=n, dics=dic, ok=0)

@app.route("/guarda_vehiculo", methods={"POST"})
def set_vehi():
    v = (request.form['marca'])
    n = int(request.form['numero'])
    document = get_auto(v, n)
    ok = set_auto(document)

    return render_template('get_vehiculo.html', vehi=v, num=n, dics=document, ok=ok)

@app.route("/data_atlas")
def get_mongo():
    document = read_auto()
    return render_template('get_mongo.html', vehi=document)
@app.route("/apig/")
def api():
    js = get_auto("toyota", 5)
    print(len(js))
    for i in js:
        print(js)
    return js

# @app.route("/api/<ticker>")
# def apid(ticker):
#     return get_auto(ticker,5

@app.route("/api/multiple/")
def api_m():
    tickers = request.args.get('tickers')
    tickers = tickers.split(',')

    result = []
    for t in tickers:
        result.append(get_auto(t, 5))
    return result

@app.route("/api/<ticker>", methods=["GET"])
def get_ticker(ticker):
    return get_auto(ticker, 5)
@app.route("/api/<ticker>", methods=["POST"])
def etl(ticker):
    document = get_auto(ticker, 5)
    return set_auto(document)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)