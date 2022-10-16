title=Git, EGit y GitHub.
date=2011-08-06
type=post
tags=Git,Tools of the Trade,tutorial
status=published
~~~~~~
<strong>Introducción</strong>

Este tutorial pretende reflejar un ciclo de trabajo básico con Git, EGit y GitHub, crear un nuevo repositorio, añadir y borrar archivos y subir ese repositorio a GitHub. Si quieres saber que es un sistema de control de versiones, las diferencias entre un sistema de control de versiones centralizado y uno distribuido o por qué Git y no Mercurial o Bazaar, te recomiendo que le eches un vistazo a alguna de las referencias.

<strong>Referencias:</strong>

<ul>
	<li><a title="Git Tutorial by Lars Vogel" href="http://www.vogella.de/articles/Git/article.html">Git Tutorial</a> y <a title="Git With Eclipse by Lars Vogel" href="http://www.vogella.de/articles/EGit/article.html" target="_blank">Git with Eclipse</a>, por <a title="Lars Vogel" href="http://www.vogella.de/" target="_blank">Lars Vogel</a>.</li>
	<li><a title="Modern Version Control with Git, Smashing Magazine" href="http://coding.smashingmagazine.com/2011/07/26/modern-version-control-with-git-series/" target="_blank">Modern Version Control with Git</a>, por <a title="Smashing Magazine" href="http://www.smashingmagazine.com/" target="_blank">Smashing Magazine</a>.</li>
	<li><a title="EGit User Guide" href="http://wiki.eclipse.org/EGit/User_Guide" target="_blank">EGit User Guide</a>.</li>
</ul>

<strong>Configuración de Git.</strong>

Hay que instalar Git, bien git-core para Linux, bien <a title="msysgit" href="http://code.google.com/p/msysgit/" target="_blank">msysgit</a> para Windows.

Una vez instalado, hay que seguir este <a title="Configuración de Git" href="http://progit.org/book/ch1-5.html" target="_blank">tutorial</a> para configurarlo. Si es en Windows, se puede usar el Git Bash que provee el msysgit. Para el propósito de este artículo, basta con rellenar nombre y email.

<strong>Instalación de EGit en Eclipse Indigo.</strong>

EGit se puede instalar directamente desde el marketplace de Eclipse:

<strong></strong>Help &gt; Eclipse Marketplace &gt; Find: "EGit" &gt; Install

Se reinicia Eclipse y queda instalado.

<strong>Creación del Proyecto de Pruebas.</strong>

Para las pruebas voy a utilizar un proyecto Java normal y corriente con una sola clase.

File &gt; New... &gt; Java Project &gt; Nombre: PruebaGit

Click con el botón derecho encima del proyecto, New &gt; Class:

<ul>
	<li>Nombre: PruebaGit</li>
	<li>Paquete: es.aguasnegras.pruebagit</li>
	<li>Se marca también la generación de main.</li>
</ul>

<a href="images/2011/08/TutorialGit1.png"><img class="size-medium wp-image-213" title="Configuración del Proyecto Java de Pruebas" src="/images/2011/08/TutorialGit1-227x300.png" alt="Configuración del Proyecto Java de Pruebas" width="227" height="300" /></a>

<a href="images/2011/08/TutorialGit2.png"><img class="size-medium wp-image-214" title="Tutorial Git 2 - Clase Java de Pruebas" src="/images/2011/08/TutorialGit2-250x300.png" alt="Clase Java de Pruebas" width="250" height="300" /></a>

<a href="images/2011/08/TutorialGit3.png"><img class="size-medium wp-image-215" title="Tutorial Git 3 - Clase Java de Pruebas en el Editor de Eclipse" src="/images/2011/08/TutorialGit3-300x233.png" alt="Clase Java de Pruebas en el Editor de Eclipse" width="300" height="233" /></a>

<strong>Añadir el proyecto a un repositorio de Git.</strong>

Click con el botón derecho encima del proyecto, Team &gt; Share Project... Selecciono Git &gt; Next. En esta pantalla marco "Use or create repository in parent folder of the project", si no existe el repositorio, debajo selecciono el proyecto y le doy a "Create repository". Finish.

<a href="images/2011/08/TutorialGit3a.png"><img class="size-medium wp-image-216" title="Tutorial Git 4 - Configuración del Repositorio de Git" src="/images/2011/08/TutorialGit3a-300x167.png" alt="Configuración del Repositorio de Git" width="300" height="167" /></a>

<a href="images/2011/08/TutorialGit4.png"><img class="size-medium wp-image-217" title="Tutorial Git 5 - Repositorio de Git Creado" src="/images/2011/08/TutorialGit4-300x167.png" alt="Repositorio de Git Creado" width="300" height="167" /></a>

Ahora, creo el archivo .gitignore. En este archivo se pondrán todos los archivos y directorios que queremos que no se añadan al control de versiones. En este caso será el directorio bin y los propios del proyecto de Eclipse (.classpath, .settings y .project).

Click con el botón derecho encima del proyecto, New &gt; File &gt; Name: .gitignore y Finish.

<a href="images/2011/08/TutorialGit5.png"><img class="size-medium wp-image-218" title="Tutorial Git 6 - Creación de .gitignore" src="/images/2011/08/TutorialGit5-259x300.png" alt="Creación de .gitignore" width="259" height="300" /></a>

Se abre el archivo para editar y pongo las entradas de arriba cada una en una línea.

<strong>Añadiendo y borrrando archivos.</strong>

Con esto ya esta todo configurado y listo para empezar a trabajar. Antes hay que entender un poco como funciona Git. En Git, los archivos tienen tres estados:

<ul>
	<li>Sin Modificar</li>
	<li>Modificados</li>
	<li>Staging (han sido modificados y además serán incluidos en el próximo commit al repositorio).</li>
</ul>

Por tanto, ahora mismo lo tengo todo en modificado, hay que añadirlo a Staging... click con el botón derecho en el proyecto, Team &gt; Add y sale una cruz verde, ya estan en Staging, ahora commit.

Click con el botón derecho en el proyecto, Team &gt; Commit, si todo ha ido bien, vemos la pantalla de commit, con el autor y el email completados. En mi caso, se ve también el .project porque se me escapó del .gitignore ;)

<a href="images/2011/08/TutorialGit6.png"><img class="size-medium wp-image-219" title="Tutorial Git 7 - Commit inicial del proyecto" src="/images/2011/08/TutorialGit6-300x279.png" alt="Commit inicial del proyecto" width="300" height="279" /></a>

Cambio ahora el main:

```prettyprint linenums
 public static void main(String[] args) {
	System.out.println("Subversion, tu antes molabas");
}
```

Para comparar los cambios (diff): click con el botón derecho en el proyecto, Team &gt; Synchronize Workspace.
En esta perspectiva (Team Synchronizing Perspective) tengo en el árbol de directorio tan solo los archivos que tienen cambios con respecto al repositorio, expando y doble click en PruebaGit.java. Se abre el Compare Editor y ahí tengo a la izquierda mi copia local, a la derecha lo que hay en el repositorio.

<a href="images/2011/08/TutorialGit7.png"><img class="size-medium wp-image-220" title="Tutorial Git 8 - Diff de dos archivos" src="/images/2011/08/TutorialGit7-300x233.png" alt="Diff de dos archivos" width="300" height="233" /></a>

Ahora voy a crear un "propiedades.properties", lo voy a añadir y lo voy a borrar. Para ello, creo el archivo, igual que hice con el .gitignore y hago commit. ¿Para borrar? Lo borro (click con el botón derecho &gt; delete) y a continuación, hago commit de nuevo. Listo, para comprobarlo, click con el botón derecho en el proyecto, Team &gt; Show in History. Selecciono el último commit y abajo a la derecha se observa que se ha borrado propiedades.properties.

<a href="images/2011/08/TutorialGit8.png"><img class="size-medium wp-image-221" title="Tutorial Git 9 - Borrado de un archivo" src="/images/2011/08/TutorialGit8-300x233.png" alt="Borrado de un archivo" width="300" height="233" /></a>

Hasta el momento, he trabajado siempre en local, es decir, contra el repositorio que hay en mi misma máquina, pero, ¿cómo lo subo a la nube?... Enter <a title="GitHub" href="http://www.github.com/" target="_blank">GitHub</a>!

<strong>Subir el repositorio a GitHub.</strong>

Accedo a mi cuenta de GitHub y le doy a Dashboard. Dentro del Dashboard, creo un repositorio nuevo (create repository):

<ul>
	<li>Project Name: PruebaGit</li>
	<li>Description: Ejemplo de uso de Git</li>
</ul>

Click en create repository y listo. En la siguiente página, lo importante es hacer click en http, para que me dé un enlace http al repositorio (lo más normal es que cualquier firewall/proxy corte el protocolo git).

<a href="images/2011/08/TutorialGit9.png"><img class="size-medium wp-image-222" title="Tutoria lGit 10 - Creación del repositorio en GitHub" src="/images/2011/08/TutorialGit9-300x213.png" alt="Creación del repositorio en GitHub" width="300" height="213" /></a>

Ahora, en el eclipse, click con el botón derecho encima del proyecto, Team &gt; Remote &gt; Push... En esta pantalla, introduzco la URI (http) que me ha dado GitHub e introduzco mi contraseña de GitHub.

<a href="images/2011/08/TutorialGit10.png"><img class="size-medium wp-image-223" title="Tutorial Git 11 - Subir el proyecto a GitHub" src="/images/2011/08/TutorialGit10-283x300.png" alt="Subir el proyecto a GitHub" width="283" height="300" /></a>

En la siguiente pantalla, escojo que quiero enviar y a donde, en mi caso particular, me basta con enviar mi master a su master. Los escojo y hago click en "Add Spec".

<a href="images/2011/08/TutorialGit11.png"><img class="size-medium wp-image-224" title="Tutorial Git 12 - Escoger que rama se quiere subir a GitHub" src="/images/2011/08/TutorialGit11-283x300.png" alt="Escoger que rama se quiere subir a GitHub" width="283" height="300" /></a>

A continuación puedo darle a "Next" para ver la pantalla de confirmación y pulsar "Finish".

<a href="images/2011/08/TutorialGit12.png"><img class="size-medium wp-image-225" title="Tutorial Git 13 - Finalizar subida de repositorio a GitHub" src="/images/2011/08/TutorialGit12-283x300.png" alt="Finalizar subida de repositorio a GitHub" width="283" height="300" /></a>

<a href="images/2011/08/TutorialGit13.png"><img class="size-medium wp-image-226" title="Tutorial Git 14 - Confirmar Subida del Proyecto a GitHub" src="images/2011/08/TutorialGit13-283x300.png" alt="Confirmar Subida del Proyecto a GitHub" width="283" height="300" /></a>

En GitHub voy a mi Dashboard, hago click encima del repositorio PruebaGit y veo que, efectivamente ya están ahí mis archivos.

<a href="images/2011/08/TutorialGit14.png"><img class="size-medium wp-image-227" title="Tutorial Git 15 - Proyecto en GitHub" src="http://www.aguasnegras.es/blog/wp-content/uploads/2011/08/TutorialGit14-300x213.png" alt="Proyecto en GitHub" width="300" height="213" /></a>

Para subir archivos, muy sencillo, click con el botón derecho encima del proyecto, Team &gt; Remote &gt; Push...

Para traer los cambios, igual, pero con pull: click con el botón derecho encima del proyecto, Team &gt; Remote &gt; Pull...

Y con esto, ya se ha cubierto la funcionalidad básica de Git, trabajo con el repositorio local, añadir, modificar y borrar archivos y subir a un repositorio remoto.

Ya en otro veré como manejar ramas, etc...
