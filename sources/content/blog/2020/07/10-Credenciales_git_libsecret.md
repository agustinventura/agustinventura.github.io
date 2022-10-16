title=Gestión de Credenciales de Git en Ubuntu Linux
date=2020-07-10
type=post
tags=Linux, Ubuntu, Git, Credenciales
status=published
~~~~~~

Últimamente he tenido que provisionar dos equipos nuevos (en casa y en el trabajo) y parte del proceso es instalar Git para acceder a los distintos repositorios (como el de este blog).

El acceso a un repositorio remoto de Git se puede hacer de dos maneras:

1. [Por cruce de clave SSH](https://git-scm.com/book/en/v2/Git-on-the-Server-Generating-Your-SSH-Public-Key): De lejos el más cómodo y mejor una vez configurado. Generas un clave en tu equipo, subes la parte pública a GitHub, GitLab, etc... y a volar. El problema es que es harto tedioso.
2. Mediante HTTPS: Cada vez que operemos sobre el repositorio remoto será como acceder a una página web y nos pedirá usuario y contraseña (credenciales). Este sistema es el más sencillo, pero dado el número de operaciones que puedes hacer en un rato sobre un remoto resulta muy tedioso estar introduciendo usuario y contraseña continuamente.

Ahí entra el concepto de [Credential Helper] (https://git-scm.com/docs/gitcredentials), habiendo a su vez varias opciones:

1. [Cache](https://git-scm.com/docs/git-credential-cache): Almacena las credenciales en memoria durante un tiempo determinado (900 sgs por defecto).
2. [Store](https://git-scm.com/docs/git-credential-store): Los almacena en un fichero... _en texto plano_. No es plan.

La solución idónea pasa por utilizar el [Keyring](https://askubuntu.com/questions/32164/what-does-a-keyring-do) del sistema operativo para guardar las credenciales cifradas y afortunadamente esto es bastante sencillo de hacer gracias al proyecto [Libsecret] (https://wiki.gnome.org/Projects/Libsecret) de GNOME. La instalación es bien sencilla:

```prettyprint
sudo apt-get install libsecret-1-0 libsecret-1-dev
cd /usr/share/doc/git/contrib/credential/libsecret
sudo make
git config --global credential.helper /usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret
```

Con apt-get se instala libsecret pero en formato fuente, por lo que hace falta ir al directorio de instalación y compilarlo (make). A partir de ahora nos pedirá las credenciales del repositorio tan solo en dos ocasiones:

1. Cuando sea la primera vez que accedemos.
2. Cuando hayan cambiado.