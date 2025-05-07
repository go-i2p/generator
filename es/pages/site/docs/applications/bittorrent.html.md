 Bittorrent sobre
I2P 2024-11 0.9.64 

Hay varios clientes bittorrent y trackers sobre I2P. Como el
direccionamiento de I2P usa un Destino en lugar de IP y puerto, los
cambios que se requieren en los softwares del tracker y del cliente para
operar sobre I2P son menores. Estos cambios se especifican debajo.
Observe con cuidado las directrices para compatibilidad con anteriores
clientes y trackers I2P.

Esta página especifica detalles del protocolo comunes a todos los
clientes y trackers. Los clientes y trackers específicos pueden
implementar otras características únicas o protocolos.

Son bienvenidos puertos adicionales de software de cliente y tracker
para I2P.

## General Guidance for Developers

Most non-Java bittorrent clients will connect to I2P via
[SAMv3](). SAM sessions (or
inside I2P, tunnel pools or sets of tunnels) are designed to be
long-lived. Most bittorrent clients will only need one session, created
at startup and closed on exit. I2P is different from Tor, where circuits
may be rapidly created and discarded. Think carefully and consult with
I2P developers before designing your application to use more than one or
two simultaneous sessions, or to rapidly create and discard them.
Bittorrent clients must not create a unique session for every
connection. Design your client to use the same session for announces and
client connections.

Also, please ensure your client settings (and guidance to users about
router settings, or router defaults if you bundle a router) will result
in your users contributing more resources to the network than they
consume. I2P is a peer-to-peer network, and the network cannot survive
if a popular application drives the network into permanent congestion.

Do not provide support for bittorrent through an I2P outproxy to the
clearnet as it will probably be blocked. Consult with outproxy operators
for guidance.

The Java I2P and i2pd router implementations are independent and have
minor differences in behavior, feature support, and defaults. Please
test your application with the latest version of both routers.

i2pd SAM is enabled by default; Java I2P SAM is not. Provide
instructions to your users on how to enable SAM in Java I2P (via
/configclients in the router console), and/or provide a good error
message to the user if the initial connect fails, e.g. \"ensure that I2P
is running and the SAM interface is enabled\".

The Java I2P and i2pd routers have different defaults for tunnel
quantities. The Java default is 2 and the i2pd default is 5. For most
low- to medium-bandwidth and low- to medium-connection counts, 3 is
sufficient. Please specify the tunnel quantity in the SESSION CREATE
message to get consistent performance with the Java I2P and i2pd
routers.

I2P supports multiple signature and encryption types. For compatibility,
I2P defaults to old and inefficient types, so all clients should specify
newer types.

If using SAM, the signature type is specified in the DEST GENERATE and
SESSION CREATE (for transient) commands. All clients should set
SIGNATURE_TYPE=7 (Ed25519).

The encryption type is specified in the SAM SESSION CREATE command or in
i2cp options. Multiple encryption types are allowed. Some trackers
support ECIES-X25519, some support ElGamal, and some support both.
Clients should set i2cp.leaseSetEncType=4,0 (for ECIES-X25519 and
ElGamal) so that they may connect to both.

DHT support requires SAM v3.3 PRIMARY and SUBSESSIONS for TCP and UDP
over the same session. This will require substantial development effort
on the client side, unless the client is written in Java. i2pd does not
currently support SAM v3.3. libtorrent does not currently support SAM
v3.3.

Without DHT support, you may wish to automatically announce to a
configurable list of known open trackers so that magnet links will work.
Consult with I2P users for information on currently-up open trackers and
keep your defaults up-to-date. Supporting the i2p_pex extension will
also help alleviate the lack of DHT support.

For more guidance to developers on ensuring your application uses only
the resources it needs, please see the [SAMv3
specification]() and [our
guide to bundling I2P with your
application]().
Contact I2P or i2pd developers for further assistance.

## Anuncios

Los clientes generalmente incluyen un parámetro falso port=6881 en el
anuncio, por compatibilidad con anteriores trackers. Los trackers pueden
ignorar el parámetro port (puerto), y no deberían necesitarlo.

The ip parameter is the base 64 of the client\'s
[Destination](#struct_Destination),
using the I2P Base 64 alphabet \[A-Z\]\[a-z\]\[0-9\]-\~.
[Destinations](#struct_Destination)
are 387+ bytes, so the Base 64 is 516+ bytes. Clients generally append
\".i2p\" to the Base 64 Destination for compatibility with older
trackers. Trackers should not require an appended \".i2p\".

Otros parámetros son los mismos que en el bittorrent estandar.

Los actuales destinos I2P para clientes son de 387 bytes o más (516 o
más con codificación Base64). Un máximo razonable a asumir, por ahora,
es 475 bytes. Como el tracker debe decodificar la Base64 para producir
respuestas compactas (vea debajo), probablemente el tracker debe
decodificar y rechazar la Base64 erróneas cuando esto se anuncie.

La respuesta tipo predeterminada es no-compacta. Los clientes pueden
solicitar una respuesta compacta con el parámetro compact=1. Un tracker
podría, pero no es un requisito, devolver una respuesta compacta cuando
se le solicite. Note: All popular trackers now support compact responses
and at least one requires compact=1 in the announce. All clients should
request and support compact responses.

A los desarrolladores de nuevos clientes I2P se les anima fuertemente a
implementar anuncios sobre su propio túnel en lugar de sobre el proxy
del cliente HTTP en el puerto 4444. Hacerlo así es tanto más eficiente
como a su vez permite al tracker aplicar destinos (vea debajo).

No hay clientes o trackers I2P conocidos que actualmente soporten
anuncios/respuestas UDP.

## Respuestas de tracker no-compactas

La respuesta no-compacta es como la del bittorrent estándar, con una
\"ip\" I2P. This is a long base64-encoded \"DNS string\", probably with
a \".i2p\" suffix.

Los trackers generalmente incluyen un clave de puerto falsa, o usan el
puerto del anuncio, por compatibilidad con anteriores clientes. Los
clientes deben ignorar el parámetro port (puerto), y no deben
solicitarlo.

The value of the ip key is the base 64 of the client\'s
[Destination](#struct_Destination), as
described above. Trackers generally append \".i2p\" to the Base 64
Destination if it wasn\'t in the announce ip, for compatibility with
older clients. Clients should not require an appended \".i2p\" in the
responses.

Otras claves y valores de respuesta son los mismos que en el bittorrent
estandar.

## Respuestas de tracker compactas

In the compact response, the value of the \"peers\" dictionary key is a
single byte string, whose length is a multiple of 32 bytes. This string
contains the concatenated [32-byte SHA-256
Hashes](#type_Hash) of the binary
[Destinations](#struct_Destination) of
the peers. This hash must be computed by the tracker, unless destination
enforcement (see below) is used, in which case the hash delivered in the
X-I2P-DestHash or X-I2P-DestB32 HTTP headers may be converted to binary
and stored. The peers key may be absent, or the peers value may be
zero-length.

Aunque el soporte para respuesta compacta es opcional para ambos,
clientes y trackers, es altamente recomendable ya que reduce el tamaño
nominal de respuesta alrededor de un 90%.

## Aplicación en destino

Some, but not all, I2P bittorrent clients announce over their own
tunnels. Trackers may choose to prevent spoofing by requiring this, and
verifying the client\'s
[Destination](#struct_Destination)
using HTTP headers added by the I2PTunnel HTTP Server tunnel. The
headers are X-I2P-DestHash, X-I2P-DestB64, and X-I2P-DestB32, which are
different formats for the same information. These headers cannot be
spoofed by the client. A tracker enforcing destinations need not require
the ip announce parameter at all.

Como varios clientes usan el proxy HTTP en lugar de sus propios túneles
para los anuncios, la aplicación de destino (en el tracker) prevendrá su
uso por aquellos clientes a menos que, o hasta que, aquellos clientes se
reconviertan para anunciarse sobre sus propios túneles.

Desafortunadamente, al crecer la red, también lo hará la cantidad de
maliciosidad, así que esperamos que en su momento todos los trackers
apliquen los destinos. Ambos, desarrolladores de trackers y clientes
deben anticiparlo.

## Nombres de Servidor de Anuncio

Announce URL host names in torrent files generally follow the [I2P
naming standards](). In addition to host names
from address books and \".b32.i2p\" Base 32 hostnames, the full Base 64
Destination (with \[or without?\] \".i2p\" appended) should be
supported. Non-open trackers should recognize their own host name in any
of these formats.

Para preservar el anonimato, los clientes por lo general deben ignorar
URLs de anuncio no-I2P en los ficheros torrent.

## Conexiones entre clientes

Las conexiones cliente-a-cliente usan el protocolo estándar sobre TCP.
Actualmente no hay clientes I2P conocidos que soporten comunicación uTP
(Protocol de Transporte utorrent).

I2P uses 387+ byte
[Destinations](#struct_Destination)
for addresses, as explained above.

Si el cliente tiene sólo el identificador criptográfico (\`hash\`) del
destino (como el de una respuesta compacta o el PEX (protocolo de
Intercambio de Pares)), debe realizar una búsqueda codificándolo con
Base 32, añadiendo el sufijo \".b32.i2p\", y consultando en el Servicio
de Nombres, que devolverá el Destino completo si está disponible.

Si el cliente tiene el Destino completo de un par (\`peer\`) que recibió
en una respuesta no-compacta, debe usarlo directamente en el
establecimiento de la conexión. No convierta un Destino de vuelta a un
identificador criptográfico (\`hash\`) Base 32, esto es bastante
ineficiente.

## Prevención de redes-cruzadas.

Para preservar el anonimato, los clientes I2P bittorrent por lo general
no soportan anuncios no-I2P, o conexiones de pares (\`peers\`). Los
proxys al exterior (\`outproxies\`) HTTP de I2P con frecuencia bloquean
anuncios. No hay proxys al exterior SOCKS conocidos que soporten tráfico
bittorrent.

Para prevenir el uso por clientes no-I2P a través de un proxy hacia el
interior (\`inproxy\`) HTTP, los trackers I2P a menudo bloquean accesos
o anuncios que contengan una cabecera HTTP X-Forwarded-For. Los trackers
deben rechazar anuncios de red estándar con IPs IPv4 o IPv6, y no
entregarlos en las respuestas.

## PEX

I2P PEX is based on ut_pex. As there does not appear to be a formal
specification of ut_pex available, it may be necessary to review the
libtorrent source for assistance. It is an extension message, identified
as \"i2p_pex\" in [the extension
handshake](http://www.bittorrent.org/beps/bep_0010.html). It contains a
bencoded dictionary with up to 3 keys, \"added\", \"added.f\", and
\"dropped\". The added and dropped values are each a single byte string,
whose length is a multiple of 32 bytes. These byte strings are the
concatenated SHA-256 Hashes of the binary
[Destinations](#struct_Destination) of
the peers. This is the same format as the peers dictionary value in the
i2p compact response format specified above. The added.f value, if
present, is the same as in ut_pex.

## DHT

El soporte DHT (tabla de hash dinámica) está incluido en el cliente
i2psnark desde la versión 0.9.2. Las diferencias preliminares con la
[BEP 5](http://www.bittorrent.org/beps/bep_0005.html) (Propuesta de
Mejora de Bittorrent 5) están descritas debajo, y están sujetas a
cambios. Contacte con los desarrolladores de I2P si quiere desarrollar
un cliente con soporte DHT.

Al contario que DHT (tabla de hash dinámica), I2P DHT no usa bit alguno
en las opciones de toma de contacto (\`handshake\`), o en el mensaje
PORT (puerto). Se anuncia con un mensaje de extensión, identificado como
\"i2p_dht\" en [la extensión
handshake](http://www.bittorrent.org/beps/bep_0010.html). Contiene un
diccionario b-codificado (\`bencoded\`) con dos claves, \"port\" y
\"rport\" (puerto de respuesta), ambos enteros.



The UDP (datagram) port listed in the compact node info is used to
receive repliable (signed) datagrams. This is used for queries, except
for announces. We call this the \"query port\". This is the \"port\"
value from the extension message. Queries use
[I2CP]() protocol number 17.

In addition to that UDP port, we use a second datagram port equal to the
query port + 1. This is used to receive unsigned (raw) datagrams for
replies, errors, and announces. This port provides increased efficiency
since replies contain tokens sent in the query, and need not be signed.
We call this the \"response port\". This is the \"rport\" value from the
extension message. It must be 1 + the query port. Responses and
announces use [I2CP]() protocol number 18.

La información compacta del par (\`peer\`) son 32 bytes (identificador
criptográfico (\`hash\`) SHA256 de 32 bytes) en lugar de 4 bytes de IP +
2 bytes de puerto. No hay puerto del par. En una respuesta, la clave
\"values\" (valores) es una lista de cadenas, conteniendo cada una la
información compacta de un único par.

Compact node info is 54 bytes (20 byte Node ID + 32 byte SHA256 Hash + 2
byte port) instead of 20 byte Node ID + 4 byte IP + 2 byte port. In a
response, the \"nodes\" key is a single byte string with concatenated
compact node info.

Requisito de identificador (\`ID\`) de nodo seguro: Para hacer más
difíciles diferentes ataques DHT (tabla de hash distribuida) los
primeros 4 bytes del identificador de nodo (\`ID\`) deben coincidir con
los primeros 4 bytes del identificador criptográfico (\`hash\`) del
destino, y los siguientes 2 bytes del identificador de nodo deben
coincidir con los siguientes 2 bytes del resultado de la operación
OR-exclusivo del hash del destino con el puerto.

En un fichero torrent, la clave \"nodos\" del diccionario de un torrent
sin tracker ha de ser determinada. Podría ser una lista de cadenas
binarias de 32 bytes (hashes SHA256) en lugar de una lista de listas que
contengan una cadena de servidor y un valor entero de puerto.
Alternativas: Una única cadena de bytes con hashes concatenados, o una
lista de cadenas por si solas.

## Trackers de datagramas (UDP)

Aún no está disponible para clientes y trackers (rastreadores
bittorrent) el soporte para trackers UDP. Las diferencias preliminares
con la (propuesta de mejora de bittorrent) [BEP
15](http://www.bittorrent.org/beps/bep_0015.html) están descritas
debajo, y son susceptibles de cambiar. Contacte con los desarrolladores
de I2P si desea desarrollar un cliente o un tracker que soporte anuncios
sobre datagramas.

See [Proposal 160]().

## Información adicional

- I2P bittorrent standards are generally discussed on [](http:///).
- A chart of current tracker software capabilities is [also available
 there](http:///files/trackers.html).
- The [I2P bittorrent
 FAQ](http:///viewtopic.php?t=2068)
- [DHT on I2P discussion](http:///topics/812)


