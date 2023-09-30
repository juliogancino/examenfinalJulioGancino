from patiotuerca import get_price

tickers =["toyota",'chevrolet','mazda','nissan','kia']
#url="https://ecuador.patiotuerca.com/ptx/api/v2/nitros?type=autos&brand=toyota&model=&subtype=&count=2&_=1696048303864"

for t in tickers:
    get_price(ticker=t, verbose=True)