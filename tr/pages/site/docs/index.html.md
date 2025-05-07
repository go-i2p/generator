 Teknik Belgeler
Dizini 2022-08 0.9.55 

I2P için teknik belgeler dizinini aşağıda bulabilirsiniz.

Bu dizin en yüksekten en alçağa doğru sıralanır. Daha yüksek katmanlar
\"istemciler\" veya uygulamalar içindir. Alt katmanlar yönelticinin
içindedir. Uygulamalar ve yöneltici arasındaki arayüz, I2CP (I2P denetim
iletişim kuralı) API yazılımıdır.

The specifications linked below are currently supported in the network.
See the [Proposals]() page
for specifications in discussion or development.

The I2P Project is committed to maintaining accurate, current
documentation. If you find any inaccuracies in the documents linked
below, please [enter a ticket identifying the
problem]().

## Teknik Belgeler Dizini

### Özet

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

İstemcilerin (uygulamalar) bir yönelticiye trafik göndermek ve almak
için kullandığı en alt düzey API . Geleneksel olarak yalnızca Java
uygulamaları ve daha yüksek düzeydeki API yazılımları tarafından
kullanılır.

- [I2CP - I2P Control Protocol / API
 overview]()
- [I2CP Specification]()
- [I2CP API
 Javadoc](http:///net/i2p/client/package-summary.html)
- [Common data structures
 specification]()
- [Data Structures
 Javadoc](http:///net/i2p/data/package-summary.html)

### Uçtan Uca Şifreleme

İstemci iletileri yöneltici tarafından uçtan uca nasıl şifrelenir.

- [ECIES-X25519-AEAD-Ratchet encryption for
 destinations]()
- [ECIES-X25519 encryption for
 routers]()
- [ElGamal/AES+SessionTag
 encryption]()
- [ElGamal and AES cryptography
 details]()

### Ağ veri tabanı

Dağıtılmış depolama ve yönelticiler ile istemciler hakkında bilgi almak.

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

### Yöneltici İleti İletişim Kuralı

I2P, ileti odaklı bir yönelticidir. Yönelticiler arasında gönderilen
iletiler I2NP iletişim kuralı ile tanımlanır.

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

### Tüneller

Eşlerin seçilmesi, bu eşler üzerinden tünellerin istenmesi ve bu
tüneller üzerinden iletilerin şifrelenerek yöneltilmesi.

- [Peer profiling and
 selection]()
- [Tunnel routing
 overview]()
- [Garlic yöneltme ve \"garlic\"
 terminolojisi]()
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

### Taşıyıcı Katman

Doğrudan (uçtan uca) yönelticiden yönelticiye iletişim için iletişim
kuralları.

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

### Diğer Yöneltici Konuları

- [Router software updates]()
- [Router reseed specification]()
- [Native BigInteger
 Library]()
- Time synchronization and NTP
- [Performance]()
- [Configuration File
 Format]()
- [GeoIP File Format]()

### Geliştirici Rehberleri ve Kaynakları

- [Yeni başlayan geliştiriciler
 rehberi]()
- [Yeni başayan çevirmenler
 rehberi]()
- [Monotone
 Guide]()
- [Developer
 Guidelines]()
- Standart İnternet üzerinde Java belgeleri: [Server
 ](https://docs.i2p-projekt.de/javadoc/) [Server ](https://eyedeekay.github.io/javadoc-i2p/) Not: Her zaman Java
 belgelerinin yayın numaralarına bakarak güncel olup olmadıklarını
 denetleyin.
- I2P içindeki Java belgeleri. [Server ](http:///javadoc-i2p/) Not:
 Her zaman Java belgelerinin yayın numaralarına bakarak güncel olup
 olmadıklarını denetleyin.
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


