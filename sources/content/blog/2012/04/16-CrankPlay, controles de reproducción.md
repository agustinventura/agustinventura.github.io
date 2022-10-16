title=CrankPlay, controles de reproducción
date=2012-04-16
type=post
tags=Android,JustPlay,Programación,Proyectos
status=published
~~~~~~
Última parte del tutorial que sigo para el CrankPlay, <a title="MusicDroid - Part III" href="http://www.helloandroid.com/tutorials/musicdroid-audio-player-part-iii" target="_blank">MusicDroid</a>, ahora voy a añadir los controles básicos de reproducción. Esta parte se me antoja que no me será de mucha utilidad, ya que es bastante dependiente del diseño de la aplicación, pero que demonios...

<h6>Controles de Reproducción</h6>

El objetivo de esta parte es añadir los controles de reproducción a la aplicación. Estos se mostrarán como una capa semitransparente sobre la lista de canciones.

Me cojo el xml que viene en la página y lo pego. Como ya me ha pasado antes, justo delante del <em>"id"</em> hay que añadir el namespace: <em>"android:"</em>. Además quito unos puntos y comas y listo. Ahora a ver si explico un poco como es el layout.

En primer lugar, si se mira el songlist.xml, lo primero que se aprecia es que usa un LinearLayout. Un LinearLayout posiciona los elementos hijos en forma de columna (o fila). Y punto. En songlist.xml posiciona los elementos en columna porque el atributo <em>"android:orientation"</em> esta establecido al valor <em>"vertical"</em>.

Esto tiene sentido porque se quiere representar una lista de valores en columna, pero sin embargo, los controles de reproducción se quieren situar los unos en función de los otros... Y esto es lo que hace un RelativeLayout, permite posicionar sus hijos relativamente entre ellos.

Lo que se hace en controls.xml es utilizar un RelativeLayout para que ocupe toda la pantalla y en su interior otro en el centro (controlado por <em>"android:layout_centerVertical"</em> y <em>"android:layout_centerHorizontal"</em>) que tendrá un área total de 170dip x 170dip. ¿<a title="dip en la documentación de android" href="http://developer.android.com/guide/topics/resources/more-resources.html#Dimension" target="_blank">Qué es un dip</a>? Pues es un "Density Independent Pixel", para hacer una idea, 1 dip = 1 pixel en una pantalla de 160 dpi. Si la pantalla tiene mayor resolución, se escala automáticamente. Vamos, que es una medida independiente del tamaño de la pantalla.

Por último, para situar los ImageView se utiliza <em>"android:layout_alignParentTop, android:layout_centerHorizontal"</em>, etc...

<h6>Añadiendo una Animación</h6>

Cosa que yo no sabía, en android se pueden declarar animaciones con xml. El tutorial propone añadir una que haga que un botón pulsado se haga más grande y otra vez más pequeño. La verdad que el xml es bastante entendible, escala por 1.5 la imagen, alcanzando este tamaño en 600 msg.

Para invocar la animación, pues por ejemplo en el OnKeyUp de los controles se invoca al método startAnimation de la vista correspondiente pasándole como parámetro la animación definida... ningún misterio.

<h6>Creando un Tema</h6>

Además de la animación, en el tutorial la actividad con los controles de reproducción es transparente y se superpone a la actividad con la lista de mp3, haciendo por tanto posible ver la canción que se esta reproducción. Para conseguir este efecto hay que diseñar un tema (una apariencia visual) para esta actividad.

Lo más sencillo, y lo que hacen en el tutorial es crear un tema que herede del tema por defecto de android y decirle que el color de fondo de la actividad sea transparente y que no tenga título. Todo esto en un archivo llamado styles.xml en <em>"res/values"</em>. Para crear el archivo, he tenido que modificar el atributo parent y establecerlo como <em>"parent="android:Theme""</em>, ya que si no, no lo reconoce.

Una vez hecho esto avisa del epígrafe de <em>"@drawable/transparent_background"</em>. Esto es debido... a que no existe, jeje.  Para crearlo, en <em>"res/values"</em> hay que crear un archivo llamado colors.xml y pegarle la definición de este transparent background.

Por último, se define la actividad en el AndroidManifest.xml aplicándole el tema.

<h6>Creando la Actividad</h6>

Pues una vez declarada, toca crearla. El código que viene en la página es bastante sencillo, se limita a gestionar la conexión con el servicio y a ejecutar la animación sobre el botón pulsado.

Como en el artículo anterior, tengo que tocar el método bind y eliminar el parámetro null que se le pasa ya que esa signatura esta deprecada y en el OnKeyUp tengo que capturar también una RemoteException. Con ésto ya compila.

Pero antes, hay que cambiar la actividad CrankPlay para que cuando se pulse en un elemento, invoque la nueva actividad y entonces empiece a reproducir. Lo único que el tutorial esta tan pasao de rosca que el método startSubActivity ya no existe, así que haré una llamada a startActivityForResult.

Y con ésto ya lanzo y andando, todo perfecto :)

<h6>Conclusiones</h6>

Bueno, en primer lugar, el autor prometía una cuarta parte del tutorial... pero va a ser que nunca se llevó a cabo xD De entrada tal y como esta a día de hoy hay 4 grandes problemas:

<ol>
	<li>Los controles no son táctiles!! Eso es, se utiliza OnKeyUp, asi que uno se puede hartar de pulsar encima que nada...</li>
	<li>Una vez parada una canción... no hay forma de reanudarla!</li>
	<li>De la misma manera, tampoco hay forma de salir de la actividad de control y volver a la lista de canciones.</li>
	<li>Por último, falta una barra de indicación de por donde va la canción o un minutero u algo, ah, y leer el id3 tag.</li>
</ol>


<div>Pues nada, creo que con eso ya tengo deberes para un rato bueno. Además hay otro tema que es hacer una actividad que me haga de explorador de archivos para seleccionar que carpeta (con sus subcarpetas) quiero leer.</div>

&nbsp;

&nbsp;