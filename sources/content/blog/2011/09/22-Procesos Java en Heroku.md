title=Procesos Java en Heroku
date=2011-09-22
type=post
tags=Heroku,Java,Programación,Tools of the Trade,tutorial
status=published
~~~~~~
Heroku no solo sirve para ejecutar aplicaciones web Java, sino que en realidad sirve para ejecutar cualquier tipo de aplicación Java. Observando el proyecto podemos ver que hay dos aplicaciones bien diferenciadas, la aplicación web (que se lanza a través del script webapp generado por Maven) y la aplicación SchemaGenerator, ejecutada a través del script schemaGenerator. Mientras que la primera es una aplicación web normal y corriente, SchemaGenerator es simplemente un proceso Java puro, se lanza se ejecuta y termina sin ningún tipo de interfaz gráfica involucrada.

A este tipo de proceso en Heroku le llaman "worker process", podría traducirlo de cualquier manera, pero paso, así que se queda como proceso worker, hala.

<strong>Tercer Práctica</strong>

El objetivo de esta práctica es desarrollar una aplicación que inserte un tick en la base de datos cada segundo. Se podrá visualizar refrescando la misma página ticks.jsp y posteriormente la escalaré a dos dynos.

Pasos:

<ol>
	<li>Crear la clase Ticker.java que insertará un tick en la base de datos cada segundo.</li>
	<li>Probar la aplicación en local.</li>
	<li>Desplegar la aplicación en Heroku, escalarla a dos dynos y detenerla.</li>
</ol>

<strong>Paso 1</strong>

Creo la clase Ticker.java, el código es trivial, con un while(true) y un sleep(1000), de todas formas queda en GitHub.

Se declara el programa en el pom.xml para generar el script que lo lanza:

```prettyprint linenums

	es.aguasnegras.helloheroku.Ticker
	ticker
```

<strong>Paso 2</strong>

Se instala en local y se ejecuta:

```prettyprint linenums
mvn install
export REPO=~/.m2/repository
export DATABASE_URL=postgres://helloheroku:helloheroku@localhost/helloheroku
sh target/bin/ticker
```

Y en otra consola:

```prettyprint linenums
export REPO=~/.m2/repository
export DATABASE_URL=postgres://helloheroku:helloheroku@localhost/helloheroku
sh target/bin/ticker
```

Ahora puedo comprobar en localhost:8080/ticks.jsp que efectivamente, se van actualizando los ticks independientemente de la aplicación.

<strong>Paso 3</strong>
Vale, ahora a desplegarla en Heroku. Para poder ejecutar el proceso en Heroku en su propio dyno, hay que declararla en el Procfile:

```prettyprint linenums
tick: sh target/bin/ticker
```

Listo, añado a git y subo a GitHub y Heroku:

```prettyprint linenums
git add .
git commit -m "añadido proceso worker"
git push github master
git push heroku master
```

Si abro http://fierce-autumn-4530.herokuapp.com/ticks.jsp puedo ver que todo sigue igual, cada vez que recargo la página se añade un tick a la base de datos. Voy a arrancar el worker:

```prettyprint linenums
heroku scale tick=2
```

Si hago un heroku ps me confirma que se han arrancado dos procesos, y es más, un heroku logs -t va refrescando la salida con dos ticks cada segundo, uno tick.1 y otro tick.2.
Además el jsp me confirma que se han ido insertando en la base de datos.
Bueno, pues ya esta. A poner el código en GitHub

<strong>Código en GitHub</strong>
<a href="https://github.com/agustinventura/helloheroku/tree/1429c05b2a83745dfda1d1f08145f7954d9922d0"><img class="aligncenter size-full wp-image-255" title="GitHub" src="/images/2011/08/github_icon.png" alt="GitHub" width="115" height="115" /></a>

<strong>Conclusiones</strong>
Bueno, pues ya he visto como se ejecuta un proceso demonio y he trasteado un poco el Procfile, que es otro fleco que convendría investigar un poco, a ver que más cosas se pueden hacer.
Es curioso que el proceso se lanza mediante un scale y no un heroku run, supongo que podría igualmente con el heroku run... a ver. Efectivamente, se puede ejecutar igualmente con un heroku run, la diferencia es que no se puede escalar, claro.
