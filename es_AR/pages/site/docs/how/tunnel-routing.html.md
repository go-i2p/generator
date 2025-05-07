 Enrutamiento de
túnel Julio de 2011
0.8.7 

## Información general

Esta página contiene una introducción a la terminología y funcionamiento
de los túneles I2P, con enlaces a páginas más técnicas, detalles y
especificaciones.

As briefly explained in the [introduction](), I2P
builds virtual \"tunnels\" - temporary and unidirectional paths through
a sequence of routers. These tunnels are classified as either inbound
tunnels (where everything given to it goes towards the creator of the
tunnel) or outbound tunnels (where the tunnel creator shoves messages
away from them). When Alice wants to send a message to Bob, she will
(typically) send it out one of her existing outbound tunnels with
instructions for that tunnel\'s endpoint to forward it to the gateway
router for one of Bob\'s current inbound tunnels, which in turn passes
it to Bob.

![Alice connecting through her outbound tunnel to Bob via his inbound
tunnel](images/tunnelSending.png "Alice connecting through her outbound tunnel to Bob via his inbound tunnel")

 A: Gateway de salida (Alice)
 B: Participante de salida
 C: Extremo de salida
 D: Pasarela (gateway) entrante
 E: Participante de entrada
 F: Punto final de entrada (Bob)

## Vocabulario de los túneles

- **Tunnel gateway** - the first router in a tunnel. For inbound
 tunnels, this is the one mentioned in the LeaseSet published in the
 [network database](). For outbound tunnels,
 the gateway is the originating router. (e.g. both A and D above)
- **Túnel punto final, endpoint** - el último ruter en un túnel (ej, C
 y F arriba)
- **Túnel participante** - todos los ruters en un túnel excepto la
 puerta de salida o el punto final (ej, B y E arriba)
- **Túnel de n-saltos** - un túnel con un número específico de saltos
 entre routers I2P, ej.:
 - **Túnel de 0 saltos** - un túnel donde la puerta de salida,
 gateway, es también el punto final, endpoint.
 - **Túnel de 1 salto** - un túnel donde la puerta de salida habla
 directamente con el punto final.
 - **Túnel de 2 (o más) saltos** - un túnel donde hay al menos un
 túnel intermedio participante, (el diagrama de arriba incluye
 dos túneles de 2 saltos - uno de salida desde Alice, uno de
 entrada hacia Bob)
- **Tunnel ID** - A [4 byte
 integer](#type_TunnelId) different
 for each hop in a tunnel, and unique among all tunnels on a router.
 Chosen randomly by the tunnel creator.

## Infomación de la construcción del túnel

Routers performing the three roles (gateway, participant, endpoint) are
given different pieces of data in the initial [Tunnel Build
Message]() to accomplish their tasks:

- **El túnel puerta de salida obtiene:**
 - **tunnel encryption key** - an [AES private
 key](#type_SessionKey) for
 encrypting messages and instructions to the next hop
 - **tunnel IV key** - an [AES private
 key](#type_SessionKey) for
 double-encrypting the IV to the next hop
 - **reply key** - an [AES public
 key](#type_SessionKey) for
 encrypting the reply to the tunnel build request
 - **IV de respuesta** - El IV para cifrar la respuesta de la
 petición de construcción del túnel.
 - **ID del túnel** - In entero de 4 bytes (sólo para las puertas
 de salida de entrada)
 - **Siguiente salto** - Cual es el siguiente ruter en el camino (a
 no ser que sea un túnel de 0 saltos, y la puerta de salida sea
 también el punto final)
 - **ID del túnel siguiente** - La ID del túnel en el siguiente
 salto
- **Todos los túneles intermedios participantes obtienen:**
 - **tunnel encryption key** - an [AES private
 key](#type_SessionKey) for
 encrypting messages and instructions to the next hop
 - **tunnel IV key** - an [AES private
 key](#type_SessionKey) for
 double-encrypting the IV to the next hop
 - **reply key** - an [AES public
 key](#type_SessionKey) for
 encrypting the reply to the tunnel build request
 - **IV de respuesta** - El IV para cifrar la respuesta de la
 petición de construcción del túnel.
 - **ID del túnel** - Un entero de 4 bytes
 - **Siguiente salto** - cuál es el siguiente ruter en el camino
 - **ID del túnel siguiente** - La ID del túnel en el siguiente
 salto
- **El túnel punto final obtiene:**
 - **tunnel encryption key** - an [AES private
 key](#type_SessionKey) for
 encrypting messages and instructions to the the endpoint
 (itself)
 - **tunnel IV key** - an [AES private
 key](#type_SessionKey) for
 double-encrypting the IV to the endpoint (itself)
 - **reply key** - an [AES public
 key](#type_SessionKey) for
 encrypting the reply to the tunnel build request (outbound
 endpoints only)
 - **IV de respuesta** - el IV para cifrar la respuesta para la
 petición de construcción del túnel (sólo para los puntos finales
 de salida)
 - **ID del túnel** - Un entero de 4 bytes (sólo para los puntos
 finales de salida)
 - **Ruter de respuesta** - para enviar la respuesta a través de la
 puerta de salida del túnel de entrada (sólo puntos finales de
 salida)
 - **ID del túnel de respuesta** - El ID del túnel del ruter de
 respuesta (sólo para puntos finales de salida)

Details are in the [tunnel creation
specification]().

## Agrupación de túneles

Several tunnels for a particular purpose may be grouped into a \"tunnel
pool\", as described in the [tunnel
specification](#tunnel.pooling). This
provides redundancy and additional bandwidth. The pools used by the
router itself are called \"exploratory tunnels\". The pools used by
applications are called \"client tunnels\".

## Tamaño del túnel {#length}

As mentioned above, each client requests that their router provide
tunnels to include at least a certain number of hops. The decision as to
how many routers to have in one\'s outbound and inbound tunnels has an
important effect upon the latency, throughput, reliability, and
anonymity provided by I2P - the more peers that messages have to go
through, the longer it takes to get there and the more likely that one
of those routers will fail prematurely. The less routers in a tunnel,
the easier it is for an adversary to mount traffic analysis attacks and
pierce someone\'s anonymity. Tunnel lengths are specified by clients via
[I2CP options](#options). The maximum number of
hops in a tunnel is 7.

### Túneles de 0-saltos

Sin routers remotos en un túnel, el usuario tiene una denegabilidad
plausible muy básica (ya que ninguno de nosotros sabe con seguridad si
el par que les envió el mensaje no estaba simplemente reenviándolo al
formar parte del túnel). Sin embargo, sería realmente fácil montar un
ataque de análisis estadístico y observar que los mensajes apuntando a
un destino específico siempre son enviados a través de una única
pasarela (\`gateway\`). El análisis estadístico contra túneles de salida
de 0-saltos son más complejos, pero podrían mostrar una información
similar (aunque sería ligeramente más difícil de montar).

### Túneles de 1-salto

With only one remote router in a tunnel, the user has both plausible
deniability and basic anonymity, as long as they are not up against an
internal adversary (as described on [threat
model]()). However, if the adversary ran a
sufficient number of routers such that the single remote router in the
tunnel is often one of those compromised ones, they would be able to
mount the above statistical traffic analysis attack.

### Túneles de 2-saltos

Con dos o más routers remotos en un túnel, los costes de montar el
ataque de análisis de tráfico aumentan, ya que muchos routers remotos
tendrían que estar comprometidos para montarlo.

### Túneles de 3 (o más)-saltos

To reduce the susceptibility to [some attacks](), 3
or more hops are recommended for the highest level of protection.
[Recent studies]() also conclude that more than 3
hops does not provide additional protection.

### Longitudes predeterminadas de los túneles

The router uses 2-hop tunnels by default for its exploratory tunnels.
Client tunnel defaults are set by the application, using [I2CP
options](#options). Most applications use 2 or 3
hops as their default.

## Comprobación de túneles {#testing}

All tunnels are periodically tested by their creator by sending a
DeliveryStatusMessage out an outbound tunnel and bound for another
inbound tunnel (testing both tunnels at once). If either fails a number
of consecutive tests, it is marked as no longer functional. If it was
used for a client\'s inbound tunnel, a new leaseSet is created. Tunnel
test failures are also reflected in the [capacity rating in the peer
profile](#capacity).

## Creación de túneles

Tunnel creation is handled by [garlic
routing]() a Tunnel Build Message to a
router, requesting that they participate in the tunnel (providing them
with all of the appropriate information, as above, along with a
certificate, which right now is a \'null\' cert, but will support
hashcash or other non-free certificates when necessary). That router
forwards the message to the next hop in the tunnel. Details are in the
[tunnel creation specification]().

## Tunnel encryption

Multi-layer encryption is handled by [garlic
encryption]() of tunnel messages. Details
are in the [tunnel specification](). The IV
of each hop is encrypted with a separate key as explained there.

## Trabajo futuro

- Podrían usarse otras técnicas de evaluación de túneles, tales como
 la envoltura garlic (\`ajo\`) de un número de pruebas en forma de
 dientes (\`cloves\`, del ajo), comprobando separadamente a los
 participantes individuales en los túneles, etc.
- Cambiar a configuración predeterminada de túneles de 3-saltos.
- En una versión de un futuro lejano, opciones especificando las
 configuraciones de depositado, mezclado y generación de datos de
 relleno criptográficamente descartables,\`chaff,\` podrían ser
 implementadas.
- En una versión de un futuro lejano, límites en la cantidad y tamaño
 de los mensajes permitidos durante la vida del túnel podrían ser
 implementados (ej. no más de 300 mensajes o 1 MB por minuto).

## Consulte también

- [Especificación de
 túneles]()
- [Especificación de creación de
 túneles]()
- [Túneles
 unidireccionales]()
- [Especificación de mensajes de
 túnel]()
- [Enrutamiento ajo
 (\'garlic\')]()
- [ElGamal/AES+SessionTag (etiqueta de
 sesión)]()
- [Opciones de
 I2CP](#options)


