---
title: Secretos en desarrollo local con Spring Boot
date: 2024-02-11
tags:
  - Java
  - Spring Boot
  - Secrets
---
Cuando trabajamos con recursos externos a nuestra aplicación (bases de datos, APIs con algún tipo de autenticación, etc...) es bastante habitual tener algún elemento como un nombre de usuario y contraseña o un token que no queremos publicar junto con el código de nuestra aplicación.
Por ejemplo, en el artículo de [Headers y HTTP Interface](https://www.agustinventura.dev/posts/headers-y-spring-boot-http-interface/) usábamos un API key en la cabecera para acceder al servidor.

Esta API key en nuestro ejemplo esta en el application.properties:
```
spring.main.web-application-type=none
logging.level.org.springframework.web=TRACE
song-server.base.url=http://localhost:3000
song-server.api-key=mytoken
```
Y como tal se puede filtrar (y se ha filtrado a GitHub). Aquí dá igual porque es un dato de prueba que no sirve para nada, pero queda claro el riesgo de que filtremos inadvertidamente datos privados como URLs de servidores y tokens, usuarios o contraseñas (secretos en general).

Otro de los problemas es que esos datos serán distintos según el entorno de ejecución, es decir, mytoken será válido para nuestro servidor de desarrollo, pero lógicamente en producción será otro dato (que incluso podemos recuperar en tiempo de ejecución de algo como [Vault](https://www.vaultproject.io/) o [AWS Secrets Manager](https://aws.amazon.com/es/secrets-manager/)).

Tenemos entonces dos problemas:
1. Como evitar filtrar secretos.
2. Como utilizar distintos secretos según el entorno.

## Como evitar filtrar secretos
La solución estandarizada en otros lenguajes y frameworks es utilizar [archivos .env](https://www.codementor.io/@parthibakumarmurugesan/what-is-env-how-to-set-up-and-run-a-env-file-in-node-1pnyxw9yxj) como en JavaScript y Node.

Desde Spring Boot 2.4 tenemos una utilidad no muy conocida como es [Spring Config Import](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.external-config.files.importing) que, hay que admitirlo, no tiene un nombre tan molón como archivos .env pero hace exactamente lo mismo.

Siguiendo con el ejemplo, vamos a llevarnos las propiedades de configuración de song server (song-server.base.url y song-server.api-key) a un archivo aparte llamado secrets.properties.

Creamos secrets.properties en src/main/resources (junto con application.properties):
```
song-server.base.url=http://localhost:3000
song-server.api-key=mytoken
```
Y lo importamos en application.properties:
```
spring.config.import=secrets.properties
spring.main.web-application-type=none
logging.level.org.springframework.web=TRACE
```
Y ahora, **lo más importante**, lo añadimos añadimos a .gitignore:
```
**/secrets.properties
```

## Como utilizar distintos secretos según el entorno
Con esto ya tenemos el archivo secrets.properties únicamente en local por lo que si construimos el jar de la aplicación en un entorno de CI/CD este jar no contendrá el archivo secrets.properties. Podemos simular esto generando nuestro jar con:
```bash
./gradlew clean bootJar
```
Y una vez creado el jar en /build/libs, lo podemos abrir con un gestor de archivos zip y borrar el secrets.properties. Con esto, podemos probar a arrancarlo:
```
java -jar playlisthistory-0.0.1-SNAPSHOT.jar
```
Nos encontraremos con un fallo similar a éste:
```
13:28:54.667 [main] ERROR org.springframework.boot.diagnostics.LoggingFailureAnalysisReporter -- 

***************************
APPLICATION FAILED TO START
***************************

Description:

Config data resource 'class path resource [secrets.properties]' via location 'secrets.properties' does not exist

```
Esto tiene todo el sentido, Spring entiende que el archivo secrets.properties es obligatorio y por tanto se niega a arrancar si no se lo proporcionamos, así que lo primero es marcarlo como optional en la importación en application.properties:
```
spring.config.import=optional:secrets.properties
spring.main.web-application-type=none
logging.level.org.springframework.web=TRACE
```
Una vez marcado como optional, si intentamos arrancar la aplicación, veremos algo así:
```
2024-02-11T13:40:57.637+01:00  INFO 63006 --- [           main] d.a.p.PlayListHistoryApplication         : Starting PlayListHistoryApplication using Java 21.0.2 with PID 63006 (/home/vagustin/Development/Projects/Personal/playlisthistory/build/libs/playlisthistory-0.0.1-SNAPSHOT.jar started by vagustin in /home/vagustin/Development/Projects/Personal/playlisthistory/build/libs)
2024-02-11T13:40:57.641+01:00  INFO 63006 --- [           main] d.a.p.PlayListHistoryApplication         : No active profile set, falling back to 1 default profile: "default"
2024-02-11T13:40:58.179+01:00  WARN 63006 --- [           main] s.c.a.AnnotationConfigApplicationContext : Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'restClient' defined in dev.agustinventura.playlisthistory.PlayListHistoryApplication: Unexpected exception during bean creation
2024-02-11T13:40:58.187+01:00  INFO 63006 --- [           main] .s.b.a.l.ConditionEvaluationReportLogger : 

Error starting ApplicationContext. To display the condition evaluation report re-run your application with 'debug' enabled.
2024-02-11T13:40:58.205+01:00 ERROR 63006 --- [           main] o.s.boot.SpringApplication               : Application run failed
...
Caused by: java.lang.IllegalArgumentException: Could not resolve placeholder 'song-server.base.url' in value "${song-server.base.url}"
```
Es decir, la aplicación arranca pero falla porque no encuentra el valor para song-server.base.url (ni para song-server.api-key, claro). Una de las mejores cosas de Spring es que nos permite especificar [propiedades de configuración como parámetros](https://docs.spring.io/spring-boot/docs/1.2.0.RELEASE/reference/html/boot-features-external-config.html), así que podemos lanzar la aplicación:
```
java -jar -Dsong-server.base.url=http://localhost:3000 -Dsong-server.api-key playlisthistory-0.0.1-SNAPSHOT.jar
```
Y ya funcionaría, así que podríamos incluir estos parámetros dentro de nuestro shell script que lanza la aplicación/Docker/Kubernetes o la tecnología que utilicemos. Esto siempre y cuando sean secretos estáticos o que podamos inyectar a través del entorno, si quisiéramos hacer una resolución dinámica, podríamos optar por utilizar [perfiles](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.profiles) y tener uno de dev que los resuelva estáticamente con el secrets.properties y otro de prod que cree un bean que ya en tiempo de ejecución vea cómo tiene que resolverlo. Algo más complejo, pero entra dentro de lo normal. 

Y por supuesto, tienes el código en [GitHub](https://github.com/agustinventura/playlisthistory).