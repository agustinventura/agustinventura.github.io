---
title: De la Historia de Usuario a la Documentación Viva con Cucumber
date: 2025-10-27
tags:
  - Development
  - Gradle
  - Cucumber
  - Gherkin
  - JUnit
  - Java
  - Spring Boot
---

Ya hemos visto en otro post mi propuesta para tener una [documentación ligera](https://www.agustinventura.dev/posts/definici%C3%B3n-de-proyectos-y-documentaci%C3%B3n-ligera/) del proyecto que se mantenga actualizada y sea realmente útil (spoiler: reduciéndola al máximo), sin embargo era documentación más bien técnica, dirigida al equipo o a posibles colaboradores. Es cierto que tenemos un README en el que especificamos que hace la aplicación (o servicio o como queramos decirle), pero... ¿cómo podemos mantener viva la documentación sobre *QUÉ* es lo que hace el proyecto detalladamente? ¿No sería genial si esta documentación fuera ejecutable y verificable? De esa manera nos podríamos asegurar siempre de que no rompemos nada y que la funcionalidad más importante de la aplicación sigue funcionando.
De la misma manera que para la documentación técnica trato de mantener un enfoque práctico y minimalista, creo que para esta documentación de funcionalidad (o comportamiento) debemos hacer lo mismo. Cuántos más artefactos superfluos tengamos (larguísimos documentos de requisitos, especificaciones de usuarios...) peor, mayor sería la entropía acumulada. Entonces, ¿cómo podemos recoger esta información? Una aproximación son las historias de usuario.

# Las historias de usuario
Todos hemos utilizado las [historias de usuario](https://es.wikipedia.org/wiki/Historias_de_usuario), algunos incluso las hemos escrito físicamente en tarjetas rayadas. Según el autor pueden contener distinta información, pero en general escribiremos:
- Título de la historia (y un código opcionalmente)
- Usuario que la ejerce
- Beneficios que obtengo si se completa

Esta aproximación a la documentación es sencilla y directa y puedes tenerla en formato físico (tarjetas), en un documento de Word, en una Wiki o en herramientas dedicadas como Jira, Trello o cualquier gestor de proyectos. Cada una de estas herramientas trata de solucionar un problema concreto:

- Tarjetas: Da satisfacción escribirlas y manejarlas, además podemos usar un kanban físico como radiador de información para que el equipo vea fácilmente el progreso. A cambio se estropean y son difíciles de modificar.
- Documento de texto: Soluciona el problema de la modificación pero a cambio perdemos tanto la fisicidad como la capacidad de gestión (cambiar estado, etc...), al menos fácilmente.
- Jira/Trello: Perdemos el formato físico pero si nos permite hacer radiadores de información y gestionar estado, modificar etc...

Con esto podemos pensar que un gestor de proyectos es la solución idónea, sin embargo todas estas soluciones tienen un problema compartido: son documentación del proyecto y la documentación se queda obsoleta.
Pensemos en la historia de usuario más sencilla del Leaderboard, devolver el mismo Leaderboard. Podemos registrarla, implementarla, etc... posteriormente decidimos que vamos a ponerle unos límites de consumo para evitar abusos, es decir, nuestra historia de usuario pasa de ser "cualquier usuario puede consultar tantas veces como desee el leaderboard" a "cualquier usuario puede consultar un máximo de 60 veces por minuto el leaderboard". Si somos extremadamente ordenados es posible que tengamos épicas en nuestro gestor de proyecto y que enlacemos las historias de usuario y esto no es baladí, sino que es una información muy valiosa. Sin embargo, más adelante es posible que refinemos la historia de usuario al introducir roles y que decidamos que los administradores no tienen límites de consulta, tenemos ya una cadena de tres historias de usuario. Podemos tomar la decisión (y sería más que razonable) de que cada historia debe ser universal y absoluta y describir el comportamiento actual del sistema, sin embargo seguimos dependiendo de nuestra disciplina a la hora de documentar y registrar.
Estamos considerando que siempre vamos a registrar las historias de usuario de la misma manera, que siempre los vamos a enlazar con las anteriores y relacionadas y que el que redacta una nuevo va a tener en cuenta el contexto anterior, todo eso con un único objetivo: tener un punto de referencia del comportamiento del sistema actual.

Pero, ¿podemos hacer algo mejor? ¿Y si hubiera una manera de expresar nuestras historias de usuario como código?

# Behavior Driven Development
Si miras la página de [BDD en la Wikipedia](https://es.wikipedia.org/wiki/Desarrollo_guiado_por_comportamiento) verás que comentan que surge a partir de [TDD](https://es.wikipedia.org/wiki/Desarrollo_guiado_por_pruebas) y estrictamente es así, Dan North lo crea en 2007 como una mejora o puente entre TDD y DDD y lo que nos permite es definir mediante un [DSL](https://es.wikipedia.org/wiki/Lenguaje_espec%C3%ADfico_de_dominio) el comportamiento del sistema, es decir lo que queremos que haga la aplicación y en un lenguaje muy parecido al natural, tanto es así que hay quién dice que estos tests los podría o debería escribir personal de negocio directamente. Yo creo que esto no va muy desencaminado, pero es mejor escribirlas juntos o al menos de una manera colaborativa (por favor, seamos comprensivos, lo más probable es que a la persona de negocio le interese 0 aprender este pseudocódigo).
Precisamente, [Fran Moreno](https://bsky.app/profile/morvader.bsky.social) tiene [un interesantísimo artículo en el que habla sobre esto (y bastantes otras cosas igualmente interesantes)](https://morvader.substack.com/i/173676808/cucumber-mal-entendido-y-mal-utilizado), lo interesante de esta herramienta es cuando se aplica en colaboración con negocio y antes de escribir nada, si vas a hacer la clásica de escribirlos después o tienes un equipo puramente técnico, no va a ser lo mejor. Pero si de verdad tienes a gente de negocio (o un cliente) involucrada, es una forma fantástica de colaborar, definir, refinar y encima quedarte con el sistema bien definido y ejecutable.
Entrando ya en detalle, el lenguaje más utilizado para BDD es Gherkin y podríamos expresar el comportamiento de un leaderboard vacío así:

```gherkin
Feature: Get Leaderboard  
  
  As a user  
  I want to retrieve the leaderboard  
  So that I can see all entries with their scores  
  
  Scenario: Retrieve empty leaderboard  
    Given a leaderboard without entries  
    When I retrieve the leaderboard  
    Then I should see no entries
```

Vaya, pero si esto es... ¡una historia de usuario! Acabamos de pasar de tener una historia de usuario que es papel (o tickets de Jira) a algo ejecutable. Esto no significa que esté de más Jira, que no deba existir (debe, ya que es donde planificamos), si no que ahora podemos comprobar de manera fehaciente la implementación de nuestras historias de usuario. Es cierto que tenemos el doble trabajo de escribirlas en Jira y en Gherkin en nuestro proyecto, pero de esta manera ganamos no solo la verificación como herramienta de QA si no el control de versiones. Pasamos a tener **documentación viva**.
Nos aseguramos de que si cambiamos el comportamiento del sistema, la build fallará y nos recordará que o bien tenemos que crear un nuevo ticket o bien modificar el existente, etc... Todo ventajas.
Junto con TDD esto compone el doble bucle del que hablo en el ADR-003: Estrategia de Pruebas de Software. Definimos el comportamiento externo del sistema mediante BDD, escribiéndolo en Gherkin y utilizamos TDD, pruebas unitarias y de aceptación para guiarnos en la implementación. BDD es el puente entre la documentación y la planificación del sistema y el diseño e implementación del mismo.
Pero [Gherkin](https://cucumber.io/docs/gherkin/reference/) (y BDD) no es un juguete, sino que podemos expresar condiciones más complejas, como tablas. Por ejemplo, se puede definir el comportamiento completo de obtener un leaderboard así:

```gherkin
Feature: Get Leaderboard

  As a user
  I want to retrieve the leaderboard
  So that I can see all entries sorted by score

  Scenario: Retrieve empty leaderboard
    Given a leaderboard without entries
    When I retrieve the leaderboard
    Then the leaderboard should be empty

  Scenario: Retrieve leaderboard sorted by score
    Given the following leaderboard entries exist:
      | playerName | score |
      | player5    | 100   |
      | player6    | 150   |
      | player7    | 120   |
    When I retrieve the leaderboard
    Then I should see the following leaderboard entries:
      | playerName | score |
      | player6    | 150   |
      | player7    | 120   |
      | player5    | 100   |
```

Resumiendo: si el Leaderboard esta vacío, devuélvemelo vacío, si no, devuélvemelo ordenado por puntuación. Exactamente lo que debe hacer un buen Leaderboard, ¿no?
Vale, esto es muy bonito, pero una vez escrito, ¿cómo hacemos para que sea ejecutable? Vamos a ello.

# Estructurando nuestros tests
Lo primero es decidir donde vamos a guardar estos features. Lo primero que tenemos que tener en cuenta es que para su ejecución van a necesitar levantar toda la aplicación, realmente son tests end to end o de aceptación, esto ya nos deja entrever que podemos ponerlo en el módulo infrastructure tal y como discutimos [al hablar de ArchUnit](https://www.agustinventura.dev/posts/como-blindar-tu-arquitectura-hexagonal-con-gradle-y-archunit/) pero... ¿realmente estos tests pertenecen a infrastructure? ¿No podríamos decir más bien que utilizan infrastructure? O más correctamente, que utilizan la aplicación aunque el punto de entrada, nuestra clase marcada con `@SpringBootApplication`, esté en el módulo infrastructure. 
Esta discusión se parece mucho a la que tuvimos con ArchUnit, las pruebas usan la aplicación pero no pertenecen a la aplicación, son un observador externo... ¿entonces? Bueno, pues podríamos ponerlas en el módulo `architecture-tests`, pero estaríamos mezclando dos cosas completamente distintas, un analizador de la estructura interna de la aplicación con un comprobador del comportamiento de la aplicación... Así que solo nos queda una opción... Sí, otro módulo que podemos llamar `acceptance-tests`.

## Creación del nuevo módulo
Ya lo hemos visto antes:

1. Añadimos el módulo `acceptance-tests` al `settings.gradle.kts`
```kotlin
rootProject.name = "leaderboard"  
  
include(  
    ":domain",  
    ":application",  
    ":infrastructure",  
    ":architecture-tests",  
    ":acceptance-tests"  
)
```

2. Creamos el directorio `acceptance-tests` y su `build.gradle.kts`. Este módulo tampoco tendrá fuentes en `main`, tan solo en `test` como el de `architecture-tests` y tan solo dependerá del módulo `infrastructure` (a diferencia del de `architecture-tests` que si dependía de los  tres ya que los analizaba, aquí solo necesitamos `infrastructure` para arrancar la aplicación).
```kotlin
plugins {  
    `java-library`  
}  
  
dependencies {  
    testImplementation(project(":infrastructure"))  
    testImplementation("org.springframework.boot:spring-boot-starter-test")  
    testImplementation("io.cucumber:cucumber-java:7.30.0")  
    testImplementation("io.cucumber:cucumber-spring:7.30.0")  
    testRuntimeOnly("io.cucumber:cucumber-junit-platform-engine:7.30.0")  
    testImplementation("io.rest-assured:rest-assured:5.5.6")  
}  
  
tasks.withType<Test> {  
    useJUnitPlatform()  
}
```

## Escribiendo los tests
Con esto ya tenemos nuestro nuevo módulo y podemos empezar a escribir los tests... aunque bueno, en realidad el primero ya lo tenemos, es justo el de aquí arriba. Por convenio, vamos a coger ese feature descrito en Gherkin y lo vamos a poner en `src/test/resources/features` y llamaremos al archivo `get_leaderboard.feature`
Lo que viene ahora es un poco complejo porque tenemos que acoplar tres partes móviles distintas: por una parte Cucumber que leerá el archivo Gherkin y lo ejecutará, por otra parte JUnit como motor de pruebas y por último, Spring que levantará la aplicación. Lo podemos ver en las dependencias que hemos usado, dejando de lado `rest-assured` para un poco de azúcar sintáctico en las pruebas, son precisamente las que implementan esta funcionalidad.

### Configuración de JUnit para ejecutar Cucumber
Esta parte es muy sencilla, sobre todo porque tenemos nuestras pruebas en un módulo aparte, si las tuviéramos en un módulo compartido, sería algo más complejo. Lo que vamos a hacer es decirle al JUnit que se ejecuta en este módulo que lance Cucumber, ¿cómo? Pues creando un archivo `junit-platform.properties` en `src/test/resources` que es el archivo de configuración de JUnit para este proyecto con este contenido:
```
cucumber.plugin=pretty
cucumber.glue=dev.agustinventura.leaderboard
cucumber.features=src/test/resources/features
```

En cuanto tenemos propiedades de configuración de Cucumber en este archivo, JUnit activará el plugin de Cucumber y le aplicará la configuración que establecemos, que por lo demás es bastante directa:
- `cucumber.plugin`: Formatea la salida con estilo, entre otras cosas usando rojo para los mensajes de error y verde para los de éxito.
- `cucumber.glue`: Es el paquete en el que va a estar la implementación en Java de los steps (ahora lo vemos) y clases auxiliares (como la que levanta el contexto de Spring)
- `cucumber.features`: Al igual que le decimos donde esta la implementación de los steps, le tenemos que decir donde están los features.

### Configuración de Cucumber y Spring
Ahora necesitamos arrancar la aplicación (Spring) cuando lanzamos Cucumber, para eso, en `src/test/java/leaderboard`creamos una clase `CucumberSpringConfiguration`:
```java
@CucumberContextConfiguration  
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)  
public class CucumberSpringConfiguration {  
  
}
```

De momento (jeje) esta clase conecta Cucumber con Spring, lo que hace es que cuando JUnit lanza Cucumber tal y como hemos configurado en el archivo de propiedades, Cucumber escanea buscando la anotación `@cucumberContextConfiguration` y cuando la encuentra, carga la clase. Como la clase también tiene la anotación `@SpringBootTest` lo que va a hacer es levantar Spring (buscando una clase marcada con `@SpringBootApplication`que todavía no tenemos... y por tanto nuestros tests van a fallar).

### Implementación de los steps
Y ya esta, solo nos quedaría implementar los steps. En el paquete que le hemos indicado a Cucumber con `cucumber.glue` creamos un nuevo paquete `steps` (por tenerlo ordenado) y ahí la clase `LeaderboardSteps`:
```java
public class LeaderboardSteps {  
  
    @LocalServerPort  
    private int port;  
  
    private Response response;  
  
    @Before  
    public void setup() {  
        RestAssured.baseURI = "http://localhost";  
        RestAssured.port = port;  
    }  
  
    @Given("a leaderboard without entries")  
    public void a_leaderboard_without_entries() {  
  
    }  
  
    @Given("the following leaderboard entries exist:")  
    public void the_following_leaderboard_entries_exist(DataTable dataTable) {  
        List<Map<String, String>> entries = dataTable.asMaps(String.class, String.class);  
  
        for (Map<String, String> entry : entries) {  
            String requestBody = String.format(  
                    "{\"playerName\": \"%s\", \"score\": %s}",  
                    entry.get("playerName"),  
                    entry.get("score")  
            );  
  
            given()  
                    .contentType(ContentType.JSON)  
                    .body(requestBody)  
                    .when()  
                    .post("/leaderboard-entries")  
                    .then()  
                    .statusCode(201);  
        }  
    }  
  
    @When("I retrieve the leaderboard")  
    public void i_retrieve_the_leaderboard() {  
        response = given()  
                .when()  
                .get("/leaderboard");  
    }  
  
    @Then("the leaderboard should be empty")  
    public void the_leaderboard_should_be_empty() {  
        assertThat(response.getStatusCode()).isEqualTo(200);  
  
        List<Object> responseBody = response.jsonPath().getList("$");  
        assertThat(responseBody).isEmpty();  
    }  
  
    @Then("I should see the following leaderboard entries:")  
    public void i_should_see_the_following_leaderboard_entries(DataTable dataTable) {  
        List<Map<String, String>> expectedEntries = dataTable.asMaps(String.class, String.class);  
  
        assertThat(response.getStatusCode()).isEqualTo(200);  
        List<Map<String, Object>> responseBody = response.jsonPath().getList("$");  
  
        assertThat(responseBody)  
                .hasSize(expectedEntries.size())  
                .extracting("playerName", "score")  
                .containsExactly(  
                        expectedEntries.stream()  
                                .map(row -> tuple(  
                                        row.get("playerName"),  
                                        Integer.parseInt(row.get("score"))  
                                ))  
                                .toArray(org.assertj.core.groups.Tuple[]::new)  
                );  
    }  
}
```

Nada extraño, creo que es bastante entendible, como arrancamos la aplicación Spring en un puerto random (lo especificamos en `CucumberSpringConfiguration`), usamos `@LocalServerPort`para obtenerlo en tiempo de ejecución y configurar `rest-assured`para utilizarlo y hacer llamadas a nuestra API REST.
Después simplemente con las anotaciones `@Given`/`@When`/`@Then`y sus descripciones lo enlazamos con el archivo feature y esa sería toda la magia.

## Lanzando los tests
Facilísimo, tenemos dos opciones:
1. Desde nuestro IDE, nos vamos al archivo `get_leaderboard.feature`y podemos lanzar toda la feature o solo uno de los escenarios, lo que queramos.
2. Desde la línea de comandos: `./gradlew :acceptance-tests:test`

En cualquier caso va a fallar porque... bueno, no tenemos código, solo los steps definidos xD

Si quieres consultarlo todo junto, lo tienes en [GitHub](https://github.com/agustinventura/leaderboard/tree/feature/003-bdd-setup)