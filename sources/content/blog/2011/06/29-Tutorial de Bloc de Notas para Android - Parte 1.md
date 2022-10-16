title=Tutorial de Bloc de Notas para Android - Parte 1
date=2011-06-29
type=post
tags=Android,Programación,tutorial
status=published
~~~~~~
La página principal de este tutorial esta <a title="Tutorial Bloc de Notas Android" href="http://developer.android.com/resources/tutorials/notepad/index.html">aquí</a>.

En general te recomiendan tener una idea de como funciona Android (para lo cual es bueno repasar los <a title="Fundamentos de Aplicaciones Android" href="http://developer.android.com/guide/topics/fundamentals.html">Fundamentos de Aplicaciones</a>) y <a title="Fuentes del Bloc de Notas" href="http://developer.android.com/resources/tutorials/notepad/codelab/NotepadCodeLab.zip">descargar</a> los proyectos preconfigurados en zip.

Descomprimo el zip como recomiendan en $HOME/Android/NotepadCodeLab.

El tutorial esta divido en tres ejercicios (que vienen con sus correspondientes soluciones) y un extra para aprender a depurar el ciclo de vida de Android.

En el primero voy a crear una lista de notas y voy a añadir notas pero no voy a poder editarlas. Muestra los principios de ListActivity y como crear y manipular opciones de menú. Además usa una base de datos SQLite para guardar las notas.

Importo los fuentes que me dan a un nuevo proyecto en eclipse (File &gt; New... &gt; Android Project) y selecciono "Create project from existing sources" y en la carpeta de la ruta introduzco $HOME/Android/NotepadCodeLab/Notepadv1. Selecciono también el Build target, en mi caso solo tengo instalado Android 2.2, así que nada, ese me vale. Finish.

En el projecto viene dado un Notepadv1.java que es la actividad principal y viene canina, solo código por defecto, y un NotesDbAdapter.java que se encarga de conectar con la base de datos.

NotesDbAdapter combina la funcionalidad de acceso a la base de datos con la de la manipulación de los datos en sí. Para empezar tiene varias constantes que definen el nombre de la base de datos (data), el de la tabla (notes) y los de las columnas (_id para la pk, el underscore es por convención, body, el texto y title, el título).

Además tiene una instancia de la base de datos SQLite como tal y otra del Context, es decir, una referencia al contexto Android de la aplicación.

Por último, tiene también una instancia de un DataBaseHelper que es una clase estática privada definida dento de NotesDbAdapter y que se encarga de abrir y cerrar la conexión así como de crear la base de datos si no existe (y subirla de version, sea lo que sea eso) .

La interfaz de NotesDbAdapter es un <a title="Create, Read, Update and Delete" href="http://es.wikipedia.org/wiki/CRUD">CRUD</a> típico: constructor (que asigna el contexto), open (que usa el DataBaseHelper y crea la base de datos si no existe), close y createNote, deleteNote, fetchAllNotes, fetchNote y updateNote.

Particularidades:

<ul>
	<li>fetchAllNotes: Devuelve un Cursor, no un List ni nada así. Importante, Cursor no es synchronized, así que no es thread safe por defecto.</li>
	<li>El método query del SQLiteDataBase tiene esta signatura: <a title="método query" href="http://developer.android.com/reference/android/database/sqlite/SQLiteDatabase.html#query(java.lang.String, java.lang.String[], java.lang.String, java.lang.String[], java.lang.String, java.lang.String, java.lang.String)">query</a>(String table, String[] columns, String selection, String[] selectionArgs, String groupBy, String having, String orderBy), es decir, no toma SQL directamente, sino que más bien se especifica la consulta a través de los parámetros.</li>
	<li>fetchNote: Utiliza una sobrecarga de query para chequear unicidad.</li>
	<li>updateNote: Utiliza un método update muy parecido a query, pero los nuevos datos se pasan dentro de un objeto ContentValues, que tiene toda la pinta de ser un Map con alguna cosa más.</li>
</ul>

A continuación paso a la capa de presentación. En res/layout esta el notepad_list.xml, que es la vista principal de la aplicación. Cosas importantes:

<ul>
	<li>Tiene que ser un xml válido con su cabecera.</li>
	<li>El primer elemento suele ser un Layout (LinearLayout en este caso).</li>
	<li>El primer elemento define el <a title="Espacio de nombres" href="http://es.wikipedia.org/wiki/Namespace">namespace</a> de Android para poder seguir usando sus elementos (componentes) visuales: xmlns:android="http://schemas.android.com/apk/res/android</li>
</ul>

Copio y pego de la página del tutorial el siguiente trozo de código:


```prettyprint linenums

&lt;ListView android:id="@android:id/list"
android:layout_width="wrap_content"
android:layout_height="wrap_content"/&gt;
&lt;TextView android:id="@android:id/empty"
android:layout_width="wrap_content"
android:layout_height="wrap_content"
android:text="@string/no_notes"/&gt;

```

Al tener dos hijos habrá que elegir cual de los dos presentar. El ListView para cuando haya una lista (de notas) y el TextView para cuando no haya nada. Es por ello que el TextView define en su etiqueta text "@string/no_notes", lo cual quiere decir que en mi recurso de strings (res/values/strings.xml) tendré una llamada no_notes que especificará el texto a mostrar cuando no hay notas.

La decisión de cual mostrar se realiza a través de los atributos android:id. Cuando el ListAdapter encargado de renderizar la lista tenga datos, se utilizará el marcado como "id/list". En caso contrario se usará "id/empty".

Esta forma de acceder a los recursos es declarativa, para hacerlo de manera programática se puede utilizar la clase android.R (para acceder a los "@android:...") o R (propia del proyecto, se genera automáticamente y se usa para acceder por ejemplo a los "@string/...").

Ya esta la vista de listado, ahora se define una vista para el detalle de las notas, se llamará "notes_row.xml". Click con el botón derecho sobre layout &gt; new... &gt; Android XML File. Nombre: "notes_row.xml" y se indica que es un Layout y en root element TextView. Solo hace falta añadir una linea, el id:

```prettyprint linenums

android:id="@+id/text1"

```

El "+" significa que si cuando se accede no existe el recurso llamado text1, se cree al vuelo.

¿Qué queda? Pues pegarlo todo usando el código propio de la actividad. Pero eso mañana.