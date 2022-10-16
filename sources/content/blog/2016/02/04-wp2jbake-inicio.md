title=Wordpress to JBake - Inicio
date=2016-02-04
type=post
tags=Java, JBake, Wordpress
status=published
~~~~~~
En la migraci&oacute;n del blog a GitHub Pages uno de los objetivos era no perder contenido, por lo que una vez puesta en pie toda la infraestructura, toca migrar los posts (mucho me temo que los comentarios si se van a perder...). Soluci&oacute;n: Hacer un peque&ntilde;o programa en Java (casi que dir&iacute;a script) que realice autom&aacute;ticamente esta conversi&oacute;n, adem&aacute;s voy a seguir TDD para "mantenerme en forma".
En un principio lo voy a plantear como una mera conversi&oacute;n de formatos, como formato inicial tengo el que devuelve Wordpress para la exportaci&oacute;n: [Wordpress Extended RSS](http://devtidbits.com/2011/03/16/the-wordpress-extended-rss-wxr-exportimport-xml-document-format-decoded-and-explained/) y como formato final quiero un archivo en el formato espec&iacute;fico de JBake, que no deja de ser [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) con unas cabeceras (metadata) particulares:

1. title: El t&iacute;tulo del post
2. date: La fecha del post
3. type: Ser&aacute; siempre post
4. tags: Las etiquetas del post
5. status: Ser&aacute; siempre published

El WXR es un solo archivo con una serie de elementos item que corresponde cada uno a un post, un elemento item tiene los siguientes campos interesantes:

1. title: casa con la cabecera title que quiero
2. pubdate: casa con la cabecera date
3. category: Las categor&iacute;as se dividen en dominios que puede ser category (bien Wordpress, bien) o post_tag, en concreto me interesan solo aquellas de tipo post_tag y su contenido, es decir tendr&eacute; que concatener el contenido de todas las categor&iacute;as de tipo post_tag.
4. content: Este es el contenido el post en s&iacute;, como se puede ver viene en HTML tal cual dentro de un CDATA, esto me permite aprovechar que con Markdown puedo utilizar el HTML inline as&iacute; que en un principio lo voy a volcar tal cual, aunque preveo ciertos problemas con las etiquetas de c&oacute;digo...

Por &uacute;ltimo, por cada item quiero generar un archivo con el nombre dd-title.md (donde dd es el d&iacute;a de la fecha) dentro de una carpeta mm (mes) dentro de una carpeta aaaa (a&ntilde;o...).

Pues con esto, empezamos!! Primero: crear el projecto en Intellij y con Maven, creo el repositorio en [GitHub](https://github.com/agustinventura/wp2jbake) y lo a&ntilde;ado.
A continuaci&oacute;n, actualizo el .gitignore, hago el commit inicial y cambio a la rama development.

El comienzo es un no brainer, necesito un main que arranque la aplicaci&oacute;n como tal y que recibir&aacute; como par&aacute;metros:

* El nombre del archivo WXR
* El directorio de salida

Eso quiere decir que la clase de entrada a la aplicaci&oacute;n (Wp2JBake) tendr&aacute; un constructor con dos par&aacute;metros, as&iacute; que siguiendo TDD, empiezo con los tests:

1. Construir con los par&aacute;metros a null.
2. Construir con el archivo origen a null.
3. Construir con el directorio destino a null.

En todos estos casos lanzar&eacute; una InvalidArgumentException, as&iacute; que inicialmente tendr&iacute;a como pruebas algo as&iacute;:

```prettyprint
private Wp2JBake sut;

@Test(expected = IllegalArgumentException.class)
public void buildWithoutParameters() {
    sut = new Wp2JBake(null, null);
}

@Test(expected = IllegalArgumentException.class)
public void buildWithoutOrigin() {
    sut = new Wp2JBake(null, "");
}

@Test(expected = IllegalArgumentException.class)
public void buildWithoutDestination() {
    sut = new Wp2JBake("", null);
}
```

Y como implementaci&oacute;n lo siguiente:

```prettyprint
public Wp2JBake(String origin, String destination) {
    if (origin == null) {
        throw new IllegalArgumentException("Origin is not a valid file");
    }
    if (destination == null) {
        throw new IllegalArgumentException("Destination is not a valid folder");
    }
}
```

Pero... un segundo, &iquest;me d&aacute; igual la IllegalArgumentException que se lanza? No, en cada caso quiero verificar que se esta lanzando la que se debe, refactorizo las pruebas, ahora voy a utilizar un @Rule de JUnit para comprobar que se lanza la excepci&oacute;n y el mensaje de error:

```prettyprint
@Rule
public ExpectedException thrown = ExpectedException.none();

private Wp2JBake sut;

@Test
public void buildWithoutParameters() {
    thrown.expect(IllegalArgumentException.class);
    thrown.expectMessage("Origin");
    sut = new Wp2JBake(null, null);
}

@Test
public void buildWithoutOrigin() {
    thrown.expect(IllegalArgumentException.class);
    thrown.expectMessage("Origin");
    sut = new Wp2JBake(null, "foo");

}

@Test
public void buildWithoutDestination() {
    thrown.expect(IllegalArgumentException.class);
    thrown.expectMessage("Destination");
    sut = new Wp2JBake("foo", null);
}
```

Vale, ya he controlado que no sea null, ahora toca comprobar que tampoco sea cadena vac&iacute;a:

```prettyprint
 @Test
public void buildWithEmptyOrigin() {
    thrown.expect(IllegalArgumentException.class);
    thrown.expectMessage("Origin");
    sut = new Wp2JBake("", "");
}

@Test
public void buildWithEmptyDestination() {
    thrown.expect(IllegalArgumentException.class);
    thrown.expectMessage("Destination");
    sut = new Wp2JBake("foo", "");
}
```

Ahora toca cambiar la implementaci&oacute;n, me voy a apoyar en las commons-lang:

```prettyprint
public Wp2JBake(String origin, String destination) {
    if (StringUtils.isEmpty(origin)) {
        throw new IllegalArgumentException("Origin is not a valid file");
    }
    if (StringUtils.isEmpty(destination)) {
        throw new IllegalArgumentException("Destination is not a valid folder");
    }
}
```

Siguiente restricci&oacute;n, el origen adem&aacute;s debe existir:

```prettyprint
@Test
public void buildWithInvalidOrigin() {
    thrown.expect(IllegalArgumentException.class);
    thrown.expectMessage("Origin");
    sut = new Wp2JBake("foo", "");
}
```

Y la implementaci&oacute;n:

```prettyprint
public Wp2JBake(String origin, String destination) {
    if (StringUtils.isEmpty(origin) || !existsOrigin(origin)) {
        throw new IllegalArgumentException("Origin is not a valid file");
    }
    if (StringUtils.isEmpty(destination)) {
        throw new IllegalArgumentException("Destination is not a valid folder");
    }
}

private boolean existsOrigin(String origin) {
    File originFile = new File(origin);
    return originFile.exists();
}
```

Esta implementaci&oacute;n hace saltar las pruebas de origen inv&aacute;lido, claro como para "callar" los tests estoy pasando como primer par&aacute;metro una cadena cualquiera, ahora falla porque no existe el par&aacute;metro foo.
Aqu&iacute; hay dos opciones:

1. Pasar un archivo que si exista.
2. Cambiar la implementaci&oacute;n para que primero compruebe que la cadena es v&aacute;lida en los dos casos y despu&eacute;s que compruebe si el archivo es v&aacute;lido.

El problema de 2 es que tendr&iacute;a que lanzar la misma excepci&oacute;n dos veces mientras que el de 1 es que se parecer&iacute;a m&aacute;s a un test de integraci&oacute;n que a una prueba unitaria en s&iacute;. Para mi gusto esta es una de las zonas grises en TDD, porque, &iquest;ahora qu&eacute; hago?&iquest;Creo un mock del SUT? No lo veo claro,
as&iacute; que tratar&eacute; de tirar por el camino del medio y pasar una ruta de archivo que sepa que siempre existe, por ejemplo, el pom.xml.

Ahora podr&iacute;a seguir comprobando que el destino no sea inv&aacute;lido, pero... &iquest;puede serlo? Al ser un directorio, si no existe, deber&iacute;a crearlo y si existe, no hacer nada. En todo caso la comprobaci&oacute;n deber&iacute;a ser si se puede crear el directorio y si se puede escribir en &eacute;l.

De aqu&iacute; saco estas dos pruebas:

```prettyprint
@Test
public void buildWithNonWritableDestination() {
    File destination = new File("destination");
    destination.mkdir();
    destination.deleteOnExit();
    destination.setReadOnly();
    thrown.expect(IllegalArgumentException.class);
    thrown.expectMessage("Destination");
    sut = new Wp2JBake("pom.xml", destination.getAbsolutePath());
}

@Test
public void buildWithNonWritableDestinationParent() {
    File destinationParent = new File("destinationParent");
    destinationParent.mkdir();
    destinationParent.deleteOnExit();
    destinationParent.setReadOnly();
    thrown.expect(IllegalArgumentException.class);
    thrown.expectMessage("Destination");
    sut = new Wp2JBake("pom.xml", destinationParent.getAbsolutePath() + File.separator + "destination");
}
```

Y la implementaci&oacute;n sigue creciento:

```prettyprint
public Wp2JBake(String origin, String destination) {
    if (StringUtils.isEmpty(origin) || !existsOrigin(origin)) {
        throw new IllegalArgumentException("Origin is not a valid file");
    }
    if (StringUtils.isEmpty(destination) || !isWritable(destination)) {
        throw new IllegalArgumentException("Destination is not a valid folder");
    }
}

private boolean isWritable(String destination) {
    File destinationFolder = new File(destination);
    if (destinationFolder.exists()) {
        return destinationFolder.canWrite();
    } else {
        return destinationFolder.getParentFile().canWrite();
    }
}

private boolean existsOrigin(String origin) {
    File originFile = new File(origin);
    String path = originFile.getAbsolutePath();
    return originFile.exists();
}
```

Por &uacute;ltimo me quedar&iacute;a probar el caso en el que ambos par&aacute;metros son v&aacute;lidos:

```prettyprint
@Test
public void buildWithValidParameters() {
    sut = new Wp2JBake("pom.xml", "destination");
    File destination = new File("destination");
    destination.delete();
}
```

Con esto puedo empezar a refactorizar y a remplatearme las cosas. La verdad que Wp2JBake empieza a tener un tama&ntilde;o considerable teniendo en cuenta que tan s&oacute;lo tiene como API un constructor. La verdad que las comprobaciones que estoy haciendo sobre los par&aacute;metros no me convencen, me dan la impresi&oacute;n de que estoy violando el Single Responsability, por otra parte ser&iacute;a un poco artificial crear una clase de validadores &uacute;nicamente.
