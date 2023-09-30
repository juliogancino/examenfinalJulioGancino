from flask import Flask
from patiotuerca import  get_price
from flask import request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/")
def api():
    return get_price("toyota")

@app.route("/api/<ticker>")
def apid(ticker):
    return get_price(ticker)

@app.route("/api/multiple/")
def api_m():
    tickers = request.args.get('tickers')
    tickers = tickers.split(',')

    result = []
    for t in tickers:
        result.append(get_price(t))
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)