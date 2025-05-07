 Protocolo de red
I2P (I2NP) October 2018 0.9.37 

El protocolo de red de I2P (I2NP), el cual está intercalado entre I2CP
(Protocolo de Cliente I2P) y los diferentes protocolos de transporte
I2P, administra el enrutado y mezclado de los mensajes entre routers,
así como la seleccion de qué transportes se usan cuando se comunica con
un par (\`peer\`) para el que hay múltiples transportes comunes
soportados.

### Definición de I2NP

Los mensajes I2PN (Protocolo de red I2P) pueden usarse para los mensajes
punto a punto, router a router, de un solo salto. Al cifrar y envolver
los mensajes dentro de otros mensajes, pueden ser enviados de forma
segura a través de múltiples saltos hasta el destino final. Las
prioridades sólo se usan localmente, en el origen, es decir cuando se
hacen colas para entregas salientes.

The priorities listed below may not be current and are subject to
change. See the [OutNetMessage
Javadocs]() for the current priority
settings. Priority queueing implementation may vary.

### Formato del mensaje

The following table specifies the traditional 16-byte header used in
NTCP. The SSU and NTCP2 transports use modified headers.

 Campo Bytes
 -------------------- ------------
 Tipo 1
 ID único 4
 Expiración 8
 Tamaño de la carga 2
 Checksum 1
 Carga 0 - 61.2KB

While the maximum payload size is nominally 64KB, the size is further
constrained by the method of fragmenting I2NP messages into multiple 1KB
tunnel messages as described on [the tunnel implementation
page](). The maximum number of fragments is
64, and the message may not be perfectly aligned, So the message must
nominally fit in 63 fragments.

El tamaño máximo de un fragmento inicial es de 956 bytes (asumiendo el
modo de entrega del TÚNEL); el tamaño máximo de un fragmento de
continuación es de 996 bytes. Por lo tanto el tamaño máximo es de
aproximadamente 956 + (62 \* 996) = 62708 bytes, o 61,2 KB.

In addition, the transports may have additional restrictions. The NTCP
limit is 16KB - 6 = 16378 bytes. The SSU limit is approximately 32 KB.
The NTCP2 limit is approximately 64KB - 20 = 65516 bytes, which is
higher than what a tunnel can support.

Observe que estos no son los límites para datagramas que el cliente ve,
ya que el router puede empaquetar juntos un LeaseSet (grupo de túneles
para un destino) de repuesta y/o etiquetas de sesión, junto con el
mensaje del cliente, en un mensaje garlic (ajo). El LeaseSet y las
etiquetas juntas pueden añadir unos 5,5 KB. Por lo tanto el límite de
datagrama actual es de alrededor de 10 KB. Este límite se incrementará
en una versión futura.

### Tipos de mensajes

Las prioridades numeradas-más-elevadas, son prioridades más altas. La
mayoría del tráfico son TunnelDataMessages (Mensajes de Datos de Túnel,
prioridad 400), así que cualquier cosa por encima de 400 es
esencialmente de alta prioridad, y cualquier cosa por debajo es de baja
prioridad. Observe también que muchos de los mensajes están por lo
general enrutados a través de túneles exploratorios, no túneles de
cliente, y por lo tanto pueden no estar en la misma cola a menos que los
primeros saltos resulte que se produzcan en el mismo par (\`peer\`).

Además, no todos los tipos de mensaje se envían sin encriptar. Por
ejemplo, cuando probamos un túnel, el router envuelve un
DeliveryStatusMessage (mensaje de estado de la entrega), que es envuelto
a su vez en un GarlicMessage (mensaje ajo), que a su vez es envuelto en
un DataMessage (mensaje de datos).

Mensaje

Tipo

Tamaño de la carga

Prioridad

Comentarios

DatabaseLookupMessage

2

 

500

Puede variar

DatabaseSearchReplyMessage

3

Typ. 161

300

El tamaño es 65 + 32\*(número de hashes) donde típicamente, los hashes
(identificadores criptográficos) para tres routers de inundación
(\`floodfill\`) son devueltos.

DatabaseStoreMessage

1

Varía

460

La prioridad puede variar. El tamaño es de 898 bytes para un LeaseSet de
2-leases (túneles hacia un destino) típico. Las estructuras de
RouterInfo están comprimidas, y el tamaño varía, sin embargo hay un
esfuerzo continuo para reducir la cantidad de datos publicados en
RouterInfo al aproximarnos a la versión 1.0.

DataMessage

20

4 - 62080

425

La prioridad puede variar dependiendo del destino.

DeliveryStatusMessage

10

12

 

Usado para respuestas de mensaje, y para probar túneles - por lo general
envuelto en un GarlicMessage (mensaje ajo).

[GarlicMessage](#op.garlic)

11

 

 

Envuelto por lo general en un DataMessage (mensaje de datos) - pero
cuando está desenvuelto, se le da una prioridad de 100 por el router
reenviante.

[TunnelBuildMessage](#tunnelCreate.requestRecord)

21

4224

500

[TunnelBuildReplyMessage](#tunnelCreate.replyRecord)

22

4224

300

TunnelDataMessage

18

1028

400

El mensaje más común. La prioridad para participantes en el túnel,
extremos de salida, y pasarelas (\`gateways\`) de entrada, se redujo a
200 desde la versión 0.6.1.33. Los mensajes de pasarela de salida (es
decir, aquellos originados localmente) permanecen en 400.

TunnelGatewayMessage

19

 

300/400

VariableTunnelBuildMessage

23

1057 - 4225

500

Un TunnelBuildMessage (mensaje de establecimiento de túnel) más corto
desde la versión 0.7.12

VariableTunnelBuildReplyMessage

24

1057 - 4225

300

Un TunnelBuildReplyMessage (mensaje de respuesta de establecimiento de
túnel) más corto desde la versión 0.7.12

Others listed in [2003 Spec]()

0,4-9,12

 

 

Obsoleto, sin usar

### Especificación completa del protocolo

[On the I2NP Specification page](). See also
the [Common Data Structure Specification
page]().

### Trabajo futuro

No está claro si el actual esquema de prioridad es generalmente
efectivo, y si las prioridades para diferentes mensajes deben seguir
siendo ajustadas. Este es un tema para posterior investigación, análisis
y pruebas.


