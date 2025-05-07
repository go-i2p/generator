 技術資料索引 2022-08 0.9.55 

以下是 I2P 技術資料的索引

这份索引从高层到低层顺序排列。 高层是为"客户端"或应用服务的。
低层处在路由本身中。 应用与路由之间的接口是I2CP(I2P控制协议) API。

The specifications linked below are currently supported in the network.
See the [Proposals]() page
for specifications in discussion or development.

The I2P Project is committed to maintaining accurate, current
documentation. If you find any inaccuracies in the documents linked
below, please [enter a ticket identifying the
problem]().

## 技術資料索引

### 總覽

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

用於客戶端（應用程序）向路由器發送和接收流量的底層 API。 傳統上僅由 Java
應用程序和更高級別的 API 來使用。

- [I2CP - I2P Control Protocol / API
 overview]()
- [I2CP Specification]()
- [I2CP API
 Javadoc](http:///net/i2p/client/package-summary.html)
- [Common data structures
 specification]()
- [Data Structures
 Javadoc](http:///net/i2p/data/package-summary.html)

### 端到端加密

客戶端信息如何經由路由器進行端到端加密。

- [ECIES-X25519-AEAD-Ratchet encryption for
 destinations]()
- [ECIES-X25519 encryption for
 routers]()
- [ElGamal/AES+SessionTag
 encryption]()
- [ElGamal and AES cryptography
 details]()

### 網路資料庫

分佈式儲存和回復有關路由器和客戶端的信息。

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

### 路由器消息协议

I2P 是一个面向消息的路由器。路由器之间发送的消息由 I2NP 协议定义。

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

### 隧道

选择节点，构建通过这些节点的隧道，并通过这些隧道对信息进行加密和路由。

- [Peer profiling and
 selection]()
- [Tunnel routing
 overview]()
- [大蒜路由和 \"大蒜
 \"术语]()
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

### 传输层

路由器与路由器进行直接（点对点）通信的协议。

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

### 其他路由器主题

- [Router software updates]()
- [Router reseed specification]()
- [Native BigInteger
 Library]()
- Time synchronization and NTP
- [Performance]()
- [Configuration File
 Format]()
- [GeoIP File Format]()

### 开发者的指南和资源

- [新开发者的指南]()
- [新翻译者的指南]()
- [Monotone
 Guide]()
- [Developer
 Guidelines]()
- 公共互联网上的Javadocs： [Server ](https://docs.i2p-projekt.de/javadoc/) [Server ](https://eyedeekay.github.io/javadoc-i2p/)
 注意：一定要通过检查版本号来验证javadocs是否是最新的。
- I2P网络内的Javadocs。 [Server ](http:///javadoc-i2p/)
 注意：一定要通过检查版本号来验证javadocs是否是最新的。
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


