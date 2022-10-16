title=Creando mi propio GitHub Pages
date=2022-10-16
type=post
tags=GitHub, GitHub Pages
status=published
~~~~~~

En [2016](https://www.aguasnegras.es/blog/2016/06/10-wp2jbake-generacion.html) decidí pasar este blog de un WordPress (que me costaba un dinero anual en hosting) a un sitio estático (aunque con comentarios de Disqus). En ese momento estuve muy influenciado
por la web de [Trisha](https://trishagee.com/) que usaba esta arquitectura pero usando todo el potencial de GitHub Pages, con Jekyll y la construcción automática del sitio al subir los
archivos markdown a GitHub (curiosamente ella ahora usa WordPress, pero claro tiene infinito más contenido que yo y de más calidad, jaja).

La cosa es que en su momento no me enteraba muy bien de Jekyll ni de como modificar los temas, etc... por lo que opté por un generador de sitios estáticos en Java llamado [jBake](https://jbake.org/)
que la verdad que esta genial, pero me obligaba a dar un paso más en la gestión de la publicación. Mi workflow era el siguiente:
1. En el repositorio [blog](https://github.com/agustinventura/blog) tenía los fuentes del blog (posts, plantillas, etc...)
2. En el repositorio [agustinventura.github.io](https://github.com/agustinventura/agustinventura.github.io) estaban los htmls resultantes de mezclar los markdown con las plantillas

Esto plantea varios inconvenientes:
- Tener dos repositorios y mantenerlos sincronizados (cosa que hacía lanzando un sh)
- No aprovechar la potencia de GitHub Pages, ya que en realidad el repositorio de pages lo usaba como un simple alojamiento estático

Llevo un tiempo tratando de retomar lo de escribir en el blog y eso requería primero una actualización de la infraestructura con al menos lo siguiente:
- Actualización del workflow de publicación
- Actualización de Disqus (o quitarlo...)
- Actualización de materializecss o cambiarlo por otro framework CSS que siga teniendo mantenimiento

Para actualizar el workflow he vuelto a mirar Jekyll y ya estaba decidido a cambiar a él, comprar un tema, etc... Cuando encontré un gran inconveniente. La cabecera de los posts con los metadatos
en jBake son un [formato propio](https://jbake.org/docs/2.6.5/#metadata_header) mientras que en Jekyll son en [FrontMatter](https://jekyllrb.com/docs/front-matter/) cosa bastante más
razonable, pero no estaba yo por la labor de hacer la migración de todos los posts a FrontMatter y además estoy contento con jBake, lo único que me interesaría sería tener un flujo de publicación
mas automatizado, así que la opción era quedarme con jBake pero automatizar más.

¿Se puede?

Pues sí, en 2018 GitHub lanzó su solución de DevOps, [GitHub Actions](https://github.com/features/actions). En teoría con esto podría detectar cuando hago un push de contenido, "compilarlo"
usando jBake y "desplegarlo" en GitHub Pages.
Cuál no sería mi sorpresa cuando descubrí que GitHub Pages por detrás funciona usando precisamente GitHub Actions y que se podía [tunear](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow)!!!

Venga, pues vamos a echarle un vistazo al workflow a medida, ¿no?

```prettyprint
name: Build blog sources and publish to GitHub Pages
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    permissions:
      id-token: write
      pages: write
    steps:
      - uses: actions/checkout@v3
      with:
        ref: master
      - uses: sdkman/sdkman-action@master
      with:
        candidate: java
        version: 17.0.4.1-tem
      - uses: actions/setup-java@v1
        with:
          java-version: 17.0.4.1
          jdkFile: ${{ steps.sdkman.outputs.file }}
      - uses: wei/wget@v1
      with:
        args: -q https://github.com/jbake-org/jbake/releases/download/v2.6.7/jbake-2.6.7-bin.zip -O jbake-2.6.7-bin.zip
      - uses: montudor/action-zip@v1
      with:
        args: unzip -qq jbake-2.6.7-bin.zip -d .
      - run: sh jbake-2.6.7-bin/bin/jbake -b sources _site
      - uses: actions/upload-pages-artifact@v0
      with:
        path: ./_site
        retention-days: 1
      - uses: actions/deploy-pages@v1
      with:
        artifact_name: github-pages
        preview: false
        token: ${{ github.token }}
```

Lo primero que hay que entender aquí es que he aprendido GitHub Actions sobre la marcha así que seguro que hay mucho que mejorar, jaja. La estructura básica de un workflow es que tiene varios jobs
que a su vez pueden tener varios steps, aunque en este caso tenemos un único job con ocho pasos.

Lo primero es darle un nombre y decirle cuando se va a ejecutar (el on), en este caso con cualquier push (solo va a haber una rama, master porque este repositorio es añejo, si fuera más moderno sería main).
Tras eso defino el job de la siguiente manera:
El entorno de ejecución será la última ubuntu (el run-on: ubuntu-latest). El environment representa el entorno de despliegue. Se pueden crear los entornos que se deseen para cualquier repositorio
(por ejemplo, dev o prod) pero cuando tienes habilitado GitHub Pages en un repositorio se define automáticamente un entorno llamado github-pages. Aquí hay que referenciarlo para saber donde desplegar.
En permissions hablamos de los permisos que va a tener el job (representado a través de un token llamado GITHUB_TOKEN), en este caso le damos permisos de escritura para sí mismo (hará falta para una
action posterior) y permisos de escritura en pages (GitHub Pages, se entiende).
Y empezamos con los pasos en sí que son bastante sencillos:
1. Con checkout@v3 se descarga la rama master del repositorio, el último commit nada más.
2. Con sdkman-action se instala [sdkman](https://www.aguasnegras.es/blog/2018/10/12-sdkman.html) y Java para ejecutar jBake
3. setup-java es autoexplicativo, se configura el Java que se acaba de instalar
4. Para jBake tenemos que dar dos pasos: primero descargarlo usando wget
5. Segundo, descomprimirlo usando el action-zip
6. Pues ya estaría el entorno instalado y configurado y los fuentes bajados, así que con el run de jbake le digo que compile los fuentes del blog que estan en la carpeta sources y los deje en _site
7. Con uploads-pages-artifact lo que se hace es generar un zip con los archivos del blog (_site)
8. Y por último, con deploy-pages, se sube el artefacto al environment de GitHub Pages. Aquí es donde necesito el token y por eso tengo que darle permisos de escritura del token en sí.

Y listo, con esto simplifico el contenido del repositorio (ya solo contiene los fuentes y el CNAME) y puedo publicar simplemente haciendo push.