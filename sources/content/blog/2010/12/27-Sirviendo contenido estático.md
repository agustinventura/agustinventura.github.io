title=Sirviendo contenido estático
date=2010-12-27
type=post
tags=Programación,Ruby on Rails
status=published
~~~~~~
Después de unas buenas (y merecidas) vacaciones, sigo con el tutorial de RoR, esta vez en el capítulo tres voy a empezar a desarrollar una aplicación completa y entendiéndola en profundidad, ya no solo voy a usar scaffolding y punto.
Empiezo por la sección de "Contenido Estático", me parece cojonuda la idea, siempre es buena idea maximizar a tope el contenido estático, ya que no solo salva tiempo de CPU, sino que además permite que funcionen las técnicas de cacheo de apache, etc...
Creo el proyecto nuevo tal y como se especifica.

```prettyprint linenums

$ rails new sample_app -T

```

El -T es nuevo, por lo visto es para NO crear un directorio de tests asociado al framework de pruebas unitarias Test::Unit, ya que se va a utilizar otro llamado RSpec.
Ahora edito el Gemfile para incluir las dependencias, incluyendo sqlite y rspec:

```prettyprint linenums

$ cat Gemfile 
source 'http://rubygems.org'

gem 'rails', '3.0.1'

gem 'sqlite3-ruby', '1.2.5', :require => 'sqlite3'

group :development do
	gem 'rspec-rails', '2.3.0'
end

group :test do
	gem 'rspec', '2.3.0'
	gem 'webrat', '0.7.1'
end

```

En un principio y sin saber muy bien como va esto, diría que son como tasks de Ant o fases del ciclo de vida de Maven, es decir, los gems solo se instalan para determinados "perfiles" de compilación, sqlite sería siempre pero rspec solo cuando hagamos "development" o "test", a ver si lo explican más adelante.
Hago un bundle install para instalar RSpec y como esta tardando, voy a mirar en la wikipedia algo de este framework.
Vaya artículo más "escueto" dice que es un framework para Behavior Driven Development (primera vez en mi vida que escucho esto) y que incluye su propio mock framework, cosa que está muy bien pensada, en general pruebas unitarias sin un mock framework se quedan un poco cortas. Y con esto ya me he respondido una de mis primeras preguntas sobre frameworks de pruebas unitarias, si que existen, al menos dos.
Anda, ha fallado el bundle install:

```prettyprint linenums

Installing nokogiri (1.4.4) with native extensions /home/case/.rvm/rubies/ruby-1.9.2-p0/lib/ruby/1.9.1/rubygems/installer.rb:483:in `rescue in block in build_extensions': ERROR: Failed to build gem native extension. (Gem::Installer::ExtensionBuildError)

/home/case/.rvm/rubies/ruby-1.9.2-p0/bin/ruby extconf.rb 
checking for libxml/parser.h... yes
checking for libxslt/xslt.h... no
-----
libxslt is missing.  please visit http://nokogiri.org/tutorials/installing_nokogiri.html for help with installing dependencies.

```

Venga, pues voy a pegarle un apt-get de las dependencias para asegurarme que lo tengo todo.

```prettyprint linenums

sudo apt-get install libxslt-dev libxml2-dev

```

Y efectivamente, libxml2 ya la tenía pero no libxslt. Hago el bundle install de nuevo.
Para instalar los archivos necesarios de RSpec:

```prettyprint linenums

$ rails generate rspec:install

```

Ahora cambio el README, hago el primer commit en git, creo el repositorio en GitHub y lo despliego en Heroku.
Seguimos con contenidos estáticos, por defecto en el directorio /public de la aplicación se encuentran los contenidos estáticos y accesibles directamente, es decir, todo lo que hay en esta carpeta es servido al cliente sin mayor problema.
Ahí esta index.html que es la página que se sirve por defecto al primer request y lo dicho, es estática.
Como ya he visto además, Rails puede mezclar código Ruby y HTML al más puro estilo jsp-old-skool... hmm... no sé si eso es una ventaja o un inconveniente y me surge otra duda ¿hay algún tipo de composite pattern?¿Un Tiles o un Facelets? In tutorial we trust...
Muy bien, ahora lo que voy a hacer es crear un controlador para que sirva el contenido estático de la aplicación, es decir, voy a empezar a integrar el contenido estático con el MVC. El controlador va a servir la página About y la de Contact.
Creo un branch en git para ir haciendo el trabajo:

```prettyprint linenums

p$ git checkout -b static-pages

```

Ahora, para crear el controlador que las va a usar se usará generate. Generate es un script de Rails que genera controladores, toma como parámetros el nombre del controlador y las acciones que ejecuta, es decir:

```prettyprint linenums

$ rails generate controller Pages home contact

```

La salida del generate dá una lista de las acciones efectuadas

```prettyprint linenums

create  app/controllers/pages_controller.rb
       route  get "pages/contact"
       route  get "pages/home"
      invoke  erb
      create    app/views/pages
      create    app/views/pages/home.html.erb
      create    app/views/pages/contact.html.erb
      invoke  rspec
      create    spec/controllers/pages_controller_spec.rb
      create    spec/views/pages
      create    spec/views/pages/home.html.erb_spec.rb
      create    spec/views/pages/contact.html.erb_spec.rb
      invoke  helper
      create    app/helpers/pages_helper.rb
      invoke    rspec
      create      spec/helpers/pages_helper_spec.rb

```

Primero se crea el pages_controller.rb, después se crean los routes de ambas acciones, se invoca erb para generar las páginas (vistas) de cada una de las acciones y por último con rspec se generan las pruebas y algunos helpers.
Las líneas de route anteriores implican que si hago una petición get a sample_app/pages/home y sample_app/pages/contact voy a obtener las páginas generadas por erb. Compruebo y todo correcto (que plantilla más fea).
Es hora de hacer que se muestre una página html plana, para ello, abro el controlador que acabo de crear:

```prettyprint linenums

class PagesController < ApplicationController
  def home
  end

  def contact
  end

end

```

Efectivamente, las acciones están vacías, así que salvo la lógica que esté definida por defecto en ApplicationController, no se ejecuta nada, habrá que redirigir a la vista, ¿no?
Punto interesante, en Ruby on Rails, se ejecuta el controlador y a continuación se renderiza la vista, es decir, no voy a tener que "redirigir"... cosa que por otra parte ya había comprobado experimentalmente, la vista estaba saliendo pero el controlador estaba vacío.
Si abro la vista en sample_app/app/views/pages, me encuentro esto:

```prettyprint linenums

&lt;h1&gt;Pages#home&lt;/h1&gt;
&lt;p&gt;Find me in app/views/pages/home.html.erb&lt;/p&gt;

```

Es decir, html SIN encabezado, ni body, ni nada. Solo la manteca. Esta bien, esto va indicando a algún sistema de plantillas como pensaba más arriba.
Se acabó. Así se sirve contenido estático.
Generalizando, con generate se crea el controlador, las vistas, etc y en views tenemos las páginas en las cuales puedo poner el html relevante.
Esta bien, se sube a git y palante.

```prettyprint linenums

$ git add .
$ git commit -am "Añadido controlador Pages (contenido estático)"

```
