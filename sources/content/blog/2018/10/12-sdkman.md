title=SDKMAN
date=2018-10-12
type=post
tags=Java
status=published
~~~~~~
[SDKMAN](https://sdkman.io/) es un gestor de entornos y herramientas Java. Cuando trabajas en un entorno "corporativo" (¿aburrido?) sueles tener claramente fijadas las versiones de herramientas de desarrollo a utilizar, por ejemplo, Java 8 en la versión 1.8.0_121 o Maven 3.2.1, etc...
Sin embargo cuando empiezas a cacharrear y a tratar de instalar cosas nuevas es relativamente normal que acabes con dos (o tres o seis) versiones del JDK: la "buena" (1.8), la de "los módulos" (9), la de "los val" (10) y la "nueva buena" (11). Todo eso puedes gestionarlo a mano, claro, para eso esta JAVA_HOME, pero ¿qué pasa si tienes varias versiones de Maven? ¿Y si son más herramientas? Ya se empieza a hacer cansino. Pues bien, SDKMAN se ocupa precisamente de eso, lo instalas y él te instala las versiones que quieras de las herramientas, te pone unas activas, etc...
Pero mejor enseño un ejemplo.
##Instalación
Pues basta con seguir las [instrucciones](https://sdkman.io/install). Yo como soy un poco particular y maniático, me gusta tener todo lo relacionado con el desarrollo ordenado en carpetas particulares, así que para la instalación especifico primero el directorio en el que quiero que me lo instale y después lanzo el script de instalación:

```prettyprint
export SDKMAN_DIR="/home/agustin/Development/Java/Tools/sdkman"
curl -s "https://get.sdkman.io" | bash
source Development/Java/Tools/sdkman/bin/sdkman-init.sh
```

Con ésto ya esta instalado (en el directorio Development/Java/Tools/sdkman).

##Uso
Vale, pues lo primero es comprobar que esta bien:

```prettyprint
sdk help
```

Una vez instalado, se puede ver todo el software disponible con list:

```prettyprint
sdk list
```

Y todas las versiones de un software concreto con list <software>:

```prettyprint
sdk list java
```

Para instalar Java 11 (OpenJDK):

```prettyprint
sdk install java 11.0.0-open
```

Y con ésto, java -version te debe devolver OpenJDK 11 (es posible que tengas que abrir un terminal nuevo).

##Desinstalación
Si por lo que sea te cansas de SDKMAN, la desinstalación son dos pasos:
1. Borrar el directorio de instalación (.sdkman en tu home por defecto)
2. Repasar .bashrc, .bash_profile o .profile para ver que no haya quedado rastro.