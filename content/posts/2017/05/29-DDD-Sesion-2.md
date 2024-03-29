---
title: Domain Driven Design, Sesión 2
date: 2017-05-29
tags:
  - SVQJUG
  - Java
  - DDD
---

Ayer tuvimos la segunda sesión de DDD en las oficinas de [Comalis](https://www.comalis.com/). Personalmente se me hizo bastante corto ya que tuvimos bastante debate y muy interesante. Yo aprendí muchísimo… pero por otra parte salí con nuevas lagunas.
Empezamos con una pequeña introducción por parte de Tamara de [Comalis](https://www.comalis.com/) sobre la empresa. Se dedican fundamentalmente al hosting, cloud, antispam, ssl, etc. Son franceses (el CPD esta en Lyon) pero tienen las oficinas aquí, en Sevilla. Tienen programa de afiliados, así que si os interesa os podéis poner en contacto con ellos que son muy agradables, nos tenían preparado hasta café y pastitas.
En lo técnico, repasamos el origen de DDD, la importancia de la reducción de la carga cognitiva al dividir el problema en varios contextos y no tener que mantenerlos todos a la vez en la cabeza. Esto puede implicar que tengamos datos duplicados entre contextos, pero de lo que se trata no es de optimizar en lo técnico, sino de desarrollar un software de calidad, flexible y adaptable.
También pasamos por encima del lenguaje ubicuo, que es el lenguaje que utilizamos para definir y describir el sistema. Debe estar lo más próximo posible al lenguaje del negocio para malentendidos o directamente definir mal el sistema.
Una vez expuesta la parte más abstracta, pasamos al caso concreto: la gestión de un gimnasio. Dentro de un gimnasio podemos tener distintos contextos: facturación, mantenimiento, gestión de personal o el técnico como tal. Este técnico puedo incluir definir rutinas para los clientes y que estos puedan ir apuntando las actividades que van realizando en el gimnasio. El caso de estudio se centraba en esta última parte, en concreto propuse dos historias de usuario:

* Como usuario, deseo poder tener rutinas asignadas para consultar en cualquier momento que actividad tengo que realizar a continuación.
* Como usuario, deseo poder ir registrando diariamente las actividades que voy realizando en el gimnasio esten o no dentro de una de mis rutinas.

![Entidades y Objetos de Valor](https://drive.google.com/uc?export=view&id=0BymoUnvpt9LxVUNHV1lSMlFuZ0E)

Empezando por el final, este fue el resultado de nuestro sesudo análisis (si que dibujamos, bien, sí… y mi Rs por lo visto parecen Zs).
En el camino tuvimos que aclarar que es una Entidad (algo que tiene identidad dentro del sistema), que es un Objeto Valor (algo que NO tiene identidad) y definir si los distintos componentes de nuestro esquema eran objetos de valor o entidades. Como cosas a destacar, pues en primer lugar que no hay una solución correcta, sino que el proceso es iterativo, se va refinando en cada iteración. Por ejemplo, originalmente pensamos que **Cliente** era un objeto valor, pero más tarde vimos claro que era una entidad.
Un punto de vista muy interesante que propuso Isra fue que muchas veces las entidades se ven desde fuera del sistema con más claridad que desde dentro del mismo. También me quedo con lo que comentó Ignacio de si vamos a *“pensar a futuro”* sobre el componente, es decir, si vamos a permitir que cambie de estado en un futuro (como puede ser un **Día** en el esquema, ya que podemos añadirle actividades en cualquier momento). También es importante considerar que este esquema representa nuestro dominio y NO se refiere en ningún momento al modelo de datos (sea cual sea).
Por último, estuvimos introduciendo el concepto de agregado y raíz del agregado, en este caso **Cliente** sería la raíz del agregado y controlaría el acceso a todo lo que se relaciona con él, como los días o las rutinas y sobre todo, mantendria la coherencia de los distintos componentes del agregado, por ejemplo, que no haya rutinas sin actividades.
Todo ésto lo acompañamos con un pequeño esbozo en forma de clases de lo que hay en la pizarra y que esta en [GitHub](https://github.com/agustinventura/ddd-svqjug)
Esto fue todo, ya que al final las dos horas se hicieron cortas. Yo salí contento y no me importaría seguir desarrollando ese primer código que tenemos en siguientes sesiones si hay interés en continuar. Y el que quiera reengancharse, bienvenido es :)

Os dejo aquí los recursos que he repasado para la sesión por si queréis echarles un vistazo:

* [Domain-Driven Design: Tackling Complexity in the Heart of Software](https://www.amazon.es/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)
* [Patterns, principles and practices of Domain-Driven Design](https://www.amazon.es/Patterns-Principles-Practices-Domain-Driven-Design/dp/1118714709)
* [DDD Quickly](https://www.infoq.com/minibooks/domain-driven-design-quickly)
* [DDD & Rest](https://www.youtube.com/watch?v=1OgvUIsv96o)
* [Whoops, where did my architecture go?](https://www.youtube.com/watch?v=v1XIcgFUIEw)

