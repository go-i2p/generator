 Index la
documentația tehnică 2022-08 0.9.55 

Urmează un index al documentației tehnice pentru I2P.

Acest index este ordonat de la cele mai mari până la cele mai mici
straturi. Straturile superioare sunt destinate „clienților" sau
aplicațiilor; straturile inferioare sunt în interiorul routerului în
sine. Interfața dintre aplicații și router este I2CP (I2P Control
Protocol) API.

The specifications linked below are currently supported in the network.
See the [Proposals]() page
for specifications in discussion or development.

The I2P Project is committed to maintaining accurate, current
documentation. If you find any inaccuracies in the documents linked
below, please [enter a ticket identifying the
problem]().

## Index la documentația tehnică

### Prezentare generală

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

API-ul cu cel mai scăzut nivel utilizat pentru clienți (aplicații)
pentru a trimite și primi trafic către un router. Folosit în mod
tradițional numai de aplicațiile Java și API-urile de nivel superior.

- [I2CP - I2P Control Protocol / API
 overview]()
- [I2CP Specification]()
- [I2CP API
 Javadoc](http:///net/i2p/client/package-summary.html)
- [Common data structures
 specification]()
- [Data Structures
 Javadoc](http:///net/i2p/data/package-summary.html)

### Criptare end-to-end

Cum mesajele client sunt criptate end-to-end de router.

- [ECIES-X25519-AEAD-Ratchet encryption for
 destinations]()
- [ECIES-X25519 encryption for
 routers]()
- [ElGamal/AES+SessionTag
 encryption]()
- [ElGamal and AES cryptography
 details]()

### Baza de date de rețea

Depozitare distribuită și regăsire de informații despre routere și
clienți.

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

### Protocolul mesajului router

I2P este un router orientat către mesaje. Mesajele trimise între routere
sunt definite prin protocolul I2NP.

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

### Tuneluri

Selectarea colegilor, solicitarea de tunele prin acei colegi și
criptarea și dirijarea mesajelor prin aceste tuneluri.

- [Peer profiling and
 selection]()
- [Tunnel routing
 overview]()
- [Rutinarea usturoiului și terminologia
 „usturoiului"]()
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

### Strat de transport

Protocoalele pentru router direct (punct la punct) la comunicarea
routerului.

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

### Alte subiecte de router

- [Router software updates]()
- [Router reseed specification]()
- [Native BigInteger
 Library]()
- Time synchronization and NTP
- [Performance]()
- [Configuration File
 Format]()
- [GeoIP File Format]()

### Ghiduri și resurse pentru dezvoltatori

- [Ghid pentru dezvoltatori
 noi]()
- [Ghidul traducătorului
 nou]()
- [Monotone
 Guide]()
- [Developer
 Guidelines]()
- Javadocs pe internet standard: [Server ](https://docs.i2p-projekt.de/javadoc/) [Server ](https://eyedeekay.github.io/javadoc-i2p/) Notă: verificați
 întotdeauna dacă javadocs-urile sunt curente verificând numărul
 lansării.
- Javadocs în interiorul I2P: [Server ](http:///javadoc-i2p/) Notă:
 verificați întotdeauna dacă javadocs-urile sunt curente verificând
 numărul lansării.
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


