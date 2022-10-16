title=Un poco de dinamismo
date=2011-02-20
type=post
tags=Programación,Ruby on Rails
status=published
~~~~~~
Siguiendo con el tutorial, ya sé añadir páginas y enrutarlas, va siendo hora de añadir algo de contenido dinámico a las páginas. Voy a hacer que el título cambie según la página en la que este. Y esto es lo que voy a chequear con TDD, es decir, que al solicitar /pages/home el título vale Home y que al solicitar /pages/about, el título vale About.
En rspec, quedaría algo así:

```prettyprint linenums

describe "GET 'home'" do
it "should be successful" do
get 'home'
response.should be_success
end
it "should have the right title" do
get 'home'
response.should have_selector("title",
:content =&gt; "Home");
end
end

```

El segundo caso, obviamente hay que añadirlo a todas las definiciones. Por otra parte la línea clave es bastante obvia, el response debe contener una etiqueta HTML title que contenga "Home", que contenga, es decir que si pongo "This is my Home" seguiría tirando... bueno, no esta mal.
Ejecuto

```prettyprint linenums

case@aesir:~/RoR/proyectos/sample_app/spec$ rspec controllers/
...
Finished in 1.28 seconds
6 examples, 3 failures

```

Eso es, mis 3 primeras pruebas siguen funcionando y las tres nuevas fallan, estoy en Red. Hora de ir a Green.
En primero lugar el tutorial me recomienda que borre el application.erb.html que hay en app/views/layouts, después de echarle un vistazo intuyo que será porque usa algo del estilo tiles o facelets para hacer un patrón composite sobre las páginas.
Borrado.
Ahora en el home.erb.html tengo que escribir todo el HTML. Completo. Esta clarísimo que el application.erb.html es para hacer de plantilla.
En fín, que escribo una página guarri y le pongo esto en title: "Ruby on Rails Tutorial Sample App | Home".
Voy a pasar rspec a ver si ya estoy en Green. Efectivamente, dos fallos, las dos páginas que no son Home, hora de modificarlas.
Se modifican, añadiendo un contenido algo distinto para cada una y andando, ya tenemos las páginas listas. Pego un rails s y efectivamente en http://localhost:3000/pages/home tengo el home, y las demás están en contact y en about.
Problemas:

<ul>
	<li>Me he cargado toda la estructura de plantillas....</li>
	<li>Poner el título en HTML plano a pelete tiene de dinámico lo mismo que un triciclo de vehículo...</li>
</ul>

Lo primero que sugiere el tutorial es poner el título en el action de cada página mediante una variable de instancia. Las variables de instancia se definen especificando una @ delante del nombre (en este caso va a ser @title) y como característica fundamental tienen que toda variable de instancia creada en el action es expuesta automáticamente a la vista... El primer paso entonces es de Java old-school, el controlador pages_controller.rb queda así:

```prettyprint linenums
class PagesController &lt; ApplicationController
def home
@title = "Home"
end
def contact
@title = "Contact"
end

```


```prettyprint linenums
 def about
@title = "About"
end
end

```

Y el title en las páginas quedaría así:

```prettyprint linenums

Ruby on Rails Tutorial Sample App | &lt;%=@title%&gt;

```

¿Alguien dijo scriptlets? Pues a ésto se le llama Embedded Ruby ERb, de ahí la extensión de las páginas.
Y ahora por seguir el orden inverso, voy a crear la plantilla para aplicársela a todas las páginas...
Para ello hay que crear en views/layout un archivo llamado application.html..erb... oh, wait... :S al parecer el nombre es obligatorio, y el contenido es este:

```prettyprint linenums

&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
&lt;title&gt;Ruby on Rails Tutorial Sample App | &lt;%= @title %&gt;&lt;/title&gt;
&lt;%= csrf_meta_tag %&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;%= yield %&gt;
&lt;/body&gt;
&lt;/html&gt;

```

El csrf_meta_tag es código que se inserta para evitar <a href="http://en.wikipedia.org/wiki/Cross-site_request_forgery" target="_blank">CSRF</a>, y el yield es el que lleva el cuerpo de la página, todo se ejecuta a la hora de traducir el erb a html.
Y ahora le quito la basurilla a las demás páginas. rspec controllers/ y todo sigue en Green.
Con esto se da por terminado el capítulo, ahora hay que añadir a git, y hacer un merge:

```prettyprint linenums

case@aesir:~/RoR/proyectos/sample_app$ git add .
case@aesir:~/RoR/proyectos/sample_app$ git commit -m "Se acabó la parte de páginas dinámicas y testing"[static-pages 3baeab7] Se acabó la parte de páginas dinámicas y testing
8 files changed, 82 insertions(+), 15 deletions(-)
create mode 100644 app/controllers/pages_controller.rb
create mode 100644 app/helpers/pages_helper.rb
create mode 100644 app/views/pages/about.html.erb
create mode 100644 spec/controllers/pages_controller_spec.rb
case@aesir:~/RoR/proyectos/sample_app$ git checkout master
Switched to branch 'master'
case@aesir:~/RoR/proyectos/sample_app$ git merge static-pages
Updating dd987a3..3baeab7
Fast-forward
app/controllers/pages_controller.rb       |   13 +++++++++
app/helpers/pages_helper.rb               |    2 +
app/views/layouts/application.html.erb    |   18 +++++--------
app/views/pages/about.html.erb            |    7 +++++
app/views/pages/contact.html.erb          |    5 +++
app/views/pages/home.html.erb             |    6 ++++
config/routes.rb                          |    5 +++
spec/controllers/pages_controller_spec.rb |   41 +++++++++++++++++++++++++++++
8 files changed, 86 insertions(+), 11 deletions(-)
create mode 100644 app/controllers/pages_controller.rb
create mode 100644 app/helpers/pages_helper.rb
create mode 100644 app/views/pages/about.html.erb
create mode 100644 app/views/pages/contact.html.erb
create mode 100644 app/views/pages/home.html.erb
create mode 100644 spec/controllers/pages_controller_spec.rb
case@aesir:~/RoR/proyectos/sample_app$ rspec spec/
......
Finished in 0.51904 seconds
6 examples, 0 failures
case@aesir:~/RoR/proyectos/sample_app$ git push
Counting objects: 38, done.
Compressing objects: 100% (26/26), done.
Writing objects: 100% (28/28), 2.79 KiB, done.
Total 28 (delta 7), reused 0 (delta 0)
To git@github.com:agustinventura/sample_app.git
dd987a3..3baeab7  master -&gt; master

```

Y bueno, ¿qué he hecho aquí? Pues básicamente, bichear con las vistas. He aprendido a utilizar el mecanismo de template de rails (aunque habría que ahondar, ver como hacer componentes, etc...) y a pasar variables a las páginas.
Ahora voy a hacer los ejercicios propuestos. En general son bastante sencillos.
El primero es repetir los pasos que ya hice al final del <a title="Comenzando el Testeo" href="http://aguasnegras.es/wp/?p=72" target="_blank">post anterior</a>, básicamente, modificar el pages_controller.rb, modificar el routes.rb y crear el Help.html.erb. Para ello, ya se sabe, primero los tests, después Red y después Green, así que toca modificar el pages_controller_spec.rb
Listo, bastante fácil.
El siguiente es modificar el fichero de pruebas para que concatene dos cadenas a la hora de chequear la validez del título. Es quizás más duro porque es Ruby a palo seco y mucho no entiendo, pero vamos, entiendo que la solución es algo como:

```prettyprint linenums

before(:each) do
    @base_title = "Ruby on Rails Tutorial Sample App "
  end

```

Ejecuto y todo guay. No termino de entender muy bien eso del before(:each) do... pufff molaría más entender Ruby, pero digo yo que ya progresaré, por hoy ya esta bien.