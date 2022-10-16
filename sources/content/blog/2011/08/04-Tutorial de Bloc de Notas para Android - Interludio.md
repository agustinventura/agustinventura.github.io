title=Tutorial de Bloc de Notas para Android - Interludio
date=2011-08-04
type=post
tags=Android,Programación,tutorial
status=published
~~~~~~
Bueno, pues como me quedé ayer con las ganas, voy a hacer hoy un poco de microbenchmarking.
En general, y después de hablar con <a title="SpanishCoders" href="http://spanishcoders.com/" target="_blank">spCoder</a>, me quedó claro que hay en general, cuatro formas de hacer ese onClick:

<ol>
	<li>Tal y como pone el tutorial, mediante una clase interna anónima.</li>
	<li>Seguimos depurando, hacemos que NoteEdit.java implemente O<a title="Documentación de onClickListener" href="http://developer.android.com/reference/android/view/View.OnClickListener.html" target="_blank">nClickListener</a></li>
	<li>Definir el onClick en el layout del botón y definir el método en el NoteEdit. A priori es la forma más elegante y mejor.</li>
</ol>

Por curiosidad, voy a aplicar cada una de las soluciones y voy a tomar dos medidas:

<ol>
	<li>Tiempo de ejecución del onCreate.</li>
	<li>Tiempo de ejecución del onClick.</li>
</ol>

El proceso de prueba será:

<ol>
	<li>Seleccionar una nota ya existente.</li>
	<li>Modificar el título.</li>
	<li>Modificar el cuerpo.</li>
	<li>Pulsar confirmar.</li>
</ol>

<strong>Primera forma</strong>, código:

```prettyprint linenums
protected void onCreate(Bundle savedInstanceState) {
		long onCreateStartTime = System.currentTimeMillis();
		//Se invoca el onCreate de Activity
		super.onCreate(savedInstanceState);
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
				long onClickStartTime = System.currentTimeMillis();
	            Bundle bundle = new Bundle();

	            bundle.putString(NotesDbAdapter.KEY_TITLE, mTitleText.getText().toString());
	            bundle.putString(NotesDbAdapter.KEY_BODY, mBodyText.getText().toString());
	            if (mRowId != null) {
	                bundle.putLong(NotesDbAdapter.KEY_ROWID, mRowId);
	            }

	            Intent mIntent = new Intent();
	            mIntent.putExtras(bundle);
	            setResult(RESULT_OK, mIntent);
	            long onClickFinishTime = System.currentTimeMillis();
	            Log.d("Tiempo de ejecución: ", Long.toString(onClickFinishTime - onClickStartTime));
	            finish();
	        }
		});
		long onCreateFinishTime = System.currentTimeMillis();
		Log.d("Tiempo de ejecución: ", Long.toString(onCreateFinishTime - onCreateStartTime));
	}
```

Tiempos:

<ol>
	<li>onCreate: 80 msg</li>
	<li>onClick: 10 msg.</li>
</ol>

<strong>Segunda forma</strong>, código:

```prettyprint linenums
@Override
	protected void onCreate(Bundle savedInstanceState) {
		long onCreateStartTime = System.currentTimeMillis();
		//Se invoca el onCreate de Activity
		super.onCreate(savedInstanceState);
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
		confirmButton.setOnClickListener(this);
		long onCreateFinishTime = System.currentTimeMillis();
		Log.d("Tiempo de ejecución: ", Long.toString(onCreateFinishTime - onCreateStartTime));
	}

	@Override
	public void onClick(View v) {
		long onClickStartTime = System.currentTimeMillis();
        Bundle bundle = new Bundle();

        bundle.putString(NotesDbAdapter.KEY_TITLE, mTitleText.getText().toString());
        bundle.putString(NotesDbAdapter.KEY_BODY, mBodyText.getText().toString());
        if (mRowId != null) {
            bundle.putLong(NotesDbAdapter.KEY_ROWID, mRowId);
        }

        Intent mIntent = new Intent();
        mIntent.putExtras(bundle);
        setResult(RESULT_OK, mIntent);
        long onClickFinishTime = System.currentTimeMillis();
        Log.d("Tiempo de ejecución: ", Long.toString(onClickFinishTime - onClickStartTime));
        finish();
	}
```

Tiempos:

<ol>
	<li>onCreate: 130 msg</li>
	<li>onClick: 8 msg.</li>
</ol>

<strong>Tercera forma</strong>, código:

```prettyprint linenums
protected void onCreate(Bundle savedInstanceState) {
		long onCreateStartTime = System.currentTimeMillis();
		//Se invoca el onCreate de Activity
		super.onCreate(savedInstanceState);
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
		long onCreateFinishTime = System.currentTimeMillis();
		Log.d("Tiempo de ejecución: ", Long.toString(onCreateFinishTime - onCreateStartTime));
	}

	public void confirmClickListener(View v) {
		long onClickStartTime = System.currentTimeMillis();
        Bundle bundle = new Bundle();

        bundle.putString(NotesDbAdapter.KEY_TITLE, mTitleText.getText().toString());
        bundle.putString(NotesDbAdapter.KEY_BODY, mBodyText.getText().toString());
        if (mRowId != null) {
            bundle.putLong(NotesDbAdapter.KEY_ROWID, mRowId);
        }

        Intent mIntent = new Intent();
        mIntent.putExtras(bundle);
        setResult(RESULT_OK, mIntent);
        long onClickFinishTime = System.currentTimeMillis();
        Log.d("Tiempo de ejecución: ", Long.toString(onClickFinishTime - onClickStartTime));
        finish();
	}
```

Y la definición del botón:

```prettyprint linenums

<Button android:id="@+id/confirm" 
	  android:text="@string/confirm"
		android:layout_width="wrap_content"
		android:layout_height="wrap_content"
		android:onClick="confirmClickListener" />

```

Veamos los tiempos:

<ol>
	<li>onCreate: 48 msg</li>
	<li>onClick: 3 msg.</li>
</ol>

Conclusiones.

<ul>
	<li>En primer lugar, hay que decir que estas pruebas son un poco cutres. Para tener algo más de fiabilidad habría que usar un framework de pruebas y ejecutar multiples veces (al menos 100) el caso de prueba. Habría que hallar entonces la media y la varianza... pero de mientras...</li>
	<li>En general, podemos decir que la tercera forma es la más natural, tan solo hay que enlazar el onClick del botón con la función que le dá soporte.</li>
	<li>De esta forma, además, se ahorra el acceder al botón programáticamente en el onCreate().</li>
	<li>Tanto la segunda como la tercera forma han arrojado valores bastante similares.</li>
	<li>Queda a bastante distancia la primera forma. No solo es la más ilegible, sino que además es la más lenta, particularmente en el onCreate. Hay que tener en cuenta que siempre hay que hacer estos métodos lo más fluido posible, ya que uno de ellos excesivamente largo puede causar una pausa perceptible para el usuario. Es decir, es preferible tener dos métodos con una duración "media" que uno solo muy largo y otro muy corto.</li>
	<li>Por último también hay que tener en cuenta otro punto. He evaluado lo que tardan en ejecutar los métodos. Pero no cómo de bien se acopla el framework de Android al uso de uno o de otro. Me explico, está claro que en la tercera forma, es el mismo framework el que se encarga de enlazar botón y función. Es decir, que el tiempo que hemos medido no es del todo real, ya que habría que sumarle algo de tiempo que tarda el framework en ejecutar esta operación. En el primer y segundo caso, podemos suponer que el framework interviene de una forma menos intrusiva, al estar manipulando a mano el botón.</li>
</ul>

Poco más... me desconcierta un poco que el mismo tutorial sugiera una forma de hacer las cosas subóptima en más de un sentido, pero bueno...

Addenda.

No todo iba a ser malo... de propina he visto el uso de la clase Log así por encima, y solo puedo decir que lo aplaudo. Me parece estupendo que traiga un sistema de logging claro y conciso ya integrado. Asimismo, el uso de los tags y del LogCat es un combo de una utilidad impresionante :D