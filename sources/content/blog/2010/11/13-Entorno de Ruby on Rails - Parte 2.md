title=Entorno de Ruby on Rails - Parte 2
date=2010-11-13
type=post
tags=Programación,Ruby on Rails
status=published
~~~~~~
Bazinga! Eso era, por fín:

```prettyprint linenums
case@aesir:~/.rvm/usr/lib$ gem update --system
Updating RubyGems
Nothing to update
```

Se vuelve a ejecutar el rvm --create y el --default y seguimos adelante, ahora a instalar rails con gem.

```prettyprint linenums
gem install rails --version 3.0.1
```

Muy bien, creo el directorio de proyecto y

```prettyprint linenums
rails new fist_app
```

Ya está creada, repaso los directorios y algún fichero de configuración según el tutorial e instalo los gems con bundle tal y como se especifica.

```prettyprint linenums
rails server
```

Y ahí esta, funcionando sin problemas. Pasamos a recapitular.

<ul>
	<li>Efectivamente, las herramientas son útiles y potentes, parece que se está pensando en todo.</li>
	<li>La estructura de directorios parece también clara y estándar.</li>
	<li>El uso de git y el incluir una carpeta tests por defecto, parece que sigue metodologías modernas, o mejor dicho, te guía al uso de las mismas.</li>
	<li>El que haya una y solo una herramienta para cada cosa, no tienes que aprender a hacer lo mismo de 4 formas distintas.</li>
</ul>

Y poco más, de momento ya esta bien, mañana más y mejor.

Vamos a descogelar sushi pa la cena.