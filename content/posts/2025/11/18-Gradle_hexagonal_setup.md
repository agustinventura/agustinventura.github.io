---
title: Configuración de Gradle con Arquitectura Hexagonal
date: 2025-11-18
tags:
  - Development
  - Gradle
  - JUnit
  - Java
  - Spring Boot
---

El proyecto va creciendo. Tenemos ya cinco módulos con responsabilidades muy definidas: tres representan la aplicación según la arquitectura hexagonal (`domain`, `application` e `infrastructure`) y dos están dedicados a las pruebas (`architecture-tests` y `acceptance-tests`).
Sin embargo, nuestro `build.gradle.kts` raíz nos impone una configuración única, propagando el plugin de gestión de dependencias de Spring (`io.spring.dependency-management`) y su BOM a **todos** los módulos. De una manera sutil, estamos contaminando nuestro dominio puro y nuestra aplicación con detalles de un framework (Spring). Además, tenemos las versiones de las dependencias dispersas por varios archivos.

¿Podemos solucionar estos problemas y dejar una base sólida para el futuro? La respuesta es sí.

# Gestionando las dependencias con Version Catalogs
Empezando en orden inverso, podemos centralizar la gestión de dependencias de una forma directa con un mecanismo llamado [Gradle Version Catalog](https://docs.gradle.org/current/userguide/version_catalogs.html).

En el directorio `gradle` (donde está el wrapper), creamos un archivo `libs.versions.toml`. Aquí definiremos versiones, librerías y plugins. Atención, como vamos buscando desacoplar de Spring, vamos a tener que especificar la versión de todas nuestras dependencias, incluyendo algunas que antes derivábamos al plugin de gestión de dependencias de Spring como la de Junit.

Este es nuestro archivo completo:
```toml
[versions]  
springBoot = "3.5.7"  
springDependencyManagement = "1.1.7"  
  
junit = "5.14.1"  
junit-platform = "1.14.1"  
mockito = "5.20.0"  
assertj = "3.27.6"  
  
archunit = "1.4.1"  
cucumber = "7.18.0"  
restAssured = "5.4.0"  
  
[libraries]  
spring-boot-starter-actuator = { module = "org.springframework.boot:spring-boot-starter-actuator" }  
spring-boot-starter-data-jdbc = { module = "org.springframework.boot:spring-boot-starter-data-jdbc" }  
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web" }  
spring-boot-starter-test = { module = "org.springframework.boot:spring-boot-starter-test" }  
spring-boot-devtools = { module = "org.springframework.boot:spring-boot-devtools" }  
  
flyway-core = { module = "org.flywaydb:flyway-core" }  
flyway-postgresql = { module = "org.flywaydb:flyway-database-postgresql" }  
postgresql = { module = "org.postgresql:postgresql" }  
  
spring-kafka = { module = "org.springframework.kafka:spring-kafka" }  
spring-kafka-test = { module = "org.springframework.kafka:spring-kafka-test" }  
  
junit-jupiter = {module = "org.junit.jupiter:junit-jupiter", version.ref = "junit"}  
junit-platform-launcher = {module = "org.junit.platform:junit-platform-launcher", version.ref = "junit-platform" }  
  
assertj = { module = "org.assertj:assertj-core", version.ref = "assertj" }  
mockito = { module = "org.mockito:mockito-core", version.ref = "mockito" }  
  
archunit = { module = "com.tngtech.archunit:archunit-junit5", version.ref = "archunit" }  
  
cucumber-java = { module = "io.cucumber:cucumber-java", version.ref = "cucumber" }  
cucumber-spring = { module = "io.cucumber:cucumber-spring", version.ref = "cucumber" }  
cucumber-junit-engine = { module = "io.cucumber:cucumber-junit-platform-engine", version.ref = "cucumber" }  
rest-assured = { module = "io.rest-assured:rest-assured", version.ref = "restAssured" }  
  
  
[plugins]  
spring-boot = { id = "org.springframework.boot", version.ref = "springBoot" }  
spring-dependency-management = { id = "io.spring.dependency-management", version.ref = "springDependencyManagement" }
```

El documento es bastante fácil de entender, aquí definimos todas las dependencias del proyecto dividido en tres secciones:
- Versions: Las versiones de las dependencias.
- Libraries: Las dependencias en sí, nótese el campo `version.ref`que apunta a la versión definida.
- Plugins: Dependencias a plugins de Gradle y no librerías como tal.

Ahora podemos actualizar el `build.gradle.kts` del módulo `infrastructure`. Fíjate en cómo usamos `libs` para referenciar las dependencias:

```kotlin
plugins {  
    id("org.springframework.boot")  
    id("java")  
}  
  
dependencies {  
    implementation(project(":application"))  
    implementation(libs.spring.boot.starter.actuator)  
    implementation(libs.spring.boot.starter.data.jdbc)  
    implementation(libs.spring.boot.starter.web)  
    implementation(libs.flyway.core)  
    implementation(libs.flyway.postgresql)  
    implementation(libs.spring.kafka)  
    developmentOnly(libs.spring.boot.devtools)  
    runtimeOnly(libs.postgresql)  
    testImplementation(libs.spring.boot.starter.test)  
    testImplementation(libs.spring.kafka.test)  
}
```

Si por ejemplo reutilizamos la dependencia de Spring Boot Test en el módulo `acceptance-tests` lo añadimos al `build.gradle.kts` así:

```kotlin
plugins {  
    `java-library`  
}  
  
dependencies {  
    testImplementation(project(":infrastructure"))  
    testImplementation(libs.spring.boot.starter.test)  
    testImplementation(libs.cucumber.java)  
    testImplementation(libs.cucumber.spring)  
    testRuntimeOnly(libs.cucumber.junit.engine)  
    testImplementation(libs.rest.assured)  
}  
  
tasks.withType<Test> {  
    useJUnitPlatform()  
}
```

Ojo, que hay dos inconvenientes:

Primero, este sistema no invalida la resolución de dependencias convencional, es decir, en cualquier módulo podemos seguir utilizando algo como `testImplementation("io.rest-assured:rest-assured:5.4.0")` y funcionaría y utilizaría esa versión de `rest-assured`en ese módulo.

Segundo, hay que ser un poco más específico en el módulo raíz para definir las dependencias. Al definirlas en el bloque `subprojects` no hay acceso a `libs` que solo esta disponible en el proyecto raíz. Pero bueno, ¿qué significa ésto? Pues poca cosa realmente, que hay que anteponer `rootProject`a todas las dependencias.
Así queda el `build.gradle.kts` del módulo raíz.

```kotlin
import io.spring.gradle.dependencymanagement.dsl.DependencyManagementExtension  
import org.springframework.boot.gradle.plugin.SpringBootPlugin  
  
plugins {  
    alias(libs.plugins.spring.boot) apply false  
    alias(libs.plugins.spring.dependency.management) apply false  
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
        "testImplementation"(rootProject.libs.junit.jupiter)  
        "testRuntimeOnly"(rootProject.libs.junit.platform.launcher)
        "testImplementation"(rootProject.libs.assertj)  
        "testImplementation"(rootProject.libs.mockito)  
    }  
}
```

# Limpiando el Build raíz
Aquí viene la parte interesante. Vamos a refactorizar el `build.gradle.kts` raíz para:
1. Eliminar la imposición de Spring en módulos que no lo necesitan (`domain`, `application`).
2. Eliminar Mockito de módulos que no lo usan.
3. Mantener una configuración base de Java y JUnit para todos.

```kotlin
plugins {  
    alias(libs.plugins.spring.boot) apply false  
    alias(libs.plugins.spring.dependency.management) apply false  
}  
  
subprojects {  
    apply(plugin = "java")  
  
    group = "dev.agustinventura"  
    version = "0.0.1-SNAPSHOT"  
  
    extensions.configure<JavaPluginExtension> {  
        toolchain {  
            languageVersion.set(JavaLanguageVersion.of(21))  
        }  
    }  
    repositories {  
        mavenCentral()  
    }  
  
    dependencies {  
        "testImplementation"(rootProject.libs.junit.jupiter)  
        "testRuntimeOnly"(rootProject.libs.junit.platform.launcher)
        "testImplementation"(rootProject.libs.assertj)  
    }  
}  
  
configure(  
    listOf(  
        project(":domain"),  
        project(":application"),  
        project(":infrastructure")  
    )  
) {  
    dependencies {  
        "testImplementation"(rootProject.libs.mockito)  
    }  
}
```

## ¿Qué hemos conseguido?

Al eliminar `io.spring.dependency-management` del bloque `subprojects`:
1. **Domain y Application:** Ahora son módulos Java puros. Usan las versiones de JUnit y AssertJ que definimos explícitamente en el `libs.versions.toml`. No saben nada de Spring.
2. **Infrastructure:** ¿Por qué funciona sin añadirle manualmente el plugin de gestión de dependencias? Porque el plugin `org.springframework.boot` (que sí aplicamos en su propio `build.gradle.kts`) aplica transitivamente el plugin de Dependency Management. Es decir, `infrastructure` sigue aprovechando el BOM de Spring.

## Configuración de Acceptance Tests

El módulo `acceptance-tests` es particular. No es una aplicación Spring Boot (no tiene el plugin `org.springframework.boot` ni clase main), pero **sí** necesita las versiones gestionadas por Spring para sus tests (Cucumber con Spring, RestAssured, etc.).
Como quitamos la configuración global del raíz, ahora debemos devolvérsela explícitamente en su `build.gradle.kts`:

```kotlin
import io.spring.gradle.dependencymanagement.dsl.DependencyManagementExtension  
import org.springframework.boot.gradle.plugin.SpringBootPlugin  
  
plugins {  
    java  
    id("io.spring.dependency-management")  
}  
  
configure<DependencyManagementExtension> {  
    imports {  
        mavenBom(SpringBootPlugin.BOM_COORDINATES)  
    }  
}  
  
dependencies {  
    testImplementation(project(":infrastructure"))  
    testImplementation(libs.spring.boot.starter.test)  
    testImplementation(libs.cucumber.java)  
    testImplementation(libs.cucumber.spring)  
    testRuntimeOnly(libs.cucumber.junit.engine)  
    testImplementation(libs.rest.assured)  
}  
  
tasks.withType<Test> {  
    useJUnitPlatform()  
}
```

¡Y listo! Hemos pasado de una configuración monolítica y acoplada a una estructura granular donde cada módulo tiene exactamente lo que necesita, con todas las versiones centralizadas en un único fichero TOML, planteando una base sólida y limpia para el resto del desarrollo. ¿Qué te parece?

Como siempre lo tienes en su propia rama en [GitHub](https://github.com/agustinventura/leaderboard/tree/feature/004-gradle_configuration_cleanup)