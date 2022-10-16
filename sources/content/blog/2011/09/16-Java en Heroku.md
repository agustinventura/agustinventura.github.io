title=Java en Heroku
date=2011-09-16
type=post
tags=Heroku,Java,Programación,Tools of the Trade,tutorial
status=published
~~~~~~
Una de las cosas que más me impresionó de Ruby on Rails, más que el framework en sí o el lenguaje, fue el excelente soporte que había creado la comunidad. Hablo específicamente de como se enlazaba tu proyecto local con GitHub y GitHub con Heroku, con lo cual podías tener el proyecto en producción en cuestión de minutos.

Esto es algo que lamentablemente no he visto en Java en los cinco años que llevo dedicado a estos menesteres, y menos con un alojamiento de la categoría de Heroku (otro día hablaré sobre ello y el PaaS, etc...). Pues bien, el pasado 25 de Agosto, <a title="Soporte de Java en Heroku" href="http://blog.heroku.com/archives/2011/08/25/java/" target="_blank">Heroku añadió soporte para Java</a>. Este paso me parece crucial. Desde mi punto de vista, la gran fortaleza de PHP, RoR, etc... viene de la comunidad, es un lenguaje "accesible" a cualquiera, basta con comparar los hostings existentes para PHP y los existentes para Java. Hay otras plataformas para Java, por ejemplo, <a title="Google App Engine" href="http://code.google.com/intl/es-ES/appengine/" target="_blank">Google App Engine</a>, pero desde mi punto de vista son mucho más restrictivas que Heroku. Como de todas formas esto es solo una impresión, he decidido seguir el <a title="Heroku For Java Workbook" href="https://github.com/heroku/java-workbook" target="_blank">Heroku For Java Workbook</a> a ver qué tal resulta :)

<strong>Requisitos</strong>

<ol>
	<li>Cuenta en GitHub.</li>
	<li>Cuenta en Heroku.</li>
	<li>Tener instalado <a title="Git, EGit y GitHub." href="http://www.aguasnegras.es/?p=201" target="_blank">Git</a></li>
</ol>

<strong>Instalación de las herramientas de línea de comando de Heroku (heroku)</strong>

Lo primero es instalar las herramientas de linea de comando de Heroku, llamadas heroku (sin mayúscula), estas a su vez tienen otros requisitos:

<ol>
	<li>Instalar Ruby (apt-get install ruby).</li>
	<li>Instalar RubyGems (se descarga de <a title="RubyGems" href="http://rubygems.org/pages/download" target="_blank">RubyGems.org</a> y se ejecuta sudo ruby setup.rb)</li>
	<li>Se instala el cliente en sí: sudo gem install heroku.</li>
	<li>Para verificar si todo ha ido bien, el comando <em>heroku version</em> debe devolver algo como <em>heroku-gem/2.6.1</em></li>
</ol>

El siguiente paso es añadir nuestra clave SSH pública a Heroku, primero se hace login: heroku auth:login, e introducimos nuestro email y contraseña.

A continuación basta con hacer heroku keys:add y listo, añadida nuestra clave SSH.

<strong>Instalación de Maven</strong>

La instalación de Maven viene descrita en su misma página de descarga de manera bastante sucinta. En cualquier caso estos son los pasos a dar:

<ol>
	<li>Descomprimir el archivo (en mi caso en $HOME/Herramientas).</li>
	<li>Añadir la variable de entorno M2_HOME, que es el directorio de Maven (en este caso sería export M2_HOME=$HOME/Herramientas/apache-maven-3.0.3)</li>
	<li>Añadir la variable de entorno M2 que son los binarios de Maven (export M2=$M2_HOME/bin)</li>
	<li>Añadir la variable MAVEN_OPTS al entorno. Esta variable son comandos que se pasan a la JVM que ejecuta Maven, en nuestro caso será para aumentar la memoria disponible para la ejecución de Maven (por defecto son 64 Mb, pero la vamos a aumentar a 256): export MAVEN_OPTS="-Xms256m -Xmx512m".</li>
	<li>Añadir la variable M2 al Path: export PATH=$M2:$PATH</li>
	<li>Si ejecutamos mvn --version debería salir la versión actual de Maven (3.0.3), la version de la JVM, etc...</li>
</ol>

<strong>Primera Práctica</strong>

El objetivo de esta primera práctica es construir una aplicación web, es decir un simple html con su web-inf, etc. Los pasos son cuatro:

<ol>
	<li>Crear la aplicación web a partir de un arquetipo de Maven.</li>
	<li>Probar la aplicación web en local.</li>
	<li>Desplegar la aplicación web en Heroku.</li>
	<li>Escalar la aplicación web en Heroku.</li>
	<li>Ver los logs de la aplicación en Heroku.</li>
	<li>Deshacer una publicación en Heroku.</li>
</ol>

<strong>Paso 1</strong>

Entro en mi directorio de trabajo (Heroku) y una vez dentro genero el proyecto con la siguiente línea:

```prettyprint linenums
mvn archetype:generate -DarchetypeCatalog=http://maven.publicstaticvoidmain.net/archetype-catalog.xml
```

Ahora Maven irá preguntando por una configuración básica del proyecto, estas son las respuestas que he ido dando:

<ol>
	<li>Pregunta el arquetipo que se desea usar, realmente solo hay uno, así que pulso 1.</li>
	<li>GroupId es el identificador del equipo de desarrollo, en este caso y por nomenclatura Java (es también el prefijo de toda la paquetería): es.aguasnegras</li>
	<li>ArtifactId es el nombre del proyecto: helloheroku</li>
	<li>Version se deja en blanco, será la 1.0-SNAPSHOT</li>
	<li>Package es la paquetería del proyecto, introduzco es.aguasnegras.helloheroku</li>
	<li>Por último, muestra un resumen y pide confirmación: Y.</li>
</ol>

Con esto tengo el proyecto creado según la estructura de directorio estándar de Maven. Debo tener un index.html, un Main.java y un pom.xml que contiene la configuración del proyecto según Maven.

Lo interesante es el Main.java. En Heroku no despliego sobre un servidor de aplicaciones (caso usual en Java) sino que es la misma aplicación la que crea su servidor, Jetty (por eso el arquetipo de Maven era embedded-jetty-archetype). Esto tiene sus pros y sus contras, pero de momento esta bien. Se puede ver en el main de Main.java como se instancia el servidor.

Una ventaja de esto es que voy a poder probar la aplicación en local sin tener que caer en todo el tedio de instalar un Tomcat, un Weblogic, un JBoss o un Glassfish. Y ese es el siguiente paso.

<strong>Paso 2</strong>

Primero hay que tener en cuenta que Maven me gestiona las dependencias (librerías, vaya) en tiempo de compilación, si quiero tenerlas disponibles en tiempo de ejecución (cuando arranque en local), tengo que exportar una variable llamada repo:

```prettyprint linenums
export REPO=~/.m2/repository
```

Para arrancar la aplicación en local, entro en el directorio (helloheroku) y ejecuto:

```prettyprint linenums
mvn install
sh target/bin/webapp
```

Abro en un navegador localhost:8080 y ahí esta: "hello, world".

Para parar la aplicación, Ctrl-c en la consola y listo. Una vez probada en local, hay que moverla (pasarla, exportarla, publicarla... publicarla, sí, me gusta) a Heroku.

<strong>Paso 3</strong>

Para publicar la aplicación en Heroku, primero hay que crear un archivo llamado "Procfile" en el raíz del proyecto y añadirle una línea describiendo como se arranca la aplicación:

```prettyprint linenums
touch Procfile
echo web: sh target/bin/webapp | tee Procfile
```

Creo un repositorio de git para el proyecto:

```prettyprint linenums
git init
git add .
git commit -m "commit inicial del proyecto helloheroku"
```

Ahora viene lo bueno, la parte de cacharreo con Heroku.

Primero creo el stack de Heroku que va a alojar la aplicación, este stack tiene que ser del tipo "cedar" que es el único que admite aplicaciones Java:

```prettyprint linenums
heroku create --stack cedar
Creating fierce-autumn-4530... done, stack is cedar
http://fierce-autumn-4530.herokuapp.com/ | git@heroku.com:fierce-autumn-4530.git
Git remote heroku added
```

El comando me ha devuelto una URL http y otra para git. Si abro la URL en un navegador, me dice que enhorabuena, tengo creada mi app.
Ahora, con git, envío el master local a Heroku:

```prettyprint linenums
git push heroku master
```

Cuando llegue a Heroku veré en la consola que se lanza un proceso de Maven (mvn install) y que se detecta el Procfile y se lanza la aplicación web. Por último, me informa de que se ha desplegado en la URL correctamente.

```prettyprint linenums
-----> Heroku receiving push
-----> Java app detected
-----> Installing Maven 3.0.3..... done
-----> Installing settings.xml..... done
-----> executing .maven/bin/mvn -B -Duser.home=/tmp/build_s6y8o29xnjfx -s .m2/settings.xml -DskipTests=true clean install

-----> Discovering process types
       Procfile declares types -&gt; web
-----> Compiled slug size is 12.8MB
-----> Launching... done, v5
       http://fierce-autumn-4530.herokuapp.com deployed to Heroku
```

Si ahora abro http://fierce-autumn-4530.herokuapp.com/ en el navegador, puedo ver el "hello, world".

Bueno, pues ya esta desplegada la aplicación en un servidor, ahora, ¿cómo se aumenta?

<strong>Paso 4</strong>

Ya esta desplegada la aplicación en un servidor, pero claro, esto no sería la nube si no pudiera ampliar fácilmente los servidores en los que ejecuta. Voy a aumentar la aplicación a dos servidores:

```prettyprint linenums
heroku scale web=2
Scaling web processes...  This action will cause your account to be billed at the end of the month
 For more information, see http://docs.heroku.com/billing
 Are you sure you want to do this? (y/n) y
Scaling web processes... done, now running 2
```

La verdad que no entiendo muy bien como pretenden cobrarme, porque no he dado ningún dato... pero oye... ellos mismos. Aunque habrá que mirar más a fondo el tema de como cobran.

Por último, voy a verificar que efectivamente estan corriendo dos instancias y voy a reducir a una de nuevo:

```prettyprint linenums
heroku ps
Process       State               Command
------------  ------------------  ------------------------------
web.1         up for 17m          sh target/bin/webapp
web.2         up for 2m           sh target/bin/webapp

heroku scale web=1
Scaling web processes... done, now running 1
```

Hasta el momento toda esta información de salida es bastante... escueta. ¿Cómo se ven los logs?

<strong>Paso 5</strong>

Pues muy fácil, hay dos forma de ver los logs, estática o dinámica. Estática, me muestra lo que hay hasta el momento:

```prettyprint linenums
heroku logs
```

Dinámica, no deja de ser un tail, va actualizando el log según se van creando mensajes nuevos:

```prettyprint linenums
heroku logs -t
```

<strong>Paso 6</strong>

Por último, Heroku ofrece soporte para control de versiones. No me refiero solo a código, si no también, como en el ejemplo a variables de entorno, por ejemplo.

Primero me aseguro de que el servidor tiene soporte para el control de releases, mediante el addon de releases:

```prettyprint linenums
heroku addons:add releases:basic
-----> Adding releases:basic to fierce-autumn-4530... failed !    
releases:basic add-on already added.
```

Esta añadido, ahora voy a añadir una variable de entorno y a verificar que se ha hecho:

```prettyprint linenums
heroku config:add MYVAR=42
Adding config vars:  MYVAR =&gt; 42
Restarting app... done, v6.

heroku config
DATABASE_URL        => postgres://tpqbfpkzqb:OILC1r62mtQ5YkqKTeA7@ec2-107-20-227-173.compute-1.amazonaws.com/tpqbfpkzqb
JAVA_OPTS           => -Xmx384m -Xss512k -XX:+UseCompressedOops
MAVEN_OPTS          => -Xmx384m -Xss512k -XX:+UseCompressedOops
MYVAR               => 42
PATH                => .maven/bin:/usr/local/bin:/usr/bin:/bin
REPO                => /app/.m2/repository
SHARED_DATABASE_URL => postgres://tpqbfpkzqb:OILC1r62mtQ5YkqKTeA7@ec2-107-20-227-173.compute-1.amazonaws.com/tpqbfpkzqb
```

Muy bien, pues ahora, toca volver atrás:

```prettyprint linenums
heroku releases
Rel   Change                          By                    When
----    ----------------------          ----------                   ----------
v6    Config add MYVAR    agustinventura@gma..  45 seconds ago           
v5    Deploy cd3c58f          agustinventura@gma..  29 minutes ago           

heroku rollback
Rolled back to v5

heroku config
DATABASE_URL        => postgres://tpqbfpkzqb:OILC1r62mtQ5YkqKTeA7@ec2-107-20-227-173.compute-1.amazonaws.com/tpqbfpkzqb
JAVA_OPTS           => -Xmx384m -Xss512k -XX:+UseCompressedOops
MAVEN_OPTS          => -Xmx384m -Xss512k -XX:+UseCompressedOops
PATH                => .maven/bin:/usr/local/bin:/usr/bin:/bin
REPO                => /app/.m2/repository
SHARED_DATABASE_URL => postgres://tpqbfpkzqb:OILC1r62mtQ5YkqKTeA7@ec2-107-20-227-173.compute-1.amazonaws.com/tpqbfpkzqb
```

¡Listo! Hecha la vuelta atrás a la última publicación estable.

<strong>Código en GitHub</strong>

<strong><a href="https://github.com/agustinventura/helloheroku/tree/cd3c58faf1ceaf0905b390f41f2f51088ca3724b"><img class="aligncenter size-full wp-image-255" title="GitHub" src="/images/2011/08/github_icon.png" alt="GitHub" width="115" height="115" /></a>
</strong>

<strong>Conclusiones</strong>

Pues de momento parece que Heroku ofrece lo que promete, uso de Java estándar, e integración con herramientas actuales: git y Maven. Además me ha sorprendido gratamente la herramienta de consola con más utilidades de lo que parece y que hace muy sencillo aumentar el número de instancias de la aplicación.

Esto sí, echo en falta... un plugin de Eclipse, tendré que investigar si existe o esta en desarrollo.

Igualmente tengo que investigar bien las opciones de facturación y algunos conceptos como dyno, stack, etc...
