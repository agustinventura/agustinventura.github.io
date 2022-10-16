title=Nueva API de Fecha y Hora en Java 8
date=2016-06-16
type=post
tags=Java, Date, Time
status=published
~~~~~~
Unos apuntes rápidos sobre la nueva API de fecha y hora en Java 8. Primero, clases fundamentales:
1. LocalDate: La fecha en el contexto local. En una zona horaria determinada.
2. LocalTime: La hora en el contexto local.
3. LocalDateTime: La composición de ambas.

Aquí lo fundamental es que corresponden al contexto local del observador, es decir esa hora es válida para Sevilla pero no para Canarias. La hora y la fecha (por extensión) si la necesito completa se representa mediante una fecha/hora y un offset con respecto a UTC. Por ejemplo, ahora mismo en Sevilla estoy en UTC +02:00 y en Canarias en UTC +01:00. Para representar eso tengo:

1. OffsetTime: Una hora con un Offset.
2. ZonedDateTime: Una fecha con una zona horaria que a su vez contiene un Offset.

Por último hay otras dos clases MUY interesantes:

1. Duration: Una cantidad de tiempo en horas. Es decir, 34.5 sgs, 173.25 horas, etc...
2. Period: Una cantidad de tiempo en fecha. Por ejemplo 3 días o 1.5 años, etc... Lo guay de esto es que maneja días conceptuales. Mientras que si uso Duration y añado un día son siempre 24 horas, Period tiene en cuenta, por ejemplo, el cambio horario, y si añado un día y ese día tiene 23 horas (porque ha habido que restar una hora), solo añade 23.

Por último, la integración con la persistencia. El problema que hay es que Java 8 es más moderno que la especificación de persistencia (JPA 2.1), así que oficialmente no hay soporte para estos tipos, pero, si se usa Hibernate como proveedor de JPA (cosa que siempre hago porque después de probar varios es el que mejor funciona), [basta con añadir una dependencia](http://docs.jboss.org/hibernate/orm/5.1/userguide/html_single/Hibernate_User_Guide.html#basic-datetime) y hay soporte automático:

```prettyprint
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-java8</artifactId>
    <version>${hibernate.version}</version>
</dependency>
```
