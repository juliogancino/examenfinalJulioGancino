import requests

def get_price(ticker: str, verbose: bool = False) -> dict:
    url = f"https://ecuador.patiotuerca.com/ptx/api/v2/nitros?brand={ticker}"

    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(url=url, headers=user_agent).json()

    modelo = r['data']['result_set'][0]['ModelValue']
    precio = r['data']['result_set'][0]['PriceValue']
    if verbose:
        print(f"{ticker} : {modelo} {precio} ")

    return {
        "ticker": ticker,
        "modelo": modelo,
        "precio": precio
    }
