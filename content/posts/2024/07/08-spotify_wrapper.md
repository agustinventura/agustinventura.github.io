---
title: Spotify Wrapper
date: 2024-07-08
tags:
  - Java
  - Spring Boot
  - Docker
  - Spotify
  - SpotifyWrapper
draft: true
---
Muchas veces quiero probar o explicar ideas y conceptos de programación nuevos y termino usando ejemplos bastante malos, sin ir más lejos [este sobre Configuration Properties](https://www.agustinventura.dev/posts/configuration-properties-con-spring-boot/) o [este sobre RestClient](https://www.agustinventura.dev/posts/secretos-en-desarrollo-local-con-spring-boot/), todos juegan alrededor del uso de una API de canciones y almacenar canciones pero creo que queda bastante diluido y hace que se pierda el hilo y no se vea exactamente a dónde quiero ir a parar.
Así que a finales del año pasado se me ocurrió una idea, ¿por qué no hago un proyecto de ejemplo que pueda utilizar para explicar cosas y hacer pruebas en un proyecto "real"? Hay mucha gente que sigue más o menos esta línea, por ejemplo, [Vlad Mihalcea](https://vladmihalcea.com/blog/) lleva años (11) usando el ejemplo de un foro/blog con Posts y Comments para dar ejemplos en sus artículos de persistencia en Java o mi compi Iván tiene una charla muy interesante sobre [Spring Boot y Testcontainers](https://youtu.be/829OAcP9uBs?si=klInBgQNRGtjm1ts) en la que desarrolla un posible ejemplo real. Vale, pues como decía en Diciembre del año pasado recibí el habitual [Spotify Wrapped](https://newsroom.spotify.com/2023-wrapped/) y, sinceramente, los resultados no me cuadraban (sobre todo los artistas más reproducidos y tal), así que se me ocurrió... ¿puedo crear mi propio Spotify Wrapped usando la [API de Spotify](https://developer.spotify.com/documentation/web-api) y la respuesta parece ser que es que sí :)

## La API de Spotify
Antes de ponerme a programar como un loco, hay que ver si hay soporte para lo que quiero hacer. Mi idea es ir accediendo a mi historial de canciones reproducidas, tener un artefacto software que dada la fecha de la última vez que se consultó la API se traiga todas las canciones reproducidas desde entonces, algo así:
![SongServerConfigurationProperties](/images/2024/07/08/01-spotify-importer.png)

Vamos leyendo las canciones y las vamos volcando en la cola.
¿Por qué en la cola? Pues porque me interesa trabajar un poco con Kafka y darle algo de complejidad al caso, poder añadir después distintos elementos a la cadena de procesamiento que enriquezcan, etc...
Vale, ahora queda preguntarse si podemos implementar esta funcionalidad con la API de Spotify y [resulta que sí](https://developer.spotify.com/documentation/web-api/reference/get-recently-played), podemos cconsultar todas las canciones reproducidas desde una determinada fecha.

El único problema que plantea la API de Spotify es más bien técnico, esta securizada usando OAuth y la gestión de tokens de autorización, refresco, etc... resulta más bien tediosa. Mientras que la exploración que he hecho tiene que ver con la complejidad esencial del problema (si puedo acceder a las canciones reproducidas desde una determinada fecha), esto es un ejemplo de complejidad accidental, yo quiero usar la API pero para eso tengo que realizar unas gestiones que no estan relacionadas con mi negocio en sí. Ahora hay dos opciones:
- Realizar la implementación del acceso a esta operación y por tanto la gestión completa de OAuth con un [cliente de bajo nivel](https://www.agustinventura.dev/posts/usando-spring-boot-http-interface/)
- Usar alguna librería que me permita acceder a la API de Spotify, es decir, que ya haya hecho este trabajo por mí... [Como esta](https://github.com/spotify-web-api-java/spotify-web-api-java), que tiene una pinta excelente, es un proyecto antiguo, pero bien mantenido, con un buen número de estrellas y forks...

Así que decidido, la idea es viable y hay una librería que nos facilita el acceso a la API. Voy a montar la infraestructura.

## Docker
