title=Logging de consultas y parametros de Hibernate
date=2017-03-27
type=post
tags=Java, Hibernate, Logging
status=published
~~~~~~
Una de las funcionalidades básicas de [Hibernate](http://hibernate.org/orm/) es abstraer la base de datos, pero sin embargo en tiempo de desarrollo resulta bastante útil controlar las consultas que va generando el motor así como sus parámetros.
Desde las primeras versiones Hibernate tiene una propiedad, *show_sql* que muestra estas consultas por consola. Esto tiene dos desventajas, la primera que usa la consola y la segunda que para habilitarlo y deshabilitarlo se depende de un archivo de configuración específico (normalmente el propio de Hibernate o incluso una clase Java si se esta utilizando la configuración Java de Spring). Además este parámetro tan sólo muestra las consultas y no los parámetros de las mismas.
La solución idónea pasa por utilizar el sistema de logging estándar que se utilice en la aplicación, así se puede mostrar en consola o registrar en un archivo o cualquier otro tipo de solución y además su activación y desactivación se hace en el sitio lógico, el archivo de configuración de logs de la aplicación.
Otra ventaja es que, además, con su configuración oportuna se pueden logar también los parámetros de las consultas (algo muy útil para contrastar con nuestro cliente SQL favorito).
Para poder mostrar estos logs hay dos loggers propios de Hibernate que configurar:

1. org.hibernate.SQL: Se encarga de mostrar las consultas.
2. org.hibernate.type.descriptor.sql.BasicBinder: Hay soluciones que proponen quedarse al nivel de type, pero en ese caso el log muestra toda la información relativas a tipos de Hibernate, no solo los valores de los parámetros. Con este logger se muestran únicamente éstos.

Y un ejemplo de configuración para log4j:
```prettyprint
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE log4j:configuration SYSTEM "log4j.dtd" >
<log4j:configuration>

	<appender name="hibernate_log" class="org.apache.log4j.ConsoleAppender">
		<layout class="org.apache.log4j.PatternLayout">
			<param name="ConversionPattern" value="%d{ABSOLUTE} %p %c - %m%n" />
		</layout>
	</appender>

	<appender name="stdout" class="org.apache.log4j.ConsoleAppender">
		<layout class="org.apache.log4j.PatternLayout">
			<param name="ConversionPattern" value="%d{ABSOLUTE} %p %c - %m%n" />
		</layout>
	</appender>
	
	<logger name="org.hibernate.SQL">
		<level value="trace" />
		<appender-ref ref="hibernate_log" />
	</logger>

	<logger name="org.hibernate.type.descriptor.sql.BasicBinder">
		<level value="trace" />
		<appender-ref ref="hibernate_log" />
	</logger>
	
	<root>
		<priority value="error" />
		<appender-ref ref="stdout" />
	</root>
</log4j:configuration>
```
