title=Un poco de Ruby para Rails
date=2011-02-21
type=post
tags=Programación,Ruby on Rails
status=published
~~~~~~
Bueno, parece que me han escuchado. El capítulo 4 del tutorial va sobre Ruby más que sobre Rails, para profundizar en el lenguaje y entender conceptos básicos (más allá de lo que viene siendo una variable de instancia...).
Lo que voy a hacer es definir un helper para construir el contenido de la etiqueta title, en vez de usar una cadena concatenada a una variable. Para ello edito el app/helpers/application_helper.rb y añado esto:

```prettyprint linenums

# Return a title on a per-page basis.
def title
base_title = "Ruby on Rails Tutorial Sample App"
if @title.nil?
base_title
else
"#{base_title} | #{@title}"
end
end
end

```

Es bastante sencillo de leer, si @title viene nulo, se "devuelve??" base_title, en otro caso la concatenación de base_title, | y title. Con ésto ya puedo dejar el título como &lt;%=title%&gt;. <strong>Atención!</strong> que va sin la @, es decir, antes era | &lt;%=@title%&gt; y ahora es &lt;%=title%&gt;, si no, solo sigue usando el título en concreto de la página.
Es decir, title=Ruby on Rails Tutorial Sample App | Help mientras que @title=Help. Según explica @title es la variable, mientras que title es la invocación a la función... Joder, que fuerte.
Entiendo que los métodos definidos en el application_helper son visibles por todas las páginas erb, así como que el scope de @title es "global" en tiempo de traducción de las páginas, por eso el application_helper puede usarlo.
Me encuentro bastante sorprendido... esto es demasiado "ágil" para mí.
Toque de clarines, en un aparente cambio de tercio, se pasa a definir el CSS de la aplicación... que suerte, con lo que me gusta a mí esto. Además toca utilizar un framework CSS, <a href="http://www.blueprintcss.org/" target="_blank">Blueprint</a>, lo cual esta muy guay porque nunca he usado uno, hay que ver la de cosas que estoy aprendiendo con este tutorial.
Abro el tar.gz de la última versión (la 1.0) y descomprimo la carpeta blueprint/ de su interior en $sample_app/public/stylesheets.
Para que lo use la plantilla de la aplicación añado esto al application.html.erb después de csrf_meta_tag:

```prettyprint linenums

&lt;%= stylesheet_link_tag 'blueprint/screen', :media =&gt; 'screen' %&gt;
&lt;%= stylesheet_link_tag 'blueprint/print',  :media =&gt; 'print' %&gt;

```

Entiendo que la parte de stylesheet_link_tag se traduce de alguna manera mágica en un link rel a la hoja de estilo en blueprint/screen o print según proceda.
Efectivamente, stylesheet_link_tag es otro helper (en este caso uno que ofrece Rails) que se encarga de buscar la hoja de estilo en el directorio por defecto (public/stylesheets) y además le concatena el .css. Lo de :media ya me sobrepasa, supongo que será otro parámetro que se pasa al helper.
Por cierto que el código fuente HTML generado por la página es LIMPÍSIMO (acostumbrado a JSF...), esto me recuerda mucho a los scriptlets de JSp :') que tiempos...
Por otra parte el stylesheet_link_tag se traduce en el link rel tal como esperaba, pero la url de la hoja de estilo es esta: /stylesheets/blueprint/screen.css?1290014457 un tanto extraño, ya veremos para qué es.
Ahora parece que se cacharrea con la consola de Ruby, así que antes que nada toca subir a git.
La consola de Ruby es un intérprete, se invoca con

```prettyprint linenums

case@aesir:~/RoR/proyectos/sample_app$ rails console

```

Para interrumpir un proceso en ejecución dentro de la consola: Ctrl-C, para salir de la consola en sí, Ctrl-D.
Y empezamos con la descripción del lenguaje en sí, ya sabía yo que de esta no me libraba, en algún momento tiene que pasar, jeje...
Comentarios: Empiezan con # y se extienden hasta el final de la línea:

```prettyprint linenums

#Esto es un comentario, y lo siguiente es una suma más un comentario
17+42 #Son 69

```

Strings: Entre "", como en Java. Igualmente, se concatenan con +. Por hacer unas pruebas:

```prettyprint linenums

ruby-1.9.2-p0 &gt; ""
=&gt; ""
ruby-1.9.2-p0 &gt; "foo"
=&gt; "foo"
ruby-1.9.2-p0 &gt; "foo" + " " + "bar"
=&gt; "foo bar"
ruby-1.9.2-p0 &gt; foo = "foo"
=&gt; "foo"
ruby-1.9.2-p0 &gt; bar = "bar"
=&gt; "bar"
ruby-1.9.2-p0 &gt; foo + " " + bar
=&gt; "foo bar"
ruby-1.9.2-p0 &gt; "#{foo} #{bar}"
=&gt; "foo bar"

```

Como curiosidad, la última línea. Se imprime foo bar mediante la interpretación de las dos cadenas con #{}. En Ruby a esto se le llama <em>interpolación</em>.
Para imprimir, se usa puts, imprime la cadena y n (retorno de línea) y devuelve nil (nulo, vaya). Hay otro similar, print, que se limita a imprimir la cadena y devolver nils, es decir, no imprime el n.

```prettyprint linenums

ruby-1.9.2-p0 &gt; puts foo
foo
=&gt; nil
ruby-1.9.2-p0 &gt; print foo
foo =&gt; nil
ruby-1.9.2-p0 &gt; print foo+"n" #Esto es igual que puts foo
foo
=&gt; nil

```

También se pueden usar cadenas definidas con comillas simples: 'foo', con una salvedad, NO permiten interpolación! (ésto no era así también en PHP?).

```prettyprint linenums

ruby-1.9.2-p0 &gt; '#{foo}'
=&gt; "#{foo}"

```

Además con estas cadenas puedo usar caracteres especiales sin escaparlos, como en n.

```prettyprint linenums

ruby-1.9.2-p0 &gt; 'esto es para marcar una nueva línea n'
=&gt; "esto es para marcar una nueva línea \n"

```

Total, que la gran utilidad viene a ser que me ahorro escapar los caracteres especiales.
Bueno, ahora que he ido a aprovisionarme al supersol y he estado hablando un rato con mi frutero de confianza, sigo, vamos a por los objetos.
En Ruby <strong>TODO</strong> es un objeto, cosa, que he de admitir que fascina mi lado más "computer scientist", purista y talibán de la informática, así que puedo escribir cosas como:

```prettyprint linenums

ruby-1.9.2-p0 &gt; "foo".length
=&gt; 3
ruby-1.9.2-p0 &gt; "foo".empty?
=&gt; false

```

En el último caso el "?" indica que el método invocado devuelve un booleano. Así que ya se puede hacer control de flujo:

```prettyprint linenums

ruby-1.9.2-p0 &gt; s = "foobar"
=&gt; "foobar"
ruby-1.9.2-p0 &gt; if s.empty?
ruby-1.9.2-p0 ?&gt;  "Es cadena vacía"
ruby-1.9.2-p0 ?&gt;  else
ruby-1.9.2-p0 &gt;     "no es cadena vacía"
ruby-1.9.2-p0 ?&gt;  end
=&gt; "no es cadena vacía"

```

Me gusta el detallito de que algo tan "rudimentario" como un intérprete, te indente el código.
Los operadores a usar son los clásicos para booleanos: ||, &amp;&amp; y !

```prettyprint linenums

ruby-1.9.2-p0 &gt; true &amp;&amp; false
=&gt; false
ruby-1.9.2-p0 &gt; true || false
=&gt; true
ruby-1.9.2-p0 &gt; !true
=&gt; false

```

Me saco de la chistera que los literales booleanos sean true o false, pero oye, funciona.
Siguiendo con el tutorial veo que si se quiere evaluar una sola condición lógica basta con poner instrucción condición, es decir:

```prettyprint linenums

ruby-1.9.2-p0 &gt; puts "Cadena no vacía" if !foo.empty?
Cadena no vacía
=&gt; nil
ruby-1.9.2-p0 &gt; if !foo.empty?
ruby-1.9.2-p0 ?&gt;  puts "cadena no vacía"
ruby-1.9.2-p0 ?&gt;  end
cadena no vacía
=&gt; nil

```

También se puede usar unless para hacer lo mismo:

```prettyprint linenums

ruby-1.9.2-p0 &gt; puts "Cadena vacía" unless !foo.empty?
=&gt; nil

```

Es como aplicar álgebra de Boole al lenguaje en sí, que friki, me parto.
Como última particularidad booleana del lenguaje, nil siempre vale false, todo lo demás, true. Hasta el 0.

```prettyprint linenums

ruby-1.9.2-p0 &gt; puts "Cero vale true" if 0
Cero vale true
=&gt; nil
ruby-1.9.2-p0 &gt; puts "nils es siempre false" unless nil
nils es siempre false
=&gt; nil

```

Por cierto, el toString() es to_s, y nil en sí también es un objeto:

```prettyprint linenums

ruby-1.9.2-p0 &gt; nil.to_s
=&gt; ""
ruby-1.9.2-p0 &gt; nil.to_s.empty?
=&gt; true
ruby-1.9.2-p0 &gt; nil.to_s.nil?
=&gt; false
ruby-1.9.2-p0 &gt; nil.nil?
=&gt; true

```

Y se agradece también que haya un método que chequee para nulos, nil?
Ahora un poco de tipos de variables, ya se ha visto que hay variables locales (title) y "de instancia" (@title), por consola obtenemos esto:

```prettyprint linenums

ruby-1.9.2-p0 &gt; title
NameError: undefined local variable or method `title' for main:Object
from (irb):34
from /home/case/.rvm/gems/ruby-1.9.2-p0@rails3/gems/railties-3.0.1/lib/rails/commands/console.rb:44:in `start'
from /home/case/.rvm/gems/ruby-1.9.2-p0@rails3/gems/railties-3.0.1/lib/rails/commands/console.rb:8:in `start'
from /home/case/.rvm/gems/ruby-1.9.2-p0@rails3/gems/railties-3.0.1/lib/rails/commands.rb:23:in `'
from script/rails:6:in `require'
from script/rails:6:in `'
ruby-1.9.2-p0 &gt; @title
=&gt; nil

```

Como me imagino que todo heredará de Object, voy a echar un vistazo a la <a title="RDoc de Object" href="http://www.ruby-doc.org/core/classes/Object.html" target="_blank">documentación</a> para hacerme una idea de que métodos heredan todos los objetos.
Tenemos .class, == o equal?, is_a? y bastantes métodos más. En general la sintaxis me parece... interesante... ahora voy a hacer un experimentillo de algo que me gustaba bastante hacer en PHP, aprovechando que el lenguaje es de tipado debil.

```prettyprint linenums

ruby-1.9.2-p0 > foo.class
 => String 
ruby-1.9.2-p0 > foo = 0
 => 0 
ruby-1.9.2-p0 > foo.class
 => Fixnum 
ruby-1.9.2-p0 > puts "Ok" if foo == 0
Ok
 => nil 
ruby-1.9.2-p0 > puts "Ok" if foo == "0"
 => nil 
ruby-1.9.2-p0 > foo.to_s.encoding
 => #<Encoding:US-ASCII> 

```

Perfecto, ha respondido maravillosamente a las patochadas que he hecho, y de propina, he descubierto un método que devuelve el encoding de las cadenas, jeje.
Bueno, como todavía voy por el punto 4.2.4 y según la barra de desplazamiento me queda la mitad... mañana más y mejor.