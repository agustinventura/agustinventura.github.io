title=Emulador de Android en Ubuntu (Initializing hardware OpenGLES emulation support)
date=2013-03-09
type=post
tags=Android,Emulador,Problemas,Programación,Tools of the Trade
status=published
~~~~~~
A veces (normalmente en una instalación nueva), los emuladores de Android no arrancan en Ubuntu de 64 bits debido a un error con OpenGLES.

Para comprobar si la solución es aplicable, hay que ejecutar este comando desde la consola:

```prettyprint linenums
$ ./emulator -avd GalaxyS -verbose
```

Donde GalaxyS será el nombre del avd que se desee arrancar, al final del log deberemos ver algo así:

```prettyprint linenums
emulator: Initializing hardware OpenGLES emulation support
Violación de segmento (`core' generado)
```

El problema y su solución se encuentra reportado <a title="Android Issue 34233" href="http://code.google.com/p/android/issues/detail?id=34233" target="_blank">aquí</a>.

Básicamente la solución consiste en lo siguiente:

```prettyprint linenums
$ cd $ANDROID_SDK/tools/lib
$ mv libOpenglRender.so libOpenglRender.so.bak
```

Y listo.