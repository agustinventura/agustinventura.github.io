title=Tizen Studio
date=2018-12-27
type=post
tags=Tizen, JavaScript
status=published
~~~~~~
A finales de 2017 participé en un concurso de Samsung llamado [Dispositivos por Apps](https://www.europe-samsung.com/smsdev/Home/Articulo/447) y que, mediante el regalo de dispositivos pretende aumentar la presencia de aplicaciones en el market propio de Samsung (Galaxy Apps).
El caso fue que que en aquel momento hice tres aplicaciones para relojes Samsung (y sin tener uno, jaja) y me saqué un reloj Samsung Gear Sport. Las aplicaciones en cuestión eran las siguientes:
<ul>
<li> [TabataTimer](https://github.com/agustinventura/TabataTimer): Un temporizador Tabata configurable, incluyendo número de rondas, duración del intervalo de trabajo y del intervalo de descanso.</li>
<li> [DiceRoller](https://github.com/agustinventura/DiceRoller): Un tirador de dados, por si te pilla en una partidilla de algo y no tienes a mano los dados, pues puedes seleccionar el tipo de dados y el número y la aplicación los "tira" por tí.</li>
<li> [SwimMonitor](https://github.com/agustinventura/SwimMonitor): La aplicación que creo que me quedó mejor de todas. Permite llevar el control de los largos que vas haciendo en la piscina y además revisar entrenamientos anteriores para poder compararlos.</li>
</ul>
Pues bien, ahora ha vuelto a salir la promoción y esta vez piden nada más y nada menos que seis aplicaciones, pero teniendo en cuenta que ya sé más o menos como funciona todo, creo que puedo sacarlas en las semanas que dan.

##Tizen Studio

Lo primero de todo es descargar el [Tizen Studio](https://developer.tizen.org/development/tizen-studio/download) en su versión de Ubuntu. El instalador pide dos dependencias:
<ul>
<li>libwebkitgtk-1.0-0: Que por fortuna se puede instalar con apt-get</li>
<li>rpm2cpio: Que también se puede instalar por apt-get</li>
</ul>

La instalación no tiene mucho más porque Tizen Studio es un Eclipse modificado.

![Tizen Studio](/images/2018/12/01-Tizen_Studio.png)

##Package Manager

Para instalar los distintos entornos de ejecución (y crear emuladores), hay que utilizar el Package Manager:

![Package Manager](/images/2018/12/02-Package_Manager.png)

En mi caso, repasando la paquetería disponible para wearables y web app development me llevo la grata sorpresa de que solo hay que instalar los emuladores. Repasando el Gear Sport, veo que la versión de Tizen que trae es la 3.0.0.2 y el Tizen Studio me ofrece hasta la 5, así que yo que sé, voy a instalar los emuladores de la 4 y la 5 y hago las aplicaciones de 3 para arriba.
Al darle a instalar me ha pedido una serie de paquetes extra del sistema operativo, en concreto:
<ul>
<li>libpng12-0</li>
<li>libsdl1.2debian</li>
<li>bridge-utils</li>
<li>openvpn</li>
</ul>
Y resulta que la primera no esta, así que toca buscar por Google y resulta que hay que [instalarla a mano](https://askubuntu.com/questions/840257/e-package-libpng12-0-has-no-installation-candidate-ubuntu-16-10-gnome)

Bueno, pues tras ésto ya se puede instalar tranquilamente y ya tenemos nuestros emuladores.

![Tizen Emulators](/images/2018/12/03-Tizen_Emulator.png)