---
title: Configuration Properties con Spring Boot
date: 2024-02-22
tags:
  - Java
  - Spring Boot
  - ConfigurationProperties
---
En [artículos anteriores](https://www.agustinventura.dev/posts/secretos-en-desarrollo-local-con-spring-boot/) usábamos propiedades de configuración para pasar distintos parámetros a nuestra aplicación, haciendo algo de memoria, teníamos un secrets.properties en src/main/resources (junto con application.properties) con este contenido:
```
song-server.base.url=http://localhost:3000
song-server.api-key=mytoken
```
Y lo importábamos en application.properties:
```
spring.config.import=secrets.properties
spring.main.web-application-type=none
logging.level.org.springframework.web=TRACE
```
Eso nos permitía usar esas propiedades (las que empiezan por song-server) en nuestra aplicación, por ejemplo, a través de la anotación @value:
```
@Bean
public Map<String, String> headers(@Value("${song-server.api-key}") String apiKey) {
  return Map.of(
      HttpHeaders.CONTENT_TYPE, APPLICATION_JSON,
      HttpHeaders.AUTHORIZATION, "Bearer " + apiKey
  );
}
```
Esto es muy cómodo y ya [hemos visto](https://www.agustinventura.dev/posts/secretos-en-desarrollo-local-con-spring-boot/#como-utilizar-distintos-secretos-seg%c3%ban-el-entorno) que nos permite incluso sobreescribir el valor pasándolo como variable de entorno. Además, @Value nos permite especificar valores por defecto y otra serie de funciones avanzadas que son muy útiles.

El problema que podemos tener por tanto, no depende de la funcionalidad en sí, sino del uso que hagamos de la misma, en concreto, este uso puede dar lugar a tener nuestro código trufado de anotaciones @Value en multitud de sitios, con el incordio que resulta para el mantenimiento de la aplicación. Lo idóneo sería tener una especie de diccionario central donde tengamos concentradas todas nuestras propiedades.

Pues esto, como no, existe y se llama [ConfigurationProperties](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config.typesafe-configuration-properties) y por supuesto, tiene [ventajas adicionales](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config.typesafe-configuration-properties.vs-value-annotation).

## Usando ConfigurationProperties para centralizar nuestra configuración
Vamos a seguir con el ejemplo y vamos a centralizar todas las propiedades de song-server en un record que se llamará SongServerConfigurationProperties y sería tal que así:
```java
@ConfigurationProperties(prefix = "song-server")
public record SongServerConfigurationProperties (String baseUrl, String apiKey) {

}
```
Esto significa que va a leer todas las propiedades que empiecen por song-server y las va a cargar en las variables definidas. Spring automáticamente interpola los nombres (esto se llama [relaxed binding](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config.typesafe-configuration-properties.relaxed-binding)) y las asigna, es decir, va a leer tanto song-server.baseUrl como song-server.base-url, le sirve cualquiera de estas definiciones.

Una vez creado este record, hay que habilitarlo mediante la anotación @EnableConfigurationProperties justo donde tenemos nuestra anotación @SpringBootApplication (o cualquier otra clase anotada con @Configuration) y podemos quitar las anotaciones @Value:
```java
@SpringBootApplication
@EnableConfigurationProperties(SongServerConfigurationProperties.class)
public class PlayListHistoryApplication {

  ...

  @Bean
  public RestClient restClient(SongServerConfigurationProperties songServerConfigurationProperties) {
    return RestClient.builder()
        .baseUrl(songServerConfigurationProperties.baseUrl())
        .defaultHeader(HttpHeaders.ACCEPT, APPLICATION_JSON)
        .defaultStatusHandler(
            HttpStatusCode::isError,
            (request, response) ->
                logger.error("Response error [code={}, body={}]", response.getStatusCode(), new String(response.getBody().readAllBytes()))
        )
        .build();
  }

  @Bean
  public Map<String, String> headers(SongServerConfigurationProperties songServerConfigurationProperties) {
    return Map.of(
        HttpHeaders.CONTENT_TYPE, APPLICATION_JSON,
        HttpHeaders.AUTHORIZATION, "Bearer " + songServerConfigurationProperties.baseUrl()
    );
  }
  ...
}
```
Y podemos probar a arrancar para obtener un error feísimo y sin sentido:
```
java.lang.IllegalArgumentException: URI with undefined scheme
```
¿Qué está pasando aquí? Que el error sea relativo a la URI nos indica que es algo relacionado con el bean restClient, ¿por qué se queja de la URI? Precisamente hemos modificado la construcción de ese bean para eliminar @Value y usar nuestro record de configuración. Si ponemos un breakpoint y observamos nuestro record, podemos ver el error.
![SongServerConfigurationProperties](/images/2024/02/22/01-configuration-properties.png)
Podemos ver que apiKey tiene valor, pero baseUrl esta a null, lo cual termina produciendo el error que vemos ya que no puede crear una URI con null como baseUrl, pero, ¿por qué pasa esto? Si miramos nuestro secrets.properties, podemos ver que mientras que la propiedad apiKey esta definida en [kebab case](https://en.wikipedia.org/wiki/Letter_case#Kebab_case), baseUrl esta definido separado por un . (es decir, base.url). Esto hace que Spring no pueda reconocer la propiedad porque el . se utiliza para separar jerárquicamente las propiedades, es decir, si quisiéramos, podríamos tener otro ConfigurationProperties con prefix "song-server.base" y ahí si definiríamos la propiedad url y la leería. Como tampoco es lo que queremos sino que es un error, lo cambiamos en secrets.properties:
```
song-server.base-url=http://localhost:3000
song-server.api-key=mytoken
```
Si volvemos a lanzar la aplicación, magia, funciona, sin haber tenido que tocar ninguna anotación @Value ni hacer ningún tipo de modificación (y en caso de hacerla hubiera sido solo en nuestro record).

¿Qué os parece? El código, ya sabéis, en [GitHub](https://github.com/agustinventura/playlisthistory).