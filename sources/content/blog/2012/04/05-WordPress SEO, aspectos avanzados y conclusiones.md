title=WordPress SEO, aspectos avanzados y conclusiones.
date=2012-04-05
type=post
tags=Programación,SEO,Tools of the Trade,WordPress,tutorial
status=published
~~~~~~
Sigo con <a title="WordPress SEO Tutorial" href="http://yoast.com/articles/wordpress-seo/" target="_blank">el artículo de Yoast</a> sobre WordPress SEO.

<h6>Optimizar las Descripciones</h6>

El siguiente punto en el que incide el artículo es en el de optimización de las etiquetas <em>"&lt;meta name="description"&gt;"</em>, estas etiquetas son utilizadas por el buscador para devolver la página cuando su contenido es coincidente con una búsqueda.

Por defecto, el buscador utiliza la primera frase de la página, pero con el plugin podemos establecer una a mano. Si tomo el post anterior como ejemplo, ahora mismo me sale lo siguiente: "Bueno, pues para darme un poco de visibilidad en Google, he instalado el plugin WordPress SEO y tiene un estupendo artículo de acciones a ..." Esta descripción es obviamente mala y se puede mejorar bastante.

Para ello, debajo de cada post una sección propia del plugin y un apartado "Meta Description", en él introduzco: " Introducción a WordPress SEO y Google Web Master Tools." Obviamente, podía haber utilizado la etiqueta para poner todo un chorro de palabras simplemente para optimizar a tope la visibilidad de la página, pero no me interesa. Creo que una cosa es mejorar la visibilidad de la página y otra tratar de manipular a los motores de búsqueda. Lo dicho, lo mismo es que soy tonto xD

En esta sección del plugin también puedo ver que el template que he puesto para los títulos hace que sea demasiado largo para los motores de búsqueda, así que en la sección "SEO Title" le quito la parte del dominio. Es decir, el SEO Title coincidirá con el título de la página.

<h6>Optimización de Imágenes</h6>

Para la optimización de imágenes, aparte de recomendar un plugin, la recomendación básica que se dá es que todas las imágenes tengan un "title" y un "alt". Dá la casualidad de que eso en particular es una neura mía y todas las imágenes lo tienen, así que mission accomplished.

<h6>XML Sitemap</h6>

El último apartado en esta sección, es la generación de un <a title="XML Sitemap en Wikipedia (inglés)" href="http://en.wikipedia.org/wiki/Site_map#XML_Sitemaps" target="_blank">XML Sitemap</a>. La idea del XML Sitemap es indexar fácilmente las páginas para los buscadores, vaya, facilitarles la vida. Se puede activar a través del plugin en la sección "SEO &gt; XML Sitemaps", marco el "Check this box to enable XML sitemap functionality." y lo dejo tal y como esta por defecto.

Sin embargo, cuando le doy "XML Sitemap" para ver lo que ha generado, me devuelve un 404, no encuentra nada en <em>"<a href="http://aguasnegras.es/sitemap_index.xml">http://aguasnegras.es/sitemap_index.xml</a>"</em>... vaya rollo.

<h6>Plantillas</h6>

A continuación, viene una sección con consejos para las plantillas.

El primero es utilizar Breadcrumbs o rastro de migas, para indicarle al usuario donde esta y patatín y patatán. Vale, ODIO, los rastros de migas, por lo cual, obviaré esta sección.

El siguiente, paradójicamente, más que sobre SEO es sobre buena escritura en general. Viene a hablar sobre los encabezados, se recomienda que si es la página principal  <em>"&lt;h1&gt;"</em> sea tan solo el nombre del sitio, que los <em>"&lt;h2&gt;" </em>sean los títulos de los posts, etc...

Esto es algo bastante relacionado con el tema que se esté usando, y he de decir que Yoko lo cumple muy bien, así que nada que tocar por aquí.

El siguiente apartado, también muy relacionado con el tema que se este usando, es no incrustar css ni javascript en las plantillas de las páginas. Así se favorece que sea cacheado en el usuario y que los motores de búsqueda no los accedan, así como la velocidad de ejecución de la página. De nuevo aqui Yoko cumple bastante bien, en la página principal hay una mínima cantidad de css introducido en un etiqueta <em>"&lt;style&gt;"</em>, pero es más que aceptable y todo lo demás en lo que toca a css y javascript se encuentra en archivos separados.

El siguiente apartado es sobre velocidad. Dejando de lado técnicas más complejas o intrusivas como puede ser minimizar el número de llamadas a la base de datos o darse de alta en un CDN, la opción recomendada es instalar algún plugin de caché, en concreto recomienda "W3 Total Cache". Hace tiempo que quiero probar uno, así que más adelante lo instalaré y lo probaré.

A continuación se habla sobre la barra lateral. Es cierto que el menú lateral es demasiado genérico. Por ejemplo, en AguasNegras aparecen mis enlaces a redes sociales en cualquier página que visites, cuando realmente solo tendría sentido en la página principal y en "Acerca De". El problema es que hoy por hoy, según dice el artículo no hay forma sencilla de corregir ésto, más que programación. Así que se queda tal y como esta.

También se recomienda hacer un Sitemap en HTML, pero claro, siendo un blog esto no tiene mucho sentido.

Finalmente se dan unos consejos sobre "Author Highlighting", pero me parece ya demasiado complicado, de nuevo hay que tocar código, etc... Así que  nada por aquí.

<h6> Contenido Duplicado</h6>

A la hora de navegar por el blog existen distintas maneras, quizás demasiadas. Por ejemplo, si se tienen varios autores, se puede acceder a cada autor mediante /author/nombredelautor. En mi caso esta desactivado, pero es cierto que para un blog unipersonal, este tipo de taxonomía no tiene sentido. En la sección "SEO &gt; Indexation" se pueden controlar todo este tipo de aspectos, por ejemplo, no indexar los archivos por fecha, o por categorías o tags.

A continuación viene una sección, que la verdad, parece un poco publicitaria, ya que muchas cosas te las explica por encima y te dice que WordPress SEO las gestiona automáticamente. También recomienda un plugin para la paginación, ya que si tienes un post muy popular en una categoría con muchos posts... digamos que se pierde un poco el grano entre la paja.

<h6>Estructura del Sitio</h6>

La primera recomendación que encuentro interesante en esta sección es que si tienes un post particularmente popular o interesante... lo conviertas en una página para maximizar su exposición. Realmente tiene sentido.

Además, se recomienda utilizar un plugin de posts relacionados, para maximizar las sinergias entre los propios posts, en concreto se recomienda <a title="Yet Another Related Posts plugin" href="http://mitcho.com/yarpp/" target="_blank">Yet Another Related Posts plugin</a>, así que nada, otro más a la lista. Creo que puede ser bastante interesante ya que en realidad yo trato de hacer esta funcionalidad a mano mediante las categorías y las etiquetas, pero claro, no es lo mismo.

<h6>Otros Aspectos</h6>

Finalizando este artículo, Yoast comenta otra serie de aspectos adicionales, por ejemplo, la importancia de fidelizar a los lectores, mediante RSS y suscripción por email, el motivar la discusión y la participación de los comentaristas, así como el hacerles un "follow back", comentar en sus blogs, seguirles en Twitter, etc... En general en este sentido creo que se habla más de la construcción de una comunidad, cosa que por supuesto, influye en el SEO.

Por último se recomienda el uso de distintas herramientas para medir el impacto de las optimizaciones, como pueden ser el mismo Google Webmaster Tools y Google Analytics.

<h6>Conclusiones</h6>

El plugin WordPress SEO tiene muchísimas funcionalidades sin lugar a dudas. Es más, creo que tiene más de las que yo voy a poder utilizar eficientemente.

Sin embargo a lo largo de todo el artículo hay varios aspectos que me han ido "sorprendiendo". En general la base del SEO esta en ofrecer buenos contenidos y que sean relevantes. Es decir, el SEO es GENERAR CONTENIDO.

Después esta generación tiene una gran parte que podríamos decir que es "maquetación". De la misma forma que para un libro se escoge una encuadernación, una portada, una tipografía, etc... En la generación de contenidos hay que tener en cuenta detalles como los títulos, las etiquetas header, las keywords, etc...

Es decir, a la hora de redactar un post, o una página, una vez terminado, hay que cuidar los aspectos SEO.

Una vez hecho esto, hay disponibles una serie de herramientas para el análisis del rendimiento de la página, como pueden ser las citadas arriba.

Y como conclusión final, hay que tener en cuenta que si escribes es para ser leido, es decir, escribes para la comunidad, y es la comunidad la que te posiciona mejor o peor, en función del valor de tus contenidos.

<div><span style="color: #333333; font-family: sans-serif; font-size: 12px; line-height: 12px; background-color: #f5f5f5;">
</span></div>
