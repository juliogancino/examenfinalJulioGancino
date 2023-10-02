import requests
import json
from mongo import client

cantidad = 5

def get_auto(ticker: str, nume: int, verbose: bool = False) -> dict:
    url = f"https://ecuador.patiotuerca.com/ptx/api/v2/nitros?brand={ticker}&count={nume}"

    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(url=url, headers=user_agent).json()
    if r['data']['result_set'] is not None:
        j = 0

        # modelo = r['data']['result_set'][j]['ModelValue']
        # precio = r['data']['result_set'][j]['PriceValue']
        # image = r['data']['result_set'][j]['MainImageUrl']
        dat = {}
        for i in range(nume):
            da1 = {
                    "kilometraje": r['data']['result_set'][j]['Mileage'],
                    "marca": r['data']['result_set'][j]['BrandValue'],
                    "modelo": r['data']['result_set'][j]['ModelValue'],
                    "precio": r['data']['result_set'][j]['PriceValue'],
                    "imagen": r['data']['result_set'][j]['MainImageUrl'],
                    "anio": r['data']['result_set'][j]['Year']
                }

            dat[j] = da1
            j = j + 1

    else:
        dat = {
            "marca" : "no existe",
            "modelo" : "No existe",
            "precio" : "No existe",
            "image" : "No existe",
            "anio" : "No existe",
            "kilometraje" : "No existe"
        }



    if verbose:
        print(dat)

    return dat
    #     {
    #     "Marca": ticker,
    #     "Modelo": modelo,
    #     "Precio": precio,
    #     "Imagen": image,
    # }

def set_auto(document: dict):
    for doc in document:
        _ = client.get_database('examenpatiotuerca').get_collection('vehiculos').insert_one(document=document[doc])
    return 1

def read_auto()-> dict:
    result = client.get_database('examenpatiotuerca').get_collection('vehiculos').find()
    return result

def read_autodos():
    result = client.get_database('examenpatiotuerca').get_collection('vehiculos').find()
    for res in result:
        print(res)

