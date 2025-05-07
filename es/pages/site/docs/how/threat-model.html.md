 Modelos de riesgo
en I2P Noviembre 2010
0.8.1 
low medium high ERR_INVALID 
 
 

- **Damage Potential**: **
- **Reliability**: **
- **Exploitability**: **
- **Affected Users**: **
- **Discoverability**: **
- **Severity**: */5*
- **Priority**: */9*

 

### Índices de ataques

- [Ataques de fuerza bruta](#bruteforce)
- [Ataques de sincronización](#timing)
- [Ataques por intersección](#intersection)
- [Ataques de denegación de servicio](#dos)
- [Ataques de etiquetado](#tagging)
- [Ataques de particionamiento](#partitioning)
- [Ataques del predecesor](#predecessor)
- [Ataques de cosechado](#harvesting)
- [Identificación a través de análisis del tráfico](#traffic)
- [Ataques Sybil](#sybil)
- [Ataques por agotamiento de amigos](#buddy)
- [Ataques de cifrados](#crypto)
- [Ataques Floodfill](#floodfill)
- [Otros ataques a la base de datos de la red](#netdb)
- [Ataques a recursos centralizados](#central)
- [Ataques de desarrollo](#dev)
- [Ataques de implementación](#impl)
- [Otras defensas](#blocklist)

 

## ¿Qué quiere decir con \"anónimo\"?

El nivel de anonimato se puede describir \"como la dificultad para
alguien de encontrar información sobre usted que no quiere que sea
encontrada\" - quien es usted, su localización, con quien se comunica, o
incluso cuándo se comunica. El anonimato \"perfecto\" no es aquí un
concepto útil - las aplicaciones no le harán indistinguible de las
personas que no utilizan ordenadores o no usan Internet. Aún así
intentamos proveer suficiente anonimato pera cumplir las verdaderas
necesidades de quien podemos - de aquellos simplemente navegando por
webs, o para aquellos que intercambian información, hasta aquellos con
miedo de ser descubiertos por organizaciones poderosas o estados.

La cuestión de si I2P provee suficiente anonimato para usted es una
pregunta difícil, pero esperemos que esta página le responda a esa
pregunta explorando como I2P opera ante varios atauqes y así puede
decidir si se amolda a sus necesidades.

Damos la bienvenida a más investigaciones y análisis sobre la
resistencia de I2P a las amenazas más abajo descritas. Se necesitan
revisiones sobre los textos ya existentes (la mayoría sobre Tor) y
trabajos originales sobre I2P.

## Sumario de la topología de la red

I2P builds off the ideas of many [other]()
[systems](), but a few key points should be kept
in mind when reviewing related literature:

- **I2P es una mixnet de rutas libres** - el creador del mensaje
 define explícitamente el camino que seguirán los mensajes enviados
 (el túnel de salida), y el receptor del mensaje define
 explícitamente el camino por el cual serán recibidos los mensajes
 (el túnel de entrada).
- **I2P no tiene puntos de entrada y salida oficiales** - todos los
 pares participan completamente en la mezcla, y no hay proxies de
 entrada o salida en la capa de red (aún así existen varios proxies
 de salida en la capa de aplicación)
- **I2P es totalmente distribuido** - no existen centros de control o
 autoridades. Cualquiera pude modificar algunos ruters para operar
 cascadas de mezcla (construyendo túneles y dando las claves
 necesarias para controlar el envío al final del túnel) o controlar
 los perfiles de los directorios, todo esto sin romper la
 compatibilidad con el resto de la red, pero por supuesto no es
 necesario hacer nada de esto (y además podría poner en peligro su
 anonimato).

We have documented plans to implement [nontrivial
delays](#stop) and [batching
strategies](#batching) whose existence is only
known to the particular hop or tunnel gateway that receives the message,
allowing a mostly low latency mixnet to provide cover traffic for higher
latency communication (e.g. email). However we are aware that
significant delays are required to provide meaningful protection, and
that implementation of such delays will be a significant challenge. It
is not clear at this time whether we will actually implement these delay
features.

En teoría, los ruters a lo largo del camino pueden inyectar un número
arbitrario de saltos antes de enviar el mensaje al siguiente par, pero
la implementación actual no lo hace.

## El modelo de amenazas

El diseño de I2P comenzó en 2003, no mucho tiempo después del llegada
del [\[Onion Routing\]](http://www.onion-router.net) (enrutamiento
cebolla), [\[Freenet\]](http://freenetproject.org/) (red libre), y
[\[Tor\]](https://www.torproject.org/). Nuestro diseño se beneficia
sustancialmente de las investigaciones publicadas en torno a esa época.
I2P usa varias técnicas de enrutamiento cebolla, así que continuamos
beneficiándonos del significativo interés académico en Tor.

Teniendo en cuenta los ataques y análisis en la [literatura sobre el
anonimato](http://freehaven.net/anonbib/topic.html) (en gran parte
[Traffic Analysis: Protocols, Attacks, Design Issues and Open
Problems](http://citeseer.ist.psu.edu/454354.html)), a continuación
describimos brevemente un gran variedad de ataques así como las defensas
en i2P. Actualizaremos esta lista según sean identificados nuevos
ataques.

Se incluyen algunos ataques que pueden ser solamente para I2P. No
tenemos soluciones perfectas para esos ataques, pero continuamos
estudiando como defendernos de ellos.

Además, muchos de esos ataques son significativamente más fáciles de lo
que deberían ser debido al pequeño tamaño actual de la red. Aunque somos
conscientes de algunas limitaciones que deben ser reparadas, I2P está
diseñado para soportar cientos de miles, o millones de pares. Según
vayamos difundiendo la palabra y la red crezca, esos ataques serán mucho
mas difíciles de llevar acabo.

The [network comparisons]() and [\"garlic\"
terminology]() pages may also be helpful
to review.

{# Hide DREAD ratings until we know how we want to use them

Attacks are judged using the [modified **DREAD**
model]():

- **Damage Potential**: If a threat exploit occurs, how much damage
 will be caused?
- **Reliability**: How reliable is the attack?
- **Exploitability**: What is needed to exploit this threat?
- **Affected Users**: How many users will be affected?
- **Discoverability**: How easy is it to discover this threat?

Each category is given a rating of low, medium or high. The severity and
priority scores are calculated using the equations outlined
[here]().

#}

### Ataques de fuerza bruta {#bruteforce}

{# DREAD_score(2, 1, 1, 1, 3) #}

Un ataque por fuerza bruta puede ser montado por adversarios pasivos o
activos, observando todos los mensajes que pasan entre todos los nodos e
intentarlo averiguar que mensaje sigue qué camino. Montar este ataque
sobre I2P no debería ser trivial, ya que todos los pares en la red
envían mensajes frecuentemente (de fin a fin y mensajes de mantenimiento
de la red), además un mensaje de fin a fin cambia su tamaño y datos a lo
largo de su camino. Además, un adversario externo tampoco tiene acceso
al mensaje, ya que la comunicación interna entre ruters está cifrada y
después enviada (haciendo que un mensaje de 1024 bytes sea
indistinguible de un mensaje de 2048 bytes)

Aún así, un atacante poderoso podría usar la fuerza bruta para detectar
tendencias - si puede enviar 5GB a una destinación I2P y monitorizar las
conexiones de red de todos, podría eliminar a todos los pares que no
recibieron los 5Gb de datos. Existen técnicas para evitar este ataque,
pero pueden ser prohibitivamente caras (vea
[Tarzan](http://citeseer.ist.psu.edu/freedman02tarzan.html)). A la
mayoría de los usuarios no les debería preocupar este ataque, ya que el
coste de montarlo es enorme (y normalmente ilegal). Aún así, el ataque
es plausible, por ejemplo, para un observador en un ISP o en un punto de
cambio de Internet. Los que deseen protegerse de este ataque deben tomar
las medidas necesarias, como poner límites bajos al ancho de banda, y
usar leasesets cifrados o no publicados para las eepsites. Otras
medidas, como retardos no triviales y rutas restringidas no se han
implementado.

As a partial defense against a single router or group of routers trying
to route all the network\'s traffic, routers contain limits as to how
many tunnels can be routed through a single peer. As the network grows,
these limits are subject to further adjustment. Other mechanisms for
peer rating, selection and avoidance are discussed on the [peer
selection page]().

### Ataques de sincronización {#timing}

{# DREAD_score(2, 2, 2, 3, 2) #}

Los mensajes de I2P son unidireccionales, y no implican necesariamente
que se enviará una respuesta. Aún así, las aplicaciones sobre I2P tienen
patrones reconocibles dentro de las frecuencias de sus mensajes - por
ejemplo, una petición HTTP tendrá un pequeño mensaje con una secuencia
larga de mensajes de respuesta conteniendo las respuestas HTTP.
Utilizando esta información y teniendo una vista general de la topología
de la red, un atacante podría inhabilitar algunos enlaces como mensajes
demasiado lentos como para ser pasados.

Este tipo de taques es poderoso, pero su aplicación a I2P no es obvia.
Debido a la variación de los retardos de los mensajes en las colas,
procesamiento de los mensajes y estrechamientos, a menudo excederán el
tiempo para pasar un mensaje a través de un enlace - incluso cuando un
atacante sabe que una respuesta será enviada tan pronto como el mensaje
llegue. Aunque hay varios escenarios en los cuales se exponen respuestas
casi automáticas - la librería de streaming lo hace (con el SYN+ACK) al
igual que que el modo de mensaje de la garantía del envío (con el
DataMessage+DeliveryStatusMessage).

Without protocol scrubbing or higher latency, global active adversaries
can gain substantial information. As such, people concerned with these
attacks could increase the latency (using [nontrivial
delays](#stop) or [batching
strategies](#batching)), include protocol
scrubbing, or other advanced tunnel routing
[techniques](#batching), but these are
unimplemented in I2P.

References: [Low-Resource Routing Attacks Against Anonymous
Systems]()

### Ataques por intersección {#intersection}

{# DREAD_score(3, 2, 2, 3, 3) #}

Los ataques de intersección contra los sistemas de baja latencia son
realmente poderosos - contactando con el objetivo periódicamente y
llevando el registro de los pares que hay en la red. Con el tiempo, y
con el movimiento, el atacante obtendrá bastante información sobre el
objetivo simplemente observando los pares que hay online cuando un
mensaje pasa a través. El costo de este ataque aumenta según aumenta el
tamaño de la red, pero puede ser válido en varios escenarios.

In summary, if an attacker is at both ends of your tunnel at the same
time, he may be successful. I2P does not have a full defense to this for
low latency communication. This is an inherent weakness of low-latency
onion routing. Tor provides a [similar
disclaimer]().

Defensa parcialmente implementada en I2P:

- [strict ordering](#ordering) of peers
- [peer profiling and selection]() from
 a small group that changes slowly
- Límite en el número de túneles rutados a través de un solo par
- Prevención de pares del mismo rango /16 de IPs por ser miembros del
 mismo único túnel.
- For I2P Sites or other hosted services, we support simultaneous
 hosting on multiple routers, or [multihoming](#intersection)

Incluso usando todas ellas, estas defensas no son una solución completa.
Además, hemos hecho algunas elecciones de diseño que podrían incrementar
las vulnerabilidades:

- No utilizamos \"nodos guardianes\" de bajo ancho de banda
- Usamos grupos de túneles compuestos de varios túneles, y el tráfico
 puede pasar de túnel a túnel.
- Los túneles no son de larga duración; los túneles se recrean cada 10
 minutos.
- El tamaño de los túneles es configurable. Aunque se recomienda 3
 saltos por túnel para protección total, algunas aplicaciones y
 servicios usan túneles de 2 saltos por defecto.

In the future, it could for peers who can afford significant delays (per
[nontrivial delays](#stop) and [batching
strategies](#batching)). In addition, this is only
relevant for destinations that other people know about - a private group
whose destination is only known to trusted peers does not have to worry,
as an adversary can\'t \"ping\" them to mount the attack.

Reference: [One Cell Enough]()

### Ataques de denegación de servicio {#dos}

Hay un montón de ataques de denegación de servicio disponibles contra
I2P, cada cual con sus costes y consecuencias:

{# DREAD_score(1, 1, 2, 1, 3) #}

**Ataque del usuario codicioso:** Esto es simplemente gente intentando
consumir muchas más recursos de los que están dispuestos a compartir. La
defensa contra este ataque es:

- Set defaults so that most users provide resources to the network. In
 I2P, users route traffic by default. In sharp distinction to [other
 networks](), over 95% of I2P users
 relay traffic for others.
- Proporcionar opciones de configuración fáciles para que los usuarios
 puedan incrementar su contribución (porcentaje de lo que se
 comparte) a la red. Mostrar medidas fáciles de entender como \"el
 ratio de lo que se comparte\" para que los usuarios puedan ver lo
 que contribbuyen.
- Manteniendo una comunidad fuerte con blogs, foros, IRC y otras
 formas de comunicación.

::: {style="clear:both"}
:::

{# DREAD_score(2, 1, 1, 2, 3) #}

**Starvation attack:** A hostile user may attempt to harm the network by
creating a significant number of peers in the network who are not
identified as being under control of the same entity (as with Sybil).
These nodes then decide not to provide any resources to the network,
causing existing peers to search through a larger network database or
request more tunnels than should be necessary. Alternatively, the nodes
may provide intermittent service by periodically dropping selected
traffic, or refusing connections to certain peers. This behavior may be
indistinguishable from that of a heavily-loaded or failing node. I2P
addresses these issues by maintaining
[profiles]() on the peers, attempting to
identify underperforming ones and simply ignoring them, or using them
rarely. We have significantly enhanced the ability to recognize and
avoid troublesome peers; however there are still significant efforts
required in this area.

::: {style="clear:both"}
:::

{# DREAD_score(1, 2, 2, 2, 3) #}

**Flooding attack:** A hostile user may attempt to flood the network, a
peer, a destination, or a tunnel. Network and peer flooding is possible,
and I2P does nothing to prevent standard IP layer flooding. The flooding
of a destination with messages by sending a large number to the
target\'s various inbound tunnel gateways is possible, but the
destination will know this both by the contents of the message and
because the tunnel\'s tests will fail. The same goes for flooding just a
single tunnel. I2P has no defenses for a network flooding attack. For a
destination and tunnel flooding attack, the target identifies which
tunnels are unresponsive and builds new ones. New code could also be
written to add even more tunnels if the client wishes to handle the
larger load. If, on the other hand, the load is more than the client can
deal with, they can instruct the tunnels to throttle the number of
messages or bytes they should pass on (once the [advanced tunnel
operation](#batching) is implemented).

::: {style="clear:both"}
:::

{# DREAD_score(1, 1, 1, 1, 1) #}

**Ataque de carga de CPU:** Hay algunos métodos que pueden hacer que
algún usuario remoto solicite que un par haga operaciones de cifrados
muy costosas, y un usuario hostil puede usar esto para saturar el par
con un gran número de solicitudes e intentar saturar la CPU. Usando
buenas prácticas de ingeniería y exigiendo certificados no triviales
(por ejemplo HashCash) puede mitigarse el problema, aunque hay
posibilidad también de que un atacante explote algún error en la
implementación.

::: {style="clear:both"}
:::

{# DREAD_score(2, 2, 3, 2, 3) #}

**Floodfill DOS attack:** A hostile user may attempt to harm the network
by becoming a floodfill router. The current defenses against unreliable,
intermittent, or malicious floodfill routers are poor. A floodfill
router may provide bad or no response to lookups, and it may also
interfere with inter-floodfill communication. Some defenses and [peer
profiling]() are implemented, however
there is much more to do. For more information see the [network database
page](#threat).

::: {style="clear:both"}
:::

### Ataques de etiquetado {#tagging}

{# DREAD_score(1, 3, 1, 1, 1) #}

Tagging attacks - modifying a message so that it can later be identified
further along the path - are by themselves impossible in I2P, as
messages passed through tunnels are signed. However, if an attacker is
the inbound tunnel gateway as well as a participant further along in
that tunnel, with collusion they can identify the fact that they are in
the same tunnel (and prior to adding [unique hop
ids](#tunnelId) and other updates, colluding peers
within the same tunnel can recognize that fact without any effort). An
attacker in an outbound tunnel and any part of an inbound tunnel cannot
collude however, as the tunnel encryption pads and modifies the data
separately for the inbound and outbound tunnels. External attackers
cannot do anything, as the links are encrypted and messages signed.

### Ataques de particionamiento {#partitioning}

{# DREAD_score(3, 1, 1, 1, 2) #}

Los ataques de particionamiento - buscar formas (técnica o
analíticamente) de separar los pares en la red - son a tener en cuenta
cuando nos enfrentamos a adversarios poderosos, ya que el tamaño de la
red juega un papel importante a la hora de determinar el anonimato. I2P
ha resuelto el problema técnico del ataque de particionamiento que corta
los enlaces entre los pares dentro de su base de datos de la red, la
cual mantiene estadísticas sobre los pares a fin de permitir que las
conexiones fragmentadas sean reparadas usando otras partes de la red.
Aunque si un atacante desconecta todos los enlaces de un par, aislando
el objetivo completamente, la base de datos poco podrá hacer para
reparar el daño. En este punto lo único que el router I2P puede intentar
hacer es avisar de que un gran número de pares anteriormente fiables han
pasado a estar no disponibles, y alertar al cliente de que está
temporalmente desconectado (este tipo de detección no está aún
implementada).

Partitioning the network analytically by looking for differences in how
routers and destinations behave and grouping them accordingly is also a
very powerful attack. For instance, an attacker
[harvesting](#harvesting) the network database will know when a
particular destination has 5 inbound tunnels in their LeaseSet while
others have only 2 or 3, allowing the adversary to potentially partition
clients by the number of tunnels selected. Another partition is possible
when dealing with the [nontrivial delays](#stop)
and [batching strategies](#batching), as the
tunnel gateways and the particular hops with non-zero delays will likely
stand out. However, this data is only exposed to those specific hops, so
to partition effectively on that matter, the attacker would need to
control a significant portion of the network (and still that would only
be a probabilistic partition, as they wouldn\'t know which other tunnels
or messages have those delays).

Also discussed on the [network database
page](#threat) (bootstrap attack).

### Ataques del predecesor {#predecessor}

{# DREAD_score(1, 1, 1, 1, 3) #}

El ataque del predecesor es obtener estadísticas pasivamente intentando
ver qué pares están \'cerca\' de la destinación, participando en sus
túneles y haciendo el seguimiento de los saltos anteriores o siguientes
( para túneles de salida o entrada, respectivamente). Con el tiempo, un
atacante usando un ejemplo aleatorio perfecto de pares y ordenación,
podría ver cuales pares parecen estar más \'cerca\' estadísticamente que
el resto, y ese par podría llegar a estar donde el el objetivo se
encuentra.

I2P avoids this in four ways: first, the peers selected to participate
in tunnels are not randomly sampled throughout the network - they are
derived from the [peer selection]()
algorithm which breaks them into tiers. Second, with [strict
ordering](#ordering) of peers in a tunnel,
the fact that a peer shows up more frequently does not mean they\'re the
source. Third, with [permuted tunnel
length](#length) (not enabled by default)
even 0 hop tunnels can provide plausible deniability as the occasional
variation of the gateway will look like normal tunnels. Fourth, with
[restricted routes](#fullRestrictedRoutes)
(unimplemented), only the peer with a restricted connection to the
target will ever contact the target, while attackers will merely run
into that gateway.

The current [tunnel build method]() was
specifically designed to combat the predecessor attack. See also [the
intersection attack](#intersection).

References: []() which is an
update to the 2004 predecessor attack paper []().

### Ataques de cosechado {#harvesting}

{# DREAD_score(1, 1, 2, 2, 3) #}

\"Harversting\", cosechado, es la compilación de una lista de usuarios
que ejecutan I2P. Puede ser usado para atacar legalmente o para ayudar a
otros ataques simplemente ejecutando un par, viendo quien se conecta al
par, y cosechando todas las referencias que pueda encontrar sobre otros
pares.

En sí mismo I2P no está diseñado para defenderse efectivamente contra
este ataque, ya que la base de datos de la red distribuida contiene toda
esta información. Aunque los siguientes factores hacen este ataque sea
un poco más difícil en la práctica:

- El crecimiento de la red hará más difícil el controlar una parte
 determinada de la red.
- Los ruters floodfill implementan límites en las peticiones para
 prevenir ataques de denegación de servicio, DOS.
- \"Modo oculto\", evita que el ruter publique su información en la
 netDb, (pero también hace que no reenvíe datos), no se usa mucho por
 ahora.

In future implementations, [basic](#nat) and
[comprehensive](#fullRestrictedRoutes) restricted
routes, this attack loses much of its power, as the \"hidden\" peers do
not publish their contact addresses in the network database - only the
tunnels through which they can be reached (as well as their public keys,
etc).

En el futuro los ruters podrán usar GeoIP para identificar si están en
un país donde la identificación de su nodo como un nodo de I2P podría
ser peligroso. En ese caso, el ruter podrá activar el modo oculto
automáticamente, o utilizar otros métodos de enrutado restringidos.

### Identificación a través de análisis del tráfico {#traffic}

{# DREAD_score(1, 1, 2, 3, 3) #}

By inspecting the traffic into and out of a router, a malicious ISP or
state-level firewall could identify that a computer is running I2P. As
discussed [above](#harvesting), I2P is not specifically designed to hide
that a computer is running I2P. However, several design decisions made
in the design of the [transport layer and
protocols]() make it somewhat difficult to
identify I2P traffic:

- Selección de puertos aleatoria
- Cifrado de todo el tráfico de punto a punto
- Intercambio de clave DH sin bytes del protocolo u otros campos
 constantes no cifrados
- Simultaneous use of both [TCP]() and
 [UDP]() transports. UDP may be much harder for
 some Deep Packet Inspection (DPI) equipment to track.

En breves tenemos planeado solucionar los problemas de análisis de
trafico ofuscando los protocolos de transporte de I2P, probablemente
incluyendo:

- Rellenando la capa de transporte para que tenga determinados
 tamaños, especialmente durante el handshake de conexión
- Estudiando las firmas de la distribución de los tamaños de los
 paquetes, y rellenando si es necesario.
- Creación de otros métodos de transporte camuflados como SSL u otros
 protocolos comunes.
- Revisión de las estrategias de relleno en las capas superiores para
 ver como afectan al tamaño de los paquetes en la capa de transporte.
- Revisar varios métodos implementados por varios cortafuegos de
 algunos estados para bloquear Tor
- Trabajar directamente con expertos en DPI, inspección profunda de
 paquetes, y expertos en ofuscación.

Reference: [Breaking and Improving Protocol
Obfuscation]()

### Ataques Sybil {#sybil}

{# DREAD_score(3, 2, 1, 3, 3) #}

Sybil describe una categoría de ataques donde el adversario crea números
arbitrariamente grandes de nodos compinchados y usan el incremento
numérico para ayudar a montar otros ataques. Por ejemplo, si un atacante
esta en una red donde los pares se seleccionan aleatoriamente y quieren
un 80% de posibilidades de ser uno de esos pares, simplemente crean
cinco veces el número de nodos que están en la red y tiran el dado.
Cuando la identidad es gratuita, Sybil puede ser una técnica muy potente
para un adversario enérgico. La técnica primaria para enfrentar esto es
simplemente hacer la identidad \'no gratuita\' -
[Tarzan](http://www.pdos.lcs.mit.edu/tarzan/) (entre otros) usa el hecho
de que la dirección IP es limitada, mientras IIP (proyecto de IRC
invisible) usaba [HashCash](http://www.hashcash.org/) para realizar un
\'cargo\' por crear una nueva identidad (prueba de trabajo). Actualmente
no hemos implementado técnica particular alguna para enfrentar Sybil,
pero incluimos certificados de posición en las estructuras de datos del
router y el destino que pueden contener un certificado HashCash de un
valor adecuado cuando sea necesario (o algún otro certificado que pruebe
la escasez).

Requerir certificados HashCash en varios sitios tiene algunos problemas:

- Mantener compatibilidad con versiones anteriores
- El problema clásico del HashCash - seleccionar valores HashCash que
 sean pruebas significativas de gasto de trabajo en máquinas
 potentes, mientras que también sean factibles en máquinas no tan
 potentes como los dispositivos móviles.

Varios límites en el número de ruters que puede haber en un rango
determinado de IPs restringe las posibilidades de los atacantes, ya que
no pueden poner más computadoras en ese bloque de IPs. Aún así esto no
es defensa contra un adversario con muchos recursos.

See the [network database page](#threat) for more
Sybil discussion.

### Ataques por agotamiento de amigos {#buddy}

{# DREAD_score(3, 2, 2, 1, 3) #}

(Reference: [In Search of an Anonymous and Secure
Lookup]() Section 5.2)

By refusing to accept or forward tunnel build requests, except to a
colluding peer, a router could ensure that a tunnel is formed wholly
from its set of colluding routers. The chances of success are enhanced
if there is a large number of colluding routers, i.e. a [Sybil
attack](#sybil). This is somewhat mitigated by our [peer
profiling]() methods used to monitor the
performance of peers. However, this is a powerful attack as the number
of routers approaches *f* = 0.2, or 20% malicious nodes, as specifed in
the paper. The malicous routers could also maintain connections to the
target router and provide excellent forwarding bandwidth for traffic
over those connections, in an attempt to manipulate the profiles managed
by the target and appear attractive. Further research and defenses may
be necessary.

### Ataques de cifrados {#crypto}

{# DREAD_score(3, 2, 1, 3, 1) #}

We use strong cryptography with long keys, and we assume the security of
the industry-standard cryptographic primitives used in I2P, as
documented [on the low-level cryptography
page](). Security features include the
immediate detection of altered messages along the path, the inability to
decrypt messages not addressed to you, and defense against
man-in-the-middle attacks. The key sizes chosen in 2003 were quite
conservative at the time, and are still longer than those used in [other
anonymity networks](https://torproject.org/). We don\'t think the
current key lengths are our biggest weakness, especially for
traditional, non-state-level adversaries; bugs and the small size of the
network are much more worrisome. Of course, all cryptographic algorithms
eventually become obsolete due to the advent of faster processors,
cryptographic research, and advancements in methods such as rainbow
tables, clusters of video game hardware, etc. Unfortunately, I2P was not
designed with easy mechanisms to lengthen keys or change shared secret
values while maintaining backward compatibility.

Upgrading the various data structures and protocols to support longer
keys will have to be tackled eventually, and this will be a [major
undertaking](), just as it will be for
[others](https://torproject.org/). Hopefully, through careful planning,
we can minimize the disruption, and implement mechanisms to make it
easier for future transitions.

En el futuro varios protocolos y estructuras de datos de I2P soportarán
el rellenado seguro de mensajes con tamaños arbitrarios, con lo que los
mensajes serán de un tamaño constante o los mensajes garlic podrán ser
modificados aleatoriamente con lo cual algunas partes parecerán contener
más subpartes de lo que realmente tienen. Hasta el momento los túneles
garlic y los mensajes de fin a fin utilizan un simple relleno aleatorio.

### Ataques de anonimato FloodFill {#floodfill}

{# DREAD_score(3, 2, 1, 2, 2) #}

In addition to the floodfill DOS attacks described [above](#ffdos),
floodfill routers are uniquely positioned to learn about network
participants, due to their role in the netDb, and the high frequency of
communication with those participants. This is somewhat mitigated
because floodfill routers only manage a portion of the total keyspace,
and the keyspace rotates daily, as explained on the [network database
page](#threat). The specific mechanisms by which
routers communicate with floodfills have been [carefully
designed](#delivery). However, these threats
should be studied further. The specific potential threats and
corresponding defenses are a topic for future research.

### Otros ataques a la base de datos de la red {#netdb}

A hostile user may attempt to harm the network by creating one or more
floodfill routers and crafting them to offer bad, slow, or no responses.
Several scenarios are discussed on the [network database
page](#threat).

### Ataque de Recurso Central {#central}

{# DREAD_score(1, 1, 1, 3, 3) #}

Hay varios recursos centralizados o limitados (algunos dentro de I2P,
algunos no) que pueden ser atacados o usados como vectores para ataques.
La desaparición de jrandom en Noviembre del 2007, seguida de la pérdida
del servicio de alojamiento de i2p.net en enero del 2008, mostraron que
muchos servicios estaban centralizados en el desarrollo y funcionamiento
de la red I2P, aunque actualmente la mayoría están descentralizados. Los
ataques a los servicios externos afectan mayormente a cómo los nuevos
usuarios pueden encontrarnos, no en la operación de la red en sí misma.

- The [website]() is mirrored and uses DNS
 round-robin for external public access.
- Routers now support [multiple external reseed
 locations](#reseed), however more reseed hosts
 may be needed, and the handling of unreliable or malicious reseed
 hosts may need improvement.
- Los ruters soportan ahora la actualización desde múltiples
 localizaciones. Un ruter malicioso de actualizaciones podría enviar
 un archivo enorme, se necesita limitar el tamaño.
- Los ruters ahora soportan múltiples actualizaciones de confianza
 firmadas.
- Los routers I2P ahora gestionan mejor [múltiples pares de inundación
 (floodfills) no fiables](#ffdos). Los routers I2P de inundación
 maliciosos [precisan](#ffdos) [mayor](#floodfill) estudio.
- The code is now stored in a [distributed source control
 system]().
- Los routers I2P confían en un solo servidor de novedades de consola,
 pero hay una URL de respaldo incluida en el código, apuntando a un
 servidor distinto. Un servidor de novedades de consola malicioso
 podría enviar un fichero enorme, es necesario limitar el tamaño.
- [Naming system services](), including
 address book subscription providers, add-host services, and jump
 services, could be malicious. Substantial protections for
 subscriptions were implemented in release 0.6.1.31, with additional
 enhancements in subsequent releases. However, all naming services
 require some measure of trust, see [the naming
 page]() for details.
- Continuamos confiando en el servicio DNS para i2p2.de, perder esto
 causaría bastante trastorno en nuestra capacidad de atraer nuevos
 usuarios, y encogería la red (de corto a medio plazo), al igual que
 lo hizo la pérdida de i2p.net.

### Ataques de desarrollo {#dev}

{# DREAD_score(2, 1, 1, 3, 1) #}

Estos ataques no son a la red, en cambio van detrás del equipo de
desarrolladores ya sea poniendo obstáculos legales a cualquiera
contribuyendo al desarrollo, o usando cualquier método disponible para
hacer que los desarrolladores boicoteen el software. Las medidas
técnicas tradicionales no pueden derrotare estos ataques, y si alguien
amenaza la vida o el sustento de un desarrollador (simplemente poniendo
una denuncia con secreto de sumario para que no pueda contarlo, con
amenaza de cárcel), podríamos tener un gran problema.

Sin embargo, estas técnicas ayudan a defenderse contra estos ataques:

- All components of the network must be open source to enable
 inspection, verification, modification, and improvement. If a
 developer is compromised, once it is noticed the community should
 demand explanation and cease to accept that developer\'s work. All
 checkins to our [distributed source control
 system]() are cryptographically signed,
 and the release packagers use a trust-list system to restrict
 modifications to those previously approved.
- Development over the network itself, allowing developers to stay
 anonymous but still secure the development process. All I2P
 development can occur through I2P - using a [distributed source
 control system](), a distributed source
 control system, IRC chat, public web servers, discussion forums
 (forum.i2p), and the software distribution sites, all available
 within I2P.

También mantenemos relaciones con organizaciones que ofrecen consejo
legal, en caso de que fuese necesario algún tipo de defensa legal.

### Ataques de implementación (errores de programación) {#impl}

{# DREAD_score(2, 2, 1, 3, 1) #}

Por mucho que nos esforcemos, incluso las aplicaciones más simples
tienen errores de diseño, e I2P no es una excepción. Pueden existir bugs
inesperados que pudieran ser explotados para atacar el anonimato o la
seguridad de las comunicaciones ejecutándose sobre I2P. Para evitar
estos ataques contra el diseño de los protocolos usados, publicamos
todos los diseños y documentación y solicitamos revisión y crítica con
la esperanza de que usando muchos ojos se mejorará el sistema. No
creemos en [la seguridad por
oscuridad](http://www.haystacknetwork.com/).

Además, el código es tratado de la misma forma, sin muchos problemas
para volver a hacer el trabajo o tirar trabajo ya hecho que no cumpla
las necesidades del sistema (incluida su fácil modificación). La
documentación del diseño y de la implementación de la red y de los
componentes de software es una parte esencial de la seguridad, ya que
sin ella sería raro que los programadores gastasen tanto tiempo en
aprenderse el software como para identificar deficiencias y errores.

En partucular, es probable que nuestras aplicaciones contengan errores
relacionados con la denegación de servicio a través de errores de
llenado de memoria (OOMS), cross-site-scripting (XSS) en la consola del
ruter, y otras vulnerabilidades no tan normales a causa de varios
protocolos.

I2P is still a small network with a small development community and
almost no interest from academic or research groups. Therefore we lack
the analysis that [other anonymity networks](https://torproject.org/)
may have received. We continue to recruit people to [get
involved]() and help.

## Otras defensas

### Listas de bloqueos {#blocklist}

Hasta cierto punto I2P puede ser afinada para evitar a los pares que
operan con direcciones IP incluidas en una lista de bloqueo (blocklist).
Comúnmente están disponibles varias listas de bloqueo en formatos
estándar, e incluyen organizaciones contrarias a I2P, adversarios de un
nivel potencialmente estatal, y otros.

En la medida en que aparecen pares activos en la lista de bloqueo
actual, bloquear sólo una parte de los pares tendería a segmentar la
red, exacerbando los problemas de alcanzabilidad, y reduciendo la
fiabilidad del conjunto. Por tanto querríamos ponernos de acuerdo en una
lista de bloqueo determinada, y habilitarla por defecto.

Las listas de bloqueo (blocklist) sólo son una parte (quizáa una pequeña
parte) de una batería de defensas contra la maliciosidad. En gran parte,
el sistema de elaboración de perfiles hace un buen trabajo de medición
del comportamiento de los routers I2P, y hace que no necesitemos confiar
en ningún contenido de la netDb. Aún así hay más cosas que se pueden
hacer. En cualquiera de las áreas de la lista anterior hay mejoras que
se pueden realizar para detectar la maliciosidad.

Si una lista de bloqueo (blocklist) está hospedada en una ubicación
central con actualizaciones automáticas, la red es vulnerable a un
[ataque al recurso centralizado](#central). La suscripción automática a
una lista ofrece al proveedor de esta la capacidad de apagar toda la red
i2p. Por completo.

Actualmente, con nuestro software se distribuye una lista de bloqueo
(blocklist) predeterminada, que incluye sólo las IPs que han sido origen
de ataques de denegación de servicio (DOS). No hay mecanismo de
actualización automático. En caso de que un rango de IPs determinado
implementase ataques graves a la red I2P, tendríamos que pedirle a la
gente que actualizase manualmente su lista de bloqueo a través de
mecanismos externos a la red como foros, blogs, etc.


