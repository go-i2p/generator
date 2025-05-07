 Introducción al
los Transportes June 2018 0.9.36 

## Transportes den I2P

Un \"transporte\" en I2P es un método para la comunicación directa de
punto a punto entre dos ruters. Los transportes tienen que proporcionar
confidencialidad e integridad contra adversarios externos a la vez que
se aseguran de que el ruter contactado es el que recibe el mensaje
indicado.

I2P supports multiple transports simultaneously. There are three
transports currently implemented:

Cada uno proporciona un modelo de \"conexión\", con autenticación
control de flujo, contestaciones y retransmisión.

## Servicios de trasnporte

El sub-sistema de transportes en I2P proporciona los siguientes
servicios:

- Reliable delivery of [I2NP]() messages.
 Transports support I2NP message delivery ONLY. They are not
 general-purpose data pipes.
- La entrega de mensajes en-orden NO está garantizada por todos los
 transportes.
- Mantiene un conjunto de direcciones de routers, una o más para cada
 transporte, que el router publica como su información global de
 contacto (la RouterInfo). Cada transporte puede conectarse usando
 una de estas direcciones, que pueden ser IPv4 o (desde la versión
 0.9.8) IPv6.
- Selección del mejor transporte para cada mensaje saliente
- Poner en cola los mensajes salientes según la prioridad
- Límite de ancho de banda, de entrada y de salida, de acuerdo con la
 configuración del ruter.
- Configuración y desmontaje de las conexiones de trasnporte
- Cifrado de las comunicaciones de fin a fin.
- Mantenimiento y límites de conexión para cada transporte,
 implementación de varios umbrales para esos límites, y la
 comunicación del estado de esos umbrales al ruter para que pueda
 hacer cambios operacionales basados en su estado.
- Abrir puertos en el cortafuegos usando UPnP (Universal Plug and
 Play)
- NAT/Cortafuegos cooperativo trasversal
- Detección de la IP local por varios métodos, incluyendo UPnP,
 inspección de los paquetes entrantes y enumeración de los
 dispositivos de red
- Coordinación del estado del cortafuegos y la IP local, y sus
 cambios, a lo largo de los transportes
- Coordinación del estado del cortafuegos y la IP local, y sus
 cambios, con el ruter y el interfaz del usuario
- Determinación de un reloj consensuado, que se usa para actualizar
 periódicamente el reloj del ruter, como respaldo para NTP
- Mantenimiento del estado de cada par, incluyendo cuando está
 conectado, si se ha conectado recientemente y si estaba accesible en
 el último intento.
- Calificación de una IP válida de acuerdo con un grupo de normas
 locales.
- Honrar las listas manuales y automáticas mantenidas por el ruter de
 los pares baneados, y denegar las conexiones entrantes o salientes a
 esos pares

## Direcciones de trasnporte

El subsistema de transporte mantiene un conjunto de direcciones de
router, cada una de las cuales lista un método de transporte, IP, y
puerto. Estas direcciones constituyen los puntos de contacto anunciados,
y son publicadas por el router en la base de datos de red. Las
direcciones también pueden contener un conjunto arbitrario de opciones
adicionales.

Cada método de transporte puede publicar múltiples direcciones de
router.

Los espenarios típicos son:

- Un ruter no tiene direcciones publicadas, con lo que es considerado
 \"oculto\" y no puede recibir conexiones entrantes
- A router is firewalled, and therefore publishes an SSU address which
 contains a list of cooperating peers or \"introducers\" who will
 assist in NAT traversal (see [the SSU spec]()
 for details)
- Un ruter no esta bloqueado por el firewall o sus puertos NAT están
 abiertos; publica ambas direcciones, NTCP y SSU, que contiene la IP
 y los puertos accesibles.

## Selección del transporte

The transport system delivers [I2NP messages]()
only. The transport selected for any message is independent of the
upper-layer protocols and contents (router or client messages, whether
an external application was using TCP or UDP to connect to I2P, whether
the upper layer was using [the streaming
library]() streaming or
[datagrams](), datagrams etc.).

Para cada mensaje saliente, el sistema de transporte solicita
\"ofertas\" de cada transporte. El transporte que ofrece el valor más
bajo (mejor) gana la apuesta y recibe el mensaje para ser entregado. Un
transporte puede negarse a apostar.

Si un transporte apuesta o no, y con qué valor, depende de numerosos
factores:

- Configuarión de las preferencias de trasnporte
- Si el transporte ya está conectado al par
- El número de las conexiones actuales comparado con varios límites de
 conexión.
- Si un intento de conexión reciente ha fallado
- El tamaño del mensaje, ya que diferentes transportes tienen
 diferentes límites de tamaño
- Si el par puede aceptar conexiones entrantes para ese transporte,
 como se indica en su RouterInfo
- Si la conexión debería ser indirecta (requiriendo introductores) o
 directa
- El transporte preferido por el par, como se anuncia en el RouterInfo

En general, los valores de las ofertas son seleccionados para que los
ruters sólo estén conectados a un solo transporte a la vez. Aunque esto
no es obligatorio.

## Nuevos transportes y trabajos futuros

Puede que se desarrollen transportes adicionales, incluyendo:

- Un transporte que parezca TLS/SSH
- Un transporte \"indirecto\" para los ruters que no sean accesibles
 por todos los otros ruters (una forma de \"ruters restringidos\")
- Transportes enchufables compatibles-con-Tor

Seguimos trabajando para ajustar los límites de las conexiones de cada
transporte. I2P está diseñado como una \"red mesh\", donde se asume que
cada ruter puede conectar con cualquier otro ruter. Esta asunción puede
ser falsa para los ruter que han excedido los límites de conexiones, y
para los ruters detrás de cortafuegos de estado restrictivos (rutas
restringidas).

Los actuales límites de la conexión son más altos para SSU (UDP seguro
semiconfiable) que para NTCP (TCP basado en NIO), partiendo de asumir
que los requisitos de memoria para una conexión NTCP son mayores que
para una SSU. Sin embargo, como los buffers (prealmacenamiento) NTCP
están parcialmente en el kernel (núcleo del sistema) y los buffers SSU
están en la pila de Java, esa asunción es difícil de verificar.

Analyze [Breaking and Improving Protocol
Obfuscation]() and see how transport-layer padding
may improve things.


