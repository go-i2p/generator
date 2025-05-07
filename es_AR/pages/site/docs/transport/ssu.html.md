 UDP Seguro
Semifiable (SSU) 2025-01 0.9.64 

**DEPRECATED** - SSU has been replaced by SSU2. SSU support was removed
from i2pd in release 2.44.0 (API 0.9.56) 2022-11. SSU support was
removed from Java I2P in release 2.4.0 (API 0.9.61) 2023-12.

SSU (also called \"UDP\" in much of the I2P documentation and user
interfaces) was one of two [transports]()
implemented in I2P. The other is [NTCP2]().
Support for [NTCP]() has been removed.

SSU was introduced in I2P release 0.6. In a standard I2P installation,
the router uses both NTCP and SSU for outbound connections.
SSU-over-IPv6 is supported as of version 0.9.8.

SSU (UDP seguro semifiable) se llama \"semifiable\" porque retransmitirá
repetidamente mensajes de no recibidos completamente, pero sólo hasta un
número máximo de veces. Después de esto, el mensaje es descartado.

## Servicios SSU

Al igual que el transporte NTCP, SSU proporciona un transporte de datos
de punto-a-punto, orientado a conexión, fiable y. A diferencia de SSU,
también proporciona detección de servicios de NAT transversales,
incluyendo:

- NAT/cortafuego trasversal cooperativo usando
 [introductores](#introduction)
- Detección de la IP local inspeccionado los paquetes de entrada y la
 [prueba de pares](#peerTesting)
- Comunicación del estado del cortafuegos y de la IP local, y los
 cambios en cualquiera de ellos a NTCP
- Coordinación del estado del cortafuegos y la IP local, y sus
 cambios, con el ruter y el interfaz del usuario

## [Especificación de dirección de router]{#ra}

Las siguientes propiedades se almacenan en la base de datos de red.

**Transport name:** SSU

**caps:** \[B,C,4,6\] [See below](#capabilities).

**host:** IP (IPv4 or IPv6). Shortened IPv6 address (with \"::\") is
allowed. May or may not be present if firewalled. Host names were
previously allowed, but are deprecated as of release 0.9.32. See
proposal 141.

**iexp\[0-2\]:** Expiration of this introducer. ASCII digits, in seconds
since the epoch. Only present if firewalled, and introducers are
required. Optional (even if other properties for this introducer are
present). As of release 0.9.30, proposal 133.

**ihost\[0-2\]:** Introducer\'s IP (IPv4 or IPv6). Host names were
previously allowed, but are deprecated as of release 0.9.32. See
proposal 141. Shortened IPv6 address (with \"::\") is allowed. Only
present if firewalled, and introducers are required.

Gracias a que SSU sólo necesita entrega semifiable, a una operativa
compatible con TCP, y a la capacidad para un alto rendimiento, esto
permite un amplio abanico de posibilidades en el control de congestión.
El algoritmo de control de congestión esbozado debajo está pensado para
ser tanto eficiente en ancho de banda, como fácil de implementar.

Los paquetes son programados de acuerdo con la política del ruter,
teniendo cuidado de no exceder la capacidad de salida del ruter o de
exceder la capacidad medida en el par remoto. La capacidad medida opera
según el inicio lento y la prevención de la congestión de TCP, con
aumentos que se suman a la capacidad de envío y disminuciones en caso de
congestión. Al contrario que TCP, algunos ruters pueden renunciar a
algunos mensajes despues de un periodo indicado o un número de
retransmisiones, mientras que continúa transmitiendo otros mensajes.

Las técnicas de detección de congestión tampoco son iguales a las de
TCP, ya que cada mensaje tiene su identificador único y no secuencial, y
cada mensaje tiene un tamaño limitado - como máximo, 32 KB. Para
transmitir eficientemente esta respuesta al remitente, el receptor
periódicamente incluye una lista de identificadores de mensaje
totalmente \'ACKed\' y también puede incluir campos de bits,
\'bitfields\', para los mensajes recibidos parcialmente, donde cada bit
representa la recogida de un fragmento. Si llegan fragmentos duplicados,
el mensaje deber ser \'ACKed\' de nuevo, o si el mensaje aún no ha sido
recibido en su totalidad, el bitfield debería ser retransmitido con
cualquier nuevo cambio.

La implementación actual no rellena los paquetes a un tamaño en
particular, en cambio simplemente coloca un solo fragmento de un mensaje
dentro de un paquete y lo envía para fuera (con cuidado de no exceder el
MTU).

### [MTU]{#mtu}

A partir de la versión del ruter 0.8.12 se usan dos valores de MTU para
IPv4: 620 y 1484. El valor del MTU es reajustado dependiendo del
porcentaje de paquetes que es retrasnmitido.

Para ambos valores MTU (unidad máxima de transmisión), es deseable que
(MTU % 16 == 12), así que la porción de la carga tras la cabecera de
28-bytes IP/UDP es un múltiplo de 16 bytes, para propositos de cifrado.

Para el valor más pequeño de MTU, es preferible empaquetar un mensaje de
construcción de túnel variable de 2646 bytes eficientemente dentro de
múltiples paquetes; el MTU de 620 bytes encaja bien dentro de 5
paquetes.

Basado en las mediciones, 1492 encaja en casi todos los mensajes I2NP
razonablemente pequeños (los mensajes I2NP más grandes pueden ser desde
1900 hasta 4500 bytes, que de todas formas no encajarían dentro del MTU
de la red).

Los valores del MTU eran 608 y 1492 para las versiones 0.8.9 - 0.8.11.
El MTU largo era de 1350 en las versiones anteriores a la 0.8.9.

Para la versión 0.8.12 el tamaño máximo del paquete recibido es de 1571
bytes. Para las versiones 0.8.9 - 0.8.11 era de 1535 bytes. Para las
versiones anteriores a 0.8.9 era de 2048 bytes.

A partir de la versión 0.9.2, si el MTU del interfaz de red del ruter es
menor de 1484, esto será publicado en la base de datos de la red, y los
otros ruters deberían respetarlo cuando una conexión es establecida.

Para IPv6, la MTU (unidad de transferencia máxima) es 1280. La cabecera
IP/UDP de IPv6 es de 48 bytes, así que usamos una MTU donde (MTN % 16 ==
0), lo que es cierto para 1280. El valor máximo de MTU de IPv6 is 1488
(el máximo era 1472 antes de la versión 0.9.28).

### [Límites de los tamaños de mensaje]{#max}

Mientras que normalmente el tamaño máximo de un mensaje es de 32KB, los
límites prácticos difieren. El protocolo limita el número de fragmentos
a 7 bits, o 128. La implementación actual limita cada mensaje a un
máximo de 64 fragmentos, lo cual es suficiente para, 64 \* 534 = 33.3
KB, cuando se usa el MTU de 608. Debido al gasto de las claves de sesión
y los LeaseSets incluidos, el límite práctico en el nivel de aplicación
es alrededor de 6KB menos, o alrededor de 26KB. Se necesita más trabajo
para poder aumentar el límite del transporte UDP por encima de 32KB.
Para las conexiones que usan un MTU más largo, son posibles mensajes más
largos.

## Periodo de inactividad

El periodo de inactividad y cierre de conexión se establece a discreción
de cada extremo, y puede variar. La actual implementación reduce el
periodo cuando el número de conexiones se aproxima al máximo
configurado, y eleva el periodo cuando el recuento de conexiones es
bajo. El periodo mínimo recomendado es de dos minutos o más, y el
periodo máximo recomendado es de diez minutos o más.

## [Claves]{#keys}

Todo el cifrado que se usa es AES256/CBC con claves de 32 bytes e IVs
(vectores de inicialización) de 16 bytes. Cuando Alice origina una
sesión con Bob, el MAC (código de autentificación de mensaje) y las
claves de sesión se negocian como parte de un intercambio DH
(Diffie-Hellman), y luego se usan respectivamente para el HMAC (MAC en
un hash cifrado) y el cifrado (de la comunicación). Durante el
intercambio DH, la introKey (clave de entrada) públicamente accesible de
Bob se usa para el MAC y el cifrado (de la comunicación).

Tanto el mensaje inicial como la subsiguiente respuesta usan la introKey
(clave de introducción) de quien responde - quien responde no necesita
conocer la introKey del solicitante (Alice). La clave de firmado DSA
usada por Bob ya debería ser conocida por Alice cuando ella contacte con
él, aunque la clave DSA de Alice puede que aún no sea concocida por Bob.

Tras recibir un mensaje, el destinatario comprueba la dirección IP y el
puerto \"desde\" de todas las sesiones establecidas - si hay
coincidencias, las claves MAC de sesión son probadas en el HMAC. Si
ninguna de esas se verifican, o si no coinciden con la IP, el receptor
prueba su introKey en el MAC, si esta no se verifica, el paquete es
denegado. Si se verifica, es interpretado de acuerdo el tipo de mensaje,
aunque si el destinatario está sobrecargado, puede que también sea
desechado.

Si Alice y Bob tienen una sesión establecida, pero Alice pierde las
claves por alguna razón y quiere contactar con Bob, ella puede
simplemente establecer una nueva sesión a través del SessionRequest y
los mensajes relacionados. Si Bob ha perdido la clave pero Alice no lo
sabe, ella primero intentará que le responda, y si Bob continúa sin
responder, ella asumirá que la clave se perdió y restablecerá una nueva.

For the DH key agreement, [RFC3526]() 2048bit
MODP group (#14) is used:

 p = 2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
 g = 2

These are the same p and g used for I2P\'s [ElGamal
encryption](#elgamal).

## [Prevención de Respuesta]{#replay}

La prevención de respuesta en la capa SSU ocurre denegando paquetes
excesivamente viejos o aquellos que reutilizan un IV. Para detectar IVs
duplicados, se utilizan una secuencia de filtros Bloom para
\"destruirlos\", y así sólo se detecten los IVs añadidos recientemente.

Los mensajesId usados en los DataMessages son definidos en capas por
encima del transporte SSU y son pasados a través transparentemente.
Estos IDs no están en un orden en particular - de hecho, es probable que
sean totalmente aleatorios. La capa SSU no intenta hacer prevención de
respuesta en los messageId - las capas superiores deberían tener esto en
cuenta.

## Direccionamiento {#addressing}

Para contactar un par SSU, se necesita uno de estos datos: una dirección
directa, para cuando el par sea accesible públicamente, o una dirección
indirecta, para usar a un tercero para que introduzca al par. No hay
restricción en el número de direcciones que un par puede tener.

 Direct: host, port, introKey, options Indirect: tag,
relayhost, port, relayIntroKey, targetIntroKey, options 

Cada una de las direcciones puede mostrar una serie de opciones -
capacidades especiales para un par en particular. Para una lista de
capacidades disponibles, vea [más abajo](#capabilities).

The addresses, options, and capabilities are published in the [network
database]().

## [Establecimiento de una sesión directa]{#direct}

El establecimiento de una sesión directa se usa cuando no hace falta un
tercero para el NAT trasversal. La secuencia del mensaje es como sigue:

### [Establecimiento de la conexión (directa)]{#establishDirect}

Alice conecta directamente con Bob. IPv6 está soportado desde la versión
0.9.8.

 Alice Bob SessionRequest
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-- SessionCreated
SessionConfirmed \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-- DeliveryStatusMessage
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-- DatabaseStoreMessage
DatabaseStoreMessage \-\-\-\-\-\-\-\-\-\-\-\-\-\--\> Data
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\> Data 

After the SessionConfirmed message is received, Bob sends a small
[DeliveryStatus message](#msg_DeliveryStatus)
as a confirmation. In this message, the 4-byte message ID is set to a
random number, and the 8-byte \"arrival time\" is set to the current
network-wide ID, which is 2 (i.e. 0x0000000000000002).

After the status message is sent, the peers usually exchange
[DatabaseStore messages](#msg_DatabaseStore)
containing their
[RouterInfos](#struct_RouterInfo),
however, this is not required.

No parece que importe el tipo del mensaje de estado o su contenidos . Se
añadió originalmente porque el mensaje DatabaseStore era retardado
varios segundos, desde que el mensaje es enviado inmediatamente, quizás
el mensaje de estado se pueda eliminar.

## [Introducción]{#introduction}

Introduction keys are delivered through an external channel (the network
database), where they have traditionally been identical to the router
Hash through release 0.9.47, but may be random as of release 0.9.48.
They must be used when establishing a session key. For the indirect
address, the peer must first contact the relayhost and ask them for an
introduction to the peer known at that relayhost under the given tag. If
possible, the relayhost sends a message to the addressed peer telling
them to contact the requesting peer, and also gives the requesting peer
the IP and port on which the addressed peer is located. In addition, the
peer establishing the connection must already know the public keys of
the peer they are connecting to (but not necessary to any intermediary
relay peer).

El establecimiento de sesiones indirectas por parte de un tercero es
necesario para el funcionamiento eficiente del NAT trasversal. Charlie,
un ruter tras un NAT o cortafuegos que no permite paquetes UDP no
solicitados de entrada, primero contacta con unos pocos pares, eligiendo
algunos para usarlos como introductores. Cada uno de estos pares (Bob,
Bill, Betty, etc) proporcionan a Charlie una etiqueta de introducción -
un número aleatorio de 4 bytes -la cual él después hace público como una
forma de contactarlo. Alice, un ruter que tiene publicado los métodos
para contactar con Charlie, primero envía un paquete RelayReques a uno o
más de los introductores, preguntando a cada uno para que le introduzca
a Charlie (ofreciendo la etiqueta de introducción para identificar a
Charlie). Bob entonces envía un paquete RelayIntro a Charlie incluyendo
el puerto y la IP pública de Charlie. Cuando Charlie recibe el paquete
RelayIntro, envía un pequeño paquete aleatorio al puerto e IP de Alice
(creando un agujero en su NAT/cortafuegos), y cuando Alice recibe el
paquete RelayResponse de Bob, ella empieza una establecimiento de sesión
completamente nuevo con el puerto y la IP especificados.

### [Establecimiento de la conexión (usando un introductor indirecto)]{#establishIndirect}

Alice primero se conecta al Bob introductor, que reenvía la petición a
Charlie.

 Alice Bob Charlie RelayRequest
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-- RelayResponse RelayIntro
\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
HolePunch (data ignored) SessionRequest
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
SessionCreated SessionConfirmed
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
DeliveryStatusMessage
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
DatabaseStoreMessage DatabaseStoreMessage
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
Data
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
Data 

Después de la creación del agujero en el NAT, la sesión es establecida
entre Alice y Charlie como si fuese directa.

### IPv6 Notes

IPv6 is supported as of version 0.9.8. Published relay addresses may be
IPv4 or IPv6, and Alice-Bob communication may be via IPv4 or IPv6.
Through release 0.9.49, Bob-Charlie and Alice-Charlie communication is
via IPv4 only. Relaying for IPv6 is supported as of release 0.9.50. See
the specification for details.

While the specification was changed as of version 0.9.8, Alice-Bob
communication via IPv6 was not actually supported until version 0.9.50.
Earlier versions of Java routers erroneously published the \'C\'
capability for IPv6 addresses, even though they did not actually act as
an introducer via IPv6. Therefore, routers should only trust the \'C\'
capability on an IPv6 address if the router version is 0.9.50 or higher.

## [Prueba del par]{#peerTesting}

La automatización del las pruebas colaborativas de accesibilidad de un
par es habilitada por una secuencia de mensajes PeerTest. Con su buen
funcionamiento, el par será capaz de determinar su estado de
accesibilidad y puede actualizar su comportamiento de acuerdo con ello.
El proceso de prueba es bastante simple:

 Alice Bob Charlie PeerTest
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
PeerTest\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--PeerTest
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--PeerTest
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--PeerTest
PeerTest\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--PeerTest


Cada uno de los mensajes PeerTest lleva un nonce identificando las
series de pruebas, como fueron inicializadas por Alice. Si Alice no
recibe un mensaje en particular que estuviese esperando, ella
retransmitirá de acuerdo con ello, y basándose en los datos recibidos o
en los mensajes perdidos, ella conocerá su estado de accesibilidad. Los
estados a los que puede llegar son:

- Si no recibe una respuesta de Bob, ella retransmitirá un número de
 veces dado, pero si nunca llega una respuesta, ella sabrá que su
 cortafuegos o NAT están desconfigurados de alguna forma, denegando
 todos los paquetes UDP de entrada incluso con una respuesta directa
 a un paquete de salida. Alternativamente, Bob puede estar caído o
 incapaz de hacer que Charlie responda.
- Si Alice no recibe un mensaje PeerTest con el nonce esperado de una
 tercera parte (Charlie), retransmitirá su petición inicial a Bob un
 cierto número de veces, incluso si ya ha recibido la respuesta de
 Bob. Si el primer mensaje de Charlie no pasa a través, pero el de
 Bob sí, ella sabe que está tras un NAT o cortafuegos que deniega los
 intentos de conexiones no solicitadas y que el reenvío de ese puerto
 no funciona correctamente (la IP y el puerto que Bob ofrece deberían
 estar reenviados/forwarded).
- Si Alice recibe el mensaje PeerTest de Bob y los dos mensajes
 PeerTest de Charle, pero la IP y el puerto de Bob adjuntos y el
 segundo mensaje de Charlie no coinciden, ella sabe que está bajo un
 NAT simétrico que está reescribiendo todos sus paquetes de salida
 con los puertos \'desde\' cambiados para cada uno de los pares
 contactados. Ella necesitará abrir explícitamente un puerto y tener
 ese puesto expuesto siempre a las conexiones remotas, ignorando
 cualquier búsqueda de puertos futura.
- Si Alice recibe el primer mensaje de Charlie pero no el segundo,
 ella retransmitirá su mensaje PeerTest a Charlie un cierto número de
 veces, pero si no se recibe ninguna respuesta sabrá que o Charlie
 está confundido o no está encendido.

Alice debería elegir a Bob arbitrariamente entre los pares conocidos que
parezcan ser capaces de participar el las pruebas de pares. Bob a su vez
debería elegir a Charlie arbitrariamente entre los pares conocidos que
parezcan ser capaces de participar el las pruebas de pares y que están
en una IP diferente a la de Bob y Alice. Si ocurre la primera condición
de error (Alice no recibe el mensaje PeerTest de Bob), Alice puede
decidir designar un nuevo par como Bob e intentar de nuevo con un nonce
diferente.

Alice\'s introduction key is included in all of the PeerTest messages so
that Charlie can contact her without knowing any additional information.
As of release 0.9.15, Alice must have an established session with Bob,
to prevent spoofing attacks. Alice must not have an established session
with Charlie for the peer test to be valid. Alice may go on to establish
a session with Charlie, but it is not required.

### IPv6 Notes

Through release 0.9.26, only testing of IPv4 addresses is supported.
Only testing of IPv4 addresses is supported. Therefore, all Alice-Bob
and Alice-Charlie communication must be via IPv4. Bob-Charlie
communication, however, may be via IPv4 or IPv6. Alice\'s address, when
specified in the PeerTest message, must be 4 bytes. As of release
0.9.27, testing of IPv6 addresses is supported, and Alice-Bob and
Alice-Charlie communication may be via IPv6, if Bob and Charlie indicate
support with a \'B\' capability in their published IPv6 address. See
[Proposal 126](/spec/proposals/126-ipv6-peer-testing) for details.

Prior to release 0.9.50, Alice sends the request to Bob using an
existing session over the transport (IPv4 or IPv6) that she wishes to
test. When Bob receives a request from Alice via IPv4, Bob must select a
Charlie that advertises an IPv4 address. When Bob receives a request
from Alice via IPv6, Bob must select a Charlie that advertises an IPv6
address. The actual Bob-Charlie communication may be via IPv4 or IPv6
(i.e., independent of Alice\'s address type).

As of release 0.9.50, If the message is over IPv6 for an IPv4 peer test,
or (as of release 0.9.50) over IPv4 for an IPv6 peer test, Alice must
include her introduction address and port. See [Proposal
158](/spec/proposals/158) for details.

## [Window,ventana, de retransmisión, ACKs y Retrasmisiones]{#acks}

The DATA message may contain ACKs of full messages and partial ACKs of
individual fragments of a message. See the data message section of [the
protocol specification page]() for details.

The details of windowing, ACK, and retransmission strategies are not
specified here. See the Java code for the current implementation. During
the establishment phase, and for peer testing, routers should implement
exponential backoff for retransmission. For an established connection,
routers should implement an adjustable transmission window, RTT estimate
and timeout, similar to TCP or [streaming]().
See the code for initial, min and max parameters.

## [Seguridad]{#security}

La dirección de la fuente UDP puede, por supuesto, ser falseada.
Adicionalmente, las IPs y los puertos contenidos en los mensajes SSU
específicos (RelayRequest, RelayResponse, RelayIntro, PeerTest) puede
que no sean legítimos. Además, algunas acciones y respuestas pueden
necesitar de ser vueltas a limitar.

Los detalles de validación no están especificados aquí. Los
desarrolladores deberían añadir defensas donde sea apropiado.

## [Capacidades del par]{#capabilities}

One or more capabilities may be published in the \"caps\" option.
Capabilities may be in any order, but \"BC46\" is the recommended order,
for consistency across implementations.

B
: Si la dirección del par contiene la capacidad \'B\', esto significa
 que desea y puede participar en una prueba de par como un \'Bob\' o
 como un \'Charlie\'. Through 0.9.26, peer testing was not supported
 for IPv6 addresses, and the \'B\' capability, if present for an IPv6
 address, must be ignored. As of 0.9.27, peer testing is supported
 for IPv6 addresses, and the presence or absense of the \'B\'
 capability in an IPv6 address indicates actual support (or lack of
 support).

C
: If the peer address contains the \'C\' capability, that means they
 are willing and able to serve as an introducer via that address -
 serving as an introducer Bob for an otherwise unreachable Charlie.
 Prior to release 0.9.50, Java routers incorrectly published the
 \'C\' capability for IPv6 addresses, even though IPv6 introducers
 was not fully implemented. Therefore, routers should assume that
 versions prior to 0.9.50 cannot act as an introducer over IPv6, even
 if the \'C\' capability is advertised.

4
: As of 0.9.50, indicates outbound IPv4 capability. If an IP is
 published in the host field, this capability is not necessary. If
 this is an address with introducers for IPv4 introductions, \'4\'
 should be included. If the router is hidden, \'4\' and \'6\' may be
 combined in a single address.

6
: As of 0.9.50, indicates outbound IPv6 capability. If an IP is
 published in the host field, this capability is not necessary. If
 this is an address with introducers for IPv6 introductions, \'6\'
 should be included (not currently supported). If the router is
 hidden, \'4\' and \'6\' may be combined in a single address.

# [Trabajo futuro]{#future}

Note: These issues will be addressed in the development of SSU2.

- El análisis del rendimiento actual del SSU es un tema para un
 trabajo futuro, incluyendo la valoración del ajuste del tamaño de
 ventana y otros parámetros, y el ajuste de la implementación del
 protocolo para mejorar el rendimiento.
- La implementación actual envía repetidamente reconocimientos para
 los mismos paquetes, lo que aumenta la sobrecarga innecesariamente.
- El pequeño valor por defecto del MTU de 620 debería ser analizado y
 probablemente aumentado. La estrategia actual de adaptación del MTU
 debería ser evaluada. ¿Cabe un paquete de streaming de 1730 bytes en
 3 paquetes pequeños SSU? Probablemente no.
- El protocolo debería ser ampliado para intercambiar MTUs durante la
 configuración.
- Rekeying is currently unimplemented and will never be.
- El uso potencial de los campos \"desafío\" en el RelayIntro y en el
 RelayResponse, y el uso del campo de relleno en el SessionRequest en
 el SessionCreated, no están documentados.
- Un conjunto de tamaños de paquetes podría ser apropiado para la
 ocultación futura de la fragmentación de los datos a adversarios
 externos, pero el túnel, garlic, y un relleno de fin a fin deberían
 ser suficiente para la mayoría de las necesidades hasta entonces.
- Los tiempos acordados en SessionCreated (sesión creada) y
 SessionConfirmed (sesión confirmada) parecen estar sin usar o
 verificar.

# Diagrama de implementación

El diagrama debe reflejar con exactitud la implementación actual, sin
embargo puede haber muchas diferencias pequeñas.

![](images/udp.png)

# [Especificación]{#spec}

[En la actualidad en la página de especificación SSU (UDP seguro
semiconfiable)](). 
