title=JUnit 4 y DataSources
date=2010-11-20
type=post
tags=JUnit,Java
status=published
~~~~~~
Cuando desarrollo aplicaciones web (y tengo tiempo) me gusta seguir una variante propia de <a title="Test Driven Development" href="http://en.wikipedia.org/wiki/Test-driven_development" target="_blank">TDD</a>. Básicamente trato de ser exhaustivo con las pruebas y en este sentido JUnit es lo suyo, diseño el DAO y le hago pruebas unitarias, diseño la capa de servicios y le hago pruebas unitarias, es más, si tengo tiempo hago pruebas unitarias sobre las mismas entidades.

A las malas malas, JUnit me sirve para probar la funcionalidad de la aplicación antes de hacer la interfaz de usuario.

Últimamente trabajo siempre con Spring o JPA, por lo que los accesos a base de datos son a través de un DataSource, bien gestionado por Spring, bien gestionado por JPA.

El caso es que para las pruebas en general, en vez de andar creando las conexiones a base de datos aparte y pasarlas a los DAO, mola crear un DataSource y publicarlo por JNDI, así nunca hay que volver a tocar nada.

Tras investigar algo me encuentro que esto no es algo que este muy trillado, así que nada, manos a la obra. Lo que hago es definir un método @BeforeClass para que me cree el DataSource y me lo publique en el contexto JNDI antes de que se ejecute ninguna prueba.

El código es bastante sencillo y autoexplicativo, para que funcione, es necesario el naming-commons.jar, naming-factory.jar y el naming-resources.jar, se encuentra normalmente en cualquier tomcat en $CATALINA_HOME/common/lib.

```prettyprint linenums
public class DataBaseTest {

	@BeforeClass
	public static void setDataSource() {
		try {
			// Create initial context
			System.setProperty(Context.INITIAL_CONTEXT_FACTORY,
					"org.apache.naming.java.javaURLContextFactory");
			System.setProperty(Context.URL_PKG_PREFIXES, "org.apache.naming");
			InitialContext ic = new InitialContext();
			ic.createSubcontext("jdbc");

			// Construct DataSource
			OracleConnectionPoolDataSource ds = new OracleConnectionPoolDataSource();
			ds.setURL("jdbc:oracle:thin:@server:port:SID");
			ds.setUser("user");
			ds.setPassword("password");

			ic.bind("jdbc/ds", ds);
		} catch (NamingException ex) {
			Logger.getLogger(DataBaseTest.class.getName()).log(
					Level.SEVERE, null, ex);
		} catch (SQLException e) {
			Logger.getLogger(DataBaseTest.class.getName()).log(
					Level.SEVERE, null, e);
		}
	}

	public DataBaseTest() {
		super();
	}

}
```

Y eso es todo, para usar exactamente esta implementación también es conveniente tener log4j y el ojdbc14.jar.

Referencias:

<ol>
	<li><a href="http://blogs.sun.com/randystuph/entry/injecting_jndi_datasources_for_junit">http://blogs.sun.com/randystuph/entry/injecting_jndi_datasources_for_junit</a></li>
	<li><a href="http://www.coderanch.com/howto/java/CodeBarnLibrariesAndFrameworks">http://www.coderanch.com/how-to/java/CodeBarnLibrariesAndFrameworks</a></li>
</ol>
