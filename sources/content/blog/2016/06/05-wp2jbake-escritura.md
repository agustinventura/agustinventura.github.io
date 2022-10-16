title=Wordpress to JBake - Escritura
date=2016-06-05
type=post
tags=Java, JBake, Wordpress
status=published
~~~~~~
Retomando la migración del blog, una vez resuelta la parte de leer los posts, hay que hacer la escritura. El enfoque pasa por lo siguiente:

1. Tener una plantilla de post que se leerá en el constructor. Esta plantilla tendrá placeholders para saber donde van los campos.
2. Tratar según que campos, por ejemplo los tags habrá que representarlos como un string y separados por comas, las etiquetas `<pre`> que indican código habrá que convertiras a prettyprint.
3. Escribir el archivo, a ser posible usando async I/O, así no se bloquea.

Empezando por lo primero, la plantilla irá en _src/main/resources_ y será la siguiente

```prettyprint
title=$title$
date=$date$
type=post
tags=$tags$
status=published
~~~~~~
$content$
```

Los placeholders he decidido que empiecen y terminen por $ para mayor seguridad. El test sería el siguiente:

```prettyprint
@Test
public void writerWithValidDestination() {
    sut = new MdWriter("src/test/destination");
}
```

Y la implementación, aprovechando para lo cual he simplificado la clase usando las clases nuevas de Java 8 _Files_ y _Path_.

```prettyprint
public class MdWriter {

    private String template;

    private String destinationFolder;

    public MdWriter(String destinationFolder) {
        if (StringUtils.isEmpty(destinationFolder) || !isWritable(destinationFolder)) {
            throw new IllegalArgumentException("Destination is not a valid folder");
        } else {
            readTemplate();
            this.destinationFolder = destinationFolder;
        }
    }

    private void readTemplate() {
        try {
            template = new String(Files.readAllBytes(Paths.get("src/main/resources/template.md")));
        } catch (IOException e) {
            throw new IllegalStateException("Could not read post template template.md: " + e.getMessage());
        }
    }

    private boolean isWritable(String destination) {
        Path destinationPath = Paths.get(destination);
        if (Files.exists(destinationPath)) {
            return Files.isWritable(destinationPath);
        } else {
            return Files.isWritable(destinationPath.getParent());
        }
    }

    public File write(Post post) {
        return null;
    }
}
```

Ahora tengo que crear la estructura de archivos en la que va el post, es decir, tengo que verificar si existe existe la ruta del tipo detinationFolder/yyyy/mm y ahí crear un archivo de nombre dd-tituloDelPost y por último, escribirlo. La verdad que todo esto es MUY fácil con _Paths_ y _Files_, así que ya no hace falta usar los _commons-io_, al menos para ésto.
Los tests:

```prettyprint
public class MdWriterTest {

    public static final String POST_DATE_FORMAT = "yyyy-MM-dd";
    public static final String TEST_POST_CONTENT = "content";
    public static final String TEST_POST_TITLE = "title";
    public static final Date TEST_POST_DATE = new Date();
    public static final String POST = "post";
    public static final String EMPTY_TAGS = "";
    public static final String PUBLISHED = "published";
    public static final String METADATA_SEPARATOR = "~~~~~~";
    public static final String FIRST_TAG = "tag1";
    public static final String SECOND_TAG = "tag2";
    private MdWriter sut;

    private String destination = "src/test/destination";

    @Before
    public void setUp() throws IOException {
        cleanDestination();
    }

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

    @Test
    public void writerWithValidDestination() {
        sut = new MdWriter(destination);
    }

    @Test(expected =  IllegalArgumentException.class)
    public void writeEmptyPost() {
        sut = new MdWriter(destination);
        sut.write(new Post());
        new File(destination).delete();
    }

    @Test
    public void writePostWithoutTags() throws IOException {
        sut = new MdWriter(destination);
        Post post = new Post().withContent(TEST_POST_CONTENT).withTitle(TEST_POST_TITLE).withPublishingDate(TEST_POST_DATE);
        File postFile = sut.write(post);
        assertThat(postFile, notNullValue());
        List<String> lines = Files.readAllLines(Paths.get(postFile.getPath()));
        assertThat(getValue(lines.get(0)), is(post.getTitle()));
        assertThat(getValue(lines.get(1)), is(getPostDate(post)));
        assertThat(getValue(lines.get(2)), is(POST));
        assertThat(getValue(lines.get(3)), is(EMPTY_TAGS));
        assertThat(getValue(lines.get(4)), is(PUBLISHED));
        assertThat(getValue(lines.get(5)), is(METADATA_SEPARATOR));
        assertThat(lines.get(6), is(post.getContent()));
        cleanDestination();
    }

    @Test
    public void writePostWithTags() throws IOException {
        sut = new MdWriter(destination);
        Post post = new Post().withContent(TEST_POST_CONTENT).withTitle(TEST_POST_TITLE).withPublishingDate(TEST_POST_DATE).withTag(FIRST_TAG).withTag(SECOND_TAG);
        File postFile = sut.write(post);
        assertThat(postFile, notNullValue());
        List<String> lines = Files.readAllLines(Paths.get(postFile.getPath()));
        assertThat(getValue(lines.get(0)), is(post.getTitle()));
        assertThat(getValue(lines.get(1)), is(getPostDate(post)));
        assertThat(getValue(lines.get(2)), is(POST));
        assertThat(getValue(lines.get(3)), is(FIRST_TAG+","+SECOND_TAG));
        assertThat(getValue(lines.get(4)), is(PUBLISHED));
        assertThat(getValue(lines.get(5)), is(METADATA_SEPARATOR));
        assertThat(lines.get(6), is(post.getContent()));
        cleanDestination();
    }

    private String getPostDate(Post post) {
        DateFormat formatter = new SimpleDateFormat(POST_DATE_FORMAT);
        return formatter.format(post.getPublishingDate());
    }

    private String getValue(String line) {
        int valueStart = line.indexOf("=")+1;
        return line.substring(valueStart);
    }

    private void cleanDestination() throws IOException {
        if (Files.exists(Paths.get(destination))) {
            Files.walkFileTree(Paths.get(destination), new SimpleFileVisitor<Path>() {
                @Override
                public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
                    Files.delete(file);
                    return FileVisitResult.CONTINUE;
                }

                @Override
                public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
                    Files.delete(dir);
                    return FileVisitResult.CONTINUE;
                }

            });
        }
    }
}
```

Y la implementación:

```prettyprint
public class MdWriter {

    public static final String TEMPLATE = "src/main/resources/template.md";
    public static final String TITLE = "$title$";
    public static final String DATE = "$date$";
    public static final String TAGS = "$tags$";
    public static final String CONTENT = "$content$";
    public static final String POST_DATE_FORMAT = "yyyy-MM-dd";
    public static final String POST_EXTENSION = ".md";
    public static final String DATE_TITLE_SEPARATOR = "-";

    private String template;

    private String destinationFolder;

    public MdWriter(String destinationFolder) {
        if (StringUtils.isEmpty(destinationFolder) || !isWritable(destinationFolder)) {
            throw new IllegalArgumentException("Destination is not a valid folder");
        } else {
            readTemplate();
            this.destinationFolder = destinationFolder;
        }
    }

    private void readTemplate() {
        try {
            template = new String(Files.readAllBytes(Paths.get(TEMPLATE)));
        } catch (IOException e) {
            throw new IllegalStateException("Could not read post template template.md: " + e.getMessage());
        }
    }

    private boolean isWritable(String destination) {
        Path destinationPath = Paths.get(destination);
        if (Files.exists(destinationPath)) {
            return Files.isWritable(destinationPath);
        } else {
            return Files.isWritable(destinationPath.getParent());
        }
    }

    public File write(Post post) {
        validatePost(post);
        Path destinationPath = getDestinationPath(post);
        createDestinationPath(destinationPath);
        String postMarkdown = getPostMarkdown(post);
        try {
            Files.write(destinationPath, postMarkdown.getBytes()
                    , StandardOpenOption.CREATE_NEW);
        } catch (IOException e) {
            throw new IllegalStateException("Error writing file " + destinationPath.toString() + ": " + e.getLocalizedMessage());
        }
        return destinationPath.toFile();
    }

    private void validatePost(Post post) {
        if (StringUtils.isEmpty(post.getTitle()) || post.getPublishingDate() == null || StringUtils.isEmpty(post.getContent())) {
            throw new IllegalArgumentException();
        }
    }

    private String getPostMarkdown(Post post) {
        String postMarkdown = template.replace(TITLE, post.getTitle());
        postMarkdown = postMarkdown.replace(DATE, getPostDate(post.getPublishingDate()));
        postMarkdown = postMarkdown.replace(TAGS, post.getTags().stream().map(Object::toString).collect(Collectors.joining(",")));
        postMarkdown = postMarkdown.replace(CONTENT, post.getContent());
        return postMarkdown;
    }

    private String getPostDate(Date publishingDate) {
        DateFormat formatter = new SimpleDateFormat(POST_DATE_FORMAT);
        return formatter.format(publishingDate);
    }

    private void createDestinationPath(Path destinationPath) {
        try {
            if (!Files.exists(destinationPath.getParent())) {
                Files.createDirectories(destinationPath.getParent());
            }
        } catch (IOException e) {
            throw new IllegalStateException("Error creating destination path " + destinationPath + ": " + e.getMessage());
        }
    }

    private Path getDestinationPath(Post post) {
        Calendar publishedCalendar = getPublishedCalendar(post);
        Path destinationPath = Paths.get(destinationFolder, Integer.toString(publishedCalendar.get(Calendar.YEAR)),
                Integer.toString(publishedCalendar.get(Calendar.MONTH)), Integer.toString(publishedCalendar.get(Calendar.DAY_OF_MONTH)) +
                        DATE_TITLE_SEPARATOR + post.getTitle() + POST_EXTENSION);
        return destinationPath;
    }

    private Calendar getPublishedCalendar(Post post) {
        Calendar publishedCalendar = Calendar.getInstance();
        publishedCalendar.setTime(post.getPublishingDate());
        return publishedCalendar;
    }
}
```
Bueno, pues ya esta, ya solo faltarían las pruebas de _Wp2JBake_ como tales, es decir, la integración. Todavía no he tocado nada de etiquetas especiales, ni he considerado el hecho de que se exportan posts que se consideran borradores (aquellos que tienen de fecha de publicación el 1AC), pero eso me debe dar la cara en las pruebas de integración.
