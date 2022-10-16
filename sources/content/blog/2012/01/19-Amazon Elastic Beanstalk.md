title=Amazon Elastic Beanstalk
date=2012-01-19
type=post
tags=Amazon,Cloud,Java,Programación,tutorial
status=published
~~~~~~
Visto que con Heroku se me esta atragantando el tema del despliegue de JSF 2, me he decidido a seguir los cantos de sirena y probar Amazon Elastic Beanstalk. La publicidad dice que Amazon me dá gratuitamente un Tomcat 6 o Tomcat 7 en la nube, así que merecía darle una ojeada. Lo primero de lo que me doy cuenta es que <a title="Amazon Elastic Beanstalk" href="http://aws.amazon.com/es/elasticbeanstalk/" target="_blank">Amazon Elastic Beanstalk</a> en realidad no es solo un Tomcat, sino que mas bien podríamos definirlo como un agrupamiento de tecnologías que Amazon ya tenía que se ofrecen simplificadamente y bajo un mismo paragüas, como EC2, S3, EBS, CloudWatch, etc... La página de Beanstalk promete que se despliegan WARs normales y corrientes y que se puede usar cualquier librería Java con normalidad, a esto le sumamos Amazon SimpleDB como base de datos relacional y Amazon DynamoDB como NoSQL y tenemos un stack potentísimo a nuestra disposición. Esta la parte buena, ahora la mala.

La mala para empezar es que solo dan un año de <a title="AWS Free Usage Tier" href="http://aws.amazon.com/es/free/" target="_blank">uso gratuito</a>. Pero no un año de tiempo de computación ni nada así, no. Un año de uso desde el momento del registro. Punto. Un poco rácano a mi parecer, preferiría que me limitasen más en recursos disponibles y no tener límite de tiempo, pero bueno.

Para continuar la muy mala. La muy mala es que, por lo que te piden en el registro, parece que vivo en Libia o en Cuba o qué sé yo. Durante el proceso de registro hay que crear una cuenta, proporcionar una tarjeta de crédito (¿no es gratuito? Entiendo que la pidan por si me paso de recursos, pero quizás en ese caso sería preferible echar abajo el servicio oportuno hasta el mes siguiente) y te hacen una llamada telefónica para que confirme con un pin que aparece en la pantalla tu identidad. Lo dicho, un poco paranoide.

Una vez habiendo pasado por todo este calvario, me decido a seguir el primer <a title="Tutorial AWS" href="http://aws.amazon.com/articles/4412341514662386" target="_blank">tutorial de ejemplo</a> en Amazon.

<strong>Resumen</strong>

<ol>
	<li>Instalar Eclipse 3.7 JEE y el plugin <a title="AWS Toolkit" href="http://aws.amazon.com/es/eclipse/">AWS Toolkit</a> para Eclipse.</li>
	<li>Crear un proyecto y configurar la cuenta de AWS.</li>
	<li>Análisis del proyecto.</li>
	<li>Crear un servidor en Elastic Beanstalk y desplegar el proyecto.</li>
	<li>Modificar el proyecto y redesplegar.</li>
	<li>Parar el servidor.</li>
</ol>

<strong>Paso 1</strong>

Descargar el Eclipse for Java EE Developers en la versión oportuna (en mi caso, Linux 64 bits) de <a title="Descarga de Eclipse" href="http://www.eclipse.org/downloads/">aquí</a>. Cuando haya bajado basta con descomprimirlo y ejecutarlo.

Para instalar el AWS Toolkit, una vez abierto el Eclipse, pulso Help &gt; Install New Software ... &gt; Add y en el diálogo Add Repository, en Name pongo "AWS" y en Location "http://aws.amazon.com/eclipse", Ok. Selecciono el nuevo repositorio en el desplegable y ya abajo sale "AWS Toolkit for Eclipse". Lo selecciono y Next, Next, acepto las licencias, acepto que se instale software sin firmar (sigh) y reinicio Eclipse una vez instalado.

Entorno instalado, guay, sin mayor problema.

<strong>Paso 2</strong>

Para crear un proyecto para desplegar en AWS, hago click en File &gt; New &gt; Other &gt; AWS &gt; AWS Java Web Project.

<a href="/images/2012/01/1-Nuevo-Proyecto-AWS.png"><img class="size-medium wp-image-384" title="Nuevo Proyecto AWS" src="/images/2012/01/1-Nuevo-Proyecto-AWS-300x244.png" alt="Nuevo Proyecto AWS" width="300" height="244" /></a>

Pulso Next. Para que un proyecto AWS sea desplegable necesita una información acerca de la cuenta del desarrollador, eso, junto con el nombre del proyecto es lo que tengo que configurar en esta pantalla. Como es la primera vez que entro, tengo que crear la cuenta, así que hago click en "Configure AWS Accounts" y veo la siguiente pantalla.

<a href="/images/2012/01/2-AWS-Accounts.png"><img class="size-medium wp-image-385" title="Configurar cuenta de AWS" src="/images/2012/01/2-AWS-Accounts-300x248.png" alt="Configurar cuenta de AWS" width="300" height="248" /></a>

Y ahí estan los datos de la cuenta, hay que ponerle un nombre de cuenta (meramente identificativo para el Eclipse), una clave de acceso y una clave secreta. Como no tengo ni idea de que es eso, hago click encima de "find your existing AWS security credentials" y una vez logado en la página de AWS veo una pantalla que haciendo scroll tiene esta pinta:

<a href="/images/2012/01/3-Security-Credentials.png"><img class="size-medium wp-image-386" title="Credenciales de Seguridad" src="/images/2012/01/3-Security-Credentials-300x163.png" alt="Credenciales de Seguridad" width="300" height="163" /></a>

Ahí (en el borrón) esta la clave de acceso y si hago click en "mostrar" veo la clave secreta. Pues nada, copiar y pegar a la ventana del Eclipse. Hago click en Ok y en la pantalla de configuración del proyecto dejo seleccionado "Basic Java Web Application". Finish.

<strong>Paso 3</strong>

El proyecto recién creado es un proyecto web dinámico normal de Eclipse.

<a href="/images/2012/01/4-Proyecto-recién-creado.png"><img class="size-medium wp-image-387" title="Proyecto Java Web AWS" src="/images/2012/01/4-Proyecto-recién-creado-300x163.png" alt="Proyecto Java Web AWS" width="300" height="163" /></a>

Tiene una carpeta src/ en la que se encuentran los fuentes de Java, de momento vacía, una carpeta webcontent en la que va el contenido web de la aplicación (jsp, html, css, js, png, gif, etc...) y dentro de ella, como es habitual, una carpeta WEB-INF con el web.xml dentro y un directorio lib (también vacío).

El web.xml es absolutamente normal, y lo único destacable es que dentro de src/ se encuentra un archivo llamado "AWSCredentials.properties" que contiene... las credenciales en texto plano. Bueno, yo no es por ser destroyer, al fín y al cabo esa información solo es accesible para el desarrollador (es decir, yo mismo), pero tampoco cuesta trabajo cifrarlo con algún hash, por aquello de mejorar algo la seguridad. Sus motivos tendrán.

De momento, el proyecto cumple lo prometido, Java Web normal y corriente. Ahora toca ver qué tal la ejecución.

<strong>Paso 4</strong>

Para ejecutar el proyecto, hago click encima de él con el botón derecho y selecciono Run As &gt; Run on Server... En esta pantalla dejo seleccionado "Manually define a new server" y selecciono un AWS Elastic Beanstalk for Tomcat 6. En "Server host name" escribo Tomcat6AWS y pulso Next.

<a href="/images/2012/01/5-Run-on-Server.png"><img class="size-medium wp-image-388" title="Nuevo Tomcat 6 AWS" src="/images/2012/01/5-Run-on-Server-253x300.png" alt="Nuevo Tomcat 6 AWS" width="253" height="300" /></a>

En la siguiente pantalla tengo que seleccionar para empezar una región en la que desplegar el proyecto. No sé si será un bug del plugin o que solo esta permitido ahí, pero solo me deja seleccionar US-East(Northern Virginia). Me hubiera gustado más seleccionar Europe(Ireland) por aquello del tiempo de latencia, pero bueno.

Lo siguiente son conceptos ya propios de Amazon Elastic Beanstalk. Una aplicación (application) es un producto software (un WAR, vaya) con una configuración y una versión determinada, mientras que un entorno (environment) es una instancia determinada de esa aplicación.

Pues vale, dejo marcado "Create a new application" y en Name pongo AWSJavaWeb. Para el Environment uso de nombre AWSJavaWeb igualmente.

<a href="/images/2012/01/6-Application-y-Environment.png"><img class="size-medium wp-image-390" title="Application y Environment" src="/images/2012/01/6-Application-y-Environment-247x300.png" alt="Application y Environment" width="247" height="300" /></a>

En la siguiente pantalla, Advanced Configuration, la verdad que no entiendo nada, parece que es algún sistema de autenticación (¿otro?), pero sigo el tutorial y selecciono "Deploy with a key pair" y le doy a Add (la cruz verde). Me sale un diálogo para introducir un nombre y un directorio, de nombre uso AWSJavaWeb y el directorio lo dejo tal y como esta. Pulso Ok y pulso Finish.

<a href="/images/2012/01/7-Advanced-Configuration.png"><img class="size-medium wp-image-392" title="Advanced Configuration" src="/images/2012/01/7-Advanced-Configuration-247x300.png" alt="Advanced Configuration" width="247" height="300" /></a>

Pero todavía sale un cuadro de diálogo más... pidiéndome la versión de la aplicación, claro. Escribo v20120118.01 (primera versión, 18 de Enero de 2012).

<a href="/images/2012/01/8-Environment-Version.png"><img class="size-medium wp-image-394" title="Versión de la Aplicación" src="/images/2012/01/8-Environment-Version-300x115.png" alt="Versión de la Aplicación" width="300" height="115" /></a>

Pulso OK y espero mientras el cuadro de diálogo me va informando. Entiendo que el proceso es generar un WAR, subirlo a Amazon S3, crear una instancia de Amazon EC2 con el Tomcat 6 y desplegarlo... nada más... Cuando acaba:

<a href="/images/2012/01/9-Resultado.png"><img class="size-medium wp-image-396" title="Aplicación desplegada en Elastic Beanstalk" src="/images/2012/01/9-Resultado-300x163.png" alt="Aplicación desplegada en Elastic Beanstalk" width="300" height="163" /></a>

<strong>Paso 5</strong>

Para ver como lleva esto los cambios, abro index.jsp y cambio el contenido de la etiqueta "title" a lo siguiente: Hello agustinventura AWS Java Web Application.

Guardo los cambios, click con el botón derecho en el proyecto, Run As &gt; Run on Server... Selecciono el servidor que ya he creado y hago click en Finish. Me vuelve a salir el cuadro de dialogo para la versión, esta vez escribo v20120118.02 y OK.

Vuelvo a esperar (aunque menos) y...

<a href="/images/2012/01/10-Cambios.png"><img class="size-medium wp-image-399" title="Cambios Desplegados" src="/images/2012/01/10-Cambios-300x163.png" alt="Cambios Desplegados" width="300" height="163" /></a>

Ahí esta, cambios desplegados en producción.

<strong>Paso 6</strong>

Para evitar que el servidor siga funcionando (y por tanto, me facturen), lo tengo qué parar. ¿Cómo? Pues en la pestaña Servers, lo selecciono y hago click en Stop (el botón rojo, o bien click con el botón derecho encima del servidor y Stop).

Y aquí me llevo la primera decepción, aunque tampoco es muy importante, tras 10 minutos esperando, decido entrar en la <a title="Consola de AWS" href="https://console.aws.amazon.com/s3/home" target="_blank">consola de aws</a> ya que me parece extraño. Entro, selecciono AWS Elastic Bean Stalk, la aplicación y al hacer click en Events, veo que ya se ha parado... hace 10 minutos. Vaya, que el plugin se ha quedado colgado, habrá que reportarlo.

<a href="/images/2012/01/11-Consola-AWS.png"><img class="size-medium wp-image-400" title="Consola AWS" src="/images/2012/01/11-Consola-AWS-300x149.png" alt="Consola AWS" width="300" height="149" /></a>

<strong>Conclusiones</strong>

Básicamente, y a falta de hacer algo más complejo, puedo dividir las conclusiones en pros y contras:

Pros:

<ol>
	<li>Parece que el desarrollo es Java Web "estándar".</li>
	<li>El servidor de despliegue es un Tomcat (con todas sus cosas buenas y malas).</li>
	<li>El plugin para Eclipse, todo un detalle.</li>
</ol>

Contras:

<ol>
	<li>El proceso de alta... creo que fue más fácil darme de alta en Paypal...</li>
	<li>¿Solo un año de prueba?¿De verdad?</li>
	<li>Los dos puntos anteriores me hacen concluir que el entorno es digamos... poco amistoso para desarrolladores aficionados, o porqué no, startups. En este sentido lleva ventaja Heroku.</li>
</ol>

El próximo paso que me gustaría dar es la prueba de fuego, a ver como se comporta para desplegar JSF 2 (que tengo atragantado en Heroku).
