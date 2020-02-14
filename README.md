# Ruuvi-microPython-TTN
Conecta Ruuvi a LoPy y este a TTN
### Descargar el código del repositorio github

El primer paso se tratará en descargar el código del correspondiente repositorio. Para ello, la forma más sencilla es usar el comando git clone con la respectiva URL del repositorio que queramos descargar.
### Subir el código al dispositivo Pycom

Una vez obtenemos el código del repositorio, debemos conectar nuestro dispositivo y encontrar cual es el nombre del puerto asociado. En nuestro caso, hemos entrado al directorio dev y dentro de la subcarpeta serial ejecutar un ls -ltr de unos de los dos archivos existentes.
Con esto hecho, podemos usar la herramienta mpfshell con el nombre del puerto que está empleando nuestro dispositivo para acceder al LoPy. Así, de este modo, podemos subir los ficheros tanto en las carpeta flash como en lib.
Se ha de tener precaución en que ruta colocamos los archivos, deben estar alojados dentro de /flash/.
### Modificar el código

Para que el código funcione en nuestro dispositivo primero debemos habernos creado una cuenta en TTN y registrar nuestro dispositivo, en nuestro caso una Lopy4.
A continuación, debemos modificar los datos de conexión a TTN con los datos obtenidos en nuestra console, estos datos se modifican en el archivo principal ‘lab3main.py’. Nos hará falta el app_eui, key_dev y el dev_eui.
Hay que tener en cuenta que el código está hecho para ser ejecutado en la frecuencia europea, habrá que modificar la frecuencia según en el país que estemos.
### Ejecutar el código

Desde mpfshell poniendo el comando ‘repl’ accedemos al repl, reiniciamos nuestro dispositivo para descartar cualquier tipo de problema y lanzamos el archivo principal, en nuestro caso lab3main.py por tanto usamos ‘import lab3main’. Esto ejecutará un bucle que envía periódicamente los datos de la ruuvi al TTN.

### Decodificación de los datos
    
Desde TTN podremos comprobar si los datos han llegado correctamente, en caso de que lo haga habrá que decodificarlos con un código en JavaScript. 

~~~
function Decoder(bytes, port) {
  var ruuvitags = {};
  var tagname = "";
  var tags = bytes.length / 5;
    var temperature = (bytes[0] << 8) | bytes[1];
    var humidity = (bytes[2] << 8) | bytes[2];
    if (bytes[0] === 0) { tagname = "stable"; }
    else if (bytes[0] === 1) {tagname = "greenfield";}
    ruuvitags= {
        "humidity": humidity/100 ,
        "temperature":temperature/100
    };
    bytes.splice(0, 5);
  return ruuvitags;
}
  
~~~

En el siguiente código hemos realizado modificaciones respecto el decodificador propuesto por el autor del repositorio que se ha seguido de guia. Estos cambios se han realizado porque al usar nosotros un solo dispositivo ruuvi no hemos visto que sea eficiente incrustar el id del propio dispositivo.
    Se ha modificado el desplazamiento y posición de los bytes ya que no se ha codificado ni enviado exactamente de la misma forma.



### Extracción de los datos

TTN no almacena los datos que le llegan por tanto si deseamos conservarlos debemos exportarlos a una plataforma que lo permita o a nuestro propio servidor. En nuestro caso hemos optado por Ubidots.
El primer paso para ello es crear una cuenta en Ubidots. La integración de Ubidots se realiza en el apartado Integration de nuestro Device en TTN, simplemente seleccionamos Ubidots ponemos el Token de Ubidots en el apartado correspondiente y ya envía los parámetros que hayamos puesto en el Decodificador, en nuestro caso temperature y humidity.
