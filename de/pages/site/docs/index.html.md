 Inhaltsverzeichnis
der Technischen Dokumentation 2022-08 0.9.55 

Das folgende ist ein Index zur technischen Dokumentation von I2P.

Dieser Index ist von abstrakteren zu systemnahen Schichten geordnet. Die
abstrakten Schichten sind für \"Klienten\" und Anwendungen gedacht, die
systemnahen befinden sich innerhalb der Vermittler selbst. Die
Schnittstelle zwischen Anwendungen und dem Vermittler ist die I2CP-(I2P
Control Protocol)-API.

The specifications linked below are currently supported in the network.
See the [Proposals]() page
for specifications in discussion or development.

The I2P Project is committed to maintaining accurate, current
documentation. If you find any inaccuracies in the documents linked
below, please [enter a ticket identifying the
problem]().

## Inhaltsverzeichnis der Technischen Dokumentation

### Übersicht

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

Die systemnächste API wird von Klienten (Anwendungen) verwendet um
Datenverkehr an Vermittler zu senden und von diesen zu empfangen.
Üblicherweise nur von Java-Anwendungen und abstrakteren APIs verwendet.

- [I2CP - I2P Control Protocol / API
 overview]()
- [I2CP Specification]()
- [I2CP API
 Javadoc](http:///net/i2p/client/package-summary.html)
- [Common data structures
 specification]()
- [Data Structures
 Javadoc](http:///net/i2p/data/package-summary.html)

### Ende zu Ende Verschlüsselung

Wie Client Nachrichten durch den Router \"Ende zu Ende\" verschlüsselt
werden.

- [ECIES-X25519-AEAD-Ratchet encryption for
 destinations]()
- [ECIES-X25519 encryption for
 routers]()
- [ElGamal/AES+SessionTag
 encryption]()
- [ElGamal and AES cryptography
 details]()

### Netzwerkdatenbank

Verteilte Speicherung und Bezug von Informationen über Vermittler und
Klienten.

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

### Router Nachrichten Protokoll

I2P ist ein Nachrichten-orientierter Vermittler. Die zwischen
Vermittlern gesendeten Nachrichten werden durch das I2NP-Protokoll
bestimmt.

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

### Tunnel

Auswahl von Knoten, Anfordern von Tunneln über diese Knoten sowie
Verschlüsseln und Vermitteln von Nachrichten über diese Tunnel.

- [Peer profiling and
 selection]()
- [Tunnel routing
 overview]()
- [Knoblauch-Vermittlung und
 \"Knoblauch\"-Terminologie]()
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

### Übertragungsschicht

Die Protokolle für direkte (Punkt-zu-Punkt)
Vermittler-zu-Vermittler-Kommunikation

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

### Andere Router Themen

- [Router software updates]()
- [Router reseed specification]()
- [Native BigInteger
 Library]()
- Time synchronization and NTP
- [Performance]()
- [Configuration File
 Format]()
- [GeoIP File Format]()

### Entwickleranleitungen und Hilfsmittel

- [Neues
 Entwicklerhandbuch]()
- [Neues
 Übersetzungshandbuch]()
- [Monotone
 Guide]()
- [Developer
 Guidelines]()
- Javadocs im Standard-Internet: [Server ](https://docs.i2p-projekt.de/javadoc/) [Server ](https://eyedeekay.github.io/javadoc-i2p/) Hinweis: Immer auf die
 Aktualität der javadocs durch Vergleich der Versionsnummer achten.
- Javadocs innerhalb von I2P: [Server ](http:///javadoc-i2p/)
 Hinweis: Immer auf die Aktualität der javadocs durch Vergleich der
 Versionsnummer achten.
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


