 Pila de
protocolos 2024-01 0.9.61 

Here is the protocol stack for I2P. See also the [Index to Technical
Documentation]().

Cada una de las capas en la pila proporciona capacidades extra. Las
capacidades están listadas debajo, comenzando en el fondo de la pila de
protocolo.

- **Capa de Internet:**\
 IP: Protocolo de Internet, permite redireccionar hacia servidores en
 la Internet regular y enrutar paquetes a través de Internet usando
 entrega de mejor-esfuerzo (\`best-effort\`, sin garantías)
- **Capa de transporte:**\
 TCP: Protocolo de Control de Transmisiones, permite la entrega de
 paquetes fiable y ordenada a través de Internet.\
 UDP: Protocolo de Datagrama de Usuario, permite entrega de paquetes
 no fiable y desordenada a través de Internet.
- **Capa de Transporte I2P:** proporciona conexiones cifradas entre 2
 routers I2P. Estos no son aún anónimos, esta es estrictamente una
 conexión salto-a-salto. Se implementaron dos protocolos para
 proporcionar estas capacidades. NTCP (TCP basado en NIO) se
 construye encima de TCP, mientras que SSU (UDP Seguro Semiconfiable)
 usa UDP.\
 [NTCP2](): TCP basado-en-NIO\
 [SSU](): UDP Seguro
 Semi-fiable
- **Capa de Túnel I2P:** proporciona conexiones de túnel con cifrado
 completo.\
 [Tunnel messages](): tunnel messages
 are large messages containing encrypted I2NP (see below) messages
 and encrypted instructions for their delivery. The encryption is
 layered. The first hop will decrypt the tunnel message and read a
 part. Another part can still be encrypted (with another key), so it
 will be forwarded.\
 [I2NP messages](): I2P Network Protocol
 messages are used to pass messages through multiple routers. These
 I2NP messages are combined in tunnel messages.
- **Capa Garlic (ajo) de I2P:** proporciona entrega de mensajes I2P
 extremo-a-extremo cifrada y anónima\
 [I2NP messages](): I2P Network Protocol
 messages are wrapped in each other and used to ensure encryption
 between two tunnels and are passed along from source to destination,
 keeping both anonymous.

Las capas siguientes estrictamente hablando ya no forman parte de la
pila del Protocolo I2P, no son parte de la funcionalidad central del
\'router I2P\'. Sin embargo, cada una de estas capas añade funcionalidad
adicional, que permite a las aplicaciones un uso simple y conveniente de
I2P.

**Capa de cliente I2P:** permite a cualquier cliente usar las
funcionalidades de I2P, sin requerir el uso directo de la API (Interfaz
de Programación de Aplicaciones) del router.\
[I2CP](): I2P Client Protocol, allows secure and
asynchronous messaging over I2P by communicating messages over the I2CP
TCP socket.

**Capa de transporte extremo-a-extremo**: permite funcionalidades del
tipo-TCP o tipo-UDP encima de I2P.\
[Streaming Library](): an implementation of
TCP-like streams over I2P. This allows easier porting of existing
applications to I2P.\
[Datagram Library](): an implementation of
UDP-like messages over I2P. This allows easier porting of existing
applications to I2P.

**Capa del interfaz para aplicaciones I2P:** librerías adicionales
(opcionales) que permiten implementaciones más fáciles sobre I2P.\
[I2PTunnel]()\
[SAMv3]()

**Capa proxy para las aplicaciones I2P:** sistemas proxy.\
Finalmente, la que puede puede ser considerada la **\'capa de aplicación
de I2P\'**, es un gran número de aplicaciones sobre I2P. Podemos ordenar
esto basándonos en las capas I2P que usan.

- **Aplicaciones de streaming/datagramas**: i2psnark, Syndie,
 i2phex\...
- **SAM applications**: IMule, i2p-bt\...
- **Other I2P
 applications**: Syndie, EepGet,
 [plugins]()\...
- **Regular applications**: Jetty, Apache, Git, browsers, e-mail\...

::: {.box style="text-align:center;"}
![I2P Network
stack](images/protocol_stack.png "I2P Network stack")\
\
Figura 1: Las capas en la pila de red de I2P.
:::

\

\* Note: SAM can use both the streaming lib and datagrams.


