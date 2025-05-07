 Index de la
documentation technique 2022-08 0.9.55 

Ce qui suit est un index de la documentation technique pour I2P.

Cette table des matières est organisée de la plus haute à la plus basse
des couches. Les couches les plus hautes sont pour les « clients » ou
les « applications » ; les couches plus basses sont dans le routeur
même. L'interface entre les applications et le routeur est l'API I2CP
(protocole de contrôle d'I2P).

The specifications linked below are currently supported in the network.
See the [Proposals]() page
for specifications in discussion or development.

The I2P Project is committed to maintaining accurate, current
documentation. If you find any inaccuracies in the documents linked
below, please [enter a ticket identifying the
problem]().

## Index de la documentation technique

### Vue d'ensemble

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

L'API de plus bas niveau utilisée par des clients (applications) pour
envoyer et recevoir du trafic vers un routeur. Traditionnellement
utilisée seulement par les applications Java et les API de plus haut
niveau.

- [I2CP - I2P Control Protocol / API
 overview]()
- [I2CP Specification]()
- [I2CP API
 Javadoc](http:///net/i2p/client/package-summary.html)
- [Common data structures
 specification]()
- [Data Structures
 Javadoc](http:///net/i2p/data/package-summary.html)

### Chiffrement bout à bout

Comment les messages client sont chiffrés de bout en bout par le
routeur.

- [ECIES-X25519-AEAD-Ratchet encryption for
 destinations]()
- [ECIES-X25519 encryption for
 routers]()
- [ElGamal/AES+SessionTag
 encryption]()
- [ElGamal and AES cryptography
 details]()

### Base de données de réseau

Stockage distribué et récupération d'informations concernant les
routeurs et clients.

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

### Protocole de message du routeur

I2P est un routeur orienté-message. Les messages envoyés entre routeurs
sont définis par le protocole I2NP.

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

### Tunnels

Sélection de pairs, requête de tunnels à travers ces pairs, et
chiffrement et acheminement des messages à travers ces tunnels.

- [Peer profiling and
 selection]()
- [Tunnel routing
 overview]()
- [Cheminement en ail et terminologie
 \"ail\"]()
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

### Couche transport

Protocoles pour communication directe (point-à-point) de routeur à
routeur.

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

### Autres sujets sur routeur

- [Router software updates]()
- [Router reseed specification]()
- [Native BigInteger
 Library]()
- Time synchronization and NTP
- [Performance]()
- [Configuration File
 Format]()
- [GeoIP File Format]()

### Guides et ressources de développeur

- [Guide du nouveau
 développeur]()
- [Guide du nouveau
 traducteur]()
- [Monotone
 Guide]()
- [Developer
 Guidelines]()
- Javadocs sur l'internet standard : [Server ](https://docs.i2p-projekt.de/javadoc/) [Server ](https://eyedeekay.github.io/javadoc-i2p/) Notez : vérifiez
 toujours que javadocs sont actuelles en vérifiant le numéro de
 version.
- JavaDocs dans I2P : [Server ](http:///javadoc-i2p/)
 Notez : vérifiez toujours que javadocs sont actuelles en vérifiant
 le numéro de version.
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


