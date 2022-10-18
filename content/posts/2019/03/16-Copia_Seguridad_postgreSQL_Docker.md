title=Copia de Seguridad de PostgreSQL en Docker
date=2019-03-16
type=post
tags=SQL, Docker, PostgreSQL
status=published
~~~~~~

Creo que en los últimos posts ha quedado bien claro las ventajas de Docker, sobre todo en un entorno de desarrollo donde nos permite provisionar rápidamente software que antes era más o menos costoso de instalar, [como una base de datos](https://www.aguasnegras.es/blog/2019/03/05-PostgreSQL_y_Docker.html) y también ha quedado claro que Docker es una herramienta super flexible, tanto que podemos escoger hasta cual deseamos que sea su directorio de trabajo a través de la [configuración](https://www.aguasnegras.es/blog/2019/03/07-Docker_y_almacenamiento.html).

Sin embargo hay un apartado que no he tocado. Al hablar de infraestructura inmutable comenté como montar el volumen de datos de PostgreSQL con un data bind para que aunque destruyera el contenedor los datos persistieran y pudiera crear un contenedor nuevo para acceder a esos datos. Esta política es muy buena para destruir y recrear contenedores, pero claro, los datos siguen estando en el mismo ordenador, el host, ¿qué pasa si este se estropea?
Es decir, creo que no hay que confundir la disponibilidad de los datos para la infraestructura con una buena copia de seguridad de toda la vida.

##Copia de Seguridad de PostgreSQL
En PostgreSQL la copia de seguridad se realiza con una herramienta llamada [pg_dump](https://www.postgresql.org/docs/11/app-pgdump.html). Esta herramienta me permite exportar los datos en formato inserts de SQL (por defecto) o en formato propietario si es una gran cantidad de datos.

Pero, si entramos en nuestro contenedor y lanzamos este pg_dump generando un archivo con la copia de seguridad... ¿cómo lo paso a mi host para moverlo a la nube o a dónde sea? Hay que tener en cuenta que el único volumen que esta montado es el de los datos, podría crear ahí una carpeta y meter la copia de seguridad, pero seamos sinceros, eso es una guarrada. ¿Entonces?

Contenedor temporal al rescate. El comando pg_dump se puede utilizar en remoto, luego hipotéticamente puedo crear un contenedor en el cual montar un volumen donde haré la copia de seguridad y lanzar desde ese contenedor el pg_dump sobre el contenedor de PostgreSQL. Dicho y hecho:

```prettyprint
docker run --rm --name pg-backup -v /home/agustin/Development/Docker/volumes/pg-backup/:/media/backup -e PGPASSWORD=docker postgres 
pg_dump -h 172.17.0.3 -U postgres -Fc mi-base-de-datos -f /media/backup/mi-backup
```

Creo un contenedor temporal (--rm) en el que montaré un directorio de mi máquina en el directorio /media/backup y le paso como variable de entorno PGPASSWORD, de esta manera al lanzar pg_dump utilizará este valor como contraseña, y ya por último uso pg_dump para realizar el volcado.

Y qué mejor manera para probar que la copia ha ido bien que restaurarla. Se puede hacer de manera equivalente a lo de arriba pero usando pg_restore:

```prettyprint
docker run --rm --name pg-restore -v /home/agustin/Development/Docker/volumes/pg-backup/:/media/backup -e PGPASSWORD=docker postgres 
pg_restore -h 172.17.0.4 -U postgres -d mi-base-de-datos /media/backup/mi-backup
```

Ojo que esto solo realizar el proceso de importación sobre la máquina de la base de datos (en este caso 172.17.0.4), tras eso se borraría y los datos quedaría en esta máquina. Hay que tener también en cuenta que pg_restore solo recupera la base de datos (el schema), no el usuario (role), así que si mi-base-de-datos correspondía al usuario mi-usuario, previamente hay que crear esta base de datos y usuario en el PostgreSQL destino (si no, tampoco pasa nada porque avisa).