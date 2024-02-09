---
title: Headers y Spring Boot HTTP Interface
date: 2024-02-09
tags:
  - Java
  - Spring Boot
  - HTTP Interface
  - REST
  - Headers
  - Authorization
  - Hexagonal Architecture
---
Siguiendo con la [serie](https://www.agustinventura.dev/posts/usando-spring-boot-http-interface/) de [clientes REST con Spring](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html), queda por cubrir un caso de uso muy frecuente, ¿cómo envío cabeceras?

Si comparamos las dos soluciones que hemos visto hasta ahora, cuando usábamos RestClient, si que enviábamos la cabecera Accept al hacer peticiones GET y cuando hacíamos la petición POST, enviamos también la cabecera Content-Type. Sin embargo al usar HTTP Interface, no lo hemos utilizado y hemos confiado en que enviamos y recibimos siempre JSON. Eso incluso nos dá cierto problema que ya hemos visto al tratar los errores en el HTTP Interface, siendo necesario eliminar el contenido del buffer de entrada si recibimos una respuesta errónea (como un 404), ya que ahí estaríamos recibiendo texto en vez de JSON y falla el parseador de JSON.

Para hacer un ejemplo algo más interesante, imaginemos que tenemos una API con parte pública (como todos los GET) y parte privada (como los POST), así que queremos hacer dos cosas:
1. Enviar en todas las peticiones la cabecera ACCEPT con JSON como el tipo aceptado.
2. Enviar en las peticiones POST únicamente la cabecera Authorization con un determinado Bearer token así como la cabecera Content-type.

Todo ésto usando HTTP Interface, claro, ya que con RestClient sería modificar los métodos oportunos.

## Enviando una cabecera en todas las peticiones
Esta precisamente puede ser la parte más sencilla, de la misma manera que al crear el RestClient que da soporte al HTTP Interface definimos un status handler por defecto, podemos asignar una cabecera a todas las peticiones:
```java
private static final String APPLICATION_JSON = MediaType.APPLICATION_JSON.getType() + "/" + MediaType.APPLICATION_JSON.getSubtype();

@Bean
public RestClient restClient(@Value("${song-server.base.url}") String baseUrl) {
  return RestClient.builder()
      .baseUrl(baseUrl)
      .defaultHeader(HttpHeaders.ACCEPT, APPLICATION_JSON)
      .defaultStatusHandler(
          HttpStatusCode::isError,
          (request, response) ->
              logger.error("Response error [code={}, body={}]", response.getStatusCode(), new String(response.getBody().readAllBytes()))
      )
      .build();
}
```
Listo, por defecto siempre vamos a enviar la cabecera ACCEPT con el tipo application/json (hace falta esa constante porque defaultHeader toma como parámetros dos String).

## Enviando cabeceras en las peticiones POST
Adjuntar cabeceras a las peticiones POST es muy sencillo (como vamos a ver ahora), sin embargo tiene su miga arquitecturalmente hablando. Vamos a empezar a la TDD por la solución más sencilla posible y analizaremos problemas y posibles errores.
Para enviar cabeceras con un único método, es tan sencillo como añadir un nuevo parámetro al método que hace el POST, anotándolo con [@RequestHeaders](https://docs.spring.io/spring-framework/reference/web/webflux/controller/ann-methods/requestheader.html):
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
  PlayListHistoryItem save(@RequestHeader Map<String, String> headers, @RequestBody PlayListHistoryItem item);
}
```
Esto hace que se nos rompa nuestro puerto de guardado, pero de momento lo podemos modificar rápidamente:
```java
public interface SaveLastPlayedPort {

  PlayListHistoryItem save (Map<String, String> headers, PlayListHistoryItem item);
}
```
Y ahora desde el sitio de uso del puerto, podemos pasar las cabeceras que queramos:
```java
@Bean
  ApplicationRunner appStarted(LoadLastPlayedPort loadLastPlayedPort, SaveLastPlayedPort saveLastPlayedPort,
      @Value("${song-server.api-key}") String apiKey) {
    return args -> {
      List<PlayListHistoryItem> lastPlayedSongs = loadLastPlayedPort.loadLastPlayedSongs();
      Optional<PlayListHistoryItem> notValidSong = loadLastPlayedPort.loadPlayedSong("foo");
      Optional<PlayListHistoryItem> playedSong = loadLastPlayedPort.loadPlayedSong(lastPlayedSongs.getFirst().id());
      PlayListHistoryItem newPlayedSong = PlayListHistoryItemBuilder.aPlayListHistoryItem().withId("SANsVA4ihQplEQIf0GZea3").withPlayedAt(
          LocalDateTime.now()).withTrack(playedSong.get().track()).build();
      saveLastPlayedPort.save(
          Map.of(HttpHeaders.CONTENT_TYPE, APPLICATION_JSON, HttpHeaders.AUTHORIZATION, "Bearer " + apiKey),
          newPlayedSong);
    };
  }
```
Aquí, para darle algo de realismo, inyectamos un api token y cuando invocamos al puerto para salvar la reproducción, le pasamos el content-type y el authorization.

Ahora si arrancamos con el log puesto a TRACE veremos algo así:
```
TRACE 4167793 --- [           main] o.s.w.s.i.RequestHeaderArgumentResolver  : Resolved request header value 'Content-Type:application/json'
TRACE 4167793 --- [           main] o.s.w.s.i.RequestHeaderArgumentResolver  : Resolved request header value 'Authorization:Bearer mytoken'
```
Pues ya estaría, ¿no? Un momento, ¿no dijimos arriba que había problemas arquitecturales? Efectivamente, aquí estamos introduciendo en nuestro SaveLastPlayedPort una dependencia con el mecanismo concreto de persistencia, el parámetro headers.
Visto de otra manera, nuestro puerto pertenece a la aplicación, expresa la funcionalidad de guardar una reproducción de una canción, sin importar dónde, podría ser una llamada REST como en este caso o insertar en una base de datos o guardar en un archivo. Si estuviéramos guardando en un archivo, ¿añadiríamos un parámetro con la ruta del archivo? Poder, podemos, pero introduce una fragilidad innecesaria además de emborronar los conceptos.

¿Qué podemos hacer entonces? La solución a un acoplamiento suele ser introducir otra capa de indirección. En este caso tenemos dos partes, un puerto que solo establece el contrato de como guardar las reproducciones y una interfaz que establece la comunicación REST, ¿qué necesitamos? Un adaptador que coordine como es esa comunicación.

Vale, ya sabemos que necesitamos introducir una nueva pieza de software, hacemos una lista de las cosas que queremos que haga este adaptador:
1. Para cargar todas las reproducciones, invocará el método loadLastPlayedSongs de SongsLocalRepository
2. Para cargar una canción en concreto, invocará el método loadLastPlayedSong de SongsLocalRepository
3. Para guardar una reproducción, invocará el método save de SongsLocalRepository, pasando las cabeceras oportunas.

Lo podríamos haber definido por comportamiento (es decir, para tal entrada quiero obtener tal salida), pero en este caso no queremos comprobar las entradas/salidas que al fin y al cabo ya sabemos cuales son sino las interacciones con el repositorio.

Podríamos escribir algo así:
```java
@Test
void givenNoIdShouldInvokeLoadLastPlayedSongs() {
  restSongsAdapter.loadLastPlayedSongs();

  verify(songsLocalRepository, times(1)).getAll();
}

@Test
void givenAnIdShouldInvokeLoadLastPlayedSong() {
  String songId = "testSongId";

  restSongsAdapter.loadPlayedSong(songId);

  verify(songsLocalRepository, times(1)).getWithId(songId);
}

@Test
void givenAPlaylistHistoryItemShouldInvokeSaveWithHeaders() {
  PlayListHistoryItem playedSong = PlayListHistoryItemsMother.getRecentlyPlayed();

  restSongsAdapter.save(playedSong);

  verify(songsLocalRepository, times(1)).post(headers, playedSong);
}
```
Esto nos permite hacer un par de cambios importantes, el primero es que nuestra interfaz SongsLocalRepository ya no tiene por qué extender los puertos, ahora la implementación de los puertos de salida es el adaptador, por lo que la interfaz quedaría así:
```java
public interface SongsLocalRepository {

@GetExchange("/items")
List<PlayListHistoryItem> getAll();

@GetExchange("/items/{id}")
Optional<PlayListHistoryItem> getWithId(@PathVariable String id);

@PostExchange("/items")
PlayListHistoryItem post(@RequestHeader Map<String, String> headers, @RequestBody PlayListHistoryItem item);
}
```
Hemos cambiado los nombres de los métodos para que estén más relacionados con HTTP y REST ya que ahora será el adaptador el que haga la conversión de conceptos de negocio a llamadas concretas. Creo que así la interfaz queda más expresiva.

La implementación concreta sería así:
```java
public class RestSongsAdapter implements LoadLastPlayedPort, SaveLastPlayedPort {

  private final Map<String, String> headers;

  private final SongsLocalRepository songsLocalRepository;

  public RestSongsAdapter(Map<String, String> headers, SongsLocalRepository songsLocalRepository) {
    this.headers = headers;
    this.songsLocalRepository = songsLocalRepository;
  }

  @Override
  public List<PlayListHistoryItem> loadLastPlayedSongs() {
    return songsLocalRepository.getAll();
  }

  @Override
  public Optional<PlayListHistoryItem> loadPlayedSong(String id) {
    return songsLocalRepository.getWithId(id);
  }

  @Override
  public PlayListHistoryItem save(PlayListHistoryItem item) {
    return songsLocalRepository.post(headers, item);
  }
}
```
Inyectamos las cabeceras que enviaremos y el repositorio e implementamos los métodos de los puertos llamando al repositorio. En este ejemplo es muy sencillo, pero este adaptador puede llegar a ser importantísimo ya que puede tener varias funciones:
1. Validar los parámetros que se enviarán al repositorio, como el item del post o el id para el get.
2. Mapear entre el modelo REST y nuestro modelo de negocio. Si tuviéramos un modelo rico con funcionalidad, este sería el punto en el que convertiríamos de los DTOs usados para comunicarnos con REST (y con anotaciones propias de Jackson, por ejemplo) a nuestro modelo de negocio.
3. Este mismo mapeo nos indica que es el punto de hacer operaciones más sofisticadas si las necesitamos, por ejemplo, nuestra entidad de dominio puede estar construida a partir de varios DTOs, incluso de DTOs con distintas tecnologías, como pueden ser provenientes de una base de datos y una API REST. Aquí es donde realizar las distintas llamadas para obtener/persistir. Esto también nos permite implementar lo que en términos de DDD se conoce como una [capa de anticorrupción](https://learn.microsoft.com/es-es/azure/architecture/patterns/anti-corruption-layer) para asegurar no solo que los datos que enviamos son correctos, si no que los que recibimos se ajustan a nuestras restricciones de dominio.

Con estos cambios, tendríamos que actualizar también la aplicación y la podríamos ejecutar:
```java
@SpringBootApplication
public class PlayListHistoryApplication {

  private static final Logger logger = LoggerFactory.getLogger(PlayListHistoryApplication.class);

  public static void main(String[] args) {
    SpringApplication.run(PlayListHistoryApplication.class, args);
  }

  private static final String APPLICATION_JSON = MediaType.APPLICATION_JSON.getType() + "/" + MediaType.APPLICATION_JSON.getSubtype();

  @Bean
  public RestClient restClient(@Value("${song-server.base.url}") String baseUrl) {
    return RestClient.builder()
        .baseUrl(baseUrl)
        .defaultHeader(HttpHeaders.ACCEPT, APPLICATION_JSON)
        .defaultStatusHandler(
            HttpStatusCode::isError,
            (request, response) ->
                logger.error("Response error [code={}, body={}]", response.getStatusCode(), new String(response.getBody().readAllBytes()))
        )
        .build();
  }

  @Bean
  public Map<String, String> headers(@Value("${song-server.api-key}") String apiKey) {
    return Map.of(
        HttpHeaders.CONTENT_TYPE, APPLICATION_JSON,
        HttpHeaders.AUTHORIZATION, "Bearer " + apiKey
    );
  }

  @Bean
  public SongsLocalRepository songsLocalRepository(RestClient restClient) {
    RestClientAdapter adapter = RestClientAdapter.create(restClient);
    HttpServiceProxyFactory factory = HttpServiceProxyFactory.builderFor(adapter).build();
    return factory.createClient(SongsLocalRepository.class);
  }

  @Bean
  public LoadLastPlayedPort loadLastPlayedPort(Map<String, String> headers, SongsLocalRepository songsLocalRepository) {
    return new RestSongsAdapter(headers, songsLocalRepository);
  }

  @Bean
  public SaveLastPlayedPort saveLastPlayedPort(Map<String, String> headers, SongsLocalRepository songsLocalRepository) {
    return new RestSongsAdapter(headers, songsLocalRepository);
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

Hemos pasado de tener un cliente REST y dos HTTP interface (necesarias por las dos implementaciones de los puertos) a tener un cliente REST, un HTTP interface y dos instancias del adaptador. También creamos el mapa con las cabeceras para inyectar en los adaptadores las cabeceras y es en ese mapa donde inyectamos nuestra API key.

De esta manera conseguimos aislar conceptos, nuestro dominio (representado por los puertos) no conoce nada de la tecnología subyacente (como eran las cabeceras que necesitábamos antes) y es el adaptador el que se encarga de unir (adaptar entre sí) los dos conceptos: nuestro modelo de dominio (en lo tocante a los puertos) y REST.

Sigues teniendo el código en [GitHub](https://github.com/agustinventura/playlisthistory)