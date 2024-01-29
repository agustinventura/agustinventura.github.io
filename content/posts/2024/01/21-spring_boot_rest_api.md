---
title: Usando Spring Boot RestClient y HTTP Interface
date: 2024-01-27
tags:
  - Java
  - Spring Boot
  - RestClient
  - REST
  - Microservicio
---
El consumo de una API REST es un caso muy habitual cuando trabajamos en una arquitectura de microservicios, y es casi que la opción por defecto para el tráfico entre los distintos microservicios (aunque si es por eficiencia, deberíamos usarlo solo para tráfico norte-sur y optar por otras opciones más eficientes como [gRPC](https://grpc.io/) para el tráfico este-oeste).
Normalmente, en el mundo de Spring usamos por defecto dos opciones:
1. Si estamos usando el stack bloqueante (web) [RestTemplate](https://spring.io/guides/gs/consuming-rest/).
2. Si usamos el stack reactivo (webflux) [WebClient](https://spring.io/guides/gs/reactive-rest-service/).

Los años de RestTemplate (13) se notan si hemos usado WebClient, ya que tiene una [API](https://docs.spring.io/spring-framework/reference/web/webflux-webclient.html) mucho más concisa y fluida, más elegante. La contraprestación es que está diseñado para trabajar con Spring WebFlux y por tanto usa los tipos de datos reactivos Flux y Mono, por lo que si tu aplicación sigue un modelo bloqueante, vas a trufar todos los usos de WebClient con bloqueos para obtener los resultados y conversiones de Mono a tipos concretos o de Flux a colecciones. 

Sin embargo, ninguna de las dos opciones es la más moderna a la hora de trabajar con APIs REST. En Spring 6.0 y Spring 6.1 se han introducido nuevos clientes que podemos utilizar.
Si estamos usando el stack bloqueante, podemos usar desde Spring 6.1 el nuevo [RestClient](https://spring.io/blog/2023/07/13/new-in-spring-6-1-restclient), que no es más que la API de WebClient sobre RestTemplate, por lo que tenemos todas las ventajas de esta API sin los inconvenientes derivados del stack reactivo que comentábamos arriba.

Pero además, desde Spring 6 podemos usar una [interfaz HTTP](https://docs.spring.io/spring-framework/reference/web/webflux-http-interface-client.html) tanto sobre RestTemplate, RestClient y WebClient que nos permite anotar interfaces con métodos @HttpExchange y derivar en Spring toda la gestión del cliente concreto. Para entendernos, haríamos algo parecido a lo que hacemos cuando definimos un RestController pero para un cliente.

En este artículo vamos a ver como usar RestClient y en uno posterior veremos como podemos cambiar el código para usar el HTTP Interface.
## La API
Vamos a montar una API de ejemplo que nos va a permitir acceder y guardar las últimas canciones que hemos reproducido en nuestro cliente multimedia favorito:
```json
{
    "items": [
        {
            "id": "RBnhX0DJw5HGmYIwjriPMu",
	    "track": {
                "album": {
                    "id": "6tKQyT3LHSMOsObqfk264N",
                    "name": "Femme Fatale"
                },
                "artists": [
                    {
                        "id": "2wJ4vsxWd7df7dRU4KcoDe",
                        "name": "Sharon Van Etten"
                    }
                ],
                "id": "2HDycU1sqxlfYQloriXcK1",
                "name": "Femme Fatale"
            },
            "played_at": "2024-01-23T13:07:21.657Z"
        },
        {
	    "id": "LS0vdfbKzKwWFXhlS3SsDu",
            "track": {
                "album": {
                    "id": "3QoFSi0dH7mXm3ajgX51Si",
                    "name": "Cosy Karaoke, Vol. 1"
                },
                "artists": [
                    {
                        "id": "0Ak6DLKHtpR6TEEnmcorKA",
                        "name": "The Vaccines"
                    }
                ],
                "id": "6JOlPrtFaVK7TYmtgi93GC",
                "name": "No One Knows"
            },
            "played_at": "2024-01-23T12:59:45.307Z"
        }
    ]
}
```
Podemos montar un servidor local con [JSON Server](https://github.com/typicode/json-server) siguiendo tres pasos:
1. Instalamos JSON Server
2. Creamos un archivo db.json
3. Copiamos los items en este archivo
4. Arrancamos JSON Server

Y con esto, en http://localhost:3000/items tendríamos la API CRUD completa de nuestras canciones.

## El Proyecto de Ejemplo
Vamos a ir a Spring Initializr (o usar el wizard de IntelliJ) y vamos a crear un proyecto con los siguientes datos:
![Spring Initializr](/images/2024/01/21/01-spring-initializr.png)
Solo añado la dependencia web porque es donde se encuentra el RestClient.
Si seguimos un diseño de [arquitectura hexagonal](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)), la raíz de nuestro agregado es PlayListHistoryItem, ya que en un principio queremos traer simplemente las últimas canciones reproducidas. El dominio completo lo podemos representar mediante una serie de records ya que no tiene comportamiento (es una mala práctica, siendo un [modelo de dominio anémico](https://martinfowler.com/bliki/AnemicDomainModel.html), pero para el ejemplo sirve).
```java
public record PlayListHistoryItem(String id, Track track, @JsonProperty("played_at") LocalDateTime playedAt) {}

public record Track(String id, String name, Album album, Set<Artist> artists) {}

public record Album(String id, String name) {}

public record Artist(String id, String name) {}
```
Otra mala práctica aquí es que hemos metido la anotación JsonProperty en un objeto de dominio. Todo ésto nos indica claramente que estamos creando DTOs y que nuestro modelo de dominio debería ser otro. Pero de nuevo lo hacemos así para mantener el ejemplo contenido.

El comportamiento de carga de estas canciones desde un sistema externo al sistema lo definimos en un puerto secundario (o de salida):
```java
public interface LoadLastPlayedPort {

  List<PlayListHistoryItem> loadLastPlayedSongs();
}
```
Y la responsabilidad de conectar concretamente con nuestro servidor local la podemos implementar en una clase SpongRepository que implementa el LoadLastPlayedPort:
```java
public class SongsLocalRepository implements LoadLastPlayedPort {

  @Override
  public List<PlayListHistoryItem> loadLastPlayedSongs() {
    return List.of();
  }
}
```
## Usando RestClient
Ahora hay que modelar SongsLocalRepository que será donde usemos el RestClient, siguiendo un enfoque [TDD](https://en.wikipedia.org/wiki/Test-driven_development) podemos escribir esta lista de comportamiento que deseamos del repositorio:
- Si no hay canciones reproducidas recientemente, devolverá una lista vacía. ¿Por qué una lista? Pues porque tendremos duplicados (al menos de la canción, ya que puedo reproducir varias veces la misma) y además el orden es importante (viene dado cronológicamente). También se podría optar para este caso por un SortedSet.
- Si hay canciones, las devolverá en una lista ordenadas por orden de reproducción, es decir, decrecientemente de lastPlayedAt.
Nuestra clase de tests será algo así:
```java
class SongsLocalRepositoryTest {

  private SongsLocalRepository songsLocalRepository;

  @BeforeEach
  void setUp() {
    songsLocalRepository = new SongsLocalRepository();
  }

  @Test
  void givenNoLastPlayedSongsShouldReturnEmptyList() {
    List<PlayListHistoryItem> lastPlayedSongs = songsLocalRepository.loadLastPlayedSongs();

    assertThat(lastPlayedSongs).isEmpty();
  }

  @Test
  void givenMoreThanOneLastPlayedSongShouldReturnSongsInDecreasingLastPlayedAtOrder() {
    List<PlayListHistoryItem> lastPlayedSongs = songsLocalRepository.loadLastPlayedSongs();

    assertThat(lastPlayedSongs).isNotEmpty();
    assertThat(lastPlayedSongs.getFirst().playedAt()).isAfter(lastPlayedSongs.getLast().playedAt());
  }
}
```
La nomenclatura no es muy consistente porque quiero obtener las canciones, pero claro, realmente lo que obtengo son PlayListHistoryItems, pero bueno... con esto, por fín podemos ir a una primera implementación:
```java
public class SongsLocalRepository implements LoadLastPlayedPort {

  @Override
  public List<PlayListHistoryItem> loadLastPlayedSongs() {
    RestClient restClient = RestClient.builder()
        .baseUrl("http://localhost:3000")
        .build();
    return restClient
        .get()
        .uri("/items")
        .accept(MediaType.APPLICATION_JSON)
        .retrieve()
        .body(new ParameterizedTypeReference<List<PlayListHistoryItem>>() {});
  }
}
```
Vale, aquí hacemos dos cosas (lo cual ya nos indica que [estamos haciendo algo mal](https://en.wikipedia.org/wiki/Single_responsibility_principle)):
1. Crear el RestClient como tal que es tan sencillo como indicarle la URL base de nuestras peticiones (con lo cual la relación RestClient a URL es 1:1, es decir, si quiero atacar otra URL, necesitaré otro cliente).
2. Hacer la petición como tal.

Entrando al detalle de la petición podemos ver que es bastante autodescriptiva:
1. Indicamos que vamos a hacer una petición GET
2. Decimos contra que URI vamos a ir, que se concatenará a la baseUrl del builder
3. Añadimos la cabecera que indica el tipo de contenido que aceptamos como respuesta
4. Hacemos la invocación en sí con retrieve
5. Convertimos el contenido de body al tipo de respuesta (el ParameterizedTypeReference es la manera que tenemos de evitar el [borrado de tipos en genéricos](https://en.wikipedia.org/wiki/Type_erasure))

Si arrancamos nuestro JSON Server y lanzamos las pruebas, nos encontramos con que pasa la que espera dos canciones, pero falla la que no espera ninguna. Esto es así porque lo que estamos haciendo es una prueba de integración y no unitaria, cuando debiera ser así. Para que sea una prueba unitaria, tenemos que aislar nuestro código creando un sustituto para RestClient, podemos por ejemplo, mockearlo y nuestras pruebas quedarían así:
```java
class SongsLocalRepositoryTest {

  private SongsLocalRepository songsLocalRepository;

  @BeforeEach
  void setUp() {
    songsLocalRepository = new SongsLocalRepository();
  }

  @Test
  void givenNoLastPlayedSongsShouldReturnEmptyList() {
    List<PlayListHistoryItem> playListHistoryItems = PlayListHistoryItemsMother.getEmptyRecentlyPlayed();
    RestClient restClient = mockRestClient(playListHistoryItems);
    RestClient.Builder restClientBuilder = mock(RestClient.Builder.class);
    try (MockedStatic<RestClient> mockedBuilder = mockStatic(RestClient.class)) {
      mockRestClientBuilder(mockedBuilder, restClientBuilder, restClient);

      List<PlayListHistoryItem> lastPlayedSongs = songsLocalRepository.loadLastPlayedSongs();

      assertThat(lastPlayedSongs).isEmpty();
    }
  }

  @Test
  void givenMoreThanOneLastPlayedSongShouldReturnSongsInDecreasingLastPlayedAtOrder() {
    List<PlayListHistoryItem> playListHistoryItems = PlayListHistoryItemsMother.getTwoRecentlyPlayed();
    RestClient restClient = mockRestClient(playListHistoryItems);
    RestClient.Builder restClientBuilder = mock(RestClient.Builder.class);
    try (MockedStatic<RestClient> mockedBuilder = mockStatic(RestClient.class)) {
      mockRestClientBuilder(mockedBuilder, restClientBuilder, restClient);

      List<PlayListHistoryItem> lastPlayedSongs = songsLocalRepository.loadLastPlayedSongs();

      assertThat(lastPlayedSongs).isNotEmpty();
      assertThat(lastPlayedSongs.getFirst().playedAt()).isAfter(lastPlayedSongs.getLast().playedAt());
    }
  }

  private RestClient mockRestClient(List<PlayListHistoryItem> items) {
    RestClient restClient = mock(RestClient.class);
    RequestHeadersUriSpec getRequest = mock(RequestHeadersUriSpec.class);
    ResponseSpec response = mock(ResponseSpec.class);
    when(restClient.get()).thenReturn(getRequest);
    when(getRequest.uri(anyString())).thenReturn(getRequest);
    when(getRequest.accept(any())).thenReturn(getRequest);
    when(getRequest.retrieve()).thenReturn(response);
    when(response.body(any(ParameterizedTypeReference.class))).thenReturn(items);
    return restClient;
  }

  private void mockRestClientBuilder(MockedStatic<RestClient> mockedBuilder, Builder restClientBuilder, RestClient restClient) {
    mockedBuilder.when(RestClient::builder).thenReturn(restClientBuilder);
    when(restClientBuilder.build()).thenReturn(restClient);
    when(restClientBuilder.baseUrl(anyString())).thenReturn(restClientBuilder);
    when(restClientBuilder.defaultHeader(anyString(), anyString())).thenReturn(restClientBuilder);
  }
}
```
El código es bastante feo: el motivo es que tenemos que mockear la llamada estática al builder de RestClient y no tenemos más remedio que usar el MockedStatic.
Lo que hacemos es utilizar un Object Mother para crear en el primer test una lista vacía y en el segundo una lista con dos elementos y que cuando se invoca al retrieve() se devuelva la lista oportuna, todo este follón es para eso, sin más.

Ahora hay una refactorización que es obvia, RestClient debería estar inyectado en nuestro repositorio (la responsabilidad del repositorio no es crear RestClient, sino usarlo para acceder a los recursos):
```java
public class SongsLocalRepository implements LoadLastPlayedPort {

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
}
```
Esto nos permite evitar la llamada estática al builder de RestClient y por tanto dejar las pruebas más concisas:
```java
class SongsLocalRepositoryTest {

  private RestClient restClient;
  private SongsLocalRepository songsLocalRepository;

  @BeforeEach
  void setUp() {
    restClient = mock(RestClient.class);
    songsLocalRepository = new SongsLocalRepository(restClient);
  }

  @Test
  void givenNoLastPlayedSongsShouldReturnEmptyList() {
    List<PlayListHistoryItem> playListHistoryItems = PlayListHistoryItemsMother.getEmptyRecentlyPlayed();
    setUpMockGetAllRequest(playListHistoryItems);

    List<PlayListHistoryItem> lastPlayedSongs = songsLocalRepository.loadLastPlayedSongs();

    assertThat(lastPlayedSongs).isEmpty();
  }

  @Test
  void givenMoreThanOneLastPlayedSongShouldReturnSongsInDecreasingLastPlayedAtOrder() {
    List<PlayListHistoryItem> playListHistoryItems = PlayListHistoryItemsMother.getTwoRecentlyPlayed();
    setUpMockGetAllRequest(playListHistoryItems);

    List<PlayListHistoryItem> lastPlayedSongs = songsLocalRepository.loadLastPlayedSongs();

    assertThat(lastPlayedSongs).isNotEmpty();
    assertThat(lastPlayedSongs.getFirst().playedAt()).isAfter(lastPlayedSongs.getLast().playedAt());
  }

  private void setUpMockRestClient(List<PlayListHistoryItem> items) {
    RequestHeadersUriSpec getRequest = mock(RequestHeadersUriSpec.class);
    ResponseSpec response = mock(ResponseSpec.class);
    when(restClient.get()).thenReturn(getRequest);
    when(getRequest.uri(anyString())).thenReturn(getRequest);
    when(getRequest.accept(any())).thenReturn(getRequest);
    when(getRequest.retrieve()).thenReturn(response);
    when(response.body(any(ParameterizedTypeReference.class))).thenReturn(items);
  }
}
```
Para cargar una canción por su id, tenemos unos pasos muy similares. Podemos especificarlo así:
```java
@Test
void givenNonExistingPlayedSongShouldReturnEmpty() {
  Optional<PlayListHistoryItem> playedSong = songsLocalRepository.loadPlayedSong("foo");

  assertThat(playedSong).isNotPresent();
}

@Test
void givenAnExistingPlayedSongShouldReturnIt() {
  PlayListHistoryItem playListHistoryItem = PlayListHistoryItemsMother.getPlayListHistoryItem();
  Optional<PlayListHistoryItem> playedSong = songsLocalRepository.loadPlayedSong(playListHistoryItem.id());

  assertThat(playedSong).isPresent();
  assertThat(playedSong.get()).isEqualTo(playListHistoryItem);
}
```
Modificamos el puerto de lectura para añadir el método que nos permite cargar una reproducción por su id:
```java
public interface LoadLastPlayedPort {

  List<PlayListHistoryItem> loadLastPlayedSongs();
  
  PlayListHistoryItem loadPlayListHistoryItem();
}
```
E implementamos de manera parecida a la anterior:
```java
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
```
Esto es más interesante porque dejando de lado la sobrecarga del método uri() que nos permite pasar un path param de manera limpia, podemos ver como [gestionar errores](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html#_error_handling).

Si no definimos ningún onStatus(), las respuestas con un código HTTP mayor que 400, lanzarán un RestClientResponseException, pero si definimos el método podemos personalizarlo. 

Por ejemplo, aquí optamos por lanzar una IllegalArgumentException si recibimos un error del rango 400.

Aprovechamos para capturar este error y devolver un Optional.empty(), con lo cual tenemos el caso de que se solicite una canción no existente. Si queremos ser exhaustivos, tendríamos que añadir otra para el caso de que sea un error del servidor (usando is5xxServerError).

Y podemos terminar los tests:
```java
@Test
void givenNonExistingPlayedSongShouldReturnEmpty() {
  String notFoundId = "foo";
  setUpMockGetNotFoundRequest(notFoundId);

  Optional<PlayListHistoryItem> playedSong = songsLocalRepository.loadPlayedSong(notFoundId);

  assertThat(playedSong).isNotPresent();
}
@Test
void givenAnExistingPlayedSongShouldReturnIt() {
  PlayListHistoryItem playListHistoryItem = PlayListHistoryItemsMother.getPlayListHistoryItem();
  setUpMockGetByIdRequest(playListHistoryItem);

  Optional<PlayListHistoryItem> playedSong = songsLocalRepository.loadPlayedSong(playListHistoryItem.id());

  assertThat(playedSong).isPresent().contains(playListHistoryItem);
}

private void setUpMockGetNotFoundRequest(String notFoundId) {
  RequestHeadersUriSpec getRequest = mock(RequestHeadersUriSpec.class);
  ResponseSpec response = mock(ResponseSpec.class);
  when(restClient.get()).thenReturn(getRequest);
  when(getRequest.uri("/items/{id}", notFoundId)).thenReturn(getRequest);
  when(getRequest.accept(any())).thenReturn(getRequest);
  when(getRequest.retrieve()).thenReturn(response);
  when(response.onStatus(any(), any())).thenThrow(IllegalArgumentException.class);
}
private void setUpMockGetByIdRequest(PlayListHistoryItem item) {
  RequestHeadersUriSpec getRequest = mock(RequestHeadersUriSpec.class);
  ResponseSpec response = mock(ResponseSpec.class);
  when(restClient.get()).thenReturn(getRequest);
  when(getRequest.uri("/items/{id}", item.id())).thenReturn(getRequest);
  when(getRequest.accept(any())).thenReturn(getRequest);
  when(getRequest.retrieve()).thenReturn(response);
  when(response.onStatus(any(), any())).thenReturn(response);
  when(response.body(PlayListHistoryItem.class)).thenReturn(item);
}
```
Por último, vamos a crear una nueva reproducción de una canción si es válida. La especificación sería algo así:
```java
@Test
void givenANullPlayedSongShouldThrowIllegalArgumentExceptionWhenStoringIt() {
  Throwable thrown = catchThrowable(() -> songsLocalRepository.save(null));

  assertThat(thrown).isInstanceOf(IllegalArgumentException.class);
}

@Test
void givenAPlayedSongShouldStoreIt() {
  PlayListHistoryItem playListHistoryItem = PlayListHistoryItemsMother.getPlayListHistoryItem();

  PlayListHistoryItem savedPlayListHistoryItem = songsLocalRepository.save(playListHistoryItem);

  assertThat(savedPlayListHistoryItem).isEqualTo(playListHistoryItem);
}
```
Lo primero es crear un nuevo puerto para especificar la operación. ¿Por qué un nuevo puerto? Pues mientras que antes teníamos dos casos distintos pero con una misma funcionalidad, la carga de datos, aquí tenemos una funcionalidad completamente distinta y que podría estar implementada de otra manera:
```java
public interface SaveLastPlayedPort {

  PlayListHistoryItem save (PlayListHistoryItem item);
}
```
Pero en nuestro caso usaremos el mismo mecanismo de implementación (RestClient), así que lo implementamos en nuestro repositorio:
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
Vamos a revisar el uso de RestClient, aunque es bastante directo:
1. Decimos que vamos a hacer un post en vez de un get
2. La uri sería la misma porque vamos a crearlo en la misma colección
3. Como es un post, llevamos contenido, le tenemos que indicar que es de tipo JSON
4. Y le indicamos en el body cuál es el contenido que vamos a enviar
5. Por último, indicamos que queremos de vuelta JSON
6. Lo enviamos
7. Recuperamos la respuesta

Lo único que puede resultar confuso aquí es que tenemos dos veces la llamada a body(), pero tiene sentido, en una para el cuerpo de la petición y en la última para parsear el cuerpo de la respuesta. Si no quisiéramos devolver nada, podríamos ignorar este último.

Ahora vamos a dejar las pruebas pasando:
```java
@Test
void givenANullPlayedSongShouldThrowIllegalArgumentExceptionWhenStoringIt() {
  Throwable thrown = catchThrowable(() -> songsLocalRepository.save(null));

  assertThat(thrown).isInstanceOf(IllegalArgumentException.class);
}

@Test
void givenAPlayedSongShouldStoreIt() {
  PlayListHistoryItem playListHistoryItem = PlayListHistoryItemsMother.getPlayListHistoryItem();
  setUpMockPostRequest(playListHistoryItem);

  PlayListHistoryItem savedPlayListHistoryItem = songsLocalRepository.save(playListHistoryItem);

  assertThat(savedPlayListHistoryItem).isEqualTo(playListHistoryItem);
}

private void setUpMockPostRequest(PlayListHistoryItem item) {
  RequestBodyUriSpec postRequest = mock(RequestBodyUriSpec.class);
  ResponseSpec response = mock(ResponseSpec.class);
  when(restClient.post()).thenReturn(postRequest);
  when(postRequest.uri(anyString())).thenReturn(postRequest);
  when(postRequest.contentType(any())).thenReturn(postRequest);
  when(postRequest.body(any(PlayListHistoryItem.class))).thenReturn(postRequest);
  when(postRequest.accept(any())).thenReturn(postRequest);
  when(postRequest.retrieve()).thenReturn(response);
  when(response.body(PlayListHistoryItem.class)).thenReturn(item);
}
```
Con esto tendríamos una cobertura completa de tests de nuestro proyecto. Si quisiéramos ser exhaustivos, ahora tendríamos que hacer pruebas de integración, usando [WireMock](https://github.com/maciejwalkowiak/wiremock-spring-boot) para mockear las respuestas del servidor, pero para no extender mucho más el artículo, vamos a ver como podríamos lanzarlo al arrancar la aplicación.

```java
@SpringBootApplication
public class PlayListHistoryApplication {

  public static void main(String[] args) {
    SpringApplication.run(PlayListHistoryApplication.class, args);
  }

  @Bean
  public RestClient restClient(@Value("${song-server.base.url}") String baseUrl) {
    return RestClient.builder()
        .baseUrl(baseUrl)
        .build();
  }

  @Bean
  public LoadLastPlayedPort loadLastPlayedPort(RestClient restClient) {
    return new SongsLocalRepository(restClient);
  }

  @Bean
  public SaveLastPlayedPort saveLastPlayedPort(RestClient restClient) {
    return new SongsLocalRepository(restClient);
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
Aquí podemos ver como se define el RestClient como un bean de Spring (leyendo su URL base de una propiedad definida en el application.properties), como instanciamos los puertos, aunque sea la misma clase de implementación, así nos mantenemos independizados de que esta implementación cambie en un futuro y como los inyectamos en un bean de tipo ApplicationRunner que se ejecutará al arrancar la aplicación.

Realmente la lógica de creación de la nueva canción debería ir en un puerto primario (o de entrada) de la aplicación, pero se va un poco del objetivo de mostrar como usar RestClient.

Si arrancamos JSON server y lanzamos la aplicación podemos ver que ejecuta sin más (¿qué esperabas? Al fín y al cabo no hemos puesto ningún mensaje de salida :P).

Tienes el código completo en [GitHub](https://github.com/agustinventura/playlisthistory)