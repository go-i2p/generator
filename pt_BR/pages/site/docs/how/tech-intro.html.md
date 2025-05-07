 I2P: Uma estrutura
escalável para comunicação anônima 2025-01 0.9.65 

- [Introdução](#intro)
- [Operação I2P](#op)
 - [Visão geral](#op.overview)
 - [Túneis](#op.tunnels)
 - [Banco de dados da rede](#op.netdb)
 - [Protocolos de transporte](#op.transport)
 - [Criptografia](#op.crypto)
- [Futuro](#future)
 - [Restricted Routes](#future.restricted)
 - [Variable Latency](#future.variablelatency)
- [Similar Networks](#similar)
 - [Tor](#similar.tor)
 - [Freenet](#similar.freenet)
- [Application Layer](#app)
 - [Streaming](#app.streaming)
 - [Naming and Addressbook](#app.naming)
 - [I2PSnark](#app.i2psnark)
 - [I2PTunnel](#app.i2ptunnel)
 - [I2P Email](#app.i2pmail)

 

NOTE: This document was originally written by jrandom in 2003. While we
strive to keep it current, some information may be obsolete or
incomplete. The transport and cryptography sections are current as of
2025-01.

# Introdução {#intro}

O I2P é uma camada de rede anônima escalável, auto-organizada e
resiliente comutada por pacotes, na qual qualquer número de diferentes
aplicativos de anonimato ou conscientes da segurança pode operar. Cada
um desses aplicativos pode fazer suas próprias compensações de
anonimato, latência e throughput sem se preocupar com a implementação
adequada de uma mixnet de rota livre, permitindo que eles misturem sua
atividade com o conjunto maior de usuários de anonimato já em execução
no topo do I2P.

Applications available already provide the full range of typical
Internet activities - **anonymous** web browsing, web hosting, chat,
file sharing, e-mail, blogging and content syndication, as well as
several other applications under development.

- Navegação na Web: usando qualquer navegador existente que suporte o
 uso de proxy.
- Chat: IRC and other protocols
- File sharing: [I2PSnark](#app.i2psnark) and other applications
- E-mail: [susimail](#app.i2pmail) and other applications
- Blog: using any local web server, or available plugins

Ao contrário de sites hospedados em redes de distribuição de conteúdo
como [Freenet](#similar.freenet) ou
[GNUnet](https://www.gnunet.org/en/), os serviços hospedados no I2P são
totalmente interativos - há mecanismos de busca tradicionais no estilo
web, quadros de avisos, blogs nos quais você pode comentar, sites
baseados em banco de dados e pontes para consultar sistemas estáticos
como o Freenet sem precisar instalá-lo localmente.

Com todos esses aplicativos habilitados para anonimato, o I2P assume o
papel do middleware orientado a mensagens - os aplicativos dizem que
querem enviar alguns dados para um identificador criptográfico (um
\"destino\") e o I2P cuida de garantir que eles cheguem lá de forma
segura e anônima. O I2P também agrupa uma biblioteca simples [de
streaming](#app.streaming) para permitir que as mensagens anônimas de
melhor esforço do I2P sejam transferidas como fluxos confiáveis e
ordenados, de forma transparente oferecendo um algoritmo de controle de
congestionamento baseado em TCP ajustado para o produto de atraso de
alta largura de banda da rede. Embora existam vários proxies SOCKS
simples disponíveis para vincular aplicativos existentes à rede, seu
valor tem sido limitado, pois quase todos os aplicativos expõem
rotineiramente o que, em um contexto anônimo , são informações
confidenciais. A única maneira segura de fazer isso é auditar
completamente um aplicativo para garantir a operação adequada e para
ajudar nisso, fornecemos uma série de APIs em várias linguagens que
podem ser usadas para aproveitar ao máximo a rede.

I2P is not a research project - academic, commercial, or governmental,
but is instead an engineering effort aimed at doing whatever is
necessary to provide a sufficient level of anonymity to those who need
it. It has been in active development since early 2003 with one full
time developer and a dedicated group of part time contributors from all
over the world. All of the work done on I2P is open source and freely
available on the [website](), with the majority of
the code released outright into the public domain, though making use of
a few cryptographic routines under BSD-style licenses. The people
working on I2P do not control what people release client applications
under, and there are several GPL\'ed applications available
([I2PTunnel](#app.i2ptunnel), [susimail](#app.i2pmail),
[I2PSnark](#app.i2psnark), [I2P-Bote](#app.i2pbote),
[I2Phex](#app.i2phex) and others.).
[Funding]() for I2P comes entirely from
donations, and does not receive any tax breaks in any jurisdiction at
this time, as many of the developers are themselves anonymous.

# Operação {#op}

## Visão geral {#op.overview}

Para entender a operação do I2P, é essencial entender alguns
conceitos-chave. Primeiro, o I2P faz uma separação estrita entre o
software que participa da rede (um \"roteador\") e os endpoints anônimos
(\"destinos\") associados a aplicativos individuais. O fato de alguém
estar executando o I2P não é geralmente um segredo. O que está oculto
são informações sobre o que o usuário está fazendo, se é que está
fazendo alguma coisa, bem como a qual roteador um destino específico
está conectado . Os usuários finais normalmente terão vários destinos
locais em seus roteadores - por exemplo, um fazendo proxy em servidores
IRC, outro dando suporte ao servidor web anônimo do usuário (\"Site
I2P\"), outro para uma instância I2Phex, outro para torrents, etc.

Outro conceito crítico para entender é o \"túnel\". Um túnel é um
caminho direcionado por uma lista explicitamente selecionada de
roteadores. Criptografia em camadas é usada, então cada um dos
roteadores pode descriptografar apenas uma única camada. As informações
descriptografadas contêm o IP do próximo roteador, junto com as
informações criptografadas a serem encaminhadas. Cada túnel tem um ponto
inicial (o primeiro roteador, também conhecido como \"gateway\") e um
ponto final. As mensagens podem ser enviadas apenas de uma maneira. Para
enviar mensagens de volta, outro túnel é necessário.

::: {.box style="text-align:center;"}
\
\
![Inbound and outbound tunnel
schematic](images/tunnels.png "Inbound and outbound tunnel schematic")\
\
Figura 1: Existem dois tipos de túneis: entrada e saída.
:::

Existem dois tipos de túneis: **túneis de \"saída\"** enviam mensagens
para longe do criador do túnel, enquanto **túneis de \"entrada\"**
trazem mensagens para o criador do túnel. A combinação desses dois
túneis permite que os usuários enviem mensagens uns aos outros. O
remetente (\"Alice\" na imagem acima) configura um túnel de saída,
enquanto o receptor (\"Bob\" na imagem acima) cria um túnel de entrada.
O gateway de um túnel de entrada pode receber mensagens de qualquer
outro usuário e as enviará até o ponto final (\"Bob\"). O ponto final do
túnel de saída precisará enviar a mensagem para o gateway do túnel de
entrada. Para fazer isso, o remetente (\"Alice\") adiciona instruções à
sua mensagem criptografada. Assim que o ponto final do túnel de saída
descriptografar a mensagem, ele terá instruções para encaminhar a
mensagem para o gateway de entrada correto (o gateway para \"Bob\").

Um terceiro conceito crítico para entender é o **\"network database\"**
(ou \"netDb\") do I2P - um par de algoritmos usados para compartilhar
metadados de rede. Os dois tipos de metadados transportados são
**\"routerInfo\"** e **\"leaseSets\"** - o routerInfo fornece aos
roteadores os dados necessários para contatar um roteador específico
(suas chaves públicas, endereços de transporte , etc.), enquanto o
leaseSet fornece aos roteadores as informações necessárias para contatar
um destino específico. Um leaseSet contém uma série de \"leases\". Cada
um desses arrendamentos especifica um gateway de túnel, que permite
atingir um destino específico. As informações completas contidas em um
arrendamento:

- Gateway de entrada para um túnel que permite chegar a um destino
 específico.
- Tempo em que um túnel expira.
- Par de chaves públicas para poder criptografar mensagens (para
 enviar através do túnel e chegar ao destino).

Os próprios roteadores enviam suas routerInfo para o netDb diretamente,
enquanto os leaseSets são enviados por meio de túneis de saída (os
leaseSets precisam ser enviados anonimamente para evitar correlacionar
um roteador com seus leaseSets).

Podemos combinar os conceitos acima para construir conexões
bem-sucedidas na rede.

Para construir seus próprios túneis de entrada e saída, Alice faz uma
pesquisa no netDb para coletar routerInfo. Dessa forma, ela reúne listas
de pares que pode usar como saltos em seus túneis. Ela pode então enviar
uma mensagem de construção para o primeiro salto, solicitando a
construção de um túnel e pedindo que o roteador envie a mensagem de
construção adiante, até que o túnel seja construído.

::: {.box style="text-align:center;"}
\
\
![Request information on other
routers](images/netdb_get_routerinfo_1.png "Request information on other routers")
                   \
\
![Build tunnel using router
information](images/netdb_get_routerinfo_2.png "Build tunnel using router information")\
\
Figura 2: Informação dos roteadores é usada para construir túneis.
:::

\

Quando Alice quer enviar uma mensagem para Bob, ela primeiro faz uma
pesquisa no netDb para encontrar o leaseSet de Bob, dando a ela seus
gateways de túnel de entrada atuais. Ela então escolhe um de seus túneis
de saída e envia a mensagem por ele com instruções para o ponto final do
túnel de saída encaminhar a mensagem em para um dos gateways de túnel de
entrada de Bob. Quando o ponto final do túnel de saída recebe essas
instruções, ele encaminha a mensagem conforme solicitado, e quando o
gateway de túnel de entrada de Bob a recebe, ela é encaminhada pelo
túnel para o roteador de Bob. Se Alice quiser que Bob seja capaz de
responder à mensagem, ela precisa transmitir seu próprio destino
explicitamente como parte da própria mensagem. Isso pode ser feito
introduzindo uma camada de nível superior, o que é feito na biblioteca
de streaming [](#app.streaming) . Alice também pode reduzir o tempo de
resposta agrupando seu LeaseSet mais recente com a mensagem para que Bob
não precise fazer uma pesquisa no netDb quando quiser responder, mas
isso é opcional.

::: {.box style="text-align:center;"}
\
\
![Connect tunnels using
LeaseSets](images/netdb_get_leaseset.png "Connect tunnels using leaseSets")\
\
Figura 3: LeaseSets são usados para conectar túneis de saída e entrada.
:::

\

Enquanto os próprios túneis têm criptografia em camadas para impedir a
divulgação não autorizada para pares dentro da rede (como a própria
camada de transporte faz para impedir a divulgação não autorizada para
pares fora da rede), é necessário adicionar uma camada adicional de
criptografia de ponta a ponta para ocultar a mensagem do ponto final do
túnel de saída e do gateway do túnel de entrada. Esta \"[garlic
criptografia](#op.garlic)\" permite que o roteador de Alice envolva
várias mensagens em uma única \"mensagem de alho\", criptografada para
uma chave pública específica para que os pares intermediários não possam
determinar quantas mensagens estão dentro do alho, o que essas mensagens
dizem ou para onde esses dentes individuais são destinados. Para uma
comunicação típica de ponta a ponta entre Alice e Bob, o alho será
criptografado para a chave pública publicada no leaseSet de Bob,
permitindo que a mensagem seja criptografada sem fornecer a chave
pública ao próprio roteador de Bob.

Outro fato importante a ter em mente é que o I2P é inteiramente baseado
em mensagens e que algumas mensagens podem ser perdidas ao longo do
caminho. Os aplicativos que usam I2P podem usar as interfaces orientadas
a mensagens e cuidar de suas próprias necessidades de controle e
confiabilidade de congestionamento , mas a maioria seria melhor atendida
reutilizando a biblioteca streaming [fornecida](#app.streaming) para
visualizar o I2P como uma rede baseada em fluxos .

## Túneis {#op.tunnels}

Tanto os túneis de entrada quanto os de saída funcionam com princípios
semelhantes. O gateway do túnel acumula uma série de mensagens de túnel,
eventualmente pré-processando-as em algo para entrega no túnel. Em
seguida, o gateway criptografa os dados pré-processados e os encaminha
para o primeiro salto. Esse par e os participantes subsequentes do túnel
adicionam uma camada de criptografia após verificar se não é uma
duplicata antes de encaminhá-la para o próximo par. Eventualmente, a
mensagem chega ao ponto final onde as mensagens são divididas novamente
e encaminhadas conforme solicitado. A diferença de surge no que o
criador do túnel faz - para túneis de entrada, o criador é o ponto final
e ele simplesmente descriptografa todas as camadas adicionadas, enquanto
para túneis de saída, o criador é o gateway e ele pré-descriptografa
todas as camadas para que, depois que todas as camadas de criptografia
por salto forem adicionadas, a mensagem chegue limpa ao ponto final do
túnel.

A escolha de pares específicos para passar mensagens, bem como sua
ordenação particular, é importante para entender tanto o anonimato
quanto as características de desempenho do I2P. Enquanto o banco de
dados da rede (abaixo) tem seus próprios critérios para escolher quais
pares consultar e armazenar entradas, os criadores de túneis podem usar
quaisquer pares na rede em qualquer ordem (e até mesmo qualquer número
de vezes) em um único túnel. Se dados de latência e capacidade perfeitos
fossem conhecidos globalmente, a seleção e a ordenação seriam conduzidas
pelas necessidades particulares do cliente em conjunto com seu modelo de
ameaça. Infelizmente, não é fácil coletar dados de latência e capacidade
anonimamente, e depender de pares não confiáveis para fornecer essas
informações tem suas próprias implicações sérias de anonimato.

De uma perspectiva de anonimato, a técnica mais simples seria escolher
pares aleatoriamente de toda a rede, ordená-los aleatoriamente e usar
esses pares nessa ordem por toda a eternidade. De uma perspectiva de
desempenho, a técnica mais simples seria escolher os pares mais rápidos
com a capacidade extra necessária, distribuir a carga entre diferentes
pares para lidar com failover transparente, e reconstruir o túnel sempre
que as informações de capacidade mudarem. Enquanto o primeiro é frágil e
ineficiente, o último requer informações inacessíveis e oferece
anonimato insuficiente. O I2P está trabalhando para oferecer uma gama de
estratégias de seleção de pares, juntamente com o código de medição com
reconhecimento de anonimato para organizar os pares por seus perfis.

Como base, o I2P está constantemente criando perfis dos pares com os
quais interage medindo seu comportamento indireto - por exemplo, quando
um par responde a uma pesquisa netDb em 1,3 segundos, essa latência de
ida e volta é registrada nos perfis para todos os roteadores envolvidos
nos dois túneis (entrada e saída) pelos quais a solicitação e a resposta
passaram, bem como no perfil do par consultado. A medição direta, como
latência ou congestionamento da camada de transporte, não é usada como
parte do perfil, pois pode ser manipulada e associada ao roteador de
medição, expondo-os a ataques triviais. Ao reunir esses perfis, uma
série de cálculos é executada em cada um para resumir seu desempenho -
sua latência, capacidade de lidar com muita atividade, se eles estão
sobrecarregados no momento e quão bem integrados à rede eles parecem
estar. Esses cálculos são então comparados para pares ativos para
organizar os roteadores em quatro níveis - rápido e alta capacidade,
alta capacidade, sem falha, e falhando. Os limites para esses níveis são
determinados dinamicamente e embora eles atualmente usem algoritmos
bastante simples, existem alternativas.

Usando esses dados de perfil, a estratégia de seleção de pares razoável
mais simples é escolher pares aleatoriamente da camada superior (rápido
e de alta capacidade), e isso é atualmente implantado para túneis de
cliente. Túneis exploratórios (usados para gerenciamento de túneis netDb
e ) escolhem pares aleatoriamente da camada \"não falhando\" (que inclui
roteadores em camadas \'melhores\' também), permitindo que o par faça
uma amostragem de roteadores mais amplamente, otimizando efetivamente a
seleção de pares por meio de escalada aleatória de
[](https://en.wikipedia.org/wiki/Hill_climbing). Essas estratégias
sozinhas, no entanto, vazam informações sobre os pares na camada
superior do roteador por meio de ataques de colheita de predecessores e
netDb. Por sua vez, existem diversas alternativas que, embora não
equilibrem a carga de forma tão uniforme, abordarão os ataques
realizados por classes específicas de adversários.

Ao escolher uma chave aleatória e ordenar os pares de acordo com sua
distância XOR dela, as informações vazadas são reduzidas em ataques
predecessores e de coleta de acordo com a taxa de falha dos pares e a
rotatividade da camada. Outra estratégia simples para lidar com ataques
de coleta de netDb é simplesmente consertar o(s) gateway(s) de túnel de
entrada, mas randomizar os pares mais adiante nos túneis. Para lidar com
ataques predecessores para adversários que o cliente contata, os pontos
de extremidade do túnel de saída também permaneceriam fixos. A seleção
de qual peer consertar no ponto mais exposto precisaria, é claro, ter um
limite para a duração, já que todos os peers falham eventualmente, então
poderia ser reativamente ajustado ou proativamente evitado para imitar
um tempo médio medido entre falhas de outros roteadores. Essas duas
estratégias podem, por sua vez, ser combinadas, usando um peer exposto
fixo e uma ordenação baseada em XOR dentro dos próprios túneis. Uma
estratégia mais rígida consertaria os peers exatos e a ordenação de um
túnel potencial, apenas usando peers individuais se todos eles
concordassem em participar da mesma forma a cada vez. Isso varia da
ordenação baseada em XOR, pois o predecessor e o sucessor de cada par
são sempre os mesmos, enquanto o XOR apenas garante que sua ordem não
mude.

As mentioned before, I2P currently (release 0.8) includes the tiered
random strategy above, with XOR-based ordering. A more detailed
discussion of the mechanics involved in tunnel operation, management,
and peer selection can be found in the [tunnel
spec]().

## Banco de dados da rede {#op.netdb}

As mentioned earlier, I2P\'s netDb works to share the network\'s
metadata. This is detailed in [the network
database]() page, but a basic explanation is
available below.

All I2P routers contain a local netDb, but not all routers participate
in the DHT or respond to leaseset lookups. Those routers that do
participate in the DHT and respond to leaseset lookups are called
\'floodfills\'. Routers may be manually configured as floodfills, or
automatically become floodfill if they have enough capacity and meet
other criteria for reliable operation.

Other I2P routers will store their data and lookup data by sending
simple \'store\' and \'lookup\' queries to the floodfills. If a
floodfill router receives a \'store\' query, it will spread the
information to other floodfill routers using the [Kademlia
algorithm](http://en.wikipedia.org/wiki/Kademlia). The \'lookup\'
queries currently function differently, to avoid an important [security
issue](#lookup). When a lookup is done, the
floodfill router will not forward the lookup to other peers, but will
always answer by itself (if it has the requested data).

Dois tipos de informações são armazenadas no banco de dados da rede.

- Um **RouterInfo** armazena informações sobre um roteador I2P
 específico e como contatá-lo
- Um **LeaseSet** armazena informações sobre um destino específico
 (por exemplo, site I2P, servidor de e-mail\...)

Todas essas informações são assinadas pela parte publicadora e
verificadas por qualquer roteador I2P que use ou armazene as
informações. Além disso, os dados contêm informações de tempo, para
evitar o armazenamento de entradas antigas e possíveis ataques. É também
por isso que o I2P agrupa o código necessário para manter o tempo
correto, consultando ocasionalmente alguns servidores SNTP (o
[pool.ntp.org](http://www.pool.ntp.org/) round robin por padrão) e
detectando distorção entre roteadores na camada de transporte.

Algumas observações adicionais também são importantes.

- **Conjuntos de arrendamento não publicados e criptografados:**

 One could only want specific people to be able to reach a
 destination. This is possible by not publishing the destination in
 the netDb. You will however have to transmit the destination by
 other means. This is supported by \'encrypted leaseSets\'. These
 leaseSets can only be decoded by people with access to the
 decryption key.

- **Inicialização:**

 Bootstrapping the netDb is quite simple. Once a router manages to
 receive a single routerInfo of a reachable peer, it can query that
 router for references to other routers in the network. Currently, a
 number of users post their routerInfo files to a website to make
 this information available. I2P automatically connects to one of
 these websites to gather routerInfo files and bootstrap. I2P calls
 this bootstrap process \"reseeding\".

- **Escalabilidade de pesquisa:**

 Lookups in the I2P network are iterative, not recursive. If a lookup
 from a floodfill fails, the lookup will be repeated to the
 next-closest floodfill. The floodfill does not recursively ask
 another floodfill for the data. Iterative lookups are scalable to
 large DHT networks.

## Protocolos de transporte {#op.transport}

A comunicação entre roteadores precisa fornecer confidencialidade e
integridade contra adversários externos enquanto autentica que o
roteador contatado é aquele que deve receber uma determinada mensagem.
Os detalhes de como os roteadores se comunicam com outros roteadores não
são críticos - três protocolos separados foram usados em diferentes
pontos para fornecer essas necessidades básicas.

I2P currently supports two transport protocols,
[NTCP2]() over TCP, and
[SSU2]() over UDP. These have replaced the
previous versions of the protocols, [NTCP]() and
[SSU](), which are now deprecated. Both protocols
support both IPv4 and IPv6. By supporting both TCP and UDP transports,
I2P can effectively traverse most firewalls, including those intended to
block traffic in restrictive censorship regimes. NTCP2 and SSU2 were
designed to use modern encryption standards, improve traffic
identification resistance, increase efficiency and security, and make
NAT traversal more robust. Routers publish each supported transport and
IP address in the network database. Routers with access to public IPv4
and IPv6 networks will usually publish four addresses, one for each
combination of NTCP2/SSU2 with IPv4/IPv6.

[SSU2]() supports and extends the goals of SSU.
SSU2 has many similarities to other modern UDP-based protocols such as
Wireguard and QUIC. In addition to the reliable transport of network
messages over UDP, SSU2 provides specialized facilities for
peer-to-peer, cooperative IP address detection, firewall detection, and
NAT traversal. As described in the [SSU spec]():

> O objetivo deste protocolo é fornecer entrega de mensagens segura,
> autenticada, semiconfiável e não ordenada, expondo apenas uma
> quantidade mínima de dados facilmente discerníveis para terceiros. Ele
> deve suportar comunicação de alto grau , bem como controle de
> congestionamento amigável ao TCP e pode incluir detecção de PMTU. Ele
> deve ser capaz de mover dados em massa de forma eficiente a taxas
> suficientes para usuários domésticos. Além disso, ele deve suportar
> técnicas para abordar obstáculos de rede, como a maioria dos NATs ou
> firewalls.

NTCP2 supports and extends the goals of NTCP. It provides an efficient
and fully encrypted transport of network messages over TCP, and
resistance to traffic identification, using modern encryption standards.

O I2P suporta múltiplos transportes simultaneamente. Um transporte
particular para uma conexão de saída é selecionado com \"bids\". Cada
transporte faz um lance para a conexão e o valor relativo desses lances
atribui a prioridade. Os transportes podem responder com lances
diferentes, dependendo se já existe uma conexão estabelecida com o peer.

The bid (priority) values are implementation-dependent and may vary
based on traffic conditions, connection counts, and other factors.
Routers also publish their transport preferences for inbound connections
in the network database as transport \"costs\" for each transport and
address.

## Criptografia {#op.crypto}

I2P uses cryptography at several protocol layers for encryption,
authentication, and verification. The major protocol layers are:
transports, tunnel build messages, tunnel layer encryption, network
database messages, and end-to-end (garlic) messages. I2P\'s original
design used a small set of cryptographic primitives that at the time
were considered secure. These included ElGamal asymmetric encryption,
DSA-SHA1 signatures, AES256/CBC symmetric encryption, and SHA-256
hashes. As available computing power increased and cryptographic
research evolved substantially over the years, I2P needed to upgrade its
primitives and protocols. Therefore, we added a concept of \"encryption
types\" and \"signature types\", and extended our protocols to include
these identifiers and indicate support. This allows us to periodically
update and extend the network support for modern cryptography and
future-proof the network for new primitives, without breaking backward
compatibility or requiring a \"flag day\" for network updates. Some
signature and encryption types are also reserved for experimental use.

The current primitives used in most protocol layers are X25519 key
exchange, EdDSA signatures, ChaCha20/Poly1305 authenticated symmetric
encryption, and SHA-256 hashes. AES256 is still used for tunnel layer
encryption. These modern protocols are used for the vast majority of
network communication Older primitives including ElGamal, ECDSA, and
DSA-SHA1 continue to be supported by most implementations for backward
compatibility when communicating with older routers. Some old protocols
have been deprecated and/or removed completely. In the near future we
will begin research on a migration to post-quantum (PQ) or hybrid-PQ
encryption and signatures to maintain our robust security standards.

These cryptographic primitives are combined together to provide I2P\'s
layered defenses against a variety of adversaries. At the lowest level,
inter-router communication is protected by the transport layer security.
[Tunnel](#op.tunnels) messages passed over the transports have their own
layered encryption. Various other messages are passed along inside
\"garlic messages\", which are also encrypted.

### Mensagens de alho {#op.garlic}

Garlic messages are an extension of \"onion\" layered encryption,
allowing the contents of a single message to contain multiple
\"cloves\" - fully formed messages alongside their own instructions for
delivery. Messages are wrapped into a garlic message whenever the
message would otherwise be passing in cleartext through a peer who
should not have access to the information - for instance, when a router
wants to ask another router to participate in a tunnel, they wrap the
request inside a garlic, encrypt that garlic to the receiving router\'s
public key, and forward it through a tunnel. Another example is when a
client wants to send a message to a destination - the sender\'s router
will wrap up that data message (alongside some other messages) into a
garlic, encrypt that garlic to the public key published in the
recipient\'s leaseSet, and forward it through the appropriate tunnels.

As \"instruções\" anexadas a cada cravo dentro da camada de criptografia
incluem a capacidade de solicitar que o cravo seja encaminhado
localmente, para um roteador remoto, ou para um túnel remoto em um
roteador remoto. Há campos nessas instruções permitindo que um par
solicite que a entrega seja adiada até que um certo tempo ou condição
seja atendida, embora eles não sejam honrados até que os [atrasos não
triviais](#future.variablelatency) sejam implantados. É possível rotear
explicitamente mensagens de alho qualquer número de saltos sem construir
túneis, ou mesmo redirecionar mensagens de túnel envolvendo-as em
mensagens de alho e encaminhando-as um número de saltos antes de
entregá-las ao próximo salto no túnel, mas essas técnicas não são usadas
atualmente na implementação existente.

### Etiquetas de sessão {#op.sessiontags}

As an unreliable, unordered, message based system, I2P uses a simple
combination of asymmetric and symmetric encryption algorithms to provide
data confidentiality and integrity to garlic messages. The original
combination was referred to as ElGamal/AES+SessionTags, but that is an
excessively verbose way to describe the simple use of 2048bit ElGamal,
AES256, SHA256 and 32 byte nonces. While this protocol is still
supported, most of the network has migrated to a new protocol,
ECIES-X25519-AEAD-Ratchet. This protocol combines X25519,
ChaCha20/Poly1305, and a synchronized PRNG to generate the 32 byte
nonces. Both protocols will be briefly described below.

#### ElGamal/AES+SessionTags {#op.elg}

Na primeira vez que um roteador deseja criptografar uma mensagem de alho
para outro roteador, ele criptografa o material de chaveamento para uma
chave de sessão AES256 com ElGamal e anexa a carga criptografada
AES256/CBC após o bloco ElGamal criptografado. Além da carga
criptografada, a seção criptografada AES contém o comprimento da carga ,
o hash SHA256 da carga não criptografada, bem como um número de
\"etiquetas de sessão\" - nonces aleatórios de 32 bytes. Na próxima vez
que o remetente quiser criptografar uma mensagem garlic para outro
roteador, em vez de ElGamal criptografar uma nova chave de sessão, eles
simplesmente escolhem uma das tags de sessão entregues anteriormente e
criptografam o payload com AES como antes, usando a chave de sessão
usada com aquela tag de sessão, prefixada com a própria tag de sessão.
Quando um roteador recebe uma mensagem criptografada garlic, eles
verificam os primeiros 32 bytes para ver se ela corresponde a uma tag de
sessão disponível - se corresponder, eles simplesmente descriptografam a
mensagem com AES, mas se não corresponder, eles descriptografam o
primeiro bloco com ElGamal.

Cada tag de sessão pode ser usada apenas uma vez para evitar que
adversários internos correlacionem desnecessariamente mensagens
diferentes como sendo entre os mesmos roteadores . O remetente de uma
mensagem criptografada ElGamal/AES+SessionTag escolhe quando e quantas
tags entregar, pré-estocando o destinatário com tags suficientes para
cobrir uma saraivada de mensagens. Mensagens de alho podem detectar a
entrega bem-sucedida da tag ao agrupar uma pequena mensagem adicional
como um cravo (uma \"mensagem de status de entrega \") - quando a
mensagem de alho chega ao destinatário pretendido e é descriptografada
com sucesso, esta pequena mensagem de status de entrega é um dos cravos
expostos e tem instruções para o destinatário enviar o cravo de volta ao
remetente original (por meio de um túnel de entrada, é claro). Quando o
remetente original recebe esta mensagem de status de entrega, ele sabe
que as tags de sessão agrupadas na mensagem de alho foram entregues com
sucesso.

As próprias tags de sessão têm uma vida útil muito curta, após a qual
são descartadas se não forem usadas. Além disso, a quantidade armazenada
para cada chave é limitada, assim como o número de chaves em si - se
muitas chegarem, mensagens novas ou antigas podem ser descartadas. O
remetente mantém o controle se as mensagens usando as tags de sessão
estão sendo transmitidas e, se não houver comunicação suficiente, ele
pode descartar aquelas que antes eram consideradas entregues
corretamente, revertendo para a criptografia ElGamal completa e cara.

#### ECIES-X25519-AEAD-Ratchet {#op.ratchet}

ElGamal/AES+SessionTags required substantial overhead in a number of
ways. CPU usage was high because ElGamal is quite slow. Bandwidth was
excessive because large numbers of session tags had to be delivered in
advance, and because ElGamal public keys are very large. Memory usage
was high due to the requirement to store large amounts of session tags.
Reliability was hampered by lost session tag delivery.

ECIES-X25519-AEAD-Ratchet was designed to address these issues. X25519
is used for key exchange. ChaCha20/Poly1305 is used for authenticated
symmetric encryption. Encryption keys are \"double ratcheted\" or
rotated periodically. Session tags are reduced from 32 bytes to 8 bytes
and are generated with a PRNG. The protocol has many similarities to the
signal protocol used in Signal and WhatsApp. This protocol provides
substantially lower overhead in CPU, RAM, and bandwidth.

The session tags are generated from a deterministic synchronized PRNG
running at both ends of the session to generate session tags and session
keys. The PRNG is a HKDF using a SHA-256 HMAC, and is seeded from the
X25519 DH result. Session tags are never transmitted in advance; they
are only included with the message. The receiver stores a limited number
of session keys, indexed by session tag. The sender does not need to
store any session tags or keys because they are not sent in advance;
they may be generated on-demand. By keeping this PRNG roughly
synchronized between the sender and recipient (the recipient precomputes
a window of the next e.g. 50 tags), the overhead of periodically
bundling a large number of tags is removed.

# Futuro {#future}

I2P\'s protocols are efficient on most platforms, including cell phones,
and secure for most threat models. However, there are several areas
which require further improvement to meet the needs of those facing
powerful state-sponsored adversaries, and to meet the threats of
continued cryptographic advances and ever-increasing computing power.
Two possible features, restricted routes and variable latency, were
propsed by jrandom in 2003. While we no longer plan to implement these
features, they are described below.

## Operação de rota restrita {#future.restricted}

I2P é uma rede de sobreposição projetada para ser executada em cima de
um pacote funcional rede comutada, explorando o princípio de ponta a
ponta para oferecer anonimato e segurança. Enquanto a Internet não
abraça mais completamente o princípio de ponta a ponta (devido ao uso de
NAT), I2P requer que uma porção substancial da rede seja alcançável -
pode haver um número de pares ao longo das bordas executando usando
rotas restritas, mas I2P não inclui um algoritmo de roteamento
apropriado para o caso degenerado onde a maioria dos pares são
inalcançáveis. No entanto, funcionaria em cima de uma rede empregando
tal algoritmo.

Restricted route operation, where there are limits to what peers are
reachable directly, has several different functional and anonymity
implications, dependent upon how the restricted routes are handled. At
the most basic level, restricted routes exist when a peer is behind a
NAT or firewall which does not allow inbound connections. This was
largely addressed by integrating distributed hole punching into the
transport layer, allowing people behind most NATs and firewalls to
receive unsolicited connections without any configuration. However, this
does not limit the exposure of the peer\'s IP address to routers inside
the network, as they can simply get introduced to the peer through the
published introducer.

Beyond the functional handling of restricted routes, there are two
levels of restricted operation that can be used to limit the exposure of
one\'s IP address - using router-specific tunnels for communication, and
offering \'client routers\'. For the former, routers can either build a
new pool of tunnels or reuse their exploratory pool, publishing the
inbound gateways to some of them as part of their routerInfo in place of
their transport addresses. When a peer wants to get in touch with them,
they see those tunnel gateways in the netDb and simply send the relevant
message to them through one of the published tunnels. If the peer behind
the restricted route wants to reply, it may do so either directly (if
they are willing to expose their IP to the peer) or indirectly through
their outbound tunnels. When the routers that the peer has direct
connections to want to reach it (to forward tunnel messages, for
instance), they simply prioritize their direct connection over the
published tunnel gateway. The concept of \'client routers\' simply
extends the restricted route by not publishing any router addresses.
Such a router would not even need to publish their routerInfo in the
netDb, merely providing their self signed routerInfo to the peers that
it contacts (necessary to pass the router\'s public keys).

Existem compensações para aqueles que estão atrás de rotas restritas,
pois eles provavelmente participarão menos frequentemente dos túneis de
outras pessoas, e os roteadores aos quais estão conectados poderão
inferir padrões de tráfego que não estariam expostos de outra forma. Por
outro lado, se o custo dessa exposição for menor do que o custo de um IP
ser disponibilizado, pode valer a pena. Isso, é claro, assume que os
pares com os quais o roteador atrás de uma rota restrita entra em
contato não são hostis - ou a rede é grande o suficiente para que a
probabilidade de usar um par hostil para se conectar seja pequena o
suficiente, ou pares confiáveis (e talvez temporários) são usados em vez
disso.

Restricted routes are complex, and the overall goal has been largely
abandoned. Several related improvements have greatly reduced the need
for them. We now support UPnP to automatically open firewall ports. We
support both IPv4 and IPv6. SSU2 improved address detection, firewall
state determination, and cooperative NAT hole punching. SSU2, NTCP2, and
address compatibility checks ensure that tunnel hops can connect before
the tunnel is built. GeoIP and country identification allow us to avoid
peers in countries with restrictive firewalls. Support for \"hidden\"
routers behind those firewalls has improved. Some implementations also
support connections to peers on overlay networks such as Yggdrasil.

## Latência variável {#future.variablelatency}

Embora a maior parte dos esforços iniciais do I2P tenham sido em
comunicação de baixa latência, ele foi projetado com serviços de
latência variável em mente desde o início. No nível mais básico, os
aplicativos executados no topo do I2P podem oferecer o anonimato da
comunicação de latência média e alta, ao mesmo tempo em que misturam
seus padrões de tráfego com tráfego de baixa latência. Internamente,
porém, o I2P pode oferecer sua própria comunicação de latência média e
alta por meio da criptografia garlic - especificando que a mensagem deve
ser enviada após um certo atraso, em um certo tempo, após um certo
número de mensagens terem passado ou outra estratégia de mistura. Com a
criptografia em camadas, apenas o roteador que o cravo expôs a
solicitação de atraso saberia que a mensagem requer alta latência,
permitindo que o tráfego se misture ainda mais com o tráfego de baixa
latência. Uma vez que a pré-condição de transmissão é atendida, o
roteador que mantém o cravo (que provavelmente seria uma mensagem de
alho) simplesmente o encaminha conforme solicitado - para um roteador,
para um túnel, ou, mais provavelmente, para um destino de cliente
remoto.

The goal of variable latency services requires substantial resources for
store-and-forward mechanisms to support it. These mechanisms can and are
supported in various messaging applications, such as i2p-bote. At the
network level, alternative networks such as Freenet provide these
services. We have decided not to pursue this goal at the I2P router
level.

# Sistemas similares {#similar}

A arquitetura do I2P se baseia nos conceitos de middleware orientado a
mensagens, a topologia de DHTs, o anonimato e criptografia de mixnets de
rota livre, e a adaptabilidade de redes comutadas por pacotes. O valor
não vem de novos conceitos de algoritmos, mas de uma engenharia
cuidadosa combinando os resultados de pesquisa de sistemas e artigos
existentes. Embora existam alguns esforços semelhantes que valem a pena
revisar, tanto para comparações técnicas quanto funcionais, dois em
particular são retirados aqui - Tor e Freenet.

See also the [Network Comparisons Page]().
Note that these descriptions were written by jrandom in 2003 and may not
currently be accurate.

## Tor {#similar.tor}

*[website](https://www.torproject.org/)*

À primeira vista, Tor e I2P têm muitas similaridades funcionais e
relacionadas ao anonimato . Embora o desenvolvimento do I2P tenha
começado antes de estarmos cientes dos esforços iniciais do estágio no
Tor, muitas das lições do roteamento onion original e dos esforços do
ZKS foram integradas ao design do I2P. Em vez de construir um sistema
essencialmente confiável e centralizado com servidores de diretório, o
I2P tem um banco de dados de rede auto-organizado com cada par assumindo
a responsabilidade de criar perfis de outros roteadores para determinar
a melhor forma de explorar os recursos disponíveis. Outra diferença
fundamental é que, enquanto I2P e Tor usam caminhos em camadas e
ordenados (túneis e circuitos/fluxos), I2P é fundamentalmente uma rede
comutada por pacotes, enquanto Tor é fundamentalmente uma rede comutada
por circuitos, permitindo que I2P roteie de forma transparente em torno
de congestionamentos ou outras falhas de rede, opere caminhos
redundantes e balanceie a carga dos dados entre os recursos disponíveis.
Enquanto o Tor oferece a funcionalidade outproxy útil ao oferecer
descoberta outproxy integrada e seleção, o I2P deixa essas decisões da
camada de aplicação para os aplicativos executados sobre o I2P - na
verdade, o I2P até externalizou a própria biblioteca de streaming
semelhante ao TCP para a camada de aplicação, permitindo que os
desenvolvedores experimentem diferentes estratégias, explorando seu
conhecimento específico de domínio para oferecer melhor desempenho.

De uma perspectiva de anonimato, há muita similaridade quando as redes
principais são comparadas. No entanto, há algumas diferenças
importantes. Ao lidar com um adversário interno ou a maioria dos
adversários externos, os túneis simplex do I2P expõem metade dos dados
de tráfego que seriam expostos com os circuitos duplex do Tor
simplesmente observando os próprios fluxos - uma solicitação e resposta
HTTP seguiriam o mesmo caminho no Tor, enquanto no I2P os pacotes que
compõem a solicitação sairiam por um ou mais túneis de saída e os
pacotes que compõem a resposta retornariam por um ou mais túneis de
entrada diferentes. Embora as estratégias de seleção e ordenação de
pares do I2P devam abordar suficientemente ataques predecessores, caso
seja necessária uma mudança para túneis bidirecionais, poderíamos
simplesmente construir um túnel de entrada e saída ao longo dos mesmos
roteadores.

Outro problema de anonimato surge no uso da criação de túneis
telescópicos pelo Tor, como simples contagem de pacotes e medições de
tempo, já que as células em um circuito passam pelo nó de um adversário
expõem informações estatísticas sobre onde o adversário está dentro do
circuito. A criação de túneis unidirecionais do I2P com uma única
mensagem para que esses dados não sejam expostos. Proteger a posição em
um túnel é importante, pois um adversário seria capaz de montar uma
série de poderosos ataques de predecessor, interseção e confirmação de
tráfego.

No geral, Tor e I2P se complementam em seu foco - Tor trabalha para
oferecer outproxying anônimo de Internet de alta velocidade, enquanto
I2P trabalha para oferecer uma rede resiliente descentralizada em si. Em
teoria, ambos podem ser usados para atingir ambos os propósitos, mas
dados os recursos limitados de desenvolvimento, ambos têm seus pontos
fortes e fracos. Os desenvolvedores do I2P consideraram as etapas
necessárias para modificar o Tor para aproveitar o design do I2P, mas
preocupações da viabilidade do Tor sob escassez de recursos sugerem que
a arquitetura de comutação de pacotes do I2P será capaz de explorar
recursos escassos de forma mais eficaz.

## Freenet {#similar.freenet}

*[website](http://www.freenetproject.org/)*

A Freenet desempenhou um papel importante nos estágios iniciais do
design do I2P - dando provas da viabilidade de uma vibrante comunidade
pseudônima completamente contida dentro da rede, demonstrando que os
perigos inerentes a outproxies poderiam ser evitados. A primeira semente
do I2P começou como uma camada de comunicação de substituição para a
Freenet, tentando fatorar as complexidades de uma comunicação ponto a
ponto escalável, anônima e segura das complexidades de um armazenamento
de dados distribuído resistente à censura. Com o tempo, no entanto,
alguns dos problemas de anonimato e escalabilidade inerentes aos
algoritmos da Freenet deixaram claro que o foco do I2P deveria
permanecer estritamente em fornecer uma camada de comunicação genérica
anônima, em vez de um componente da Freenet. Com o passar dos anos, os
desenvolvedores da Freenet passaram a ver as fraquezas no design antigo,
o que os levou a sugerir que eles exigiriam uma camada \"pré-mistura\"
para oferecer anonimato substancial. Em outras palavras, a Freenet
precisa ser executada sobre uma mixnet como I2P ou Tor, com \"nós
clientes\" solicitando e publicando dados através da mixnet para os
\"nós servidores\" que então buscam e armazenam os dados de acordo com
os algoritmos heurísticos de armazenamento de dados distribuídos da
Freenet.

A funcionalidade que a Freenet oferece é bastante complementar a
fornecida pela I2P. Enquanto a Freenet fornece nativamente muitas das
ferramentas para operacionalizar sistemas de alta e média latências, a
I2P fornece nativamente uma rede mix de baixa latência apropriada para
oferecer um anonimato adequado. A lógica de separar a rede mix do
sistema de armazenamento distribuído e resiliente a censura parece ainda
ser auto-evidente do ponto de vista de engenharia, anonimato, segurança
e alocação de recursos, de modo que se espera que a equipe da Freenet
prosseguirá com esforços nessa direção, se não simplesmente reusando (ou
ajudando a melhorar, na medida do necessário) as redes mix existentes
como I2P ou Tor.

# Appendix A: Application layer {#app}

O I2P em si não faz muita coisa - ele simplesmente envia mensagens para
destinos remotos e recebe mensagens direcionadas a destinos locais - a
maior parte do trabalho interessante acontece nas camadas acima dele.
Por si só, o I2P pode ser visto como uma camada IP anônima e segura, e a
biblioteca de streaming [](#app.streaming) empacotada como uma
implementação de uma camada TCP anônima e segura sobre ela. Além disso,
[I2PTunnel](#app.i2ptunnel) expõe um sistema genérico de proxy TCP para
entrar ou sair da rede I2P, além de uma variedade de aplicativos de rede
que fornecem mais funcionalidade para usuários finais.

## Biblioteca de streaming {#app.streaming}

A biblioteca de streaming I2P pode ser vista como uma interface de
streaming genérica (espelhando soquetes TCP), e a implementação suporta
um [protocolo de janela
deslizante](http://en.wikipedia.org/wiki/Sliding_Window_Protocol) com
várias otimizações, para levar em conta o alto atraso sobre I2P. Os
fluxos individuais podem ajustar o tamanho máximo do pacote e outras
opções, embora o padrão de 4 KB compactados pareça uma troca razoável
entre os custos de largura de banda da retransmissão de mensagens
perdidas e a latência de múltiplas mensagens.

Além disso, em consideração ao custo relativamente alto das mensagens
subsequentes, o protocolo da biblioteca de streaming para agendamento e
entrega de mensagens foi otimizado para permitir que mensagens
individuais passadas contenham o máximo de informações disponíveis. Por
exemplo, uma pequena transação HTTP com proxy por meio da biblioteca de
streaming pode ser concluída em uma única viagem de ida e volta - a
primeira mensagem agrupa um SYN, FIN e a pequena carga útil (uma
solicitação HTTP normalmente se encaixa) e a resposta agrupa o SYN, FIN,
ACK e a pequena carga útil (muitas respostas HTTP se encaixam). Embora
um ACK adicional deva ser transmitido para informar ao servidor HTTP que
o SYN/FIN/ACK foi recebido, o proxy HTTP local pode entregar a resposta
completa ao navegador imediatamente.

No geral, no entanto, a biblioteca de streaming tem muita semelhança com
uma abstração do TCP, com suas janelas deslizantes, algoritmos de
controle de congestionamento (início lento e prevenção de
congestionamento) e comportamento geral dos pacotes (ACK, SYN, FIN, RST,
etc.).

## Nomeando biblioteca e livro de endereços {#app.naming}

*For more information see the [Naming and Address
Book]() page.*

*Developed by: *

A nomenclatura dentro do I2P tem sido um tópico frequentemente debatido
desde o início com defensores em todo o espectro de possibilidades. No
entanto, dada a demanda inerente do I2P por comunicação segura e
operação descentralizada, o sistema de nomenclatura tradicional no
estilo DNS está claramente fora, assim como as \"regras da maioria\"
sistemas de votação. Em vez disso, o I2P vem com uma biblioteca de
nomenclatura genérica e uma implementação base projetada para trabalhar
com um nome local para mapeamento de destino, bem como um aplicativo
complementar opcional chamado \"Address Book\". O catálogo de endereços
é um sistema de nomenclatura seguro, distribuído e legível por humanos,
orientado por uma rede de confiança, sacrificando apenas a chamada para
que todos os nomes legíveis por humanos sejam globalmente únicos ao
exigir apenas a exclusividade local. Enquanto todas as mensagens no I2P
são criptograficamente endereçadas por seu destino, pessoas diferentes
podem ter entradas no catálogo de endereços local para \"Alice\" que se
referem a destinos diferentes. As pessoas ainda podem descobrir novos
nomes importando catálogos de endereços publicados de pares
especificados em sua rede de confiança, adicionando as entradas
fornecidas por terceiros, ou (se algumas pessoas organizarem uma série
de catálogos de endereços publicados usando um sistema de registro por
ordem de chegada, primeiro a ser atendido) as pessoas podem escolher
tratar esses catálogos de endereços como servidores de nomes, emulando o
DNS tradicional.

O I2P não promove o uso de serviços semelhantes ao DNS, pois o dano
causado pelo sequestro de um site pode ser tremendo - e destinos
inseguros não têm valor algum. O DNSsec em si ainda recorre a
registradores e autoridades de certificação, enquanto com o I2P, as
solicitações enviadas a um destino não podem ser interceptadas ou a
resposta falsificada, pois são criptografadas para as chaves públicas do
destino, e um destino em si é apenas um par de chaves públicas e um
certificado. Os sistemas no estilo DNS , por outro lado, permitem que
qualquer um dos servidores de nomes no caminho de pesquisa monte ataques
simples de negação de serviço e falsificação. Adicionar um certificado
autenticando as respostas como assinadas por alguma autoridade de
certificação centralizada resolveria muitos dos problemas de servidores
de nomes hostis, mas deixaria ataques de repetição abertos, bem como
ataques de autoridades de certificação hostis.

A nomeação de estilo de votação também é perigosa, especialmente dada a
eficácia dos ataques Sybil em sistemas anônimos - o invasor pode
simplesmente criar um número arbitrariamente alto de pares e \"votar\"
com cada um para assumir um determinado nome. Métodos de prova de
trabalho podem ser usados para tornar a identidade não livre, mas
conforme a rede cresce, a carga necessária para contatar todos para
conduzir a votação online é implausível, ou se a rede completa não for
consultada, diferentes conjuntos de respostas podem ser alcançáveis.

Assim como na Internet, no entanto, o I2P está mantendo o design e a
operação de um sistema de nomenclatura fora da camada de comunicação
(semelhante ao IP). A biblioteca de nomenclatura empacotada inclui uma
interface simples de provedor de serviços na qual sistemas de
nomenclatura alternativos podem ser conectados, permitindo que os
usuários finais conduzam que tipo de trocas de nomenclatura eles
preferem.

## I2PTunnel {#app.i2ptunnel}

*Developed by: *

O I2PTunnel é provavelmente o aplicativo cliente mais popular e versátil
do I2P, permitindo proxy genérico dentro e fora da rede I2P. O I2PTunnel
pode ser visto como quatro aplicativos de proxy separados - um
\"cliente\" que recebe conexões TCP de entrada e as encaminha para um
determinado destino I2P, um \"httpclient\" (também conhecido como
\"eepproxy\") que atua como um proxy HTTP e encaminha as solicitações
para o destino I2P apropriado (após consultar o serviço de nomenclatura,
se necessário), um \"servidor\" que recebe conexões de streaming I2P de
entrada em um destino e as encaminha para um determinado host+porta TCP,
e um \"httpserver\" que estende o \"servidor\" analisando a solicitação
e as respostas HTTP para permitir uma operação mais segura. Há um
aplicativo adicional \"socksclient\", mas seu uso não é incentivado
pelos motivos mencionados anteriormente.

O I2P em si não é uma rede outproxy - as preocupações com anonimato e
segurança inerentes a uma rede mix que encaminha dados para dentro e
para fora da mix mantiveram o design do I2P focado em fornecer uma rede
anônima que seja capaz de atender às necessidades do usuário sem exigir
recursos externos. No entanto, o aplicativo I2PTunnel \"httpclient\"
oferece um gancho para outproxy - se o nome do host solicitado não
terminar em \".i2p\", ele escolhe um destino aleatório de um conjunto de
outproxies fornecido pelo usuário e encaminha a solicitação para eles.
Esses destinos são simplesmente instâncias de \"servidor\" I2PTunnel
executadas por voluntários que explicitamente escolheram executar
outproxies - ninguém é um outproxy por padrão, e executar um outproxy
não diz automaticamente a outras pessoas para fazer proxy através de
você. Embora outproxies tenham fraquezas inerentes, eles oferecem uma
prova de conceito simples para usar I2P e fornecem alguma funcionalidade
sob um modelo de ameaça que pode ser suficiente para alguns usuários.

O I2PTunnel habilita a maioria dos aplicativos em uso. Um \"httpserver\"
apontando para um servidor web permite que qualquer um execute seu
próprio site anônimo (ou \"Site I2P\") - um servidor web é empacotado
com o I2P para esse propósito, mas qualquer servidor web pode ser usado.
Qualquer um pode executar um \"cliente\" apontando para um dos
servidores IRC hospedados anonimamente, cada um dos quais está
executando um \"servidor\" apontando para seu IRCd local e se
comunicando entre IRCds por seus próprios túneis \"cliente\". Usuários
do final do também têm túneis \"cliente\" apontando para os destinos
POP3 e SMTP do [I2Pmail](#app.i2pmail) (que por sua vez são simplesmente
instâncias de \"servidor\" apontando para servidores POP3 e SMTP), bem
como túneis \"cliente\" apontando para o servidor CVS do I2P ,
permitindo desenvolvimento anônimo. Às vezes, as pessoas até executaram
proxies \"cliente\" para acessar as instâncias de \"servidor\" apontando
para um servidor NNTP.

## I2PSnark {#app.i2psnark}

*I2PSnark desenvolvido: jrandom, et al, portado de
[mjw](http://www.klomp.org/mark/)\'s
[Snark](http://www.klomp.org/snark/) cliente*

Junto com a instalação do I2P, o I2PSnark oferece um cliente BitTorrent
anônimo simples com recursos multitorrent, expondo todas as
funcionalidades por meio de uma interface web HTML simples.

## I2Pmail/susimail {#app.i2pmail}

*Developed by: *

I2Pmail is more a service than an application - postman offers both
internal and external email with POP3 and SMTP service through I2PTunnel
instances accessing a series of components developed with mastiejaner,
allowing people to use their preferred mail clients to send and receive
mail pseudonymously. However, as most mail clients expose substantial
identifying information, I2P bundles susi23\'s web based susimail client
which has been built specifically with I2P\'s anonymity needs in mind.
The I2Pmail/mail.i2p service offers transparent virus filtering as well
as denial of service prevention with hashcash augmented quotas. In
addition, each user has control of their batching strategy prior to
delivery through the mail.i2p outproxies, which are separate from the
mail.i2p SMTP and POP3 servers - both the outproxies and inproxies
communicate with the mail.i2p SMTP and POP3 servers through I2P itself,
so compromising those non-anonymous locations does not give access to
the mail accounts or activity patterns of the user.


