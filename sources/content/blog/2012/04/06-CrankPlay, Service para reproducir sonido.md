title=CrankPlay, Service para reproducir sonido.
date=2012-04-06
type=post
tags=Android,JustPlay,Programación,Proyectos
status=published
~~~~~~
Siguiendo la <a title="MusicDroid part II" href="http://www.helloandroid.com/tutorials/musicdroid-audio-player-part-ii" target="_blank">segunda parte de MusicDroid</a>, voy a hacer un Service (servicio) para reproducir la música. Para lo cual necesito primero definir claramente que es un Service.

Según la documentación <a title="Service en Application Fundamentals" href="http://developer.android.com/guide/topics/fundamentals.html#Components" target="_blank">oficial de Android</a>, un Service es... bueno, es una chapa, vaya que un Service es un proceso en segundo plano sin interfaz de usuario y con el cual puede comunicarse cualquier otro componente o artefacto que viva en el ecosistema. La parte interesante es que esta comunicación es asíncrona y se hace por paso de mensajes (como todo en Android), así que cuidado con esta parte.

<h6>Desarrollo del Service</h6>

Ahora, en el tutorial, viene una parte que tengo que terminar de entender más a fondo. El tema es que para comunicarse con un Service hay que definir una interfaz en un lenguaje llamado <a title="AIDL en StackOverflow" href="http://stackoverflow.com/questions/6326903/aidl-android-interface-definition-language" target="_blank">AIDL</a>, de momento voy a seguir al pie de la letra el tutorial y me creo mi CPSInterface.aidl y copio y pego tal cual, ya más adelante veré de mejorar esta parte (o entender mejor).

Efectivamente, al salvarlo, en el directorio gen, me ha creado un paquete com.crankcode.crankplay.services en el que ha creado el correspondiente .java. Maravilloso.

Ahora toca crear el Service en sí, CPService en este caso concreto. Este servicio se une con la clase generada anteriormente (CPSInterface.java) proveyendo una implementación de una clase abstracta interna de esa interfaz, CPSInterface.Stub, y este Stub es el que ejecuta la lógica para utilizar el MediaPlayer. Para mi gusto hay un abuso de clases anónimas (como en casi todo lo de Android), pero de momento esta bien así, a seguir adelante.

El siguiente paso es obvio, el Stub hace uso de una serie de funciones, playSong, prevSong, etc... que hay que definir en el CPService, en el tutorial viene un ejemplo de una. En general la lógica era la que ya hacía la Activity, pero además metiéndole la gestión de mensajes necesaria para comunicarse con el invocador.

Esta parte es la siguiente en ser analizada. Lo primero de lo que se queja es de que no existe playbackstart.png, así que me cojo tanto ese icono como playbackpause.png y los copio al res/drawable... Joe, si que esta desfasao el tutorial, yo tengo cuatro subdirectorios: drawable-hdpi, etc... Bueno, de momento lo copio a todos y ya lo veré en más detalle.

Una vez añadidos, se queja de que no existe el constructor de Notification. Claro, de entrada lo primero que veo en el tutorial es que hay que crear un NotificationManager para gestionar las notificaciones, así que añado el onCreate y el onDestroy... pero esto no cambia nada, vaya plan. Claro, tiene toda la pinta de que el constructor que se utiliza de Notification esta absoluta y totalmente deprecated. Un vistazo rápido a la <a title="Documentación de Notification" href="http://developer.android.com/reference/android/app/Notification.html" target="_blank">documentación</a>  me confirma que ese constructor ya no existe, así que usaré el siguiente:

```prettyprint linenums
Notification notification = new Notification(
					R.drawable.playbackstart, file, System.currentTimeMillis());
```

Con esto se ha terminado el servicio, ahora toca usar el servicio desde la actividad.

<h6>Uso del Service</h6>

Lo primero es declarar el servicio en el applicationManifest.xml y aquí me vuelvo a encontrar que el atributo class que usa el tutorial ya no existe, pues nada, lo declaro así:

```prettyprint linenums
<service android:name=".services.CPService" android:process=":remote"/>
```

Y cruzo los dedos... Una vez en la actividad, la lógica es bastante sencilla, se crea una instancia de la interfaz del servicio (CPSInterface) y se hace un bind en el OnCreate a ese servicio. Este bind lo he tenido que cambiar también a lo siguiente:

```prettyprint linenums
this.bindService(new Intent(CrankPlay.this, CPService.class),
				mConnection, Context.BIND_AUTO_CREATE);
```

Para hacer el bind es necesario tener una instancia de un ServiceConnection que es una clase que se encarga de gestionar la conexión y desconexión del servicio.

Y por último, se cambia el updateSongs y el OnListItemClick para hacer llamadas al servicio en vez de ejecutar la lógica de reproducción.

Pues con esto listo... vamos a ver si funciona. Pues no, no funciona, cuando hago click en una canción termina saliéndome una excepcion que dice "contentView required". Después de bichear un rato por Google, parece que el error esta relacionado con la gestión de notificaciones (que lógicamente ha evolucionado bastante en estos años). Para hacer una prueba rápida, voy a tratar de quitar las notificaciones, asi que comento todo el código relativo al NotificationManager y las notificaciones.

Y ahora sí que arranca y reproduce. Bueno, pues parte dos de la misión, arreglar el tema de las notificaciones.

Y efectivamente, el tema de las notificaciones estaba más que deprecated, quedaría así

```prettyprint linenums
//Create the notification
Notification notification = new Notification(
	R.drawable.playbackstart, file, System.currentTimeMillis());
Context context = getApplicationContext();
//Create the intent that will be fired when user clicks on the notification
Intent notificationIntent = new Intent(this, CrankPlay.class);
//The PendingIntent represents the firing of above intent
PendingIntent contentIntent = PendingIntent.getActivity(this, 0,
	notificationIntent, 0);
//Notification general information
notification.setLatestEventInfo(context, "Playing ", file,
	contentIntent);
//Display
nm.notify(NOTIFY_ID, notification);
```

Los pasos a dar son bastante sencillos:

<ol>
	<li>Crear la notificación, incluyendo el icono a presentar, el texto descriptivo (en este caso es el nombre de la canción) y el momento de la notificación.</li>
	<li>Crear el Intent que se lanzará cuando se haga click en la notificación</li>
	<li>Crear el PendingIntent, que no es más que el disparador del Intent anterior, los parámetros son la actividad que lo lanza, un request code que no se usa, el intent que se lanzará y una serie de flags.</li>
	<li>Se añaden unos datos adicionales a la notificación y el PendingIntent.</li>
	<li>Se lanza la notificación.</li>
</ol>

Con estos cambios pruebo a arrancar... et voilà, todo perfectamente funcional. Es más, gracias al servicio, puedo ejecutar otras aplicaciones, que sencillamente haciendo click en la notificación, vuelvo a CrankPlay. ¡Bien!

<h6>Notas</h6>

Quizás en esta parte es donde el tutorial ha envejecido de peor manera. Por ejemplo, la declaración del Service o el uso de notificaciones. No solo eso sino que si se consulta cualquier fuente más moderna (por ejemplo, <a title="Android Service Tutorial, por Lars Vogel (inglés)" href="http://www.vogella.de/articles/AndroidServices/article.html" target="_blank">esta</a> de Lars Vogel ) veremos que hoy en día hay otras opciones de Service no descritas en el tutorial, como por ejemplo crear un Service que se ejecute dentro del mismo hilo de la aplicación, con lo cual nos ahorramos crear el AIDL. No obstante si se quiere que el Service se ejecute en su propio hilo, sigue siendo absolutamente necesario el AIDL.

Esto abre una serie de consideraciones a la hora de diseñar la aplicación que tendré que considerar (por ejemplo, si el servicio es local... ¿muere si el sistema acaba con la actividad principal? En ese caso quizás no sea lo que necesito...).