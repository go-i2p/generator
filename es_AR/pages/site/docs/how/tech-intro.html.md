 I2P: Un sistema
escalable para las comunicaciones anónimas 2025-01 0.9.65 

- [Introducción](#intro)
- [Como funciona I2P](#op)
 - [Información general](#op.overview)
 - [Túneles](#op.tunnels)
 - [Base de datos de la red](#op.netdb)
 - [Protocolos de transporte](#op.transport)
 - [Cifrado](#op.crypto)
- [El futuro](#future)
 - [Restricted Routes](#future.restricted)
 - [Variable Latency](#future.variablelatency)
- [Similar Networks](#similar)
 - [Tor](#similar.tor)
 - [Freenet](#similar.freenet)
- [Application Layer](#app)
 - [Streaming](#app.streaming)
 - [Naming and Addressbook](#app.naming)
 - [I2PSnark](#app.i2psnark)
 - [I2PTunnel](#app.i2ptunnel)
 - [I2P Email](#app.i2pmail)

 

NOTE: This document was originally written by jrandom in 2003. While we
strive to keep it current, some information may be obsolete or
incomplete. The transport and cryptography sections are current as of
2025-01.

# Introducción {#intro}

I2P es una capa de red auto organizada, resistente, anónima, dentro de
la cual pueden funcionar un gran número de aplicaciones con diferentes
modelos de seguridad y anonimato. Cada una de estas aplicaciones pueden
usar sus propios niveles de seguridad y sus propios niveles de
rendimiento, sin preocuparse por crear una implementación apropiada de
una red libre, permitiendoles mezclar sus actividades con un gran número
de usuarios anónimos que ya utilizan I2P.

Applications available already provide the full range of typical
Internet activities - **anonymous** web browsing, web hosting, chat,
file sharing, e-mail, blogging and content syndication, as well as
several other applications under development.

- Navegación web: usando cualquier navegador que soporte un proxy.
- Chat: IRC and other protocols
- File sharing: [I2PSnark](#app.i2psnark) and other applications
- E-mail: [susimail](#app.i2pmail) and other applications
- Blog: using any local web server, or available plugins

Unlike web sites hosted within content distribution networks like
[Freenet](#similar.freenet) or [GNUnet](https://www.gnunet.org/en/), the
services hosted on I2P are fully interactive - there are traditional
web-style search engines, bulletin boards, blogs you can comment on,
database driven sites, and bridges to query static systems like Freenet
without needing to install it locally.

Con todos estas aplicaciones anónimas habilitadas, I2P toma el rol de
aplicación mensajera, una aplicación, por ejemplo, dice que quiere
enviar datos a un identificador criptográfico (un \"destino\") e I2P se
encarga de asegurarse de que lleguen seguros y anónimos. I2P también
ofrece un librería simple de [streaming](#app.streaming) que permite que
los mensajes sean enviados como streams fiables y ordenados, ofreciendo
transparentemente algoritmos de control de congestión TCP ajustados para
el retardo de alto de bandda de producto de la red. Aunque hay proxys
SOCKS para usar casi cualquier aplicación con I2P estas se han limitado,
ya que la mayoría de las aplicaciones muestran, lo que se llama en el
contexto anónimo, información sensible. La única forma segura de usar
aplicaciones externas sería comprobar completamente la aplicación para
asegurarse que funciona bien, y para ayudar con este problema
proporcionamos una serie de APIs en varios idiomas que pueden usarse
para sacarle el mayor provecho a la red.

I2P is not a research project - academic, commercial, or governmental,
but is instead an engineering effort aimed at doing whatever is
necessary to provide a sufficient level of anonymity to those who need
it. It has been in active development since early 2003 with one full
time developer and a dedicated group of part time contributors from all
over the world. All of the work done on I2P is open source and freely
available on the [website](), with the majority of
the code released outright into the public domain, though making use of
a few cryptographic routines under BSD-style licenses. The people
working on I2P do not control what people release client applications
under, and there are several GPL\'ed applications available
([I2PTunnel](#app.i2ptunnel), [susimail](#app.i2pmail),
[I2PSnark](#app.i2psnark), [I2P-Bote](#app.i2pbote),
[I2Phex](#app.i2phex) and others.).
[Funding]() for I2P comes entirely from
donations, and does not receive any tax breaks in any jurisdiction at
this time, as many of the developers are themselves anonymous.

# Cómo funciona {#op}

## Información general {#op.overview}

Para entender como funciona I2p es esencial entender varios conceptos.
Primero, I2P hace una separación completa entre las aplicaciones usadas
en la red (un \"ruter\") y los puntos finales anónimos
(\"destinaciones\") asociados a las aplicaciones individuales. El hecho
de que alguien ejecute I2P normalmente no es un secreto. Lo que se
oculta es la información y lo que hace el usuario, así como las
destinaciones particulares a la que se conecta el ruter. Los usuarios
finales tendrán normalmente varias destinaciones locales en su ruter -
por ejemplo, una destinación conectando con servidores IRC, otras para
las webs anónimas (eepsites), otra para I2Phex, otra para los torrets,
etc.

Otro concepto crítico a entender es el concepto de \"túnel\". Un túnel
es un camino directo a través de una lista seleccionada y explícita de
ruters. Se usa un cifrado por capas, por lo cual cada ruter sólo puede
descifrar una capa. La información descifrada contiene la IP del ruter
siguiente, así como la información cifrada para ser enviada. Cada túnel
tiene un punto de inicio (el primer ruter, también conocido como
\"gateway\") y un punto final. Los mensajes sólo se pueden enviar en una
dirección. Para enviar un mensaje de respuesta se debe crear un nuevo
túnel.

::: {.box style="text-align:center;"}
\
\
![Inbound and outbound tunnel
schematic](images/tunnels.png "Inbound and outbound tunnel schematic")\
\
Figura 1: Existen 2 tipos de túneles: de entrada y de salida.
:::

Existen 2 tipos de túneles: **túneles \"outbound\", de salida** envían
mensajes hacia fuera desde el creador de túneles, mientras que **túneles
\"inbound\", de entrada** llevan los mensajes hasta el creador de
túneles . Combinando estos 2 túneles los usuarios pueden enviar mensajes
a otros usuarios. El remitente (\"Alice\" en la imagen anterior) crea un
túnel de salida, mientras que el receptor (\"Bob\" en la imagen de
arriba) crea un túnel entrante. La puerta de salida de un túnel de
entrada puede recibir mensajes de cualquier usuario que serán enviados
hasta en punto final (\"Bob\"). El punto final del túnel de salida
necesita enviar el mensaje a la puerta de salida del túnel de entrada.
Para conseguir esto, el remitente (\"Alice\") añade instrucciones al
mensaje cifrado. Una vez que el punto final y el túnel de salida
descifran el mensaje, tendrán las instrucciones para poder enviar el
mensaje la puerta de salida de entrada correcta (la puerta de salida
hacia \"Bob\").

Un tercer concepto crítico es el de la **\"base de datos de la red\"**
(o \"netDb\") - un par de algoritmos hechos para compartir los datos de
la red. Los 2 tipos de datos compartidos son **\"routerInfo\"** y
**\"leaseSets\"** - la información del ruter, ruterinfo, da a los ruters
la información necesaria para poder contactar con un ruter en particular
(sus claves públicas, dirección de transporte, etc), mientras que el
leaseSet le da a los ruters un número de \"leases\", asignaciones. Cada
una de estas asignaciones especifica una puerta de salida de un túnel,
la cual permite alcanzar una destinación específica. La información
completa en un lease es:

- Gateway de entrada para un túnel que permite alcanzar una
 destinación específica.
- Tiempo de espiración del túnel.
- Par de claves públicas para poder cifrar el mensaje (para enviarlo a
 través del túnel y alcanzar su destino).

Los ruters envían su routerInfo directamente a la netDB, mientras que
los leaseSets son enviados a través de los túneles de salida (los
leaseSets tienen que ser enviados anónimamente para evitar la
correlación del ruter con sus leaseSets)

Podemos combinar los anteriores conceptos para construir conexiones
dentro de la red.

Para crear sus propios tuneles de entrada y salida, Alice no mira en la
netDB para obtener la información. Ella obtiene listas de pares que
puede usar como saltos en sus túneles. Entonces puede enviar un mensaje
de construcción al primer salto, solicitando la construcción de un túnel
y pidiendo a ese ruter que siga adelante con la construcción del
mensaje, hasta que el túnel ha sido construido.

::: {.box style="text-align:center;"}
\
\
![Request information on other
routers](images/netdb_get_routerinfo_1.png "Request information on other routers")
                   \
\
![Build tunnel using router
information](images/netdb_get_routerinfo_2.png "Build tunnel using router information")\
\
Figura 2: La información del ruter es usada para construir túneles.
:::

\

Cuando Alice quiere enviar un mensaje a Bob, primero mira en la netDB
hasta encontrar la leaseSet de Bob, dando sus propias gateways de
entrada. Entonces ella elije uno de los túneles de salida y envía su
mensaje con instrucciones para que el punto final de túnel de salida
reenvíe el mensaje a unos de las gateways de entrada de BoB. Cuando el
punto final del túnel de salida recibe estas instrucciones, reenvía el
mensaje como se ha pedido, y cuando el la gateway del túnel de entrada
de Bob lo recibe, es enviado hasta el ruter de Bob. Si Alice quiere que
Bob pueda responder al mensaje necesita transmitir explícitamente su
propia destinación como parte del mensaje. Esto puede hacerse
introduciendo una capa de nivel superior, lo cual se hace en la
librearía de [streaming](#app.streaming). Alice también puede acortar el
tiempo de respuesta construyendo su LeaseSet mas reciente con el
mensaje, con lo cual Bob no necesita mirar en la netDB para responder,
pero esto es opcional.

::: {.box style="text-align:center;"}
\
\
![Connect tunnels using
LeaseSets](images/netdb_get_leaseset.png "Connect tunnels using leaseSets")\
\
Figura 3: Los LeaseSets son usados para conectar los túneles de entrada
y salida.
:::

\

Mientras que los túneles están cifrados en capas para prevenir ser
revelados sin permiso a otros pares de la red (ya que la capa de
transporte en sí misma no previene la muestra no autorizada a pares
fuera de la red), es necesario añadir un final adicional a la capa de
cifrado final para ocultar el mensaje del punto final del túnel de
salida y de la puerta de salida del túnel de entrada. Este \"[cifrado
garlic](#op.garlic)\" permite al ruter de Alice envolver varios mensajes
en un simple \"mensaje garlic\", cifrado para una calve pública en
particular y así los pares intermediarios no pueden determinar cuantos
mensajes hay dentro del mensaje garlic, que dicen esos mensajes, o a
donde están destinados los mensajes individuales. Para una comunicación
típica entre Alice y Bob, el garlic será cifrado con la clave pública
publicada en el leaseSet de bob, permitiendo que el mensaje sea cifrado
sin dar la clave pública al dueño del ruter de Bob.

Otra cosa importante a tener en cuenta es que I2P esta totalmente basado
en mensajes y que algunos mensajes se pueden perder a lo largo del
camino. Las aplicaciones que usan I2P pueden usar el interfaz orientado
a mensajes y cuidar de su propio control de congestión y necesidades de
fiabilidad, pero la mayoría estaría más satisfecha reutilizando la
librería de [streaming](#app.streaming) que proveemos para ver I2P como
una red basada en streams.

## Túneles {#op.tunnels}

Ambos túneles, de entrada y de salida funcionan con los mismos
principios. La puerta de salida del túnel acumula un número de mensajes,
eventualmente pre procesandolos para poder ser entregados. Después, la
puerta de salida cifra esa información pre procesada y la envía al
primer salto. El par y los siguientes túneles participantes añaden una
capa de cifrado después de verificar que no es duplicado y antes de
enviarlo al siguiente par. Eventualmente, este mensaje llega al punto
final, donde el mensaje es dividido de nuevo y enviado conforme a lo
solicitado. La diferencia surge en lo que hace el creador del túnel -
para los túneles de entrada, el creador es el punto final y simplemente
descifra todas las capas añadidas, mientras que para los túneles de
salida, el creador es la puerta de salida y pre descifra todas las capas
con lo que después de que todos las capas de cifrado por salto son
añadidas, el mensaje llega en claro al túnel de punto final.

La elección de los pares específicos par pasar los mensajes al igual que
su orden es importante para entender el anonimato y el rendimiento de
I2P. Mientras que la base de datos de la red (debajo) tiene su propio
criterio al elegir en qué pares consultar y almacenar entradas, los
creadores de los túneles pueden usar cualquier par en la red y en
cualquier orden (e incluso cualquier número de veces) en un solo túnel.
Si se conocen globalmente la latencia exacta y capacidad de datos, la
selección del orden vendrá dada por las necesidades particulares del
cliente y su modelo de seguridad. Desafortunadamente, no es trivial
obtener anónimamente la latencia y la capacidad de datos, y al
dependerse de pares no confiables para obtener esta información crea
serios problemas en el anonimato.

Desde la perspectiva del anonimato, la técnica más simple sería elegir
pares aleatoriamente de toda la red, ordenarlos aleatoriamente y usar
esos pares en ese orden eternamente. Desde la perspectiva del
rendimiento, la técnica más simple sería elegir los pares más rápidos
con la capacidad necesaria, repartiendo la carga entre varios pares para
manejar transparentemente los fallos, y para reconstruir el túnel cuando
cambie la información sobre la capacidad disponible. Mientras que el
primer modelo es frágil y deficiente, el segundo necesita información no
accesible y no ofrece suficiente anonimato. I2P en cambio funciona
ofreciendo un amplio abanico de estrategias de selección de pares, junto
con código que tienen en cuenta el nivel de anonimato para organizar los
pares y sus perfiles.

Por defecto I2P está constantemente comprobando los pares con los que
interactúa y midiendo su comportamiento - por ejemplo, cuando un par
responde a una búsqueda de netBD en 1,3 segundos, la latencia de vuelta
es guardada en los perfiles de todos los ruters implicados en los 2
túneles (de entrada y de salida) por los que la respuesta ha pasado, así
como el perfil del par consultado. Las mediciones directas, como el
retardo de la capa de transporte o la congestión, no se usan como parte
del perfil, ya que puede manipularse y ser asociada con el ruter que
está midiendo, exponiéndolo a ataques triviales. Mientras se calculan
estos perfiles, una serie de cálculos se ejecutan en cada uno para
resumir su rendimiento - su latencia, su capacidad para manejar la
pérdida de actividad, si está saturado, y cómo de bien está integrado
dentro de la red. Estos cálculos son entonces comparados por los pares
activos para organizar los ruters en 4 niveles - rápido y con gran
capacidad, gran capacidad, sin caídas y con caídas. Los umbrales de
estos niveles son determinados dinámicamente, y mientras que se usan
algoritmos bastantes sencillos también existen otras alternativas.

Using this profile data, the simplest reasonable peer selection strategy
is to pick peers randomly from the top tier (fast and high capacity),
and this is currently deployed for client tunnels. Exploratory tunnels
(used for netDb and tunnel management) pick peers randomly from the
\"not failing\" tier (which includes routers in \'better\' tiers as
well), allowing the peer to sample routers more widely, in effect
optimizing the peer selection through randomized [hill
climbing](https://en.wikipedia.org/wiki/Hill_climbing). These strategies
alone do however leak information regarding the peers in the router\'s
top tier through predecessor and netDb harvesting attacks. In turn,
several alternatives exist which, while not balancing the load as
evenly, will address the attacks mounted by particular classes of
adversaries.

Tomando una clave aleatoria y ordenando los pares de acuerdo a su
distancia XOR de ella, la información expuesta es reducida en los
ataques del predecesor y de cosechado conforme a la velocidad de fallo
del par y de su mezcla de niveles. Otra estrategia simple para tratar
con el ataque del cosechado de la netDB es simplemente fijando la puerta
de salida(s) de túnel de entrada, ya sea aleatorizando los pares más
lejos o en los túneles. Para tratar con el ataque del predecesor por
adversarios con los que contacta el cliente, los puntos finales del
túnel de salida deberían permanecer también fijos. Para seleccionar que
par fijar en el punto más expuesto se necesitará, por supuesto, un
límite de duración ya que todos los pares fallan más tarde o más
temprano, con lo cual podría ser ajustado de manera reactiva o evitado
de manera activa, para imitar el tiempo medio de los fallos de otros
ruters. Estas 2 estrategias pueden ser combinadas en turnos, usando un
par expuesto fijo y un orden basado en XOR dentro de los propios
túneles. Una estrategia más rígida sería fijar los pares justos y
ordenarlos en un túnel potencial, sólo usando pares individuales si
todos están de acuerdo en participar de la misma forma cada vez. Esto
varía del ordenado basado en XOR en que el predecesor y sucesor de cada
par es siempre el mismo, mientras que el XOR asegura que el orden no
cambie.

As mentioned before, I2P currently (release 0.8) includes the tiered
random strategy above, with XOR-based ordering. A more detailed
discussion of the mechanics involved in tunnel operation, management,
and peer selection can be found in the [tunnel
spec]().

## Base de datos de la red {#op.netdb}

As mentioned earlier, I2P\'s netDb works to share the network\'s
metadata. This is detailed in [the network
database]() page, but a basic explanation is
available below.

All I2P routers contain a local netDb, but not all routers participate
in the DHT or respond to leaseset lookups. Those routers that do
participate in the DHT and respond to leaseset lookups are called
\'floodfills\'. Routers may be manually configured as floodfills, or
automatically become floodfill if they have enough capacity and meet
other criteria for reliable operation.

Other I2P routers will store their data and lookup data by sending
simple \'store\' and \'lookup\' queries to the floodfills. If a
floodfill router receives a \'store\' query, it will spread the
information to other floodfill routers using the [Kademlia
algorithm](http://en.wikipedia.org/wiki/Kademlia). The \'lookup\'
queries currently function differently, to avoid an important [security
issue](#lookup). When a lookup is done, the
floodfill router will not forward the lookup to other peers, but will
always answer by itself (if it has the requested data).

En la base de datos de la red se almacenan dos tipos de información.

- **RouterInfo** almacena información sobre un ruter I2P determinado y
 como contactar con él.
- **LeaseSet** almacena información sobre una destinación específica
 (e.g. web I2P, servidor de correo\...)

Toda esta información es firmada par la parte publicadora y verificada
por cualquier ruter I2P que use o almacene la información. Además, los
datos contienen información de la hora para evitar el almacenamiento de
entradas antiguas y posibles ataques. Esto es por que I2P empaqueta el
código necesario para mantener la fecha correcta, a veces consultando
algunos servidores SNTP (por defecto
[pool.ntp.org](http://www.pool.ntp.org/)) y detectando diferencias entre
los ruters y la capa de transporte.

Hay algunos comentarios adicionales que también son importantes:

- **Leasesets cifrados y no publicados:**

 One could only want specific people to be able to reach a
 destination. This is possible by not publishing the destination in
 the netDb. You will however have to transmit the destination by
 other means. This is supported by \'encrypted leaseSets\'. These
 leaseSets can only be decoded by people with access to the
 decryption key.

- **Obteniendo los pares iniciales o Bootstrapping:**

 Bootstrapping the netDb is quite simple. Once a router manages to
 receive a single routerInfo of a reachable peer, it can query that
 router for references to other routers in the network. Currently, a
 number of users post their routerInfo files to a website to make
 this information available. I2P automatically connects to one of
 these websites to gather routerInfo files and bootstrap. I2P calls
 this bootstrap process \"reseeding\".

- **Escalabilidad de las búsquedas:**

 Lookups in the I2P network are iterative, not recursive. If a lookup
 from a floodfill fails, the lookup will be repeated to the
 next-closest floodfill. The floodfill does not recursively ask
 another floodfill for the data. Iterative lookups are scalable to
 large DHT networks.

## Protocolos de transporte {#op.transport}

La comunicación entre ruters necesita proporcionar confidencialidad e
integridad contra cualquier adversario externo mientras se autentifica
que el ruter contactado es el que debe recibir el mensaje. Los detalles
de como se comunican los ruters con otros ruters no son críticos - se
han usado tres protocolos diferentes en varios puntos para suplir estas
necesidades.

I2P currently supports two transport protocols,
[NTCP2]() over TCP, and
[SSU2]() over UDP. These have replaced the
previous versions of the protocols, [NTCP]() and
[SSU](), which are now deprecated. Both protocols
support both IPv4 and IPv6. By supporting both TCP and UDP transports,
I2P can effectively traverse most firewalls, including those intended to
block traffic in restrictive censorship regimes. NTCP2 and SSU2 were
designed to use modern encryption standards, improve traffic
identification resistance, increase efficiency and security, and make
NAT traversal more robust. Routers publish each supported transport and
IP address in the network database. Routers with access to public IPv4
and IPv6 networks will usually publish four addresses, one for each
combination of NTCP2/SSU2 with IPv4/IPv6.

[SSU2]() supports and extends the goals of SSU.
SSU2 has many similarities to other modern UDP-based protocols such as
Wireguard and QUIC. In addition to the reliable transport of network
messages over UDP, SSU2 provides specialized facilities for
peer-to-peer, cooperative IP address detection, firewall detection, and
NAT traversal. As described in the [SSU spec]():

> La meta de este protocolo es proporcionar la entrega de mensajes de
> forma segura, con autentificación, semifiable y no ordenada, revelando
> sólo una pequeña cantidad de datos fácilmente discernible para
> terceras partes. Debe soportar comunicaciones de alto nivel así como
> sistemas de control de congestión adaptados-a-TCP, y puede incluir
> también detección de PMTU (máxima unidad de transferencia de la red).
> Debe ser capaz de mover eficientemente un gran volumen de datos a
> velocidades suficientes para los usuarios domésticos. Además debe
> soportar técnicas para afrontar los obstáculos en la red, como la
> mayoría de NATs (traductores de direcciones de red) o de cortafuegos
> (firewalls).

NTCP2 supports and extends the goals of NTCP. It provides an efficient
and fully encrypted transport of network messages over TCP, and
resistance to traffic identification, using modern encryption standards.

I2P soporta simultáneamente varios tipos de transportes. Para conexiones
de salida se selecciona un determinado tipo de transporte a través de
\"pujas\". Cada tipo de transporte puja por la conexión y el valor
relativo de esa puja asignará la prioridad. Los transportes pueden
responder con varias apuestas, dependiendo de si ya hay una conexión
establecida con el par.

The bid (priority) values are implementation-dependent and may vary
based on traffic conditions, connection counts, and other factors.
Routers also publish their transport preferences for inbound connections
in the network database as transport \"costs\" for each transport and
address.

## Cifrado {#op.crypto}

I2P uses cryptography at several protocol layers for encryption,
authentication, and verification. The major protocol layers are:
transports, tunnel build messages, tunnel layer encryption, network
database messages, and end-to-end (garlic) messages. I2P\'s original
design used a small set of cryptographic primitives that at the time
were considered secure. These included ElGamal asymmetric encryption,
DSA-SHA1 signatures, AES256/CBC symmetric encryption, and SHA-256
hashes. As available computing power increased and cryptographic
research evolved substantially over the years, I2P needed to upgrade its
primitives and protocols. Therefore, we added a concept of \"encryption
types\" and \"signature types\", and extended our protocols to include
these identifiers and indicate support. This allows us to periodically
update and extend the network support for modern cryptography and
future-proof the network for new primitives, without breaking backward
compatibility or requiring a \"flag day\" for network updates. Some
signature and encryption types are also reserved for experimental use.

The current primitives used in most protocol layers are X25519 key
exchange, EdDSA signatures, ChaCha20/Poly1305 authenticated symmetric
encryption, and SHA-256 hashes. AES256 is still used for tunnel layer
encryption. These modern protocols are used for the vast majority of
network communication Older primitives including ElGamal, ECDSA, and
DSA-SHA1 continue to be supported by most implementations for backward
compatibility when communicating with older routers. Some old protocols
have been deprecated and/or removed completely. In the near future we
will begin research on a migration to post-quantum (PQ) or hybrid-PQ
encryption and signatures to maintain our robust security standards.

These cryptographic primitives are combined together to provide I2P\'s
layered defenses against a variety of adversaries. At the lowest level,
inter-router communication is protected by the transport layer security.
[Tunnel](#op.tunnels) messages passed over the transports have their own
layered encryption. Various other messages are passed along inside
\"garlic messages\", which are also encrypted.

### Mensajes Garlic {#op.garlic}

Garlic messages are an extension of \"onion\" layered encryption,
allowing the contents of a single message to contain multiple
\"cloves\" - fully formed messages alongside their own instructions for
delivery. Messages are wrapped into a garlic message whenever the
message would otherwise be passing in cleartext through a peer who
should not have access to the information - for instance, when a router
wants to ask another router to participate in a tunnel, they wrap the
request inside a garlic, encrypt that garlic to the receiving router\'s
public key, and forward it through a tunnel. Another example is when a
client wants to send a message to a destination - the sender\'s router
will wrap up that data message (alongside some other messages) into a
garlic, encrypt that garlic to the public key published in the
recipient\'s leaseSet, and forward it through the appropriate tunnels.

Las \"instrucciones\" adjuntas a cada diente, \'clove\', dentro de la
capa de cifrado incluyen la habilidad de solicitar que el diente sea
enviado localmente a un ruter remoto, o a un túnel remoto en un ruter
remoto. Hay campos en esas instrucciones que permiten a un par solicitar
que el envío sea retrasado un cierto tiempo o hasta que se cumpla cierta
condición, pero no funcionará hasta que los [retardos no
triviales](#future.variablelatency) funcionen en estas versiones. Es
posible enrutar explícitamente mensajes garlic de cualquier número de
saltos sin construir túneles, o incluso re enrutar mensajes de túnel
envolviéndolos en un mensaje garlic y enviándolos por unos cuantos
saltos antes de enviarlos al siguiente salto en el túnel, pero estas
técnicas no se usan en en las implementaciones existentes.

### Etiquetas de sesión {#op.sessiontags}

As an unreliable, unordered, message based system, I2P uses a simple
combination of asymmetric and symmetric encryption algorithms to provide
data confidentiality and integrity to garlic messages. The original
combination was referred to as ElGamal/AES+SessionTags, but that is an
excessively verbose way to describe the simple use of 2048bit ElGamal,
AES256, SHA256 and 32 byte nonces. While this protocol is still
supported, most of the network has migrated to a new protocol,
ECIES-X25519-AEAD-Ratchet. This protocol combines X25519,
ChaCha20/Poly1305, and a synchronized PRNG to generate the 32 byte
nonces. Both protocols will be briefly described below.

#### ElGamal/AES+SessionTags {#op.elg}

La primera vez que un ruter quiere cifrar un mensaje para otro ruter,
estos cifran las claves para una clave de sesión AES256 con ElGamal y
adjunta la payload ya cifrado AES256/CBC después del bloque cifrado
ElGamal. Además del payload cifrado, las sección del cifrado AES
contiene el tamaño de la carga, el hash SHA256 del payload no cifrado,
así como el número de \"etiquetas de sesión\" - nonces aleatorios de 32
bits. La siguiente vez que el remitente desea cifrar un mensaje garlic
para otro ruter, en vez de de cifrar una nueva clave de sesión con
ElGamal, simplemente elijen una de las etiquetas enviadas de la sesión
anterior y cifran con AES el payload como anteriormente, usando la clave
de sesión usada con la etiqueta de la sesión, antepuesto con la misma
etiqueta de sesión. Cuando un ruter recibe un mensaje cifrado garlic,
comprueba los primeros 32 bytes para ver si coinciden con una etiqueta
de sesión disponible - si lo hace, simplemente descifran el mensaje con
AES, pero si no, descifran el primer bloque con ElGamal

Cada etiqueta de sesión puede usarse sólo una vez para evitar que
adversarios internos puedan relacionar diferentes mensajes al enviarse
estos entre los mismos ruters. El remitente de un mensaje cifrado con
etiqueta de sesión + ElGamal/AES elije cuando y cuantas etiquetas a
enviar, poniendo a disposición del que recibe suficientes etiquetas para
trabajar con un buen número de mensajes. Los mensajes Garlic pueden
detectar la llegada exitosas de las etiquetas construyendo un mensaje
adicional tipo clove (un \"mensaje de estado de entrega\") - cuando el
mensaje llega al destinatario elegido y es descifrado correctamente,
este pequeño mensaje de estado de entrega es uno de los dientes
expuestos y tiene instrucciones para el destinatario para que retorne al
remitente original (a través de un túnel de entrada, claro). Cuando el
remitente original recibe el mensaje de estado de envío, sabe que la
etiqueta de sesión incluida en el mensaje garlic ha sido enviada
exitosamente.

Las etiquetas de sesión tienen un vida muy corta, después de la cual son
descartadas y no se usan más. Además, el número almacenado de ellas por
cada clave es limitado, como también está limitado el número de claves -
si llegan demasiadas, serán descartados los mensajes nuevos o los
viejos. El remitente lleva el seguimiento de los mensajes con etiquetas
de sesión que pasan a través suyo, y si no hay comunicación suficiente
podría descartar los mensajes supuestamente enviados correctamente,
volviendo al costoso cifrado ElGamal.

#### ECIES-X25519-AEAD-Ratchet {#op.ratchet}

ElGamal/AES+SessionTags required substantial overhead in a number of
ways. CPU usage was high because ElGamal is quite slow. Bandwidth was
excessive because large numbers of session tags had to be delivered in
advance, and because ElGamal public keys are very large. Memory usage
was high due to the requirement to store large amounts of session tags.
Reliability was hampered by lost session tag delivery.

ECIES-X25519-AEAD-Ratchet was designed to address these issues. X25519
is used for key exchange. ChaCha20/Poly1305 is used for authenticated
symmetric encryption. Encryption keys are \"double ratcheted\" or
rotated periodically. Session tags are reduced from 32 bytes to 8 bytes
and are generated with a PRNG. The protocol has many similarities to the
signal protocol used in Signal and WhatsApp. This protocol provides
substantially lower overhead in CPU, RAM, and bandwidth.

The session tags are generated from a deterministic synchronized PRNG
running at both ends of the session to generate session tags and session
keys. The PRNG is a HKDF using a SHA-256 HMAC, and is seeded from the
X25519 DH result. Session tags are never transmitted in advance; they
are only included with the message. The receiver stores a limited number
of session keys, indexed by session tag. The sender does not need to
store any session tags or keys because they are not sent in advance;
they may be generated on-demand. By keeping this PRNG roughly
synchronized between the sender and recipient (the recipient precomputes
a window of the next e.g. 50 tags), the overhead of periodically
bundling a large number of tags is removed.

# El futuro {#future}

I2P\'s protocols are efficient on most platforms, including cell phones,
and secure for most threat models. However, there are several areas
which require further improvement to meet the needs of those facing
powerful state-sponsored adversaries, and to meet the threats of
continued cryptographic advances and ever-increasing computing power.
Two possible features, restricted routes and variable latency, were
propsed by jrandom in 2003. While we no longer plan to implement these
features, they are described below.

## Funcionamiento restringido del ruter {#future.restricted}

I2P es una red designada para ejecutarse sobre una red conmutada de
paquetes funcionales, usando el principio de fin a fin para ofrecer
anonimato y seguridad. Mientras que Internet ya no abraza el principio
de fin a fin (por el uso de NAT), I2P necesita tener a su disposición
una gran parte de la red - puede haber algunos pares ejecutándose en los
bordes usando ruters restringidos no accesibles, pero I2P no incluye un
algoritmo apropiado de enrutamiento para el extraño caso de que la
mayoría de los pares no sean accesibles. Aún así podría funcionar sobre
una red que utilizase dicho algoritmo.

Restricted route operation, where there are limits to what peers are
reachable directly, has several different functional and anonymity
implications, dependent upon how the restricted routes are handled. At
the most basic level, restricted routes exist when a peer is behind a
NAT or firewall which does not allow inbound connections. This was
largely addressed by integrating distributed hole punching into the
transport layer, allowing people behind most NATs and firewalls to
receive unsolicited connections without any configuration. However, this
does not limit the exposure of the peer\'s IP address to routers inside
the network, as they can simply get introduced to the peer through the
published introducer.

Beyond the functional handling of restricted routes, there are two
levels of restricted operation that can be used to limit the exposure of
one\'s IP address - using router-specific tunnels for communication, and
offering \'client routers\'. For the former, routers can either build a
new pool of tunnels or reuse their exploratory pool, publishing the
inbound gateways to some of them as part of their routerInfo in place of
their transport addresses. When a peer wants to get in touch with them,
they see those tunnel gateways in the netDb and simply send the relevant
message to them through one of the published tunnels. If the peer behind
the restricted route wants to reply, it may do so either directly (if
they are willing to expose their IP to the peer) or indirectly through
their outbound tunnels. When the routers that the peer has direct
connections to want to reach it (to forward tunnel messages, for
instance), they simply prioritize their direct connection over the
published tunnel gateway. The concept of \'client routers\' simply
extends the restricted route by not publishing any router addresses.
Such a router would not even need to publish their routerInfo in the
netDb, merely providing their self signed routerInfo to the peers that
it contacts (necessary to pass the router\'s public keys).

Existen inconvenientes para aquellos detrás de ruters restringidos ya
que participarán menos frecuentemente en los túneles de otra gente, y
los ruters a los que está conectado podrían ser capaces de descubrir
patrones en el tráfico que de otra forma no podrían verse. Por otro
lado, si el coste de exponer esos patrones es menor que el coste de de
hacer que la IP esté disponible, puede valer la pena. Esto, por
supuesto, suponiendo que los pares de los ruters con los que contacta el
ruter restringido no son hostiles - o por que la red es suficientemente
grande como para que la probabilidad de conectarse a un ruter hostil sea
muy pequela, o porque se usan pares de confianza (y quizás temporales).

Restricted routes are complex, and the overall goal has been largely
abandoned. Several related improvements have greatly reduced the need
for them. We now support UPnP to automatically open firewall ports. We
support both IPv4 and IPv6. SSU2 improved address detection, firewall
state determination, and cooperative NAT hole punching. SSU2, NTCP2, and
address compatibility checks ensure that tunnel hops can connect before
the tunnel is built. GeoIP and country identification allow us to avoid
peers in countries with restrictive firewalls. Support for \"hidden\"
routers behind those firewalls has improved. Some implementations also
support connections to peers on overlay networks such as Yggdrasil.

## Latencia variable {#future.variablelatency}

Incluso aunque la mayoría de los esfuerzos iniciales han sido para que
I2P tenga una comunicación de baja latencia, fue diseñado desde el
principio para servicios de latencia variable. Al nivel más básico, las
aplicaciones corriendo sobre I2P pueden ofrecer anonimato en
comunicaciones de media y alta latencia mientras mezcla su tráfico con
tráfico de baja latencia. Sin embargo, internamente I2P puede ofrecer
sus comunicaciones de media y alta latencia a través de su cifrado
garlic - especificando que el mensaje debe ser enviado después de un
cierto retraso, en un determinado momento, después de que hayan pasado
cierto número de mensajes o cualquier otra estrategia de mezclado. Con
el cifrado por capas sólo el ruter que hizo la petición de retraso sabrá
que el mensaje requiere alta latencia, permitiendo que el tráfico se
mezcle más con el tráfico de baja latencia. Una vez que la condición de
transmisión se cumple, el ruter que mantiene el \'clove\' (que en sí
mismo podría ser como un mensaje garlic) simplemente envía su petición -
a un ruter, a un túnel, o, lo más probable, a una destinación cliente
remota.

The goal of variable latency services requires substantial resources for
store-and-forward mechanisms to support it. These mechanisms can and are
supported in various messaging applications, such as i2p-bote. At the
network level, alternative networks such as Freenet provide these
services. We have decided not to pursue this goal at the I2P router
level.

# Sistemas similares {#similar}

La arquitectura de I2P está basada en el concepto de software orientado
a mensajes, la topología de DHTs, el cifrado y anonimato de redes de
mezcla libres, y la adaptabilidad de las redes conmutadas de paquetes.
Su valor no reside en nuevos conceptos o algoritmos, sino en la
cuidadosa combinación de resultados de investigación de trabajos y
sistemas ya existentes. Mientras que hay varios esfuerzos similares a
los que vale la pena echar un ojo, se han elegido 2 en particular para
comparaciones técnicas y funcionales - Tor y Freenet.

See also the [Network Comparisons Page]().
Note that these descriptions were written by jrandom in 2003 and may not
currently be accurate.

## Tor {#similar.tor}

*[página web](https://www.torproject.org/)*

A primera vista, Tor e I2P tienen muchas similitudes en lo que se
refiere a funcionamiento y anonimato. Aunque I2P se empezó a desarrollar
antes eramos conscientes de los esfuerzos hechos al inicio de Tor,
muchas de las lecciones aprendidas de la red onion original y ZKS fueron
integradas en el diseño de I2P. En vez de construir un sistema
centralizado y de confianza con servidores de directorios, I2P tiene su
propia base de datos de red auto organizable en la que cada par toma la
responsabilidad de acceder al perfil de otros ruters para determinar
como aprovechar los recursos disponibles. Otra diferencia básica es que
mitras I2P y Tor usan rutas ordenadas y en capas (túneles y
circuitos/streams), I2P es fundamentalmente una red conmutada de
paquetes, mientras que Tor es fundamentalmente un circuito conmutado,
permitiendo a I2P enrutar evitando congestiones y otros fallos de la red
transparentemente , operar en vías redundantes, y hacer balance de carga
de los datos a través de los recursos disponibles. Mientras que Tor
ofrece una funcionalidad tan útil como el outproxy ofreciendo el
descubrimiento y selección de outproxy integrado, I2P deja esas
decisiones sobre la capa de aplicación a las aplicaciones ejecutándose
sobre I2P - de hecho, I2P incluso ha exteriorizado la librería de
streaming tipo TCP a la capa de aplicación, permitiendo a los
desarrolladores el experimentar con diferentes estrategias, usando el
conocimiento específico de dominio para ofrecer mejores rendimientos.

Desde el punto de vista del anonimato, cuando comparamos el núcleo de
las redes hay muchas similaridades entre ellos. Pero hay unas cuantas
diferencias claves. Cuando se trata de lidiar con adversario interno o
varios adversarios externos observando los propios flujos de datos, los
túneles simples de I2P exponen la mitad de información en el tráfico de
lo que exponen los circuitos dobles de Tor - una petición y respuesta
HTTP seguirían el mismo camino en Tor, mientras que I2P el paquete que
hace la consulta iría a través de uno o más túneles y el paquete con la
respuesta regresarían a través de otro o más túneles de entrada
diferentes. Mientras que la selección del orden y estrategias por parte
del par deberían ser suficientes para enfrentarse a los ataques de
predecesor, podríamos simplemente construir un túnel de entrada y de
salida a través de los mismos ruters.

Otro problema para el anonimato aparece en el uso por parte de Tor de la
creación telescópica de túnel, un simple contador y medidor de tiempo de
los paquetes que pasan a través de un nodo enemigo puede obtener
información estadística sobre la posición de la víctima en el circuito.
La creación unidireccional para cada mensaje en I2P hace que esta
información no sea expuesta. Ocultar la posición de un túnel es
importante, ya que un adversario podría montar una serie de potentes
ataques como el de predecesores, intersección y confirmación de tráfico.

En conjunto, Tor e I2P se complementan el uno al otro - Tor funciona
ofreciendo outproxing a Internet de alta velocidad y anónimo, mientras
que I2P ofrece una red resistente y descentralizada dentro de sí mismo.
En teoría se pueden usar los 2 para obtener los mismos fines, pero dados
los limitados recursos de desarrollo, ambos tienen sus ventajas e
inconvenientes. Los desarrolladores de I2P han considerado los pasos
necesarios para modificar Tor para para la mejora del diseño de I2P,
pero preocupaciones sobre la viabilidad de Tor con bajo escasos recursos
sugiere que la arquitectura de enrutamiento de paquetes de I2P será
capaz de funcionar más eficientemente con recursos escasos.

## Freenet {#similar.freenet}

*[página web](http://www.freenetproject.org/)*

Freenet jugó un rol importante en los primeros pasos del diseño de I2P -
mostrando pruebas de la viabilidad de una comunidad vibrante
completamente dentro de la red, mostrando que los peligros inherentes de
los outproxies podían ser evitados. La primera semilla de I2P comenzó
como el remplazo de una capa de comunicación para Freenet, al intentar
extraer la complejidad de una comunicación de punto a punto segura y
anónima de las complicaciones del almacenamiento distribuido resistente
a la censura. Aunque la final, algunos de los problemas de escalabilidad
y anonimato inherentes a los algoritmos de Freenet dejó claro que
debería enfocarse I2P para proveer una capa de comunicación anónima por
sí misma en vez de ser un componente de Freenet. A través de los años,
los desarrolladores de Freenet se han dado cuenta de las debilidades del
viejo diseño, provocando que sugiriese la necesidad de una capa de \"pre
mezcla\" para ofrecer el suficiente anonimato. En otras palabras,
Freenet debe ejecutarse sobre una mixnet como I2P o Tor, con \"nodos
cliente\" solicitando y publicando datos a través de la mixnet a los
\"nodos servidores\" los cuales entonces almacenan los datos de acuerdo
con la heurística de los algoritmos de almacenamiento de datos
distribuidos de Freenet.

Las funcionalidades de Freenet son muy complementarias a las de I2P, ya
que Freenet provee nativamente muchas herramientas para operar en
sistemas de media y alta latencia, mientras que I2P provee nativamente
una red de baja latencia adecuada para ofrecer anonimato. La lógica para
separar la mixnet de los datos distribuidos resistentes a censura, son
muy evidentes desde la perspectiva del anonimato, seguridad y de la
asignación de los recursos, con lo que esperamos que el equipo de
Freenet ponga sus esfuerzos en esta dirección, aunque sea reutilizando
(o ayudando a mejorar, si es necesario) las redes existentes como I2P y
Tor.

# Appendix A: Application layer {#app}

En sí, I2p no hace mucho - simplemente envía mensajes a destinaciones
remotas y recibe mensajes hacia destinaciones locales - la mayoría del
trabajo interesante es sobre las capas que hay sobre I2P. Por sí mismo
I2P puede verse como una capa de IP anónima y segura, y la [librería
streaming](#app.streaming) incluida como una implementación de una capa
TCP segura y anónima sobre I2P. Más allá de esto, el
[I2PTunnel](#app.i2ptunnel) expone un sistema genérico TCP para entrar
dentro o salir de la red I2P, más una gran variedad de aplicaciones para
proveer más funcionalidades a los usuarios finales.

## Librería de streaming {#app.streaming}

La librería de streaming de I2P puede verse como un interfaz genérico de
streaming (reflejando sockets TCP), y la implementación soporta el
[protocolo sliding
window](http://en.wikipedia.org/wiki/Sliding_Window_Protocol) con varias
optimizaciones, para tener en cuenta los altos retardos en I2P. Los
streams individuales pueden ajustar el tamaño máximo de paquetes y otras
opciones, aunque la compresión por defecto de 4KB parece una
compensación razonable entre el coste de ancho de banda de reenviar los
mensajes perdidos y la latencia de múltiples mensajes.

Además, considerando el alto coste de un mensaje, la librería de
streaming para programar y enviar mensajes ha sido optimizada para
permitir que los mensajes individuales enviados contengan tanta
información como esté disponible. Por ejemplo, una pequeña transacción
HTTP enviada a través de la librería de streaming puede ser completada
en una simple vuelta - el primer mensaje empaqueta a SYN, FIN y un
pequeña carga (normalmente encaja una solicitud HTTP) y la respuesta
empaqueta el SYN, FIN, ACK y una pequeña carga (muchas respuestas HTTP
encajan). Mientras que el ACK adicional debe ser transmitido para
decirle al servido HTTP que el SYN/FIN/ACK ha llegado, el proxy HTTP
local puede enviar al navegador inmediatamente la respuesta completa.

En conjunto, la librería de streaming se parece mucho a una abstracción
de TCP, con sus sliding windows, algoritmos de control de congestión
(inicio lento e impedimento de congestiones), y comportamiento general
de paquetes (ACK, SYN, FIN, RST, etc).

## Naming library and address book {#app.naming}

*For more information see the [Naming and Address
Book]() page.*

*Developed by: *

Los nombres de dominio en I2P han sido debatidos a menudo desde el
principio, con defensores para todos los tipos de posibilidades. Sin
embargo, y dada la necesidad de comunicaciones seguras y
descentralizadas, el sistema tradicional al estilo DNS no es viable, al
igual que no lo son los sistemas de votos en los que la \"mayoría
manda\". Por el contrario, I2P incluye una librería genérica para
nombres de dominios y una implementación básica diseñados para trabajar
con nombres locales y mapearlos, así como un pluguin opcional llamado
\"addressbook\", lista de direcciones. La lista de direcciones es un
sistema de dominios distribuido, basado en un sistema de confianza
seguro basado en web y legible, sólo sacrificando el hecho de que los
dominios puedan ser leídos por los humanos globalmente para ser sólo
entendibles localmente. Ya que todos los mensajes en I2P están dirigidos
criptográficamente por su destinación, diferentes personas pueden tener
entradas en la lista de direcciones para \"Alice\", pero refiriéndose a
destinaciones diferentes. La gente puede descubrir nuevos nombres
importando lista de direcciones publicadas por pares específicos de su
web de confianza, añadiendo estas entradas a través de una tercera
parte, o (si alguien organiza listas de direcciones usando sistema de
registro tipo el primero que entra el primero es servido) la gente puede
escoger tratar estas lista de direcciones como servidores de dominio,
emulando los DNS tradicionales.

I2P no recomienda el uso de servicios tipo DNS, ya que el daño hecho por
una web maliciosas puede ser enorme - una destinación insegura no tiene
valor. DNSsec sigue apoyándose en autoridades certificadas, mientras que
con I2P las solicitudes a una destinación no pueden ser interceptadas o
la respuesta suplantada ya que están cifradas con la clave pública de la
destinación, y una destinación en sí misma no es más que un par de
claves y un certificado. Por otra parte, los sistemas del tipo DNS
permiten que cualquiera de los servidores en el camino de búsqueda pueda
montar ataques de denegación de servicio o ataques de suplantación.
Añadiendo sobre un certificado autentificándose la respuesta firmada por
alguna autoridad centralizada de certificados, podría solucionar muchos
de los problemas con los servidores de dominio hostiles, pero lo dejaría
abierto a ataques de respuesta y a ataques de autoridad certificada
hostil.

El sistema de dominios por votos también es peligroso, sobre todo por la
efectividad de los ataques Sybil en sistemas anónimos- el atacante puede
simplemente crear un número aleatorio muy grande de pares y \"votar\"
con cada uno para apoderarse de un dominio cualquiera. Existen métodos
que pueden usarse para hacer que crear una identidad no sea gratis, pero
a medida que la red crece la carga que se necesita para contactar a
todos y hacer votación online es enorme, o si no hace falta la red
completa, se podrían encontrar otras soluciones.

Aún así, al igual que con Internet, I2P mantiene el diseño y
funcionamiento de un sistema de dominios aparte de la capa de
comunicación (como IP). La librería de dominios incluye un interfaz
simple de servicio al cual puede conectarse cualquier sistema de
dominios, permitiendo a los usuarios finales elegir qué tipo de sistema
de dominios prefieren.

## I2PTunnel {#app.i2ptunnel}

*Developed by: *

I2pTunnel es probablemente la aplicación más versátil y popular de I2P,
permitiendo \'proxificar\' dentro y fuera de la red I2P. Se puede ver
I2PTunnel como cuatro aplicaciones de proxy diferentes - un cliente que
recibe conexiones TCP de entrada y las envía a una destinación I2P, un
\"cliente http\" (\"eeproxy\") que funciona con un proxy HTTP y envía
las peticiones a la destinación I2P apropiada (Después de preguntar a un
servicio de dominios si es necesario), un \"servidor\" el cual recibe
conexiones de entrada de I2P en una destinación y los envía a un
host+puerto TCP dado, y un \"servidor http\" el cual amplía el
\"servidor\" pasando las solicitudes y respuestas HTTP para permitir un
funcionamiento seguro. Hay una aplicación adicional \"socksclient\",
pero su uso no se fomenta por razones mencionadas anteriormente.

En sí mismo I2P no es una red creada para outproxy - los problemas de
seguridad de una red que envía datos dentro y fuera de esta han hecho
que el diseño de I2P se haya centrado en crear una red anónima con
capacidad para cubrir las necesidades de los usuarios sin necesitar
recursos externos. Aún así la aplicación de \"httpclient\" I2PTunnel
ofrece la posibilidad de \'outproxying\' - si el nombre de dominio no
termina en .i2p, elije una destinación aleatoria de una lista de
outproxies para el usuario dado y se lo envía. Estas destinaciones son
simplemente \"servidores\" I2PTunnels ejecutados por voluntarios que han
decidido explícitamente ejecutar outproxies - nadie es un outproxy por
defecto, y ejecutar un outproxy no hace que nadie pase automáticamente a
través de su ruter. Aunque los outproxys tienen debilidades inherentes,
ofrecen un servicio para I2P que tiene un modelo de seguridad que puede
ser suficiente para algunos usuarios.

I2PTunnel es el que permite el funcionamiento de la mayoría de las
aplicaciones. Un \"servidor http\" apuntando a un servidor web permite a
cualquiera tener su propia web anónima ( o \"eepsite\") - un servidor
web se incluye por defecto en I2P para este propósito, pero se puede
utilizar cualquier servidor web. Cualquiera puede ejecutar un
\"cliente\" apuntando a cualquiera de los servidores IRC, todos ellos
ejecutan un \"servidor\" apuntando a su demonio IRCd local y
comunicándose entre servidores IRCd a través de sus propios túneles
\"cliente\". Los usuarios finales también tienen túneles clientes
apuntando a las destinaciones POP3 y SMTP de [I2Pmail](#app.i2pmail) (
que realmente sólo son simples instancias \"servidores\" apuntando a
servidores POP3 y SMTP), también hay túneles apuntando al servidor CVS
de I2P, permitiendo el desarrollo anónimo. Incluso a veces hay gente que
ha ejecutado proxies \"clientes\" para acceder instancias de
\"servidores\" apuntando a servidores NNTP.

## I2PSnark {#app.i2psnark}

*I2Psnark es programado por jrandom y otros, portado desde el cliente
[Snark](http://www.klomp.org/snark/) de
[mjw](http://www.klomp.org/mark/).*

Incluido en la instalación de I2P, I2PSnark ofrece un cliente anónimo de
BitTorrent con capacidades para multitorrents, mostrando todas sus
funcionaliudades a través de in unterfaz web HTML.

## I2Pmail/susimail {#app.i2pmail}

*Developed by: *

I2Pmail is more a service than an application - postman offers both
internal and external email with POP3 and SMTP service through I2PTunnel
instances accessing a series of components developed with mastiejaner,
allowing people to use their preferred mail clients to send and receive
mail pseudonymously. However, as most mail clients expose substantial
identifying information, I2P bundles susi23\'s web based susimail client
which has been built specifically with I2P\'s anonymity needs in mind.
The I2Pmail/mail.i2p service offers transparent virus filtering as well
as denial of service prevention with hashcash augmented quotas. In
addition, each user has control of their batching strategy prior to
delivery through the mail.i2p outproxies, which are separate from the
mail.i2p SMTP and POP3 servers - both the outproxies and inproxies
communicate with the mail.i2p SMTP and POP3 servers through I2P itself,
so compromising those non-anonymous locations does not give access to
the mail accounts or activity patterns of the user.


