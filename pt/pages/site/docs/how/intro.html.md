 Uma introdução
suave sobre como o I2P funciona 

O I2P é um projeto para construir, implantar e manter uma rede que
suporte comunicação segura e anônima . Pessoas que usam o I2P estão no
controle das compensações entre anonimato, confiabilidade, uso de
largura de banda e latência. Não há um ponto central na rede sobre o
qual a pressão pode ser exercida para comprometer a integridade,
segurança ou anonimato do sistema. A rede suporta reconfiguração
dinâmica em resposta a vários ataques e foi projetada para fazer uso de
recursos adicionais conforme eles se tornam disponíveis. Claro, todos os
aspectos da rede são abertos e disponíveis gratuitamente.

Diferente de muitas outras redes de anonimização, o I2P não tenta
fornecer anonimato ao esconder o origem de alguma comunicação e não o
destinatário, ou vice-versa. O I2P é projetado para permitir que os
pares usando I2P se comuniquem anonimamente --- tanto o remetente quanto
o destinatário são não identificáveis um para o outro, assim como para
terceiros. Por exemplo, hoje existem tanto sites da web em I2P
(permitindo publicação/hospedagem anônima) quanto proxies HTTP para a
web normal (permitindo navegação anônima na web). Ter a capacidade de
executar servidores dentro do I2P é essencial, pois é muito provável que
quaisquer proxies de saída para a Internet normal sejam monitorados,
desativados, ou até mesmo tomados para tentar ataques mais maliciosos.

The network itself is message oriented - it is essentially a secure and
anonymous IP layer, where messages are addressed to cryptographic keys
(Destinations) and can be significantly larger than IP packets. Some
example uses of the network include \"I2P Sites\" (webservers hosting
normal web applications within I2P), a BitTorrent client (\"I2PSnark\"),
or a distributed data store. With the help of the
[I2PTunnel]() application, we are able to
stream traditional TCP/IP applications over I2P, such as SSH, IRC, a
squid proxy, and even streaming audio. Most people will not use I2P
directly, or even need to know they\'re using it. Instead their view
will be of one of the I2P enabled applications, or perhaps as a little
controller app to turn on and off various proxies to enable the
anonymizing functionality.

An essential part of designing, developing, and testing an anonymizing
network is to define the [threat model](),
since there is no such thing as \"true\" anonymity, just increasingly
expensive costs to identify someone. Briefly, I2P\'s intent is to allow
people to communicate in arbitrarily hostile environments by providing
good anonymity, mixed in with sufficient cover traffic provided by the
activity of people who require less anonymity. This way, some users can
avoid detection by a very powerful adversary, while others will try to
evade a weaker entity, *all on the same network*, where each one\'s
messages are essentially indistinguishable from the others.

## Por que?

There are a multitude of reasons why we need a system to support
anonymous communication, and everyone has their own personal rationale.
There are many [other efforts]() working on
finding ways to provide varying degrees of anonymity to people through
the Internet, but we could not find any that met our needs or threat
model.

## Como?

The network at a glance is made up of a set of nodes (\"routers\") with
a number of unidirectional inbound and outbound virtual paths
(\"tunnels\", as outlined on the [tunnel
routing]() page). Each router is
identified by a cryptographic RouterIdentity which is typically long
lived. These routers communicate with each other through existing
transport mechanisms (TCP, UDP, etc), passing various messages. Client
applications have their own cryptographic identifier (\"Destination\")
which enables it to send and receive messages. These clients can connect
to any router and authorize the temporary allocation (\"lease\") of some
tunnels that will be used for sending and receiving messages through the
network. I2P has its own internal [network
database]() (using a modification of the Kademlia
algorithm) for distributing routing and contact information securely.

::: {.box style="text-align:center;"}
![Exemplo de topologia de
rede](images/net.png "Exemplo de topologia de rede")
:::

Acima, Alice, Bob, Charlie e Dave estão todos executando roteadores com
um único Destino em seu roteador local. Cada um deles tem um par de
túneis de entrada de 2 saltos por destino (rotulados 1, 2, 3, 4, 5 e 6),
e um pequeno subconjunto de cada pool de túneis de saída desses
roteadores é mostrado com túneis de saída de 2 saltos . Para
simplificar, os túneis de entrada de Charlie e os túneis de saída de
Dave não são mostrados, nem o restante do pool de túneis de saída de
cada roteador (normalmente abastecido com alguns túneis por vez). Quando
Alice e Bob conversam entre si, Alice envia uma mensagem por um de seus
túneis de saída (rosa) visando um dos túneis de entrada (verde) de Bob
(túnel 3 ou 4). Ela sabe enviar para esses túneis no roteador correto
consultando o banco de dados da rede, que é constantemente atualizado
conforme novos leases são autorizados e os antigos expiram.

If Bob wants to reply to Alice, he simply goes through the same
process - send a message out one of his outbound tunnels targeting one
of Alice\'s inbound tunnels (tunnel 1 or 2). To make things easier, most
messages sent between Alice and Bob are
[garlic]() wrapped, bundling the
sender\'s own current lease information so that the recipient can reply
immediately without having to look in the network database for the
current data.

To deal with a wide range of attacks, I2P is fully distributed with no
centralized resources - and hence there are no directory servers keeping
statistics regarding the performance and reliability of routers within
the network. As such, each router must keep and maintain profiles of
various routers and is responsible for selecting appropriate peers to
meet the anonymity, performance, and reliability needs of the users, as
described in the [peer selection]() page.

The network itself makes use of a significant number of [cryptographic
techniques and algorithms]() - a full
laundry list includes 2048bit ElGamal encryption, 256bit AES in CBC mode
with PKCS#5 padding, 1024bit DSA signatures, SHA256 hashes, 2048bit
Diffie-Hellman negotiated connections with station to station
authentication, and [ElGamal /
AES+SessionTag]().

O conteúdo enviado por I2P é criptografado por meio de criptografia de
três camadas: criptografia garlic (usada para verificar a entrega da
mensagem ao destinatário), criptografia de túnel (todas as mensagens que
passam por um túnel são criptografadas pelo gateway do túnel até o ponto
final do túnel) e criptografia de camada de transporte entre roteadores
(por exemplo, o transporte TCP usa AES256 com chaves efêmeras).

Criptografia ponta a ponta (I2CP) (aplicativo cliente para aplicativo
servidor) foi desabilitada na versão 0.6 do I2P; criptografia ponta a
ponta (alho) (roteador cliente I2P para roteador servidor I2P) do
roteador \"a\" de Alice para o roteador \"h\" de Bob permanece. Observe
o uso diferente dos termos ! Todos os dados de a para h são
criptografados ponta a ponta, mas a conexão I2CP entre o roteador I2P e
os aplicativos não são criptografados ponta a ponta! A e h são os
roteadores de Alice e Bob, enquanto Alice e Bob no gráfico a seguir são
os aplicativos em execução no topo do I2P.

::: {.box style="text-align:center;"}
![Criptografia em camadas de ponta a
ponta](images/endToEndEncryption.png "Criptografia em camadas de ponta a ponta")
:::

The specific use of these algorithms are outlined
[elsewhere]().

Os dois principais mecanismos para permitir que pessoas que precisam de
forte anonimato usem a rede são mensagens roteadas garlic explicitamente
atrasadas e túneis mais abrangentes para incluir suporte para mensagens
de pooling e mixagem. Eles estão atualmente planejados para a versão
3.0, mas mensagens roteadas garlic sem atrasos e túneis FIFO estão
atualmente em vigor. Além disso, a versão 2.0 permitirá que pessoas
configurem e operem atrás de rotas restritas (talvez com pares
confiáveis), bem como a implantação de transportes mais flexíveis e
anônimos.

Some questions have been raised with regards to the scalability of I2P,
and reasonably so. There will certainly be more analysis over time, but
peer lookup and integration should be bounded by `O(log(N))` due to the
[network database]()\'s algorithm, while end to
end messages should be `O(1)` (scale free), since messages go out K hops
through the outbound tunnel and another K hops through the inbound
tunnel, with K no longer than 3. The size of the network (N) bears no
impact.

## Quando?

I2P initially began in Feb 2003 as a proposed modification to
[Freenet](http://freenetproject.org) to allow it to use alternate
transports, such as [JMS](), then grew into its own
as an \'anonCommFramework\' in April 2003, turning into I2P in July,
with code being written in earnest starting in August \'03. I2P is
currently under development, following the
[roadmap]().

## Quem?

We have a small [team]() spread around several
continents, working to advance different aspects of the project. We are
very open to other developers who want to get involved and anyone else
who would like to contribute in other ways, such as critiques, peer
review, testing, writing I2P enabled applications, or documentation. The
entire system is open source - the router and most of the SDK are
outright public domain with some BSD and Cryptix licensed code, while
some applications like I2PTunnel and I2PSnark are GPL. Almost everything
is written in Java (1.5+), though some third party applications are
being written in Python and other languages. The code works on [Sun Java
SE](http://java.com/en/) and other Java Virtual Machines.

## Onde?

Anyone interested should join us on the IRC channel #i2p-dev (hosted
concurrently on irc.freenode.net, irc.postman.i2p, irc.echelon.i2p,
irc.dg.i2p and irc.oftc.net). There are currently no scheduled
development meetings, however [archives are
available]().

The current source is available in [git]().

## Informação Adicional

See [the Index to Technical Documentation]().


