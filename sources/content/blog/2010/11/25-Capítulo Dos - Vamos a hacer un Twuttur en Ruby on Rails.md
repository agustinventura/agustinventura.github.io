title=Capítulo Dos - Vamos a hacer un Twuttur en Ruby on Rails
date=2010-11-25
type=post
tags=Programación,Ruby on Rails
status=published
~~~~~~
Pues eso, utilizando <a title="Wikipedia - Scaffolding" href="http://en.wikipedia.org/wiki/Scaffold_(programming)" target="_blank">scaffolding</a> a cascoporro vamos a hacer un Twuttur, la idea no es hacerme experto en RoR del tirón, sino ir poco a poco viendo la estructura en general y el funcionamiento de una aplicación.

```prettyprint linenums
rails new demo_app
```

Y ya tenemos la base creada. Edito el Gemfile, que creo recordar que contiene los módulos (Gems) de los que depende la aplicación. Lo dejo con esta pinta:

```prettyprint linenums
source 'http://rubygems.org'

gem 'rails', '3.0.1'
gem 'sqlite3-ruby', '1.2.5', :require =&gt; 'sqlite3'
```

Esc+:wq... entiendo que estoy diciendo que voy a usar rails 3.0.1 y sqlite3-ruby 1.2.5 lo cual depende de sqlite3. Para instalar estas dependencias:

```prettyprint linenums
bundle install
```

Ahora, antes de seguir, commit inicial a GitHub, creando previamente un repositorio.

```prettyprint linenums
git init
Initialized empty Git repository in /home/case/RoR/proyectos/demo_app/.git/
case@aesir:~/RoR/proyectos/demo_app$ git add .
case@aesir:~/RoR/proyectos/demo_app$ git commit -m "Commit Inicial"
case@aesir:~/RoR/proyectos/demo_app$ git remote add origin git@github.com:agustinventura/demo_app.git
case@aesir:~/RoR/proyectos/demo_app$ git push origin master
Counting objects: 63, done.
Compressing objects: 100% (48/48), done.
Writing objects: 100% (63/63), 85.79 KiB, done.
Total 63 (delta 2), reused 0 (delta 0)
To git@github.com:agustinventura/demo_app.git
 * [new branch]      master -&gt; master
```

Con esto, como he venido viendo, ya estoy listo para empezar a picar código.
En primer lugar, las entidades, hay dos claramente definidas con los siguientes atributos:

<ol>
	<li>User: id (integer), name (string), mail (string)</li>
	<li>Micropost: id (integer), content (string), user_id (integer)</li>
</ol>

Me gusta mucho que primero se definan las entidades conceptualmente y después nos metamos a ver si tablas en base de datos, si clases o qué... primero un modelo de datos consistente, el resto vendrá solo.
Ahora, se tira de scaffold para generar el User, importante, no se indica el id porque se genera automáticamente:

```prettyprint linenums
rails generate scaffold User name:string email:string
invoke  active_record
      create    db/migrate/20101123192053_create_users.rb
      create    app/models/user.rb
      invoke    test_unit
      create      test/unit/user_test.rb
      create      test/fixtures/users.yml
       route  resources :users
      invoke  scaffold_controller
      create    app/controllers/users_controller.rb
      invoke    erb
      create      app/views/users
      create      app/views/users/index.html.erb
      create      app/views/users/edit.html.erb
      create      app/views/users/show.html.erb
      create      app/views/users/new.html.erb
      create      app/views/users/_form.html.erb
      invoke    test_unit
      create      test/functional/users_controller_test.rb
      invoke    helper
      create      app/helpers/users_helper.rb
      invoke      test_unit
      create        test/unit/helpers/users_helper_test.rb
      invoke  stylesheets
      create    public/stylesheets/scaffold.css
```

Una vez más me encuentro con buenas prácticas embebidas (bonito palabro...), se generan automáticamente los tests unitarios. Muy bien.
Mirando bien la salida esta también el controlador y hasta el CSS!! Vamos, que esta listo para funcionar, solo hay que crear la base de datos.
Para eso se "migra" usando Rake, el tutorial promete explicar más adelante esto de las migraciones, de momento ejecuto el comando en plan script-kiddie:

```prettyprint linenums
rake db:migrate
(in /home/case/RoR/proyectos/demo_app)
==  CreateUsers: migrating ====================================================
-- create_table(:users)
   -&gt; 0.0285s
==  CreateUsers: migrated (0.0287s) ===========================================
```

Comparando los tiempos que tarda mi portátil en ejecutar las cosas con el tutorial me entran ganas de llorar... pero no de ahorrar para comprar uno nuevo, jeje.
Arranco el servidor con

```prettyprint linenums
rails s
```

Y en http://localhost:3000/ tengo la aplicación. Joder, de momento es igual que la de ejemplo, lo mismo me he equivocao.
Pues no, es que esta en http://localhost:3000/users, ha generado solo toda la funcionalidad CRUD, ahí tenemos un listado de usuarios (inicialmente vacío) con la opción de añadir nuevo y para los existentes, show, edit y destroy.
Se me ocurre que siendo un poco cabrón puedo inyectar código malicioso... a ver qué tratamiento hace por defecto, pero bueno, tampoco me voy a poner en ese plan, que hay más cosas que aprender.
Interesante, cuando le doy a destroy automáticamente me dispara un confirm javascript.
Ahora el tutorial pasa a una discusión sobre el MVC en Ruby on Rails. De entrada me llama la atención que el controlador invoca la clase que genera el html y es el controlador el que devuelve el html. Aparte, las peticiones pasan obligatoriamente por un router de Rails.
Y llegamos a la madre del cordero, la arquitectura REST. Simplificadamente, es algo para lo que la especificación de servlets de Java tiene soporte pero nunca se ha usado y la verdad sea dicha, a mí me parece extremadamente elegante. Consiste en usar el par url | método http para definir la acción que hace el usuario. Por ejemplo http://localhost:3000/users | GET significa "quiero el listado de usuarios", pero http://localhost:3000/users | POST significa "quiero crear el usuario (cuyos datos van en el POST)"... espectacular, sencillo y se adapta como un guante al http.
La vista... la vista... jejeje... el users/index.html.erb es good old jsp como el que dice pero con Ruby dentro en vez de Java, la verdad que muchas veces echo de menos este enfoque en el mundo de componentes JSF, GWT, etc... En fín, a lo que iba, por lo visto el controlador carga la variable @users y el erb puede verla automáticamente.
Esta parte acaba con una reseña sobre el scaffolding, explicando, por ejemplo, que no te valida los datos (me autorrespondo), que no te genera un layout (vaya, esto es más plano que google) y que los tests generados son bastante inflexibles. Además no hay login ni autenticación de ningún tipo.
Bueno, poco a poco, ya es bastante que te genera el CRUD solo y de una forma bastante clara.
Para el próximo día me dejo de deberes la parte de microposts que incluye ya cosas como validaciones y relaciones 1:n.