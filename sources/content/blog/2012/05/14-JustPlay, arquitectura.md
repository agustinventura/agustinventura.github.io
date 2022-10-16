title=JustPlay, arquitectura
date=2012-05-14
type=post
tags=Android,JustPlay,Programación,Proyectos
status=published
~~~~~~
Bueno, ya va siendo hora de empezar el trabajo en JustPlay.

Después de mucho documentarme sobre <a title="Activity - Android Developers" href="http://developer.android.com/reference/android/app/Activity.html" target="_blank">Activities</a>, <a title="Services - Android Developers" href="http://developer.android.com/guide/topics/fundamentals/services.html" target="_blank">Services</a> y <a title="Processes and Threads - Android Developers" href="http://developer.android.com/guide/topics/fundamentals/processes-and-threads.html" target="_blank">Threads</a>, creo que tengo una aproximación bastante buena a la arquitectura que voy a intentar implementar.

<h6><strong>Introducción</strong></h6>

Un requisito fundamental es que la aplicación consuma los mínimos recursos posibles, con lo cual cabría pensar que se puede implementar mediante una Activity normal y corriente. Esto es un error, una Activity tiene un ciclo de vida determinado y cabe suponer (aunque no he hecho la prueba) que en cuanto pasara al estado <em>"Paused"</em>, se terminaría la reproducción de música.

Por tanto hay que buscar otro componente que escape del ciclo de vida de la Activity y con el cual se pueda comunicar la Activity es decir, un Service. El <a title="Service Lifecycle - Android Developers" href="http://developer.android.com/guide/topics/fundamentals/services.html#Lifecycle" target="_blank">ciclo de vida del Service</a> hace que este permanezca vivo aún cuando la Activity pase a cualquier estado que no sea <em>"Resumed".</em>

En el tutorial de CrankPlay ya se ha visto <a title="CrankPlay, Service para reproducir sonido." href="http://aguasnegras.es/?p=422" target="_blank">un ejemplo</a> de esto, sin embargo este ejemplo estaba claramente desfasado y se le pueden criticar varios puntos desde el punto de vista de mis requisitos:

<ol>
	<li>La comunicación entre procesos (IPC) no me es necesaria, tan solo necesito que una única actividad acceda al servicio.</li>
	<li>La definición de la interfaz con AIDL tan solo es necesaria si se desea IPC, por tanto, basta con heredar de Service.</li>
	<li>Además, en cuanto a este Service, hay que considerar que no es algo que yo lance y me pueda olvidar de él, sino que tendré que comunicarme periódicamente con él (modificación de la playlist, start/stop, etc...), es decir, necesito un <a title="Bound Service - Android Developers" href="http://developer.android.com/guide/topics/fundamentals/bound-services.html" target="_blank">BoundService</a>.</li>
	<li>Por último, tal y como dice la documentación en numerosos sitios, un Service se ejecuta en el mismo thread que el UI Thread, con lo cual... necesitaré un thread propio que se encargue de la reproducción (actividad pesada por definición).</li>
</ol>

Gráficamente, esta propuesta quedaría <a title="Arquitectura JustPlay" href="https://docs.google.com/drawings/d/1aBKs0rDh2qzGWODF9TKh1FXBoFJdIpBsJ9o1rtsJAvY/edit" target="_blank">así</a>.

Ahora voy a montar la infraestructura básica.

<h6>Implementación</h6>

La actividad de momento no tiene mayor historia, basta con dejarla tal cual.

Para implementar el Service, creo una nueva clase (MediaService) y hago que herede de Service. Para que sea realmente funcional, lo declaro en el AndroidManifest.xml:


```prettyprint linenums

<service android:name="com.crankcode.services.MediaService" android:exported="false"/>;

```


El atributo <em>"android:exported=false"</em>, lo que indica es que el servicio no estará disponible para otras actividades del sistema, un poco de programación defensiva.

Para el thread, simplemente creo la clase MediaThread y hago que implemente Runnable.

Para arrancar el MediaService, en el onCreate de MediaPlayer escribo lo siguiente:


```prettyprint linenums

@Override
public void onCreate(Bundle savedInstanceState) {
  super.onCreate(savedInstanceState);
  startService(new Intent(getBaseContext(), MediaService.class));
  setContentView(R.layout.main);
}

```


Y en el MediaService, defino su onStart así:


```prettyprint linenums

@Override
public void onStart(Intent intent, int startId) {
  Log.d("CrankPlayer", "MediaService.onStart()");
  this.mediaThread = new Thread(new MediaThread());
  this.mediaThread.start();
  super.onStart(intent, startId);
}

```


Por último, en el run de MediaService meto un chivato:

```prettyprint linenums

public void run() {
  Log.d("CrankPlayer", "MediaThread.run");
}

```


Ahora, a arrancar y ver si todo ha ido bien.

Y todo correcto, funcionando a la primera.

<h6>TODO</h6>


<ol>
	<li>Añadir la instancia de MediaPlayer al Thread</li>
	<li>Hacer el bind del service en la activity.</li>
</ol>


<h6>Código</h6>

Como de costumbre, el código esta en GitHub:

<a href="https://github.com/agustinventura/JustPlay"><img class="size-full wp-image-255" title="JustPlay en GitHub" src="/images/2011/08/github_icon.png" alt="JustPlay en GitHub" width="115" height="115" /></a>
