---
title: Secretos en desarrollo local con Spring Boot
date: 2024-01-19
tags:
  - Java
  - Spring Boot
  - Secrets
draft: true
---

Cuando trabajamos con recursos externos a nuestra aplicación (bases de datos, APIs con algún tipo de autenticación, etc...) es bastante habitual tener algún elemento como un nombre de usuario y contraseña o un token que no queremos publicar junto con el código de nuestra aplicación.
Dejando de lados posibles modificaciones de la configuración, esta suele ser la principal diferencia entre los distintos entornos de ejecución de nuestra aplicación.
La manera más habitual de gestionar estos entornos en Spring Boot es utilizar diferentes perfiles (profiles), por ejemplo, el perfil development para la máquina de desarrollo local y el perfil production para el entorno de producción. Además, estos valores que se diferencian por perfiles normalmente se almacenan en los archivos de configuración de la aplicación, siendo esto tan frecuente que Spring Boot nos permite cargar automáticamente archivos de configuración en función del perfil con el que se esté ejecutando la aplicación. Por ejemplo, podríamos tener tres archivos de configuración:
- application.yml: Con las propiedades generales de la aplicación (por ejemplo, que por defecto el perfil por defecto sea local)
- application-development.yml: Con las propiedades específicas de desarrollo local, como nuestro usuario y contraseña de la base de datos local.
- application-production.yaml: Con las propiedades de producción, como obtener el usuario y la contraseña con [AWS Secrets Manager](https://docs.spring.io/spring-cloud-config/reference/server/environment-repository/aws-secrets-manager.html)

En este caso tenemos la circunstancia de que si utilizamos las propiedades por defecto de [Spring Data JPA](https://spring.io/projects/spring-data-jpa/), por ejemplo para PostgreSQL, en local, podemos subirlas inadvertidamentes con el código de nuestra aplicación a git. Me explico, para configurar la conexión a la base de datos tendríamos que añadir algo tal que así a nuestro application-development.yml:
```yml
spring:
  datasource:
    driver-class-name: org.postgresql.Driver
    username: user
    password: pass
    url: jdbc:postgresql://localhost:5432/myapp
```
Si subimos este archivo (como es habitual), filtramos el usuario y contraseña de base de datos, que si bien no es un gran problema porque es local, puede que sea una instancia compartida o que tengamos cualquier otro problema.
Ante esta situación tenemos dos opciones:

Podemos cargar los datos sensibles de variables de entorno, es decir, definir los datos sensibles tal que así:
```bash
export DB_USER=user
export DB_PASS=pass
``` 

Y nuestro archivo application-development.yml así:
```yml
spring:
  datasource:
    driver-class-name: org.postgresql.Driver
    username: ${DB_USER}
    password: ${DB_PASSWORD}
    url: jdbc:postgresql://localhost:5432/myapp
```

Esta opción esta bien pero nos obliga a estar pendientes de si tenemos las variables de entorno definidas, si tenemos distintos proyectos, tenemos que usar distintos nombres de variables de entorno, etc... Digamos que es poco escalable (aunque puede tener su sentido para inyectar propiedades por ejemplo en el entorno de producción).

Afortunadamente hay otra opción