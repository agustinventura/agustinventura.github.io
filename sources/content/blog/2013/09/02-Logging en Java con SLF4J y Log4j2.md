title=Logging en Java con SLF4J y Log4j2
date=2013-09-02
type=post
tags=Java,Programación,Tools of the Trade,log4j,logging,slf4j,tutorial
status=published
~~~~~~
En este artículo se hace una breve introducción a la generación de logs en Java usando SLF4J y Log4j2, así como un breve repaso de las mejores prácticas relativas.

<h5>Introducción</h5>

En Java se da una circunstancia muy extraña, siendo el logging tan importante como es, no hay una buena solución integrada en el framework como tal. Es cierto que existe la <a title="Java Logging Framework en Wikipedia" href="http://en.wikipedia.org/wiki/Java_logging_framework" target="_blank">Java Logging API o Java Logging Framework</a>, pero fue una adición bastante a posteriori (en concreto, se añadió en el 2002, en la versión 1.4 del JDK). Para cuando esta API salió como parte del JDK ya teníamos un "estándar" de facto, <a title="Log4j 1.2" href="http://logging.apache.org/log4j/1.2/" target="_blank">Log4j</a>, que fue creado en el 1999. Mientras tanto, y haciendo honor a aquella vieja <a title="XKCD - Standards" href="http://xkcd.com/927/" target="_blank">tira de XKCD</a>, seguían saliendo frameworks de loggings: <a title="Logback" href="http://logback.qos.ch/" target="_blank">logback</a>, <a title="commons-logging" href="http://commons.apache.org/proper/commons-logging/" target="_blank">commons-logging</a>, <a title="SLF4J" href="http://www.slf4j.org/" target="_blank">slf4j</a> y otros tipos de soluciones a cada cual más exótica. En <a title="The Logging Mess" href="http://techblog.bozho.net/?p=503" target="_blank">este artículo</a> se hace un repaso bastante completo de la historia del desaguisado.
A verano de 2013, la  situación no ha mejorado, tal y como recoge una reciente <a title="State of Logging in Java 2013" href="http://zeroturnaround.com/rebellabs/the-state-of-logging-in-java-2013/" target="_blank">encuesta de ZeroTurnAround</a>. Si acaso se clarifican dos tendencias:

<ol>
	<li>En general, se suele usar una fachada de abstracción sobre el sistema de logs como puede ser SLF4J o commons-logging. Entiendo que ésto es debido a que muchas organizaciones imponen el uso de un framework de logging en concreto y mediante esta indirección ganas flexibilidad.</li>
	<li>Log4J sigue siendo 14 años después el framework de logging más usado. Si eso no es un estándar de facto...</li>
</ol>

Por tanto, parece razonable aplicar la filosofía de fachada de logging + framework de logging para el desarrollo de un nuevo producto. En cuanto a fachada de logging se usará SLF4J y como framework de logging se explicará el uso de Log4j2. ¿Por qué el 2 y no el 1? Pues básicamente por velocidad. El logging es una actividad que realmente es accesoria, por tanto no debería consumir recursos del sistema apenas, la página de Log4j2 explica que esta es una de las motivaciones tras la versión 2 del framework, y <a title="Log4j2 Performance close to insane" href="http://www.grobmeier.de/log4j-2-performance-close-to-insane-20072013.html#.UiMaLt9wB2N" target="_blank">este artículo</a> confirma su velocidad. Sin embargo hay que tener en cuenta que Log4j2 esta actualmente en beta 8, pero dado que vamos a usar SLF4J se puede sustituir por su versión 1 o por logback o como se desee.
Otro aspecto a considerar a la hora de usar la versión 2 de log4j es que cuando se usa Maven, el log4j 1.2.x incluye varias dependencias que lo más normal es que no se usen, como javax.mail, geronimo-jms, etc...

<h5>Configuración</h5>

La configuración en un proyecto con Maven es tan sencilla como añadir las siguientes dependencias al pom.xml:

```prettyprint linenums

<!-- slf4j -->
<dependency>
	<groupId>org.slf4j</groupId>
	<artifactId>slf4j-api</artifactId>
	<version>1.7.5</version>
</dependency>
<!-- log4j2 -->
<dependency>
	<groupId>org.apache.logging.log4j</groupId>
	<artifactId>log4j-api</artifactId>
	<version>2.0-beta8</version>
</dependency>
<dependency>
	<groupId>org.apache.logging.log4j</groupId>
	<artifactId>log4j-core</artifactId>
	<version>2.0-beta8</version>
</dependency>
<dependency>
	<groupId>org.apache.logging.log4j</groupId>
	<artifactId>log4j-slf4j-impl</artifactId>
	<version>2.0-beta8</version>
</dependency>

```

La primera dependencia es la api de SLF4J, que realmente es la que se utilizará en la aplicación para escribir los mensajes de log. A continuación esta la API y el Core de Log4j2 y por último el puente entre SLF4J y Log4j2. Ya que SLF4J es una fachada de logging, el proyecto incluye varios puentes para trabajar con los frameworks más comunes, sin embargo, como Log4j2 es un proyecto nuevo, es éste el que incluye el puente para SLF4J.

<h5>Uso</h5>

El uso de SLF4J es bastante sencillo, basta con instanciar el objeto de logging, el logger:

```prettyprint linenums
private static Logger logger = LoggerFactory.getLogger(Logging.class);
```

Esta variable es privada para evitar que otras clases puedan usarla, porque en ese caso parecería que el error se ha producido en nuestra clase Logging, además es static para que tan solo haya una instancia del logger sin importar las instancias que haya de la clase (es decir, es singleton). Se puede usar también una instancia normal, cada aproximación tiene sus pros y sus contras como se discute <a title="Static vs. Instance loggers" href="http://www.slf4j.org/faq.html#declared_static">aquí</a>.
En cuanto al uso del logger es muy sencillo:

```prettyprint linenums
public static void main (String... args) {
	logger.info("Starting application");
	logger.debug("Loading Lannister house");
	House lannister = new House("Lannister");
	logger.debug("Invoking Clegane bannerman");
	lannister.invokeBannerMan("Clegane");
	logger.debug("Invoking erroneous bannerman");
	lannister.invokeBannerMan(null);
	logger.info("Ended application");
}
```

En este ejemplo, se crea una Casa llamada Lannister y se invoca a dos banderizos, uno llamado Clegane y otroal que por error se pasa null como nombre.
El resultado de ejecutar este programa es el siguiente:

```prettyprint linenums
14:21:23.629 [main] ERROR es.aguasnegras.logging.model.House - Error loading house Lannister bannerman: bannerman name can't be empty
Exception in thread "main" java.lang.IllegalStateException: Cant invoke bannerman without name
	at es.aguasnegras.logging.model.House.invokeBannerMan(House.java:44)
	at es.aguasnegras.logging.Logging.main(Logging.java:20)
```

La ejecución de la aplicación falla al invocar el banderizo con null (normal)
Como se ve la invocación al logger es en todo caso la misma, variando solo según el nivel de importancia del mensaje de error. En total en SLF4J vienen definidos los siguientes niveles de log:

<ol>
	<li> Error: Ocurrió un error en la aplicación.</li>
	<li>Warn: Se ha dado una circunstancia de posible error.</li>
	<li>Info: Información sobre la ejecución de la aplicación.</li>
	<li>Debug: Información importante para debuggear la aplicación.</li>
	<li>Trace: Información de traza sobre la ejecución de la aplicación.</li>
</ol>

En otros frameworks existe un nivel adicional de log: Fatal, pero SLF4J no lo recoge, he <a title="SLF4J y nivel de log Fatal" href="http://www.slf4j.org/faq.html#fatal">aquí</a> la explicación. Yo personalmente creo que puedo vivir sin ello.
El objeto de cualquier framework de logging es que podamos configurar fácilmente cuales de estos mensajes se mostrarán según el entorno. Lo más normal es que en desarrollo deseemos mostrar los mensajes de debug y superiores, mientras que en producción se establezca el nivel a info (o incluso a error). Ahora bien, si hay un error en producción, lo más interesante es ajustar directamente el nivel de log a trace y así dispondríamos de toda la información relevante.
Sin embargo, en el ejemplo pese a tener invocaciones a debug, a info y a trace, tan solo sale el mensaje relativo al error (que además se registra en la clase House). Esto es porque aún no hemos definido la configuración de los mensajes de log y por defecto log4j2 tan solo recoge los mensajes con nivel Error.

<h5>Configuración de Log4j2</h5>

En primer lugar, hay que decir que la configuración de log4j2 se realiza bien mediante un archivo xml, bien mediante un archivo json. En log4j 1.2 se podía configurar también mediante un archivo .properties, como a mí nunca me gustó esa opción (la veía confusa), agradezco que la hayan quitado.
Lo primero es crear en main/resources un fichero log4j2.xml (tal y como se explica <a title="Configuración de Log4j2" href="http://logging.apache.org/log4j/2.x/manual/configuration.html#AutomaticConfiguration">aquí</a>), una vez creado, se completa tal que así:

```prettyprint linenums

<?xml version="1.0" encoding="UTF-8"?>
<configuration status="WARN">
  <appenders>
    <Console name="Console" target="SYSTEM_OUT">
      <PatternLayout pattern="%d{HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/>
    </Console>
  </appenders>
  <loggers>
    <root level="trace">
      <appender-ref ref="Console"/>
    </root>
  </loggers>
</configuration>

```

El archivo empieza con el elemento <em>configuration</em> que tiene un atributo <em>status</em>, ese atributo significa el nivel de log de error que quiero aplicar al mismo log4j, a warn esta bien.
A continuación defino un <em>appender</em>. Se puede pensar un appender es un destino de los mensajes de log, se puede tener un appender para presentar por consola, otro para guardar en archivo, otro para enviar por email o combinación de todos los anteriores. <a title="Appenders de Log4j2" href="http://logging.apache.org/log4j/2.x/manual/layouts.html">Aquí</a> se pueden consultar todos los appenders que hay.
A su vez un appender tiene un <em>layout</em> que no es más que la forma de darle formato al mensaje de log: bien siguiendo un patrón, bien en html, etc... de nuevo hay una extensa <a title="Appenders de Log4j2" href="http://logging.apache.org/log4j/2.x/manual/layouts.html">lista</a>.
Y por último estan los <em>logger</em> como tal. Los loggers tienen una particularidad, y es que existe un logger "padre" del que heredan todos los existentes: root, después de él se podrán crear los que sean oportunos, pero al menos siempre existirá root. Un logger tiene un nivel (que es el nivel mínimo de log cuyos mensajes se mostrarán) y una lista de appenders que se utilizarán para mostrar los mensajes.
De momento solo tengo configurado root y con nivel <em>trace</em> con lo que se mostrarán todos los mensajes que se generen. Tal que así:

```prettyprint linenums

17:02:03.721 [main] INFO  es.aguasnegras.logging.Logging - Starting application
17:02:03.723 [main] DEBUG es.aguasnegras.logging.Logging - Loading Lannister house
17:02:03.742 [main] TRACE es.aguasnegras.logging.model.House - Loaded house Lannister without bannermen
17:02:03.742 [main] DEBUG es.aguasnegras.logging.Logging - Invoking Clegane bannerman
17:02:03.763 [main] TRACE es.aguasnegras.logging.model.BannerMan - Loaded bannerman Clegane with house Lannister
17:02:03.763 [main] TRACE es.aguasnegras.logging.model.House - Adding bannerman Clegane to house Lannister
17:02:03.763 [main] DEBUG es.aguasnegras.logging.Logging - Invoking erroneous bannerman
17:02:03.763 [main] ERROR es.aguasnegras.logging.model.House - Error loading house Lannister bannerman: bannerman name can't be empty
Exception in thread "main" java.lang.IllegalStateException: Cant invoke bannerman without name
	at es.aguasnegras.logging.model.House.invokeBannerMan(House.java:44)
	at es.aguasnegras.logging.Logging.main(Logging.java:20)

```

Y ahora se puede empezar a modificar la configuración. Por ejemplo, si quiero que aparezcan todos los mensajes de error para Logging pero para las demás clases que solo aparezcan de info para arriba, puedo añadir este logger a la configuración:

```prettyprint linenums

<loggers>
	<root level="trace">
		<appender-ref ref="Console" />
	</root>
	<logger name="es.aguasnegras.logging.model" level="info" additivity="false">
		<appender-ref ref="Console" />
	</logger>
</loggers>

```

Estoy creando un logger nuevo para el paquete <em>es.aguasnegras.logging.model</em> que recogerá todos los mensajes de información y los mostrará por el appender <em>Console</em>. El atributo <em>additivity</em> a false indica que los mensajes que se muestren por este logger no se deberán mostrar por root (si no, saldrían duplicados).
Es importante tener en cuenta que el nivel de log de root es el mínimo para todo el sistema. Es decir, si yo arriba cambio el nivel de root por <em>error</em> y el de model por <em>trace</em> tan solo se mostrarán los mensajes de error, ya que el resto no se evaluarán.
Si por ejemplo ahora quisiera que si se mostraran todos los mensajes de log de la clase BannerMan, podría hacer así:

```prettyprint linenums

<root level="trace">
	<appender-ref ref="Console" />
</root>
<logger name="es.aguasnegras.logging.model" level="info" additivity="false">
	<appender-ref ref="Console" />
</logger>
<logger name="es.aguasnegras.logging.model.BannerMan" level="trace" additivity="false">
	<appender-ref ref="Console" />
</logger>

```

Y así, sucesivamente. Aquí, por mantener el ejemplo sencillo, solo he utilizado un appender, pero cada logger podría usar un appender distinto, por ejemplo, root podría utilizar la consola, pero model podría usar un archivo.

<h5>Uso Eficiente de la API</h5>

Arriba comentaba que un framework de logging, sobre todo ha de ser rápido y no consumir ciclos de CPU, ni memoria, etc... En general, para evitar el consumo "tonto" de recursos en muchos sitios recomiendan hacer lo siguiente:

```prettyprint linenums

if (logger.isTraceEnabled()) {
	logger.trace("Adding bannerman " + bannerManName + " to house " + name);
}

```

Este código, desde mi punto de vista tiene varios inconvenientes:

<ol>
<li>En el caso mejor (trace no esta habilitado), se ejecuta una instrucción</li>
<li>En el caso peor (trace esta habilitado), se ejecutan dos instrucciones y además se construye la cadena con el mensaje</li>
<li>Además, para cumplir con DRY, nos veremos tentados de crear una fachada de logging sobre la fachada de logging (WTF!)</li>
</ol>

Para evitar todo esto, en SLF4J <a title="Forma más rápida de logar" href="http://www.slf4j.org/faq.html#logging_performance">recomiendan esta forma de logar</a>:

```prettyprint linenums

logger.trace("Adding bannerman {} to house {}", bannerManName, name);

```

Así de sencillo y de fácil. Por supuesto el método acepta múltiples parámetros y si se pasa un objeto se invoca el toString.

<h5>Código</h5>


Pues con esto se acaba este pequeño repaso de lo fundamental sobre SLF4J y Log4j2, el código, en github (para variar).

<a href="https://github.com/agustinventura/logging"><img title="Ejemplos de Logging en GitHub" src="/images/github_icon.png" alt="JustPlay en GitHub" width="115" height="115" /></a>
