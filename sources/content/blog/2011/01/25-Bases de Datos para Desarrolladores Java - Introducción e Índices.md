title=Bases de Datos para Desarrolladores Java - Introducción e Índices
date=2011-01-25
type=post
tags=Base de Datos,Java,Programación
status=published
~~~~~~
En general en una aplicación Java cualquiera los problemas empiezan desde abajo, con el diseño de la base de datos. He visto (y trabajo) con bases de datos en las que una tabla tiene 5 campos de primary key y uno solo de información. Que esto es un desperdicio se ve a simple vista. Después vienen los parches a nivel superior (en Java) y se termina yendo al infierno el rendimiento de la aplicación.
Lo bonito, y lo malo del diseño de base de datos es que no te terminas dando cuenta de que esta mal hasta que la aplicación esta avanzada, empieza a crecer y en ese momento es tarde para cambiarlo. Vamos, que es un infierno.

Lo mejor de toda esta historia es que cada uno lo ve de su manera... efectivamente, para cada guía, suele haber una contraguía, así que vamos a ver si <strong>todo el que lea esto se anima a discutir lo que aquí digo.</strong> (gracias :))
En general hay una serie de guías que <strong>no </strong>te enseñan en la facultad, estas guías te las van dando la experiencia y el instinto (recordando siempre que hay gente que no aprende ni a palos y que además tiene el instinto atrofiado), pero hace tiempo que ví en Stack Overflow un <a title="Database development mistakes" href="http://stackoverflow.com/questions/621884/database-development-mistakes-made-by-application-developers" target="_blank">resumen bastante bueno</a> y descubrí también un sitio dedicado a tratar el tema en más profundidad, <a title="Use the Index, Luke" href="http://use-the-index-luke.com/" target="_blank">Use the Index, Luke</a>.

Voy a ver si escribo un par de artículos tratando los temas que considero importantes o interesantes para un desarrollador Java. Por tanto, no voy a hablar de SQL (que también puede ser que las consultas estén mal construidas), ya que asumo que se usa un Hibernate o cualquier implementación de JPA, hecha por gente más lista que yo. Voy a hablar del diseño de la base de datos y la forma de sacarle el mayor partido posible a la misma.

Un breve recordatorio de la teoría más esencial y fundamental para esto.

<ol>
	<li>Base de Datos: Para mí es un conjunto de datos estructurado e interrelacionado. Punto. Para más detalles, la <a title="Base de Datos, Wikipedia." href="http://es.wikipedia.org/wiki/Base_de_datos" target="_blank">wikipedia</a>.</li>
	<li>Índices: La información de la base de datos esta ordenada (estructurada) siguiendo unos determinados índices. Estos son implícitos (clave primaria) o explícitos (create index...). La utilidad se puede examinar pensando en una guía de teléfonos. La guía de teléfonos (en papel :P) se encuentra indexada por primer apellido. Sin embargo en una base de datos podemos indexar por primer apellido, segundo apellido, nombre o incluso número de teléfono, según nos sea conveniente. ¿Para qué es útil ésto? Para nada, excepto para flexibilizar el acceso a la información, lo que es lo mismo, poder buscar (más rápido, más eficientemente) por distintos criterios. Normalmente en la guía de teléfonos buscábamos por primer apellido, después por segundo apellido y por último, por nombre. En una aplicación normalmente se pide buscar por cualquiera de ellos o combinación.</li>
	<li>Por último la dicotomía de siempre... memoria vs. ciclos (y potencialmente más memoria). Un índice es un <a title="Wikipedia, árbol binario" href="http://es.wikipedia.org/wiki/Arbol_binario" target="_blank">B-Tree</a> normalmente, por tanto mantenerlo ocupa espacio en disco y, naturalmente, hay que calcularlo y mantenerlo actualizado. Por tanto no puedo indexar todo lo que quiera o lo que me gustaría. En el ejemplo de la guía, es como si tuviéramos un tomo por cada uno de los criterios de ordenación (cosa que podríamos hacer, pero... buff..., ¿no?). Aparte la guía hay que hacerla nueva todos los años.</li>
</ol>

Y aquí va la primera perla de sabiduría del artículo de Stack Overflow, uso apropiado de índices:

<ul>
	<li>Las claves externas (fóraneas, o como se le diga en español) deben estar siempre indexadas.</li>
	<li>Si se usa un campo en una cláusula <em>where</em> debería estar indexado.</li>
	<li>En el caso anterior deberías plantearte tener índices de varias columnas  según las consultas que hagas.</li>
</ul>

Eso es todo, de cosecha propia un par de recomendaciones:

<ul>
	<li>Las claves primarias están siempre indexadas, no hace falta que se cree un índice sobre ellas (la guía de teléfonos YA viene indexada por apellidos y nombre).</li>
	<li>No siempre debes tener un índice en un campo que se usa en un <em>where</em>, puede ser que solo lo uses en una consulta que se ejecuta raramente y no te compense, o cualquier otro motivo. Es decir, conoce cuando saltarte la regla.</li>
</ul>

Poco más, a ver si se me van ocurriendo más cosas o alguien comenta algo.

<span style="font-size: small;"><span style="line-height: 24px;">P.D.: No, no aparezco en la guía de teléfonos, marqué la opción de no aparecer :)</span></span>