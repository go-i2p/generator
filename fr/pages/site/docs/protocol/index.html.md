 Protocol Stack 2024-01 0.9.61 

Here is the protocol stack for I2P. See also the [Index to Technical
Documentation]().

Each of the layers in the stack provides extra capabilities. The
capabilities are listed below, starting at the bottom of the protocol
stack.

- **Internet Layer:**\
 IP : Protocole Internet, permet l'adréessage d'hôtes sur l'Internet
 ordinaire et le routage de paquets par Internet en utilisant la
 livraison au mieux.
- **Transport Layer:**\
 TCP: Transmission Control Protocol, allow reliable, in-order
 delivery of packets across the internet.\
 UDP: User Datagram Protocol, allow unreliable, out-of-order delivery
 of packets across the internet.
- **I2P Transport Layer:** provide encrypted connections between 2 I2P
 routers. These are not anonymous yet, this is strictly a hop-to-hop
 connection. Two protocols are implemented to provide these
 capabilities. NTCP2 builds on top of TCP, while SSU uses UDP.\
 [NTCP2](): NIO-based TCP\
 [SSU](): Secure
 Semi-reliable UDP
- **I2P Tunnel Layer:** provide full encrypted tunnel connections.\
 [Tunnel messages](): tunnel messages
 are large messages containing encrypted I2NP (see below) messages
 and encrypted instructions for their delivery. The encryption is
 layered. The first hop will decrypt the tunnel message and read a
 part. Another part can still be encrypted (with another key), so it
 will be forwarded.\
 [I2NP messages](): I2P Network Protocol
 messages are used to pass messages through multiple routers. These
 I2NP messages are combined in tunnel messages.
- **I2P couche Ail :** fournit la livraison de message I2P chiffrés et
 anonymes de bout à bout.\
 [I2NP messages](): I2P Network Protocol
 messages are wrapped in each other and used to ensure encryption
 between two tunnels and are passed along from source to destination,
 keeping both anonymous.

The following layers are strictly speaking no longer part of the I2P
Protocol stack, they are not part of the core \'I2P router\'
functionality. However, each of these layers adds additional
functionality, to allow applications simple and convenient I2P usage.

**I2P Client Layer:** allow any client to use I2P functionality, without
requiring the direct use of the router API.\
[I2CP](): I2P Client Protocol, allows secure and
asynchronous messaging over I2P by communicating messages over the I2CP
TCP socket.

**I2P End-to-end Transport Layer:** allow TCP- or UDP-like functionality
on top of I2P.\
[Streaming Library](): an implementation of
TCP-like streams over I2P. This allows easier porting of existing
applications to I2P.\
[Datagram Library](): an implementation of
UDP-like messages over I2P. This allows easier porting of existing
applications to I2P.

**I2P Application Interface Layer:** additional (optional) libraries
allowing easier implementations on top of I2P.\
[I2PTunnel]()\
[SAMv3]()

**I2P Application Proxy Layer:** proxy systems.\
Finalement, ce que l'on pourrait considérer être la **\'couche
d'application I2P\'**, est un grand nombre de d'applications au-dessus
d'I2P. Nous pouvons ordonner ceci en nous basant sur la couche de pile
d'I2P qu'elles utilisent.

- **Streaming/applications de datagramme** : i2psnark, Syndie,
 i2phex...
- **SAM applications**: IMule, i2p-bt\...
- **Other I2P
 applications**: Syndie, EepGet,
 [plugins]()\...
- **Regular applications**: Jetty, Apache, Git, browsers, e-mail\...

::: {.box style="text-align:center;"}
![I2P Network
stack](images/protocol_stack.png "I2P Network stack")\
\
Figure 1: The layers in the I2P Network stack.
:::

\

\* Note: SAM can use both the streaming lib and datagrams.


