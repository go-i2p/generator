 Garlic Routing,
enrutado Garlic Marzo de 2014. 0.9.12 

## Garlic Routing y terminología \"Garlic\"

Los términos \"garlic routing, enrutado garlic\" y \"garlic encryption,
cifrado garlic\"son usados a menudo imprecisamente para designar la
tecnología de I2P. Aquí vamos a explicar la historia de estos términos,
su significados,y el uso de los métodos \"garlic\" en I2P.

\"Garlic Routing\" fue acuñado por [Michael J.
Freedman](http://www.cs.princeton.edu/~mfreed/) en la [Master\'s
thesis](http://www.freehaven.net/papers.html) de Roger Dingledine en
Free Haven. Sección 8.1.1 (Junio 2000), derivado de [Onion
Routing](http://www.onion-router.net/).

\"Garlic\" fue quizás usado por los desarrolladores originales de I2P
porque implementa un forma de agrupación tal y como Freedman describió,
o simplemente para enfatizar las diferencias con Tor. La razón exacta
puede haberse perdido en el tiempo. Generalmente, cuando nos referimos
al término \"garlic\", puede significar una de estas tres cosas:

1. Cifrado por capas
2. Agrupa varios mensajes juntos
3. Cifrado ElGamal/AES

Desafortunadamente, el uso del término \"garlic\" por parte de I2P en
los pasados siete años no ha sido siempre preciso; por lo tanto los
usuarios están avisados para cuando se topen con el término. Esperemos
que la siguiente explicación dejará las cosas más claras.

### Cifrado por capas

El enrutado Onion es una técnica para construir caminos, o túneles, a
través de una serie de pares, y después usar ese túnel. Los mensajes son
repetidamente cifrados por el creador, y después descifrados por cada
salto. Durante la fase de construcción sólo las instrucciones de
enrutado para el siguiente salto son expuestas a cada par. Durante la
fase de operación los mensajes se pasan a través del túnel, y el mensaje
y sus instrucciones de enrutado sólo son mostradas en el punto final del
túnel.

This is similar to the way Mixmaster (see [network
comparisons]()) sends messages - taking a
message, encrypting it to the recipient\'s public key, taking that
encrypted message and encrypting it (along with instructions specifying
the next hop), and then taking that resulting encrypted message and so
on, until it has one layer of encryption per hop along the path.

En este senido, \"garlic routing\" como concepto general es idéntico a
\"onion routing\". Aunque tal y como se ha implementado en I2P tiene
varias diferencias con la implementación de Tor; ver más abajo. Aun así,
hay similitudes substanciales, como algunas de las que se beneficia I2P
gracias [al gran número de estudios académicos sobre la onion
routing](http://www.onion-router.net/Publications.html), [Tor, y mixnets
similares](http://freehaven.net/anonbib/topic.html).

### Construyendo múltiples mensajes

Michael Freedman definión \"garlic routing\" como una extensión de onion
routing, en la cual varios mensajes son agrupados juntos. El llamó a
cada mensaje \"bulb, bulbo\". Todos los mensajes, cada uno con sus
instrucciones de envío, son expuestos en el punto final. Esto permite
una agrupación eficiente del \"bloque de respuesta\" de una una ruta
onion con el mensaje original.

Este concepto ha sido implementado en I2p como se describe más abajo.
Nuestro término para \"bulbs, bulbos\" garlic es \"cloves, dientes del
ajo\". Puede contener cualquier número de mensajes, en vez de un solo
mensaje. Esta es una gran diferencia con la implementación de Tor. Aun
así, es sólo una de las diferencias entre I2P y Tor; quizás por si misma
no sea suficiente para justificar un cambio de terminología.

Otra diferencia con el método descrito por Freedman es que el camino es
unidireccional - no existe un \"punto de retorno\" como en el enrutado
onion o en los bloques de respuesta mixmaster, lo que simplifica mucho
el algoritmo y permite una entrega fiable.

### Cifrado ElGamal/AES

In some cases, \"garlic encryption\" may simply mean
[ElGamal/AES+SessionTag]() encryption
(without multiple layers).

## Métodos \"Garlic\" en I2P

Ahora que hemos definido varios términos \"garlic\", podemos decir que
I2P usa rutado garlic, agrupación y cifrado en tres partes:

1. Para la construcción y enrutado a través de los túneles (cifrado por
 capas)
2. Para determinar el éxito o fallo del envío de un mensaje de fin a
 fin (agrupamiento)
3. Para publicar algunas entradas en la base de datos de la red
 (amortiguando la posibilidad de un ataque de análisis exitoso)
 (ElGamal/AES)

Hay muchas otras formas de usar esta técnica para mejorar el rendimiento
de la red, aprovechando las compensaciones de la latencia del
transporte, y derivando datos a través de caminos redundantes para
incrementar la fiabilidad.

### Rutado y construcción de los túneles

En I2P los túneles son unidireccionales. Cada parte construye dos
túneles, uno para el tráfico de salida y otro para el de entrada. Por lo
tanto se necesitan cuatro túneles para una vuelta completa de un mensaje
y su respuesta.

Tunnels are built, and then used, with layered encryption. This is
described on the [tunnel implementation
page](). Tunnel building details are defined
on [this page](). We use
[ElGamal/AES+SessionTag]() for the
encryption.

Tunnels are a general-purpose mechanism to transport all [I2NP
messages](), and [Garlic
Messages](#msg_Garlic) are not used to build
tunnels. We do not bundle multiple [I2NP
messages]() into a single [Garlic
Message](#msg_Garlic) for unwrapping at the
outbound tunnel endpoint; the tunnel encryption is sufficient.

### Agrupación de mensajes de fin a fin.

At the layer above tunnels, I2P delivers end-to-end messages between
[Destinations](#struct_Destination).
Just as within a single tunnel, we use
[ElGamal/AES+SessionTag]() for the
encryption. Each client message as delivered to the router through the
[I2CP interface]() becomes a single [Garlic
Clove](#struct_GarlicClove) with its own
[Delivery
Instructions](#struct_GarlicCloveDeliveryInstructions),
inside a [Garlic Message](#msg_Garlic).
Delivery Instructions may specify a Destination, Router, or Tunnel.

Generalmente, un mensaje Garlic sólo contiene un clove. Aun así, el
ruter agrupa periódicamente dos dientes adicionales en el mensaje
Garlic:

![Garlic Message
Cloves](/_static/images/garliccloves.png "Garlic Message Cloves"){style="text-align:center;"}

1. A [Delivery Status
 Message](#msg_DeliveryStatus), with
 [Delivery
 Instructions](#struct_GarlicCloveDeliveryInstructions)
 specifying that it be sent back to the originating router as an
 acknowledgment. This is similar to the \"reply block\" or \"reply
 onion\" described in the references. It is used for determining the
 success or failure of end to end message delivery. The originating
 router may, upon failure to receive the Delivery Status Message
 within the expected time period, modify the routing to the far-end
 Destination, or take other actions.
2. A [Database Store
 Message](#msg_DatabaseStore), containing a
 [LeaseSet](#struct_LeaseSet) for
 the originating Destination, with [Delivery
 Instructions](#struct_GarlicCloveDeliveryInstructions)
 specifying the far-end destination\'s router. By periodically
 bundling a LeaseSet, the router ensures that the far-end will be
 able to maintain communications. Otherwise the far-end would have to
 query a floodfill router for the network database entry, and all
 LeaseSets would have to be published to the network database, as
 explained on the [network database page]().

By default, the Delivery Status and Database Store Messages are bundled
when the local LeaseSet changes, when additional [Session
Tags](#type_SessionTag) are delivered,
or if the messages have not been bundled in the previous minute. As of
release 0.9.2, the client may configure the default number of Session
Tags to send and the low tag threshold for the current session. See the
[I2CP options specification](#options) for
details. The session settings may also be overridden on a per-message
basis. See the [I2CP Send Message Expires
specification](#msg_SendMessageExpires) for
details.

Obviamente, los mensajes adicionales son agrupados por un propósito
específico, y no son parte del esquema general de rutado.

Desde la versión 0.9.12, el mensaje de estado de entrega está
encapsulado en otro mensaje ajo (garlic) por el originador, así que los
contenidos están cifrados y no son visibles para los routers I2P en la
ruta de retorno.

### Almacenamiento en la base de datos de un FloodFill

As explained on the [network database
page](#delivery), local
[LeaseSets](#struct_LeaseSet) are sent
to floodfill routers in a [Database Store
Message](#msg_DatabaseStore) wrapped in a
[Garlic Message](#msg_Garlic) so it is not
visible to the tunnel\'s outbound gateway.

## Trabajo futuro

The Garlic Message mechanism is very flexible and provides a structure
for implementing many types of mixnet delivery methods. Together with
the unused delay option in the [tunnel message Delivery
Instructions](#struct_TunnelMessageDeliveryInstructions),
a wide spectrum of batching, delay, mixing, and routing strategies are
possible.

En particular, hay potencial para mucha más flexibilidad en el punto
final del túnel de salida. Los mensajes podrían ser rutados desde ahí a
uno o varios túneles (con lo cual se minimizarían las conexiones de
punto a punto), o enviar a varios túneles para hacerlo redundante, o
hacer streming de audio o vídeo.

Estos experimentos pudrían entrar en conflicto con la necesidad de
seguridad y anonimato, ya sea limitando ciertos caminos de enrutado,
restringiendo los mensajes I2NP que puedan ser enviados a través de
varios caminos, e imponiendo ciertos tiempos de espiración a los
mensajes.

As a part of [ElGamal/AES encryption](), a
garlic message contains a sender specified amount of padding data,
allowing the sender to take active countermeasures against traffic
analysis. This is not currently used, beyond the requirement to pad to a
multiple of 16 bytes.

Encryption of additional messages to and from the [floodfill
routers](#delivery).

## Referencias

- El término de garlic routing, rutado de ajo, fue acuñado en la
 [Master\'s thesis](http://www.freehaven.net/papers.html) en Free
 Haven de Roger Dingledine (June 2000), ver sección 8.1.1 de
 [Michael J. Freedman](http://www.cs.princeton.edu/~mfreed/).
- [Publicaciones sobre ruter
 Onion](http://www.onion-router.net/Publications.html)
- [Rutado Onion en la
 Wikipedia](http://en.wikipedia.org/wiki/Onion_routing)
- [Rutado Garlic en la
 Wikipedia](http://en.wikipedia.org/wiki/Garlic_routing)
- [I2P Meeting 58]() (2003) discussing the
 implementation of garlic routing
- [Tor](https://www.torproject.org/)
- [Publicaciones en Free
 Heaven](http://freehaven.net/anonbib/topic.html)
- El rutado Onion fue descrito por primera vez en 1996 por David M.
 Goldschlag, Michael G. Reed, and Paul F. Syverson en [Hiding Routing
 Information](http://www.onion-router.net/Publications/IH-1996.pdf).


