 Indeks ke
Dokumentasi Teknis 2022-08 0.9.55 

Berikut adalah indeks dokumentasi teknis untuk I2P.

Indeks ini diurutkan dari lapisan tertinggi ke terendah. Lapisan lebih
tinggi adalah untuk \"klien\" or aplikasi; Lapisan lebih rendah adalah
di dalam router itu sendiri. Antarmuka antara aplikasi dan roiter adalah
API I2CP (I2P Control Protocol)

The specifications linked below are currently supported in the network.
See the [Proposals]() page
for specifications in discussion or development.

The I2P Project is committed to maintaining accurate, current
documentation. If you find any inaccuracies in the documents linked
below, please [enter a ticket identifying the
problem]().

## Indeks ke Dokumentasi Teknis

### Ikhtisar

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

API tingkat paling rendah untuk klien (aplikasi) untuk mengirim dan
menerima lalu lintas data ke sebuah router. Biasanya digunakan oleh
aplikasi Java dan API tingkat tinggi.

- [I2CP - I2P Control Protocol / API
 overview]()
- [I2CP Specification]()
- [I2CP API
 Javadoc](http:///net/i2p/client/package-summary.html)
- [Common data structures
 specification]()
- [Data Structures
 Javadoc](http:///net/i2p/data/package-summary.html)

### Enkripsi end-to-end

Cara pesan klien terenkripsi end-to-end oleh router.

- [ECIES-X25519-AEAD-Ratchet encryption for
 destinations]()
- [ECIES-X25519 encryption for
 routers]()
- [ElGamal/AES+SessionTag
 encryption]()
- [ElGamal and AES cryptography
 details]()

### Database Jaringan

Penyimpanan terdistribusi dan pengambilan informasi tentang router dan
klien.

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

### Protokol Pesan Router

I2P adalah router berorientasi pesan. Pesan-pesan yang dikirimkan antar
router didefinisikan oleh protokol IPNP.

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

Pemilihan peer, permintaan tunnel melalui peer tersebut, dan enkripsi
serta pengalihan pesan melalui tunnel tersebut.

- [Peer profiling and
 selection]()
- [Tunnel routing
 overview]()
- [Garlic routing dan istilah
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

### Transport Layer

Protokol untuk komunikasi router langsung (point-to-point).

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

### Topik Lain Router

- [Router software updates]()
- [Router reseed specification]()
- [Native BigInteger
 Library]()
- Time synchronization and NTP
- [Performance]()
- [Configuration File
 Format]()
- [GeoIP File Format]()

### Panduan Pengembang dan Sumber Daya

- [Panduan Pengembang
 Baru]()
- [Panduan Penerjemah
 Baru]()
- [Monotone
 Guide]()
- [Developer
 Guidelines]()
- Javadocs tentang Internet standar: [Server ](https://docs.i2p-projekt.de/javadoc/) [Server ](https://eyedeekay.github.io/javadoc-i2p/) Catatan: selalu
 periksa apakah javadocs adalah terbaru dengan memeriksa nomor rilis.
- Javadocs di dalam I2P: [Server ](http:///javadoc-i2p/)
 Catatan: selalu periksa apakah javadocs adalah terbaru dengan
 memeriksa nomor rilis.
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


