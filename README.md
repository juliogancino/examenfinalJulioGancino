# examenfinalJulioGancino

## EXAMEN FINAL DEL MODULO TRATAMIENTO DE DATOS
### SISTEMA DE CONSUMO DE DATOS DE PATIOTUERCA.COM

>En este documento va a encontrar las directrices de como manejar el sistema que generar'a al clonar este repo.

######
El sistema tiene 4 partes importantes
- Menu principal
- Inicio
- Carga de vehículos desde la API de patiotuerca.com
- Visualizador de vehículos cargados desde MongoDB Atlas

Toda la interfáz gráfica fue desarrollada **responsive**, esto quiere decri que se adapta automáticamente a cualquier 
dispositivo, para ello usamos el framework Bootstrap.

***
## Menu principal

Todas las paginas pueden ser accedidas desde el menú principal.
![Pagina index.html](/static/images/menu.png)
Que esta conformado de dos opciones y un buscador
* Inicio: que me lleva al inicio de la página
* Data In MongoDb: que me lleva a una página donde puedo ver todos los vehiculos que subí  a la base 
  de datos
* Buscar: Es un buscador de veh'iculos directamente a la p'agina de https://ecuador.patiotuerca.com/, 
por defecto esta seteado para buscar 6 veh'iculos. Puede aceptar cualquier tipo de nombre de marca 
incluso nombres separados como Mercedes Benz.  

***
## Inicio

![Pagina index.html](/static/images/index.png)

Como se muestra en la imagen, esta es la página principal de la aplicación, es el archivo index.html que es llamado
desde el archivo api.py y usando flask para renderizar el html.

Su funcionamiento es simple, solo debemos colocar el nombre de una marca en al parte que nos lo pide, y el número de
vehículos que quiere que se muestren. Porqué lo hago así?, pues porque al consumir la API de patiotuerca encontré que 
si no se pone un numero de pedido, falla la respuesta. y después de varias pruebas establecí que sean 6.
Al presionar el botón Cargar ejecuta el siguiente código.

~~~
@app.route("/carga_vehiculo", methods=["POST"])
def get_vehi():
    v = (request.form['marca'])
    n = int((request.form['numero']))
    dic = get_auto(v, n)
    # dic = ["juan","pedro",'jose']
    return render_template('get_vehiculo.html', vehi=v, num=n, dics=dic, ok=0)
~~~
Que consume la funcion get_auto que a su vez consume la API de patiotuera y me retorna una nueva página web que es la 
que se muestra en el siguiente punto.

***
## Carga de vehículos desde la API de patiotuerca.com
![Pagina index.html](/static/images/cargavehiculo.png)

Como se muestra en la figura anterior se ha realizado una búsqueda de 3 vehículos Mercedes Benz.

El siguiente paso es presionar el botón **Cargar** y lo que reraliza es una carga a la base de datos de MongoDB Atlas 
usando el siguiente código:
~~~
@app.route("/guarda_vehiculo", methods={"POST"})
def set_vehi():
    v = (request.form['marca'])
    n = int(request.form['numero'])
    document = get_auto(v, n)
    ok = set_auto(document)

    return render_template('get_vehiculo.html', vehi=v, num=n, dics=document, ok=ok)
~~~
Que consume la función get_auto para realizar una busqueda con los datos preestablecidos, y luego ejecuta ota función 
llamada set_auto que guarda los vehículos en la nube, finalmente retorna un valor si ha ingresado correctamente, y 
renderiza la misma página, pero con la variable **ok** para que muestre un mensaje de guardado exitosamente, como se 
muestra en la siguiente imagen.
![Pagina index.html](/static/images/cargavehiculoOK.png)

Como adicional, si no queremos guardar esos vehículos y queremos otra nueva búsqueda, no necesitamos volver a la 
página _Inicio_, sino que directamente podemos realizar la búsqueda desde el **buscador** incorporado en el menú de la 
cabecera.![Pagina index.html](/static/images/buscador.png)

La diferencia principal entre éste buscador y el menú _Inicio_ es que no podemos elegir el número de vehículos a ver, 
ya que esta seteado a 6.

***
## Visualizador de vehículos cargados desde MongoDB Atlas
En el meú superior podemos dar click en la opción _Data in MongoDB_ y lo que nos hace es cargar todos los vehículos que 
se encuentran en la base de datos ATLAS
![Pagina index.html](/static/images/recuperadb.png)
Para obtener esa info usamos el siguiente código
~~~
@app.route("/data_atlas")
def get_mongo():
    document = read_auto()
    return render_template('get_mongo.html', vehi=document)
~~~

Donde consumimos  la función **read_auto()** para leer los datos de la base mongoDB Atlas, éste nos devuelve un 
diccionario completo, no realizamos búsquedas especializadas, ya sea por nombre o por modelo, es simplemente descargar
toda la base de datos y organizarla en la página web.

Para finalizar este _README_ voy presentar las características del software usado para realizar este exámen.

***
## Specs
* Python 3.11.4
* pymongo 4.5.0
* requests 2.31.0
* Flask 2.3.3
* Jinja2 3.1.2
* python-dotenv 1.0.0
* Boostrap 5.1.3

>“Incluso cuando te tomas unas vacaciones de la tecnología, la tecnología no se toma un descanso de ti”. Douglas Coupland