title=JustPlay, explorador de archivos
date=2012-05-17
type=post
tags=Android,JustPlay,Programación,Proyectos
status=published
~~~~~~
Uno de mis requisitos en JustPlay (de hecho, el fundamental), es poder reproducir a partir de archivos sueltos o directorios.

Por tanto, necesitaré un explorador de archivos, aunque sea muy básico, que permita ver los archivos en la memoria del dispositivo y añadirlos a una lista de reproducción. Gráficamente, la interacción entre las actividades sería <a title="Interacción Actividades JustPlay" href="https://docs.google.com/drawings/d/1GCzJBHeAYgXh5ZlZmsyjQJic8RM3ECh6oD-AYEWRTAo/edit" target="_blank">así</a>. En general la devolución del parámetro no tendrá mayor problema, ya que se puede hacer a través del intent de vuelta.

Para crear el explorador de archivos voy a seguir <a title="Simple File Explorer - Android-er" href="http://android-er.blogspot.com.es/2010/01/implement-simple-file-explorer-in.html" target="_blank">este tutorial</a>, por supuesto añadiendo cosas de mi cosecha según me vaya pareciendo.

<h6>Creación de CrankExplorer</h6>

En primer lugar creo la activity tal cual heredando de CrankActivity y le añado la implementación por defecto de todos los métodos del ciclo de vida.

Ahora la declaro en el AndroidManifest:


```prettyprint linenums

<activity android:name=".FileExplorer" android:label="@string/explorer_name"/>

```


Para arrancarla, creo un botón en MediaPlayer:


```prettyprint linenums

<Button
android:id="@+id/buttonOpenExplorer"
android:layout_width="wrap_content"
android:layout_height="wrap_content"
android:text="@string/open_explorer"
android:onClick="openCrankExplorer" />

```


Y el listener:


```prettyprint linenums

public void openCrankExplorer(View v) {
  Intent openCrankExplorer = new Intent(this, CrankExplorer.class);
  startActivityForResult(openCrankExplorer, REQUEST_CODE);
}

```


Con esto ya puedo llamar a FileExplorer desde MediaPlayer.

Ahora toca implementar FileExplorer, en general la implementación seguirá estas líneas:

<ol>
	<li>Se mostrarán todos los archivos y directorios que se puedan leer.</li>
	<li>Si se hace click en un directorio se abrirá.</li>
	<li>Si se hace click en un archivo, se abrirá un diálogo de confirmación para añadirlo a la lista de reproducción.</li>
	<li>Si se deja presionado un directorio se abrirá un menú contextual para añadir todo su contenido a la lista de reproducción.</li>
</ol>

Al lío, siguiendo lo que comentan, hago un layout para los archivos, le voy a llamar file_row.xml y a continuación creo el layout de FileExplorer, crankexplorer.xml. No tiene mucha historia ya que es una lista y punto.

En cuanto a la actividad, lo primero que hago es filtrar los archivos mediante un FilenameFilter, para que solo muestre aquellos directorios y archivos que sean legibles y si es un archivo, que además termine en mp3 u ogg.

Añado un onListItemClick y si es un directorio se invocará a getDir sobre él, mientras que si es un archivo, se mostrará un diálogo que permitirá dos acciones:

<ol>
	<li>Añadir el archivo a la lista de reproducción.</li>
	<li>Cancelar</li>
</ol>

Por último, para devolver la canción a MediaPlayer, creo un método finish().

Para ir acabando, falta el menú contextual que me permita seleccionar un directorio para añadir (junto con todos los archivos contenidos en él y sus subdirectorios).
Primero creo el <a title="Defining a Menu in XML - Android Developers" href="http://developer.android.com/guide/topics/ui/menus.html#xml" target="_blank">layout del menu</a> y lo llamo crankexplorer_context.xml a continuación en el onCreate, registro la lista para el menú contextual:

```prettyprint linenums

registerForContextMenu(getListView());

```


Después tengo que crear dos métodos del ciclo de vida, el primero, la creación del menú:


```prettyprint linenums

@Override
public void onCreateContextMenu(ContextMenu menu, View v,
  ContextMenuInfo menuInfo) {
  super.onCreateContextMenu(menu, v, menuInfo);
  menu.setHeaderTitle(R.string.directory_contextual_title);
  MenuInflater inflater = getMenuInflater();
  inflater.inflate(R.menu.crankexplorer_context, menu);
}

```


Y el segundo, la acción a ejecutar cuando se selecciona:


```prettyprint linenums

@Override
public boolean onContextItemSelected(MenuItem item) {
  switch (item.getItemId()) {
    case R.id.addDirectoryItem:
      AdapterContextMenuInfo info = (AdapterContextMenuInfo) item
      .getMenuInfo();
      this.selected = new File(this.path.get((int) info.id));
      if (this.selected.isDirectory()) {
        finish();
      }
      return true;
   default:
     return super.onContextItemSelected(item);
  }
}

```


Para acabar, implemento el método finish() para devolver bien la canción seleccionada, bien todas las canciones:


```prettyprint linenums

@Override
public void finish() {
  Intent data = new Intent();
  if (this.selected != null) {
    if (this.selected.isFile()) {
      data.putExtra("selectedFile", this.selected);
    } else if (this.selected.isDirectory()) {
      List<File> filesInDirectory = this.explodeDir(this.selected);
      data.putExtra("selectedFiles",
        (ArrayList<File>) filesInDirectory);
    }
  }
  setResult(RESULT_OK, data);
  super.finish();
}

```


Y en MediaPlayer creo un onActivityResult que procese la vuelta desde FileExplorer:


```prettyprint linenums

@Override
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
  if (data.hasExtra("selectedFile")) {
    this.playlist.add((File) data.getExtras().get("selectedFile"));
    this.renderPlaylist();
  } else if (data.hasExtra("selectedFiles")) {
    List<File> fileList = (List<File>) data.getExtras().get(
      "selectedFiles");
    this.playlist.addAll(fileList);
    this.renderPlaylist();
  }
}

```



<h6>TODO</h6>

Pues ya solo queda:

<ol>
	<li>Hacer el bind del service en MediaPlayer</li>
	<li>Reproducir con un MediaPlayer en el thread.</li>
</ol>


<h6>Código</h6>

Sigue en GitHub

<a href="https://github.com/agustinventura/JustPlay"><img class="size-full wp-image-255" title="JustPlay en GitHub" src="/images/2011/08/github_icon.png" alt="JustPlay en GitHub" width="115" height="115" /></a>
