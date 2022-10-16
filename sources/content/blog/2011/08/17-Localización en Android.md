title=Localización en Android
date=2011-08-17
type=post
tags=Android,Programación,tutorial
status=published
~~~~~~
En general en mi trabajo soy fanático de la<a title="i18n y L18n en Wikipedia" href="http://es.wikipedia.org/wiki/Internacionalizaci%C3%B3n_y_localizaci%C3%B3n" target="_blank"> internacionalización (i18n) y la localización (L18n)</a>, aunque la aplicación que este en desarrollo ni siquiera vaya a ser traducida nunca a ningún otro idioma.

El motivo es sencillo, si uso localización, cuando necesite poner un botón "Buscar" lo pondré en un archivo, por lo que al final todos los botones de "Buscar" de la aplicación apuntarán al mismo archivo (al mismo recurso). Ya se sabe que los clientes son caprichosos y es más que posible que pidan que ese "Buscar" se cambie por un "Encontrar"... y ahí es donde esta la potencia de la localización, basta con cambiar la palabra en el archivo adecuado. Se puede argüir que gracias a los IDEs modernos es sencillo hacer un search &amp; replace all, pero creo que la opción de cambiar directamente lo que deseas en un archivo gana por goleada. Aparte, en lo personal, me dá mucha rabia que los informáticos en general tengan la duplicación de código por el anticristo (o así debiera ser) pero no tengan nada en contra de la duplicación sin medida de literales de textos.

En Android, el concepto de "Recurso" no incluye tan solo los textos, sino también, como dice la <a title="Documentación de Localization" href="http://developer.android.com/guide/topics/resources/localization.html" target="_blank">documentación</a>: cadenas de texto, layouts, sonidos, gráficos y cualquier otro conjunto de datos estáticos. Cuando la aplicación se ejecuta, Android escoge automáticamente de entre todos los recursos provistos, el que mejor se adapta, no solo teniendo en cuenta el idioma, sino también la orientación del dispositivo, tamaño de pantalla, etc...

Por defecto, al desarrollar una aplicación se crean una serie de recursos por defecto, en el tutorial del bloc de notas ya ví algunos. En general es cualquier cosa dentro del directorio res/ y en ese caso vi las cadenas de texto (res/values/strings.xml) y los layouts (res/layout/notes_list.xml, res/layout/note_edit.xml, etc...).  La <a title="Los recursos por defecto son importantes." href="http://developer.android.com/guide/topics/resources/localization.html#defaults-r-important" target="_blank">documentación</a> recomienda que los recursos por defecto sean siempre completos, es decir, si mi strings.xml tiene siete cadenas de texto, las mismas debe tener el que se usa por defecto, ya que si cambio el locale del dispositivo del español al inglés, la aplicación se cerrará inesperadamente al no encontrar el recurso. Una buena estrategia, aunque suene extraña, es desarrollar la aplicación enteramente en inglés usando el string.xml, y después copiar y pegar al archivo localizado y traducir. Todo de una tacada.

Vale, muy bien la teoría, excelente, pero, ¿cómo traduzco el tutorial del bloc de notas?. Pues un poco más de teoría. En el caso de los textos, si quiero un strings.xml en español, iría en el directorio /res/values-es/strings.xml. Ah, perfecto, ¿y si quiere español de España y de Perú? En ese caso, tendremos dos directorios: /res/values-es-rES y /res/values-es-rPE. La primera parte (el "es") viene dado por el código de lenguaje según la <a title="Códigos de lenguajes en ISO 639" href="http://www.loc.gov/standards/iso639-2/php/code_list.php" target="_blank">ISO 639-1</a> (atención, la 1, no la 2, es de dos letras, no de tres. Lo siento por catalanes y demás afectados), después tendremos como parte fija el guión y la r (-r) y el código de región según la <a title="Códigos de regiones segun ISO 3166" href="http://en.wikipedia.org/wiki/ISO_3166-1-alpha-2#Officially_assigned_code_elements" target="_blank">ISO 3166-1-alpha-2</a>.

Vale, pero eso es lo que se refiere a lenguajes, ¿qué pasa si me interesa tener unos gráficos para pantallas grandes y otros para pantallas pequeñas? Pues que los gráficos por defecto estarán en /res/drawable, los de pantallas grande en /res/drawable-large y los de pantalla pequeña en /res/drawable-small, se puede consultar en la Tabla 2, <a title="Recursos alteranativos." href="http://developer.android.com/guide/topics/resources/providing-resources.html#AlternativeResources" target="_blank">aquí</a>.  Un momento... ¿y si quiero textos en español para dispositivos con pantalla grande? Pues eso: /res/values-es-rES-large... hala, toma ya. Pero... ¿y si tengo definidos textos en español y textos para pantalla grande en dos archivos distintos (res/values-es-rES y res/values-large) y usa la aplicación alguien con un Android con pantalla grande y en español? Pues hay unas <a title="Reglas de Resolución de Recursos" href="http://developer.android.com/guide/topics/resources/providing-resources.html#BestMatch" target="_blank">reglas de resolución de recursos</a>, pero en general, según la documentación, casi siempre mandan las locales.

Una vez visto esto, la guía dá una serie de recomendaciones:

<ol>
	<li>Proveer siempre los recursos por defecto, para evitar petes como ya he visto antes.</li>
	<li>En vez de definir un layout por idioma, usar un único layout, pero que sea flexible, que tenga capacidad de expandirse o contraerse y de controlar su tamaño programáticamente.</li>
	<li>Traducir únicamente lo imprescindible, si la aplicación por defecto esta en español de España, y quiero aportar también español de México, puede ser que no tenga que traducir todas las frases sino simplemente aquellas que incluyan por ejemplo "coche" y cambiarlo por "auto".</li>
</ol>

Y ahora, al lío. Traducción del bloc de notas:

<ol>
	<li>En el proyecto Notepadv3, creo dentro de la carpeta /res la carpeta values-es-rES.</li>
	<li>Click con el botón derecho encima de la carpeta recién creada, New... &gt; Android XML File.</li>
	<li>En nombre del archivo, usamos strings.xml y veremos que al crearlo dentro de esta carpeta nos aparece como escogidos los calificadores de pais y región.</li>
	<li>Click en Finish</li>
</ol>

<a href="/images/2011/08/Pantallazo-New-Android-XML-File-.png"><img class="size-medium wp-image-251" title="Creación de strings.xml para es-ES" src="/images/2011/08/Pantallazo-New-Android-XML-File--300x294.png" alt="Creación de strings.xml para es-ES" width="300" height="294" /></a>

Ahora a copiar y traducir:

<ol>
	<li>Abro el strings.xml original y copio todas las etiquetas &lt;string&gt;</li>
	<li>Las pego en mi nuevo strings.xml</li>
	<li>Traduzco.</li>
	<li>Arranco el emulador y cierro la aplicación para ponerlo en español (tecla home &gt; tecla menu &gt; settings &gt; language &amp; keyboard &gt; select language &gt; Español).</li>
	<li>Vuelvo a arrancar la aplicación... et voilà!</li>
</ol>

<a href="/images/2011/08/Pantallazo-Bloc-de-Notas-en-Español.png"><img class="size-medium wp-image-252" title="Bloc de Notas traducido al español" src="/images/2011/08/Pantallazo-Bloc-de-Notas-en-Español-300x278.png" alt="Bloc de Notas traducido al español" width="300" height="278" /></a>

Y eso es todo, si quieres los fuentes del proyecto, los tienes en GitHub.

<a title="Fuentes en GitHub" href="https://github.com/agustinventura/Bloc-de-Notas-en-Espa-ol" target="_blank"><img class="aligncenter size-full wp-image-255" title="GitHub" src="/images/2011/08/github_icon.png" alt="GitHub" width="115" height="115" /></a>
