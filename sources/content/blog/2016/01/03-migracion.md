title=Migrando el blog
date=2016-01-03
type=post
tags=Java, JBake, Wordpress
status=published
~~~~~~

Desde hace ya bastantes años llevo pagando religiosamente todos los años un dominio (aguasnegras.es) y un alojamiento para tener el blog.
El blog ha tenido mejores y peores momentos, pero en general me gusta tener un sitio donde poder escribir en un momento dado, y por supuesto compartir con la comunidad (sobre todo en español, es por lo que escribo en este idioma).

El asunto es que si nos paramos a pensarlo, el blog tiene bastantes pocos comentarios y sobre todo entradas mías, es decir, es fundamentalmente un medio de solo lectura. Hace ya un tiempo que pienso que tener para ésto un Wordpress con su PHP y su MySQL es bastante asesino y hasta antieconómico (en sentido general, porque el hosting me cuesta cuatro duros al año, tampoco vamos a ser ruinas). Otra cosa que me molesta bastante es tener que andar actualizando Wordpress (cosa lógica y normal) y aunque ya las actualizaciones sean automáticas, pues me molesta.

Total, que a esto le sumamos que GitHub ofrece desde hace tiempo [GitHub Pages](https://pages.github.com/) que consiste en alojamiento gratuito para HTML estático y más a huevo imposible... quedaría pendiente el tema de los comentarios, pero precisamente para esto, [Disqus](https://disqus.com/) permite incluirlos por Javascript con una configuración muy sencilla.

Con esto ya va quedando claro el enfoque, ahora habría que ver como generar el HTML, ya que escribir HTML a pelo es posible, pero es más bien coñazo. GitHub Pages usa [Jekyll](https://jekyllrb.com/) que permite usar Markdown para escribir, pero como buen javero de pro he buscado una opción similar en Java, [JBake](http://jbake.org/). Eso sí, el inconveniente es claro, con Jekyll lo único que hay que subir a GitHub son los archivos .md mientras que con JBake tendré que generar el HTML y subirlo.

Por tanto, hay tres trabajos importantes que hacer para estudiar la viabilidad de usar GitHub Pages para alojar el blog:

1. Integrar Disqus en JBake.
2. Personalizar el HTML generado por JBake.
3. Ver como subir los fuentes y HTML a GitHub y estudiar el workflow de publicación.
