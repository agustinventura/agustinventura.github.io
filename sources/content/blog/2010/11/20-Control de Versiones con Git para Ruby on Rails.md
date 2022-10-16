title=Control de Versiones con Git para Ruby on Rails
date=2010-11-20
type=post
tags=Programación,Ruby on Rails
status=published
~~~~~~
Vale, una semana más tarde, siguiente capítulo, Git. En Subversion ya soy el experto de la empresa, así que mato dos pájaros de un tiro aprendo Git por el mismo precio :)

Ya lo tengo instalado siguiendo las instrucciones de <a title="Pro Git" href="http://progit.org/" target="_blank">Pro Git</a>, así que seguimos para adelante, la sugerencia de usar co en vez de checkout ya que checkout es demasiado "verbose" me la voy a saltar también, me gusta lo verbose (soy de los que odian los splash screens de las distros de linux, me gusta ver el texto).

El core editor, según la sección de instalación de Pro Git esta establecido como gVim, por si acaso, checkeo:

```prettyprint linenums
git config --list
```

Salida

```prettyprint linenums
user.name=Agustin Ventura
user.email=agustin@aguasnegras.es
core.editor=gvim
merge.tool=gvimdiff
```

Todo correcto, toca crear el primer repositorio. En la raíz de la aplicación de pruebas que hice (first_app) ejecuto:

```prettyprint linenums
case@aesir:~/RoR/proyectos/first_app$ git init
Initialized empty Git repository in /home/case/RoR/proyectos/first_app/.git/
```

Con esto he creado el repositorio, ahora el tutorial comenta que para llevar la lista de los archivos ignorados git usa un archivo .gitignore y que rails ya me ha creado uno por defecto conteniendo según que tipos de archivo (los logs, los de sqlite, los tmp...), vaya que viene todo integrado, muy bien. Como estoy usando gVim, sigo el consejo del tutorial y dejo el .gitignore tal y como sigue:

```prettyprint linenums

.bundle
db/*.sqlite3*
log/*.log
*.log
tmp/**/*
tmp/*
doc/api
doc/app
*.swp
*~
.DS_Store

```

Y ahora vamos a añadir los archivos que ya tenemos, tan fácil como

```prettyprint linenums

git add .

```

Ya está, por lo visto van a parar a una lista de "archivos para enviar a git", una especie de caché, podemos comprobar que archivos hay ahí con

```prettyprint linenums

git status

```

Que claro, ahora mismo son todos, jeje... Es hora de hacer commit con, si, eso mismo:

```prettyprint linenums

git commit -m "Commit Inicial del Proyecto first_app"

```

Me gusta que git te obligue a poner siempre un comentario en los commit, eso esta muy bien.
Con esto he hecho los cambios al repositorio local, no al remoto, vaya que esto funciona en dos niveles, un poco "a là" Maven.
Por último, para ver los commits

```prettyprint linenums

git log

```

Es hora de proporcionarse un repositorio remoto, así que habrá que crear una cuenta en <a href="https://github.com/">GitHub</a>.
GitHub ofrece un servicio de hosting gratuito de repositorios para código libre, para ello le doy a "Tarifas y Registros" y pulso en "Crear una cuenta gratuita".
Escojo nombre de usuario, pongo mail y contraseña y listo... vaya, ni siquiera me pide el clásico mail de confirmación. Pues mejor.
En la misma pantalla principal tengo un botón "Nuevo repositorio", así que yo que soy muy valiente le doy del tirón. Nombre, del proyecto, descripción y esta página como web y palante. Esta muy bien, me ponen ahora un tutorial de como empezar a usar el repositorio e incluso como migrar desde SVN.
Ya está creado, es hora de añadir el repositorio y ver que pasa. La guía me avisa que es posible que tenga que mirar unos temas de claves SSH, pero primero voy a probar a pelo, si no, ya nos meteremos en berenjenales.
Primero añado el repositorio remoto:

```prettyprint linenums

git remote add origin git@github.com:agustinventura/first_app.git

```

Y después le doy a enviar los cambios del master (lo que es el trunk en subversion) al repositorio.

```prettyprint linenums

case@aesir:~/RoR/proyectos/first_app$ git push origin master
The authenticity of host 'github.com (207.97.227.239)' can't be established.
RSA key fingerprint is 16:27:ac:a5:76:28:2d:36:63:1b:56:4d:eb:df:a6:48.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'github.com,207.97.227.239' (RSA) to the list of known hosts.
Permission denied (publickey).
fatal: The remote end hung up unexpectedly

```

Falla, toca leer el <a href="http://help.github.com/linux-key-setup/">tutorial</a>, que casualmente usa Ubuntu, así que no debe ser muy complicado.
El tutorial dice que en .ssh en mi home, debo tener una serie de claves id_rsa o id_dsa y que haga una copia porque las vamos a generar... no es el caso, así que paso a generarlas.

```prettyprint linenums

ssh-keygen -t rsa -C "agustinventura@aguasnegras.es"

```

Y listo, generados el id_rsa y el id_rsa.pub.
Ahora en GitHub le doy a "Configuración" y añadir una nueva clave pública, es bastante sencillo, donde pone "Llave" pongo el contenido de id_rsa.pub (ays, benditas clases de Introducción a la Matemática Discreta...).
Para comprobar si todo ha ido bien:

```prettyprint linenums

ssh git@github.com
PTY allocation request failed on channel 0
ERROR: Hi agustinventura! You've successfully authenticated, but GitHub does not provide shell access
                     Connection to github.com closed.


```

Perfecto, vuelvo a hacer el push.

```prettyprint linenums


Counting objects: 63, done.
Compressing objects: 100% (49/49), done.
Writing objects: 100% (63/63), 86.09 KiB, done.
Total 63 (delta 2), reused 0 (delta 0)
To git@github.com:agustinventura/first_app.git
 * [new branch]      master -> master

```

Volviendo al tutorial de RoR, me encuentro con que también me hacen una introducción a un flujo de trabajo basado en branch, edit, commit, merge.
Las ventajas de esto son evidentes, si trabajamos en un branch, tenemos siempre el master "limpio", dicen que git es muy bueno haciendo los merge... ya veremos.
Creo la rama

```prettyprint linenums

git checkout -b modify-README
Switched to a new branch 'modify-README'

```

Perfecto, estoy en la rama. Para la edición de ejemplo, se recomienda usar un lenguaje de formateo llamado <a href="http://daringfireball.net/projects/markdown/">Markdown</a>, por lo visto es para convertir fácilmente a xhtml y GitHub lo reconoce para el formateo de según que documentos, ya le echaré un vistazo.
Renombro el archivo como README.markdown y lo edito para poner lo sugerido en el ejemplo.

```prettyprint linenums

git mv README README.markdown
gvim README.markdown 

```

Con git -status compruebo que todo este bien y hago commit, usando git commit -a me puedo saltar el comando add, ya que lo ejecuta solo.

```prettyprint linenums

git commit -a -m "Modificado archivo README"
[modify-README ee90542] Modificado archivo README
 2 files changed, 5 insertions(+), 256 deletions(-)
 delete mode 100644 README
 create mode 100644 README.markdown

```

Para hacer el merge, se hace un checkout del master y un merge de la rama.

```prettyprint linenums

git checkout master
Switched to branch 'master'
git merge modify-README
Updating 0afa892..ee90542
Fast-forward
 README          |  256 -------------------------------------------------------
 README.markdown |    5 +
 2 files changed, 5 insertions(+), 256 deletions(-)
 delete mode 100644 README
 create mode 100644 README.markdown

```

Y listo, se borra la rama

```prettyprint linenums

git branch -d modify-README
Deleted branch modify-README (was ee90542).

```

Por último, push y voy a GitHub a ver si ha funcionado.

```prettyprint linenums

git push
Counting objects: 4, done.
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 419 bytes, done.
Total 3 (delta 1), reused 0 (delta 0)
To git@github.com:agustinventura/first_app.git
   0afa892..ee90542  master -> master

```

Todo perfecto en GitHub... Hora de un descanso.