title=Add-ons para Heroku
date=2011-09-22
type=post
tags=Heroku,Java,Programación,Tools of the Trade,tutorial
status=published
~~~~~~
La arquitectura de Heroku es modular, es decir, se pueden añadir funcionalidades al Stack mediante piezas de software llamadas add-ons. Un ejemplo de eso lo vi <a title="Java en Heroku" href="http://www.aguasnegras.es/blog/?p=263" target="_blank">aquí</a> cuando añadí el soporte para gestión de releases a través de un add-on.

Hay <a title="Add-ons de Heroku" href="http://addons.heroku.com/" target="_blank">bastantes más add-ons</a> disponibles en la página, para enviar sms, para conectar como amazon rds, etc... Los hay gratuitos, de pago, en beta... en fín, de todo tipo.

En esta práctica voy a añadir el add-on de <a title="Redis en la Wikipedia (inglés)" href="http://en.wikipedia.org/wiki/Redis_(data_store)" target="_blank">Redis</a>.

<strong>Instalación de Redis</strong>

Pues por fín una instalación de un solo paso:

```prettyprint linenums
sudo apt-get install redis-server
```

Una vez instalado, para verificar:

```prettyprint linenums
redis-cli
```

Y debe responder una bonita consola de la que salgo con Ctrl-C.

<strong>Cuarta Práctica</strong>

Dado que Redis es un almacén del tipo clave - valor (key-value), se da bastante bien para hacer cachés, lo que haré será configurar Redis como un almacenamiento que expire cada 30 segundos, es decir que solo se leerá de la base de datos realmente cada 30 segundos, el resto de las veces se impactará contra Redis. Esto es muy burdo, claro, pero sirve para hacer una demo.

Pasos:

<ol>
	<li>Configurar la aplicación para usar Redis.</li>
	<li>Actualizar TickDAO para que use Redis.</li>
	<li>Probar la aplicación en local.</li>
	<li>Desplegar en Heroku.</li>
</ol>

<strong>Paso 1</strong>

Esta parte es tan sencilla como añadir al pom.xml esto:

```prettyprint linenums

<dependency>
         <groupId>redis.clients</groupId>
         <artifactId>jedis</artifactId>
         <version>2.0.0</version>
</dependency>

```

<strong>Paso 2</strong>
En este paso se modifica TickDAO para primero intente leer los ticks de Redis y si no vaya a la base de datos.
En primer lugar añado como variables estáticas un pool de conexiones a Redis (jedisPool) y la clave de los ticks:

```prettyprint linenums

private static JedisPool jedisPool;
private static final String TICKCOUNT_KEY = "tickcount";

```

A continuación, en el bloque de código static en el que inicializo PostgreSQL, aprovecho y cargo también el pool de Redis, solo resalto que la URL de Redis se lee de una variable de entorno llamada REDISTOGO_URL:

```prettyprint linenums

//Inicialización de Redis
Pattern REDIS_URL_PATTERN = Pattern.compile("^redis://([^:]*):([^@]*)@([^:]*):([^/]*)(/)?");
Matcher matcher = REDIS_URL_PATTERN.matcher(System.getenv("REDISTOGO_URL"));
matcher.matches();
Config config = new Config();
config.testOnBorrow = true;
jedisPool = new JedisPool(config, matcher.group(3),
Integer.parseInt(matcher.group(4)), Protocol.DEFAULT_TIMEOUT, matcher.group(2));

```

Por último, el getTickCount() queda así:

```prettyprint linenums

public int getTickCount() throws SQLException {
		Jedis jedis = jedisPool.getResource();
		int tickcount = 0;
		String tickcountValue = jedis.get(TICKCOUNT_KEY);
		if (tickcountValue != null) {
			System.out.println("read from redis cache");
			tickcount = Integer.parseInt(tickcountValue);
		} else {
			tickcount = getTickcountFromDb();
			jedis.setex(TICKCOUNT_KEY, 30, String.valueOf(tickcount));
		}
		jedisPool.returnResource(jedis);
		return tickcount;
	}

```

Es decir, cuando se va a hacer una lectura, primero se hace desde Redis, si el valor no existe (es null) se lee de base de datos y se inserta en Redis.
A probar.

<strong>Paso 3</strong>
Aquí vendría todo el mvn install, etc, pero antes, como  ya estoy harto de andar exportando las variables de entorno cada vez que voy a hacer algo en local, voy a hacer dos cosas.
Primero, voy a crear un exportarVariables.sh que exportar tanto REPO, como POSTGRESQL_URL como REDISTOGO_URL.
Así que:

```prettyprint linenums

gedit exportarVariables.sh

```

Y pongo lo siguiente:

```prettyprint linenums

export REPO=~/.m2/repository
export DATABASE_URL=postgres://helloheroku:helloheroku@localhost/helloheroku
export REDISTOGO_URL=redis://:@localhost:6379/

```

Ahora hago el script ejecutable:

```prettyprint linenums

chmod 777 exportarVariables.sh

```

Y como segundo paso, ya que este archivo solo es aplicable en local, lo añado al .gitignore. Hala, listo, ahora sí que sigo de la manera habitual:

```prettyprint linenums

mvn install
. ./exportarVariables.sh
sh target/bin/webapp

```

Y ahí esta, si entro en localhost:8080/ticks.jsp, veré que siempre muestra los mismos ticks... hasta que pasan 30 segundos, que actualiza la cuenta con el número de veces que haya recargado la página. Es decir, se esta escribiendo en base de datos, pero no se esta leyendo. Hasta pasados 30 segundos, claro.

<strong>Paso 4</strong>
Vale, pues para desplegar, primero tengo que añadir el add-on de Redis al Stack de esta aplicación en Heroku:

```prettyprint linenums

heroku addons:add redistogo:nano
-----> Adding redistogo:nano to fierce-autumn-4530... done, v11 (free)

```

Correcto, ahora basta con dar los pasos habituales:

```prettyprint linenums

git add .
git commit -m "añadido Redis para caché de lectura"
git push github master
git push heroku  master

```


Listo, con esto ya hago un heroku open y abro ticks.jsp, puedo ver que el comportamiento es exactamente igual que cuando ejecuto en local.

<strong>Código en GitHub</strong>
<a href="https://github.com/agustinventura/helloheroku/tree/b8c1b4a76276beae93be5d2f56ae28d78d94c78c"><img src="/images/2011/08/github_icon.png" alt="GitHub" title="GitHub" width="115" height="115" class="aligncenter size-full wp-image-255" /></a>

<strong>Conclusiones</strong>
Añadir add-ons a Heroku es trivial, en general consiste en bajar la librería que proporciona la api y listo (teniendo instalado el servicio en local, claro).
También es interesante que si escalo el proceso tick a un par de dynos, siguen impactando contra Redis, es decir, no levantan su propia instancia de Redis, realmente esta funcionando como una caché en RAM.
