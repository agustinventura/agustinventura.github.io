title=Sun Java y OpenJDK en Linux
date=2011-11-11
type=post
tags=Heroku,Java,Programación
status=published
~~~~~~
Para trabajar con Heroku, recomiendan usar OpenJDK, sin embargo, hasta el momento vengo usando el Sun JDK, así que voy a instalar el OpenJDK:

```prettyprint linenums
$ sudo apt-get install openjdk-6-jdk
```

Con esto se instala el OpenJDK 6, pero con un desafortunado efecto secundario:

```prettyprint linenums
$ java -version
java version "1.6.0_22"
OpenJDK Runtime Environment (IcedTea6 1.10.2) (6b22-1.10.2-0ubuntu1~11.04.1)
OpenJDK 64-Bit Server VM (build 20.0-b11, mixed mode)
```

Efectivamente, se ha establecido el OpenJDK como máquina virtual de Java por defecto, pero esto no es lo que quiero (al menos, yo no), me gustaría seguir usando el Sun JDK. Afortunadamente, qué JDK usar esta regido por el <a title="Linux Alternatives System" href="http://alternatives.sourceforge.net/" target="_blank">Linux Alternatives System</a>, que básicamente es un sistema para poder cambiar entre varias implementaciones de un mismo programa, y Ubuntu trae un programa que se llama update-java-alternatives que te sirve para cambiar, en mi caso ha sido:

```prettyprint linenums

$ sudo update-java-alternatives -s java-6-sun

```

Listo, ahora ya:

```prettyprint linenums

$ java -version
java version "1.6.0_26"
Java(TM) SE Runtime Environment (build 1.6.0_26-b03)
Java HotSpot(TM) 64-Bit Server VM (build 20.1-b02, mixed mode)

```
