 Índice de la
Documentación técnica 2022-08 0.9.55 

A continuación hay in índice de la documentación técnica de I2P.

Este índice está ordenado desde la capa más alta a la más baja. Las
capas más altas son para las aplicaciones \"clientes\"; Las capas
menores son las que están dentro del propio ruter. El interfaz entre las
aplicaciones y el ruter es el API I2CP (Protocolo de Control de I2P).

The specifications linked below are currently supported in the network.
See the [Proposals]() page
for specifications in discussion or development.

The I2P Project is committed to maintaining accurate, current
documentation. If you find any inaccuracies in the documents linked
below, please [enter a ticket identifying the
problem]().

## Índice de la Documentación técnica

### Información general

[Technical
Introduction]()

[A Less-Technical
Introduction]()

[Threat model and
analysis]()

[Comparisons to other anonymous
networks]()

[Specifications]()

[Protocol stack chart]()

[Papers on I2P]()

[Presentations, articles, tutorials, videos, and
interviews]()

El API de menor nivel usado por los clientes (aplicaciones) para enviar
y recibir tráfico a un ruter. Tradicionalmente usado sólo por
aplicaciones en Java y APIs de mayor nivel.

- [I2CP - I2P Control Protocol / API
 overview]()
- [I2CP Specification]()
- [I2CP API
 Javadoc](http:///net/i2p/client/package-summary.html)
- [Common data structures
 specification]()
- [Data Structures
 Javadoc](http:///net/i2p/data/package-summary.html)

### Cifrado de extremo a extremo

Cómo son cifrados por el ruter los mensajes de fin a fin.

- [ECIES-X25519-AEAD-Ratchet encryption for
 destinations]()
- [ECIES-X25519 encryption for
 routers]()
- [ElGamal/AES+SessionTag
 encryption]()
- [ElGamal and AES cryptography
 details]()

### Base de datos de la red

Almacenamiento distribuido y obtención de información sobre los ruters y
los clientes.

- [Network database overview, details, and threat
 analysis]()
- [Cryptographic
 hashes](#SHA256)
- [Cryptographic
 signatures](#sig)
- [Red25519 signatures]()
- [Router reseed specification]()
- [Base32 Addresses for Encrypted
 Leasesets]()

### Protocolo de los mensajes del ruter

I2P es un ruter orientado a mensajes. Los mensajes que se envían entre
los ruters son definidos por el protocolo I2NP.

- [I2NP - I2P Network Protocol
 Overview]()
- [I2NP Specification]()
- [I2NP
 Javadoc](http:///net/i2p/data/i2np/package-summary.html)
- [Common data structures
 specification]()
- [Encrypted Leaseset
 specification]()
- [Data Structures
 Javadoc](http:///net/i2p/data/package-summary.html)

### Túneles

Seleccionando pares, solicitando túneles a través de esos pares, y
cifrando y enrutando mensajes a través de esos túneles.

- [Peer profiling and
 selection]()
- [Tunnel routing
 overview]()
- [Rutado Garlic y terminología
 \"garlic\"]()
- [Tunnel building and
 encryption]()
- [ElGamal/AES]()
 for build request encryption
- [ElGamal and AES cryptography
 details]()
- [Tunnel building specification
 (ElGamal)]()
- [Tunnel building specification
 (ECIES-X25519)]()
- [Low-level tunnel message
 specification]()
- [Unidirectional
 Tunnels]()
- [Peer Profiling and Selection in the I2P Anonymous
 Network](pdf/I2P-PET-CON-2009.1.pdf)
 2009 paper (pdf), not current but still generally accurate

### Capa de transporte

Los protocolos para las comunicaciones directas (punto a punto) de ruter
a ruter.

- [Transport layer
 overview]()
- [NTCP]() TCP-based
 transport overview and specification
- [NTCP2 specification]()
- [SSU]() UDP-based
 transport overview
- [SSU specification]()
- [SSU2 specification]()
- [NTCP transport
 encryption](#tcp)
- [SSU transport
 encryption](#udp)
- [Transport
 Javadoc](http:///net/i2p/router/transport/package-summary.html)
- [NTCP
 Javadoc](http:///net/i2p/router/transport/ntcp/package-summary.html)
- [SSU
 Javadoc](http:///net/i2p/router/transport/udp/package-summary.html)

### Otros temas sobre el Ruter

- [Router software updates]()
- [Router reseed specification]()
- [Native BigInteger
 Library]()
- Time synchronization and NTP
- [Performance]()
- [Configuration File
 Format]()
- [GeoIP File Format]()

### Recursos y guías para desarrolladores

- [Guía para nuevos
 desarrolladores]()
- [Guía para el nuevo
 traductor]()
- [Monotone
 Guide]()
- [Developer
 Guidelines]()
- Jacadocs en el Internet normal: [Server ](https://docs.i2p-projekt.de/javadoc/) [Server ](https://eyedeekay.github.io/javadoc-i2p/) Nota: verifique
 siempre que los Javadocs son actuales comprobando los números de
 versiones.
- Javadocs en I2P: [Server ](http:///javadoc-i2p/) Nota:
 verifique siempre que los Javadocs son actuales comprobando los
 números de versiones.
- [Proposals]()
- [Embedding the router in your
 application]()
- [How to Set up a Reseed
 Server]()
- [Ports used by I2P]()
- [Updating the wrapper
 manually]()
- [User forum](http://)
- [Developer forum inside
 I2P](http:///)
- [Bug tracker](https://i2pgit.org/i2p-hackers/i2p.i2p/issues)
- [I2P Source exported to GitHub](https://github.com/i2p/i2p.i2p)
- [I2P Source Git Repo inside I2P](http://git.idk.i2p/i2p/i2p.i2p.git)
- [Source translation at
 Transifex](https://www.transifex.net/projects/p/I2P/)
- [Roadmap]()
- [To Do List]() (not
 current)
- [Ancient invisiblenet I2P
 documents]() (2003)
- [The ancient I2P mailing list](http://zzz.i2p/archive/index.html)
 2004-07 to 2006-10


