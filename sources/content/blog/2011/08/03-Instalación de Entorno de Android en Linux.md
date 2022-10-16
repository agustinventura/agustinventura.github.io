title=Instalación de Entorno de Android en Linux
date=2011-08-03
type=post
tags=Android,Programación,tutorial
status=published
~~~~~~
Pasos para instalar el Android SDK, Eclipse y Android Development Toolkit en Eclipse:

<ol>
	<li>Si el sistema es Ubuntu de 64 bits, instalar los <a title="instalación de ia32-libs" href="http://developer.android.com/sdk/installing.html#troubleshooting" target="_blank">ia32-libs</a></li>
	<li>Instalar JDK de Sun: 
```prettyprint linenums
sudo apt-get install sun-java6-jdk
```
</li>
	<li>Asegurarse de que se esta usando el JDK de Sun: 
```prettyprint linenums
java -version
```
 debe devolver (entre otras cosas) Java HotSpot</li>
	<li>Descargar <a title="Descarga SDK de Android" href="http://developer.android.com/sdk/index.html" target="_blank">SDK de Android</a></li>
	<li>Descomprimir SDK (por ejemplo en $HOME/Android)</li>
	<li>Descargar <a title="Descarga de Eclipse Indigo" href="http://www.eclipse.org/downloads/" target="_blank">Eclipse Indigo</a>, vale la "Classic Edition"</li>
	<li>Descomprimir Eclipse ($HOME/Android)</li>
	<li>En $HOME/Android debe haber dos carpetas: android-sdk-linux_x86 y eclipse.</li>
	<li>Ejecutar Eclipse y pulsar Help &gt; Install New Software... y pulsar el botón Add...</li>
	<li>En Name introducir "ADT Plugin" y en location https://dl-ssl.google.com/android/eclipse/</li>
	<li>En la pantalla de Install New Software seleccionar este sitio y marcar todo el software que nos ofrece para instalar.</li>
	<li>Aceptar las licencias y ante el aviso de "Unsigned Software", aceptar igualmente.</li>
	<li>Reiniciar Eclipse y pulsar Window &gt; Preferences y seleccionar Android en el menú de la izquierda.</li>
	<li>Aceptar el aviso de Google (marcando si deseamos o no enviar datos de uso)</li>
	<li>En SDK Location introducir $HOME/Android/android-sdk-linux_x86</li>
	<li>Pulsar Apply, OK.</li>
</ol>

Listo, con esto ya esta todo instalado en Eclipse y listo para funcionar, otro día repasaré el proceso de creado de AVDs.