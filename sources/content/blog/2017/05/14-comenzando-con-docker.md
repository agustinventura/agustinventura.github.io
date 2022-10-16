title=Comenzando con Docker
date=2017-05-14
type=post
tags=Docker
status=published
~~~~~~
[Docker](https://www.docker.com/) es una tecnología de contenedores relativamente reciente (de 2013) que si bien ha puesto sobre el terreno de juego el concepto de contenedores (aunque estos son tan antiguos como del 2005 que fue cuando salieron con Solaris...). Un contenedor viene a ser una máquina virtual ligera, en realidad es una aplicación (se ejecuta en espacio de usuario, usa el kernel del sistema operativo, etc...) en la que se puede instalar un sistema operativo y unas aplicaciones (una imagen) y por tanto se comportará como una máquina virtual a efectos prácticos. La ventaja de esta aproximación es que mientras una máquina virtual tiene unos recursos fijos que toma del sistema anfitrión, Docker no, con lo que es más eficiente y ligero.
La verdad es que todo el mundo habla de Docker, pero todavía no me he encontrado a nadie que lo use en producción. No obstante, este sistema es muy cómodo para montar entornos de desarrollo.
Lo primero, como siempre, es instalar Docker. La página de [instalación] (https://docs.docker.com/engine/installation/linux/ubuntu/) no refiere aún información para Ubuntu 17.04, a ver que me voy encontrando.
El primer paso de la instalación es instalar una serie de paquetes que para mi sorpresa (no) ya tengo instalados. A continuación, y resumiendo las detalladísimas instrucciones de instalación (esto es buena documentación y lo demás son tonterías), los pasos para la instalación son los siguientes:
```prettyprint
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce
```
Y aquí viene el primer problema, el repositorio añadido es para la versión actual de ubuntu *($lsb_release -cs)* devuelve *zesty*, y aún no hay soporte, así que veo dos opciones, o bien instalo el de xenial (modificando a mano el nombre del repositorio) o bien instalo los binarios. Por lo que veo en [askubuntu] (https://askubuntu.com/questions/909691/how-to-install-docker-on-ubuntu-17-04) lo de instalar la versión de xenial no es tan descabellado, así que nada, palante. Modifico en *sources.list* la definición del repositorio y donde pone *zesty* pongo *xenial* y repito los dos últimos pasos de arriba. Docker instalado :D
Ahora hay otra sección, de pasos tras la instalación. La más relevante es la de ejecutar docker sin tener que usar sudo (ojo, que esto puede ser un riesgo de seguridad, pero como es para un entorno de desarrollo...). Básicamente hay que crear un grupo de usuarios para docker y añadir el usuario actual a ese grupo (y reiniciar la sesión para que pille los cambios, claro):
```prettyprint
sudo groupadd docker
sudo usermod -aG docker $USER
```
A continuación comentan que docker se inicia por defecto al arrancar el sistema. Esto no me parece muy bien ya que no siempre voy a querer iniciar docker, pero bueno, tampoco tengo ganas de liarlo mucho, así que ahí se queda.
Y listo, el resto de paso son resolución de problemas y aspectos avanzados que tampoco me afectan mucho. Ahm... ¿y cómo se verifica que ésto funciona? Muy fácil:
```prettyprint
docker run hello-world
```
Para seguir, esta el [getting-started](https://docs.docker.com/get-started/), que retoma justo en ese paso. Tras un breve repaso teórico (e importante) se pasa a definir un contenedor mediante un Dockerfile, que no es más que un archivo de texto plano en el que se provisiona el sistema a partir de una imagen base y se ejecutan ciertas acciones de configuración. Vamos con el ejemplo:
	FROM python:2.7-slim
	
	WORKDIR /app
	ADD . /app
	RUN pip install -r requirements.txt
	EXPOSE 80
	
	ENV NAME World
	CMD ["python", "app.py"]
Aquí hay tres partes bien diferenciadas:
1. Instalación de la imagen (que ya viene con python en este caso)
2. Configuración del entorno: compartir la carpeta app con el anfitrión, instalar dependencias y abrir el puerto 80 al exterior.
3. Configuración y ejecución de la aplicación concreta.

Como la carpeta donde esta el *Dockerfile* se esta montando en */app*, se crean en esa misma carpeta los archivos *requirements.txt* y *app.py*, con lo que para editar los archivos (y desarrollar) puedo usar mi equipo mientras que para ejecutarlo se usará el contenedor. Con ésto, se puede crear la imagen y ejecutarla:
```prettyprint
docker build -t friendlyhello .
docker run -p 4000:80 friendlyhelloworld
```
Al *build* se le indica el nombre de la imagen y el directorio en el que esta el *Dockerfile* mientras que al *run* se le pasa la redirección del puerto, es decir, el puerto del anfitrión 4000 redirigirá al puerto 80 del contenedor y el nombre de la imagen.
Para el *build* hay que esperar un poco a que descargue de internet :)
Cuando ejecuto el *run* puedo ver que se ha arrancado la aplicación y si accedo al puerto 4000 en localhost, puedo ver en la consola la traza de peticiones HTTP que se ejecutan.
Como esto no siempre es útil, se pueden ejecutar las imágenes en modo *detached* (en segundo plano), tan solo pasando el parámetro *-d* a *run*:
```prettyprint
docker run -d -p 4000:80 friendlyhelloworld
```
Con *docker ps* se puede consultar los contenedores que se estan ejecutando y con *docker stop* se pueden parar:
```prettyprint
docker ps
docker stop e02aa5295525
```
El getting started continúa explicando que existen registro de imágenes en la nube y que puedes guardar ahí tus imágenes y compartirlas y tal (cosa muy útil). Yo me voy a saltar esa parte y sin embargo si voy a probar algo de la [introducción de Okta] (http://developer.okta.com/blog/2017/05/10/developers-guide-to-docker-part-1).
Primero, ¿cómo puedo saber que imágenes tengo en mi sistema?
```prettyprint
docker image list
```
En mi caso tengo tres:
* friendlyhello: La imagen que acabo de crear
* python: La base de la imagen que acabo de crear
* hello-world: La prueba de funcionamiento
Vale, ¿y como puedo borrar una imagen que ya no necesito?:
```prettyprint
docker rmi python:2.7-slim
```
Con ésto por ejemplo me cargo la imagen python:2.7-slim y _todos los contenedores que la usan_, así que ojocuidao. Eso sí, no me cargo las imágenes derivadas como puede ser *friendlyhello*.
Bueno, otra cosa, cuando paro un contenedor (con *stop*) resulta que el contenedor se queda en estado parado. ¿Y si no lo necesito más? Pues puedo listar todos los contenedores (esten en ejecución o no) y borrar el que escoja:
```prettyprint
docker ps -a
docker rm distracted_goodall
```

Y hasta aquí voy a llegar con la introducción, ya que ahora empieza divergir mi camino. En la próxima, Docker y Spring Boot.
