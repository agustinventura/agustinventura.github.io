title=Docker y almacenamiento: Como cambiar el directorio de las imágenes y contenedores
date=2019-03-07
type=post
tags=SQL, Docker, PostgreSQL
status=published
~~~~~~

Los contenedores no solo tienen la ventaja de ser entornos aislados sino que además ocupan muy poco espacio en disco. Esto se debe a varias causas:

1. No tienen el sistema operativo al completo (como una máquina virtual) lo cual ya de por sí es un ahorro de espacio.
2. El proceso de tener una imagen e ir "instanciando" contenedor no ocupa tanto como podríamos esperar (tamaño de imagen x contenedores) gracias a [UnionFS](https://stackoverflow.com/questions/32775594/why-does-docker-need-a-union-file-system), ya que solo se cambian los cambios de cada contenedor en particular.

Esto esta de maravilla y por ejemplo, hoy he montado un [Oracle XE en un contenedor](https://github.com/fuzziebrain/docker-oracle-xe) para lo que he tenido que hacer mi propia imagen. Si hago

```prettyprint
docker image ls
```

Puedo ver que la imagen de Oracle Linux sobre la que se monta mi imagen de Oracle XE pesa 117 Mb y la imagen de Oracle XE 8,76 Gb.

![docker image ls](/images/2019/03/07/docker-image-ls.png)

Si ahora miro el tamaño del contenedor con

```prettyprint
docker container ls -s
```

El contenedor ocupa apenas 471 Mb. Nada mal, ¿eh?

![docker container ls -s](/images/2019/03/07/docker-container-ls-s.png)

Sin embargo, hay veces en que estamos limitados en espacio. Por ejemplo, yo tengo un SSD, compartido con Windows 10 (aunque no sé para qué si lo arranco de higos a brevas) y además en mi Ubuntu tengo dos particiones, una para / con 28 Gb y otra para /home con 59 Gb.

![df -h | grep sda](/images/2019/03/07/df-h-grep-sda.png)

Entonces no me interesa guardar las imágenes y los contenedores en / ya que me lo llenaría (sobre todo en este caso que Oracle es más bien glotón), por lo que me interesa cambiar el directorio en el que Docker guarda los datos.

##Moviendo el directorio de datos de Docker

Buscando un poco en mi caso concreto, Ubuntu, he llegado a [esta guía](https://askubuntu.com/questions/631450/change-data-directory-of-docker) que lamentablemente esta obsoleta. En todo caso propone hacer un symlink, cosa que siempre debe funcionar, pero no me parece muy limpia.

Si miro el archivo que citan en esa solución ("/etc/default/docker") se dice que el archivo no aplica para systemd... que es lo que usa Ubuntu (después de abandonar upstart...), pero dan un [enlace a la documentación](https://docs.docker.com/engine/admin/systemd/) en el mismo archivo que tiene la clave: el archivo [daemon.json](https://docs.docker.com/engine/reference/commandline/dockerd//#daemon-configuration-file) que permite configurar el demonio de Docker.

Así que dicho y hecho, basta con irse a /etc/docker y crear el archivo daemon.json si no existe y poner ahí el directorio que quiera, por ejemplo:

```prettyprint
{
	"data-root": "/home/agustin/Development/Docker/data"
}
```
Y ahora, obviamente, toca bajar y volver a subir el servicio:

```prettyprint
sudo service docker stop
sudo service docker start
```

Y listo, a partir de ahora no solo las imágenes, sino los datos de contenedores, volúmenes, etc... me los guardará en ese directorio (que al estar en /home es otra partición distinta de /).

