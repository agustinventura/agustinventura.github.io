title=Wordpress to JBake - Parseo
date=2016-03-20
type=post
tags=Java, JBake, Wordpress
status=published
~~~~~~
Pues ahora que ya tengo el constructor y construyo un objeto siempre que, al menos es coherente, toca parsear el xml para extraer los datos.
En Java, esencialmente hay tres formas de parsear xml, todas dentro de lo que se denomina Java XML Processing API, [JAXP](https://docs.oracle.com/javase/tutorial/jaxp/index.html):

1. [SAX](https://docs.oracle.com/javase/tutorial/jaxp/sax/index.html): La API originaria, orientada a eventos. Muy rápida, muy eficiente y muy farragosa. Técnicamente es una API de streaming mediante push, es decir, nosotros arrancamos el procesamiento del documento y la API empieza a funcionar mandándonos eventos conforme va encontrando elementos.
2. [DOM](https://docs.oracle.com/javase/tutorial/jaxp/dom/index.html): La API orientada a objetos, representa el XML como un árbol en memoria. Muy fácil de acceder, muy tragón de recursos. Técnicamente, se representa el árbol del DOM en memoria y listo, se puede acceder libremente, por ejemplo usando XPath.
3. [StAX](https://docs.oracle.com/javase/tutorial/jaxp/stax/index.html): A partir del JDK 1.5 se encuentra disponible esta API que es un modelo mixto, se basa en un modelo de streaming (parecido a SAX) pero más sencillo de utilizar y además permite escribir. Técnicamente se define como una API de streming mediante pull, es decir, que somos nosotros los que vamos indicanto los elementos que queremos acceder. Eso sí, al ser de streaming solo permite avanzar en el documento, es decir, no podemos ignorar el elemento 1, tratar el 2 y en función de este retroceder a tratar el 1.

En mi caso en particular, y dado que el modelo de "ir hacia delante" se adapta perfectamente al caso de uso (ya que simplemente estoy emparejando), pero tampoco necesito tantísima eficiencia ni tengo ganas de fastidiarme la vida, voy a utilizar StAX.

Pero lo primero, ahora que tengo que trabajar "en serio" es utilizar datos de verdad para las pruebas. Para eso hay dos opciones:

1. Guardo un XML de pruebas en forma de un String en un archivo .java y lo leo de ahí.
2. Guardo un archivo XML como tal.

Pues como que la primera opción es una tontería, he optado por la segunda. He sacado la exportación de datos que proporciona Wordpress y he dejado unos cuantos posts que sean más o menos representativos y listo. Lo guardo en _src/resources/wp-source.xml_. Antes de seguir, ya no tiene sentido que los tests sigan usando el _pom.xml_ para las pruebas, así que lo cambio y lo lanzo. Todo en verde, como cabía esperar.

Ahora bien, ya tengo mi objeto de la clase Wp2JBake creado con el origen y el destino debidamente especificado, ¿como arranco el procesamiento? Hay que tener en cuenta que realmente el método de proceso no tiene por qué devolver nada, ya que el resultado efectivo de la salida es una estructura de archivos con el resultado de la conversión.
Sin embargo, creo que es "gratis" devolver los elementos que se han generado y así se posibilita poder comprobar el resultado de la generación.

Así que primero el test:

```prettyprint
@Test
public void processEmptyXML() {
    sut = new Wp2JBake("src/test/resources/empty.xml", "src/test/destination");
    Set<File> markdowns = sut.generateJBakeMarkdown();
    assertThat(markdowns, is(empty()));
    File destination = new File("destination");
    destination.delete();
}
```

Obviamente, esta en rojo, allá va la implementación:

```prettyprint
public Set<File> generateJBakeMarkdown() {
    return new HashSet<File>();
}
```

Y aquí, ya voy devolviendo un Set (porque todos los elementos serán distintos, cada archivo representa un post y cada post es único) y uso uno no ordenado, porque en realidad me dá igual el orden de iteración, ya que [como decidí](../02/04-wp2jbake.html) los archivos vendrán ordenados por su ruta, es decir, si existen, por definición estan ordenados.

Vale, y ahora, test de verdad:

```prettyprint
@Test
public void processXML() {
    sut = new Wp2JBake("src/test/resources/wp-source.xml", "src/test/destination");
    Set<File> markdowns = sut.generateJBakeMarkdown();
    assertThat(markdowns, is(not(empty())));
    for (File markdown: markdowns) {
        assertThat(markdown.exists(), is(true));
    }
    File destination = new File("destination");
    destination.delete();
}
```

Ahora tengo que modificar el método _generateJBakeMarkdown_ para que genere los archivos Markdown. En un principio hay dos formas de hacer ésto:

1. Parseo el XML, genero una estructura de datos en memoria (una representación de los posts, vaya) y después la recorro y la paso a los archivos markdown. Desventaja, que para eso para qué demonios uso StAX y el streaming, si voy a comer memoria uso DOM y listo.
2. Parseo el XML y cada vez que se detecte un item (un post) lo voy escribiendo dinámicamente. Creo que esta opción es más complicada, pero más ligera.

Vamos a por 2, para ello leeré el XML y lo volcaré... pero un momento, una cosa es saber leer el XML y otra escribir el Markdown, es decir, que mi clase lectora (_Wp2JBake_) a su vez debe comunicarse (usar) otra para escribir (_MdWriter_).
Pensando un poco más sobre esta clase _MdWriter_... debería recibir como parámetro en su constructor el destino de las escrituras y eso me lleva a pensar, que realmente es a ella a la que le corresponde comprobar si es un destino legal, es decir, que el constructor de _Wp2JBake_ ahora quedaría así (también he aprovechado y _origin_ lo he guardado en un atributo de la clase):

```prettyprint
public Wp2JBake(String origin, String destination) {
    if (StringUtils.isEmpty(origin) || !existsOrigin(origin)) {
        throw new IllegalArgumentException("Origin is not a valid file");
    } else {
        this.origin = origin;
    }
    this.mdWriter = new MdWriter(destination);
}
```

Mientras que _MdWriter_ sería así:

```prettyprint
public class MdWriter {

    private File destinationFolder;

    public MdWriter(String destination) {
        if (StringUtils.isEmpty(destination) || !isWritable(destination)) {
            throw new IllegalArgumentException("Destination is not a valid folder");
        } else {
            destinationFolder = new File(destination);
        }
    }

    private boolean isWritable(String destination) {
        File destinationFolder = new File(destination);
        if (destinationFolder.exists()) {
            return destinationFolder.canWrite();
        } else {
            return isWritableDestinationParent(destinationFolder);
        }
    }

    private boolean isWritableDestinationParent(File destinationFolder) {
        File destinationParent = getDestinationParent(destinationFolder);
        return destinationParent.canWrite();
    }

    private File getDestinationParent(File destinationFolder) {
        String parentPath = destinationFolder.getParent();
        if (parentPath == null) {
            parentPath = "";
        }
        return new File(parentPath);
    }
}
```

Por cierto que la teoría TDDista dice que esto no debería hacerse, que primero hay que pasar el test y después ponerse a refactorizar y tal... Hombre, yo eso no lo comparto tanto, creo que esta bien ir pensando un poco las cosas. Además, como ya tengo hechos los tests, los puedo volver a ejecutar para ver que no me he cargado nada.
Que hablando de las pruebas, ahora tengo que crear las pruebas propias de esta nueva clase y llevarme todas las encargadas de testear la corrección del directorio destino a esa clase. Al separarlo además ya no tengo que diferenciar entre los tipos de excepción (era muy cantoso que estaba pasando del Single Responsability) y el código queda mucho más limpio:

```prettyprint
public class Wp2JBakeTests {

    private Wp2JBake sut;

    @Test(expected = IllegalArgumentException.class)
    public void buildWithoutParameters() {
        sut = new Wp2JBake(null, null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void buildWithoutOrigin() {
        sut = new Wp2JBake(null, "foo");

    }

    @Test(expected = IllegalArgumentException.class)
    public void buildWithEmptyOrigin() {
        sut = new Wp2JBake("", "");
    }

    @Test(expected = IllegalArgumentException.class)
    public void buildWithInvalidOrigin() {
        sut = new Wp2JBake("foo", "");
    }

    @Test
    public void buildWithValidParameters() {
        sut = new Wp2JBake("src/test/resources/wp-source.xml", "src/test/destination");
    }

    @Test
    public void processEmptyXML() {
        sut = new Wp2JBake("src/test/resources/empty.xml", "src/test/destination");
        Set<File> markdowns = sut.generateJBakeMarkdown();
        assertThat(markdowns, is(empty()));
    }

    @Test
    public void processXML() {
        sut = new Wp2JBake("src/test/resources/wp-source.xml", "src/test/destination");
        Set<File> markdowns = sut.generateJBakeMarkdown();
        assertThat(markdowns, is(not(empty())));
        for (File markdown: markdowns) {
            assertThat(markdown.exists(), is(true));
        }
        File destination = new File("destination");
        destination.delete();
    }
}

public class MdWriterTest {

    private MdWriter sut;

    @Test(expected = IllegalArgumentException.class)
    public void writerWithoutDestination() {
        sut = new MdWriter(null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void writerWithEmptyDestination() {
        sut = new MdWriter("");
    }

    @Test(expected = IllegalArgumentException.class)
    public void writerWithNonWritableDestination() {
        File destination = new File("destination");
        destination.mkdir();
        destination.deleteOnExit();
        destination.setReadOnly();
        sut = new MdWriter(destination.getAbsolutePath());
    }

    @Test(expected = IllegalArgumentException.class)
    public void writerWithNonWritableDestinationParent() {
        File destinationParent = new File("destinationParent");
        destinationParent.mkdir();
        destinationParent.deleteOnExit();
        destinationParent.setReadOnly();
        sut = new MdWriter(destinationParent.getAbsolutePath() + File.separator + "destination");
    }
}
```

Bueno, pues ahora tengo que leer el XML e ir cargando los Strings que el escritor se encargará de volcar a disco... muy bien. Lo primer es crear la factoría de eventos. Por cierto, menuda bazofia el tutorial oficial de Oracle, menos mal que [Lars Vogel](http://www.vogella.com/tutorials/JavaXML/article.html)  tiene un grandísimo tutorial (danke schön Lars!):

```prettyprint
public Set<File> generateJBakeMarkdown() {
        XMLEventReader eventReader = getEventReader();
        return new HashSet<File>();
    }

    private XMLEventReader getEventReader() {
        XMLInputFactory inputFactory = XMLInputFactory.newInstance();
        InputStream in = null;
        XMLEventReader eventReader = null;
        try {
            in = new FileInputStream(origin);
            eventReader = inputFactory.createXMLEventReader(in);
        } catch (FileNotFoundException e) {
            throw new IllegalStateException("Could not find origin file: " + e.getMessage());
        } catch (XMLStreamException e) {
            throw new IllegalStateException("Could not read origin file: " + e.getMessage());
        }
        return eventReader;
    }
```

He optado por lanzar un IllegalStateException si ocurre alguna de las excepciones, ya que eso no debería ocurrir y a lo que lleva es exactamente a eso, un estado ilegal del programa :)
Hmmm... por otra parte, tengo la prueba con el XML vacío, pero ahora que lo pienso ¡¡¡no tengo ninguna con un XML inválido!!! Me creo un XML _invalid.xml_ que contiene solo la cabecera con un número de versión que no existe:

```prettyprint
<?xml version="-1.0" encoding="utf-8"?>
```

Y su test:

```prettyprint
@Test(expected = IllegalStateException.class)
public void processInvalidXML() {
    sut = new Wp2JBake("src/test/resources/invalid.xml", "src/test/destination");
    Set<File> markdowns = sut.generateJBakeMarkdown();
}
```

Me esta empezando a parecer que la lectura también debería ir en otra clase y _Wp2JBake_ tan solo orquestrar la lectura con la escritura... pero bueno, ya iremos viendo de momento sigo, así. Toca tratar los eventos. El tutorial hace un típico bucle while con el eventReader que implementa _Iterator_, pero claro, el tutorial es antiguo, al fin y al cabo y pensándolo bien... yo lo que quiero hacer es un filter y un collect, es decir, que puedo usar la API de Streams de Java 8. La única historia es convertir el _XMLEventReader_ a un _Stream<XMLEvent>_, pero eso es relativamente fácil:

```prettyprint
public Set<File> generateJBakeMarkdown() {
    XMLEventReader eventReader = getEventReader();
    Iterable<XMLEvent> eventsIterable = () -> eventReader;
    Stream<XMLEvent> xmlEvents = StreamSupport.stream(eventsIterable.spliterator(), false);
    return new HashSet<File>();
}
```

Bueno, pues después de echar hora y pico probando con filter, map, flatmap etc, hay un problema, y es que StAX entiende todo el documento secuencialmente, con lo cual no puedo hacer un filter y quedarme solo con los elemntos de tipo _item_ y después acceder a los elementos que contienen estos, porque un elemento esta suelto, así que nada, toca iteradores y bucles for de toda la vida. Para que sea más entendible (y orientado a objetos), me voy a crear una clase _Post_ para ir guardando los resultados y después volcarlos al archivo pertinente.
Esta clase la monto con una API fluida para que la construcción me sea más sencilla y los correspondientes getters:

```prettyprint
public class Post {
    private String title;

    private LocalDate publishingDate;

    private Set<String> tags = new TreeSet<>();

    private String content;

    public Post () {

    }

    public Post withTitle(String title) {
        this.title = title;
        return this;
    }

    public Post withPublishingDate(LocalDate publishingDate) {
        this.publishingDate = publishingDate;
        return this;
    }

    public Post withTag(String tag) {
        this.tags.add(tag);
        return this;
    }

    public Post withContent(String content) {
        this.content = content;
        return this;
    }

    public String getTitle() {
        return title;
    }

    public LocalDate getPublishingDate() {
        return publishingDate;
    }

    public Set<String> getTags() {
        return tags;
    }

    public String getContent() {
        return content;
    }
}
```

En fín, ya han pasado como tres horas y el test sigue sin funcionar... me deprimo...
Sigo con el for, la estrategia es muy sencilla, si detecto un elemento _item_, creo un nuevo _Post_ y conforme vaya detectando los elementos _title_, _pubDate_, _category_ y _content_ voy invocando a los métodos _with*_ del _Post_. En el momento que detecte el cierre del _item_, escribo a disco:

```prettyprint
public Set<File> generateJBakeMarkdown() {
    XMLEventReader eventReader = getEventReader();
    Iterable<XMLEvent> eventsIterable = () -> eventReader;
    Stream<XMLEvent> xmlEvents = StreamSupport.stream(eventsIterable.spliterator(), false);
    return new HashSet<File>();
}
```
Desafortunadamente, el tema es más complejo de lo que parecía. Dado que StAX solo lee en un sentido (palante), de poco me sirve la API de streams de Java 8, ya que tengo que ir tomando decisiones en función del elemento que llegue, por ejemplo, un elemento _title_ se debe ignorar salvo que previamente se haya recibido un _item_.
No digo que no sea posible hacerlo con streams, solo que después de muchos relíos es más sencillo hacerlo con dos while:

1. El primer while que itera sobre todos los elementos proporcionados por StAX.
2. El segundo while empieza cuando se detecta un _item_ y termina cuando se cierra el _item_, leyendo por tanto un post completo.

Con esto en mente es bastante fácil:

```prettyprint
public Set<File> generateJBakeMarkdown() {
        HashSet<File> exportResult = new HashSet<>();
        XMLEventReader eventReader = getEventReader();
        try {
            exportPosts(exportResult, eventReader);
        } catch (XMLStreamException e) {
            throw new IllegalStateException("Error reading XML " + origin + ": " + e.getMessage());
        }
        return exportResult;
    }

    private void exportPosts(HashSet<File> exportResult, XMLEventReader eventReader) throws XMLStreamException {
        Post post = null;
        while (eventReader.hasNext()) {
                XMLEvent event = eventReader.nextEvent();
                if (isPostStart(event)) {
                    post = exportPost(exportResult, eventReader, post);
                }
        }
    }

    private Post exportPost(HashSet<File> exportResult, XMLEventReader eventReader, Post post) throws XMLStreamException {
        if (post != null) {
            exportResult.add(mdWriter.write(post));
        }
        post = readPost(eventReader);
        return post;
    }

    private Post readPost(XMLEventReader eventReader) throws XMLStreamException {
        Post exportedPost = new Post();
        boolean postRead = false;
            while (!postRead && eventReader.hasNext()) {
                XMLEvent event = eventReader.nextEvent();
                if (event.isStartElement()) {
                    exportedPost = loadPostFromEvent(event, eventReader, exportedPost);
                } else if (isPostEnd(event)) {
                    postRead = true;
                }
            }
        return exportedPost;
    }

    private boolean isPostEnd(XMLEvent event) {
        return event.isEndElement() && "item".equals(event.asEndElement().getName().getPrefix() + event.asEndElement().getName().getLocalPart());
    }

    private boolean isPostStart(XMLEvent event) {
        return event.isStartElement() && "item".equals(getEventFullName(event));
    }

    private Post loadPostFromEvent(XMLEvent event, XMLEventReader eventReader, Post post) {
        String name = getEventFullName(event);
        try {
            switch (name) {
                case "title":
                    post = loadTitle(eventReader, post);
                    break;
                case "pubDate":
                    post = loadPublishingDate(eventReader, post);
                    break;
                case "category":
                    if (isTag(event)) {
                        post = loadCategory(eventReader, event, post);
                    }
                    break;
                case "contentencoded":
                    post = loadContent(eventReader, post);
                    break;
                default:
                    break;
            }
        } catch (XMLStreamException e) {
            throw new IllegalStateException("Error parsing " + name + ": " + e.getMessage());
        }
        return post;
    }

    private Post loadContent(XMLEventReader eventReader, Post post) throws XMLStreamException {
            return post.withContent(eventReader.nextEvent().asCharacters().getData());
    }

    private Post loadCategory(XMLEventReader eventReader, XMLEvent event, Post post) throws XMLStreamException {
            return post.withTag(eventReader.nextEvent().asCharacters().getData());
    }

    private Post loadPublishingDate(XMLEventReader eventReader, Post post) throws XMLStreamException {
            return post.withPublishingDate(parsePubDate(eventReader));
    }

    private Post loadTitle(XMLEventReader eventReader, Post post) throws XMLStreamException {
            return post.withTitle(eventReader.nextEvent().asCharacters().getData());
    }

    private String getEventFullName(XMLEvent event) {
        return event.asStartElement().getName().getPrefix() + event.asStartElement().getName().getLocalPart();
    }

    private boolean isTag(XMLEvent event) {
        return "post_tag".equals(event.asStartElement().getAttributeByName(new QName("domain")).getValue());
    }


    private Date parsePubDate(XMLEventReader eventReader) throws XMLStreamException {
        Date publishingDate = null;
        try {
            String pubDate = eventReader.nextEvent().asCharacters().getData();
            pubDate = extractDate(pubDate);
            SimpleDateFormat format = new SimpleDateFormat("dd MMM yyyy");
            publishingDate = format.parse(pubDate);
        } catch (ParseException e) {
            throw new IllegalStateException("Could not parse pubDate: " + e.getMessage());
        }
        return publishingDate;
    }

    private String extractDate(String pubDate) {
        //Date is supplied as this: Wed, 30 Nov -0001 00:00:00 +0000, we need to extract just the date
        pubDate = pubDate.substring(pubDate.indexOf(",")+2);
        int hourIndex = pubDate.indexOf(":")-3;
        pubDate = pubDate.substring(0, hourIndex);
        return pubDate;
    }

    private XMLEventReader getEventReader() {
        XMLInputFactory inputFactory = XMLInputFactory.newInstance();
        InputStream in = null;
        XMLEventReader eventReader = null;
        try {
            in = new FileInputStream(origin);
            eventReader = inputFactory.createXMLEventReader(in);
        } catch (FileNotFoundException e) {
            throw new IllegalStateException("Could not find origin file: " + e.getMessage());
        } catch (XMLStreamException e) {
            throw new IllegalStateException("Could not read origin file: " + e.getMessage());
        }
        return eventReader;
    }

    private boolean existsOrigin(String origin) {
        File originFile = new File(origin);
        String path = originFile.getAbsolutePath();
        return originFile.exists();
    }
```

Lo del parseo de la fecha ha sido un espectáculo... no he sido capaz de sacarlo con el DateFormatter para convertirlo a un LocalDate.
Bueno, pues ahora que lo tengo... ¿no tendría más sentido que todo eso fuera a una clase propia? Digamos WpReader. Pues sí, porque ahora mismo mi clase principal se esta responsabilizando de saber como se leen los posts y qué hacer con los posts leidos, así que es mucho más claro hacerlo con una colaboradora.
Pero claro, si me llevo la lógica aparte, ¿cómo aviso de que se puede escribir un nuevo post sin romper el while que itera sobre todos los elementos del XML?
Bueno, pues finamente diría que voy a usar un patrón observador, para notificar de cuando hay un nuevo post. Técnicamente lo que voy a hacer es implementar un callback y así _Wp2JBake_ queda mucho más clara:

```prettyprint
public class Wp2JBake {

    private WpReader wpReader;

    private MdWriter mdWriter;

    private HashSet<File> exportResult;

    public Wp2JBake(String origin, String destination) {
        this.wpReader = new WpReader(origin);
        this.mdWriter = new MdWriter(destination);
    }

    public Set<File> generateJBakeMarkdown() {
        exportResult = new HashSet<>();
        wpReader.readPosts(this);
        return exportResult;
    }

    public void postRead(Post post) {
        exportResult.add(mdWriter.write(post));
    }
}
```

Y por otro lado tenemos _WpReader_:

```prettyprint
public class WpReader {

    public static final String ITEM = "item";
    public static final String TITLE = "title";
    public static final String PUB_DATE = "pubDate";
    public static final String CATEGORY = "category";
    public static final String CONTENT = "contentencoded";
    public static final String POST_TAG = "post_tag";
    public static final String DOMAIN = "domain";
    private String origin;

    public WpReader(String origin) {
        if (StringUtils.isEmpty(origin) || !existsOrigin(origin)) {
            throw new IllegalArgumentException("Origin is not a valid file");
        } else {
            this.origin = origin;
        }
    }

    private boolean existsOrigin(String origin) {
        File originFile = new File(origin);
        return originFile.exists();
    }

    public void readPosts(Wp2JBake wp2JBake) {
        XMLEventReader eventReader = getEventReader();
        try {
            readXML(wp2JBake, eventReader);
        } catch (XMLStreamException e) {
            throw new IllegalStateException("Error reading XML " + origin + ": " + e.getMessage());
        }
    }

    private void readXML(Wp2JBake wp2JBake, XMLEventReader eventReader) throws XMLStreamException {
        while (eventReader.hasNext()) {
            readElement(wp2JBake, eventReader);
        }
    }

    private void readElement(Wp2JBake wp2JBake, XMLEventReader eventReader) throws XMLStreamException {
        XMLEvent event = eventReader.nextEvent();
        if (isPostStart(event)) {
            Post post = readPost(eventReader);
            wp2JBake.postRead(post);
        }
    }

    private Post readPost(XMLEventReader eventReader) throws XMLStreamException {
        Post exportedPost = new Post();
        boolean postRead = false;
        while (!postRead && eventReader.hasNext()) {
            XMLEvent event = eventReader.nextEvent();
            if (event.isStartElement()) {
                exportedPost = loadAttribute(event, eventReader, exportedPost);
            } else if (isPostEnd(event)) {
                postRead = true;
            }
        }
        return exportedPost;
    }

    private boolean isPostEnd(XMLEvent event) {
        return event.isEndElement() && ITEM.equals(event.asEndElement().getName().getPrefix() + event.asEndElement().getName().getLocalPart());
    }

    private Post loadAttribute(XMLEvent event, XMLEventReader eventReader, Post post) {
        String name = getEventFullName(event);
        try {
            post = loadAttribute(event, eventReader, post, name);
        } catch (XMLStreamException e) {
            throw new IllegalStateException("Error parsing " + name + ": " + e.getMessage());
        }
        return post;
    }

    private Post loadAttribute(XMLEvent event, XMLEventReader eventReader, Post post, String name) throws XMLStreamException {
        switch (name) {
            case TITLE:
                post = loadTitle(eventReader, post);
                break;
            case PUB_DATE:
                post = loadPublishingDate(eventReader, post);
                break;
            case CATEGORY:
                if (isTag(event)) {
                    post = loadCategory(eventReader, post);
                }
                break;
            case CONTENT:
                post = loadContent(eventReader, post);
                break;
            default:
                break;
        }
        return post;
    }

    private Post loadContent(XMLEventReader eventReader, Post post) throws XMLStreamException {
        return post.withContent(eventReader.nextEvent().asCharacters().getData());
    }

    private Post loadCategory(XMLEventReader eventReader, Post post) throws XMLStreamException {
        return post.withTag(eventReader.nextEvent().asCharacters().getData());
    }

    private Post loadPublishingDate(XMLEventReader eventReader, Post post) throws XMLStreamException {
        return post.withPublishingDate(parsePubDate(eventReader));
    }

    private Post loadTitle(XMLEventReader eventReader, Post post) throws XMLStreamException {
        return post.withTitle(eventReader.nextEvent().asCharacters().getData());
    }

    private boolean isTag(XMLEvent event) {
        return POST_TAG.equals(event.asStartElement().getAttributeByName(new QName(DOMAIN)).getValue());
    }


    private Date parsePubDate(XMLEventReader eventReader) throws XMLStreamException {
        Date publishingDate = null;
        try {
            String pubDate = eventReader.nextEvent().asCharacters().getData();
            pubDate = extractDate(pubDate);
            SimpleDateFormat format = new SimpleDateFormat("dd MMM yyyy");
            publishingDate = format.parse(pubDate);
        } catch (ParseException e) {
            throw new IllegalStateException("Could not parse pubDate: " + e.getMessage());
        }
        return publishingDate;
    }

    private String extractDate(String pubDate) {
        //Date is supplied as this: Wed, 30 Nov -0001 00:00:00 +0000 (RFC822 presumably), we need to extract just the date
        pubDate = pubDate.substring(pubDate.indexOf(",")+2);
        int hourIndex = pubDate.indexOf(":")-3;
        pubDate = pubDate.substring(0, hourIndex);
        return pubDate;
    }

    private boolean isPostStart(XMLEvent event) {
        return event.isStartElement() && ITEM.equals(getEventFullName(event));
    }

    private String getEventFullName(XMLEvent event) {
        return event.asStartElement().getName().getPrefix() + event.asStartElement().getName().getLocalPart();
    }

    private XMLEventReader getEventReader() {
        XMLInputFactory inputFactory = XMLInputFactory.newInstance();
        InputStream in = null;
        XMLEventReader eventReader = null;
        try {
            in = new FileInputStream(origin);
            eventReader = inputFactory.createXMLEventReader(in);
        } catch (FileNotFoundException e) {
            throw new IllegalStateException("Could not find origin file: " + e.getMessage());
        } catch (XMLStreamException e) {
            throw new IllegalStateException("Could not read origin file: " + e.getMessage());
        }
        return eventReader;
    }
}
```

Pues para terminar con esta sección que se ha alargado más de lo que esperaba, me queda modificar los tests:

```prettyprint
@RunWith(MockitoJUnitRunner.class)
public class WpReaderTest {

    private WpReader sut;

    @Mock
    private Wp2JBake observer;

    @Test(expected = IllegalArgumentException.class)
    public void readerWithoutOrigin() {
        sut = new WpReader(null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void readerWithEmptyOrigin() {
        sut = new WpReader("");
    }

    @Test(expected = IllegalArgumentException.class)
    public void buildWithInvalidOrigin() {
        sut = new WpReader("foo");
    }

    @Test(expected = IllegalStateException.class)
    public void readEmptyXML() {
        sut = new WpReader("src/test/resources/empty.xml");
        sut.readPosts(observer);
    }

    @Test(expected = IllegalStateException.class)
    public void readInvalidXML() {
        sut = new WpReader("src/test/resources/invalid.xml");
        sut.readPosts(observer);
    }

    @Test
    public void readValidXML() {
        sut = new WpReader("src/test/resources/wp-source.xml");
        ArgumentCaptor<Post> postCapturer = ArgumentCaptor.forClass(Post.class);
        sut.readPosts(observer);
        verify(observer, times(7)).postRead(postCapturer.capture());
    }
}
```

Con esto ya ha quedado perfecto, si no tanto el software, si los tests. Cada clase tiene una responsabilidad bien definida y así se refleja en los tests. Eso sí, en esta última clase he tenido que meter Mockito para simular el _Wp2JBake_ que me hace falta para el callback. Lo bueno de esto es que con Mockito puedo verificar las llamadas a los métodos y por primera vez tengo todos los tests en verde.
Eso sí, los tests de _Wp2JBake_ se han quedado en realidad como pruebas de integración, así que no me preocupa que el test original siga en rojo porque realmente hasta que no este implementada la escritura no debería pasar a verde :).
