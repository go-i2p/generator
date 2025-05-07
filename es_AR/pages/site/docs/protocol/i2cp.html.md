 I2CP
2025-04 0.9.66 

El Protocolo de Cliente de I2P (I2CP) presenta una fuerte
compartimentalización de los asuntos entre el router I2P y cualquier
cliente que quiera comunicarse a través de la red. Habilita mensajería
segura y asíncrona mediante el envío y recepción de mensajes sobre un
único socket TCP. Con I2CP una aplicación cliente le dice al router
quiénes son ellos (sus \"destinos\"), qué anonimato, fiabilidad, y
latencia tienen los intercambios a realizar, y a dónde enviar los
mensajes. A la contra el router usa I2CP para decirle al cliente cuándo
llega cualquier mensaje, y para pedirle autorización para que se usen
algunos túneles.

The protocol itself is implemented in Java, to provide the [Client
SDK](). This SDK is exposed in the i2p.jar package,
which implements the client-side of I2CP. Clients should never need to
access the router.jar package, which contains the router itself and the
router-side of I2CP. There is also a [C library
implementation](). A non-Java client would also
have to implement the [streaming library]()
for TCP-style connections.

Applications can take advantage of the base I2CP plus the
[streaming]() and
[datagram]() libraries by using the [Simple
Anonymous Messaging]() or
[BOB]() protocols, which do not require clients to
deal with any sort of cryptography. Also, clients may access the network
by one of several proxies - HTTP, CONNECT, and SOCKS 4/4a/5.
Alternatively, Java clients may access those libraries in
ministreaming.jar and streaming.jar. So there are several options for
both Java and non-Java applications.

Client-side end-to-end encryption (encrypting the data over the I2CP
connection) was disabled in I2P release 0.6, leaving in place the
[ElGamal/AES end-to-end encryption]() which
is implemented in the router. The only cryptography that client
libraries must still implement is [DSA public/private key
signing](#DSA) for
[LeaseSets](#msg_CreateLeaseSet) and [Session
Configurations](#struct_SessionConfig), and
management of those keys.

En una instalación I2P estándar, el puerto 7654 es usado por clientes de
Java externos para comunicarse con el router local vía I2CP. Por
defecto, el router se liga a la dirección 127.0.0.1. Para ligarse a
0.0.0.0, establezca la opción de la configuración avanzada del router
`i2cp.tcp.bindAllInterfaces=true` y reinicie. Los clientes en la misma
JVM (Máquina Virtual Java), pasan los mensajes directamente al router a
través de una interfaz JVM interna.

Some router and client implementations may also support external
connections over SSL, as configured by the i2cp.SSL=true option. While
SSL is not the default, it is strongly recommended for any traffic that
may be exposed to the open Internet. The authorization user/password (if
any), the [Private
Key](#type_PrivateKey) and [Signing
Private Key](#type_SigningPrivateKey)
for the
[Destination](#struct_Destination) are
all transmitted in-the-clear unless SSL is enabled. Some router and
client implementations may also support external connections over domain
sockets.

## Especificación del protocolo I2CP

Now on the [I2CP Specification page]().

## Inicialización I2CP

When a client connects to the router, it first sends a single protocol
version byte (0x2A). Then it sends a [GetDate
Message](#msg_GetDate) and waits for the [SetDate
Message](#msg_SetDate) response. Next, it sends a
[CreateSession Message](#msg_CreateSession)
containing the session configuration. It next awaits a [RequestLeaseSet
Message](#msg_RequestLeaseSet) from the router,
indicating that inbound tunnels have been built, and responds with a
CreateLeaseSetMessage containing the signed LeaseSet. The client may now
initiate or receive connections from other I2P destinations.

## Opciones de I2CP {#options}

### Opciones del lado-del-router

The following options are traditionally passed to the router via a
[SessionConfig](#struct_SessionConfig) contained
in a [CreateSession Message](#msg_CreateSession)
or a [ReconfigureSession
Message](#msg_ReconfigureSession).

Opciones del lado-del-router

Opción

Desde la versión

Parámetros recomendados

Rango permitido

Por defecto

Descripción

clientMessageTimeout

 

 

8\*1000 - 120\*1000

60\*1000

El tiempo de espera (ms) para todos los mensajes enviados. No usado. Vea
la especificación del protocolo para configuraciones por-mensaje.

crypto.lowTagThreshold

0.9.2

 

1-128

30

Número mínimo de etiquetas de sesión ElGamal/AES antes de que enviemos
más. Recomendado: aproximadamente \'tagsToSend \* 2/3\'

crypto.ratchet.inboundTags

0.9.47

 

1-?

160

Inbound tag window for ECIES-X25519-AEAD-Ratchet. Local inbound tagset
size. See proposal 144.

crypto.ratchet.outboundTags

0.9.47

 

1-?

160

Outbound tag window for ECIES-X25519-AEAD-Ratchet. Advisory to send to
the far-end in the options block. See proposal 144.

crypto.tagsToSend

0.9.2

 

1-128

40

Número de etiquetas de sesión ElGamal/AES para enviar de golpe. Para los
clientes con anchos de baja relativamente bajos para el par cliente
(IRC, algunas aplicaciones UDP), esto valor puede ser más bajo.

explicitPeers

 

 

 

null

Lista separada por comas de los Hashes Base 64 de los pares con los que
construir túneles para pasar a través; sólo para depuración

i2cp.dontPublishLeaseSet

 

true, false

 

false

Generalmente suele ser verdadero para los clientes y falso para los
servidores

i2cp.fastReceive

0.9.4

 

true, false

false

Si es verdadero, el ruter simplemente envía el MessagePayload, en lugar
de enviar MessageStatus y esperar por un ReceiveMessageBegin.

i2cp.leaseSetAuthType

0.9.41

0

0-2

0

The type of authentication for encrypted LS2. 0 for no per-client
authentication (the default); 1 for DH per-client authentication; 2 for
PSK per-client authentication. See proposal 123.

i2cp.leaseSetEncType

0.9.38

4,0

0-65535,\...

0

The encryption type to be used, as of 0.9.38. Interpreted client-side,
but also passed to the router in the SessionConfig, to declare intent
and check support. As of 0.9.39, may be comma-separated values for
multiple types. See PublicKey in common strutures spec for values. See
proposals 123, 144, and 145.

i2cp.leaseSetOfflineExpiration

0.9.38

 

 

 

The expiration of the offline signature, 4 bytes, seconds since the
epoch. See proposal 123.

i2cp.leaseSetOfflineSignature

0.9.38

 

 

 

The base 64 of the offline signature. See proposal 123.

i2cp.leaseSetPrivKey

0.9.41

 

 

 

A base 64 X25519 private key for the router to use to decrypt the
encrypted LS2 locally, only if per-client authentication is enabled.
Optionally preceded by the key type and \':\'. Only \"ECIES_X25519:\" is
supported, which is the default. See proposal 123. Do not confuse with
i2cp.leaseSetPrivateKey which is for the leaseset encryption keys.

i2cp.leaseSetSecret

0.9.39

 

 

\"\"

Base 64 encoded UTF-8 secret used to blind the leaseset address. See
proposal 123.

i2cp.leaseSetTransientPublicKey

0.9.38

 

 

 

\[type:\]b64 The base 64 of the transient private key, prefixed by an
optional sig type number or name, default DSA_SHA1. See proposal 123.

i2cp.leaseSetType

0.9.38

1,3,5,7

1-255

1

The type of leaseset to be sent in the CreateLeaseSet2 Message.
Interpreted client-side, but also passed to the router in the
SessionConfig, to declare intent and check support. See proposal 123.

i2cp.messageReliability

 

 

BestEffort, None

BestEffort

Asegurarse de que está desactivado; None fue implementado en 0.8.1; la
librería de straming por defecto es None como en 0.8.1, la parte cliente
es None como en 0.9.4

i2cp.password

0.8.2

string

 

 

Para la autorización, si es requerida por el router. Si el cliente está
ejecutandose en la misma JVM (máquina virtual Java) que el router, no se
requiere esta opción. Advertencia - el nombre de usuario y la contraseña
se envían en claro al router, a menos que se use SSL (i2cp.SSL=true). La
autorización sólo está recomendada cuando se usa SSL.

i2cp.username

0.8.2

string

 

 

inbound.allowZeroHop

 

true, false

 

true

Si es de entrada están permitidos los túneles de cero saltos

outbound.allowZeroHop

 

true, false

 

true

Si es de salida están permitidos los túneles de cero saltos

inbound.backupQuantity

 

El número de bytes de la IP para comparar y determinar si los dos ruters
están en el mismo túnel. 0 para deshabilitarlo

outbound.IPRestriction

 

El número de bytes de la IP para comparar y determinar si los dos ruters
están en el mismo túnel. 0 para deshabilitarlo

inbound.length

 

Cantidad aleatoria a añadir o sustraer a la longitud de los túneles
entrantes. Un número positivo significa añadir una cantidad aletoria de
0 a x ambos incluidos. Un número negativo -x significa añadir una
cantidad aleatoria de -x a x ambos incluidos. El router limitará la
longitud total del túnel de 0 a 7 ambos incluidos. La varianza por
defecto era 1 antes de la versión 0.7.6.

outbound.lengthVariance

 

Cantidad aleatoria a añadir o sustraer a la longitud de los túneles
salientes. Un número positivo x significa añadir una cantidad aleatoria
de 0 a x ambos incluidos. Un número negativo -x significa añadir una
cantidad de -x a x ambos incluidos. El router limitará la longitud total
del túnel de 0 a 7 ambos incluidos. La varianza por defecto era 1 antes
de la versión 0.7.6.

inbound.nickname

 

string

 

 

Nombre del túnel - usado por lo general en routerconsole, que usara los
primeros pocos caracteres del identificador criptográfico (\`hash\`)
Base64 del destino por defecto.

outbound.nickname

 

string

 

 

Nombre del túnel - ignorado por lo general a menos que inbound.nickname
(apodo entrante) no esté establecido.

outbound.priority

0.9.4

Ajustes de prioridades para los mensajes de salida. Más alto indica más
prioridad.

inbound.quantity

 

Número de túneles entrantes. El límite fue elevado de 6 a 16 en la
versión 0.9; sin embargo, números superiores a 6 son incompatibles con
versiones anteriores.

outbound.quantity

 

Se usa para mantener consistente el orden de los pares (peers) entre
reinicios.

outbound.randomKey

0.9.17

Base 64 encoding of 32 random bytes

 

 

inbound.\*

 

 

 

 

Cualquier otra opción con el prefijo \"inbound\" es almacenada en las
\"opciones desconocidas\" del grupo de configuraciones del túnel de
entrada.

outbound.\*

 

 

 

 

Cualquier otra opción con el prefijo \"outbound\" es almacenada en las
\"opciones desconocidas\" del grupo de configuraciones del túnel de
salida.

shouldBundleReplyInfo

0.9.2

true, false

 

true

Configúrela a \'falso\' para deshabilitar que se llegue a empaquetar un
LeaseSet de respuesta. Para los clientes que no publican su LeaseSet
(túneles a su destino I2P), esta opción debe marcarse verdadera para que
las repuestas sean posibles. También se recomienda \'verdadero\', para
los servidores alojados de modo redundante (multihomed) con tiempos de
conexión largos.

Poniéndolo en \"false\", falso, puede ahorrar bastante ancho de banda de
salida, especialmente si el cliente está configurado para usar un gran
número de túneles de entrada (Leases). Si las respuestas son aún
necesarias, esto puede cambiar la carga a el cliente más lejano final y
en el floodfill. Hay varios casos donde \"false\" podría ser apropiado:

- Dirección unidireccional, no se necesita respuesta
- El LeaseSet está publicado y un latencia de respuesta mayor es
 aceptable
- El LeaseSet está publicado, el cliente es un \"servidor\", todas las
 conexiones son de entrada, por lo que la destinación lejana que se
 está conectanda ya tiene el leaseset, obviamente. Las conexiones o
 son cortas, o son aceptables para la latencia o conexiones de larga
 duración para incrementar temporalmente mientras que la otra
 descarga de nuevo el LeaseSet después de expirar. Los servidores
 HTTP puede encajar en estos requerimientos.

Nota: Una gran cantidad de configuraciones, el tamaño o variaciones en
las configuraciones pueden causar bastantes problemas en el rendimiento
o fiabilidad.

Note: As of release 0.7.7, option names and values must use UTF-8
encoding. This is primarily useful for nicknames. Prior to that release,
options with multi-byte characters were corrupted. Since options are
encoded in a [Mapping](#type_Mapping),
all option names and values are limited to 255 bytes (not characters)
maximum.

### Opciones de la parte cliente

Las siguientes opciones son interpretadas por la parte cliente, y serán
interpretadas si pasan a la I2PSession a través de la llamada
I2PClient.createSession(). La librería de streaming también debería
pasar estas opciones a través de I2CP. Otras implementaciones pueden
tener otros valores por defecto.

Opciones de la parte cliente

Opción

Desde la versión

Parámetros recomendados

Rango permitido

Por defecto

Descripción

i2cp.closeIdleTime

0.7.1

1800000

Si es verdadero, el ruter simplemente envía el MessagePayload, en lugar
de enviar MessageStatus y esperar por un ReceiveMessageBegin.

i2cp.gzip

0.6.5

true, false

 

true

Gzip los datos de salida

i2cp.leaseSetAuthType

0.9.41

0

0-2

0

The type of authentication for encrypted LS2. 0 for no per-client
authentication (the default); 1 for DH per-client authentication; 2 for
PSK per-client authentication. See proposal 123.

i2cp.leaseSetBlindedType

0.9.39

 

0-65535

See prop. 123

The sig type of the blinded key for encrypted LS2. Default depends on
the destination sig type. See proposal 123.

i2cp.leaseSetClient.dh.nnn

0.9.41

b64name:b64pubkey

 

 

The base 64 of the client name (ignored, UI use only), followed by a
\':\', followed by the base 64 of the public key to use for DH
per-client auth. nnn starts with 0 See proposal 123.

i2cp.leaseSetClient.psk.nnn

0.9.41

b64name:b64privkey

 

 

The base 64 of the client name (ignored, UI use only), followed by a
\':\', followed by the base 64 of the private key to use for PSK
per-client auth. nnn starts with 0. See proposal 123.

i2cp.leaseSetEncType

0.9.38

0

0-65535,\...

0

The encryption type to be used, as of 0.9.38. Interpreted client-side,
but also passed to the router in the SessionConfig, to declare intent
and check support. As of 0.9.39, may be comma-separated values for
multiple types. See also i2cp.leaseSetPrivateKey. See PublicKey in
common strutures spec for values. See proposals 123, 144, and 145.

i2cp.leaseSetKey

0.7.1

 

 

 

Para leasesets cifrados. SessionKey (clave de sesión) Base 64 (44
caracteres)

i2cp.leaseSetOption.nnn

0.9.66

srvKey=srvValue

 

 

A service record to be placed in the LeaseSet2 options. Example:
\"\_smtp.\_tcp=1 86400 0 0 25 \...b32.i2p\" nnn starts with 0. See
proposal 167.

i2cp.leaseSetPrivateKey

0.9.18

 

 

 

Base 64 private keys for encryption. Optionally preceded by the
encryption type name or number and \':\'. For LS1, only one key is
supported, and only \"0:\" or \"ELGAMAL_2048:\" is supported, which is
the default. As of 0.9.39, for LS2, multiple keys may be
comma-separated, and each key must be a different encryption type. I2CP
will generate the public key from the private key. Use for persistent
leaseset keys across restarts. See proposals 123, 144, and 145. See also
i2cp.leaseSetEncType. Do not confuse with i2cp.leaseSetPrivKey which is
for encrypted LS2.

i2cp.leaseSetSecret

0.9.39

 

 

\"\"

Base 64 encoded UTF-8 secret used to blind the leaseset address. See
proposal 123.

i2cp.leaseSetSigningPrivateKey

0.9.18

 

 

 

Clave privada Base 64 para firmas. Precedido opcionalmente por el tipo
de clave y \':\'. DSA_SHA1 es la predeterminada. El tipo de clave tiene
que coincidir con el tipo de firma en el destino I2P. I2CP generará la
clave pública desde la clave privada. Se utiliza para claves
persistentes de leasets entre reinicios.

i2cp.leaseSetType

0.9.38

1,3,5,7

1-255

1

The type of leaseset to be sent in the CreateLeaseSet2 Message.
Interpreted client-side, but also passed to the router in the
SessionConfig, to declare intent and check support. See proposal 123.

i2cp.messageReliability

 

 

BestEffort, None

None

Asegurarse de que está desactivado; None fue implementado en 0.8.1; None
es el valor por defecto en 0.9.4

i2cp.reduceIdleTime

0.7.1

1200000

Conectar con el ruter usando SSL. Si el cliente se está ejecutando en la
misma JVM que el ruter esta opción es ignorada, y el cliente conecta con
el ruter internamente.

i2cp.tcp.host

 

 

 

127.0.0.1

Hostname del ruter. Si el cliente se ejecuta en la misma JVM como un
ruter, esta opción es ignorada, y el cliente se conecta al ruter
internamente.

i2cp.tcp.port

 

 

1-65535

7654

Puerto I2CP del ruter. Si el cliente se ejecuta en la misma JVM como un
ruter, esta opción es ignorada, y el cliente se conecta al ruter
internamente.

Nota: todos los argumentos, incluyendo los números, son cadenas de
caracteres. Los valores True/false son cadenas de caracteres y son
sensibles a las mayúsculas o minúsculas. Cualquier otro que no sea
\"true\" en minúsculas será interpretado como falso. Todas los nombres
de opciones son sensibles a las mayúsculas/minúsculas.

## Formato de los datos del payload I2CP y de Multiplexing {#format}

The end-to-end messages handled by I2CP (i.e. the data sent by the
client in a [SendMessageMessage](#msg_SendMessage)
and received by the client in a
[MessagePayloadMessage](#msg_MessagePayload)) are
gzipped with a standard 10-byte gzip header beginning with 0x1F 0x8B
0x08 as specified by [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt). As
of release 0.7.1, I2P uses ignored portions of the gzip header to
include protocol, from-port, and to-port information, thus supporting
streaming and datagrams on the same destination, and allowing
query/response using datagrams to work reliably in the presence of
multiple channels.

La función gzip puede apagarse completamente, aunque si se pone la
opción i2cp.gzip=false, se cambia el valor de esfuerzo de gzip a 0, lo
que puede ahorrar un poco de CPU. Implementations may select different
gzip efforts on a per-socket or per-message basis, depending on an
assessment of the compressibility of the contents. Due to the
compressibility of destination padding implemented in API 0.9.57
(proposal 161), compression of the streaming SYN packets in each
direction, and of repliable datagrams, is recommended even if the
payload is not compressible. Implementations may wish to write a trivial
gzip/gunzip function for a gzip effort of 0, which will provide large
efficiency gains over a gzip library for this case.

Bytes

Contenido

0-2

Cabecera gzip 0x1F 0x8B 0x08

3

Opciones de gzip

4-5

Puerto de origen I2P (mtime de Gzip)

6-7

Puerto de destino de I2p (mtime de Gzip)

8

Zflags de Gzip (set to 2 to be indistinguishable from the Java
implementation)

9

Protocolo I2P (6= Streaming, 17 = Datagram, 18 = Raw Datagrams) (OS de
Gzip)

Note: I2P protocol numbers 224-254 are reserved for experimental
protocols. I2P protocol number 255 is reserved for future expansion.

La integridad de los datos es verificada con el estándar gzip CRC-32
como es especificado por el [RFC
1952](http://www.ietf.org/rfc/rfc1952.txt).

## Important Differences from Standard IP

I2CP ports are for I2P sockets and datagrams. They are unrelated to your
local sockets or ports. Because I2P did not support ports and protocol
numbers prior to release 0.7.1, ports and protocol numbers are somewhat
different from that in standard IP, for backward compatibility:

- Port 0 is valid and has special meaning.
- Ports 1-1023 are not special or privileged.
- Servers listen on port 0 by default, which means \"all ports\".
- Clients send to port 0 by default, which means \"any port\".
- Clients send from port 0 by default, which means \"unspecified\".
- Servers may have a service listening on port 0 and other services
 listening on higher ports. If so, the port 0 service is the default,
 and will be connected to if the incoming socket or datagram port
 does not match another service.
- Most I2P destinations only have one service running on them, so you
 may use the defaults, and ignore I2CP port configuration.
- Protocol 0 is valid and means \"any protocol\". However, this is not
 recommended, and probably will not work. Streaming requires that the
 protocol number is set to 6.
- Streaming sockets are tracked by an internal connection ID.
 Therefore, there is no requirement that the 5-tuple of
 dest:port:dest:port:protocol be unique. For example, there may be
 multiple sockets with the same ports between two destinations.
 Clients do not need to pick a \"free port\" for an outbound
 connection.

## Trabajo futuro {#future}

- El mecanismo actual de autorización puede modificarse para usar
 contraseñas \'hashed\'.
- Las claves privadas firmantes están incluidas en el mensaje de Crear
 Lease Set (grupo de túneles al mismo destino), no son requeridas. La
 revocación no está implementada. Deben ser reemplazadas con datos
 aleatorios o eliminadas.
- Some improvements may be able to use messages previously defined but
 not implemented. For reference, here is the [I2CP Protocol
 Specification Version 0.9]() (PDF) dated
 August 28, 2003. That document also references the [Common Data
 Structures Specification Version 0.9]().

## See Also {#links}

[C library implementation](http://git.repo.i2p/w/libi2cp.git) 
