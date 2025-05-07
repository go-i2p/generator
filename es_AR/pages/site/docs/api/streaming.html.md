 Streaming
Protocol 2024-09 0.9.64 

## Información general

The streaming library is technically part of the \"application\" layer,
as it is not a core router function. In practice, however, it provides a
vital function for almost all existing I2P applications, by providing a
TCP-like streams over I2P, and allowing existing apps to be easily
ported to I2P. The other end-to-end transport library for client
communication is the [datagram library]().

The streaming library is a layer on top of the core [I2CP
API]() that allows reliable, in-order, and
authenticated streams of messages to operate across an unreliable,
unordered, and unauthenticated message layer. Just like the TCP to IP
relationship, this streaming functionality has a whole series of
tradeoffs and optimizations available, but rather than embed that
functionality into the base I2P code, it has been factored off into its
own library both to keep the TCP-esque complexities separate and to
allow alternative optimized implementations.

En consideración al relativamente alto coste de los mensajes, el
protocolo de la librería streaming para programar y entregar esos
mensajes ha sido optimizado para permitir que los mensajes individuales
pasen a contener tanta información como esté disponible. Por ejemplo,
una pequeña transacción HTTP proxificada a través de la librería
streaming puede ser completada en un sólo viaje de ida y vuelta - los
primeros mensajes empaquetan un SYN, FIN, y la pequeña carga de la
petición HTTP, y la respuesta empaqueta el SYN, FIN, ACK, y la carga de
la respuesta HTTP. Aunque un ACK adicional debe ser transmitido para
decirle al servidor HTTP que el SYN/FIN/ACK ha sido recibido, el proxy
HTTP local a menudo puede entregar la respuesta completa de forma
inmediata al navegador.

La librería streaming presenta mucha semejanza a una abstracción de TCP,
con sus ventanas (de protocolo) deslizantes, algoritmos de control de
congestión (tanto de inicio lento como de elusión de congestión), y
comportamiento general del paquete (ACK, SYN, FIN, RST, cálculo RTO,
etc.).

La librería streaming es una librería robusta que está optimizada para
operar sobre I2P. Tiene una instalación de fase-única, y contiene una
implementación de ventanización (protocolo) completa.

## API

The streaming library API provides a standard socket paradigm to Java
applications. The lower-level [I2CP]() API is
completely hidden, except that applications may pass [I2CP
parameters](#options) through the streaming
library, to be interpreted by I2CP.

The standard interface to the streaming lib is for the application to
use the [I2PSocketManagerFactory]() to create
an [I2PSocketManager](). The application then
asks the socket manager for an [I2PSession](),
which will cause a connection to the router via
[I2CP](). The application can then setup
connections with an [I2PSocket]() or receive
connections with an [I2PServerSocket]().

Here are the [full streaming library Javadocs]().

Para ver un buen ejemplo de uso, vea el código de i2psnark.

### Opciones y valores predeterminados {#options}

The options and current default values are listed below. Options are
case-sensitive and may be set for the whole router, for a particular
client, or for an individual socket on a per-connection basis. Many
values are tuned for HTTP performance over typical I2P conditions. Other
applications such as peer-to-peer services are strongly encouraged to
modify as necessary, by setting the options and passing them via the
call to
[I2PSocketManagerFactory]().createManager(\_i2cpHost,
\_i2cpPort, opts). Time values are in ms.

Note that higher-layer APIs, such as [SAM](),
[BOB](), and
[I2PTunnel](), may override these defaults
with their own defaults. Also note that many options only apply to
servers listening for incoming connections.

Desde la versión 0.9.1 la mayoría de las opciones, pero no todas, pueden
ser cambiadas en un administrador de socket activo o sesión. Vea los
Javadocs para más detalles.

 Option Default Notes
 --------------------------------------------------- ------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 i2cp.accessList null Lista separada por comas - o espacios - de hashes de pares (\`peers\`) Base64 usada bien como lista de acceso, o como lista negra. As of release .
 i2cp.destination.sigType DSA_SHA1 Usar la lista de acceso como lista blanca para conexiones entrantes. El nombre o número del tipo de firma para un destino pasajero As of release .
 i2cp.enableAccessList false Usar la lista de acceso como lista blanca para conexiones entrantes. As of release .
 i2cp.enableBlackList false Usar la lista de acceso como lista negra para conexiones entrantes. As of release .
 i2p.streaming.answerPings true Responder o no a los pings entrantes.
 i2p.streaming.blacklist null Lista separada por comas - o espacios - de hashes de pares (\`peers\`) Base64 que sera usada como lista negra para las conexiones entrantes a TODOS los destinos en el contexto. Esta opción debe ser configurada en las propiedades contextuales, NO en el argumento createManager() de las opciones. Observe que establecer esto en el contexto del router no afectará a clientes fuera del router en una JVM y contexto aparte. As of release .
 i2p.streaming.bufferSize 64K Cuántos datos de transmisión (en bytes) serán aceptados que no hayan sido emitidos aún.
 i2p.streaming.congestionAvoidanceGrowthRateFactor 1 Cuando estamos evitando la congestión, aumentamos el tamaño de la ventana (protocolo) al ritmo de `1/(tamañodeventana*factor)`. En TCP estándar, los tamaños de ventana se miden en bytes, mientras que en I2P los tamaños de ventana se miden en mensajes. Un número más alto significa un crecimiento más lento.
 i2p.streaming.connectDelay -1 Cuánto esperar después de crear una instancia de nueva conexión antes de intentar conectar realmente. Si esto es \<= 0 conecta inmediatamente sin datos inciales. Si es mayor que 0, espera hasta que la salida del flujo de datos (\`stream\`) sea evacuada, se llene el buffer, o que pasen muchos milisegundos, e incluye cualquier dato inicial con el SYN.
 i2p.streaming.connectTimeout 5\*60\*1000 Durante cuánto bloquear al conectar, en milisegundos. Valores negativos significan indefinidamente. El valor predeterminado es 5 minutos.
 i2p.streaming.disableRejectLogging false Desactivar o no las advertencias en los registros (\`logs\`), cuando se rechaza una conexión entrante debido a los límites de la conexión. As of release .
 i2p.streaming.dsalist null Lista separada por comas/espacios de identificadores criptográficos Base64 de pares (peer hashes) o nombres de nodos, a ser conectados usando un destino DSA alternativo. Sólo se aplica si está habilitada la multisesión y la sessión primaria es no-DSA (generalmente sólo para clientes compartidos). Esta opción se debe establecer en las propiedades de contexto, NO en el argumento de las opciones de createManager() . Observe que estableciendo esto en el contexto del router I2P no afectará a los a los clientes fuera de este en una JVM y contexto aparte. As of release .
 i2p.streaming.enforceProtocol true Escuchar o no sólo el protocolo streaming. Configurando a verdadero (\`true\`) prohibirá la comunicación con Destinos que usen una versión más temprana que la 0.7.1 (publicada en marzo de 2009). Configure a verdadero si ejecuta múltiples protocolos sobre este Destino. As of release . Default true as of release 0.9.36.
 i2p.streaming.inactivityAction 2 (send) (0=nada, 1=desconectar) Qúe hacer durante un periodo de inactividad - no hacer nada, desconectar, o enviar un ACK duplicado.
 i2p.streaming.inactivityTimeout 90\*1000 Tiempo de inactividad antes de enviar un keepalive (mantener viva)
 i2p.streaming.initialAckDelay 750 Retardo antes de enviar un ack (acuse de recibo)
 i2p.streaming.initialResendDelay 1000 El valor incial del campo de demora del reenvío en la cabecera del paquete, marca 1000. No está implementado completamente; vea debajo.
 i2p.streaming.initialRTO 9000 Tiempo límite inicial (si no hay [datos compartidos](#sharing) disponibles). As of release .
 i2p.streaming.initialRTT 8000 Estimación de (RTT/RTD) tiempo de viaje de ida y vuelta (si no hay [datos compartidos](#sharing) disponibles). Deshabilitado desde la versión 0.9.8; usa el RTT real.
 i2p.streaming.initialWindowSize 6 (si no hay [datos compatidos](#sharing) disponibles) En TCP estándar, los tamaños de las ventanas se miden en bytes, mientras que en I2P los tamaños de las ventanas se miden en mensajes.
 i2p.streaming.limitAction reset What action to take when an incoming connection exceeds limits. Valid values are: reset (reset the connection); drop (drop the connection); or http (send a hardcoded HTTP 429 response). Any other value is a custom response to be sent. backslash-r and backslash-n will be replaced with CR and LF. As of release .
 i2p.streaming.maxConcurrentStreams -1 (0 o valores negativos significan ilimitado) Esto es un límite total para la combinación entrante y saliente.
 i2p.streaming.maxConnsPerMinute 0 Límite de conexión entrante (por pares (\'peer\`); 0 significa deshabilitado) As of release .
 i2p.streaming.maxConnsPerHour 0 (por pares (\`peer\`); 0 significa deshabilitado) As of release .
 i2p.streaming.maxConnsPerDay 0 (por pares (\`peer\`); 0 significa deshabilitado) As of release .
 i2p.streaming.maxMessageSize 1730 The maximum size of the payload, i.e. the MTU in bytes.
 i2p.streaming.maxResends 8 Número máximo de retransmisiones antes de fallo.
 i2p.streaming.maxTotalConnsPerMinute 0 Límite de conexión entrante (todos los pares (\`peers\`); 0 significa deshabilitado) As of release .
 i2p.streaming.maxTotalConnsPerHour 0 (todos los pares (\`peers\`); 0 significa deshabilitado) Usar con precaución ya que exceder esto deshabilitará un servidor por un largo periodo. As of release .
 i2p.streaming.maxTotalConnsPerDay 0 (todos los pares (\`peers\`); 0 significa deshabilitado) Usar con precaución ya que exceder esto deshabilitará un servidor por un largo periodo. As of release .
 i2p.streaming.maxWindowSize 128 
 i2p.streaming.profile 1 (bulk) 1=bulk; 2=interactive; see important notes [below](#profile).
 i2p.streaming.readTimeout -1 Durante cuánto bloquear al leer, en milisegundos. Valores negativos significan indefinidamente.
 i2p.streaming.slowStartGrowthRateFactor 1 Cuando estemos en un inicio lento, elevaremos el tamaño de la ventana (del protocolo) a un ritmo de 1/(factor). En TCP estándar, los tamaños de ventana se miden en bytes, mientras que en I2P los tamaños de ventana se miden en mensajes. Un número más alto significa un crecimiento más lento.
 i2p.streaming.tcbcache.rttDampening 0.75 Ref: RFC 2140. Valor del punto flotante. Puede ser establecido sólo mediante las propiedades contextuales, no las opciones de conexión As of release .
 i2p.streaming.tcbcache.rttdevDampening 0.75 Ref: RFC 2140. Valor del punto flotante. Puede ser establecido sólo mediante las propiedades contextuales, no las opciones de conexión As of release .
 i2p.streaming.tcbcache.wdwDampening 0.75 Ref: RFC 2140. Valor del punto flotante. Puede ser establecido sólo mediante las propiedades contextuales, no las opciones de conexión As of release .
 i2p.streaming.writeTimeout -1 Durante cuánto bloquear al escribir/limpiar, en milisegundos. Los valores negativos significan indefinidamente.

## Especificación del protocolo

[Vea la página Especificación de la librería
streaming.]()

## Detalles de la implementación

### Instalar

El iniciador envía un paquete con el distintitivo SYNCHRONIZE
(sincronizar) establecido. Este paquete puede contener también los datos
iniciales. El par (\`peer\`) responde con un paquete con el distintivo
SYNCHRONIZE establecido. Este paquete puede contener también los datos
de respuesta iniciales

El iniciador puede enviar paquetes de datos adicionales, hasta el tamaño
de ventana inicial, antes de recibir la respuesta SYNCHRONIZE. Estos
paquetes también tendrán el campo \`envíar Identificador de Stream\`
establecido a 0. Los receptores deben guardar en el buffer los paquetes
recibidos sobre flujos (\`streams\`) desconocidos durante un periodo
corto de tiempo, ya que pueden llegar estropeados, adelantándose al
paquete SYNCHRONIZE.

### Selección y negociación MTU

El máximo tamaño de mensaje (también llamado MTU / MRU) es negociado al
menor valor soportado por los dos pares (\`peers\`). Como los mensajes
túnel están acotados a 1KB, una elección MTU pobre llevaría a una gran
cantidad de tráfico de control. La MTU está especificada por la opción
i2p.streaming.maxMessageSize. La MTU está especificada por la opción
i2p.streaming.maxMessageSize. La MTU actual por defecto de 1720 fue
elegida para encajar precisamente en dos mensajes túnel I2NP de 1K,
incluyendo el tráfico de control para un caso típico. Note: This is the
maximum size of the payload only, not including the header.

Note: For ECIES connections, which have reduced overhead, the
recommended MTU is 1812. The default MTU remains 1730 for all
connections, no matter what key type is used. Clients must use the
minimum of the sent and received MTU, as usual. See proposal 155.

El primer mensaje en una conexión incluye un Destino de 387 bytes
(típico) añadido por la capa streaming, y usualmente un LeaseSet (todos
los leases o túneles autorizados a recibir conexiones para un destino
concreto) de 898 bytes (típico), y claves de Sesión, empaquetadas en un
mensaje Ajo (\`Garlic\`) por el router (El LeaseSet y las Claves de
Sesión no serán empaquetadas si se estableció previamente una Sesión
ElGamal). Por lo tanto, la meta de encajar una petición HTTP completa en
un sólo mensaje I2NP (I2P Network Protocol) de 1KB no siempre es
alcanzable. Sin embargo, la elección de MTU, junto con una cuidadosa
implementación de fragmentación y estrategias de elaboración de lotes en
el procesador del túnel de la pasarela de salida (\`gateway\`), son
factores importantes en el ancho de banda, latencia, fiabilidad y
eficiencia de la red, especialmente para conexión de vida-larga.

### Integridad de los datos

Data integrity is assured by the gzip CRC-32 checksum implemented in
[the I2CP layer](#format). There is no checksum
field in the streaming protocol.

### Encapsulado de paquetes

Each packet is sent through I2P as a single message (or as an individual
clove in a [Garlic Message]()). Message
encapsulation is implemented in the underlying
[I2CP](), [I2NP](), and
[tunnel message]() layers. There is no
packet delimiter mechanism or payload length field in the streaming
protocol.

### Retardo opcional

Los paquetes de datos pueden incluir un campo opcional de retardo que
especifica el retardo solicitado en ms hasta que el receptor deba emitir
un ack (acuse de recibo) del paquete. Los valores válidos van de 0 a
60000 ambos incluidos. Un valor de 0 solicita un ack inmediato. Esto
sólo es un valor aconsejado, los receptores deben usar un ligero retardo
para que se pueda acusar recibo de paquetes adicionales con un único
ack. Algunas implementaciones pueden incluir un valor aconsejado de
\[RTT (tiempo de ida y vuelta) medido / 2\] en este campo. Para valores
opcionales de retardo distintos de cero, los receptores deben limitar a
unos pocos segundos como mucho el retardo máximo antes de enviar un ack.
Los valores de retardo mayores a 60000 indican taponamiento, vea debajo.

### Ventana de recepción y taponamiento

Las cabeceras TCP incluyen la \'ventana de recepción\' en bytes. El
protocolo de transporte streaming no contiene una ventana de recepción,
sólo usa un única indicación de taponamiento/no-taponamiento. Cada
extremo debe mantener su propia estimación de la ventana de recepción
del otro extremo, bien en bytes o en paquetes. El tamaño mínimo
recomendado del buffer para implementaciones de receptor es de 128
paquetes o 217 KB (aproximadamente 128x1730). A causa de la latencia de
la red I2P, la pérdida de paquetes, y el control de la congestión
resultante, un buffer de este tamaño raramente se llena. Sin embargo, el
desbordamiento es probable que ocurra en conexiones \"local loopback\"
(del propio router I2P a si mismo) de alto ancho de banda.

Para indicar con rapidez el estado de desbordamiento, y recuperarse de
este sin dificultad, hay un mecanismo simple para la reversión en el
protocolo de transporte streaming. Si se recibe un paquete con un un
campo opcional de retardo de valor 60001 o superior, eso indica
\"taponamiento\" o una ventana de recepción de cero. Un paquete con un
campo opcional de retardo de valor 60000 o menos indica
\"destaponamiento\". Los paquetes sin un campo opcional de retardo no
afectan al estado de taponamiento/destaponamiento.

Después de que sea taponado, no se deben enviar más paquetes con datos
hasta que el transmitente sea destaponado, excepto para paquetes de
datos \"sonda\" ocasionales para compensar posibles paquetes de
destaponamiento perdidos. El extremo taponado debe iniciar un
\"cronómetro de persistencia\" para controlar el sondeado, como en TCP.
El extremo que se esté destaponando debe enviar varios paquetes con este
campo de retardo establecido, o continuar enviándolos periódicamente
hasta que se reciban de nuevo paquetes de datos. El tiempo de espera
máximo para el destaponamiento depende de la implementación El tamaño de
ventana de recepción del transmitente y la estrategia de control de
congestión de este tras ser destaponado dependen de la implementación.

### Control de la congestión

La librería streaming utiliza fases estándar de inicio-lento
(crecimiento exponencial de la ventana (del protocolo)) y de elusión de
congestión (crecimiento lineal de la ventana), con retroceso
exponencial. La ventanización y los acuses de recibo
(\'acknowledments\') cuentan paquetes, no bytes.

### Cerrar

Cualquier paquete, incluyendo uno con el distintivo SYNCHRONIZE
establecido, puede haber enviado también el distintivo CLOSE. La
conexión no está cerrada hasta que el par (\`peer\`) responde con el
distintivo CLOSE. Los paquetes CLOSE también pueden contener datos.

### Ping / Pong

No hay función de ping en la capa I2CP (equivalente a ICMP echo) o en
los datagramas. Esta función se proporciona en el transporte streaming.
Los pings y pongs pueden no estar combinados con un paquete streaming
estándar; si la opción ECHO está establecida, entonces la mayoría del
resto de indicativos, opciones, ackThrough, sequenceNum, NACKs, etc. se
ignoran.

Un paquete de ping debe tener establecidos los indicadores ECHO (eco),
SIGNATURE_INCLUDED (firma incluida), y FROM_INCLUDED (origen incluido).
El sendStreamId (identificador de stream de envío) puede o no
corresponder con una conexión existente.

Un paquete pong debe tener el indicador ECHO establecido. El
sendStreamId debe ser cero, y el receiveStreamId es el sendStreamId del
ping. Antes de la versión 0.9.18, el paquete pong no incluye ningún
cargamento que estuviera contenido en el ping.

Desde la versión 0.9.18 los pings y pongs puede que contengan un
cargamento. El cargamento en el ping, hasta un máximo de 32 bytes, es
devuelto en el pong.

El protocolo de streaming puede ser configurado para deshabilitar el
envío de pongs con la configuración i2p.streaming.answerPings=false .

### i2p.streaming.profile Notes {#profile}

This option supports two values; 1=bulk and 2=interactive. The option
provides a hint to the streaming library and/or router as to the traffic
pattern that is expected.

\"Bulk\" means to optimize for high bandwidth, possibly at the expense
of latency. This is the default. \"Interactive\" means to optimize for
low latency, possibly at the expense of bandwidth or efficiency.
Optimization strategies, if any, are implementation-dependent, and may
include changes outside of the streaming protocol.

Through API version 0.9.63, Java I2P would return an error for any value
other than 1 (bulk) and the tunnel would fail to start. As of API
0.9.64, Java I2P ignores the value. Through API version 0.9.63, i2pd
ignored this option; it is implemented in i2pd as of API 0.9.64.

While the streaming protocol includes a flag field to pass the profile
setting to the other end, this is not implemented in any known router.

### Compartición del bloque de control {#sharing}

La librería streaming (de flujo) soporta compartición del Bloque de
Control \"TCP\" (protocolo de control de transmisiones). Esto comparte
tres importantes parámetros de la librería streaming (tamaño de la
ventana, tiempo de viaje de ida y vuelta (RTT/RTD), variación del RTT)
entre las conexiones al mismo par (\`peer\`) remoto. Esto se usa para la
compartición \"temporal\" en el momento de apertura/cierre de la
conexión, no para la compartición \"coral\" durante una conexión (Vea
[RFC 2140](http://www.ietf.org/rfc/rfc2140.txt)). Hay una compartición
separada por ConnectionManager (administrador de conexión) (ej: por
destino local), así que no hay información sobre filtraciones a otros
destinos en el mismo router. Los datos compartidos para un par
(\`peer\`) dado expiran después de unos pocos minutos. Los siguientes
parámetros de Compartición del Bloque de Control pueden ser establecidos
en cada router.

- RTT_DAMPENING = 0.75
- RTTDEV_DAMPENING = 0.75
- WINDOW_DAMPENING = 0.75

### Otros parámetros {#other}

Los siguientes parámetros son internos, pero pueden ser de interés para
el análisis:

- MIN_RESEND_DELAY = 100 ms (minimum RTO)
- MAX_RESEND_DELAY = 45 sec (maximum RTO)
- MIN_WINDOW_SIZE = 1
- TREND_COUNT = 3
- MIN_MESSAGE_SIZE = 512 (minimum MTU)
- INBOUND_BUFFER_SIZE = maxMessageSize \* (maxWindowSize + 2)
- INITIAL_TIMEOUT (valid only before RTT is sampled) = 9 sec
- \"alpha\" ( RTT dampening factor as per RFC 6298 ) = 0.125
- \"beta\" ( RTTDEV dampening factor as per RFC 6298 ) = 0.25
- \"K\" ( RTDEV multiplier as per RFC 6298 ) = 4
- PASSIVE_FLUSH_DELAY = 175 ms
- Maximum RTT estimate: 60 sec

### Historial

La librería streaming ha crecido orgánicamente para I2P - primero mihi
implementó la \"librería mini streaming\" como parte de I2PTunnel, que
estaba limitada a un tamaño de ventana de 1 mensaje (requiriendo un ACK
antes de enviar el siguiente), y entonces fue desgajado en una interfaz
streaming genérica (a semejanza de los sockets TCP) y la implementación
streaming completa fue desplegada con un protocolo de ventanas
deslizantes y optimizaciones para tener en cuenta el alto valor del
producto (ancho-de-banda x demora). Los flujos (\`streams\`)
individuales pueden ajustar su tamaño máximo de paquete y otras
opciones. El tamaño predeterminado del mensaje se selecciona para
encajar de forma precisa en dos mensajes túnel I2NP (I2P Network
Protocol) de 1KB, y es un compromiso de equilibrio razonable entre el
coste en ancho de banda de retransmitir mensajes perdidos, y la latencia
y tráfico de control de múltiples mensajes.

## Trabajo futuro {#future}

El comportamiento de la librería streaming tiene un profundo impacto
sobre el rendimiento en el nivel-aplicación, y como tal, es un área
importante para análisis detallados.

- Podrían ser necesarios ajustes adicionales de los parámetros de
 librería streaming.
- Another area for research is the interaction of the streaming lib
 with the NTCP and SSU transport layers. See [the NTCP discussion
 page]() for details.
- La interacción de los algoritmos de enrutado con la librería
 streaming afecta fuertemente al rendimiento. En particular, la
 distribución aleatoria de mensajes a múltiples túneles entre los que
 están en depósito, lleva a un alto grado de entregas estropeadas que
 resultan en tamaños de ventana más pequeños de lo que serían en otro
 caso. Actualmente el router enruta mensajes para un único par
 desde/hacia el destino a través de un conjunto consistente de
 túneles, hasta la expiración del túnel o un fallo en la entrega. El
 fallo del router y los algoritmos de selección del túnel deben ser
 revisados en busca de posibles mejoras.
- Los datos en el primer paquete SYN (sincronizar) pueden exceder la
 MTU (Unidad Máxima de Transporte) del receptor.
- El campo DELAY_REQUESTED (demora requerida) podría ser usado más.
- Los paquetes iniciales SYNCHRONIZE duplicados sobre streams de
 vida-corta pueden ser no reconocidos y eliminados.
- No envía la MTU en una retransmisión.
- Los datos se envían al recorrido a menos que la ventana de salida
 esté llena (es decir sin-Nagle o TCP_NODELAY). Probablemente debe
 haber una opción de configuración para esto.
- zzz ha añadido código de depuración a la librería streaming para
 registrar (\`log\`) paquetes en un formato compatible-wireshark
 (pcap); utilice esto para analizar el rendimiento con mayor detalle.
 El formato puede requerir mejoras para mapear más parámetros de
 librería streaming en campos TCP.
- Hay propuestas para reemplazar la librería streaming con TCP
 estándar (o quizá con una capa vacía junto con sockets crudos
 (\`raw\`)). Desafortunadamente esto sería incompatible con la
 librería streaming pero sería bueno para comparar el rendimiento de
 los dos.


