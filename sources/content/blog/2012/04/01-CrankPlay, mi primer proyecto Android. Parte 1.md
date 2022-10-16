title=CrankPlay, mi primer proyecto Android. Parte 1
date=2012-04-01
type=post
tags=Android,JustPlay,Programación,Proyectos
status=published
~~~~~~
Bueno, pues después de un tiempo dedicado a un proyecto que tengo por ahí y que anda un poco empantanado, voy a empezar a hacer algo que llevo tiempo queriendo hacer. Un reproductor de mp3 para mi móvil.

Voy a empezar haciendo una pequeña elicitación de requisitos "grosso modo" para tenerlo como guía de aquí en adelante.

<strong>Requisitos</strong>

El reproductor tendrá las siguientes funcionalidades:

<ol>
	<li>Contará con una lista de reproducción en la que se almacenarán las canciones a reproducir en orden.</li>
	<li>Leerá las canciones de directorios en el almacenamiento del móvil, pudiendo en todo caso seleccionar una carpeta con lo cual se incluirían todos los mp3 en ella y sus subcarpetas en la lista de reproducción.</li>
	<li>Contará con los controles básicos en un reproductor musical: Play, Stop, Pause, Next, Back, Volumen.</li>
</ol>

Como requisitos no funcionales:

<ol>
	<li>Deberá consumir los recursos mínimos posibles.</li>
</ol>

<strong>Enfoque del Desarrollo</strong>

Pues para desarrollar, voy a empezar basándome en el <a title="MusicDroid Audio Player, HelloAndroid" href="http://www.helloandroid.com/tutorials/musicdroid-audio-player-part-i" target="_blank">tutorial MusicDroid de HelloAndroid</a>. Este tutorial tiene ya bastantes años, así que iré haciendo un repaso de las APIs involucradas, actualizándolas según sea necesario.

<strong>Paso 1 - Crear el Proyecto</strong>

El primer paso es sencillo, creo el proyecto, inicializo git, creo repositorio en GitHub y lo subo, para más detalles, <a title="Git, EGit y GitHub." href="http://www.aguasnegras.es/?p=201" target="_blank">Tutorial de Git y GitHub</a>.

Resultado, ya esta el proyecto en GitHub:

<a href="https://github.com/agustinventura/CrankPlay"><img class="size-full wp-image-255" title="CrankPlay en GitHub" src="/images/2011/08/github_icon.png" alt="CrankPlay en GitHub" width="115" height="115" /></a>

Ahora toca empezar con el tutorial de MusicDroid.

<strong>Paso 2 - Lista de canciones</strong>

El primer paso del tutorial es simplemente mostrar una lista de todos los archivos .mp3 que hay en la tarjeta sd.

Lo primero es el layout, el songlist.xml. Lo he modificado un poco de la siguiente manera:

<ol>
	<li>He sacado la cadena de texto "No songs found" al strings.xml.</li>
	<li>He cambiado el layout_weight, lo he quitado porque daba un warning en combinación con el layout_width.</li>
</ol>

Ahora, se hace el layout correspondiente a cada canción, song_item.xml. Es copiar y pegar y solo modifico el id, lo cambio por <em>@+id/song_title</em>.

<strong>Paso 3 - Actividad CrankPlay</strong>

Lo primero que hago en la Activity es hacer que extienda de ListActivity para poder gestionar nativamente el layout ListView. A continuación copio y pego las variables locales:

<ol>
	<li>MEDIA_PATH: directorio en el que estan los mp3 (la tarjeta SD por defecto).</li>
	<li>songs: lista de canciones en MEDIA_PATH.</li>
	<li>mp: instancia de MediaPlayer que reproducirá las canciones.</li>
	<li>currentPosition: posición de la canción que se esta reproduciendo.</li>
</ol>

En cuanto al OnCreate, sin misterios, se encarga de arrancar la aplicación y actualizar la lista de canciones.

En cuanto el updateSongList se encarga de cargar el directorio especificado en MEDIA_PATH y buscar en él todos los archivos terminados en .mp3 con la ayuda de la clase Mp3Filter.

Siguiente paso del tutorial, reproducir una canción cuando se hace click en ella. Para ello se usa un OnListItemClick que únicamente se encarga de llamar al método playSong, pasándole el nombre del archivo de la canción.

PlaySong se limita a usar el objeto mp para reproducir la canción. Primero se hace un reset con lo cual se pausa cualquier canción que se este reproduciendo y se carga la canción nueva. Se crea una clase interna anónima para implementar OnCompletionListener, que se limita a invocar al método nextSong para reproducir la siguiente canción (de haberla).

Y por último nextSong, sencillamente comprueba que no sea la última canción y si no lo es, incrementa currentPosition y llama a playSong.

Listo.

<strong>Paso 4 - Probar la Aplicación</strong>

Si ejecuto la aplicación directamente (Click con el botón derecho en el proyecto Run as &gt; Android Application), se muestra el mensaje definido para el caso de que no haya canciones <em>"No songs found"</em>, y es correcto, hay que subir mp3s a la tarjeta SD.

Este apartado del tutorial ya esta un poco desfasado, los emuladores ya se pueden crear con el AVD Manager de Eclipse con la tarjeta SD ya creada, con lo cual basta con enviar el mp3 al dispositivo usando el adb en la línea de comandos. El primer paso es tener arrancado el emulador.

El segundo enviar el mp3 de prueba:


```prettyprint linenums

~/Android/android-sdks/platform-tools$ ./adb push ~/Música/Noel\ Gallagher\'s\ High\ Flying\ Birds\ -\ Noel\ Gallagher\'s\ High\ Flying\ Birds\ \(Deluxe\ Version\)\ \[theLEAK\]/01.\ Everybody\'s\ On\ The\ Run.mp3 /sdcard/Prueba.mp3

```


Y listo, ya sale andando y tengo Prueba.mp3 en la lista de canciones.

Ahora bien, si le doy a reproducir no se escucha nada, y en el LogCat se puede ver un Warning: "obtainBuffer timed out (is the CPU pegged?)". Por lo visto este fallo lo produce el tener habilitados los snapshots en el emulador, así que nada, lo deshabilito y reinicio.

Listo, ya reproduce el mp3, así que ahí lo dejo, mañana más y mejor.
