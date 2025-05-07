 Roteamento Alho março de 2014 0.9.12 

## Roteamento e Terminologia \"Alho\"

Os termos \"roteamento de alho\" e \"criptografia de alho\" são
frequentemente usados de forma bastante vaga quando se referem à
tecnologia do I2P. Aqui, explicamos a história dos termos, os vários
significados e o uso dos métodos \"de alho\" no I2P.

\"Roteamento de alho\" foi primeiramente mencionado por [Michael J.
Freedman](http://www.cs.princeton.edu/~mfreed/) na  dissertação de
mestrado de Roger Dingledine no Free Haven [Seção
8.1.1](http://www.freehaven.net/papers.html) (junho de 2000), derivado
de [Roteamento Onion](http://www.onion-router.net/).

\"Alho\" pode ter sido usado originalmente por desenvolvedores do I2P
porque o I2P implementa uma forma de agrupamento como Freedman descreve,
ou simplesmente para enfatizar diferenças gerais do Tor. O raciocínio
específico pode estar perdido na história. Geralmente, ao se referir ao
I2P, o termo \"alho\" pode significar uma de três coisas:

1. Criptografia em camadas
2. Agrupando várias mensagens
3. Criptografia ElGamal/AES

Infelizmente, o uso da terminologia \"alho\" pelo I2P nos últimos sete
anos nem sempre foi preciso; portanto, o leitor é advertido ao se
deparar com o termo. Espero que a explicação abaixo esclareça as coisas.

### Criptografia em camadas

O roteamento cebola é uma técnica para construir caminhos, ou túneis,
através de uma série de pares, e então usar esse túnel. As mensagens são
criptografadas repetidamente pelo originador e então descriptografadas
por cada salto. Durante a fase de construção, somente as instruções de
roteamento para o próximo salto são expostas a cada par. Durante a fase
operacional, as mensagens são passadas através do túnel, e a mensagem e
suas instruções de roteamento são expostas somente ao ponto final do
túnel.

This is similar to the way Mixmaster (see [network
comparisons]()) sends messages - taking a
message, encrypting it to the recipient\'s public key, taking that
encrypted message and encrypting it (along with instructions specifying
the next hop), and then taking that resulting encrypted message and so
on, until it has one layer of encryption per hop along the path.

Nesse sentido, \"roteamento alho\" como um conceito geral é idêntico ao
\"roteamento cebola\". Conforme implementado no I2P, é claro, há várias
diferenças em relação à implementação no Tor; veja abaixo. Mesmo assim,
há semelhanças substanciais, de modo que o I2P se beneficia de uma
[grande quantidade de pesquisa acadêmica sobre roteamento
cebola](http://www.onion-router.net/Publications.html), [Tor e mixnets
semelhantes](http://freehaven.net/anonbib/topic.html).

### Agrupando várias mensagens

Michael Freedman definiu \"roteamento alho\" como uma extensão do
roteamento cebola, no qual várias mensagens são agrupadas. Ele chamou
cada mensagem de \"bulbo\". Todas as mensagens, cada uma com suas
próprias instruções de entrega, são expostas no ponto final . Isso
permite o agrupamento eficiente de um \"bloco de resposta\" de
roteamento cebola com a mensagem original.

Este conceito é implementado no I2P, conforme descrito abaixo. Nosso
termo para \"bulbos\" de alho é \"dentes\". Qualquer número de mensagens
pode ser contido, em vez de apenas uma única mensagem. Esta é uma
distinção significativa do roteamento de cebola implementado no Tor. No
entanto, é apenas uma das muitas diferenças arquitetônicas importantes
entre I2P e Tor; talvez não seja, por si só, suficiente para justificar
uma mudança na terminologia.

Outra diferença do método descrito por Freedman é que o caminho é
unidirecional - não há \"ponto de virada\" como visto no roteamento
onion ou nos blocos de resposta do mixmaster, o que simplifica muito o
algoritmo e permite uma entrega mais flexível e confiável.

### Criptografia ElGamal/AES

In some cases, \"garlic encryption\" may simply mean
[ElGamal/AES+SessionTag]() encryption
(without multiple layers).

## Métodos \"Alho\" em I2P

Agora que definimos vários termos \"alho\", podemos dizer que I2P usa
roteamento, agrupamento e criptografia de alho em três lugares:

1. Para construção e roteamento através de túneis (criptografia em
 camadas)
2. Para determinar o sucesso ou o fracasso da entrega de mensagens de
 ponta a ponta (agrupamento)
3. Para publicar algumas entradas de banco de dados de rede (reduzindo
 a probabilidade de um ataque de análise de tráfego bem-sucedido)
 (ElGamal/AES)

Há também maneiras significativas pelas quais essa técnica pode ser
usada para melhorar o desempenho da rede, explorando compensações entre
latência de transporte/taxa de transferência e ramificando dados por
caminhos redundantes para aumentar a confiabilidade.

### Construção e roteamento de túneis

No I2P, os túneis são unidirecionais. Cada parte constrói dois túneis,
um para tráfego de saída e um para tráfego de entrada. Portanto, quatro
túneis são necessários para uma única mensagem de ida e volta e
resposta.

Tunnels are built, and then used, with layered encryption. This is
described on the [tunnel implementation
page](). Tunnel building details are defined
on [this page](). We use
[ElGamal/AES+SessionTag]() for the
encryption.

Tunnels are a general-purpose mechanism to transport all [I2NP
messages](), and [Garlic
Messages](#msg_Garlic) are not used to build
tunnels. We do not bundle multiple [I2NP
messages]() into a single [Garlic
Message](#msg_Garlic) for unwrapping at the
outbound tunnel endpoint; the tunnel encryption is sufficient.

### Agrupamento de mensagens de ponta a ponta

At the layer above tunnels, I2P delivers end-to-end messages between
[Destinations](#struct_Destination).
Just as within a single tunnel, we use
[ElGamal/AES+SessionTag]() for the
encryption. Each client message as delivered to the router through the
[I2CP interface]() becomes a single [Garlic
Clove](#struct_GarlicClove) with its own
[Delivery
Instructions](#struct_GarlicCloveDeliveryInstructions),
inside a [Garlic Message](#msg_Garlic).
Delivery Instructions may specify a Destination, Router, or Tunnel.

Geralmente, uma mensagem de alho conterá apenas um dente. No entanto, o
roteador agrupará periodicamente dois dentes adicionais na mensagem de
alho:

![Garlic Message
Cloves](/_static/images/garliccloves.png "Garlic Message Cloves"){style="text-align:center;"}

1. A [Delivery Status
 Message](#msg_DeliveryStatus), with
 [Delivery
 Instructions](#struct_GarlicCloveDeliveryInstructions)
 specifying that it be sent back to the originating router as an
 acknowledgment. This is similar to the \"reply block\" or \"reply
 onion\" described in the references. It is used for determining the
 success or failure of end to end message delivery. The originating
 router may, upon failure to receive the Delivery Status Message
 within the expected time period, modify the routing to the far-end
 Destination, or take other actions.
2. A [Database Store
 Message](#msg_DatabaseStore), containing a
 [LeaseSet](#struct_LeaseSet) for
 the originating Destination, with [Delivery
 Instructions](#struct_GarlicCloveDeliveryInstructions)
 specifying the far-end destination\'s router. By periodically
 bundling a LeaseSet, the router ensures that the far-end will be
 able to maintain communications. Otherwise the far-end would have to
 query a floodfill router for the network database entry, and all
 LeaseSets would have to be published to the network database, as
 explained on the [network database page]().

By default, the Delivery Status and Database Store Messages are bundled
when the local LeaseSet changes, when additional [Session
Tags](#type_SessionTag) are delivered,
or if the messages have not been bundled in the previous minute. As of
release 0.9.2, the client may configure the default number of Session
Tags to send and the low tag threshold for the current session. See the
[I2CP options specification](#options) for
details. The session settings may also be overridden on a per-message
basis. See the [I2CP Send Message Expires
specification](#msg_SendMessageExpires) for
details.

Obviamente, as mensagens adicionais são atualmente agrupadas para
propósitos específicos, e não fazem parte de um esquema de roteamento de
propósito geral.

A partir da versão 0.9.12, a mensagem de status de entrega é encapsulada
em outra mensagem Garlic pelo originador para que o conteúdo seja
criptografado e não fique visível para os roteadores no caminho de
retorno.

### Armazenamento no banco de dados da rede Floodfill

As explained on the [network database
page](#delivery), local
[LeaseSets](#struct_LeaseSet) are sent
to floodfill routers in a [Database Store
Message](#msg_DatabaseStore) wrapped in a
[Garlic Message](#msg_Garlic) so it is not
visible to the tunnel\'s outbound gateway.

## Trabalho futuro

The Garlic Message mechanism is very flexible and provides a structure
for implementing many types of mixnet delivery methods. Together with
the unused delay option in the [tunnel message Delivery
Instructions](#struct_TunnelMessageDeliveryInstructions),
a wide spectrum of batching, delay, mixing, and routing strategies are
possible.

Em particular, há potencial para muito mais flexibilidade no ponto final
do túnel de saída. As mensagens poderiam ser roteadas de lá para um dos
vários túneis (minimizando assim as conexões ponto a ponto), ou
multicast para vários túneis para redundância, ou streaming de áudio e
vídeo.

Tais experimentos podem entrar em conflito com a necessidade de garantir
segurança e anonimato, como limitar certos caminhos de roteamento,
restringir os tipos de mensagens I2NP que podem ser encaminhadas por
vários caminhos e impor certos tempos de expiração de mensagens.

As a part of [ElGamal/AES encryption](), a
garlic message contains a sender specified amount of padding data,
allowing the sender to take active countermeasures against traffic
analysis. This is not currently used, beyond the requirement to pad to a
multiple of 16 bytes.

Encryption of additional messages to and from the [floodfill
routers](#delivery).

## Referências

- O termo roteamento de alho foi cunhado pela primeira vez na tese de
 mestrado de Roger Dingledine, Free Haven
 [](http://www.freehaven.net/papers.html) (junho de 2000), veja Seção
 8.1.1 de autoria de [Michael J.
 Freedman](http://www.cs.princeton.edu/~mfreed/).
- [Publicações em
 onion-router.net](http://www.onion-router.net/Publications.html)
- [Roteamento Cebola na
 Wikipédia](http://en.wikipedia.org/wiki/Onion_routing)
- [Roteamento Alho na
 Wikipédia](http://en.wikipedia.org/wiki/Garlic_routing)
- [I2P Meeting 58]() (2003) discussing the
 implementation of garlic routing
- [Tor](https://www.torproject.org/)
- [Publicações em
 freehaven.net](http://freehaven.net/anonbib/topic.html)
- O roteamento onion foi descrito pela primeira vez em [Ocultando
 informações de
 roteamento](http://www.onion-router.net/Publications/IH-1996.pdf)
 por David M. Goldschlag, Michael G. Reed e Paul F. Syverson em 1996.


