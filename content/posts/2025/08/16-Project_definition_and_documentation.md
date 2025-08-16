---
title: Definición de Proyectos y Documentación Ligera
date: 2025-08-16
tags:
  - Development
  - Documentación
  - README.md
  - ADRs
  - CONTRIBUTING.md
  - C4 Model
---

### La tentación de empezar a programar (y por qué deberías esperar)

Como desarrolladores, nuestro primer impulso al empezar un proyecto es casi siempre el mismo: abrir el IDE y ponernos a picar código. 🚀 Ya sea eligiendo dependencias, escribiendo tests o definiendo el modelo de dominio, esa es la parte divertida, ¿verdad?

Este enfoque funciona para pruebas de concepto rápidas. Pero si estás construyendo un producto a largo plazo, sobre todo en equipo, necesitas un plan. Hasta la idea más simple puede significar algo diferente para cada persona.

Poner las cosas por escrito no es para crear reglas inamovibles, sino para tener **una referencia compartida**. Un mapa que nos guíe y que, por supuesto, puede cambiar y evolucionar. Lo importante es que esa evolución quede registrada para que todo el equipo sepa hacia dónde vamos.

### El ejemplo del *leaderboard*

Imagina una tabla de clasificación para un videojuego.

* **Mi idea inicial**: Pienso en las recreativas de los 80. Dos columnas (`PLAYER` y `SCORE`) y un top 10. Simple.
* **Otras posibles ideas**: ¿Por qué solo diez? ¿Y si añadimos el número de partidas? ¿O la puntuación media? ¿Y si registramos la fecha para ver el mejor jugador de la semana, del mes o del año? Si el juego es online, ¿podríamos tener un ranking por regiones?

Se entiende, ¿no? 🤔 Si no registras el alcance del proyecto, es muy fácil caer en un ciclo de desarrollo sin fin o tener la sensación de que nunca terminas nada.

---

### Paso 1: Definir el «qué» (lo que vamos a construir)

El primer objetivo es claro: documentar qué estamos construyendo **ahora**.

#### El `README.md`: tu punto de partida

El lugar más sencillo y universal para esto es un archivo `README.md` en la raíz del proyecto. Es un estándar y lo primero que cualquiera mira en un repositorio.

Para nuestro *leaderboard*, podría ser algo así:

```markdown
Este proyecto es un servicio de backend para gestionar un leaderboard de videojuegos. Su objetivo es registrar las puntuaciones de los jugadores y ofrecer un ranking global.

El desarrollo de este servicio sirve como un ejercicio práctico para aplicar y documentar principios de diseño y arquitectura de software.
```

Y luego, detallar la funcionalidad principal:

```markdown
**Entrada de datos:**
El servicio ofrece dos mecanismos para gestionar puntuaciones:
* **Interfaz Asíncrona:** Para comunicación entre sistemas (backend-to-backend).
* **Interfaz Síncrona:** Para herramientas de administración que requieren una respuesta inmediata.

**Consulta de datos:**
* **Interfaz Síncrona:** Para solicitar el ranking actualizado de jugadores.
```

#### Una imagen vale más que mil palabras: Diagramas C4

Pero el «qué» no es solo texto. Para visualizar la arquitectura, olvídate de UML y prueba [**C4 Model**](https://c4model.com/). Es un sistema de diagramas mucho más sencillo.

Este sería el **diagrama de contexto** de nuestro *leaderboard*:

![Leaderboard C4 Context Diagram](/images/2025/08/17-Context_diagram.png)

La magia de C4 es que se escribe como código, así que puedes guardar el diagrama como un simple archivo de texto (por ejemplo, en `docs/diagrams/c4/context_diagram.dsl`) y versionarlo junto con tu aplicación.

#### No te olvides de los Requisitos No Funcionales (NFRs)

Ya tenemos el "qué", pero ¿cómo debe comportarse el servicio? ¿Qué esperamos de su rendimiento, seguridad o disponibilidad? Estos son los [**requisitos no funcionales**](https://en.wikipedia.org/wiki/Non-functional_requirement).

No hace falta complicarse. Un simple documento (`docs/NFRs.md`) enlazado en el `README.md` es suficiente. Puedes apuntar ideas iniciales como:
* **Rendimiento**: "El sistema debe poder servir al menos una petición por segundo".
* **Backups**: "No se contempla una política de backups en la fase inicial".
* **Despliegue**: "Se desplegará usando un fichero `.jar` y scripts de shell".

Como se ve, no hay idea mala, lo importante es tener registrado lo que se hace. Es una brújula para guiar tus decisiones técnicas.

---

### Paso 2: Justificar el «porqué» con ADRs

Ahora que sabemos el "qué", toca el "cómo". Pero antes de decidir el "cómo", es crucial entender el **"porqué"**.

Una forma ligera de registrar estas decisiones son los [**Architecture Decision Records (ADRs)**](https://en.wikipedia.org/wiki/Architectural_decision). Son documentos breves que explican una decisión importante, las alternativas consideradas y las razones de la elección.

Por ejemplo:
* **¿Qué arquitectura usamos?** ¿Capas, Hexagonal, CQRS? Esto merece un ADR.
* **¿Cómo implementamos la API?** ¿gRPC, REST, GraphQL? Otro ADR.

En mi caso, para el *leaderboard*, empezaré con una **arquitectura hexagonal** (documentado en `docs/ADRs/ADR-001_Architecture.md`). Si en el futuro decido cambiar a CQRS, crearé un nuevo ADR explicando por qué.

Lo bueno es que el motivo no tiene por qué ser puramente técnico. Puedes escoger una tecnología simplemente por **curiosidad o para aprender**. Si luego no funciona, creas otro ADR explicando los problemas y el cambio de rumbo. Lo importante es que quede constancia.

---

### Paso 3: Detallar el «cómo» en el `CONTRIBUTING.md`

Ya tenemos el qué y el porqué. Solo nos falta explicar el **cómo**.

Si hemos elegido una arquitectura hexagonal, ¿cómo la vamos a organizar? ¿Qué estrategia de testing (BDD, TDD) seguiremos? Toda esta información técnica debe ir en un archivo `CONTRIBUTING.md`.

Este documento es la guía para cualquiera que quiera contribuir al proyecto. Podrías pensar que es excesivo para un proyecto personal, pero recuerda: **tu "yo" del futuro también es un contribuidor**. 😉 Además, nunca sabes quién querrá enviarte una PR.

---

### Resumen: Tu proyecto documentado y listo para crecer

Con estos tres pasos, tienes tu proyecto perfectamente definido:

* ✅ **El Qué**: `README.md` y diagramas de contexto de C4.
* ✅ **El Porqué**: Architecture Decision Records (ADRs).
* ✅ **El Cómo**: `CONTRIBUTING.md`.

Como ves, no hablamos de la documentación tradicional: documentos aburridos que nadie lee o diagramas que se quedan obsoletos. Este enfoque se parece más a la [**documentación como código**](https://en.wikipedia.org/wiki/Software_documentation): texto plano, control de versiones y herramientas ágiles. Es una documentación viva, útil y, sobre todo, mantenible.

Si te interesa, puedes ver el ejemplo completo de esta documentación en [**este repositorio de GitHub**]().

¡Gracias por leer!