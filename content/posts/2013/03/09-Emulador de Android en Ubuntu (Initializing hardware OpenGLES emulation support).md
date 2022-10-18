---
title: Emulador de Android en Ubuntu (Initializing hardware OpenGLES emulation support)
date: 2013-03-09
tags:
  - Android
  - Emulador
  - Problemas
  - Programación
  - Tools of the Trade
---
A veces (normalmente en una instalación nueva), los emuladores de Android no arrancan en Ubuntu de 64 bits debido a un error con OpenGLES.

Para comprobar si la solución es aplicable, hay que ejecutar este comando desde la consola:

```shell
$ ./emulator -avd GalaxyS -verbose
```

Donde GalaxyS será el nombre del avd que se desee arrancar, al final del log deberemos ver algo así:

```shell
emulator: Initializing hardware OpenGLES emulation support
Violación de segmento (`core' generado)
```

El problema y su solución se encuentra reportado <a title="Android Issue 34233" href="http://code.google.com/p/android/issues/detail?id=34233" target="_blank">aquí</a>.

Básicamente la solución consiste en lo siguiente:

```shell
$ cd $ANDROID_SDK/tools/lib
$ mv libOpenglRender.so libOpenglRender.so.bak
```

Y listo.