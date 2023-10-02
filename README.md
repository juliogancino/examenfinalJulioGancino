# examenfinalJulioGancino

## EXAMEN FINAL DEL MODULO TRATAMIENTO DE DATOS
### SISTEMA DE CONSUMO DE DATOS DE PATIOTUERCA.COM (APIs)

>En este documento va a encontrar las directrices de como manejar el sistema que generará al clonar este repo.

######
El sistema tiene 2 archivos  importantes
1. api.py
2. patiotuerca.py


***
## ARCHIVO api.py

Todas las rutas pueden ser accedidas desde éste archivo.

Que esta conformado de varias funciones, pero la principal para inciar la aplicacion web es la primera
#### API  "/"  -> index()
~~~
@app.route("/")
def index():
    return render_template('index.html')
~~~

Para ello usamos la palabra reservada **render_template** que me permite cargar una página html, y enviar también datos, 
como ya lo veremos mas adelante.

**render_template** es una dependencia del framework Flask que me permite renderizar una página web, en este caso la 
página que será renderizada es el index.html

#### API  "/carga_vehiculo"
Esta api me permite cargar los vehículos que se lean desde la API de patiotuerca.com y el código es el siguiente:
~~~
@app.route("/carga_vehiculo", methods=["POST"])
def get_vehi():
    v = (request.form['marca'])
    n = int((request.form['numero']))
    dic = get_auto(v, n)
    # dic = ["juan","pedro",'jose']
    return render_template('get_vehiculo.html', vehi=v, num=n, dics=dic, ok=0)
~~~
Lo que realiza este código es la lectura de 2 datos de la página index.html , los datos marca y numero.

**marca** es la marca de vehículo a buscar y **numero** es el numero de vehúculos que vamos a leer, pero porque pedimos 
ese dato, pues al analizar el resultado del API de patiotuerca.com encontramos ques es una variable importante al 
momento de buscar los datos, sin ese número tenía muchas fallas de respuesta, estos datos son enviados por 
POST desde un form del *index.html* pero tambien son recibidos desde el **buscador** que se encuentra en la parte 
superior derecha de la pagina (la principal diferencia es que le buscador no permite el ingreso de numero de vehículos
está seteado a 6) , luego consumimos la función _get_auto_ que busca los autos, devolviendo un diccionario que será 
visualizado en la página web **get_vehiculo.html** 

![Pagina index.html](/buscador0.png)


#### API  "/guarda_vehiculo"
Esta api me permite guardar los vehículos que se lean desde la API de patiotuerca.com y el código es el siguiente:
~~~
@app.route("/guarda_vehiculo", methods={"POST"})
def set_vehi():
    v = (request.form['marca'])
    n = int(request.form['numero'])
    document = get_auto(v, n)
    ok = set_auto(document)

    return render_template('get_vehiculo.html', vehi=v, num=n, dics=document, ok=ok)
~~~

Se recibe dos datos importante **marca** y **numero**, que como las otras funcliones, son para determinar la busqueda.

Con esos datos, consumimos la función get?auto que busca los autos usando la API de patiotuerca.com y devuelve un 
diccionario, con ese dato, podemos cargarlo a la base de datos mongoDB Atlas, y para ello usamos la función **set_auto**.

Todas las funciones antes descritas se encuentran en el archivo patiotuerca.py que será explicado más adelante.

#### API  "/data_atlas"
Esta api me permite obtener todos los vehículos que se han cargado en la base de datos Atlas.
~~~
@app.route("/data_atlas")
def get_mongo():
    document = read_auto()
    return render_template('get_mongo.html', vehi=document)
~~~
Funciona de la siguiente manera:

Hacemos un llamado a la función **read_auto** importado del archivo **patiotuerca.py**, basicamente lo que hace es 
devolverme un diccionario que será enviado (variable _vehi_) a la página web **get_mongo.html** utilizando flask para renderizarla.

Dentro de esa página se realiza una iteracion para mostrar los datos obtenidos de la nube.

#### Datos adicionales
Hay algunas APIs que se encuentran en este archivo, pero que fueron usadas de pruebas antes de usar finalmente las 
antes descritas, por ello no fueron eliminados.
***
## ARCHIVO patiotuerca.py
Básicamente tiene 3 funciones principales.
1. get_auto
2. set_auto
3. read_auto

Cada una de ellas será descrita a continuación.

#### Función get_auto
Esta función me permite obtener los datos de la API de patiotuerca.com
~~~
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
~~~
Básicamente la función consume la API y luego devuelve varios valores en un JSON que son cargados en un diccionario, pero la 
lectura la limitamos a un número especifico de respuestas, porque sin éste número la API devuelve errores.

Con ello asignamos iteramos el json y cargamos en un diccionario que lo enviamos de retorno.

#### Función set_auto
Esta función me permite guardar los datos de la API en la base de datos **Atlas**
~~~
def set_auto(document: dict):
    for doc in document:
        _ = client.get_database('examenpatiotuerca').get_collection('vehiculos').insert_one(document=document[doc])
    return 1
~~~
Su funcionamiento es sencillo, recibe un diccionario, y lo iteramos para subir de uno en uno usando pymongo, tratamos 
de usar **insert_many** pero no funcionó, así que mejor solo lo iteramos y guardamos de uno en uno. 

#### Función 
Esta función me permite leer todos los datos de la API en la base de datos **Atlas**
~~~
def read_auto()-> dict:
    result = client.get_database('examenpatiotuerca').get_collection('vehiculos').find()
    return result
~~~
Al igual que la función anterior su funcionamiento es sencillo, solo leemos todos los datos de la base de datos mongoDB 
y retornammos el resultado, que luego será iterado en pagina web. 
***
_Para finalizar quiero indicar que hay funciones que no se utilizan, pero es porque hice varias pruebas antes usar estas 
últimas_
***
## Problemas presentados

El principal problema que tuve es el tiempo, me hubiera gustado hacer mejores cosas, pero lastimosamente calculé mal
mis deberes profesionales, familiares y de estudiante de maestría, a parte de ello, cualquier problema que surgió lo 
resolví leyendo los manuales directamente en las páginas oficiales, especialemente de Flask y de Jinja2, si bien puede 
ver que hay código que no se utiliza es porque repeti varias veces la clase que nos impartió hasta entenderla muy bien
y luego de eso, solo fue leer manuales. Adicionalmente debo agregar que no he trabajado con python en ningún proyecto
pero ahora entiendo porque es tan popular.

También quiero comentarle que yo tengo mucho años de experiencia en el desarrollo por ello no se me complicó mucho 
el examén y espero obtener una buena nota. 

Para finalizar este _README_ voy presentar las características del software usado para realizar este exámen.
***
## Mapa de Navegación APIs [Realizado en excalidraw.com]

![Pagina index.html](/Mapa_de_navegacionAPIs.png)
***
## Specs
* Python 3.11.4
* pymongo 4.5.0
* requests 2.31.0
* Flask 2.3.3
* python-dotenv 1.0.0

>“Incluso cuando te tomas unas vacaciones de la tecnología, la tecnología no se toma un descanso de ti”. Douglas Coupland