title=Seguimos con el Tuíte, ahora vamos a crear los microposts
date=2010-12-02
type=post
tags=Programación,Ruby on Rails
status=published
~~~~~~

<p>La estructura de un micropost es fácil a más no poder:</p>


<ul>
<li>content (string)</li>
<li>user_id (integer)</li>
<li>que guay que rails me genera solo el id para los microposts :)</li>
</ul>


<p>Así que nada, tiro de nuevo de scaffolding:</p>


```prettyprint linenums
case@aesir:~/RoR/proyectos/demo_app$ rails generate scaffold Micropost content:string user_id:integer
```


<p>Y hago el migrate para crearlo en la base de datos</p>


```prettyprint linenums
case@aesir:~/RoR/proyectos/demo_app$ rake db:migrate
(in /home/case/RoR/proyectos/demo_app)
==  CreateMicroposts: migrating ===============================================
-- create_table(:microposts)
   -&gt; 0.0061s
==  CreateMicroposts: migrated (0.0066s) ======================================
```


<p>Si hago un cat del route.rb, me sale que efectivamente ha añadido solo los microposts</p>


```prettyprint linenums
cat config/routes.rb
DemoApp::Application.routes.draw do
  resources :microposts

  resources :users
```


<p>Esto del router no lo veo yo muy claro, estaría bien profundizar en esta parte de la arquitectura, quiero decir, si tengo el controlador, ¿para qué es el router? hmmm<br />
Como en el caso de Users, la combinación de métodos http con la url, me dá todas las acciones posibles, listar todos, crear, editar, ver y borrar, un CRUD de toda la vida, nada nuevo por aquí.<br />
Esta vez voy a mirar el controlador pero voy a tratar de entender algo, el asunto en cuestión esta en app/controllers/microposts_controller.rb, la primera cosa que me llama la atención es que puede devolver la salida tanto en html como en xml y parece que nativamente, tiene sentido de cara a una integración con web services.<br />
Aparte estan comentados los métodos a los que se responde, voy a mirar el método del formulario para crear un nuevo micropost (http://localhost:3000/microposts/new):</p>


```prettyprint linenums

form id="new_micropost" class="new_micropost" action="/microposts" accept-charset="UTF-8" method="post"

```


<p>Ahí esta, va en un post, creo uno y le doy a edit, ver código fuente:</p>

hmm... un poco más abajo:

```prettyprint linenums

input name="_method" type="hidden" value="put" />
```


<p>Parece que sobreescribe el método con algún javascript de satanás... habrá que investigarlo también.<br />
En el caso del enlace de borrar:</p>


```prettyprint linenums
a href="/microposts/1" data-confirm="Are you sure?" data-method="delete" rel="nofollow" 
```


<p>Ahí tenemos también el método y el mensaje de confirmación para el borrado, está bien.<br />
Evidentemente me deja crear un micropost con user_id = 2 sin problema, no se ha forzado la integridad referencial... aún.<br />
Pero primero el tutorial me sugiere añadir un tamaño máximo al contenido de los micropost, 140, pero yo voy a escoger 144 que es 12^2 y me mola más...<br />
Edito el modelo de micropost en app/models/micropost.rb</p>


```prettyprint linenums
case@aesir:~/RoR/proyectos/demo_app$ cat app/models/micropost.rb
class Micropost &lt; ActiveRecord::Base 	validates :content, :length =&gt; { :maximum =&gt; 144}
end
```


<p>Voy a probarlo... (con <em>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis aliquet arcu vitae massa pharetra nec malesuada diam facilisis. Donec orci aliquam.</em>) y...</p>


```prettyprint linenums
1 error prohibited this micropost from being saved:
Content is too long (maximum is 144 characters)
```


<p>Perfecto, le quito una letra y pa dentro, funciona.<br />
A por la integridad referencial. Vamos a ver, un usuario tiene muchos microposts... pues eso pero en inglés:</p>


```prettyprint linenums
case@aesir:~/RoR/proyectos/demo_app$ cat app/models/user.rb
class User &lt; ActiveRecord::Base
	has_many: micropost
end
```


<p>Y claro, un micropost... "pertenece" a un usuario:</p>


```prettyprint linenums
class Micropost &lt; ActiveRecord::Base 	belongs_to :user 	validates :content, :length =&gt; { :maximum =&gt; 144}
end
```


<p>El tutorial sugiere que se mire mediante la consola de rails, que me dá la impresión que es una especie de intérprete del sql de RoR, algo similar al intérprete de hql de Eclipse, por ejemplo:</p>


```prettyprint linenums
case@aesir:~/RoR/proyectos/demo_app$ rails console
Loading development environment (Rails 3.0.1)
ruby-1.9.2-p0 &gt; first_user = User.first
SyntaxError: /home/case/RoR/proyectos/demo_app/app/models/user.rb:2: syntax error, unexpected ':', expecting keyword_end
	has_many: micropost
	         ^
```


<p>Yeeeppaaa, fallo de síntaxis! Corrijo y:</p>


```prettyprint linenums
Loading development environment (Rails 3.0.1)
ruby-1.9.2-p0 &gt; first_user = User.first
 =&gt; #
ruby-1.9.2-p0 &gt;
```


<p>Y</p>


```prettyprint linenums
ruby-1.9.2-p0 &gt; first_user.microposts
 =&gt; [#, #, #]
ruby-1.9.2-p0 &gt;
```


<p>Hora de poner a prueba esa integridad referencial en la web... primero voy a hacer un db:migrate por lo que pueda pasar y a ver... Pues me deja, supongo que habrá que hacer algo más, se me estará escapando alguna cosa.<br />
Sigo con el tutorial que ya entraremos en eso, digo yo.<br />
Lo que viene ahora es una chapa de teoría y además muy parecida a lo que gasto yo en el trabajo, todas las clases del modelo heredan de ActiveRecord::Base (que algo me dice que implementa toda la funcionalidad CRUD parametrizando simplemente el nombre de tabla). Nota: Sería muy interesante ver si hay soporte para tipos de acceso a las colecciones, es decir, si el acceso a microposts se podría definir como lazy o eager a là JPA.<br />
Los controladores heredan de ApplicationController que a su vez hereda de ActionController::Base (¿por qué algunas clases llevan el ::Loquesea y otras no?). El ActionController según dice el tutorial, aporta métodos de conveniencia para la gestión de http y generación de html, así como acceso a las entidades del modelo.<br />
Pos mu bien.<br />
Toca subida a GitHub y a Heroku, simplemente para refrescar la memoria con los comandos.

<p>El capítulo termina con una serie de comentarios (Strengths and Weaknesses), comentarios sobre las debilidades:</p>


<ul>
<li>No custom layout or styling. Hmm... esto no creo que sea realmente un problema, cualquier aplicación web tiene este problema al principio =)</li>
<li>No static pages (like “Home” or “About”), tampoco creo que sea algún problema, digo yo que rails podrá servir contenido estático.</li>
<li>No user passwords... bueno, ya puestos, podríamos tirar de LDAP... o algo asín, ¿alguien dijo soporte de certificado digital? Dios, mi trabajo me está obsesionando.</li>
<li>No user images</li>
<li>No signing in</li>
<li>No security. Este resume el anterior y el de contraseñas ¿no? No creo que valga repetir ;P</li>
<li>No automatic user/micropost association. Síiiii</li>
<li>No notion of “following” or “followed”... ¿esto no sería una relación de User sobre sí mismo?</li>
<li>No micropost feed</li>
<li>No test-driven development. Me parece que es ponerse un poco pijo, pero vale.</li>
<li><strong>No real understanding. Aquí estoy de acuerdo!</strong></li>
</ul>


<p>Y fín, del capítulo, supongo que en el próximo empezará la manteca.</p>

