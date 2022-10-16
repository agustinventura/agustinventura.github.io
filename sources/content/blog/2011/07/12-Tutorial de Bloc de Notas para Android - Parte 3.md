title=Tutorial de Bloc de Notas para Android - Parte 3
date=2011-07-12
type=post
tags=Android,Programación,tutorial
status=published
~~~~~~
Sigo con el tutorial, que más vale tarde que nunca... Entonces, repasando un poco lo hecho, tengo una tabla en la bd de la aplicación (un sqlite) que contiene las notas.

Asimismo, tengo un activity que se encarga de presentar una lista con las notas creadas que de momento no tienen nada, tan solo un título "Note x" donde x es un autosecuencial, además un secuencial de Java, por lo cual en cada ejecución de la aplicación se repiten ya que se resetea el contador a 1. Esto no me gusta y da la casualidad de que tengo un autoincremental en la base de datos, así que voy a tratar de presentarlo en vez de ese.

Analizando lo que tengo, en base de datos no hay que tocar nada, ya tengo todos los datos. Asímismo el NotesDbAdapter.java se trae absolutamente todos los campos cuando accede, con lo cual el id secuencial lo tengo en el cursor que llega a la activity, ¿qué queda entonces? Tan solo presentarlo.

Primero modifico la vista de presentación de cada nota, es decir, el notes_row.xml, tan solo tiene un TextView y voy a necesitar dos: uno para el id y otro para el título:

¿Dónde se rellena esta vista? En el fillData(), precisamente tenemos un array de String que son los datos que leemos del cursor (from) y un array de int que son en qué elementos los insertamos en la vista:

```prettyprint linenums
 String[] from = new String[] { NotesDbAdapter.KEY_ROWID, NotesDbAdapter.KEY_TITLE };
 int[] to = new int[] { R.id.text1, R.id.text2 };
```

Y con esto ya tengo una primera aproximación:

<a href="/images/2011/07/Pantallazo-5554android2.2.png"><img class="aligncenter size-medium wp-image-141" title="Pantallazo modificación propia del tutorial Notepad" src="/images/2011/07/Pantallazo-5554android2.2-300x278.png" alt="" width="300" height="278" /></a>Con lo cual ya se diferencia entre notas aunque tengan el mismo título.

Bueno, <a title="Tutorial Notepad - Parte 2" href="http://developer.android.com/resources/tutorials/notepad/notepad-ex2.html">sigo con el tutorial</a>, creo un nuevo proyecto Android, from existing sources, etc... Listo. En esta parte del tutorial, se va a implementar la funcionalidad de edición de las notas (a través de un activity nuevo) y el borrado de las mismas a través del menú contextual.

Para empezar, el strings.xml se ha actualizado, incorporando los textos necesarios para la funcionalidad nueva "confirm", "edit note", etc... Sin embargo el NotesDbAdapter.java sigue siendo el mismo, normal, la funcionalidad ya estaba contemplada desde el principio.

En el Notepadv2.java parece que esta el grueso de los cambios. De entrada me encuentro con unos int que representan las activity que hay:

```prettyprint linenums
private static final int ACTIVITY_CREATE=0;
private static final int ACTIVITY_EDIT=1;
```

También tengo dos enteros para las entradas del menú:

```prettyprint linenums
private static final int INSERT_ID = Menu.FIRST;
private static final int DELETE_ID = Menu.FIRST + 1;
```

Por último en la sección de declaraciones, el Cursor. El cursor antes era una variable del método fillData y ahora pasa a ser una variable de instancia de esta actividad:

```prettyprint linenums
private Cursor mNotesCursor;
```

El método onCreate no tiene más cambios, y el fillData tan solo los necesarios debidos al cambio de visibilidad del cursor. Los demás métodos, onCreateOptionsMenu no tiene más cambios, pero onMenuItemSelected si que tiene un pequeño, pero importante, ahora invoca al método createNote.

Llegamos a la sección de métodos nuevos. Un breve comentario sobre cada uno de ellos:

<ul>
	<li>onCreateContextMenu: Blanco y en botella... el método encargado de generar el menú contextual (con el borrar).</li>
	<li>onContextItemSelected: Más de lo mismo, se encargará de gestionar la selección del elemento del menú contextual.</li>
	<li>createNote: supongo que se encargará de llamar a la actividad de inserción/edición de notas.</li>
	<li>onListItemClick: de nuevo supongo que se encargará de gestionar el click en cada uno de los elementos de la lista (notas??)</li>
	<li>onActivityResult: esto tiene toda la pinta de ser un finalizador, para liberar recursos al salir de la actividad, vaya.</li>
</ul>

Poco más, mañana seguiré con la parte de implementación pura y dura.
