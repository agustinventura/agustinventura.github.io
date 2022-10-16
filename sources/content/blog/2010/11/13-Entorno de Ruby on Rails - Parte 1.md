title=Entorno de Ruby on Rails - Parte 1
date=2010-11-13
type=post
tags=Ruby on Rails
status=published
~~~~~~
Para seguir el tutorial voy a usar mi viejo buen portátil (tiene ya 6 años), con una Ubuntu 10.04 y el siguiente stack de desarrollo (siguiendo lo recomendado en el tutorial):

<ul>
	<li>Editor: gVim (y las extensiones de ruby de vim)</li>
	<li>Control de versiones: git (apt-get install git-core)</li>
	<li>Ruby versión 1.8.7</li>
</ul>

Y hasta aquí todo bien, no deja de ser todo apt-get install, ahora el tutorial recomienda instalar <a title="Ruby Version Management" href="http://rvm.beginrescueend.com/" target="_blank">RVM (Ruby Version Management)</a>, un gestor de versiones de Ruby. El tema me suena, haciendo un símil con Java, yo puedo estar desarrollando con Java 1.6 pero querer compilar con Java 1.5 (por cuestión de compatibilidad o cualquier motivo), al parecer Ruby tiene una herramienta que gestiona este tipo de cosas... la verdad, tiene buena pinta, vamos a ver.

La instalación es con git (primera toma de contacto):

```prettyprint linenums
bash &lt; &lt;( curl http://rvm.beginrescueend.com/releases/rvm-install-head )
```

se ejecuta sin problemas y sale un bonito texto dando información varia. Básicamente y según la sección "Postinstall" de la misma página de rvm, hay que añadir una línea al final del .bashrc:

```prettyprint linenums
[[ -s "$HOME/.rvm/scripts/rvm" ]] &amp;&amp; . "$HOME/.rvm/scripts/rvm"  # This loads RVM into a shell session
```

Se comprueba si esta funcionando con:

```prettyprint linenums
type rvm | head -n1
```

Salida, correcta, así que seguimos y nos volvemos al tutorial donde dicen como usar RVM una vez instalado.

Básicamente, según estoy entendiendo, Ruby se distribuye en Gems, que son programas autosuficientes con sus librerías, etc... y con RVM vamos a instalar varios perfiles de ejecución incluyendo sus Gems y vamos a definir uno por defecto.

Asi que nada:

```prettyprint linenums
rvm install 1.8.7 #instala Ruby 1.8.7
rvm install 1.9.2 #instala Ruby 1.9.2
#etiquetamos lo perfiles
rvm --create 1.8.7@rails2
rvm --create 1.9.2@rails3
#usamos rails3 por defecto
rvm --default use 1.9.2@rails3
```

Por cierto, la compilación de la versiones de Ruby... tarda. O será que mi portátil esta ya bien viejuno.

Una vez hechas todas estas operaciones, me llevo la grata sorpresa de que de propina tenemos instalado RubyGems, un gestor de paquetes de Ruby, para probarlo:

```prettyprint linenums
which gem
```

Trato de actualizar tal y como dice el manual:

```prettyprint linenums
gem update --system
```

Y... ¡ZAS!¡En toda la boca!

```prettyprint linenums
no such file to load -- zlib
```

Y por fín se pone interesante la cosa, veo un post específico para la configuración: <a title="Ruby on Rails 3 and Ubuntu" href="http://toranbillups.com/blog/archive/2010/09/01/How-to-install-Rails-3.0-and-Ruby-1.9.2-on-Ubuntu" target="_blank">How to install Rails 3.0 and Ruby 1.9.2 on Ubuntu</a>, aunque me salto los dos primeros pasos, ya tengo instalado RVM y Ruby 1.8.7... sigo intentando pero nada de nada, sigue diciendo que no hay zlib... vaya. En <a title="Stackoverflow: Ruby and Zlib" href="http://stackoverflow.com/questions/2441248/rvm-ruby-1-9-1-troubles" target="_blank">Stackoverflow</a> leo esto:

<blockquote>rvm package install zlib
rvm remove 1.9.1
rvm install 1.9.1 -C --with-zlib-dir=$rvm_path/usr</blockquote>

Y en la <a title="RVM y zlib" href="http://rvm.beginrescueend.com/packages/zlib/" target="_blank">referencia de RVM</a> esto:

```prettyprint linenums
$ rvm package install zlib
$ rvm remove 1.9.2
$ rvm install 1.9.2
```

Esto parece más razonable... buf, otra vez a compilar... vamos a por un café que siempre viene bien.