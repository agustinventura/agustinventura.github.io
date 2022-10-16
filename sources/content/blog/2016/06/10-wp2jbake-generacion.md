title=Wordpress to JBake - Generación de Archivos
date=2016-06-10
type=post
tags=Java, JBake, Wordpress
status=published
~~~~~~
Bueno, pues ya queda la parte final, lanzarlo. Creo un método _main_ en _Wp2JBake_, el primer argumento será el archivo de origen y el segundo el directorio de destino.
Como de toda la gestión de errores se encarga el programa en sí, lo único que tengo que hacer es capturar la posible _IllegalArgumentException_ y listo:

```prettyprint
public static void main (String... args) {
    if (args.length!=2) {
        System.out.println("Wp2JBake needs two arguments to work: First the input file and second the destination folder");
    } else {
        try {
            Wp2JBake exporter = new Wp2JBake(args[0], args[1]);
            Set<File> exportResult = exporter.generateJBakeMarkdown();
            if (!exportResult.isEmpty()) {
                System.out.println("Export successful in " + args[1]);
            }
        } catch (IllegalArgumentException | IllegalStateException e) {
            System.out.println("Error exporting: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

Ahora queda lo de siempre, generar el jar en Maven con todas sus dependencias. Añado al pom.xml la configuración del assembly-plugin para que genere el Manifest ya que sin él, el jar no sería ejecutable y además le digo que empaquete las dependencias junto con el jar:

```prettyprint
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-assembly-plugin</artifactId>
            <version>2.6</version>
            <configuration>
                <descriptorRefs>
                    <descriptorRef>jar-with-dependencies</descriptorRef>
                </descriptorRefs>
                <archive>
                    <manifest>
                        <mainClass>com.digitalsingular.wp2jbake.Wp2JBake</mainClass>
                    </manifest>
                </archive>
            </configuration>
            <executions>
                <execution>
                    <id>assemble-all</id>
                    <phase>package</phase>
                    <goals>
                        <goal>single</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

Y por fín se acabó, con ésto ya genero la exportación.
