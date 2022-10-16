title=Tutorial de Bloc de Notas para Android – Parte 4
date=2011-08-01
type=post
tags=Android,Programación,tutorial
status=published
~~~~~~
Recapitulando lo anterior (hace ya 13 días a lo tonto...), se había a añadir la funcionalidad CRUD al bloc de notas, ya tengo puestos los métodos en el código del activity y solo hará falta completar.

Primero. Borrado.

El borrado habitualmente se hace mediante el menú contextual (igual que la edición, ahora que lo pienso...), para ello hay que registrar en el menú contextual el ListView, todo se puede hacer mediante métodos de la clase Activity, añadiendo al onCreate lo siguiente:

```prettyprint linenums
registerForContextMenu(getListView());
```

Con esto ya podemos invocar al menú contextual desde el ListView, pero claro, estará vacío, así que hace falta rellenar el onCreateContextMenu, que es muy similar al onCreateOptionsMenu, solo que además puede interactuar con la vista que lo invoca y además acepta opciones:

```prettyprint linenums
public void onCreateContextMenu(Menu menu, View v,
        ContextMenu.ContextMenuInfo menuInfo) {
    super.onCreateContextMenu(menu, v, menuInfo);
    menu.add(0, DELETE_ID, 0, R.string.menu_delete);
}
```

Con esto se crea un menú contextual que contiene un único item, borrar. ¿Qué pasa cuando se pulsa un elemento del menú contextual? Pues que se ejecuta onContextItemSelected que contiene la lógica de reconocimiento del elemento y de borrado:

```prettyprint linenums
public boolean onContextItemSelected(MenuItem item) {
    switch(item.getItemId()) {
    case DELETE_ID:
        AdapterContextMenuInfo info = (AdapterContextMenuInfo) item.getMenuInfo();
        mDbHelper.deleteNote(info.id);
        fillData();
        return true;
    }
    return super.onContextItemSelected(item);
}
```

Aquí es especialmente importante la línea 5, si miro <a href="http://developer.android.com/reference/android/widget/AdapterView.AdapterContextMenuInfo.html" target="_blank">la documentación</a>, ese info.id lo que devuelve es el identificador de la fila en la que se ha llamado al menú contextual, y se pasa tal cual al delete. Evidentemente en este ejemplo, se asume que ese id es el identificador de la nota también en la base de datos, pero no tiene por qué ser así... cuidado.

Para crear una nota, se usará un Intent. En general Android funciona mediante paso de mensajes, por tanto, para crear una nota, habrá que enviar un mensaje (Intent), solicitando que se cree. Tendré esto en el createNote:

```prettyprint linenums
Intent i = new Intent(this, NoteEdit.class);
startActivityForResult(i, ACTIVITY_CREATE);
```

Para crear el Intent, pasamos el Activity como implementación de Context, para dotar de un contexto de ejecución, y la clase (en este caso NoteEdit.class) que queremos que lo reciba. Tal y como <a title="Documentación de Intent" href="http://developer.android.com/reference/android/content/Intent.html#Intent(android.content.Context, java.lang.Class&lt;?&gt;)" target="_blank">insinúa la documentación</a>, esta forma es un poco suboptima, ya que se hardcodea la clase y esto es susceptible de cambiar. La forma habitual de usar los Intent, según leo en la documentación, es declarando intent-filters en el manifest, pero de momento, así se queda.

Más cosas, el <a title="Documentación de startActivityForResult" href="http://developer.android.com/reference/android/app/Activity.html#startActivityForResult(android.content.Intent, int)" target="_blank">startActivityForResult</a>, inicia la actividad y deja la que lo invoca esperando el resultado de ella (lo apila como proceso, supongo), cuando la nueva actividad termine de ejecutar invocará al método onActivityResult() de la invocadora. La otra forma de invocar una actividad es con <a title="Documentación de startActivity" href="http://developer.android.com/reference/android/app/Activity.html#startActivity(android.content.Intent)" target="_blank">startActivity</a>, que lo lanza y punto. Otra diferencia importante entre estos dos métodos, es que startActivity puede ser invocado sin existir una Activity, puede servir para crear una actividad nueva sin otra ya existente... ahí queda eso...

Con este método tenemos completado el caso de creación de una nueva nota, ahora bien, ¿cómo se edita una nueva nota? Pues pulsando sobre ella en la lista. ¿Y qué pasa cuando se pulsa sobre ella? Pues que se ejecuta <a title="Documentación de onListItemClick" href="http://developer.android.com/reference/android/app/ListActivity.html#onListItemClick(android.widget.ListView, android.view.View, int, long)">onListItemClick</a>, que toma de parámetros, la lista en la que se hizo click, la vista dentro del ListView en la que se hizo click, la posición de la lista en la que se hizo click y por último, el identificador del elemento en el que se hizo click. El método se completaría así:

```prettyprint linenums
protected void onListItemClick(ListView l, View v, int position, long id) {
        super.onListItemClick(l, v, position, id);
        Cursor c = mNotesCursor;
        c.moveToPosition(position);
        Intent i = new Intent(this, NoteEdit.class);
        i.putExtra(NotesDbAdapter.KEY_ROWID, id);
        i.putExtra(NotesDbAdapter.KEY_TITLE, c.getString(
                c.getColumnIndexOrThrow(NotesDbAdapter.KEY_TITLE)));
        i.putExtra(NotesDbAdapter.KEY_BODY, c.getString(
                c.getColumnIndexOrThrow(NotesDbAdapter.KEY_BODY)));
        startActivityForResult(i, ACTIVITY_EDIT);

    }
```

Lo primero, si mNotesCursor, es un atributo de mi actividad, ¿por qué se asigna a una variable local? Pues parece ser que por una particularidad de Dalvik, esta técnica hace que se acceda mucho más rápido al cursor, por tanto te recomiendan aplicarla siempre que puedas... vaya plan.

A continuación se situa el cursor en el registro de base de datos que indica position (que es la posición de la nota en la lista y ha de coincidir con la posición en la base de datos... se me ocurre que esto puede dar problemas si en la base de datos se hacen borrados lógicos y no físicos) y se crea un Intent nuevo.

Este Intent tiene un bundle interno que sirve digamos de cajón de sastre, para pasar la información que se quiera, el uso es mediante el método putExtra, y ahí se añaden todos los campos que tiene la nota.

Por último, se lanza la Activity, pero esta vez indicándole que es una edición (ACTIVITY_EDIT). La gracia de indicar estos modos de acceso, es que se devuelven a la actividad que lo invoca en su método onActivityResult, así se puede saber de donde se viene, si de una creación o una edición.

El método <a title="Documentación de onActivityResult" href="http://developer.android.com/reference/android/app/Activity.html#onActivityResult(int, int, android.content.Intent)" target="_blank">onActivityResult</a> recibe tres parámetros: el requestCode (es decir, el código que nosotros le hemos pasado), el resultCode (por convenio, si es distinto de 0, es correcto, tenemos un par de <a title="ResultCodes predefinidos" href="http://developer.android.com/reference/android/app/Activity.html#RESULT_CANCELED" target="_blank">constantes predefinidas</a>) y un Intent de vuelta que trae posibles resultados de la Activity recién terminada.

En nuestro caso, el código quedará así:

```prettyprint linenums
protected void onActivityResult(int requestCode, int resultCode, Intent intent) {
    	super.onActivityResult(requestCode, resultCode, intent);
    	Bundle extras = intent.getExtras();

    	switch(requestCode) {
    	case ACTIVITY_CREATE:
    	    String title = extras.getString(NotesDbAdapter.KEY_TITLE);
    	    String body = extras.getString(NotesDbAdapter.KEY_BODY);
    	    mDbHelper.createNote(title, body);
    	    fillData();
    	    break;
    	case ACTIVITY_EDIT:
    	    Long mRowId = extras.getLong(NotesDbAdapter.KEY_ROWID);
    	    if (mRowId != null) {
    	        String editTitle = extras.getString(NotesDbAdapter.KEY_TITLE);
    	        String editBody = extras.getString(NotesDbAdapter.KEY_BODY);
    	        mDbHelper.updateNote(mRowId, editTitle, editBody);
    	    }
    	    fillData();
    	    break;
    	}
    }
```

Haciendo un recorrido, vemos que si es un ACTIVITY_CREATE, se accede al título y el cuerpo que vienen en el Intent con los resultados, y se crea la nota a través del mDbHelper.

Si es un ACTIVITY_EDIT, además habrá que acceder en el Intent al Id de la nota, y se procederá a actualizar. Eso es todo.

Se puede observar que la lógica de acceso a datos queda encapsulada en esta Activity, es decir, la clase NoteEdit no va a tener lógica de acceso a base de datos, ya que es innecesario, todas las operaciones las gestiona ListActivity.

Con esto ya esta implementada esta clase, ¿qué queda? Pues NoteEdit.java con su correspondiente layout, pero eso lo dejo para la Parte 5 :).