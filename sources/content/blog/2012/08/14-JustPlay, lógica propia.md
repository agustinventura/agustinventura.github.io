title=JustPlay, lógica propia
date=2012-08-14
type=post
tags=Android,JustPlay,Programación,Proyectos
status=published
~~~~~~
Vale, una vez terminado el guarreo con el ciclo de vida, toca implementar la lógica de negocio propia de la aplicación.
Al ser JustPlay un reproductor de mp3 y ogg, vamos a ver que lógica tenemos que implementar:

<h6>Funcionalidad Detallada</h6>


<ol>
	<li>Gestión de la lista de reproducción, añadir directorios y canciones sueltas, borrar la lista de reproducción, eliminar canciones en particular y reordenarla mediante drag&amp;drop.</li>
	<li>Reproducir: Reproducir toda la playlist desde el principio hasta el final dándole al botón de play.</li>
	<li>Reproducir una canción: Empezar a reproducir toda la playlist desde la canción seleccionada.</li>
	<li>Parar: Parar la reproducción, al darle a play se volverá a reproducir la lista desde el principio.</li>
	<li>Pausar: Parar la reproducción, al darle a play se continuará con la reproducción donde estaba.</li>
	<li>Canción anterior: Reproducir la canción anterior, en caso de ser la primera se reproducirá desde el principio.</li>
	<li>Canción siguiente: Reproducir la canción siguiente, en caso de ser la última no se hará nada.</li>
	<li>Avance rápido: Avanzar 15 sgs en la canción. Si la posición actual de la canción + 15 sgs &gt; longitud de la canción, se pasa a la siguiente canción.</li>
	<li>Retroceso: Retroceder 15 sgs en la canción. Si la posición actual de la canción - 15 sgs &lt; 0, se comienza desde el principio.</li>
</ol>


<h6>Definición de Responsabilidades</h6>

Entre los artefactos existentes voy a dividir la responsabilidad de la siguiente manera:

<h6>MediaPlayer:</h6>


<ul>
	<li>Gestión de la interfaz del usuario.</li>
	<li>Mostrar la playlist y los controles.</li>
	<li>Toda la lógica de negocio la delega en MediaService y MediaThread</li>
</ul>


<h6>FileExplorer</h6>


<ul>
	<li>Mostrar los contenidos de la memoria del teléfono, recordando el último directorio visitado.</li>
	<li>Enviar a MediaPlayer una canción en concreto o las contenidas en un directorio y sus subdirectorios.</li>
</ul>


<h6>MediaServiceBinder</h6>


<ul>
	<li>Devuelve una instancia de MediaService al objeto que lo solicite (MediaPlayer en este caso).</li>
</ul>


<h6>MediaService</h6>


<ul>
	<li>Mantiene vivo MediaThread aunque se cierre MediaPlayer.</li>
	<li>Presenta las notificaciones al usuario en la barra de estado.</li>
	<li>Gestiona el CallManager que permite parar la reproducción cuando hay una llamada y volverla a iniciar cuando esta termina.</li>
</ul>


<h6>MediaThread</h6>


<ul>
	<li>Gestiona la reproducción de la playlist implementando toda la funcionalidad detallada arriba.</li>
</ul>

&nbsp;