title=JustPlay, binding al servicio
date=2012-05-18
type=post
tags=Android,JustPlay,Programación,Proyectos
status=published
~~~~~~
El siguiente paso en el desarrollo de JustPlay resulta bastante obvio, ligar el MediaPlayer con el MediaService, o lo que es lo mismo, hacer un bind. Para no perderme, he hecho un pequeño diagrama de interacción entre <a title="Diagrama de Interacción entre CrankPlayer y MediaService" href="https://docs.google.com/drawings/d/1onAU0Ucfi0twATpAlizEuqY9OBoZo_0T9MjD195un4w/edit" target="_blank">MediaPlayer y MediaService</a>.

En él se aprecia que aparte de los métodos de negocio necesarios (denotados por una línea discontínua), todavía me faltan por implementar dos métodos del ciclo de vida: el bind y el unbind, que son precisamente los que me permiten establecer una comunicación bidireccional con el MediaService para indicar acciones y realizar y obtener resultados.

<h6>Bind y Unbind de MediaService</h6>

La definición más pura de Service dice que este es un componente aislado que ejecuta una computación. Esto esta muy bien pero en realidad, si no te puedes comunicar con él, su uso es bastante limitado, para eso existen los <a title="Bound Services - Android Developers" href="http://developer.android.com/guide/topics/fundamentals/bound-services.html" target="_blank">bound services</a>. Un bound service se puede combinar con un servicio "normal" (y de hecho es lo que hago) y además ofrece dos métodos adicionales, el bind y el unbind. Lo importante es que en el bind devuelve una interfaz que permite interactuar con él.

Primero entonces creo la clase que hará de fachada del servicio que extiende de <a title="Binder - Android Developers" href="http://developer.android.com/reference/android/os/Binder.html" target="_blank">Binder</a>:

```prettyprint linenums
public class MediaServiceBinder extends Binder {

  private final MediaService mediaService;

  public MediaServiceBinder(MediaService mediaService) {
    this.mediaService = mediaService;
  }
}
```

A continuación, declaro una variable de esta clase en el servicio:

```prettyprint linenums
private final IBinder mediaServiceBinder = new MediaServiceBinder(this);
```

Y la devuelve en el método onBind:

```prettyprint linenums
@Override
public IBinder onBind(Intent bindingIntent) {
  return this.mediaServiceBinder;
}

@Override
public boolean onUnbind(Intent intent) {
  // Nothing to do here
  return super.onUnbind(intent);
}
```

El onUnbind, de momento he considerado que no requiere ninguna acción en especial.

Vale, con esto el servicio ya devuelve su fachada.

Ahora viene la parte de MediaPlayer, siguiendo el diagrama de interacción, voy a hacer el bind en el onStart:

```prettyprint linenums
@Override
public void onStart() {
  super.onStart();
  Intent intent = new Intent(this, MediaService.class);
  bindService(intent, mediaServiceConnection, Context.BIND_AUTO_CREATE);
}
```

Pero bindService no devuelve el MediaServiceBinder inmediatamente, sino que es devuelto asincronamente, para eso se pasa el objeto mediaServiceConnection, que es una implementación de <a title="Service Connection - Android Developers" href="http://developer.android.com/reference/android/content/ServiceConnection.html" target="_blank">ServiceConnection</a>, además creo una instancia propia de MediaServiceBinder:

```prettyprint linenums
private MediaServiceBinder mediaServiceBinder = null;

private ServiceConnection mediaServiceConnection = new ServiceConnection() {
  public void onServiceConnected(ComponentName className,
    IBinder service) {
    mediaServiceBinder = (MediaServiceBinder) service;
  }

  public void onServiceDisconnected(ComponentName arg0) {
    mediaServiceBinder = null;
  }
};
```

Para acabar con esta parte, en el onPause de MediaPlayer, hago el unBind:

```prettyprint linenums
@Override
public void onPause() {
  unbindService(mediaServiceConnection);
  super.onPause();
}
```

Con ésto ya estan implementados los servicios del ciclo de vida, y ahora ya solo me queda por implementar la lógica de negocio.

<h6>TODO</h6>


<ol>
	<li>Añadir el MediaPlayer al MediaThread</li>
	<li>Definir fachada de MediaService (o lógica de negocio) en MediaServiceBinder.</li>
	<li>Implementar la lógica en MediaService y MediaThread.</li>
</ol>


<h6>Código</h6>

En GitHub (para variar):

<a href="https://github.com/agustinventura/JustPlay"><img class="size-full wp-image-255" title="CrankPlayer en GitHub" src="/images/2011/08/github_icon.png" alt="CrankPlayer en GitHub" width="115" height="115" /></a> Repositorio de JustPlay en GitHub
