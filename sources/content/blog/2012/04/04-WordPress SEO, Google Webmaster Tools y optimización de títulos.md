title=WordPress SEO, Google Webmaster Tools y optimización de títulos.
date=2012-04-04
type=post
tags=Programación,SEO,Tools of the Trade,WordPress,tutorial
status=published
~~~~~~
Bueno, pues para darme un poco de visibilidad en Google, he instalado el <a title="WordPress SEO plugin" href="http://wordpress.org/extend/plugins/wordpress-seo/" target="_blank">plugin WordPress SEO</a> y tiene un <a title="WordPress SEO Tutorial" href="http://yoast.com/articles/wordpress-seo/" target="_blank">estupendo artículo</a> de acciones a realizar para utilizarlo, así que lo voy a seguir y voy a ir comentando.

<h6>Entorno</h6>

A día de hoy lo que tengo es un WordPress 3.3.1 con WordPress SEO 1.1.5

<h6>SEO</h6>

A continuación voy a ir siguiendo lo más fielmente posible las instrucciones que se dan en el artículo punto por punto.

<h6>Permalinks</h6>

Dice con toda razón que los permalinks han de ser legibles. Por ejemplo, ahora mismo los permalinks de aguasnegras.es son del tipo <em>"<a href="http://www.aguasnegras.es/blog/?p=410">http://www.aguasnegras.es/blog/?p=410</a>"</em>. Claramente es un error, debería incluir al menos el título del post, así que me voy a "Ajustes &gt; Enlaces Permanentes" y lo cambio, por probar solo a título del post.

Vaya, me dice que no puede modificar el .htaccess y que tengo que añadir un código a mano... Bueno, pues nada, lo añado. Pero sin embargo ahora al mostrar la página principal me dice que no encuentra nada... ufff... Esto tiene más bien pinta de estar relacionado con algo más, así que mejor dejo de tocar. Siguiente apartado.

<h6>WWW o no WWW</h6>

Este punto es interesante, ya me obliga a pensar en el branding del sitio. Personalmente siempre que pienso en el sitio, pienso en "aguasnegras", así que creo que el branding sería más adecuado como "aguasnegras.es" a secas. Esto implica dos cambios, ambos en "Ajustes &gt; Generales". En "Dirección de WordPress (URL)" y "Dirección del Sitio (URL)", elimino las www y acepto.

El siguiente paso que comenta Yoast es hacer esto también en <a title="Google Webmaster Tools" href="https://www.google.com/webmasters/tools/" target="_blank">Google Webmaster Tools</a>... lo cual estaría muy bien si supiera lo que es :D Según la página principal, sirve para mejorar la visibilidad de mi sitio en Google, pues nada, inicio sesión y le doy a añadir un sitio. En la URL introduzco <em>"aguasnegras.es"</em>. A continuación me dice que descargue un archivo html de verificación y lo suba a mi sitio, nada más fácil. Subido, verifico y le doy a continuar.

Y ya estoy en el panel de control de Google Webmaster Tools para aguasnegras.es. Hago click en "Información del Sitio &gt; Configuración" y como URL establezco "aguasnegras.es". Sin embargo al darle a "Guardar" me informa que tengo que confirmar que soy el propietario del dominio y patatín y patatán... después de cacharrear un rato, decido añadir a mis sitios "www.aguasnegras.es" y de repente empiezan a funcionar todas las analíticas y todo va bien... pues vaya, nada, ya hago el cambio y listo.

La verdad que el Google Webmaster Tools promete... habrá que echarle un vistazo más detenidamente otro día.

<h6>Títulos de los Posts</h6>

El tutorial sigue hablando del título de los posts, el título no solo es el texto que se muestra en la pantalla, si no que será lo primero que se muestre en los resultados de búsqueda.

Se recomienda que las primeras palabras del título sean las más significativas, ya que los motores de búsqueda hacen más hincapié sobre ellas... así como la gente cuando lee. Vaya, es de cajón, pero nunca me había dado por pensarlo, a partir de ahora tendré más cuidado.

Con la opción "SEO &gt; Titles" puedo controlar como se muestran los títulos de las páginas de mi sitio, no solo de los posts. Como no estoy seguro de como esta el header.php de mi tema, marco la casilla de "Force rewrite titles". Para probar, en el "Title Template" de "Homepage" pongo el ejemplo que viene en el artículo en sí: "%%sitename%% &amp;#8226; %%sitedesc%%", pulso "Save Settings" y recargo... Perfecto, me muestra "AguasNegras &amp;#8226; This was not supposed to be like this", para darle un toque personal, dejo el título del sitio como "AguasNegras || This was not supposed to be like this", jeje.

Así en plan rápido, establezco las siguientes plantillas:

<ol>
	<li>Posts y Pages: %%title%% @ %%sitename%%</li>
	<li>Category: %%category%% @ %%sitename%%</li>
	<li>Post_Tag: %%tag%% @ %%sitename%%</li>
	<li>Author Archive: %%name%% @ %%sitename%%</li>
	<li>Date Archives: %%date%% @ %%sitename%%</li>
	<li>Search Pages: %%searchphrase%% @ %%sitename%%</li>
	<li>404 Pages: Uops! @ %%sitename%%</li>
</ol>

Lo pruebo todo y perfecto, funcionan todos los títulos