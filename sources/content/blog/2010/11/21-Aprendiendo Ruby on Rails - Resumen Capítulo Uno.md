title=Aprendiendo Ruby on Rails - Resumen Capítulo Uno
date=2010-11-21
type=post
tags=Programación,Ruby on Rails
status=published
~~~~~~
Bueno, pues en el capítulo uno del tutorial he configurado el entorno y seguido un pequeño workflow de trabajo, desde la creación de la aplicación hasta su despliegue en Heroku, pasando por el control de versiones con Git y GitHub.

El único inconveniente que le veo es que... efectivamente, no he aprendido nada de Ruby ni de Rails.

Ahora pequeña lista de cosas que me gustan:

<ul>
	<li>Ecosistema de herramientas bien acoplado y funcional (espectacular la comunicación Heroku - GitHub)</li>
	<li>Generador de código automático (¿<a title="Spring Roo" href="http://www.springsource.org/roo" target="_blank">Spring Roo</a>?)</li>
	<li>El tutorial te hace seguir buenas prácticas y con herramientas modernas.</li>
	<li>El entorno de desarrollo es UNIX!</li>
	<li>No es necesario un IDE mamotrético, al menos de momento.</li>
</ul>

Cosas que no me han gustado:

<ul>
	<li>Todavía no he visto nada de código como tal, jeje.</li>
	<li>Pequeños problemas en la instalación.</li>
	<li>Algunos conceptos se dan demasiado rápido, habría que verlos más pausadamente (ver lista más abajo).</li>
</ul>

Ahora voy a resumir los pasos de instalación en la Ubuntu 10.04:

<ol>
	<li>Paquetes apt-get: gVim, Git, ruby, curl, <del datetime="2010-11-24T16:11:06+00:00">libruby1.8</del>, zlib1g-dev, libssl-dev, libreadline5-dev, build-essential, rubygems, <del datetime="2010-11-24T16:11:06+00:00">irb</del>, ri, <del datetime="2010-11-24T16:11:06+00:00">rdoc</del>, rake, ruby1.8-dev, libopenssl-ruby, sqlite3, libsqlite3-dev, <del datetime="2010-11-24T16:11:06+00:00">sqlite3-ruby</del>libsqlite3-ruby</li>
	<li>RVM: Con Git, seguir instrucciones en su página.</li>
	<li>Instalación de Ruby 1.9.2 en RVM con zlib leer <a title="Ruby 1.9.2 y Zlib" href="http://rvm.beginrescueend.com/packages/zlib/" target="_blank">aquí</a></li>
	<li>Instalación de Rails 3 en sí, <a href="http://www.aguasnegras.es/wp/?p=15" target="_blank">aquí</a></li>
	<li>También es más que conveniente una cuenta de usuario de GitHub y otra de Heroku.</li>
</ol>

Y listo. Conceptos que me gustaría repasar:

<ul>
	<li>Lenguaje Ruby como tal.</li>
	<li>Gems</li>
	<li>Rake</li>
	<li>RVM</li>
	<li>Rails</li>
	<li>Git</li>
	<li>Heroku</li>
	<li>Markdown</li>
</ul>

Y "ya esta", claro, hay que tener en cuenta que Ruby y Rails es el objetivo fundamental, así que eso espero tenerlo bastante cubierto de aquí a terminar.

Hmmm... una cosa que me llama la atención ahora que lo pienso, ¿no hay ningún framework de pruebas unitarias? Interesante, a ver si el tutorial dice algo.