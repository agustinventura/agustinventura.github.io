title=Spring Boot y AngularJS
date=2017-05-07
type=post
tags=Java, Spring Boot, JavaScript, Angular
status=draft
~~~~~~
Con [Spring Boot](https://start.spring.io/) es relativamente sencillo generar un backend para una aplicación por complejo que sea su dominio, precisamente lo bueno de Spring Boot es que permite realizar rápidamente todo el trabajo de infraestructura para centrarse por una parte en el código del dominio y por otra... en la UI.
En los últimos años hemos pasado de un paradigma de desarrollo en servidor a uno nuevo cliente/servidor (otra vez). El servidor suele ser una API [REST ] (https://en.wikipedia.org/wiki/Representational_state_transfer) mientras que los clientes son típicamente aplicaciones Android, iOS y Web (lo cual incluye otros servicios REST y con eso emergen los microservicios...). En materia de clientes web, el ganador en toda la historia ha sido JavaScript y básicamente, dentro de JavaScript hay dos grandes frameworks:
	
1. [React] (https://facebook.github.io/react/): Abanderado por Facebook, realmente es una librería de componentes ricos para el cliente.
2. [Angular] (https://angular.io/): La opción de Google. Antes era conocido como AngularJS pero al alcanzar la versión 2 lo reescribieron completamente y le cambiaron el nombre. Viene a ser un framework MVC completo para el cliente.

Después de llevar un tiempo observando el desarrollo, creo que voy a tirar por Angular, ya que me parece más completo, en general por lo que veo, React requiere más código para conectar todas las partes, mientras que Angular es más rígido pero más completo.
Recientemente, me he encontrado con un tutorial de [Matt Raible] (https://twitter.com/mraible?lang=es) en el que desarrolla justo este ejemplo, un backend rápido y sencillo con Spring Boot y un frontend con Angular, el tutorial esta [aquí] (http://developer.okta.com/blog/2017/04/26/bootiful-development-with-spring-boot-and-angular).

##### Creación del backend
La parte de creación del backend es bastante sencilla la única diferencia es que he ordenado algo más el código (por mera manía). Dos cosas que me llaman la atención:

1. La anotación @GetMapping. No tenía ni idea de que existieran estos atajos.
2. El uso de Spring Data REST. Esta muy bien (pero que muy bien) para el objeto del tutorial, desarrollar una aplicación rápido. Sin embargo creo que publicar los repositorios como recursos REST, si bien puede resultar cómodo, es un antipatrón, estamos mezclando dos cosas bien distintas, el acceso a datos y la representación de los datos. Eso por no hablar de que directamente se exponen las entidades del modelo de negocio en vez de usar DTOs. En resumen, que el proyecto es MUY útil para realizar pruebas pero no lo veo apto para producción.

Aparte de ésto, poco más que resaltar.

##### Creación del frontend

###### Instalación de Angular
El primer paso es instalar [node.js] (https://nodejs.org/en/download/) cosa que yo hice por apt. El siguiente es instalar [npm] (https://www.npmjs.com/), también a tiro de apt. Y ahora sigo instalando el [CLI de Angular] (https://github.com/angular/angular-cli#installation):
```prettyprint
npm install -g @angular/cli
```
En mi caso, y al haber instalado mediante apt, falla ya que no hay permisos de escritura en el directorio de instalación, por lo que toca hacer sudo:
```prettyprint
sudo npm install -g @angular/cli
```
Y ahí ya si lo instala y lo confirmo con:
```prettyprint
ng --version
```

 

