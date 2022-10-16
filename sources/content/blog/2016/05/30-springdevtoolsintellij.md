title=Spring Boot Developer Tools e Intellij IDEA
date=2016-05-30
type=post
tags=Java, Spring, Intellij IDEA
status=published
~~~~~~
Una de las mejores incorporaciones que tuvo Spring Boot en la versión 1.3 fueron las [Developer Tools](https://spring.io/blog/2015/06/17/devtools-in-spring-boot-1-3).
De entre toda la funcionalidad, lo que me parece mas útil es sin lugar a dudas el automatic restart, que relanza la aplicación en cuanto detecta cambios en un
fichero que esta en el classpath y el LiveReload, que en conjunción con un plugin de Chrome detecta cuando ha habido cambios en la aplicación (como un reinicio)
y refresca automáticamente la página.

Juntando estas dos cosas, y dejando de lado el consumo de recursos, codificar en Java se convierte prácticamente en lo mismo que trabajar con un lenguaje de scripting
como PHP.

Sin embargo, el soporte de los developers tools no es automático del todo en Intellij IDEA, el IDE que más suelo utilizar en casa, para ello hay que [habilitar
dos opciones](https://patrickgrimard.io/2016/01/18/spring-boot-devtools-first-look/):

1. En Settings (ctrl-alt-s) > Build, Execution, Deployment > Compiler hay que marcar "Make project automatically"
2. En el registro que se puede acceder mediante ctrl-shift-a y buscando "Registry" hay que habilitar la clave compiler.automake.allow.when.app.running para que el
automake funcione también mientras la aplicación esta arrancada.

Con ésto, y si tenemos un equipo suficientemente potente (aunque mi portátil tiene ya 5 años lo mueve bastante bien), cualquier cambio en nuestras clases se cargará
automáticamente al reiniciar la aplicación. Eso sí, dado que Intellij IDEA guarda automáticamente los archivos cuando detecta cambios, esto puede dar lugar a algunos
errores o reinicios en falso (por ejemplo, cuando estamos escribiendo un método y nos vamos a StackOverflow a resolver alguna duda). Para eso se pueden ajustar las
opciones de autosave tal y como se explica en la misma [documentación del IDE](https://www.jetbrains.com/help/idea/2016.1/saving-and-reverting-changes.html).
