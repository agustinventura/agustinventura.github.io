---
title: Usando Spring Boot HTTP Interface
date: 2024-02-02
tags:
  - Java
  - Spring Boot
  - HTTP Interface
  - REST
---
Este artículo es una continuación del [anterior](https://www.agustinventura.dev/posts/usando-spring-boot-restclient), en el que usábamos RestClient para acceder a una API REST. Si no lo has leído, repásalo porque vamos a usar la misma API de reproducción de canciones para nuestro ejemplo.

Como resumen rápido, en el artículo anterior teníamos esta API de canciones que hemos reproducido recientemente y usábamos el nuevo RestClient para acceder a ella y hacer algunas operaciones básicas, como traerlas todas, buscar una por su id o crear una nueva reproducción. 

Hasta aquí, todo bien, ¿cuál es el problema? Pues que en realidad, para hacer una operación relativamente sencilla, tenemos mucho código, ¿no? Si repasamos el código final del repositorio:
```java
public class SongsLocalRepository implements LoadLastPlayedPort, SaveLastPlayedPort {

  private static final String LAST_PLAYED_SONGS_COLLECTION = "/items";

  private final RestClient restClient;

  public SongsLocalRepository(RestClient restClient) {
    this.restClient = restClient;
  }

  @Override
  public List<PlayListHistoryItem> loadLastPlayedSongs() {
    return restClient
        .get()
        .uri(LAST_PLAYED_SONGS_COLLECTION)
        .accept(MediaType.APPLICATION_JSON)
        .retrieve()
        .body(new ParameterizedTypeReference<List<PlayListHistoryItem>>() {});
  }

  @Override
  public Optional<PlayListHistoryItem> loadPlayedSong(String id) {
    try {
      PlayListHistoryItem playedSong = restClient
          .get()
          .uri(LAST_PLAYED_SONGS_COLLECTION + "/{id}", id)
          .accept(MediaType.APPLICATION_JSON)
          .retrieve()
          .onStatus(HttpStatusCode::is4xxClientError, (request, response) -> {
            throw new IllegalArgumentException();
          })
          .body(PlayListHistoryItem.class);
        return Optional.ofNullable(playedSong);
    } catch (IllegalArgumentException iae) {
      return Optional.empty();
    }
  }

  @Override
  public PlayListHistoryItem save(PlayListHistoryItem item) {
    if (item == null) {
      throw new IllegalArgumentException("Stored song can't be null");
    }
    return restClient
        .post()
        .uri(LAST_PLAYED_SONGS_COLLECTION)
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .body(item)
        .retrieve()
        .body(PlayListHistoryItem.class);
  }
}
```
Vemos que el uso que hacemos es bastante similar en todos los casos, cambiando alguna particularidad como el tratamiento de errores en el load o la doble llamada a body en el caso del save. 

Cabe preguntar entonces, ¿no hay una manera más sencilla de implementar ésto? Pues sí y existe de hace años, [Feign](https://github.com/OpenFeign/feign). Básicamente, Feign nos permite definir una interfaz que contendrá nuestros puntos de llamada HTTP y en tiempo de ejecución inyectar la implementación que hará estas llamadas, esto no solo tiene la ventaja de simplificar el código sino que además nos permite poder cambiar fácilmente el cliente que usamos. 

En nuestro ejemplo, con Spring, podríamos cambiar de RestTemplate a RestClient sin tocar otro punto que la construcción del cliente de Feign. Además de ésto Feign tiene muchas más funcionalidades, pero si queremos solamente un uso básico, aquí vienen las buenas noticias... desde Spring 6 no necesitamos añadir Feign si no que podemos utilizar [HTTP Interfaces](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html#rest-http-interface).

## Usando HTTP Interface
Como dice el nombre, usar HTTP Interface es tan sencillo como crear una interfaz y añadirle unas anotaciones (como las que usamos en [Spring MVC](https://spring.io/guides/tutorials/rest/) para definir los resources), vamos a migrar nuestro repositorio a esta interfaz:
```java
public interface SongsLocalRepository extends LoadLastPlayedPort, SaveLastPlayedPort {

  @Override
  @GetExchange("/items")
  List<PlayListHistoryItem> loadLastPlayedSongs();

  @Override
  @GetExchange("/items/{id}")
  Optional<PlayListHistoryItem> loadPlayedSong(@PathVariable String id);

  @Override
  @PostExchange("/items")
  PlayListHistoryItem save(@RequestBody PlayListHistoryItem item);
}
```
Y listo, con apenas 11 líneas tenemos lo mismo que teníamos antes, pero es que además, al estar utilizando un componente propio de Spring, nos podemos evitar las pruebas unitarias (es más, no podemos hacer pruebas unitarias porque realmente no tenemos implementación). Si podría tener sentido en un contexto más amplio tener pruebas de integración, pero en nuestra prueba no es necesario.

Como podemos ver, todas las anotaciones son muy parecidas a las que usaríamos si estuviéramos haciendo un servidor con Spring MVC y no un cliente. En concreto el uso de @PathVariable (o @RequestParam) y @RequestBody son exactamente iguales.

Como último paso, tenemos que proveer el cliente concreto, esto lo hacemos en la clase de la aplicación, donde creamos los beans de Spring oportunos:
```java
@SpringBootApplication
public class PlayListHistoryApplication {

  private static final Logger logger = LoggerFactory.getLogger(PlayListHistoryApplication.class);

  public static void main(String[] args) {
    SpringApplication.run(PlayListHistoryApplication.class, args);
  }

  @Bean
  public RestClient restClient(@Value("${song-server.base.url}") String baseUrl) {
    return RestClient.builder()
        .baseUrl(baseUrl)
        .defaultStatusHandler(
            HttpStatusCode::isError,
            (request, response) ->
              logger.error("Response error [code={}, body={}]", response.getStatusCode(), new String(response.getBody().readAllBytes()))
            )
        .build();
  }

  @Bean
  public LoadLastPlayedPort loadLastPlayedPort(RestClient restClient) {
    RestClientAdapter adapter = RestClientAdapter.create(restClient);
    HttpServiceProxyFactory factory = HttpServiceProxyFactory.builderFor(adapter).build();
    return factory.createClient(SongsLocalRepository.class);
  }

  @Bean
  public SaveLastPlayedPort saveLastPlayedPort(RestClient restClient) {
    RestClientAdapter adapter = RestClientAdapter.create(restClient);
    HttpServiceProxyFactory factory = HttpServiceProxyFactory.builderFor(adapter).build();
    return factory.createClient(SongsLocalRepository.class);
  }

  @Bean
  ApplicationRunner appStarted(LoadLastPlayedPort loadLastPlayedPort, SaveLastPlayedPort saveLastPlayedPort) {
    return args -> {
      List<PlayListHistoryItem> lastPlayedSongs = loadLastPlayedPort.loadLastPlayedSongs();
      Optional<PlayListHistoryItem> notValidSong = loadLastPlayedPort.loadPlayedSong("foo");
      Optional<PlayListHistoryItem> playedSong = loadLastPlayedPort.loadPlayedSong(lastPlayedSongs.getFirst().id());
      PlayListHistoryItem newPlayedSong = PlayListHistoryItemBuilder.aPlayListHistoryItem().withId("SANsVA4ihQplEQIf0GZea3").withPlayedAt(
          LocalDateTime.now()).withTrack(playedSong.get().track()).build();
      saveLastPlayedPort.save(newPlayedSong);
    };
  }
}
```

Aquí si tenemos algo más de complicación. Para crear los puertos ya no instanciamos directamente el repositorio (no podemos, ya que es una interfaz), sino que utilizando un adaptador para nuestro RestClient (podríamos estar usando también [WebClient o RestTemplate](https://github.com/spring-projects/spring-framework/wiki/What%27s-New-in-Spring-Framework-6.x)) y una factoría devolvemos el cliente.

La configuración de RestClient si es más interesante. Ahora podemos hacer un tratamiento de errores genérico, en vez de tenerlo que hacer en todos los métoodos que lo usan. Por ejemplo, aquí se ha optado simplemente por logar el error en la consola y seguir ejecutando, pero tendría sentido dividirlo en dos:
1. Si es un error de cliente, devolver Optional.empty
2. Si es un error de servidor, lanzar una excepción propia

Esto lo podemos conseguir si en el defaultStatusHandler utilizamos is4xxClientError y is5xxServerError, pero para el ejemplo nos quedamos con ésto. 

**Importante**: Si queremos que devuelva correctamente Optional.empty en caso de un 404, tenemos que invocar necesariamente response.getBody().readAllBytes(), ya que esto consume el contenido del response, dejándolo vacío. Si no hacemos ésto, tratará de mapear el contenido de response a un objeto (PlayListHistoryItem en este caso), pero el contenido será de tipo text/plain en vez de JSON y fallará.

Como en el anterior, tienes el código en [GitHub](https://github.com/agustinventura/playlisthistory)