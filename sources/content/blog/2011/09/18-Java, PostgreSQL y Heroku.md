title=Java, PostgreSQL y Heroku
date=2011-09-18
type=post
tags=Base de Datos,Heroku,Java,PostgreSQL,Programación,Tools of the Trade,tutorial
status=published
~~~~~~
Ya he visto como desplegar en Heroku, pero lo que he desplegado no llega ni al nivel de aplicación web, en realidad es una página web estática y punto. Para poder considerarla aplicación web ha de tener algún tipo de contenido dinámico, normalmente este contenido se genera de algún almacén persistente, usualmente una base de datos.
Por tanto voy a ver como me las apaño para poner una base de datos en Heroku y atacarla desde mi aplicación. En realidad en la primera práctica, el comentado "heroku config" me daba alguna pista, supongo que usaré una base de datos <a title="PostgreSQL en Wikipedia" href="http://es.wikipedia.org/wiki/PostgreSQL" target="_blank">PostgreSQL</a> alojada en <a title="Amazon Web Services" href="http://aws.amazon.com/es/" target="_blank">AmazonWeb Services</a>, vamos a ver si es así, pero antes...

<strong>Instalación de PostgreSQL</strong>

Para poder desarrollar y desplegar en local hará falta una instancia de PostgreSQL. Afortunadamente la instalación en debian/ubuntu/mint es tan sencilla como:

```prettyprint linenums
sudo apt-get install postgresql
```

PostgreSQL es un metapaquete que contiene varias utilidades, el servidor (versión 8.4), el cliente (versión 8.4) y sus dependencias.

Para no liarme voy a seguir el <a title="Heroku for Java Workbook" href="https://github.com/heroku/java-workbook" target="_blank">Heroku for Java Workbook</a> a la hora de configurar el PostgreSQL.

Lo primero es crear un usuario de PostgreSQL con privilegios de superusuario. En el libro lo llaman foo, pero como a mí no me gusta un nombre tan genérico lo voy a llamar helloheroku... mucho mejor, no veas... :P

```prettyprint linenums
sudo -u postgres createuser -P helloheroku
```

Como viene siendo habitual, ahora hay que contestar una serie de preguntas:

<ol>
	<li>Contraseña: helloheroku</li>
	<li>Repetir la contraseña: pues eso</li>
	<li>¿Es superusuario?: s</li>
</ol>

Creo la base de datos como tal. Será una base de datos en localhost, se llamará helloheroku y la creará el usuario helloheroku:

```prettyprint linenums
createdb -U helloheroku -W -h localhost helloheroku
```

De contraseña, helloheroku. Y pruebo la conexión:

```prettyprint linenums
psql -U helloheroku -W -h localhost helloheroku
Contraseña para usuario helloheroku:
psql (8.4.8)
conexión SSL (cifrado: DHE-RSA-AES256-SHA, bits: 256)
Digite «help» para obtener ayuda.

helloheroku=# \q
```

De propina, como trabajar con una base de datos en modo CLI es un poco... árido, voy a instalar <a title="pgAdmin" href="http://www.pgadmin.org/" target="_blank">pgAdmin</a>:

```prettyprint linenums
sudo apt-get install pgadmin3
```

Y listo, ahora sí, práctica dos.

<strong>Segunda Práctica</strong>

El objetivo de esta práctica es crear una página web que guarde el número de veces que es cargada. Así de fácil.

Para ello se usará una tabla de base de datos que guardará un timestamp. Se creará también una página en JSP que cada vez que se cargue, almacenará un nuevo timestamp (llamado tick), en la base de datos y mostrará el número de ticks que hay en total.

Esta solución se puede hacer tan fácil o compleja como se quiera. Pero en un alarde de sentido común, el cuaderno de trabajo propone hacerlo en JSP y JDBC plano, sin más historias. Es muy interesante el comentario de que Heroku es compatible con Hibernate o JPA.

En resumen, estos son los pasos que se darán:

<ol>
	<li>Configurar la aplicación web del tutorial anterior para usar PostgreSQL.</li>
	<li>Crear el DAO en Java (la clase que se encargará de acceder a la base de datos).</li>
	<li>Crear la página JSP que al cargarse inserte un tick en la base de datos y muestre los que hay.</li>
	<li>Crear una clase que se ejecutará al ser desplegada la aplicación y que creará el esquema de base de datos.</li>
	<li>Probar en local.</li>
	<li>Desplegar en Heroku.</li>
</ol>

Hay que reconocer que el paso cuatro es un poco raro, lo más normal sería ejecutar previamente las operaciones que sean sobre la base de datos por separado, pero vamos a ello.

<strong>Paso 1</strong>

Para añadir el soporte de PostgreSQL basta con añadir la dependencia al pom.xml:

```prettyprint linenums

<!-- PostgreSQL -->
<dependency>
	<groupId>postgresql</groupId>
	<artifactId>postgresql</artifactId>
	<version>9.0-801.jdbc4</version>
</dependency>

```

Y listo, ahora se puede crear el DAO.

<strong>Paso 2</strong>

No voy a copiar la clase DAO ya que es bastante convencional, basta con copiarla y pegarla en un archivo llamado TickDAO.java en el mismo directorio que el Main.java (no debiera ser así pero tampoco me voy a poner exquisito para una prueba de concepto). Sin embargo si que voy a comentar las cosas que me vayan llamando la atención.

Lo primero es que no se crea ningún tipo de pool de conexiones ni nada, lo único que hay es un bloque de código estático que lee la url de la base de datos de la variable de entorno del dyno "DATABASE_URL" y la parsea para adaptarla a lo que espera jdbc, guardándola después en una variable estática.

La conexión se abre y se cierra en cada uno de los tres métodos que acceden a la base de datos, que son para insertar un tick nuevo, para leer cuantos ticks hay y para crear la base de datos (supongo que este método se llamará desde la clase que se ejecuta para crear el esquema de la base de datos).

También es interesante ver que no se hace ningún tipo de tratamiento de errores, aparte de un finally para cerrar la conexión. Las excepciones simplemente se relanzan para arriba.

Asímismo no hay ningún framework de gestión de logs, se usa System.out. Ya en la práctica anterior, en la sección de logs decía que el comando "heroku logs" funcionaba sobre System.out y System.err, aún así molaría tener algún tipo de framework para poder gestionar más fácilmente los logs y activar y desactivar declarativamente los de debug, por ejemplo. Supongo que no será muy complicado de integrar (en realidad espero que sea inmediato).

Nada más que comentar, la clase no es ninguna maravilla, pero funcionará y es para lo que es.

<strong>Paso 3</strong>

El jsp lo pongo directamente en src/main/webapp, y se llama ticks.jsp. No tiene nada de particular, son dos scriptlets JSP.

El primero instancia un TickDAO y llama a la función insertTick.

El segundo llama a la función getTickCount y listo.

Me hace gracia que comentan que es importante saber que el acceso a base de datos no esta transaccionado y por tanto dos usuarios concurrentes podrían tener problemas de lecturas no consistentes. En fín, nunca es tarde para inculcar buenas prácticas, supongo.

<strong>Paso 4</strong>

En este paso en general se añadirán los mecanismos para hacer que la base de datos exista al ejecutar la aplicación.

En primer lugar, creo una clase SchemaCreator.java en src/es/aguasnegras/helloheroku que simplemente instancia un TickDAO y llama a su función createTable().

Después añado al pom.xml lo siguiente en la sección programs del plugin appassembler-maven-plugin como primer elemento:

```prettyprint linenums


<program>
	<mainClass>es.aguasnegras.helloheroku.SchemaCreator</mainClass>
	<name>schemaCreator</name>
</program>

```

De esta manera consigo que cuando se ejecuta Maven sobre el proyecto, se generan scripts (tanto de shell como .bat) que me permiten lanzar tanto la clase SchemaCreator como Main.

Me surge una duda... efectivamente, el createTable() hace un "drop table if exists", así que cada vez que se ejecute el script, se creará la base de datos desde cero. Tampoco es que me importe, vaya.

Bueno, pues ya esta, ahora habrá que probarlo en local, digo yo.

<strong>Paso 5</strong>

Para probar la aplicación, hay que exportar la variable de entorno DATABASE_URL:

```prettyprint linenums
export DATABASE_URL=postgres://helloheroku:helloheroku@localhost/helloheroku
```

No hay que olvidar exportar también la variable REPO:

```prettyprint linenums
export REPO=~/.m2/repository
```

Ahora hay que ejecutar el script que crea la base de datos:

```prettyprint linenums
sh target/bin/schemaCreator
```

Y por último, se lanza la aplicación:

```prettyprint linenums
sh target/bin/webapp
```

Si todo ha ido bien, al abrir en el navegador, http://localhost:8080/ticks.jsp, debería ver 1 Ticks... efectivamente, conforme le voy dando a recargar me va aumentando secuencialmente. Hala, pos yasta, ahora a subir a Heroku.

<strong>Paso 6</strong>

Los pasos, son los de siempre, añadir a git y enviar a heroku (en mi caso, también a GitHub):

```prettyprint linenums
git add .
git commit -m "Añadida interacción con base de datos PostgreSQL como ejemplo"
git push github master
git push heroku master
```

Esta última línea lanza Maven sobre el proyecto como ya se vió y lo compila correctamente.

Para lanzar el proceso schemaCreator, heroku me permite lanzar comandos remotos:

```prettyprint linenums
heroku run "sh target/bin/schemaCreator"
Running sh target/bin/schemaCreator attached to terminal... up, run.1
the jdbc connection string is: jdbc:postgresql://ec2-107-20-227-173.compute-1.amazonaws.com/...?user=...&amp;password=...
Creating ticks table.
```

Abro http://fierce-autumn-4530.herokuapp.com/ticks.jsp en el navegador... et voilà, andando.

<strong>Código en GitHub</strong>

<strong><a href="https://github.com/agustinventura/helloheroku/tree/8e64800881682f1d848a37f9f625f8f0bae21beb" target="_blank"><img class="aligncenter size-full wp-image-255" title="GitHub" src="/images/2011/08/github_icon.png" alt="GitHub" width="115" height="115" /></a>Conclusiones</strong>

Heroku soporta una base de datos plenamente madura, como es PostgreSQL y con un esfuerzo mínimo, de hecho, hay que invertir más tiempo en configurarla en local que en remoto.

De nuevo las dudas que me surgen son administrativas, ¿cuánto espacio tengo de tablespace? ¿Y de conexiones concurrentes? etc...

Quedaría también pendiente usar alguna tecnología más sofísticada para conectar a base de datos, usando algún tipo de pooling de conexiones, pero no me parece complicado para nada.
