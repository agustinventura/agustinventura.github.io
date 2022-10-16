title=Comenzando el Testeo
date=2011-02-16
type=post
tags=Programación,Ruby on Rails
status=published
~~~~~~
Estoy rememorando mi trabajo de hace 8 horas... variables que no sabes si se usan en otro sitio, temor a limpiar cosas, en fín... una pesadilla. Por eso, ESTE es el momento de empezar el testing en la aplicación RoR, he hecho un controlador (vacío, sí) y es hora de asegurarnos que ahora y siempre haga lo que tiene que hacer (nada).
El tutorial, aparte de recomendar TDD y contarte que RSpec es un domain specific language para hacer pruebas en Ruby, dice de instalar autotest, una herramienta que ejecuta continuamente las pruebas sobre los archivos cambiados. Vaya, que si toco un controlador me ejecuta las pruebas dándome feedback instantáneo, una primera aproximación a la integración contínua.
Amos a ello.

```prettyprint linenums

$ gem install autotest -v 4.4.6
$ gem install autotest-rails-pure -v 4.1.2

```

Para lo demás recomiendan seguir <a href="http://automate-everything.com/2009/08/gnome-and-autospec-notifications/"> este tutorial </a>, que para mi sorpresa es de un compi de aquí de Sevilla y escrito en perfecto cristiano.
Se resume en:

```prettyprint linenums

$ gem install ZenTest
$ gem install redgreen
$ sudo apt-get install libnotify-bin

```

No he ejecutado con sudo, espero que no pase nada, si no... habrá que arreglarlo que es lo divertido de esto. Además en el script que recomienda Manuel Morales, me he permitido quitar todas las referencias a imágenes, que paso de ellas.
Sigo con el tutorial en sí. Se hace una breve introducción a TDD y el ciclo "Red, Green, Refactor".

<ul>
	<li>Red: Se escribe un test (o tests) que falle</li>
	<li>Green: Se escribe un test (o tests) que funcione</li>
	<li>Refactor: Se refactoriza el código, es la hora de eliminar duplicación, aplicar patrones, lo que se me ocurra para que quede bien.</li>
</ul>

Para empezar a picar los tests en rojo, se recomienda eliminar primero los tests de views y helpers, para mantenerlos todos juntos. A mí a priori no me parece buena idea, prefiero mantenerlo todo en limpito y separado, pero el tutorial no lo he hecho yo, así que nada:

```prettyprint linenums

case@aesir:~/RoR/proyectos/sample_app$ rm -rf spec/views/
case@aesir:~/RoR/proyectos/sample_app$ rm -rf spec/helpers

```

Ahora abro el test que ha quedado, en /spec/controller y... madre mía, esto no lo entiende ni dios... y dice el colega que se parece al inglés y que es fácil de usar... joder, si el lo dice, pos vale. Analizando este código según lo explicado:

```prettyprint linenums

describe "GET 'home'" do
  it "should be successful" do
    get 'home'
    response.should be_success
  end
end

```

La primera línea NO hace nada, solo dice qué hace el test.
La segunda línea dice que el test debería ser correcto, vaya que tampoco hace nada.
La tercera línea ya si hace una petición GET a /pages/home.
Y la cuarta simplemente comprueba que el resultado tiene un código 200.
Moraleja... 4 líneas para 2 funcionales... un poco boilerplate.
Ejecuto los tests:

```prettyprint linenums

case@aesir:~/RoR/proyectos/sample_app$ rspec /spec
/home/case/.rvm/gems/ruby-1.9.2-p0@rails3/gems/rspec-core-2.3.1/lib/rspec/core/configuration.rb:388:in `load': no such file to load -- /spec (LoadError)

```

Ufff... pos vamos bien... el tutorial es de "mucha" ayuda, recomienda desinstalar rspec y volverlo a instalar.
El fallo sin embargo parece que viene dado por el no such file to load... hmm, lo mismo si pruebo pasándole como parámetro el test en sí...

```prettyprint linenums

case@aesir:~/RoR/proyectos/sample_app/spec/controllers$ rspec pages_controller_spec.rb
..
Finished in 0.61139 seconds
2 examples, 0 failures

```

Voilá... po vaya plan, que raro que falle cuando se le pasa el directorio... esto va a haber que mirarlo porque si no, promete ser un coñazo... Parece ser que si le paso como parámetro /spec/controllers también va... pos bueno, puede valer.
Ahora se me dice que arranque autotest... y falla también, en concreto falla redgreen, dice que no existe un archivo (que efectivamente no existe)... fuf, vaya plan, ¿no?
El problema parece que es de que <a title="redgreen y test-unit" href="http://kresimirbojcic.com/2009/09/redgreen-plugin-not-working-with-ruby-1-9-1/" target="_blank">redgreen necesita test-unit</a>, pero para eso hay que actualizar gem, en total:

```prettyprint linenums

case@aesir:~/RoR/proyectos/sample_app$ gem update --system
case@aesir:~/RoR/proyectos/sample_app$ gem install test-unit -v 1.2.3

```

Se ejecuta... y vuelve a fallar, joder, menuda CHUSTA, paso del autotest.
La siguiente sección habla de Spork, un servidor de pruebas que el mismo tutorial dice que es experimental y que si se quiere, que se salte esa sección... maaadre mía, así será, yo paso.
Sigo, con el lío, hacer un test Red para la página "about", copio y pego en el mismo pages_controller_spec.rb el de home, pero cambiando "home" por "about" y va que chuta. Lo ejecuto:

```prettyprint linenums

case@aesir:~/RoR/proyectos/sample_app/spec/controllers$ rspec pages_controller_spec.rb

```

Y todo correcto, 3 testes, 1 fallo, no hay route para la acción about en el controlador pages.
Una pequeña parte que me he saltado es que esto comprueba si la acción exista, pero claro... que exista la acción no significa que exista la página como tal, jeje.
Para eso hay que usar un render_views justo debajo de la declaración del PagesController:

```prettyprint linenums

describe PagesController do
render_views

```

Una vez hecho esto, a convertir ese Red en un Green. Pasos a dar:
Añadir accion al controlador: Es decir, al final de pages_controller.rb añadir esto:

```prettyprint linenums

def about
end

```

Añadir el about al route: En routes.rb añadir:

```prettyprint linenums

get "pages/about"

```

Por último, crear la vista, el about.html.erb

```prettyprint linenums

&lt;h1&gt;Pages#about&lt;/h1&gt;
&lt;p&gt;Find me in app/views/pages/about.html.erb&lt;/p&gt;

```

Y vamos a ver si da green... Sí, listo.
Reflexión, en verdad este capítulo para lo que sirve más bien es para comprobar si tenemos asentados los conocimientos relativos al enrutamiento de peticiones, aparte de configurar el tema de pruebas.
En cuanto a las pruebas... pues mal, no sé si será el rspec en particular o qué, pero entre los problemas y las investigaciones que he hecho, no parece que por ejemplo redgreen sea lo más estable del mundo... y lo del Spork... para echarle de comer aparte.
En fín, tampoco pasa nada por estar ejecutando las pruebas a manubrio en otra consola, no hay que ser tan exigente.