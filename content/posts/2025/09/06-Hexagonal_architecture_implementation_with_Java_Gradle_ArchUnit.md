---
title: Como blindar tu arquitectura hexagonal con Gradle y ArchUnit
date: 2025-09-06
tags:
  - Development
  - Hexagonal Architecture
  - Gradle
  - ArchUnit
  - Java
  - Spring Boot
---

### 1. ¿Qué es (realmente) la Arquitectura Hexagonal?

La **arquitectura hexagonal** está de moda, pero cuando te pones a investigar, te das cuenta de que el nombre es lo de menos. ¿Es hexagonal? ¿Ports & Adapters? ¿Arquitectura cebolla? ¿O incluso *Clean Architecture*? 🤔 La idiosincrasia es que realmente no es una arquitectura rígida, sino más bien un patrón, una serie de guías para construir tu aplicación.

En todas sus variantes, el flujo de la información es, a grandes rasgos, el siguiente:

`Adaptador de Entrada` → `Puerto de Entrada` → `Servicio de Aplicación` → `Dominio` → `Puerto de Salida` → `Adaptador de Salida`

Para que se entienda mejor, imaginemos que nos piden el *leaderboard* de jugadores a través de una API REST. El flujo sería algo así:

1.  **Adaptador REST**: Recibe la petición HTTP e invoca al caso de uso.
2.  **Caso de Uso (Servicio Leaderboard)**: Implementa la lógica para cargar el *leaderboard* y para ello invoca a un puerto de salida.
3.  **Puerto de Salida (Adaptador SQL)**: Habla con la base de datos, obtiene los datos y devuelve el objeto *Leaderboard*.
4.  **Caso de Uso (Servicio Leaderboard)**: Recibe el objeto del adaptador y lo devuelve.
5.  **Adaptador REST**: Convierte el objeto *Leaderboard* a un DTO y lo devuelve como respuesta HTTP.

Como ves, incluso esta nomenclatura no es fija, a mí me gusta llamar a los puertos de entrada _Caso de Uso_. Lo importante son **dos reglas fundamentales**:

* Cada capa habla **únicamente** con la siguiente.
* Todas las capas pueden usar el **Dominio**.

Si lo reducimos a esto, vemos que la implementación depende mucho del lenguaje y de sus herramientas.

---

### 2. Tres Formas de Organizar tu Proyecto en Java

Centrándonos en Java, se me ocurren tres formas principales de separar las capas de nuestra aplicación, de menos a más estricta:

#### Opción 1: Paquetes
La opción más sencilla. Tendríamos un paquete raíz (ej: `dev.agustinventura.leaderboard`) y dentro, tres paquetes principales: `domain`, `application` e `infrastructure`.

* **Ventajas**: Fácil y rápido de implementar.
* **Desventajas**: Depende totalmente de la disciplina del equipo. Nada impide que una clase rompa las reglas y acceda a un paquete que no debe. Su sencillez es su mayor debilidad.

#### Opción 2: Módulos de la Herramienta de Construcción (Gradle/Maven)
La idea es que el proyecto raíz reconozca tres carpetas como módulos independientes: `domain`, `application` e `infrastructure`.

* **Ventajas**: **Garantías fuertes**. Es imposible que el módulo `application` vea al de `infrastructure` si no lo declaras. Las dependencias son explícitas.
* **Desventajas**: Mayor complejidad de configuración y sigue habiendo un hueco: dentro del módulo `infrastructure`, un adaptador de entrada (un controlador REST) podría llamar directamente a un adaptador de salida (un repositorio SQL).

#### Opción 3: Módulos de la Plataforma Java (JPMS)
Introducidos en Java 9, permiten definir explícitamente qué paquetes exportas de un módulo y cuáles necesitas.

* **Ventajas**: **Máximo control** (puedes ocultar implementaciones) y es **Java puro**, independiente de la herramienta de construcción.
* **Desventajas**: Poco extendido en aplicaciones y puedes encontrar problemas de compatibilidad con librerías antiguas.

Para este artículo, nos quedaremos con la **Opción 2**, ya que ofrece un buen equilibrio entre garantías y complejidad.

---

### 3. Manos a la Obra: Modularizando con Gradle ⚙️

Vamos a ver un ejemplo práctico modularizando el proyecto *Leaderboard* partiendo de un esqueleto generado con Spring Initializr.

#### El Proyecto Raíz
Aquí definimos la configuración común para todos los submódulos.

##### `settings.gradle.kts`
Indicamos a Gradle que nuestro proyecto tiene tres módulos:
```kotlin
rootProject.name = "leaderboard"

include(
    ":domain",
    ":application",
    ":infrastructure"
)
```

##### `build.gradle.kts`
Definimos la versión de Java, el gestor de dependencias de Spring y las librerías de testing comunes para todos los módulos. Esto nos simplifica mucho la configuración individual.

```kotlin
import io.spring.gradle.dependencymanagement.dsl.DependencyManagementExtension
import org.springframework.boot.gradle.plugin.SpringBootPlugin

plugins {
	id("org.springframework.boot") version "3.5.5" apply false
	id("io.spring.dependency-management") version "1.1.7" apply false
}

subprojects {
    apply(plugin = "java")
    apply(plugin = "io.spring.dependency-management")

    group = "dev.agustinventura"
    version = "0.0.1-SNAPSHOT"

    extensions.configure<JavaPluginExtension> {
        toolchain {
            languageVersion.set(JavaLanguageVersion.of(21))
        }
    }

    configure<DependencyManagementExtension> {
        imports {
            mavenBom(SpringBootPlugin.BOM_COORDINATES)
        }
    }

    repositories {
        mavenCentral()
    }

    dependencies {
        "testImplementation"("org.junit.jupiter:junit-jupiter-api")
        "testRuntimeOnly"("org.junit.jupiter:junit-jupiter-engine")
        "testImplementation"("org.assertj:assertj-core")
        "testImplementation"("org.mockito:mockito-core")
    }
}
```

#### Los Módulos Individuales
##### Módulo `domain`
El más simple. Es una librería Java pura, sin dependencias.

```kotlin
plugins {
    "java-library"
}

dependencies {

}
```

##### Módulo `application`
También es Java puro y su __única dependencia__ es el módulo `domain`.

```kotlin
plugins {
    "java-library"
}

dependencies {
    implementation(project(":domain"))
}
```

##### Módulo `infrastructure`
Aquí está toda la "magia" tecnológica: Spring Boot, acceso a datos, mensajería, etc. Depende de `application` (y transitivamente de `domain`).

```kotlin
plugins {
    id("org.springframework.boot")
    id("java")
}

dependencies {
    implementation(project(":application"))
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.boot:spring-boot-starter-data-jdbc")
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.flywaydb:flyway-core")
    implementation("org.flywaydb:flyway-database-postgresql")
    implementation("org.springframework.kafka:spring-kafka")
    developmentOnly("org.springframework.boot:spring-boot-devtools")
    runtimeOnly("org.postgresql:postgresql")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework.kafka:spring-kafka-test")
}
```

### 4. La Solución Final: Blindando la Arquitectura con ArchUnit ✅
Como mencionamos, la estructura de módulos tiene un punto débil: dentro de `infrastructure`, las clases pueden llamarse entre sí sin control. Para evitarlo, vamos a usar __ArchUnit__.

ArchUnit es una librería para hacer __pruebas de arquitectura__. Nos permite escribir tests que verifiquen que nuestro código cumple las reglas que hemos definido. Es como un _linter_, pero a nivel de arquitectura.

¿Cómo añadimos ArchUnit? Podemos pensar en dos opciones de entrada.

#### 1. En cada módulo:
Añadimos la dependencia de ArchUnit al módulo raíz (para compartirla entre todos los módulos) y codificamos las reglas en cada módulo. Hay dos desventajas:
- Tenemos las reglas arquitectónicas diseminadas por todo el proyecto, no hay una visión en conjunto.
- Al estar constreñida la prueba que ejecutamos a un solo módulo no tiene una visibilidad completa del proyecto, por ejemplo, si ponemos en el módulo de aplicación la regla de que este no sea referenciado desde el módulo de dominio, como esta regla se ejecuta en el módulo aplicación no sabe que esta haciendo el módulo de dominio y no puede comprobarlo. Es decir, ArchUnit necesita una visión global sobre todo el proyecto, cosa bastante razonable ya que queremos comprobar el conjunto de reglas.
#### 2. Otro módulo de Gradle:
Si, crear submódulos para adaptadores de entrada y salida lo consideraba atomización, pero es que ésto precisamente no es atomización sino que estamos añadiendo nueva funcionalidad a la aplicación.
Este nuevo módulo será dependiente de los otros tres y podrá comprobar la interacción de ellos, es como un observador externo del sistema.

#### Implementación de ArchUnit
##### 1. Añadimos el nuevo módulo `architecture-tests` al `settings.gradle.kts`.
```kotlin
rootProject.name = "leaderboard"

include(
    ":domain",
    ":application",
    ":infrastructure",
    ":architecture-tests"
)
```

##### 2. Configuramos su `build.gradle.kts` para que dependa de los otros tres módulos y de ArchUnit.
Este módulo es especial: no tendrá código en src/main, solo en src/test.
```kotlin
plugins {
    `java-library`
}

dependencies {
    testImplementation(project(":domain"))
    testImplementation(project(":application"))
    testImplementation(project(":infrastructure"))
    testImplementation("org.junit.jupiter:junit-jupiter-api")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine")
    testImplementation("com.tngtech.archunit:archunit-junit5:1.4.1")
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

##### 3. Escribimos las reglas como si fueran tests unitarios.

##### Reglas de Dominio (`DomainRulesTest.java`)
Verificamos que el dominio es puro e independiente.

- __Regla__: Ninguna clase de domain debe depender de application, infrastructure o de frameworks como Spring.

```java
package dev.agustinventura.leaderboard.architecture_tests;  
  
import com.tngtech.archunit.junit.AnalyzeClasses;  
import com.tngtech.archunit.junit.ArchTest;  
import com.tngtech.archunit.lang.ArchRule;  
  
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;  
  
@AnalyzeClasses(packages = "dev.agustinventura.leaderboard")  
class DomainRulesTest {  
  
    @ArchTest  
    static final ArchRule domainShouldBeIndependent = noClasses()  
            .that().resideInAPackage("..domain..")  
            .should().dependOnClassesThat()  
            .resideInAPackage("..application..")  
            .orShould().dependOnClassesThat()  
            .resideInAPackage("..infrastructure..");  
  
    @ArchTest  
    static final ArchRule domainShouldNotDependOnFrameworks = noClasses()  
            .that().resideInAPackage("..domain..")  
            .should().dependOnClassesThat()  
            .resideInAnyPackage(  
                    "org.springframework.."  
            );  
}
```

##### Reglas de Aplicación (`ApplicationRulesTest.java`)
Definimos sus dependencias y convenciones de nombrado.

- __Regla__: `application` no debe depender de `infrastructure`.

- __Regla__: Los servicios deben terminar en `Service`, los puertos de entrada en `UseCase`, los de salida en `Port`, etc...

```java
import com.tngtech.archunit.junit.AnalyzeClasses;  
import com.tngtech.archunit.junit.ArchTest;  
import com.tngtech.archunit.lang.ArchRule;  
  
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.classes;  
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;  
  
@AnalyzeClasses(packages = "dev.agustinventura.leaderboard")  
class ApplicationRulesTest {  
  
    /**
     * Rule 1: The application layer should not depend on the infrastructure layer.
     * The application should only know about abstractions (ports), not concrete implementations.
     */
    @ArchTest
    static final ArchRule applicationShouldNotDependOnInfrastructure = noClasses()
            .that().resideInAPackage("..application..")
            .should().dependOnClassesThat()
            .resideInAPackage("..infrastructure..");

    /**
     * Rule 2: The application layer can only depend on the domain and itself.
     * This ensures that the application logic is not coupled to anything external, except for the business core.
     * Dependencies on standard Java libraries are allowed.
     */
    @ArchTest
    static final ArchRule applicationShouldOnlyDependOnDomain = classes()
            .that().resideInAPackage("..application..")
            .should().onlyDependOnClassesThat()
            .resideInAnyPackage(
                    "dev.agustinventura.leaderboard.application..",
                    "dev.agustinventura.leaderboard.domain..",
                    "java.."
            );

    /**
     * Rule 3: Naming convention for application services.
     * Ensures that classes implementing use cases follow a consistent pattern
     * and are in the correct package.
     */
    @ArchTest
    static final ArchRule applicationServicesShouldBeNamedCorrectly = classes()
            .that().haveSimpleNameEndingWith("Service")
            .and().areNotInterfaces()
            .should().resideInAPackage("..application.service..")
            .as("Application services should end with 'Service' and be in the 'service' package");

    /**
     * Rule 4: Input ports (Use Cases) must be interfaces ending in 'UseCase'.
     * These define the use cases that the application offers.
     */
    @ArchTest
    static final ArchRule inputPortsShouldBeUseCaseInterfaces = classes()
            .that().resideInAPackage("..application.port.in..")
            .should().haveSimpleNameEndingWith("UseCase")
            .andShould().beInterfaces()
            .as("Input ports must be interfaces and end with 'UseCase'");

    /**
     * Rule 5: Output ports (Ports) must be interfaces ending in 'Port'.
     * These define the dependencies that the application needs from the outside (e.g., a repository).
     */
    @ArchTest
    static final ArchRule outputPortsShouldBePortInterfaces = classes()
            .that().resideInAPackage("..application.port.out..")
            .should().haveSimpleNameEndingWith("Port")
            .andShould().beInterfaces()
            .as("Output ports must be interfaces and end with 'Port'");
}
```

##### Reglas de Infraestructura (`InfrastructureRulesTest.java`)
Finalmente, ponemos orden en la capa más externa.

- __Regla__: Los adaptadores de entrada no deben acceder directamente a los de salida.

- __Regla__: Los controladores REST deben estar en su paquete y terminar en `Controller`, los repositorios de Spring en `Repository`.

- __Regla__: Las clases de configuración de Spring estarán en el paquete `dev.agustinventura.leaderboard.infrastructure.config`

- __Regla__: Solo habrá un punto de entrada de la aplicación con la anotacion `@SpringBootApplication`. Esta regla la hemos definido con __JUnit__ y no con ArchUnit.

```java
import com.tngtech.archunit.core.domain.JavaClass;  
import com.tngtech.archunit.core.domain.JavaClasses;  
import com.tngtech.archunit.core.importer.ClassFileImporter;  
import com.tngtech.archunit.junit.AnalyzeClasses;  
import com.tngtech.archunit.junit.ArchTest;  
import com.tngtech.archunit.lang.ArchRule;  
import org.junit.jupiter.api.Test;  
  
import java.util.List;  
  
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.classes;  
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;  
import static org.assertj.core.api.Assertions.assertThat;  
  
@AnalyzeClasses(packages = "dev.agustinventura.leaderboard")  
class InfrastructureRulesTest {  
  
    /**  
     * Rule 1: Input adapters should not directly access output adapters.     
     * They must go through the application layer.     
     */    
    @ArchTest  
    static final ArchRule inputAdaptersShouldNotAccessOutputAdapters = noClasses()  
            .that().resideInAPackage("..infrastructure.adapter.in..")  
            .should().dependOnClassesThat()  
            .resideInAPackage("..infrastructure.adapter.out..");  
  
    /**  
     * Rule 2: Convention for REST controllers.     
     * They must be in the 'in.web' package, be annotated with @RestController, and their name must end with 'Controller'.     
     */    
    @ArchTest  
    static final ArchRule controllersShouldFollowConvention = classes()  
            .that().areAnnotatedWith("org.springframework.web.bind.annotation.RestController")  
            .should().resideInAPackage("..infrastructure.adapter.in.web..")  
            .andShould().haveSimpleNameEndingWith("Controller")  
            .as("REST controllers must be in the 'in.web' package and end with 'Controller'");  
  
    /**  
     * Rule 3: Convention for persistence adapters.     
     * They must be in the 'out.persistence' package, be annotated with @Repository, and their name must end with 'Repository'.     
     */    
    @ArchTest  
    static final ArchRule persistenceAdaptersShouldFollowConvention = classes()  
            .that().areAnnotatedWith("org.springframework.data.repository.Repository")  
            .should().resideInAPackage("..infrastructure.adapter.out.persistence.jdbc.")  
            .andShould().haveSimpleNameEndingWith("Repository")
            .andShould().beInterfaces()
            .as("Persistence adapters must be in the 'out.persistence' package and end with 'Adapter'");  
  
    /**  
     * Rule 4: Spring configuration classes must be in the 'config' package.     
     */    
    @ArchTest  
    static final ArchRule configurationClassesShouldBeInConfigPackage = classes()  
            .that().areAnnotatedWith("org.springframework.context.annotation.Configuration")  
            .and().doNotHaveSimpleName("LeaderboardApplication")  
            .should().resideInAPackage("..infrastructure.config..")  
            .as("@Configuration classes must be in the 'config' package");  
  
    /**  
     * Rule 5: Prevent multiple entry points. There will be only one @SpringBootApplication placed in infrastructure     
     * root.  
     */    
    @Test  
    void aSingleSpringBootApplicationShouldExistInTheInfrastructureRoot() {  
        JavaClasses importedClasses = new ClassFileImporter()  
                .importPackages("dev.agustinventura.leaderboard");  
  
        List<JavaClass> applicationClasses = importedClasses.stream()  
                .filter(javaClass -> javaClass.isAnnotatedWith("org.springframework.boot.autoconfigure.SpringBootApplication"))  
                .toList();  
  
        assertThat(applicationClasses).hasSize(1);  
  
        JavaClass mainClass = applicationClasses.getFirst();  
        assertThat(mainClass.getSimpleName()).isEqualTo("LeaderboardApplication");  
        assertThat(mainClass.getPackageName()).isEqualTo("dev.agustinventura.leaderboard.infrastructure");  
    }
}
```

### 5. Conclusión
¡Y listo! Ahora tenemos una estructura de proyecto robusta y, lo más importante, un sistema automático que vigila que nadie se salte las reglas.

Si ejecutas los tests ahora, fallarán, porque los proyectos están vacíos. Al más puro estilo TDD, ya tenemos nuestras pruebas en rojo esperando a que la implementación las ponga en verde.

Ten en cuenta que estas reglas hay que mantenerlas vivas, por ejemplo, cuando añada DTOs crearé nuevas reglas para que estos DTOs acompañen en la paquetería a sus adaptadorers o puedo querer añadir Jackson por ejemplo a las comprobaciones del módulo de domain.

Puedes ver todo el ejemplo en [**este repositorio de GitHub**](https://github.com/agustinventura/leaderboard/tree/feature/002-project_setup).