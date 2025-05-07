 La base de datos
de la red 2025-03 0.9.65 

## Información general

La netDb de I2P es una base de datos distribuida especializada que
contiene 2 tipos de datos - información de contacto del ruter y la
información de contacto de la destinación. Cada parte de los datos es
firmada por la parte apropiada y verificada por cualquiera que las use o
las almacene. Además, los datos tienen información cambiante,
permitiendo que las entradas irrelevantes sean desechadas, que nuevas
entradas puedan reemplazar las antiguas y protección contra cierto tipos
de ataques.

La netDb se distribuye con una técnica simple llamada \"FloodFill\",
donde un subconjunto de ruters, llamados ruters \"floodfill\", mantienen
la base de datos distribuida.

## RouterInfo {#routerInfo}

Cuando un ruter I2P quiere contactar con otro ruter, necesitan conocer
algunas partes claves de los datos - estas partes están agrupadas y
firmadas por el ruter dentro de una estructura llamda \"RouterInfo\",
que es distribuida con el hash SHA256 de la identidad del ruter como una
clave de cifrado. La estructura en sí misma contiene:

- The router\'s identity (an encryption key, a signing key, and a
 certificate)
- The contact addresses at which it can be reached
- Cuándo fue publicada.
- Un conjunto de opciones de texto arbitrarias
- La firma de lo anterior, generada por la clave de firmado de la
 identidad.

### Opciones esperadas

Las siguientes opciones de texto, que aunque no son requeridas
explicitamente se espera que esten presentes:

**caps** (Datos de capacidad - usados para indicar si se participa como
floodfill, ancho de banda aproximado y la accesibilidad observada.)

**D**: Medium congestion (as of release 0.9.58)

**E**: High congestion (as of release 0.9.58)

**f**: Inundación (floodfill)

**G**: Rejecting all tunnels (as of release 0.9.58)

**H**: Oculto

**K**: Estos valores pueden ser usados por otros ruters para tomar
decisiones básicas. ¿Deberíamos conectar con este ruter? ¿Deberíamos
intentar rutar un túnel a través de ese ruter? En particular, la opción
de la capacidad de ancho de banda sólo se usa para determinar cuando el
ruter cumple un umbral para poder rutar túneles. Por encima del umbral
mínimo el ancho de banda anunciado no es usado o confiable en ningún
sitio del ruter, excepto para mostrar en el interfaz del usuario para
depurar y para el análisis de tráfico.

Valid NetID numbers:

Usage

NetID Number

Reserved

0

Reserved

1

Current Network (default)

2

Reserved Future Networks

3 - 15

Forks and Test Networks

16 - 254

Reserved

255

### Opciones adicionales

Additional text options include a small number of statistics about the
router\'s health, which are aggregated by sites such as [](http:///) for network performance analysis
and debugging. These statistics were chosen to provide data crucial to
the developers, such as tunnel build success rates, while balancing the
need for such data with the side-effects that could result from
revealing this data. Current statistics are limited to:

- Tasas de creación de túneles exploratorios exitosos, rechazados y
 con periodo de espera agotado
- Media del número de túneles participantes en 1 hora

These are optional, but if included, help analysis of network-wide
performance. As of API 0.9.58, these statistics are simplified and
standardized, as follows:

- Option keys are stat\_(statname).(statperiod)
- Option values are \';\' -separated
- Stats for event counts or normalized percentages use the 4th value;
 the first three values are unused but must be present
- Stats for average values use the 1st value, and no \';\' separator
 is required
- For equal weighting of all routers in stats analysis, and for
 additional anonymity, routers should include these stats only after
 an uptime of one hour or more, and only one time every 16 times that
 the RI is published.

Example:

 stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
 stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
 stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
 stat_tunnel.participatingTunnels.60m = 289.20

Floodfill routers may publish additional data on the number of entries
in their network database. These are optional, but if included, help
analysis of network-wide performance.

The following two options should be included by floodfill routers in
every published RI:

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

Example:

 netdb.knownLeaseSets = 158
 netdb.knownRouters = 11374

The data published can be seen in the router\'s user interface, but is
not used or trusted by any other router.

### Opciones de familia

Desde la versión 0.9.24, los routers I2P pueden declarar que son parte
de una \"familia\", operada por la misma entidad. No se usarán varios
routers I2P de la misma familia en un único túnel.

Las opciones de familia son:

- **family** (El nombre de la familia)
- **family.key** The signature type code of the family\'s [Signing
 Public
 Key](#type_SigningPublicKey)
 (in ASCII digits) concatenated with \':\' concatenated with the
 Signing Public Key in base 64
- **family.sig** The signature of ((family name in UTF-8) concatenated
 with (32 byte router hash)) in base 64

### Caducidad de RouterInfo

RouterInfo no tienen tiempo de caducidad. Cada ruter puede mantener su
propia política local a la hora de controlar la frecuencia de las
búsquedas de RouterInfo y el uso de memoria y espacio en le disco. En la
implementación actual, estas son las políticas generales:

- No existe vencimiento durante la primera hora encendido, ya que los
 datos almacenados podrían ser viejos.
- No existe vencimiento si hay 25 o menos menos routerInfos
- Según aumenta el número de RouterInfos, el tiempo de espiración
 disminuye, en el intento de mantener un número razonable de
 RouterInfos . El número de espiración con menos de 120 ruters es de
 72 horas, mientras que el tiempo de caducidad con 300 ruters es de
 30 horas.
- RouterInfos containing [SSU]() introducers
 expire in about an hour, as the introducer list expires in about
 that time.
- Los FloodFills tienen un tiempo de expiración corto (1 hora) para
 todos los RoutersInfos locales, ya que como RoutersInfos válidos
 serán re publicados.

### Almacenamiento persistente de RouterInfo

Los RoutersInfos son periodicamente escritos en el disco duro para que
estén disponibles después de reiniciar.

It may be desirable to persistently store Meta LeaseSets with long
expirations. This is implementation-dependent.

### Consulte también

[Especifiaciones de
RouterInfo](#struct_RouterInfo)

[Javadoc de
RouterInfo](http:///net/i2p/data/router/RouterInfo.html)

## LeaseSet {#leaseSet}

La segunda parte de los datos distribuidos en la netDb es un
\"LeaseSet\" - el cual documenta un conjunto de **puntos de entradas de
túnel (leases o contratos)** para una destinación de un cliente en
particular. Cada uno de estos leases especifica la siguiente
información:

- La puerta de salida de túnel del ruter (especificando su identidad)
- El ID del túnel con los que el túnel envía mensajes (un número de 4
 bytes)
- Cuando expirará ese túnel.

El propio LeaseSet es almacenado en la netDb bajo la clave derivada del
hash SHA256 de la destinación. One exception is for Encrypted LeaseSets
(LS2), as of release 0.9.38. The SHA256 of the type byte (3) followed by
the blinded public key is used for the DHT key, and then rotated as
usual. See the Kademlia Closeness Metric section below.

Además de estos leases, el LeaseSet incluye:

- The destination itself (an encryption key, a signing key and a
 certificate)
- Una clave pública de cifrado adicional: usada para el cifrado de fin
 a fin de los mensajes garlic
- Una clave de firma pública adicional: para la revocación del
 LeaseSet, pero actualmente no se usa.
- La firma de toda la información del LeaseSet, para asegurarse de que
 la Destinación publicó ese LeaseSet.

[Especificaciones del
Lease](#struct_Lease)\
[Especificaciones del
LeaseSet](#struct_LeaseSet)

[Javadoc del
Lease](http:///net/i2p/data/Lease.html)\
[Javadoc del
LeaseSet](http:///net/i2p/data/LeaseSet.html)

As of release 0.9.38, three new types of LeaseSets are defined;
LeaseSet2, MetaLeaseSet, and EncryptedLeaseSet. See below.

### LeaseSets no publicados {#unpublished}

A LeaseSet for a destination used only for outgoing connections is
*unpublished*. It is never sent for publication to a floodfill router.
\"Client\" tunnels, such as those for web browsing and IRC clients, are
unpublished. Servers will still be able to send messages back to those
unpublished destinations, because of [I2NP storage messages](#lsp).

### LeaseSets Revocados {#revoked}

Un LeaseSet puede ser *revocado* publicando un nuevo LeaseSet sin
leases. Las revocaciones tienen que ser firmadas por la clave de firmado
adicional del LeaseSet. La revocación no está completamente
implementada, y no está claro si tiene algún uso práctico. Este es el
único uso planeado para la clave de firmado, por lo cual no se usa.

### LeaseSet2 (LS2) {#ls2}

As of release 0.9.38, floodfills support a new LeaseSet2 structure. This
structure is very similar to the old LeaseSet structure, and serves the
same purpose. The new structure provides the flexibility required to
support new encryption types, multiple encryption types, options,
offline signing keys, and other features. See proposal 123 for details.

### Meta LeaseSet (LS2) {#meta}

As of release 0.9.38, floodfills support a new Meta LeaseSet structure.
This structure provides a tree-like structure in the DHT, to refer to
other LeaseSets. Using Meta LeaseSets, a site may implement large
multihomed services, where several different Destinations are used to
provide a common service. The entries in a Meta LeaseSet are
Destinations or other Meta LeaseSets, and may have long expirations, up
to 18.2 hours. Using this facility, it should be possible to run
hundreds or thousands of Destinations hosting a common service. See
proposal 123 for details.

### LeaseSets Cifrados (LS1) {#encrypted}

This section describes the old, insecure method of encrypting LeaseSets
using a fixed symmetric key. See below for the LS2 version of Encrypted
LeaseSets.

En un LeaseSet *cifrado*, todos los leases (túneles) están cifrados con
una clave aparte. Los leases sólo pueden ser decodificados, y por tanto
el destino sólo puede ser contactado, por aquellos con la clave. No hay
ninguna señal ni otro tipo de indicación directa de que el LeaseSet esté
cifrado. Los LeaseSets cifrados no son ampliamente usados, y es un
asunto a trabajar en el futuro investigar si la interfaz de usuaro y la
implementación de LeaseSets cifrados se podría mejorar.

### LeaseSets Cifrados (LS2) {#encrypted2}

As of release 0.9.38, floodfills support a new, EncryptedLeaseSet
structure. The Destination is hidden, and only a blinded public key and
an expiration are visible to the floodfill. Only those that have the
full Destination may decrypt the structure. The structure is stored at a
DHT location based on the hash of the blinded public key, not the hash
of the Destination. See proposal 123 for details.

### Expiración del LeaseSet

For regular LeaseSets, the expiration is the time of the latest
expiration of its leases. For the new LeaseSet2 data structures, the
expiration is specified in the header. For LeaseSet2, the expiration
should match the latest expiration of its leases. For EncryptedLeaseSet
and MetaLeaseSet, the expiration may vary, and maximum expiration may be
enforced, to be determined.

### Almacenamiento persistente del LeaseSet

No persistent storage of LeaseSet data is required, since they expire so
quickly. Howewver, persistent storage of EncryptedLeaseSet and
MetaLeaseSet data with long expirations may be advisable.

### Encryption Key Selection (LS2) {#ls2keys}

LeaseSet2 may contain multiple encryption keys. The keys are in order of
server preference, most-preferred first. Default client behavior is to
select the first key with a supported encryption type. Clients may use
other selection algorithms based on encryption support, relative
performance, and other factors.

## Secuencia de arranque {#bootstrap}

La netDb (base de datos de red) es descentralizada, aún así necesita al
menos una referencia a un par (peer) para que el proceso de integración
le una a la red. Esto se consigue \"resembrando\" el router I2P con la
RouterInfo de un par activo - específicamente, obteniendo su fichero
`routerInfo-$hash.dat` y almacenándolo en su directorio `netDb/`.
Cualquiera puede proporcionarle estos ficheros - incluso usted puede
proporcionárselos a otros exponiendo su propio directorio netDb. Para
simplificar el proceso, hay voluntarios que publican sus directorios
netDb (o un subconjunto) en Internet (fuera de I2P), y las URLs de estos
directorios están codificadas dentro de la aplicación I2P. Cuando el
router I2P arranca por primera vez, descarga automáticamente el fichero
de una de estas URLs seleccionada de forma aleatoria.

## Inundación (floodfill) {#floodfill}

The floodfill netDb is a simple distributed storage mechanism. The
storage algorithm is simple: send the data to the closest peer that has
advertised itself as a floodfill router. When the peer in the floodfill
netDb receives a netDb store from a peer not in the floodfill netDb,
they send it to a subset of the floodfill netDb-peers. The peers
selected are the ones closest (according to the [XOR-metric](#kad)) to a
specific key.

Determinar quien es parte del floodfill netDb es algo trivial - se
muestra en el routerinfo publicado de cada ruter como una capacidad.

Los flodfill no tienen inguna autoridad central y no forman ningún
\"consenso\" - sólo implementan una capa DHT.

### Convertirse en un ruter floodfill {#opt-in}

Al contrario que en Tor, donde los servidores están incluidos y son de
confianza, y operados por identidades conocidas, los miembros de los
pares floodfill de I2P no necesitas ser de confianza, y cambian con el
tiempo.

Para incrementar la fiabilidad de la netDb, y minimizar el impacto del
tráfico de la netDb en un ruter, floodfill solo está activo por defecto
en los routers configurados para compartir un gran ancho de banda. Los
routers con límites grandes de compartición de ancho de banda (lo que se
puede configurar manualmente, ya que por defecto es mucho más bajo)
presuntamente tienen conexiones de baja latencia, y es más probable que
estén disponibles 24/7. El ancho de banda mínimo a compartir para
convertirse en floodfill es de 128 KBytes/sec.

Además, un ruter debe pasar varios pruebas adiciones para comprobar su
salud (tiempo de espera de los mensajes de salida, retraso de los
trabajos, etc) antes de que se active automáticamente como un floodfill.

Con las reglas actuales para la aceptación automática, aproximadamente
el 6% de los routers en la red son routers floodfill.

Mientras que algunos pares se configuran manualmente para ser floodfill,
otros son simplemente ruters con gran ancho de banda que son
automáticamente convertidos en floodfill cuando el número de pares
floodfill baja de un límite. Esto evita el daño por un tiempo largo
cuando se pierden la mayoría de los ruters floodfill a causa de un
ataque. A su vez, estos pares dejarán de ser floodfill cuando ya haya
suficientes floodfills activos.

### El papel del ruter floodfill

Los únicos servicios que tienen de más los ruters floodfill que no
tienen los ruters no floodfill es aceptar almacenamientos en la netDb y
el responder a las solicitudes de la netDb. Ya que normalmente tienen un
gran ancho de banda, es más usual que participen en un gran número de
túneles (por ejemplo como un \"relay\" para otros), pero esto no está
relacionado directamente con sus servicios distribuidos de la base de
datos.

## Medida de cercanía Kademlia {#kad}

The netDb uses a simple Kademlia-style XOR metric to determine
closeness. To create a Kademlia key, the SHA256 hash of the
RouterIdentity or Destination is computed. One exception is for
Encrypted LeaseSets (LS2), as of release 0.9.38. The SHA256 of the type
byte (3) followed by the blinded public key is used for the DHT key, and
then rotated as usual.

A modification to this algorithm is done to increase the costs of [Sybil
attacks](#sybil-partial). Instead of the SHA256 hash of the key being
looked up of stored, the SHA256 hash is taken of the 32-byte binary
search key appended with the UTC date represented as an 8-byte ASCII
string yyyyMMdd, i.e. SHA256(key + yyyyMMdd). This is called the
\"routing key\", and it changes every day at midnight UTC. Only the
search key is modified in this way, not the floodfill router hashes. The
daily transformation of the DHT is sometimes called \"keyspace
rotation\", although it isn\'t strictly a rotation.

Las claves de enrutado nunca se envían por-el-cable en ninguno de los
mensajes I2NP, sólo se usan localmente para determinar la distancia.

## Network Database Segmentation - Sub-Databases {#segmentation}

Traditionally Kademlia-style DHT\'s are not concerned with preserving
the unlinkability of information stored on any particular node in the
DHT. For example, a piece of information may be stored to one node in
the DHT, then requested back from that node unconditionally. Within I2P
and using the netDb, this is not the case, information stored in the DHT
may only be shared under certain known circumstances where it is
\"safe\" to do so. This is to prevent a class of attacks where a
malicious actor can try to associate a client tunnel with a router by
sending a store to a client tunnel, then requesting it back directly
from the suspected \"Host\" of the client tunnel.

### Segmentation Structure

I2P routers can implement effective defenses against the attack class
provided a few conditions are met. A network database implementation
should be able to keep track of whether a database entry was recieved
down a client tunnel or directly. If it was recieved down a client
tunnel, then it should also keep track of which client tunnel it was
recieved through, using the client\'s local destination. If the entry
was recieved down multiple client tunnels, then the netDb should keep
track of all destinations where the entry was observed. It should also
keep track of whether an entry was recieved as a reply to a lookup, or
as a store.

In both the Java and C++ implementations, this achieved by using a
single \"Main\" netDb for direct lookups and floodfill operations first.
This main netDb exists in the router context. Then, each client is given
it\'s own version of the netDb, which is used to capture database
entries sent to client tunnels and respond to lookups sent down client
tunnels. We call these \"Client Network Databases\" or \"Sub-Databases\"
and they exist in the client context. The netDb operated by the client
exists for the lifetime of the client only and contains only entries
that are communicated with the client\'s tunnels. This makes it
impossible for entries sent down client tunnels to overlap with entries
sent directly to the router.

Additionally, each netDb needs to be able to remember if a database
entry was recieved because it was sent to one of our destinations, or
because it was requested by us as part of a lookup. If a database entry
it was recieved as a store, as in some other router sent it to us, then
a netDb should respond to requests for the entry when another router
looks up the key. However, if it was recieved as a reply to a query,
then the netDb should only reply to a query for the entry if the entry
had already been stored to the same destination. A client should never
answer queries with an entry from the main netDb, only it\'s own client
network database.

These strategies should be taken and used combined so that both are
applied. In combination, they \"Segment\" the netDb and secure it
against attacks.

## Mecanismos de almacenaje, verificación y bloqueo {#delivery}

### Almacenamiento del RouterInfo en los pares

[I2NP]() DatabaseStoreMessages containing the
local RouterInfo are exchanged with peers as a part of the
initialization of a [NTCP]() or
[SSU]() transport connection.

### Almacenamiento del LeaseSet en los pares {#lsp}

[I2NP]() DatabaseStoreMessages containing the
local LeaseSet are periodically exchanged with peers by bundling them in
a garlic message along with normal traffic from the related Destination.
This allows an initial response, and later responses, to be sent to an
appropriate Lease, without requiring any LeaseSet lookups, or requiring
the communicating Destinations to have published LeaseSets at all.

### Floodfill Selection

El DatabaseStoreMessage (mensaje de almacén de base de datos) debe
enviarse al router de inundación (\`floodfill\`, extienden la red I2P al
desplegarse en inundación portando la base de datos distribuida netDb)
más cercano al lugar donde se esté guardando la clave de enrutado actual
para el RouterInfo o el LeaseSet. Actualmente el router floodfill más
cercano se obtiene mediante una búsqueda en la base de datos local.
Incluso si ese router floodfill no es en realidad el más cercano, lo
inundará \"hacia si\" enviándo el mensaje a otros múltiples routers de
inundación. Esto proporciona un alto grado de tolerencia a fallos.

En el Kademlia tradicional, un par (\`peer\`) haría una búsqueda
\"find-closest\" (encuentra al más cercano) antes de insertar un
elemento en la DHT (tabla de hash dinámica) hacia el objetivo más
cercano. Como la operación de verificación tenderá a descubrir los
routers floodfills más cercanos si están presentes, un router mejorará
rápidamente su conocimiento del \"vecindario\" de la DHT para el
RouterInfo (información para contactar routers) y los LeaseSets
(información para contactar destinos) que publica regularmente. Aunque
I2NP no define un mensaje \"find-closest\", si fuera necesario un router
simplemente podría hacer una búsqueda iterativa de la clave con el bit
menos significativo invertido (es decir, la clave \^ 0x01) hasta que no
se reciban pares más cercanos en los DatabaseSearchReplyMessages
(mensajes de respuesta de búsqueda de la base de datos). Esto asegura
que se encontrará al verdadero par más cercano incluso si un par
más-distante tiene el elemento netDb.

### Almacenamiento de RouterInfo en los Floodfills

A router publishes its own RouterInfo by directly connecting to a
floodfill router and sending it a [I2NP]()
DatabaseStoreMessage with a nonzero Reply Token. The message is not
end-to-end garlic encrypted, as this is a direct connection, so there
are no intervening routers (and no need to hide this data anyway). The
floodfill router replies with a [I2NP]()
DeliveryStatusMessage, with the Message ID set to the value of the Reply
Token.

In some circumstances, a router may also send the RouterInfo
DatabaseStoreMessage out an exploratory tunnel; for example, due to
connection limits, connection incompatibility, or a desire to hide the
actual IP from the floodfill. The floodfill may not accept such a store
in times of overload or based on other criteria; whether to explicitly
declare non-direct store of a RouterInfo illegal is a topic for further
study.

### Almacenamiento de LeaseSet en los Floodfills

El almacenamiento de los LeaseSets es mucho más sensible que el de los
RouterInfos, ya que un ruter debe de tener cuidad de que el LeaseSet no
pueda ser asociado con el ruter.

A router publishes a local LeaseSet by sending a
[I2NP]() DatabaseStoreMessage with a nonzero Reply
Token over an outbound client tunnel for that Destination. The message
is end-to-end garlic encrypted using the Destination\'s Session Key
Manager, to hide the message from the tunnel\'s outbound endpoint. The
floodfill router replies with a [I2NP]()
DeliveryStatusMessage, with the Message ID set to the value of the Reply
Token. This message is sent back to one of the client\'s inbound
tunnels.

### Inundación

Like any router, a floodfill uses various criteria to validate the
LeaseSet or RouterInfo before storing it locally. These criteria may be
adaptive and dependent on current conditions including current load,
netdb size, and other factors. All validation must be done before
flooding.

After a floodfill router receives a DatabaseStoreMessage containing a
valid RouterInfo or LeaseSet which is newer than that previously stored
in its local NetDb, it \"floods\" it. To flood a NetDb entry, it looks
up several (currently ) floodfill routers closest to the
routing key of the NetDb entry. (The routing key is the SHA256 Hash of
the RouterIdentity or Destination with the date (yyyyMMdd) appended.) By
flooding to those closest to the key, not closest to itself, the
floodfill ensures that the storage gets to the right place, even if the
storing router did not have good knowledge of the DHT \"neighborhood\"
for the routing key.

The floodfill then directly connects to each of those peers and sends it
a [I2NP]() DatabaseStoreMessage with a zero Reply
Token. The message is not end-to-end garlic encrypted, as this is a
direct connection, so there are no intervening routers (and no need to
hide this data anyway). The other routers do not reply or re-flood, as
the Reply Token is zero.

Floodfills must not flood via tunnels; the DatabaseStoreMessage must be
sent over a direct connection.

Floodfills must never flood an expired LeaseSet or a RouterInfo
published more than one hour ago.

### Búsquedas de RouterInfo y LeaseSet {#lookup}

The [I2NP]() DatabaseLookupMessage is used to
request a netdb entry from a floodfill router. Lookups are sent out one
of the router\'s outbound exploratory tunnels. The replies are specified
to return via one of the router\'s inbound exploratory tunnels.

Las consultas generalmente se envían a los dos routers floodfill
\"buenos\" (en los que la conexión no falla) más próximos a la clave
solicitada, en paralelo.

If the key is found locally by the floodfill router, it responds with a
[I2NP]() DatabaseStoreMessage. If the key is not
found locally by the floodfill router, it responds with a
[I2NP]() DatabaseSearchReplyMessage containing a
list of other floodfill routers close to the key.

Las consultas de LeaseSet (información para contactar destinos) están
cifradas extremo-a-extremo con garlic (ajo) desde la versión 0.9.5. Las
consultas de RouterInfo (información para contactar routers) no están
cifradas y por tanto son vulnerables a espionaje por el extremo exterior
(outbound endpoint, OBEP) del túnel cliente. Esto es debido a lo caro
del cifrado ElGamal. El cifrado de la consulta RouterInfo puede que sea
habilitado en una futura versión.

Desde la versión 0.9.7 las respuestas a una consulta de LeaseSet (un
DatabaseStoreMessage o un DatabaseSearchReplyMessage) estarán cifradas
mediante la inclusión de la clave de sesión y la etiqueta en la
consulta. Esto esconde la respuesta desde la pasarela de entrada
(inbound gateway, IBGW) del túnel de respuesta. Las respuestas a
consultas a de RouterInfo serán cifradas si se habilita el cifrado de
consultas.

(Reference: [Hashing it out in Public]() Sections
2.2-2.3 for terms below in italics)

Due to the relatively small size of the network and flooding redundancy,
lookups are usually O(1) rather than O(log n). A router is highly likely
to know a floodfill router close enough to the key to get the answer on
the first try. In releases prior to 0.8.9, routers used a lookup
redundancy of two (that is, two lookups were performed in parallel to
different peers), and neither *recursive* nor *iterative* routing for
lookups was implemented. Queries were sent through *multiple routes
simultaneously* to *reduce the chance of query failure*.

Desede la versión 0.8.9 las *consultas iterativas* se implementaron sin
redundancia en la consulta. Esta es una consulta más eficiente y fiable,
que funcionará mucho mejor cuando no sean conocidos todos los pares de
inundación (\`floodfill peers\`), y elimina una seria limitación al
crecimiento de la red. Al crecer la red y que cada router conozca sólo
un pequeño subconjunto de los pares de inundación, las consultas
llegarán a ser O(log n). Incluso si los pares no devuelven referencias
más cercanas a la clave, la consulta continúa con el par
más-próximo-a-continuación, para añadir robustez, y para prevenir que un
par de inundación malicioso acapare (\`black-holing\`) una parte del
espacio de la clave. Las consultas continúan hasta que se alcance el
total del tiempo límite de la consulta o se haya consultado al número de
pares máximo.

Los *identificadores (\`IDs\`) de nodos* son *verificables* en aquellos
\[nodos\] en los que usamos el identificador criptográfico del router
(\`hash\`) directamente tanto como identificador (\`ID\`) de nodo y como
clave Kademlia. Las respuestas incorrectas que no sean más cercanas a la
clave de búsqueda son ignoradas por lo general. Dado el actual tamaño de
la red, un router tiene *conocimiento detallado del vecindario del
espacio del identicador (\`ID\`) del destino*.

### Verificación del almacenamiento de la RouterInfo

Note: RouterInfo verification is disabled as of release 0.9.7.1 to
prevent the attack described in the paper [Practical Attacks Against the
I2P Network](). It is not clear if
verification can be redesigned to be done safely.

Para verificar que un almacenamiento fue exitoso, un router simplemente
espera cerca de 10 segundos, entonces envía una consulta a otro router
de inundación (\`floodfill\`) cercano a la clave (pero no al que se
envió el almacenamiento). Las consultas establecieron uno de los túneles
exploratorios de salida del router. Las consultas están cifradas
extremo-a-extremo con garlic (ajo) para prevenir la vigilancia en el
extremo exterior (OutBound End Point, OBEP).

### Verificación del almacenamiento del LeaseSet

Para verificar que el almacenamiento fue exitoso, un router simplemente
espera cerca de 10 segundos, y luego envía una consulta a otro router de
inundación (\`floodfill\`) cercano a la clave (pero no al que se envió
el almacenamiento). Las consultas establecieron uno de los túneles de
salida del cliente para el destino del LeaseSet (grupo de túneles para
un destino) que se está verificando. Para prevenir la vigilancia en el
OBEP (extremo exterior) del túnel de salida, las consultas están
cifradas extremo-a-extremo con garlic (ajo). Se especifica a las
respuestas que vuelvan a través de uno de los túneles de entrada del
cliente.

Desde la versión 0.9.7, las respuestas tanto para las consultas de
RouterInfo como de LeaseSet (un DatabaseStoreMessage o un
DatabaseSearchReplyMessage) estarán cifradas para ocultar la respuesta
desde la pasarela de entrada (\`inbound gateway\`, IBGW) del túnel de
respuesta.

### Exploración

*Exploration* is a special form of netdb lookup, where a router attempts
to learn about new routers. It does this by sending a floodfill router a
[I2NP]() DatabaseLookup Message, looking for a
random key. As this lookup will fail, the floodfill would normally
respond with a [I2NP]() DatabaseSearchReplyMessage
containing hashes of floodfill routers close to the key. This would not
be helpful, as the requesting router probably already knows those
floodfills, and it would be impractical to add all floodfill routers to
the \"don\'t include\" field of the DatabaseLookup Message. For an
exploration query, the requesting router sets a special flag in the
DatabaseLookup Message. The floodfill will then respond only with
non-floodfill routers close to the requested key.

### Notas sobre las respuestas a consultas

La respuesta a una solicitud de consulta es o bien (si tiene éxito) un
mensaje de alcemacenamiento en la base de datos (DSM), o (si falla) un
mensaje de respuesta de búsqueda en la base de datos (DSRM). El DSRM
contiene un campo \'from\' (desde) en el hash del router para indicar la
fuente de la respueta; el DSM no. El campo \'from\' (desde) del DSRM no
está autentificado y pude ser vigilado o inválido. No hay otras
etiquetas de respuesta. Por lo tanto, cuando se hacen múltiples
solicitudes en paralelo, es difícill monitorizar el rendimiento de los
diferentes routers de inundación.

## Alojamiento redundante (MultiHoming) {#multihome}

Los destinos I2P pueden ser alojados simultáneamente en múltiples
routers I2P, usando las mismas claves pública y privada
(tradicionalmente almacenadas en los ficheros eepPriv.dat). Como ambas
ambas instancias publicarán periódicamente sus LeaseSets hacia los pares
de inundación (floodfill peers), el LeaseSet (túneles al mismo destino
I2P) publicado más recientemente será devuelto a un par como resultado
de una búsqueda en la base de datos. Como los LeaseSets tienen (como
mucho) 10 minutos de vida, si alguno de los routers I2P se cae, el corte
será como mucho de 10 minutos, y normalmente mucho menos tiempo. La
función de alojamiento redundante (multihoming) ha sido verificada y
está en uso en varios servicios de la red.

As of release 0.9.38, floodfills support a new Meta LeaseSet structure.
This structure provides a tree-like structure in the DHT, to refer to
other LeaseSets. Using Meta LeaseSets, a site may implement large
multihomed services, where several different Destinations are used to
provide a common service. The entries in a Meta LeaseSet are
Destinations or other Meta LeaseSets, and may have long expirations, up
to 18.2 hours. Using this facility, it should be possible to run
hundreds or thousands of Destinations hosting a common service. See
proposal 123 for details.

## Análisis de amenazas {#threat}

Also discussed on [the threat model
page](#floodfill).

Un usuario hostil puede intentar dañar la red creando uno o más ruters
floodfill y configurándolos para ofrecer respuestas malas, lentas o
incluso no ofrecerlas. Algunos escenarios se discuten más abajo.

### Mitigación general a través del crecimiento

There are currently around floodfill routers in the
network. Most of the following attacks will become more difficult, or
have less impact, as the network size and number of floodfill routers
increase.

### Mitigación general a través de la redundancia

Via flooding, all netdb entries are stored on the 
floodfill routers closest to the key.

### Falsificaciones

Todas las entradas de la netdb están firmadas por sus creadores, por lo
que ningún ruter puede crear un RouterInfo o un LeaseSet.

### Lento o sin respuestas

Each router maintains an expanded set of statistics in the [peer
profile]() for each floodfill router,
covering various quality metrics for that peer. The set includes:

- Tiempo medio de respuesta
- Porcentaje de consultas respondidas con los datos solicitados
- Porcentaje de los almacenamientos que fueron verificados
 satisfactoriamente
- El último almacenaje exitoso
- La última búsqueda exitosa
- Última respuesta

Cada vez que un ruter necesita determinar cual ruter floodfill está más
cercano a cierta clave, utiliza estas medidas para determinar que
floodfills son \"buenos\". Estos métodos, y umbrales, usados para
determinar \"lo bueno que es\" son relativamente nuevos, y pueden ser
revisados y mejorados. Mientras que un ruter que no responda será
identificado y evitado rápidamente, los ruters que sólo son maliciosos a
veces pueden ser mucho más difíciles de manejar.

### Ataque Sybil (espacio de claves completo) {#sybil}

An attacker may mount a [Sybil attack]() by
creating a large number of floodfill routers spread throughout the
keyspace.

(In a related example, a researcher recently created a [large number of
Tor relays]().) If successful, this could be an
effective DOS attack on the entire network.

Si los floodfills no se comportan suficientemente mal para ser marcados
como \"malos\" usando las medidas del perfil del par descritas antes,
sería un escenario muy difícil de manejar. Las respuestas de la red Tor
pueden ser mucho más ágiles en el caso de los relays, ya que los relays
maliciosos pueden ser eliminados manualmente del consenso. Algunas
respuestas factibles para la red I2P son listadas debajo, aunque ninguna
de ellas es totalmente satisfactoria:

- Crear una lista de hashes de ruters malos o IPs, y anunciar la lista
 de varias formas (novedades de consola, web, forums, etc.); los
 usuarios tendrían que descargar la lista manualmente y añadirla a
 \"lista negra\" local.
- Pedir a todos los usuarios de la red el activar el floodfill
 manualmente (luchar contra Sybil con más Sybil)
- Liberar una nueva versión del software que incluya la lista \"mala\"
 inscrustada en el código
- Liberar una versión del software nueva que mejore los umbrales y las
 medidas del perfil de los pares, para intentar identificar los pares
 \"malos\" automáticamente.
- Añadir una ampliación que descalifique floodfills si hay demasiados
 de ellos en un único bloque de IPs
- Implementar una lista negra automática basada en suscripciones
 controlada por un único grupo individual. Esto esencialmente
 implementaría una parte del modelo de \"consenso\" de Tor.
 Desafortunadamente le daría a un solo grupo el poder de bloquear la
 participación de cualquier ruter o IP en la red, o incluso apagar o
 destruir la red entera.

Este ataque se hace más difícil cuanto más grande es la red.

### Ataque Sybil (espacio de claves parcial) {#sybil-partial}

An attacker may mount a [Sybil attack]() by
creating a small number (8-15) of floodfill routers clustered closely in
the keyspace, and distribute the RouterInfos for these routers widely.
Then, all lookups and stores for a key in that keyspace would be
directed to one of the attacker\'s routers. If successful, this could be
an effective DOS attack on a particular I2P Site, for example.

Ya que el espacio de claves está indexado por el hash criptográfico
(SHA256) de la clave, un atacante tiene que usar la fuerza bruta para
generar repetidamente hashes de routers hasta que tenga suficientes que
estén suficientemente cerca de la clave. La cantidad de potencia de
cálculo requerida para esto, la cual depende del tamaño de la red, es
desconocida.

Como una defensa parcial contra este ataque, el algoritmo usado para
determinar la \"cercanía\" Kademlia varía con el tiempo. En vez de usar
el hash de la clave (por ejemplo H(k)) para determinar la cercanía,
usamos el Hash de la clave añadido a la cadena de datos actuales, por
ejemplo H(k + YYYYMMDD). En otras palabras, el espacio de claves
completo de la netdb \"rota\" cada día a la media noche UTC. Cualquier
ataque parcial al espacio de claves tendría que regenerarse cada día,
después de cada rotación los ruters atacantes no estarán ya cerca de la
clave del objetivo.

Este ataque se hace más difícil según crece la red. Aunque estudios
recientes han demostrado que la rotación del espacio de claves no es
particularmente efectiva. Un atacante podría pre-calcular numerosos
hashes de ruters de antemano, y sólo son necesarios unos pocos ruters
para \"eclipsar\" una parte del espacio de claves en sólo media hora
después de la rotación.

Una de las consecuencias de la rotación diaria del espacio de claves es
que la base de datos de la red distribuida se vuelve no fiable durante
unos minutos tras la rotación \-- las búsquedas fallarán porque los
nuevos routers \"más cercanos\" no han recibido aún un almacenamiento.
El alcance del problema, y los métodos para mitigarlo (por ejemplo con
\"handoffs, manos fuera\" de la netdb a media noche) es un tema para
futuros estudios.

### Ataques Bootstrap, de arranque

Un atacante podría intentar arrancar nuevos ruters dentro de una red
aislada o controlada en su mayoría por él tomando control de una web de
resiembra, o engañando a los desarrolladores para que añadan su web de
resembrado dentro del código del ruter.

Existen varias defensas posibles, y la mayoría ya están planeadas:

- Desautoriza recurrir a HTTP desde HTTPS para el resembrado. Un
 atacante mediante un ataque de hombre-en-el-medio (MitM) podría
 simplemente bloquear HTTPS, y responder al HTTP.
- Incluyendo los datos de resiembra en el instalador

Defensas que están implementadas:

- Cambiar la tarea de resembrado para obtener un subconjunto de
 RouterInfos desde varias webs de resiembra en vez de usar una única
 web.
- Creando un servicio de monitoreo de resiembras fuera de la red, que
 periódicamente pregunte a las webs de resiembra y verifique que los
 datos no están corruptos o son inconsistentes con otras vistas de la
 red.
- Desde la versión 0.9.14, los datos de resembrado están empaquetados
 en un fichero zip firmado, y la firma se verifica cuando es
 descargado. See [the su3
 specification](#su3)
 for details.

### Captura de peticiones

See also [lookup](#lookup) (Reference: [Hashing it out in
Public]() Sections 2.2-2.3 for terms below in
italics)

Similar a un ataque bootstrap, un atacante usando un ruter floodfill
podría intentar \"dirigir\" a los pares a un subconjunto de ruters
controlados por él devolviendo sus referencias.

Esto es raro que funcione vía exploración, porque la exploración es una
tarea de baja frecuencia. Los ruters obtienen la mayoría de sus
referencias sobre los pares cuando crean los túneles normales. Los
resultados de exploración están generalmente limitados a unos pocos
hashes de ruters, y cada petición de exploración es dirigida a un ruter
floodfill aleatorio.

As of release 0.8.9, *iterative lookups* are implemented. For floodfill
router references returned in a [I2NP]()
DatabaseSearchReplyMessage response to a lookup, these references are
followed if they are closer (or the next closest) to the lookup key. The
requesting router does not trust that the references are closer to the
key (i.e. they are *verifiably correct*. The lookup also does not stop
when no closer key is found, but continues by querying the next-closet
node, until the timeout or maximum number of queries is reached. This
prevents a malicious floodfill from black-holing a part of the key
space. Also, the daily keyspace rotation requires an attacker to
regenerate a router info within the desired key space region. This
design ensures that the query capture attack described in [Hashing it
out in Public]() is much more difficult.

### Selección del Relay basado en DHT

(Reference: [Hashing it out in Public]() Section 3)

This doesn\'t have much to do with floodfill, but see the [peer
selection page]() for a discussion of the
vulnerabilities of peer selection for tunnels.

### Fugas de información

(Reference: [In Search of an Anonymous and Secure
Lookup]() Section 3)

This paper addresses weaknesses in the \"Finger Table\" DHT lookups used
by Torsk and NISAN. At first glance, these do not appear to apply to
I2P. First, the use of DHT by Torsk and NISAN is significantly different
from that in I2P. Second, I2P\'s network database lookups are only
loosely correlated to the [peer
selection]() and [tunnel
building]() processes; only
previously-known peers are used for tunnels. Also, peer selection is
unrelated to any notion of DHT key-closeness.

Algunos de estos serán más interesantes cuando la red I2P sea mucho más
grande. Ahora mismo, cada ruter conoce una gran porción de la red, con
lo que mirando por un RouterInfo en particular en la base de datos de la
red no indica que ese ruter se vaya a usar en un túnel. Quizás cuando la
red sea 100 veces más grande, la búsqueda sea correlativa. Por supuesto,
una red más grande hace que un ataque Sybil sea mucho más difícil.

However, the general issue of DHT information leakage in I2P needs
further investigation. The floodfill routers are in a position to
observe queries and gather information. Certainly, at a level of *f* =
0.2 (20% malicious nodes, as specifed in the paper) we expect that many
of the Sybil threats we describe
([here](#sybil), [here](#sybil) and
[here](#sybil-partial)) become problematic for several reasons.

## Historial {#history}

[Movido a la página de discusión de la
netdb]().

## Trabajo futuro {#future}

Cifrado de fin a fin de las búsquedas y respuestas adicionales en la
netDb.

Mejores métodos de seguimiento de las respuestas de las búsquedas.


