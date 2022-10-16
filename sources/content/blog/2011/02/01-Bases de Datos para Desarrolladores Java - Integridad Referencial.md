title=Bases de Datos para Desarrolladores Java - Integridad Referencial
date=2011-02-01
type=post
tags=Base de Datos,Java,Programación
status=published
~~~~~~
Como el entorno de desarrollo se ha caído y llevo dos horas aburrido, sigo.

Segundo Ítem: Usar siempre <strong>SIEMPRE</strong> la integridad referencial.

O lo que es lo mismo, si usamos MySQL <strong>NO </strong>usar MyIsam, ya que no tiene soporte para integridad referencial.

Hay gente que dice que trabajar sin integridad referencial es más rápido y cómodo. Es verdad, pero al final es como dispararse en el pie. Muchas veces la integridad referencial te salva de cometer errores de calado. Por ejemplo, si borramos los usuarios de un foro, ¿quién sale como autor de sus posts? Por tanto no podemos "borrar" los usuarios, hay que recurrir a un "borrado lógico", es decir, un campo activo o borrado o como se le quiera llamar. El inconveniente, que puede ser que nunca borremos.

Otra ventaja colateral es que las claves ajenas, suelen estar siempre indexadas, por tanto en consultas de join, habrá un incremento del rendimiento frente a sistemas como MyIsam.

Más ventajas (no estrictamente derivadas de la integridad referencial, sino que es aplicable a todo el diseño de la base de datos), es las restricciones sobre datos. Supongamos que tenemos un formulario para introducir nuevos posts y que en el artefacto encargado de realizar ese insert, realizamos las validaciones oportunas: campos que no estén en blanco, que exista el usuario que realiza el post, etc... Supongamos ahora que queremos hacer otro formulario similar en otra zona, podemos repetir el código de las validaciones, o podríamos concentrar esas validaciones en la base de datos y están en un único sitio. Además en general la sintaxis es mucho menos engorrosa y más natural en SQL. Por otra parte si en el futuro otro desarrollador realiza otro formulario contra esa tabla, tendrá las restricciones de manera explícita, sin tener que buscar código anterior que utilice dicha tabla para comprobar las restricciones.

Para terminar el asunto, si no queremos integridad referencial (que puede ser), a lo mejor es que ni siquiera necesitamos una base de datos SQL. Existen multitud de sistemas <a title="Wikipedia, NoSQL" href="http://es.wikipedia.org/wiki/NoSQL" target="_blank">NoSQL</a> enfocados a sistemas sin integridad referencial: <a title="MongoDB" href="http://www.mongodb.org/" target="_blank">MongoDB</a>, <a title="Apache Cassandra" href="http://cassandra.apache.org/" target="_blank">Cassandra</a>, <a title="Apache CouchDB" href="http://couchdb.apache.org/" target="_blank">CouchDB</a>