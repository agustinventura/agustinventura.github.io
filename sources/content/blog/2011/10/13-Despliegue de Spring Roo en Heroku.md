title=Despliegue de Spring Roo en Heroku
date=2011-10-13
type=post
tags=Heroku,Java,PostgreSQL,Programación,Spring Roo,Tools of the Trade,tutorial
status=published
~~~~~~
Hasta ahora, las aplicaciones que he desplegado eran muy básicas, hechas con jsp y acceso a base de datos a base de jdbc plano.

Estas tecnologías no estan mal (y de hecho son la base de todo lo posterior), pero lo más normal es utilizar frameworks para el desarrollo de aplicaciones Java.

La quinta práctica del libro de Java para Heroku es un despliegue de aplicaciones hechas con <a title="Spring Roo" href="http://www.springsource.org/roo" target="_blank">Spring Roo</a> en Heroku. Spring Roo es un framework que viene a ser como Rails para Ruby. Simplifica el desarrollo con funciones tan básicas como crear el toString o el equals automáticamente o tan avanzadas como generar el CRUD de una base de datos directamente.

Así que con esta práctica voy a matar dos pájaros de un tiro, voy a probar Spring Roo y voy a desplegar un artefacto más complejo en Heroku. A ello.

<strong>Instalación de Spring Roo</strong>

Lo primero es descargar el framework de <a title="Descarga de Spring Roo en SpringSource" href="http://www.springsource.com/download/community" target="_blank">aquí</a>. Después sigo las <a title="Instalación de Spring Roo" href="http://static.springsource.org/spring-roo/reference/html/intro.html#intro-installation" target="_blank">instrucciones de instalación</a>:

<ol>
	<li>Descomprimir el archivo, en mi caso en $HOME/Java/spring-roo-1.1.5.RELEASE</li>
	<li>Crear enlace simbólico: sudo ln -s /home/case/Java/spring-roo-1.1.5.RELEASE/bin/roo.sh /usr/bin/roo</li>
	<li>Probar que funciona:</li>
</ol>


```prettyprint linenums
cd Java/spring-roo-1.1.5.RELEASE/
mkdir roo-test
roo quit
```

Si todo ha ido bien, debe haber salido Roo así en <a title="ASCII Art en la Wikipedia" href="http://en.wikipedia.org/wiki/ASCII_art" target="_blank">ASCII art</a> monísimo. Ya esta instalado Spring Roo y puedo borrar roo-test, hala a retomar el tema.

<strong>Quinta Práctica</strong>

El objetivo de esta práctica es más bien sencillo, se va a usar Spring Roo para crear un ejemplo clásico, el Pet Clinic y se va a preparar esta aplicación creada con Roo para desplegar en Heroku.

Pasos:

<ol>
	<li>Crear la aplicación con Roo.</li>
	<li>Preparar el pom.xml añadiendo las dependencias adecuadas y la configuración correcta para su despliegue en Heroku.</li>
	<li>Crear una clase que arranque Jetty (el servidor integrado).</li>
	<li>Configurar la base de datos PostgreSQL en la aplicación.</li>
	<li>Probar la aplicación en local.</li>
	<li>Desplegar en Heroku.</li>
</ol>

<strong>Paso 1</strong>

Crear la aplicación es más bien sencillo:

```prettyprint linenums
cd Heroku
mkdir petclinic
cd petclinic
roo script --file clinic.roo
```

Me escupe un montón de logs por la consola y en teoría, listo. Examinando un poco la aplicación, pues nada, es una aplicación Java que sigue la estructura de Maven, con su pom.xml y nada, todo perfecto, sus entidades, sus controladores... su páginas web, tiene pinta de estar hecho con Spring MVC... vale, al lío.

<strong>Paso 2</strong>

En este paso, lo primero es añadir Jetty y PostgreSQL al pom.xml:

```prettyprint linenums

<dependency>
		<groupId>org.eclipse.jetty</groupId>
		<artifactId>jetty-webapp</artifactId>
		<version>7.4.4.v20110707</version>
	</dependency>
	<dependency>
		<groupId>org.mortbay.jetty</groupId>
		<artifactId>jsp-2.1-glassfish</artifactId>
		<version>2.1.v20100127</version>
	</dependency>
	<dependency>
		<groupId>postgresql</groupId>
		<artifactId>postgresql</artifactId>
		<version>9.0-801.jdbc4</version>
	</dependency>

```

Ahora cambio el scope de servlet-api de provided a compile. Si se usa Tomcat, Tomcat incluye la librería servlet.jar (la API de Servlet), pero Jetty no, así que hay que descargarla. Hay que cambiar igual el scope de org.springframework.roo.annotations, si la ejecuto en local con Roo, estará la librería de anotaciones de Roo, pero claro, en Heroku no esta.

Siguiente paso, añadir el plugin appassembler para que genere el script con el que arrancar la aplicación:

```prettyprint linenums


<plugin>
			<groupId>org.codehaus.mojo</groupId>
			<artifactId>appassembler-maven-plugin</artifactId>
			<version>1.1.1</version>
			<executions>
				<execution>

<phase>package</phase>
					<goals><goal>assemble</goal></goals>
					<configuration>
						<assembleDirectory>target</assembleDirectory>
						<extraJvmArguments>-Xmx512m</extraJvmArguments>

<programs>

<program>
								<mainClass>com.springsource.petclinic.PetclinicMain</mainClass>
								<name>webapp</name>
							</program>
						</programs>
					</configuration>
				</execution>
			</executions>
		</plugin>

```

Y por último, hay que quitar la línea de packaging para que genere un jar en vez de un war, listo.

<strong>Paso 3</strong>

Ahora hay que crear la clase Main.java en src/main/java, exactamente igual que la que puse en la primera práctica, tampoco tiene más historia.

<strong>Paso 4</strong>

Para configurar la aplicación para que use PostgreSQL hay que tocar el applicationContext.xml, que es el archivo de configuración de Spring. Se encuentra en src/main/resources/META-INF/spring. Aquí, hay que cambiar las propiedades username, password y url por tan solo url de la siguiente manera:

Que es el parseo para la cadena de conexión a PostgreSQL que ya ví. En el applicationContext.xml veo que el driver de conexión a la base de datos está parametrizado, así que tengo que cambiarlo, en el mismo directorio esta un archivo database.properties en el que esta la propiedad que me interesa, database.driverClassName, lo dejo así:

```prettyprint linenums
database.driverClassName=org.postgresql.Driver
```

Por último, en el persistence.xml (que esta en src/main/resources/META-INF), hay que cambiar el valor del hibernate.dialect, a org.hibernate.dialect.PostgreSQLDialect.

<strong>Paso 5</strong>

Todo listo, ahora toca probar en local:

```prettyprint linenums
export REPO=~/.m2/repository/
export DATABASE_URL=postgres://helloheroku:helloheroku@localhost/helloheroku
mvn install
sh target/bin/webapp
```

Listo, entro en http://localhost:8080 y ahí esta el PetClinic con Spring Roo y contra PostgreSQL. Genial

<strong>Paso 6</strong>

Para el despliegue de la aplicación en Heroku, primero hay que crear el Procfile con la definición de la actividad web:

gedit Procfile

Y añado:


```prettyprint linenums

web:sh target/bin/webapp

```

Lo añado todo a un repositorio de git, creo el entorno de Heroku, lo subo todo a Heroku y GitHub y abro la aplicación:


```prettyprint linenums

git init

git add pom.xml Procfile src/

heroku create --stack cedar

git push github master

git push heroku master

heroku open


```


Y listo, funcionando!

<strong>Código en GitHub</strong>

<strong><a href="https://github.com/agustinventura/Petclinic-con-Spring-Roo-en-Heroku"><img class="aligncenter size-full wp-image-255" title="GitHub" src="/images/2011/08/github_icon.png" alt="GitHub" width="115" height="115" /></a>
</strong>

<strong>Conclusiones</strong>

Este ejemplo es, de lejos, el más interesante, ya que demuestra tres cosas:

<ol>
	<li>Que Heroku parece ser capaz de trabajar sin problemas con los frameworks mayoritarios de Java.</li>
	<li>Que realmente, los frameworks de Java son tremendamente potentes si se sabe como usarlos, aportando una gran flexibilidad.</li>
	<li>Y por último, creo que mi primera impresión estaba justificada. Tenemos un entorno capaz de acercar el mundo Java EE a la mayoría de desarrolladores... con todo lo que ello implica. Ahora es cosa nuestra aprovecharlo o no.</li>
</ol>

Y con esto, he terminado con Heroku de momento, me sigue quedando pendiente clarificar el tema de dynos, bds, etc... A ver si me pongo...
