title=Tutorial de Bloc de Notas para Android - Parte 6
date=2011-08-03
type=post
tags=Android,Programación,tutorial
status=published
~~~~~~
Bueno, pues ayer había rellenado el cuerpo del onCreate del EditNote.java y quedaba una cosa que no me gusta un pelo, que es rellenar ese onClick de la clase anónima interna. Para no salirme mucho (de momento) del objetivo, que es el tutorial, me limitaré a seguir el tutorial y después haré los experimentos oportunos.

Recordando igualmente de antesdeayer, toda la interacción con la base de datos se hace en la Activity Notepadv2, con lo cual el onClick lo único que ha de hacer es montar el mensaje necesario y devolverlo a la actividad que le ha invocado. Facilísimo, vaya:

```prettyprint linenums
public void onClick(View view) {
            Bundle bundle = new Bundle();

            bundle.putString(NotesDbAdapter.KEY_TITLE, mTitleText.getText().toString());
            bundle.putString(NotesDbAdapter.KEY_BODY, mBodyText.getText().toString());
            if (mRowId != null) {
                bundle.putLong(NotesDbAdapter.KEY_ROWID, mRowId);
            }

            Intent mIntent = new Intent();
            mIntent.putExtras(bundle);
            setResult(RESULT_OK, mIntent);
            finish();
        }
```

Bien, se construye un bundle en el que se introducen los datos de los EditText y el id de la nota (si es una edición), a continuación se construye el Intent que se devuelve y se establece el bundle anterior como sus extras. Con <a title="Documentación de setResult" href="http://developer.android.com/reference/android/app/Activity.html#setResult(int, android.content.Intent)" target="_blank">setResult</a> se establece el código de resultado y el Intent a devolver. Por último, ese <a title="Documentación de finish()" href="http://developer.android.com/reference/android/app/Activity.html#finish()" target="_blank">finish</a> se encarta de devolver el ActivityResult (que contendrá el código de resultado y el Intent) a la Activity que llamó a esta. Finito.

Vale, aquí no esta muy limpia la API,, creo yo, setResult toma un int y un Intent, y finish dice que pasa un <a title="Documentación de ActivityResult" href="http://developer.android.com/reference/android/app/Instrumentation.ActivityResult.html" target="_blank">ActivityResult</a> a la Activity que había invocado a la que termina... pero sin embargo esta "invocadora", en su onActivityResult, recibe requestCode (int), resultCode (int) y el Intent. Que no digo que no, pero limpio, limpio lo que se dice muy limpio, pues tampoco es...

Por último, hay que declarar la activity en el AndroidManifest.xml, así que lo abro, paso de wizard y le doy al xml a pelo... busco la línea &lt;/activity&gt; de la de Notepadv2 y añado esto:

```prettyprint linenums

<activity android:name=".NoteEdit" />

```

Hora de darle a Run... ;)

Y efectivamente, con esto ya esta listo... me quedo con la espina clavada de la clase interna anónima, así que mañana haré un poco de microbenchmarking y probaré distintas cosas que me ha recomendado <a title="SpanishCoders" href="http://www.spanishcoders.com" target="_blank">spCoder</a>.