title=PostgreSQL en Docker
date=2019-03-05
type=post
tags=SQL, Docker, PostgreSQL
status=published
~~~~~~

Una de las ventajas de [Docker](https://www.aguasnegras.es/blog/2017/05/14-comenzando-con-docker.html) es que te aisla del problema de tener que instalar el software que necesitas para desarrollar.
La encapsulación en contenedores no es solo una ventaja para los pasos a producción y la [infraestructura como código](https://en.wikipedia.org/wiki/Infrastructure_as_code) sino que lo es, especialmente en entornos de desarrollo.
En muchas ocasiones instalas una base de datos o una cola de mensajes y ajustando la configuración te la terminas cargando y tienes que volver a crearla. La ventaja de Docker es que parte de esa premisa, se asume que te vas a cargar el sistema... y que no pasa nada. Y seamos sinceros, esto es muy frecuente que pase en los entornos de desarrollo (para eso estan).
Si bien hay tareas que son relativamente sencillas como instalar un [PostgreSQL](https://www.postgresql.org/) que se puede hacer a tiro de apt, con Docker es MUCHO más sencillo y además tiene la ventaja de que si te cansas, puedes eliminar los contenedores y las imágenes y no has tocado tu sistema.

##PostgreSQL en Docker
Lo primero es traer la imagen de [PostgreSQL](https://hub.docker.com/_/postgres), que es la plantilla a partir de la cual se crea el contenedor en concreto:

```prettyprint
docker pull postgres
```

Con esto ya se puede arrancar un contenedor tal y como indican en la misma documentación de la imagen:

```prettyprint
docker run --name mi-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

Esto funciona y lo que hace es crear un contenedor llamado "mi-postgres" que va a correr en background (-d) y la contraseña de la base de datos va a ser "mysecretpassword".

##Conectarse

Para verificar que funciona, se puede crear un contenedor temporal que se conecte a la base de datos con el mismo cliente psql.

Primero tengo que saber la ip de mi contenedor:

```prettyprint
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' pg-rx
```

Supongamos que esto devuelve 172.17.0.2 ahora creo un contenedor temporal que lanza el psql usando la ip para conectar:

```prettyprint
docker run -it --rm --name psql postgres psql -h 172.17.0.2 -U postgres
```

Con -it se indica a Docker que cree una sesión interactiva y con --rm que al cerrar la sesión se destruya el contenedor. La última parte indica que lo cree a partir de la imagen postgres y que lance el comando psql al host 172.17.0.2 con el usuario postgres. Pedirá la contraseña del usuario "posgres" que será "secretpassword".

##Persistiendo los datos
Hasta aquí muy bien, pero hay dos problemas:

1. Que solo se puede conectar desde otro contenedor ya que el puerto que usa PostgreSQL por defecto solo es accesible a través de la red interna que crea Docker para los contenedores.
2. Que si por lo que sea el contenedor se destruye, se pierden los datos ya que estan en su interior. Esto en un entorno de integración continua me puede dar igual ya que alguna herramienta automatizaría el recuperarlos, pero lo cierto es que tampoco cuesta solucionarlo guardándolo en un directorio del host.

Soluciones:

1. Exponer el puerto 5432 en el host.
2. Utilizar un databind a una carpeta en el host. Se podría utilizar un volume, de hecho es lo recomendado pero como la solución mas habitual que se suele ver es el databind, pues databind.

Primero se crea el directorio para guardar los datos, algo así:

```prettyprint
mkdir -p $HOME/docker/volumes/pgsql
```

Y se crea un contenedor nuevo:

```prettyprint
docker run --name pg -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $HOME/docker/volumes/pgsql/:/var/lib/postgresql/data postgres
```

Cosas nuevas: con el -p se le indica que el puerto "5432" del host (el primer puerto) lo mapee al "5432" del contenedor (el segundo) y con -v que la carpeta creada anteriormente la mapee a la carpeta "/var/lib/postgresql/data". Ojo con esto que si pones otro directorio falla el arranque del contenedor.

Pues ya esta, ahora puedo utilizar una herramienta en mi host como DBeaver para conectar con el PostgreSQL del contenedor y además si por lo que sea hay que cargarse el contenedor, los datos persisten (mientras siga la carpeta, claro).