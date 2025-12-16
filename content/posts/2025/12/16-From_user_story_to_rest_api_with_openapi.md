---
title: De la historia de usuario a la API REST con OpenAPI
date: 2025-12-16
tags:
  - Development
  - Gradle
  - JUnit
  - Java
  - Spring Boot
  - Cucumber
  - OpenAPI
---

En [artículos anteriores](https://www.agustinventura.dev/posts/de-la-historia-de-usuario-a-la-documentaci%C3%B3n-viva-con-cucumber/) vimos cómo aplicar BDD con Cucumber y JUnit para ejecutar historias de usuario. Ahora implementaremos la API REST que satisface esas pruebas utilizando Spring Boot y **OpenAPI Specification**.

Dado que estamos creando un backend, nuestras historias de usuario se traducen en llamadas a una API REST (conforme a nuestros [ADRs](https://www.agustinventura.dev/posts/definici%C3%B3n-de-proyectos-y-documentaci%C3%B3n-ligera/)). Podríamos implementar rápidamente un `RestController` de Spring MVC, sin embargo, este enfoque tiene problemas graves:
1. **Exposición del dominio:** Tendemos a devolver entidades (como `LeaderboardEntry`) en lugar de DTOs, acoplando la API a la lógica interna.
2. **Falta de contrato:** El código se convierte en la única fuente de verdad, dificultando la integración para terceros.
3. **Documentación pobre:** Aunque [Springdoc](https://springdoc.org/) genera documentación visual, es un resultado de la implementación, no una especificación previa.

La solución pasa por **OpenAPI Specification** (actualmente en versión 3.2.0). Sus ventajas:
- **Contrato único:** Un solo archivo JSON/YAML define rutas, métodos y datos.
- **Generación automática:** Crea tanto el código del servidor (interfaces y DTOs) como clientes para los consumidores.
- **Contract-First:** Define la API antes de escribir una sola línea de código.

Vamos a definir por tanto una API con dos operaciones:
- `GET` para obtener el leaderboard.
- `POST` para crear una nueva entrada.
## Definición de la API
Utilizaremos **OpenAPI 3.1.0** (la versión más alta soportada actualmente por el plugin de generación de código [OpenAPI Generator](https://openapi-generator.tech/docs/plugins/#gradle)).

```yaml
openapi: 3.1.0  
info:  
  title: Leaderboard API  
  description: API for the Leaderboard service  
  version: 1.0.0  
tags:  
  - name: Leaderboard  
    description: Operations related to scores and players  
paths:  
  /v1/leaderboard:  
    get:  
      tags:  
        - Leaderboard  
      summary: Retrieves the leaderboard  
      description: Returns a paginated list of scores.  
      operationId: getLeaderboard  
      responses:  
        '200':  
          description: A sorted list of leaderboard entries  
          content:  
            application/json:  
              schema:  
                type: array  
                items:  
                  $ref: '#/components/schemas/LeaderboardEntry'  
        '500':  
          description: Internal Server Error  
          content:  
            application/json:  
              schema:  
                $ref: '#/components/schemas/Error'  
  /v1/leaderboard/entries:  
    post:  
      tags:  
        - Leaderboard  
      summary: Adds a new entry to the leaderboard  
      operationId: addLeaderboardEntry  
      requestBody:  
        required: true  
        content:  
          application/json:  
            schema:  
              $ref: '#/components/schemas/LeaderboardEntry'  
      responses:  
        '201':  
          description: Entry created successfully  
          headers:  
            Location:  
              description: URI of the resource  
              schema:  
                type: string  
                format: uri  
        '400':  
          description: Invalid input data  
          content:  
            application/json:  
              schema:  
                $ref: '#/components/schemas/Error'  
        '500':  
          description: Internal Server Error  
          content:  
            application/json:  
              schema:  
                $ref: '#/components/schemas/Error'  
components:  
  schemas:  
    LeaderboardEntry:  
      type: object  
      description: Represents a saved score record  
      required:  
        - playerName  
        - score  
      properties:  
        playerName:  
          type: string  
          minLength: 3  
          maxLength: 20  
          example: 'PlayerOne'  
        score:  
          type: integer  
          format: int64  
          minimum: 0  
          example: 12345  
    Error:  
      type: object  
      properties:  
        code:  
          type: integer  
          example: 400  
        message:  
          type: string  
          example: "El nombre del jugador es obligatorio"
```

La especificación es bastante clara, pero analicemos los bloques clave que definirán nuestro código:

**1. Metadatos y Organización (`info` y `tags`)** Primero, `openapi` indica la versión de la especificación (la 3.1.0 para compatibilidad). El bloque `info` contiene los metadatos globales; aquí la clave es el campo `version`, la salvaguarda para gestionar el ciclo de vida y futuros cambios de la API. Por su parte, `tags` nos permite agrupar los recursos de forma lógica para mantener la documentación navegable.

**2. Los Recursos (`paths`)** Esta es la sección más interesante. Por cada recurso definimos los verbos HTTP soportados: `GET` para leer el leaderboard y `POST` para crear entradas. Cada operación incluye información descriptiva y, lo más importante, operativa:
- **`operationId`:** El generador usará este ID para nombrar los métodos en la interfaz Java (`getLeaderboard`, `addLeaderboardEntry`).
- **Tipado Fuerte:** Tanto en `requestBody` (entradas) como en `responses` (salidas), definimos estrictamente el `content` aceptado (JSON) y su estructura (`schema`). El `POST` es interesante: si todo va bien (`201`),  devolvemos una cabecera `Location` con la URI del nuevo recurso.

**3. Modelos de Datos (`components`)** En lugar de repetir estructuras, referenciamos definiciones alojadas en `components/schemas`. Aquí definimos nuestros tipos (`LeaderboardEntry`, `Error`) con sus restricciones de validación.

**Decisiones de Diseño Explícitas** :
- **Versionado en URL:** Anteponemos `/v1` a los paths para gestionar versiones.
- **Simplicidad en la respuesta:** No hemos creado un objeto envoltorio "Leaderboard"; la respuesta es directamente un array de `LeaderboardEntry`.
- **Formato único:** La API es estricta y solo negocia contenido en formato `application/json`.

## Generación del código

Para generar el código servidor, configuramos el plugin [OpenAPI Generator](https://openapi-generator.tech/docs/plugins/#gradle) en el `build.gradle.kts` del módulo `infrastructure`:
```kotlin
import org.openapitools.generator.gradle.plugin.tasks.GenerateTask  
  
plugins {  
    alias(libs.plugins.spring.boot)  
    alias(libs.plugins.spring.dependency.management)  
    alias(libs.plugins.openapi.generator)  
    java  
}  
  
dependencies {  
    implementation(project(":domain"))  
    implementation(project(":application"))  
    implementation(platform(libs.spring.boot.bom))  
    implementation(libs.spring.boot.starter.actuator)  
    implementation(libs.spring.boot.starter.data.jdbc)  
    implementation(libs.spring.boot.starter.web)  
    implementation(libs.flyway.core)  
    implementation(libs.flyway.postgresql)  
    implementation(libs.spring.kafka)  
    implementation(libs.swagger.annotations)  
    implementation(libs.validation.api)  
    implementation(libs.springdoc.openapi.starter.webmvc.ui)  
    implementation(libs.mapstruct)  
    annotationProcessor(libs.mapstruct.processor)  
  
    runtimeOnly(libs.postgresql)  
    testImplementation(libs.spring.boot.starter.test)  
    testImplementation(libs.spring.kafka.test)  
    testImplementation(libs.instancio.junit)  
}  
  
tasks.withType<GenerateTask> {  
    generatorName.set("spring")  
    inputSpec.set("$projectDir/src/main/resources/api/openapi.yaml")  
    outputDir.set(layout.buildDirectory.dir("generated").get().asFile.absolutePath)  
    apiPackage.set("dev.agustinventura.leaderboard.adapters.in.rest")  
    modelPackage.set("dev.agustinventura.leaderboard.adapters.in.rest.dto")  
    modelNameSuffix.set("RESTDTO")  
    openapiGeneratorIgnoreList.set(listOf("src/main/java/org/openapitools/OpenApiGeneratorApplication.java"))
    configOptions.set(  
        mapOf(  
            "useSpringBoot3" to "true",  
            "delegatePattern" to "true",  
            "openApiNullable" to "false",  
            "documentationProvider" to "springdoc",
            "useTags" to "true"  
        )  
    )  
}  
  
java {  
    sourceSets.main {  
        java {  
            srcDir(layout.buildDirectory.dir("generated/src/main/java").get().asFile.absolutePath)  
        }  
    }}  
  
tasks.compileJava {  
    dependsOn(tasks.withType<GenerateTask>())  
}  
  
tasks.clean {  
    delete(layout.buildDirectory.dir("generated"))  
}
```

Tal y como vimos en [la configuración de Gradle para arquitectura hexagonal](https://www.agustinventura.dev/posts/configuraci%C3%B3n-de-gradle-con-arquitectura-hexagonal/), definimos la dependencia del plugin en `libs.versions.toml`. Una vez aplicado, configuramos la tarea `tasks.withType<GenerateTask>` con los parámetros clave:

**Configuración General:**
- **`generatorName`:** Establecido a `spring`. Esto asegura que el código generado incluya las anotaciones de Spring MVC (como `@RestController`).
- **`inputSpec` / `outputDir`:** Definen la ubicación del contrato YAML y el directorio destino de los archivos generados.
- **`apiPackage` / `modelPackage`:** El paquete para las interfaces y DTOs de la API. Siguiendo la arquitectura hexagonal, lo ubicamos en `adapters.in.rest` (adaptador de entrada con tecnología REST) y los DTOs en `adapters.in.rest.dto`.
- **`modelNameSuffix`:** Una propiedad muy útil para evitar colisiones de nombres. Al añadir el sufijo `RESTDTO`, nuestra definición `LeaderboardEntry` se generará como la clase `LeaderboardEntryRESTDTO`. Todo queda perfectamente distinguible del dominio.
- **`openapiGeneratorIgnoreList`:** **Crítica.** El generador intenta crear por defecto una clase `OpenApiGeneratorApplication` con su propio `main`. Esto confunde a Spring Boot al arrancar. Con esta lista, bloqueamos su generación para usar exclusivamente nuestra propia clase de aplicación.

**Opciones de Configuración (`configOptions`):** Estas opciones controlan el comportamiento fino del generador:
- **`useSpringBoot3`:** Activa la compatibilidad con Spring Boot 3, sustituyendo, por ejemplo, los imports de `javax` por `jakarta`.
- **`delegatePattern`:** **Imprescindible.** En lugar de generar controladores con lógica incrustada o interfaces genéricas con `NativeWebRequest`, genera una interfaz delegada (`LeaderboardApiDelegate`) con métodos fuertemente tipados. Nosotros solo tenemos que implementar esta interfaz, manteniendo nuestro código limpio y desacoplado.
- **`openApiNullable`:** A `false` para evitar que los campos opcionales se envuelvan en un objeto `JsonNullable`. Simplifica el manejo de datos, ya que la obligatoriedad ya está definida en el contrato YAML.
- **`documentationProvider`:** Al usar `springdoc`, las clases generadas incluyen anotaciones que alimentan automáticamente la interfaz de Swagger UI.
- **`useTags`:** Genera una interfaz por cada `tag` definido en el YAML. Así tendremos `LeaderboardAPI` separado de una hipotética `UserAPI`, manteniendo el código organizado.

**Integración con el ciclo de vida de Gradle:** Por último, enlazamos la generación con el build:
- **Bloque `java`:** Añadimos la carpeta de generados a los `sourceSets`. Esto es fundamental para que el IDE reconozca las clases y no marque errores de compilación.
- **`compileJava`:** Añadimos una dependencia (`dependsOn`) para garantizar que el código se genere antes de intentar compilar el proyecto.
- **`clean`:** Aseguramos que al ejecutar `gradle clean`, se elimine también el directorio de código generado para evitar artefactos obsoletos.

Para generar los fuentes ejecutamos:

```bash
./gradlew :infrastructure:build
```

Esto generará:
- **DTOs:** POJOs con anotaciones de validación, Swagger y Jackson.
- **LeaderboardAPI:** Interfaz con `@RequestMapping` y `@Operation`.
- **LeaderboardAPIDelegate:** La interfaz que debemos implementar.
- **APIUtil:** Clase de utilidad de uso interno por las clases generadas.

## Implementación de la API
Vamos a hacer que pase nuestra primera prueba de aceptación: devolver un leaderboard vacío.
### Arrancar la aplicación
Necesitamos definir el punto de entrada de la aplicación, la clase que marcamos con `@SpringBootApplication` y que hará que sea ejecutable:d

```java
package dev.agustinventura.leaderboard;  
  
import org.springframework.boot.SpringApplication;  
import org.springframework.boot.autoconfigure.SpringBootApplication;  
  
@SpringBootApplication  
public class LeaderboardApplication {  
  
    public static void main(String[] args) {  
        SpringApplication.run(LeaderboardApplication.class, args);  
    }  
}
```

### 1. El Test Unitario
Siguiendo TDD, primero definimos el comportamiento del adaptador mediante un test unitario:

```java
class LeaderboardRestAdapterTest {  
  
    private final LeaderboardRestAdapter sut = new LeaderboardRestAdapter();  
  
    @Test  
    @DisplayName("Given a leaderboard without entries, it should return an empty list")  
    void givenALeaderboardWithoutEntriesShouldReturnEmptyLeaderboard() {  
        ResponseEntity<List<LeaderboardEntryRESTDTO>> response = sut.getLeaderboard();  
  
        assertThat(response.getStatusCode().is2xxSuccessful()).isTrue();  
        assertThat(response.getBody()).isEmpty();  
    }  
}
```

### 2. El Adaptador (Implementación)
Implementamos la interfaz generada `LeaderboardApiDelegate`:

```java
public class LeaderboardRestAdapter implements LeaderboardApiDelegate {  
  
    @Override  
    public ResponseEntity<List<LeaderboardEntryRESTDTO>> getLeaderboard() {  
        return ResponseEntity.ok(Collections.emptyList());  
    }  
}
```
### 3. Configuración Hexagonal

Para respetar la **Arquitectura Hexagonal**, el adaptador debe ser un POJO puro, agnóstico al framework. Evitamos anotar la clase con `@RestController` o `@Component` y delegamos la inyección a una clase de configuración externa:

```java
package dev.agustinventura.leaderboard.configuration;  
  
import dev.agustinventura.leaderboard.adapters.in.rest.LeaderboardApiDelegate;  
import dev.agustinventura.leaderboard.adapters.in.rest.LeaderboardRestAdapter;  
import org.springframework.context.annotation.Bean;  
import org.springframework.context.annotation.Configuration;  
  
@Configuration  
public class LeaderboardApplicationConfiguration {  
  
    @Bean  
    public LeaderboardApiDelegate leaderboardApiDelegate() {  
        return new LeaderboardRestAdapter();  
    }  
}
```

### Resultado

Con esto, alcanzamos dos hitos importantes:
1. **Tests en Verde:** Si ejecutamos `./gradlew test`, Cucumber validará correctamente el escenario de leaderboard vacío (aunque fallará el de crear entradas, que aún no hemos implementado).
2. **Documentación Viva:** Si ejecutamos `./gradlew bootRun`, Spring Boot levantará la aplicación y detectará la documentación generada.

Accediendo a `http://localhost:8080/swagger-ui/index.html` veremos el laboratorio de pruebas interactivo, totalmente sincronizado con nuestro contrato YAML original, listo para ser utilizado por el equipo de frontend o clientes externos.

Tienes el código completo en [GitHub](https://github.com/agustinventura/leaderboard/tree/feature/006-OpenAPI_implementation)