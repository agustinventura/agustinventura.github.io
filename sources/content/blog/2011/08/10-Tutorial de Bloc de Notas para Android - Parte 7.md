title=Tutorial de Bloc de Notas para Android - Parte 7
date=2011-08-10
type=post
tags=Android,Programación,tutorial
status=published
~~~~~~
Actualmente, la aplicación de bloc de notas deja mucho que desear, no solo con respecto al aspecto gráfico o usabilidad de la misma, sino que además no esta integrada en el ciclo de vida.

Una Activity tiene un <a title="Ciclo de Vida de Activity" href="http://developer.android.com/reference/android/app/Activity.html#ActivityLifecycle" target="_blank">ciclo de vida</a> determinado y el programador se tiene que ajustar a él. Por ejemplo, si se arranca la aplicación y se le da a crear o editar una nota y a continuación al botón de atrás, la Activity se cierra inesperadamente. Para evitar este tipo de cosas, el tutorial propone dos soluciones:

<ol>
	<li>Integrar la Activity NoteEdit en el ciclo de vida de una Activity de Android.</li>
	<li>Mover toda la lógica de acceso a base de datos necesaria a NoteEdit (si se pulsa el botón atrás, se disparará el onPause() que se encargará de salvar la nota a la base de datos)</li>
</ol>

En general esto implica algunas funciones nuevas (básicamente, los callbacks del ciclo de vida) y movimiento de código de un lado a otro. A ello.

Con el nuevo enfoque (acceso a la base de datos en NoteEdit), se hace inútil pasar todos los datos de la nota a NoteEdit, basta con pasar el mRowId. Si mRowId es null, será una creación de nueva nota, en otro caso será una edición y se cargarán los datos de la base de datos. Borro en NoteEdit.java las líneas 46 y 47 y de la 50 a la 55.

Creo también una instancia de clase de NotesDbAdapter y se inicializa en el onCreate, justo después del super.onCreate().

Ahora viene la obtención del mRowId, se sigue este orden:

<ol>
	<li>Si la Activity estaba en ejecución anteriormente, habrá una instancia salvada, que se habrá pasado. En este caso se obtiene de esa instancia.</li>
	<li>Si no, es posible que el Intent traiga el mRowId, habrá que comprobarlo.</li>
	<li>Por último, puede ser que no venga de ninguna de las maneras y que, por tanto, sea un alta.</li>
</ol>

Sustituyo el código de las líneas 46 a 50 por este:

```prettyprint linenums
//Si la aplicación no tiene estado salvado, mRowId será nulo. En caso de tenerlo, se recupera.
mRowId = (savedInstanceState == null) ? null :
    (Long) savedInstanceState.getSerializable(NotesDbAdapter.KEY_ROWID);
     //Si mRowId vale nulo, es que no había instancia salvada del estado de la aplicación
     if (mRowId == null) {
        //Se comprueba si mRowId viene en el Intent
        Bundle extras = getIntent().getExtras();
         //Aún así puede ser que no venga y entonces valdrá nulo, siendo un alta de nueva nota
         mRowId = extras != null ? extras.getLong(NotesDbAdapter.KEY_ROWID)
                     : null;
     }
```

Nota de interés, en el primer caso se usa getSerializable porque <a title="Documentación de getSerializable" href="http://developer.android.com/reference/android/os/Bundle.html#getSerializable(java.lang.String)" target="_blank">devuelve un Object</a> (una instancia de Serializable, más concretamente), mientras que getLong <a title="Documentación de getLong" href="http://developer.android.com/reference/android/os/Bundle.html#getLong(java.lang.String)" target="_blank">devuelve un long</a> (el tipo primitivo), así que no serviría para hacer la comparación con null (getLong nunca podrá devolver null). Hmm... si embargo mRowId es de tipo Long, luego cuando en la última línea se hace ese getLong, en caso de venir (una edición), hay que hacer un autoboxing. No sé en la Dalvik VM, pero en Java "vanilla" el uso indiscriminado de autoboxing es una pérdida de rendimiento bastante gorda, habrá que estar pendiente de ello...

Una vez accedido y cargado el mRowId (bien del Intent, bien del savedInstance), es hora de cargar los campos (o no, claro), para ello se invoca a un nuevo método llamado populateFields() (implementación más adelante).

En lo que respecta al onClickListener, queda tal que así:

```prettyprint linenums
confirmButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                setResult(RESULT_OK);
                finish();
            }
});
```

A por ese populateFields... el tema es muy sencillo, si mRowId es distinto de nulo, habrá que cargar la nota desde la base de datos y establecer los valores de los textos:

```prettyprint linenums
private void populateFields() {
        if (mRowId != null) {
            Cursor note = mDbHelper.fetchNote(mRowId);
            startManagingCursor(note);
            mTitleText.setText(note.getString(
                        note.getColumnIndexOrThrow(NotesDbAdapter.KEY_TITLE)));
            mBodyText.setText(note.getString(
                    note.getColumnIndexOrThrow(NotesDbAdapter.KEY_BODY)));
        }
}
```

Aquí pasa algo interesante, para adaptar la aplicación totalmente al ciclo de vida, tendríamos que implementar un método onPause() que entre otras cosas, liberase el cursor, y en el onResume() volver a abrirlo, etc... en general, gestionar el recurso del Cursor. Bueno, pues como ese caso es bastante, común, para eso se utiliza el <a title="Documentanción de startManagingCursor" href="http://developer.android.com/reference/android/app/Activity.html#startManagingCursor(android.database.Cursor)" target="_blank">startManagingCursor</a>, se encarga de acoplar el ciclo de vida del cursor... y por cierto, esta deprecado... otra guasita del tutorial, ya me dá la risa floja.

Sigo, ahora hay que implementar el onSaveInstanceState, que es llamado por el framework Android antes de matar la aplicación. Va a hacer dos tareas, guardar la nota en la base de datos (creando una nueva o actualizando) y guardar el mRowId en el savedInstanceState para que lo pueda usar el onCreate.

```prettyprint linenums
@Override
protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        saveState();
        outState.putSerializable(NotesDbAdapter.KEY_ROWID, mRowId);
}
```

Siguiente, el onPause(), en este caso, solo hay que guardar en base de datos (ya que no se va a matar la Activity):

```prettyprint linenums
@Override
protected void onPause() {
        super.onPause();
        saveState();
    }
```

Y el onResume(), más de lo mismo, no se ha destruido la aplicación, asi que basta con leer los valores de la base de datos (es decir, invocar el populateFields()). Pregunta, ¿es necesario? Si la Activity no se ha llegado a matar, ¿hace falta volver a cargar los valores? Me lo dejo como ejercicio.

```prettyprint linenums
@Override
    protected void onResume() {
        super.onResume();
        populateFields();
    }
```

Y el saveState():

```prettyprint linenums
private void saveState() {
        String title = mTitleText.getText().toString();
        String body = mBodyText.getText().toString();

        if (mRowId == null) {
            long id = mDbHelper.createNote(title, body);
            if (id &gt; 0) {
                mRowId = id;
            }
        } else {
            mDbHelper.updateNote(mRowId, title, body);
        }
    }
```

Lo único a reseñar es que si mRowId es null y la inserción es correcta (id &gt; 0), se carga el mRowId, es decir, cuando se recargue la Activity o se vuelva a ejecutar el onCreate, será una edición, no un alta.

Ahora toca limpiar el Notepadv3, quitando llamadas varias a la base de datos. En primer lugar, el onActivityResult, ya simplemente hay que refrescar la vista, por si ha habido posibles cambios (hmm... esto también es muy optimizable):

```prettyprint linenums
@Override
protected void onActivityResult(int requestCode, int resultCode, Intent intent) {
    super.onActivityResult(requestCode, resultCode, intent);
    fillData();
}
```

Igual para el onListClickItem, ya no hace falta acceder a base de datos, y el mRowId viene dado por el id que recibe el método:

```prettyprint linenums
@Override
    protected void onListItemClick(ListView l, View v, int position, long id) {
        super.onListItemClick(l, v, position, id);
        Intent i = new Intent(this, NoteEdit.class);
        i.putExtra(NotesDbAdapter.KEY_ROWID, id);
        startActivityForResult(i, ACTIVITY_EDIT);
    }
```

Por último, el Cursor ya no hace falta que sea una variable de instancia de la Activity, sino que puede ser una variable local del fillData.

Bueno, pues con esto termina el tutorial de Google que empecé hace ya más de un mes... no ha estado mal, quizás me ha faltado constancia. Me queda el detalle de examinar más de cerca lo que he apuntado arriba del ciclo de vida... y una vez hecho eso, habrá que buscar una idea de aplicación a desarrollar (ya tengo una primera...). Aparte, también le echaré un vistazo al <a title="Curso de Android de Maestros del Web" href="http://www.maestrosdelweb.com/editorial/curso-android/" target="_blank">libro de Maestros del Web</a>, que tiene una pinta bastante buena.

creo que cuando lo haya leído, haré un post de conclusiones sobre Android así en general, aunque mi primera impresión es muy positiva. Si alguien ha seguido la serie hasta aquí, gracias por leerme :).