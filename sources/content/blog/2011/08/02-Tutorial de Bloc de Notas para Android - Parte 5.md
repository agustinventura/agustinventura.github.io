title=Tutorial de Bloc de Notas para Android - Parte 5
date=2011-08-02
type=post
tags=Android,Programación,tutorial
status=published
~~~~~~
Con respecto a la pantalla de edición/inserción de notas nuevas, nos dan ya el layout, llamado note_edit.xml. En él tenemos una distribución de elementos de la siguiente manera: LinearLayout, TextView, EditText y Button (todo ello dentro a su vez de un LinearLayout). El primer LinearLayout tiene orientation=vertical, para disponer los elementos en vertical (nada que ver con la posición de la pantalla) y el segundo tiene orientation=horizontal. Dentro de él hay un TextView y un EditText con layout_weight = 1. Este parámetro indica la importancia (y por tanto el espacio en pantalla) que ocupará un elemento determinado. Por defecto, vale 0.

La gestión del espacio ocupado por un elemento, es un poco extraña. En caso de que el parámetro no este establecido (o valga 0), el elemento ocupará el espacio mínimo e imprescindible para mostrarse. En el ejemplo de arriba, el TextView no tiene parámetro, luego ocupará el mínimo espacio posible, mientras que el EditText lo tiene a 1, lo que hace que ocupe todo el espacio restante en el LinearLayout padre. Si pongo los dos a 1, pasan a ocupar la mitad del LinearLayout cada uno. Si lo dejo en el TextView a 1 y lo cambio en el EditText a 2, el TextView ocupará un tercio del espacio y los restantes dos tercios, el EditText... y así sucesivamente.

Para los otros tres elementos, solo tiene layout_weight = 1 el EditText (de nuevo), lo cual significa que el TextView ocupará el mínimo espacio posible, el Button igual y el resto del espacio lo ocupará el EditText.

Para aportar la lógica de negocio de esta vista, hay que crear la clase NoteEdit, así que click con el botón derecho encima del paquete com.android.demo.notepad2 &gt; New &gt; Class... En Name pongo NoteEdit y en Superclass com.android.app.Activity (hereda de Activity). Finish.

Ahora hace falta crear en onCreate (valga la redundancia), click con el botón derecho encima del editor de la clase Source &gt; Implement/Override methods y selecciono el onCreate(Bundle).

Aquí esta el método correctamente creado y con comentarios:

```prettyprint linenums
protected void onCreate(Bundle savedInstanceState) {
        //Se invoca el onCreate de Activity
	super.onCreate(savedInstanceState);
	//Si es una edición, hay que guardar el identificador de la nota
	Long mRowId = null;
	//Se asigna el layout
	setContentView(R.layout.note_edit);
	//Se le dá el título
	setTitle(R.string.edit_note);
	//Se cargan los componentes para establecer los textos (si es una edición)
	mTitleText = (EditText) findViewById(R.id.title);
	mBodyText = (EditText) findViewById(R.id.body);
	//Si es una edición, los datos de la nota vendrán dentro de los extras del Intent
	Bundle extras = getIntent().getExtras();
	if (extras != null) {
		//Caso de que haya estos extras, se le dan los valores adecuados a los EditText
		String title = extras.getString(NotesDbAdapter.KEY_TITLE);
		String body = extras.getString(NotesDbAdapter.KEY_BODY);
		//Y se guarda el identificador en BD de la nota
		mRowId = extras.getLong(NotesDbAdapter.KEY_ROWID);
		//Comprobación de nulo, ya que se permite crear notas sin cuerpo o sin título
		if (title != null) {
		    mTitleText.setText(title);
		}
		if (body != null) {
		    mBodyText.setText(body);
		}
	}
	//Se trae el botón de confirmar para añadirle un listener del click
	Button confirmButton = (Button) findViewById(R.id.confirm);
	//ATENCIÓN, el Listener se crea como una Inner Class Anónima!!
	confirmButton.setOnClickListener(new View.OnClickListener() {
	        public void onClick(View view) {
		}
	});
}
```

Bueno, a ver, cosas que me llaman la atención...

<ol>
	<li>¿Por qué mTitleText y mBodyText son variables de instancia y mRowId es de método? ¿No sé supone que se optimiza accediendo mediante variables locales? Voy a tener que pensar sobre esto...</li>
	<li>Hablando de mRowId... es Long, no long (¿quizás para evitar autoboxing?)</li>
	<li>Por último... una clase anónima interna?? WTF?? Esto se lo voy a tener que preguntar a mi <a title="SpanishCoders" href="http://www.spanishcoders.com" target="_blank">primo</a>, y aún así no descarto hacer algún microbenchmark a ver si mediante una clase interna normal va igual y por lo menos gano en legibilidad...</li>
</ol>

En fín, mañana lo acabo y si me dá tiempo,