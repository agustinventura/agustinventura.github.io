title=Tutorial de Bloc de Notas para Android - Parte 2
date=2011-07-04
type=post
tags=Android,Programación,tutorial
status=published
~~~~~~
Para empezar a unir la base de datos con las vistas que hemos definido, lo primero es usar la clase ListActivity, que como dice la <a title="API de ListActivity" href="http://developer.android.com/reference/android/app/ListActivity.html">documentación</a>, es una actividad que presenta una lista de elementos provenientes de un array o un cursor y aporta una serie de gestores llamados cuando el usuario interactua con ellos:

```prettyprint linenums
 public class Notepadv1 extends ListActivity
```

Ahora hay que completar el onCreate(), cuando se inicia la aplicación, ¿qué tiene que ocurrir?&amp;

<ol>
	<li>Obtener datos de la base de datos.</li>
	<li>Establecer la vista oportuna</li>
	<li>Completar la vista dependiendo de los datos obtenidos.</li>
</ol>

El método onCreate además toma un Bundle como parámetro, “savedInstanceState”, que es el estado de la aplicación guardado mediante el método onSaveInstanceState, es decir, sirve para recuperar el estado de la aplicación en la última ejecución.

Para acceder a la base de datos hay que declarar un miembro privado de la clase del tipo NotesDbAdapter que se llamará mDbHelper.

El método queda tal que así:

```prettyprint linenums

public void onCreate(Bundle savedInstanceState) {
super.onCreate(savedInstanceState);
setContentView(R.layout.notepad_list);
mDbHelper = new NotesDbAdapter(this);
mDbHelper.open();
fillData();
}
```


De momento, fillData se deja así y se pasa a rellenar el onCreateOptionsMenu(). Este método es llamado para crear el menú de opciones de la aplicación. Se encarga en esencia de generar este menú.

```prettyprint linenums

public boolean onCreateOptionsMenu(Menu menu) {
boolean result = super.onCreateOptionsMenu(menu);
menu.add(0, INSERT_ID, 0, R.string.menu_insert);
return result;
}
```


Si se mira la <a title="Documentación de Menu#add" href="http://developer.android.com/reference/android/view/Menu.html#add(int, int, int, java.lang.CharSequence)">documentación del método add</a>, quedará claro que se esta añadiendo un menú con identificador grupal 0 (este identificador es para crear conjuntos de elementos visuales), identificador únido INSERT_ID (esta variable habrá que declararla), orden 0 y su texto será la cadena menu_insert, que hay que declararla también en strings.xml

La declaración de INSERT_ID es interesante:

```prettyprint linenums

public static final int INSERT_ID = Menu.FIRST

```


La clase Menu, tiene definidas unas cuantas constantes, como Menu.FIRST (1) o Menu.NONE(0), que conviene mirar.

El siguiente método, onOptionsItemSelected(MenuItem item), se encarga de ejecutar la accion asociada al elemento de menú que se ha seleccionado. En nuestro caso, solo un elemento de menú y se encargará de crear una nota nueva:

```prettyprint linenums

public boolean onOptionsItemSelected(MenuItem item) {
switch (item.getItemId()) {
case INSERT_ID:
createNote();
return true;
}
```




```prettyprint linenums

return super.onOptionsItemSelected(item);

```


El método createNote() de momento se limita a crear una nota vacía con un identificador generado automáticamente:

```prettyprint linenums

private void createNote() {
String noteName = "Note " + mNoteNumber++;
mDbHelper.createNote(noteName, "");
fillData();
}
```


Una vez creada la nota, vuelve a rellenar la lista de notas existentes.

En cuanto al fillData:

```prettyprint linenums

private void fillData() {
// Get all of the notes from the database and create the item list
Cursor c = mDbHelper.fetchAllNotes();
startManagingCursor(c);

String[] from = new String[] { NotesDbAdapter.KEY_TITLE };
int[] to = new int[] { R.id.text1 };

// Now create an array adapter and set it to display using our row
SimpleCursorAdapter notes =
new SimpleCursorAdapter(this, R.layout.notes_row, c, from, to);
setListAdapter(notes);
}

```


Se traen las notas de la base de datos y se pasan a un adaptador que se encarga de rellenar la vista a partir de un Cursor. A destacar:

<ul>
	<li>from: Una lista de cadena que contiene los campos que se accederan en cada uno de los elementos. En este caso, solo el titulo.</li>
	<li>to: Los campos de la vista que se rellenarán con los valores obtenidos en el from. Cuidao que tiene que casar el orden del from con el del to.</li>
	<li>startManagingCursor: simplemente anuncia al sistema Android que se tiene que encargar él de gestionar el cursor.</li>
	<li>El constructor del SimpleCursorAdapter: pues nada, se le pasa el contexto, la vista "plantilla", el origen de datos (cursor en este caso), lo que queremos leer y donde queremos escribirlo.</li>
	<li>Por último, setListAdapter informe a la actividad de que sus datos están en el adaptador del cursor. Vamos, patrón decorador por un tubo, muy parecido a la forma de gestionar archivos en Java.</li>
</ul>

Y con esto, listo, Run as &gt; Android Application y volando.

De momento la aplicación simplemente se limita a crear Note 1, Note 2, Note 3... Note n.

Se irá mejorando.