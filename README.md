# CyberAware
Clasificacion de tweets en base a comunidades
## Instalacion en Linux (recomendada para servidor AWS)
La siguiente guia esta hecha para un sistema ubuntu 20.04. Sin embargo funciona para cualquier distribucion Linux, adaptando cada comando al sistema correspondiente.

Para una guia mas detallada puedes seguir los tutoriales de digital ocean
  - <a href="https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-ubuntu-18-04">Apache, MySQL y PHP</a>
  - <a href="https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-phpmyadmin-on-ubuntu-18-04">phpMyAdmin</a>

### Install Apache HTTP Server
```
sudo apt update
sudo apt install apache2
```
### Install MySQL Database
```
sudo apt install mysql-server
sudo mysql
```
- Esto configurara la clave del usuario de mysql para ajustarla al proyecto
- Se recomienda copiar linea por linea para ejecutar por separado
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Unab.2021';
FLUSH PRIVILEGES;
exit
```
### Install PHP Engine
```
sudo apt install php libapache2-mod-php php-mysql
sudo systemctl restart apache2
```
### Install phpMyAdmin Tool

<b>ADVERTENCIA:</b> Durante la instalacion surgiran varios puntos importantes a los que se debe estar atento:

- Lo primero es elegir el motor web que se utilizara. En la lista aparece <b>Apache 2</b> <b>destacado</b> pero aun asi este no esta <b>seleccionado</b> por lo que se apretar la <b>barra espaciadora</b> para marcarlo (aparecera un asterisco) luego presionar <b>TAB</b> y <b>ENTER</b> para continuar la instalacion.
- La segunda seleccion es para las crenciales simplemente selecciona <b>YES</b> y presiona <b>ENTER</b>
- En la tercera nos pedira ingresar manualmente una clave, escribimos <b>Unab.2021</b> y le damos <b>ENTER</b>
```
sudo apt install phpmyadmin php-mbstring php-zip php-gd php-json php-curl
sudo phpenmod mbstring
sudo systemctl restart apache2
```
### Configurar la base de datos
- Crear base de datos con el nombre <b>CyberAware</b>
- Importar el archivo <b>CrearTablas.sql</b> ubicado en ``` /cyberaware/scripts/misc/ ```
### Install Miniconda
- Descargar miniconda desde <a href="https://docs.conda.io/en/latest/miniconda.html">aqui. </a>
- Una vez descargado dirigirse a la ubicación del archivo y correr el siguiente comando
```
bash Miniconda3-latest-Linux-x86_64.sh
```
### Levantar Página Web
- Instalar las librerias de python necesarias para el proyecto. En el directorio <b>/cyberaware/script</b> correr el siguiente comando:
 ```
 pip install -r requsitos.txt
 ```
- Copiar el directorio a <b>/var/www/html/..</b>
- Descargar las stopwords: abrir un entorno de python e ingresar las siguientes lineas:
```
import nltk
nltk.download('stopwords')
```

- Una vez instaladas las librerias tenemos que levantar el servicio ubicado en ```/cyberaware/scripts/misc/OLDtrash```:
```
nohup python Servicio.py &
```
### Antes de ejecutar script de python.
- Asegurarse de modificar las rutas desde el archivo ```/cyberaware/config.ini```
- Asegurarse de ingresar los tokens de la API de Twitter y las credenciales de la base de datos en el archivo ```/cyberaware/.env```
- <b>IMPORTANTE</b>:

  Las credencias de la base de datos configuradas en el .env solo funcionaran en los script de python. 
  Los archivos .php ubicado en /cyberaware/front/template y /cyberaware/back/ no  toman las credenciales desde el archivo .env y deben ser copiadas "en duro"
  en los siguientes archivos:
  - ```/cyberaware/back/tweets/tabla_tweets.php```
  - ```/cyberaware/back/tabla-buscador.php```
  - ```/cyberaware/back/data-grafico.php```
  - ```/cyberaware/back/tweets/tabla_tweets.php```
  - ```/cyberaware/front/comunidades.php```
  - ```/cyberaware/front/editar.php```


- Por ultimo correr el archivo Main.py en ```/cyberaware/scripts/```:
```
python Main.py
```

### FAQ

- <b>Como modificar la obtencion de datos de los scripts?</b>

  Para cambiar la manera en que se obtienen datos, ya sean Tweets, archivos o cualquier otra fuente de datos (.csv, .txt, etc) se deben modificar los archivos ubicados en ```/cyberaware/scripts/modules/Twitter```.

  Deben modificarse para adaptarlos al nuevo formato de la data. Posterior a eso de deben modificar los archivos InsertarDB.py y/o eliminar el InsertarRT.py, asimismo crear una nueva base de datos acorde a la data que se este recuperando. 
  
  Los demas archivos deberian funcionar sin problema si es que se adapto correctamente la obtencion de datos.

- <b>Como obtener los tokens para utilizar la API de Twitter?</b>

  Se debe crear una cuenta de Twitter de desarrollador y pedir los tokens creando un proyecto en https://developer.twitter.com/en/docs/twitter-api

- <b>Como modificar los Hashtags a consultar con la API?</b>

  Los hashtags deben modificarse en el archivo config.ini. Se deben ingresar cada uno separados con una coma ( , ) sin espacios entre ellos:
    - HT = malware,trojan,ransomware

### Pendientes/Trabajo futuro

- Mejoramiento: Modificar el bautizar comunidades (```/cyberaware/front/editar.php```)
  - Posee una interface básica
- Pendiente: Pasar a inglés PoC
