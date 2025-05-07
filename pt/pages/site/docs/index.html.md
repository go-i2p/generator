 Índex para a
Documentação Técnica 2022-08 0.9.55 

\'Seguir\' é um índex para a documentação técnica para o I2P.

Este índice é ordenado da camada mais alta para a mais baixa. As camadas
mais altas são para \"clientes\" ou aplicações; as camadas mais baixas
são internas ao próprio roteador. A interface entre as aplicações e o
roteador é a API do protocolo I2CP (Protocolo de Controle da I2P).

The specifications linked below are currently supported in the network.
See the [Proposals]() page
for specifications in discussion or development.

The I2P Project is committed to maintaining accurate, current
documentation. If you find any inaccuracies in the documents linked
below, please [enter a ticket identifying the
problem]().

## Índex para a Documentação Técnica

### Sinopse

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

A API de baixo-nivel usada por clientes (aplicações) para enviar e
receber trafego para um roteador. Tradicionalmente usado apenas por
aplicações Java e APIs de alto-nível.

- [I2CP - I2P Control Protocol / API
 overview]()
- [I2CP Specification]()
- [I2CP API
 Javadoc](http:///net/i2p/client/package-summary.html)
- [Common data structures
 specification]()
- [Data Structures
 Javadoc](http:///net/i2p/data/package-summary.html)

### End-to-End Encryption

Como as mensagens de cliente são criptografadas de ponta a ponta pelo
roteador

- [ECIES-X25519-AEAD-Ratchet encryption for
 destinations]()
- [ECIES-X25519 encryption for
 routers]()
- [ElGamal/AES+SessionTag
 encryption]()
- [ElGamal and AES cryptography
 details]()

### Banco de dados da rede

Armazenamento distribuído e recuperação de informações relativas aos
roteadores e clientes.

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

### Protocolo de mensagens do roteador

A I2P é baseada em roteamento orientado-a-mensagens. As mensagens
enviadas entre os roteadores são definidas pelo protocolo I2NP.

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

### Tuneis

Selecionando pares, requisitando túneis através de tais pares,
criptografando e roteando mensagens através desses túneis.

- [Peer profiling and
 selection]()
- [Tunnel routing
 overview]()
- [Roteamento e terminologia
 \"alho\"]()
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

### Camada de transporte

Os protocolos para a comunicação direta (ponto-a-ponto) de roteador para
roteador

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

### Outros tópicos sobre o roteador

- [Router software updates]()
- [Router reseed specification]()
- [Native BigInteger
 Library]()
- Time synchronization and NTP
- [Performance]()
- [Configuration File
 Format]()
- [GeoIP File Format]()

### Guia para Desenvolvedores e Recursos

- [Guia para novos
 desenvolvedores]()
- [Guia para novos
 tradutores]()
- [Monotone
 Guide]()
- [Developer
 Guidelines]()
- Javadocs na internet ordinária: [Server ](https://docs.i2p-projekt.de/javadoc/) [Server ](https://eyedeekay.github.io/javadoc-i2p/) Nota: sempre verifique
 qual javadocs é o atual, verificando o número do lançamento.
- Javadocs na I2P: [Server ](http:///javadoc-i2p/) Nota:
 sempre verifique qual javadocs é o atual, verificando o número do
 lançamento.
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


