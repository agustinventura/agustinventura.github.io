---
title: Despliegue en Heroku
date: 2010-11-21
tags:
  - Programación
  - Ruby on Rails
---
Por último y para acabar con el ciclo de vida, voy a ver el despliegue en <a href="http://heroku.com/">Heroku</a>.
Primero te das de alta y te envían un mail de confirmación, con este email vas a una página en la que pones la contraseña y listo.
Ahora hay que instalar el gem de Heroku

```shell

gem install heroku

```

Una vez hecho esto, añado también mi clave pública a Heroku para poder comunicarlo con Git (increible esto... vaya ecosistema, me tiene alucinando).

```shell

heroku keys:add

```

Le suministro la información de la cuenta de Heroku y lo hace todo solo.
Por último, creo la aplicación:

```shell

heroku create

```

Con esto ya esta hecho, basta con pasar la aplicación de Git a Heroku (flipo).

```shell

git push heroku master

```

Y se acabó, si se desea se puede lanzar la aplicación desde la misma línea de comandos

```shell

heroku open

```


A volar... la verdad que de momento me gusta lo que veo, unas herramientas bien coordinadas para hacerle la vida más sencilla al desarrollador con un ecosistema amigable. Me gusta.