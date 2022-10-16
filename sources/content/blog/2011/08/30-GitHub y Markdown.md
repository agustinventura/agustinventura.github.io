title=GitHub y Markdown
date=2011-08-30
type=post
tags=Git,GitHub,Markdown,Programación,Tools of the Trade,tutorial
status=published
~~~~~~
Si entro en el repositorio PruebaGit que cree en <a title="Git, EGit y GitHub." href="http://www.aguasnegras.es/?p=201" target="_blank">este artículo</a>, GitHub es tan amable de avisarme de que no encuentra un archivo README.

En primer lugar, ¿qué es un README? Un archivo README contiene información genérica sobre el proyecto, como instalar, como configurar, como usar, licencia, contacto con el autor, bugs, etc... Para más detalles esta el artículo de la <a title="Archivo README, Wikipedia (inglés)" href="http://en.wikipedia.org/wiki/README" target="_blank">wikipedia</a> (en inglés, el artículo en español es bastante malo).

Bien, pues GitHub te recomienda poner un archivo README en la raíz de tu proyecto, y para ello puedes usar varios lenguajes de maquetado. Un lenguaje de maquetado es un archivo de texto plano (normal y corriente) pero que usa una síntaxis especial y específica para poder pasarle una herramienta y convertirlo a HTML. Yo voy a utilizar <a title="Markdown" href="http://daringfireball.net/projects/markdown/" target="_blank">Markdown</a>.

La gracia viene en que voy a crear un archivo README.markdown y GitHub lo podrá convertir al vuelo en un HTML, de esta manera el que utilice un navegador web para explorar GitHub podrá ver una descripción de mi proyecto en HTML, que siempre queda mejor que en texto plano.

Como ya digo, voy a crear el README del proyecto PruebaGit y voy a incluir los siguientes datos: Descripción del proyecto, como instalar y contacto con el autor, con esos tres apartados creo que ya es suficiente.

Click con el botón derecho en PruebaGit &gt; New... &gt; File &gt; Name: README.markdown. Con esto se abre el archivo en blanco.

A continuación voy a ir describiendo como voy usando el lenguaje Markdown para darle formato al texto:

<ol>
	<li>Título: Prueba Git. Para forzar que sea el primer encabezado, lo subrayo con =</li>
	<li>Para definir otro párrafo, basta con dejar una línea en blanco, o solo rellena con espacios o con tabuladores (y supongo que cualquier combinación de ellos).</li>
	<li>Instalación: Éste epígrafe es de tipo título 2, así que lo subrayo con -</li>
	<li>Los items de instalación son una lista, basta con comenzar cada item con -, * ó +. Con esto he tenido problemas (como se puede ver en el repositorio). La lista tiene que estar separada del párrafo anterior por una línea en blanco, si no, no la estima como válida.</li>
	<li>Contacto, de nuevo título 2, así que se subraya con -</li>
	<li>Enlaces: Los enlaces funcionan poniendo entre corchetes el título del enlace y a continuación, entre paréntesis, la url del enlace: [AguasNegras](http://www.aguasnegras.es/blog/?p=201).</li>
	<li>Los enlaces de mail, igual, título entre corchetes y entre paréntesis la dirección de mail: [agustinventura](http://www.aguasnegras.es/blog/?p=201)</li>
</ol>

Y eso es todo, los resultados se pueden ver <a title="README de PruebaGit en GitHub." href="https://github.com/agustinventura/PruebaGit/blob/master/README.markdown" target="_blank">aquí</a>. Como detalle curioso e interesante, podemos decir que GitHub automáticamente te muestra el README en la página principal del repositorio del proyecto (<a title="Repositorio de PruebaGit." href="https://github.com/agustinventura/PruebaGit" target="_blank">ejemplo</a>).