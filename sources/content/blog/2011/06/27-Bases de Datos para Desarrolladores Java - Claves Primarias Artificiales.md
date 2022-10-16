title=Bases de Datos para Desarrolladores Java - Claves Primarias Artificiales
date=2011-06-27
type=post
tags=Base de Datos,Java
status=published
~~~~~~
La teoría pura y dura de base de datos dice que para una entidad determinada, tendremos varias claves candidatas, que son aquellas que identifican únicamente a la entidad y la clave primaria se escoge de entre ellas como la menor.
Para un usuario podemos tener como claves candidatas: DNI, nombre de usuario, nombre y apellidos. Nombre y apellidos se descarta (por larga) y ya tenemos que escoger entre DNI y nombre de usuario. A gusto.

El problema de esto es cuando vamos arrastrando relaciones. Por ejemplo, un post podría tener como clave primaria su título, y un comentario el título y el autor, ¿verdad?

¿Qué pasa si cambia el título? Pues que hay que modificar también sus referencias. ¿Y si cambia el usuario que escribió el comentario?¿Debemos dejar que un usuario modifique su nombre? Habría que usar un "ON UPDATE CASCADE" o algún artefacto similar.

¿Y sí en vez de esto cada tabla tiene un identificador único artificial? Un número autogenerado que identifique unívocamente cada una de las filas en la base de datos. La mayoría de bases de datos tienen algún sistema para gestionar esto, en MySQL existen los auto_increment, en Oracle los sequence, etc... En caso de que no haya, siempre se puede utilizar una tabla para generarlos.

Las ventajas son claras, si el post tiene un identificador 135 y el usuario un identificador 7, el identificador del comentario será (135, 7). El usuario se podrá cambiar el nombre tantas veces como desee sin afectar al resto de los datos, e incluso el post podrá cambiar de título sin más. Y ya en ello, ¿no sería mejor que el comentario tuviera su propio id único? Imaginemos por ejemplo que un comentario contesta a otro, si el id del comentario fuera (135, 7), la clave externa sobre la tabla tendría que tener dos campos (por ejemplo, id_post_comentario_respuesta, id_usuario_comentario_respuesta), con un id único, basta con uno solo (id_comentario_respuesta).

Como todo, esta solución tiene críticas. La más importante es que la base de datos deja de estar en <a title="Primera Forma Normal" href="http://es.wikipedia.org/wiki/1NF" target="_blank">Primera Forma Normal</a>, es decir, puedo tener dos veces al mismo usuario, Agustín con Id 2 y Agustín de nuevo con Id 3, y por tanto tengo que introducir algún otro artificio, como que "la que sería clave primaria", ahora relegada a clave candidata, sea unique.

Esto me obliga a incluir una segunda declaración de índice, etc... En el <a title="Claves Primarias Artificiales en la Wikipedia" href="http://en.wikipedia.org/wiki/Surrogate_key" target="_blank">artículo de la wikipedia</a> se pueden consultar más detalles (en inglés, lo siento).

En general, en mi experiencia, suele ser más que conveniente tenerlo,  ya que nunca sabes cuanto puede crecer la base de datos y en consecuencia cada vez vas teniendo más "sucio" el esquema de base de datos, arrastrando claves primarias compuestas y los "on update cascade", o te ves forzado a impedir que el usuario cambie su nombre, y otros tipos de restricciones absurdas.