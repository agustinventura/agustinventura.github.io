title=Certificados y Dispositivos en Tizen Studio
date=2018-12-28
type=post
tags=Tizen, JavaScript
status=published
~~~~~~

##Certificados
Una de las cosas que piden para poder subir software (o instalarlo en dispositivos de prueba) en Samsung es disponer de un certificado, tanto de autor como de distribuidor.
Para crear un certificado podemos utilizar el mismo Certificate Manager de Tizen Studio, pero que en esta versión no viene instalado, así que lo primero es ir al Package Manager y en la sección Tizen SDK Tools > Baseline SDK instalar el Certificate Manager.

![Tizen Package Manager and Certificate Manager](/images/2018/12/04-Package_Manager_Certificate_Manager.png)

Y en Extension SDK hay que instalar el Samsung Certificate Extension y el Samsung Wearable Extension.

![Tizen Samsung Certificate Extension](/images/2018/12/04.1-Package_Manager_Extension.png)

En el momento que esta instalado, lo podemos abrir desde el mismo Tizen Studio y pregunta si ya tenemos uno, etc... Resulta que yo tenía uno, pero se me olvidó la contraseña y esto trae bastantes problemas, ya que no puedo actualizar las aplicaciones que tengo publicadas. Primero tengo que eliminarlas y después republicarlas con el nuevo. En fín, ya lo haré, de momento voy a crear un certificado nuevo. En la pantalla inicial, pulso el +

![Empty Certificate Manager](/images/2018/12/05-Certificate_Manager_Empty.png)

Y cuando me pregunta si un certificado de tipo Tizen o Samsung, selecciono Samsung. A continuación dejo marcado Mobile / Wearable y le pongo un nombre al perfil del certificado.

Dejo marcado Create a new author certificate y en la siguiente pantalla pongo mi nombre y una contraseña. Si todo ha ido bien, al darle a next nos pide conectar con la cuenta de Samsung y nos sale la típica ventana de OAuth.

Si todo va bien (a mí me ha dado un par de ventanas de error pero ha seguido funcionando...) nos pide una ruta para guardar una copia de seguridad del certificado y pasamos a crear un nuevo certificado de distribuidor.

Lo dejo todo por defecto e incluso me detecta el DUID (número único de dispositivo) del Gear Sport.

##Dispositivos
Vale, pues ahora que tengo el certificado, voy a probar a ejecutar el Tabata Timer en el Gear Sport que tengo. Para eso hay que configurar primero el dispositivo.
<ul>
<li>En Ajustes > Sobre Gear, habilitar Depuración.</li>
<li>Además hará falta tener el dispositivo en la misma red wifi que el ordenador.</li>
</ul>

Ahora en Tizen Studio abrimos el Device Manager y le damos al Remote Device Manager, que es un icono como de un móvil enganchado a un monitor.

![Remote Device Manager Button](/images/2018/12/07-Remote_Device_Manager.png)

Y en la ventana que sale le damos a Scan Devices (el primer botón que tiene forma... de algo, yo que sé). Si todo ha ido bien veremos en el Gear un aviso con la clave RSA y si queremos conectar, le damos que sí y ya lo vemos en la ventana.

![Remote Device Manager](/images/2018/12/08-Remote_Device_Manager.png)

Pues nada, podemos cerrar (sólo el Remote Device Manager) y ya podemos lanzar la aplicación a tiro de click con el botón derecho Run As > Tizen Web App.