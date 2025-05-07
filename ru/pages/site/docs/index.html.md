 Ссылка для
техническую документацию 2022-08 0.9.55 

Далее приведена ссылка на техническую документацию по I2P.

Этот индекс упорядочен от высшего к низшему слоям. Более высокие слои
для \"клиентов\" или приложений; Низшие слои для самого маршрутизатора.
Интерфейсом между приложениями и маршрутизатором является API I2CP (I2P
Control Protocol)

The specifications linked below are currently supported in the network.
See the [Proposals]() page
for specifications in discussion or development.

The I2P Project is committed to maintaining accurate, current
documentation. If you find any inaccuracies in the documents linked
below, please [enter a ticket identifying the
problem]().

## Ссылка для техническую документацию

### Обзор

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

Низкоуровневый API используется для клиентов (приложений) для отправки и
получения трафика с маршрутизатора. Традиционно используется только Java
приложениями и высокоуровневыми API.

- [I2CP - I2P Control Protocol / API
 overview]()
- [I2CP Specification]()
- [I2CP API
 Javadoc](http:///net/i2p/client/package-summary.html)
- [Common data structures
 specification]()
- [Data Structures
 Javadoc](http:///net/i2p/data/package-summary.html)

### Шифрование из-конца-в-конец

Как сообщения клиентов из-конца-в-конец шифруются маршрутизатором

- [ECIES-X25519-AEAD-Ratchet encryption for
 destinations]()
- [ECIES-X25519 encryption for
 routers]()
- [ElGamal/AES+SessionTag
 encryption]()
- [ElGamal and AES cryptography
 details]()

### Сетевая база данных

Распределенное хранилище и получение информации о маршрутизаторах и
клиентах.

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

### Протокол Сообщений Маршрутизатора

I2P - это маршрутизатор, ориентированный на сообщения. Сообщения
пересылаются между маршрутизаторами и описываются протоколом I2NP.

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

### Туннели

Выбор узлов, запрос туннелей через эти узлы, шифрование и маршрутизация
сообщений через эти туннели.

- [Peer profiling and
 selection]()
- [Tunnel routing
 overview]()
- [Чесночная маршрутизация и \"чесночная\"
 терминология]()
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

### Транспортный Уровень

Протоколы для прямой (точка-точка) связи маршрутизатор-маршрутизатор.

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

### Другие Темы о Маршрутизаторе

- [Router software updates]()
- [Router reseed specification]()
- [Native BigInteger
 Library]()
- Time synchronization and NTP
- [Performance]()
- [Configuration File
 Format]()
- [GeoIP File Format]()

### Источники и Руководства Разработчика

- [Руководство для Нового
 Разработчика]()
- [Руководство для Нового
 Переводчика]()
- [Monotone
 Guide]()
- [Developer
 Guidelines]()
- Javadocs в обычном интернет: [Server ](https://docs.i2p-projekt.de/javadoc/) [Server ](https://eyedeekay.github.io/javadoc-i2p/) Примечание: всегда
 убеждайтесь в том, что все javadoc актуальны, проверяя номер релиза.
- Javadocs внутри I2P: [Server ](http:///javadoc-i2p/)
 Примечание: всегда убеждайтесь в том, что все javadoc актуальны,
 проверяя номер релиза.
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


