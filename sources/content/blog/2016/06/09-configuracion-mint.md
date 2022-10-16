title=Configuración de Linux Mint
date=2016-06-09
type=post
tags=Linux
status=published
~~~~~~
Aprovechando que he actualizado el portátil (le he puesto 16 Gb de RAM y un SSD de 240 Gb), voy a documentar un poco mi configuración para que no se me vuelva a olvidar.
En primer lugar he instalado el último Linux Mint disponible, el 17.3 Rosa. No soy un gran fan de Mint (de hecho me parece que gráficamente hablando se han quedado un poco desfasados).
Una vez instalado he dado los siguientes pasos:

1. Actualizar el sistema: apt-get update && apt-get upgrade
2. Instalar los últimos drivers de nvidia a través del mismo Administrador de controladores de Mint. Con eso y reiniciando ya me encuentra el HDMI (cosas de tener una tarjeta gráfica dual) y por tanto puedo usar el monitor de 23".
3. Instalar los drivers del adaptador wifi usb. El adaptador wifi de mi portátil deja bastante que desear, así que habitualmente uso un d-link usb para el wifi. La cosa es que el driver que trae por defecto Ubuntu (y Mint por extensión) es bastante malo (MUY malo), pero afortunadamente la comunidad se ha currado un driver mejor, [éste](https://github.com/pvaret/rtl8192cu-fixes)
4. Instalar vim.
5. Desactivar la gestión de energía del wifi usb (wlan1) para que siempre vaya al máximo. Consume más, pero la verdad, la batería del portátil ya es vieja y dura media hora, así que me dá igual xD. En fín, me creo un script que lo desactivará en cada inicio: sudo vi sudo touch /etc/pm/power.d/wireless. Y ahí pongo las siguientes dos líneas:

```prettyprint
#!/bin/sh
/sbin/iwconfig wlan0 power off
```

Por último, le cambio los permisos a 755: sudo chmod 755 /etc/pm/power.d/wireless y listo.
6. Deshabilitar la tarjeta wifi por defecto: añado iface wlan0 inet manual a /etc/network/interfaces
7. En Configuración del Sistema > Apariencia > Efectos, desactivar
8. En Configuración del Sistema > Preferencias > Ajuste de ventanas, desactivar
9. En Configuración del Sistema > Preferencias > Escritorio, desactivar mostrar iconos de escritorio
10. Instalar Chrome
11. Instalar Atom
12. Instalar terminator
13. Instalar Java. Seamos sinceros, el OpenJDK por no hablar del IceTea son reguleros, así que instalo el Java oficial de Oracle usando el PPA de [Webupd8](http://www.webupd8.org/2012/09/install-oracle-java-8-in-ubuntu-via-ppa.html)

Y ahora vamos con una lista de consejos sacados de [Easy Linux Tips](https://sites.google.com/site/easylinuxtipsproject) y aplicados según mi buen criterio:

1. Disminuir lo proclive que es el sistema a usar la SWAP, sobre todo ahora que tengo 16 Gb de RAM. El swappiness es un parámetro del 0 al 100, así que lo voy a dejar en 5. Para eso edito el archivo /etc/sysctl.conf y al final pongo el parámetro vm.swappiness=5
2. Otra opción a tunear ahí es el uso de la caché. El procesador usa una caché de datos y otra de inodes (información del sistema de ficheros). Habitualmente tiene prioridad total la de datos, pero en equipos de escritorio se [recomienda](http://bicosyes.com/2007/10/mejorando-rendimiento-en-linux-de-escritorio/) ponerlo al 50. Para eso se usa el parámetro vm.vfs_cache_pressure=50 en /etc/sysctl.conf.
3. Desactivar la hibernación. Bueno, lo de hibernar los equipos me parece una soberana gilipollez (así de claro), así que lo desactivo ejecutando ésto: sudo mv -v /etc/polkit-1/localauthority/50-local.d/com.ubuntu.enable-hibernate.pkla / sencillamente muevo el archivo de configuración a root, así ya no lo encuentra y listo
4. Ahora vamos con el tuneo específico para el SSD, que es la primera vez que lo hago. En primer lugar, le añado noatime en /etc/fstab a las dos particiones ext4 que tengo (/ y /home), de esta manera, no se escribirá la hora de acceso a los ficheros en el disco y me ahorro escrituras (que son satán para los SSD). Los vuelvo a montar con sudo mount -a
5. TRIM es un comando que sirve para optimizar el uso y acceso de la SSD y en general mantener la velocidad. Bueno, pues por lo visto en Ubuntu y Mint se ejecuta a través de un cron semanal (bieeeeennn old school total). Lo voy a pasar a rc.local para que se ejecute en cada arranque y listo. Edito /etc/rc.local y añado dos líneas: fstrim / y fstrim /home antes del exit 0. Por último, desactivo el cron, sencillamente muevo el script de sitio: sudo mv -v /etc/cron.weekly/fstrim /fstrim

Ahora unos trucos para acelerar el arranque:
1. Deshabilitar la splash screen, a mí de todas formas no me gusta, prefiero ver el proceso de arranque. Edito la configuración de grub en /etc/default/grub y la línea GRUB_CMDLINE_LINUX_DEFAULT="quiet splash" la cambio por GRUB_CMDLINE_LINUX_DEFAULT="profile". De esa manera puedo controlar el proceso de arranque y además me hace un profiling para acelerarlo un poco.
2. Instalo bum (bootup manager) y desactivo varios servicios que vienen activos y que no uso: openvpn, virtualbox-guest-utils y saned.

Y por último, las chorradas:
1. Instalar grub-customizer para poner bonito el grub sin tener que usar la línea de comando. Ponerle una imagen, etc...
2. Instalar el conky y ajustar el .conkyrc
