 O Banco de Dados
da Rede 2025-03 0.9.65 

## Sinopse

O netDb do I2P é um banco de dados distribuído especializado, contendo
apenas dois tipos de dados - informações de contato do roteador
(**RouterInfos**) e informações de contato de destino (**LeaseSets**).
Cada pedaço de dados é assinado pela parte apropriada e verificado por
qualquer um que o use ou armazene. Além disso, os dados têm informações
de vivacidade dentro deles, permitindo que entradas irrelevantes sejam
descartadas, entradas mais novas substituam as mais antigas e proteção
contra certas classes de ataque.

O netDb é distribuído com uma técnica simples chamada \"floodfill\",
onde um subconjunto de todos os roteadores, chamados \"roteadores
floodfill\", mantém o banco de dados distribuído.

## RouterInfo {#routerInfo}

Quando um roteador I2P quer contatar outro roteador, ele precisa saber
algumas peças-chave de dados - todas as quais são agrupadas e assinadas
pelo roteador em uma estrutura chamada \"RouterInfo\", que é distribuída
com o SHA256 da identidade do roteador como a chave. A estrutura em si
contém:

- A identidade do roteador (uma chave de criptografia, uma chave de
 assinatura e um certificado)
- Os endereços de contato onde pode ser contatado
- Quando isso foi publicado
- Um conjunto de opções de texto arbitrárias
- A assinatura do acima, gerada pela chave de assinatura da identidade

### Opções esperadas

As seguintes opções de texto, embora não sejam estritamente necessárias,
são esperadas estarem presentes:

**caps** (Sinalizadores de capacidades - usados para indicar
participação de floodfill, largura de banda aproximada e acessibilidade
percebida)

**D**: Medium congestion (as of release 0.9.58)

**E**: High congestion (as of release 0.9.58)

**f**: Enchimento

**G**: Rejecting all tunnels (as of release 0.9.58)

**H**: Oculto

**K**: Esses valores são usados por outros roteadores para decisões
básicas. Devemos nos conectar a este roteador? Devemos tentar rotear um
túnel através deste roteador? O sinalizador de capacidade de largura de
banda, em particular, é usado apenas para determinar se o roteador
atende a um limite mínimo para túneis de roteamento. Acima do limite
mínimo, a largura de banda anunciada não é usada ou confiável em nenhum
lugar no roteador, exceto para exibição na interface do usuário e para
depuração e análise de rede.

Valid NetID numbers:

Usage

NetID Number

Reserved

0

Reserved

1

Current Network (default)

2

Reserved Future Networks

3 - 15

Forks and Test Networks

16 - 254

Reserved

255

### Opções adicionais

Additional text options include a small number of statistics about the
router\'s health, which are aggregated by sites such as [](http:///) for network performance analysis
and debugging. These statistics were chosen to provide data crucial to
the developers, such as tunnel build success rates, while balancing the
need for such data with the side-effects that could result from
revealing this data. Current statistics are limited to:

- Taxas de sucesso, rejeição e tempo limite de construção de túnel
 exploratório
- Média de 1 hora de túneis participantes

These are optional, but if included, help analysis of network-wide
performance. As of API 0.9.58, these statistics are simplified and
standardized, as follows:

- Option keys are stat\_(statname).(statperiod)
- Option values are \';\' -separated
- Stats for event counts or normalized percentages use the 4th value;
 the first three values are unused but must be present
- Stats for average values use the 1st value, and no \';\' separator
 is required
- For equal weighting of all routers in stats analysis, and for
 additional anonymity, routers should include these stats only after
 an uptime of one hour or more, and only one time every 16 times that
 the RI is published.

Example:

 stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
 stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
 stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
 stat_tunnel.participatingTunnels.60m = 289.20

Floodfill routers may publish additional data on the number of entries
in their network database. These are optional, but if included, help
analysis of network-wide performance.

The following two options should be included by floodfill routers in
every published RI:

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

Example:

 netdb.knownLeaseSets = 158
 netdb.knownRouters = 11374

The data published can be seen in the router\'s user interface, but is
not used or trusted by any other router.

### Opções de família

A partir da versão 0.9.24, os roteadores podem declarar que fazem parte
de uma \"família\", operada pela mesma entidade. Vários roteadores na
mesma família não serão usados em um único túnel.

As opções familiares são:

- **family** (O sobrenome)
- **family.key** The signature type code of the family\'s [Signing
 Public
 Key](#type_SigningPublicKey)
 (in ASCII digits) concatenated with \':\' concatenated with the
 Signing Public Key in base 64
- **family.sig** The signature of ((family name in UTF-8) concatenated
 with (32 byte router hash)) in base 64

### Expiração do RouterInfo

O RouterInfos não tem um tempo de expiração definido. Cada roteador é
livre para manter sua própria política local para compensar a frequência
de pesquisas do RouterInfo com o uso de memória ou disco. Na
implementação atual, existem as seguintes políticas gerais:

- Não há expiração durante a primeira hora de atividade, pois os dados
 armazenados persistentemente podem ser antigos.
- Não há expiração se houver 25 ou menos RouterInfos.
- Conforme o número de RouterInfos locais cresce, o tempo de expiração
 diminui, em uma tentativa de manter um número razoável de
 RouterInfos. O tempo de expiração com menos de 120 roteadores é de
 72 horas, enquanto o tempo de expiração com 300 roteadores é de
 cerca de 30 horas.
- RouterInfos containing [SSU]() introducers
 expire in about an hour, as the introducer list expires in about
 that time.
- Os floodfills usam um tempo de expiração curto (1 hora) para todos
 os RouterInfos locais, pois os RouterInfos válidos serão
 frequentemente republicados neles.

### Armazenamento persistente RouterInfo

Os RouterInfos são gravados periodicamente no disco para que fiquem
disponíveis após uma reinicialização.

Pode ser desejável armazenar persistentemente Meta LeaseSets com
expirações longas. Isso depende da implementação.

### Ver também

[Especificação
RouterInfo](#struct_RouterInfo)

[Javadoc do
RouterInfo](http:///net/i2p/data/router/RouterInfo.html)

## LeaseSet {#leaseSet}

O segundo pedaço de dados distribuído no netDb é um \"LeaseSet\" -
documentando um grupo de **pontos de entrada de túnel (leases)** para um
destino de cliente específico. Cada um desses leases especifica as
seguintes informações:

- O roteador do gateway do túnel (especificando sua identidade)
- O ID do túnel naquele roteador para enviar mensagens com (um número
 de 4 bytes)
- Quando esse túnel irá expirar.

O próprio LeaseSet é armazenado no netDb em a chave derivada do SHA256
do destino. Uma exceção é para Encrypted LeaseSets (LS2), a partir da
versão 0.9.38. O SHA256 do tipo byte (3) seguido pela chave pública cega
é usado para a chave DHT, e então rotacionado como de costume. Veja a
seção Métrica de Proximidade do Kademlia abaixo.

Além desses arrendamentos, o LeaseSet inclui:

- O destino em si (uma chave de criptografia, uma chave de assinatura
 e um certificado)
- Chave pública de criptografia adicional: usada para criptografia de
 ponta a ponta de mensagens de alho
- Chave pública de assinatura adicional: destinada à revogação do
 LeaseSet, mas não é utilizada no momento.
- Assinatura de todos os dados do LeaseSet, para garantir que o
 Destino publicou o LeaseSet.

[Especificação de
arrendamento](#struct_Lease)\
[Especificação
LeaseSet](#struct_LeaseSet)

[Arrendamento
Javadoc](http:///net/i2p/data/Lease.html)\
[LeaseSet
Javadoc](http:///net/i2p/data/LeaseSet.html)

A partir da versão 0.9.38, três novos tipos de LeaseSets são definidos;
LeaseSet2, MetaLeaseSet e EncryptedLeaseSet. Veja abaixo.

### LeaseSets não publicados {#unpublished}

Um LeaseSet para um destino usado apenas para conexões de saída é *não
publicado*. Ele nunca é enviado para publicação em um roteador
floodfill. Túneis \"clientes\", como aqueles para navegação na web e
clientes IRC, não são publicados. Os servidores ainda poderão enviar
mensagens de volta para esses destinos não publicados, por causa das
[mensagens de armazenamento I2NP](#lsp).

### Conjuntos de arrendamento revogados {#revoked}

Um LeaseSet pode ser *revogado* publicando um novo LeaseSet com zero
leases. As revogações devem ser assinadas pela chave de assinatura
adicional no LeaseSet. As revogações não são totalmente implementadas e
não está claro se elas têm algum uso prático. Este é o único uso
planejado para essa chave de assinatura, então ela não é usada no
momento.

### LeaseSet2 (LS2) {#ls2}

A partir da versão 0.9.38, os floodfills oferecem suporte a uma nova
estrutura LeaseSet2. Essa estrutura é muito semelhante à antiga
estrutura LeaseSet e atende ao mesmo propósito. A nova estrutura fornece
a flexibilidade necessária para oferecer suporte a novos tipos de
criptografia, vários tipos de criptografia, opções, chaves de assinatura
offline, e outros recursos. Consulte a proposta 123 para obter detalhes.

### Meta LeaseSet (LS2) {#meta}

A partir da versão 0.9.38, os floodfills suportam uma nova estrutura
Meta LeaseSet. Esta estrutura fornece uma estrutura semelhante a uma
árvore no DHT, para se referir a outros LeaseSets. Usando Meta
LeaseSets, um site pode implementar grandes serviços multihomed, onde
vários Destinos diferentes são usados para fornecer um serviço comum. As
entradas em um Meta LeaseSet são Destinos ou outros Meta LeaseSets, e
podem ter expirações longas, de até 18,2 horas. Usando este recurso,
deve ser possível executar centenas ou milhares de Destinos hospedando
um serviço comum. Veja a proposta 123 para detalhes.

### LeaseSets criptografados (LS1) {#encrypted}

Esta seção descreve o método antigo e inseguro de criptografar LeaseSets
usando uma chave simétrica fixa. Veja abaixo a versão LS2 de LeaseSets
criptografados.

Em um *LeaseSet criptografado* , todos os Leases são criptografados com
uma chave separada. Os leases só podem ser decodificados e, portanto, o
destino só pode ser contatado, por aqueles com a chave. Não há nenhum
sinalizador ou outra indicação direta de que o LeaseSet está
criptografado. LeaseSets criptografados não são amplamente utilizados, e
é um tópico para trabalho futuro pesquisar se a interface do usuário e a
implementação de LeaseSets criptografados podem ser melhoradas.

### LeaseSets criptografados (LS2) {#encrypted2}

A partir da versão 0.9.38, os floodfills oferecem suporte a uma nova
estrutura EncryptedLeaseSet. O destino fica oculto, e apenas uma chave
pública oculta e uma expiração são visíveis para o floodfill. Somente
aqueles que têm o destino completo podem descriptografar a estrutura. A
estrutura é armazenada em um local DHT com base no hash da chave pública
oculta, não no hash do destino. Veja a proposta 123 para obter detalhes.

### Vencimento do LeaseSet

Para LeaseSets regulares, a expiração é o momento da última expiração de
seus leases. Para as novas estruturas de dados LeaseSet2, a expiração é
especificada no cabeçalho. Para LeaseSet2, a expiração deve corresponder
à última expiração de seus leases. Para EncryptedLeaseSet e
MetaLeaseSet, a expiração pode variar, e a expiração máxima pode ser
imposta, a ser determinada.

### Armazenamento persistente LeaseSet

Não é necessário armazenamento persistente de dados do LeaseSet, pois
eles expiram muito rapidamente. No entanto, o armazenamento persistente
de dados do EncryptedLeaseSet e do MetaLeaseSet com expirações longas
pode ser aconselhável.

### Seleção de chave de criptografia (LS2) {#ls2keys}

LeaseSet2 pode conter várias chaves de criptografia. As chaves estão em
ordem de preferência do servidor, a mais preferida primeiro. O
comportamento padrão do cliente é selecionar a primeira chave com um
tipo de criptografia suportado. Os clientes podem usar outros algoritmos
de seleção com base no suporte à criptografia, desempenho relativo e
outros fatores.

## Inicialização {#bootstrap}

O netDb é descentralizado, no entanto, você precisa de pelo menos uma
referência a um peer para que o processo de integração o vincule. Isso é
feito \"reseeding\" seu roteador com o RouterInfo de um peer ativo -
especificamente, recuperando seu arquivo `routerInfo-$hash.dat` e
armazenando-o em seu diretório `netDb/` . Qualquer um pode fornecer
esses arquivos a você - você pode até mesmo fornecê-los a outros expondo
seu próprio diretório netDb. Para simplificar o processo, voluntários
publicam seus diretórios netDb (ou um subconjunto) na rede regular (não
i2p), e as URLs desses diretórios são codificadas em I2P. Quando o
roteador é inicializado pela primeira vez, ele busca automaticamente em
uma dessas URLs, selecionada aleatoriamente.

## Enchimento {#floodfill}

O floodfill netDb é um mecanismo simples de armazenamento distribuído. O
algoritmo de armazenamento é simples: envie os dados para o peer mais
próximo que anunciou a si mesmo como um roteador floodfill. Quando o
peer no floodfill netDb recebe um netDb store de um peer que não está no
floodfill netDb, ele o envia para um subconjunto de os floodfill
netDb-peers. Os peers selecionados são os mais próximos (de acordo com a
[métrica XOR](#kad)) de uma chave específica.

Determinar quem faz parte do floodfill netDb é trivial - ele é exposto
em cada routerInfo publicado do roteador como um recurso.

Os floodfills não têm autoridade central e não formam um \"consenso\" -
eles apenas implementam uma sobreposição DHT simples.

### Opt-in do roteador Floodfill {#opt-in}

Ao contrário do Tor, onde os servidores de diretório são codificados e
confiáveis, e operados por entidades conhecidas, os membros do conjunto
de pares de floodfill I2P não precisam ser confiáveis, e mudam ao longo
do tempo.

Para aumentar a confiabilidade do netDb e minimizar o impacto do tráfego
netDb em um roteador, o floodfill é habilitado automaticamente somente
em roteadores configurados com altos limites de largura de banda.
Roteadores com altos limites de largura de banda (que devem ser
configurados manualmente, já que o padrão é muito menor) são presumidos
como estando em conexões de latência mais baixa e têm mais probabilidade
de estar disponíveis 24 horas por dia, 7 dias por semana. A largura de
banda mínima de compartilhamento atual para um roteador floodfill é de
128 KBytes/seg.

Além disso, um roteador deve passar por vários testes adicionais de
integridade (tempo de fila de mensagens de saída, atraso de trabalho,
etc.) antes que a operação de floodfill seja habilitada automaticamente.

Com as regras atuais para opt-in automático, aproximadamente 6% de
roteadores na rede são roteadores floodfill.

Enquanto alguns pares são configurados manualmente para serem floodfill,
outros são simplesmente roteadores de alta largura de banda que
automaticamente voluntariam quando o número de pares floodfill cai
abaixo de um limite. Isso evita qualquer dano de rede de longo prazo,
perdendo a maioria ou todos os floodfills para um ataque. Por sua vez,
esses pares deixarão de fazer o floodfill quando houver muitos
floodfills pendentes.

### Funções do roteador Floodfill

Os únicos serviços de um roteador floodfill que são adicionais aos de
roteadores não floodfill são aceitar armazenamentos netDb e responder a
consultas netDb. Como eles geralmente têm alta largura de banda, é mais
provável que participem de um grande número de túneis (ou seja, sejam um
\"retransmissor\" para outros), mas isso não está diretamente
relacionado aos seus serviços de banco de dados distribuídos.

## Métrica de proximidade Kademlia {#kad}

O netDb usa uma métrica XOR simples no estilo Kademlia para determinar a
proximidade. Para criar uma chave Kademlia, o hash SHA256 do
RouterIdentity ou Destination é calculado. Uma exceção é para Encrypted
LeaseSets (LS2), a partir da versão 0.9.38. O SHA256 do tipo byte (3)
seguido pela chave pública cega é usado para a chave DHT, e então
rotacionado como de costume.

Uma modificação neste algoritmo é feita para aumentar os custos de
[ataques Sybil](#sybil-partial). Em vez do hash SHA256 da chave sendo
pesquisada ou armazenada, o hash SHA256 é obtido da chave de pesquisa
binária de 32 bytes anexada com a data UTC representada como uma string
ASCII de 8 bytes aaaaMMdd, ou seja, SHA256(chave + aaaaMMdd). Isso é
chamado de \"chave de roteamento\" e muda todos os dias à meia-noite
UTC. Somente a chave de pesquisa é modificada dessa forma, não os hashes
do roteador de inundação. A transformação diária do DHT às vezes é
chamada de \"rotação do espaço de chaves\", embora não seja estritamente
uma rotação.

Chaves de roteamento nunca são enviadas na rede em nenhuma mensagem
I2NP, elas são usadas apenas localmente para determinação de distância .

## Network Database Segmentation - Sub-Databases {#segmentation}

Traditionally Kademlia-style DHT\'s are not concerned with preserving
the unlinkability of information stored on any particular node in the
DHT. For example, a piece of information may be stored to one node in
the DHT, then requested back from that node unconditionally. Within I2P
and using the netDb, this is not the case, information stored in the DHT
may only be shared under certain known circumstances where it is
\"safe\" to do so. This is to prevent a class of attacks where a
malicious actor can try to associate a client tunnel with a router by
sending a store to a client tunnel, then requesting it back directly
from the suspected \"Host\" of the client tunnel.

### Segmentation Structure

I2P routers can implement effective defenses against the attack class
provided a few conditions are met. A network database implementation
should be able to keep track of whether a database entry was recieved
down a client tunnel or directly. If it was recieved down a client
tunnel, then it should also keep track of which client tunnel it was
recieved through, using the client\'s local destination. If the entry
was recieved down multiple client tunnels, then the netDb should keep
track of all destinations where the entry was observed. It should also
keep track of whether an entry was recieved as a reply to a lookup, or
as a store.

In both the Java and C++ implementations, this achieved by using a
single \"Main\" netDb for direct lookups and floodfill operations first.
This main netDb exists in the router context. Then, each client is given
it\'s own version of the netDb, which is used to capture database
entries sent to client tunnels and respond to lookups sent down client
tunnels. We call these \"Client Network Databases\" or \"Sub-Databases\"
and they exist in the client context. The netDb operated by the client
exists for the lifetime of the client only and contains only entries
that are communicated with the client\'s tunnels. This makes it
impossible for entries sent down client tunnels to overlap with entries
sent directly to the router.

Additionally, each netDb needs to be able to remember if a database
entry was recieved because it was sent to one of our destinations, or
because it was requested by us as part of a lookup. If a database entry
it was recieved as a store, as in some other router sent it to us, then
a netDb should respond to requests for the entry when another router
looks up the key. However, if it was recieved as a reply to a query,
then the netDb should only reply to a query for the entry if the entry
had already been stored to the same destination. A client should never
answer queries with an entry from the main netDb, only it\'s own client
network database.

These strategies should be taken and used combined so that both are
applied. In combination, they \"Segment\" the netDb and secure it
against attacks.

## Mecânica de armazenamento, verificação e pesquisa {#delivery}

### Armazenamento RouterInfo para pares

[I2NP]() DatabaseStoreMessages containing the
local RouterInfo are exchanged with peers as a part of the
initialization of a [NTCP]() or
[SSU]() transport connection.

### Armazenamento LeaseSet para pares {#lsp}

[I2NP]() DatabaseStoreMessages containing the
local LeaseSet are periodically exchanged with peers by bundling them in
a garlic message along with normal traffic from the related Destination.
This allows an initial response, and later responses, to be sent to an
appropriate Lease, without requiring any LeaseSet lookups, or requiring
the communicating Destinations to have published LeaseSets at all.

### Floodfill Selection

O DatabaseStoreMessage deve ser enviado para o floodfill mais próximo da
chave de roteamento atual para o RouterInfo ou LeaseSet que está sendo
armazenado. Atualmente, o floodfill mais próximo é encontrado por uma
pesquisa no banco de dados local. Mesmo que esse floodfill não esteja
realmente mais próximo, ele o inundará \"mais perto\" enviando-o para
vários outros floodfills. Isso fornece um alto grau de tolerância a
falhas.

No Kademlia tradicional, um peer faria uma busca \"find-closest\" antes
de inserir um item no DHT para o alvo mais próximo. Como a operação de
verificação tenderá a descobrir floodfills mais próximos se eles
estiverem presentes, um roteador melhorará rapidamente seu conhecimento
da \"vizinhança\" do DHT para o RouterInfo e LeaseSets que ele publica
regularmente. Embora o I2NP não defina uma mensagem \"find-closest\", se
for necessário, um roteador pode simplesmente fazer uma busca iterativa
por uma chave com o bit menos significativo invertido (ou seja, chave \^
0x01) até que nenhum peer mais próximo seja recebido no
DatabaseSearchReplyMessages. Isso garante que o verdadeiro par mais
próximo será encontrado mesmo que um par mais distante tenha o item
netdb.

### Armazenamento RouterInfo para Floodfills

A router publishes its own RouterInfo by directly connecting to a
floodfill router and sending it a [I2NP]()
DatabaseStoreMessage with a nonzero Reply Token. The message is not
end-to-end garlic encrypted, as this is a direct connection, so there
are no intervening routers (and no need to hide this data anyway). The
floodfill router replies with a [I2NP]()
DeliveryStatusMessage, with the Message ID set to the value of the Reply
Token.

In some circumstances, a router may also send the RouterInfo
DatabaseStoreMessage out an exploratory tunnel; for example, due to
connection limits, connection incompatibility, or a desire to hide the
actual IP from the floodfill. The floodfill may not accept such a store
in times of overload or based on other criteria; whether to explicitly
declare non-direct store of a RouterInfo illegal is a topic for further
study.

### Armazenamento LeaseSet para Floodfills

O armazenamento de LeaseSets é muito mais sensível do que para
RouterInfos, pois um roteador deve tomar cuidado para que o LeaseSet não
possa ser associado ao roteador.

A router publishes a local LeaseSet by sending a
[I2NP]() DatabaseStoreMessage with a nonzero Reply
Token over an outbound client tunnel for that Destination. The message
is end-to-end garlic encrypted using the Destination\'s Session Key
Manager, to hide the message from the tunnel\'s outbound endpoint. The
floodfill router replies with a [I2NP]()
DeliveryStatusMessage, with the Message ID set to the value of the Reply
Token. This message is sent back to one of the client\'s inbound
tunnels.

### Inundação

Like any router, a floodfill uses various criteria to validate the
LeaseSet or RouterInfo before storing it locally. These criteria may be
adaptive and dependent on current conditions including current load,
netdb size, and other factors. All validation must be done before
flooding.

After a floodfill router receives a DatabaseStoreMessage containing a
valid RouterInfo or LeaseSet which is newer than that previously stored
in its local NetDb, it \"floods\" it. To flood a NetDb entry, it looks
up several (currently ) floodfill routers closest to the
routing key of the NetDb entry. (The routing key is the SHA256 Hash of
the RouterIdentity or Destination with the date (yyyyMMdd) appended.) By
flooding to those closest to the key, not closest to itself, the
floodfill ensures that the storage gets to the right place, even if the
storing router did not have good knowledge of the DHT \"neighborhood\"
for the routing key.

The floodfill then directly connects to each of those peers and sends it
a [I2NP]() DatabaseStoreMessage with a zero Reply
Token. The message is not end-to-end garlic encrypted, as this is a
direct connection, so there are no intervening routers (and no need to
hide this data anyway). The other routers do not reply or re-flood, as
the Reply Token is zero.

Floodfills must not flood via tunnels; the DatabaseStoreMessage must be
sent over a direct connection.

Floodfills must never flood an expired LeaseSet or a RouterInfo
published more than one hour ago.

### Pesquisa RouterInfo e LeaseSet {#lookup}

The [I2NP]() DatabaseLookupMessage is used to
request a netdb entry from a floodfill router. Lookups are sent out one
of the router\'s outbound exploratory tunnels. The replies are specified
to return via one of the router\'s inbound exploratory tunnels.

As pesquisas geralmente são enviadas para os dois roteadores floodfill
\"bons\" (a conexão não falha) mais próximos da chave solicitada, em
paralelo.

If the key is found locally by the floodfill router, it responds with a
[I2NP]() DatabaseStoreMessage. If the key is not
found locally by the floodfill router, it responds with a
[I2NP]() DatabaseSearchReplyMessage containing a
list of other floodfill routers close to the key.

As pesquisas do LeaseSet são criptografadas com garlic de ponta a ponta
a partir da versão 0.9.5. As pesquisas do RouterInfo não são
criptografadas e, portanto, são vulneráveis à espionagem pelo ponto de
extremidade de saída (OBEP) do túnel do cliente. Isso se deve ao custo
da criptografia ElGamal. A criptografia de pesquisa do RouterInfo pode
ser habilitada em uma versão futura.

A partir da versão 0.9.7, as respostas a uma pesquisa LeaseSet (uma
DatabaseStoreMessage ou uma DatabaseSearchReplyMessage) serão
criptografadas incluindo a chave de sessão e a tag na pesquisa. Isso
oculta a resposta do gateway de entrada (IBGW) do túnel de resposta. As
respostas às pesquisas RouterInfo serão criptografadas se habilitarmos a
criptografia de pesquisa.

(Reference: [Hashing it out in Public]() Sections
2.2-2.3 for terms below in italics)

Devido ao tamanho relativamente pequeno da rede e à redundância de
inundação, as pesquisas são geralmente O(1) em vez de O(log n). É
altamente provável que um roteador conheça um roteador de inundação
próximo o suficiente da chave para obter a resposta na primeira
tentativa. Em versões anteriores à 0.8.9, os roteadores usavam uma
redundância de pesquisa de dois (ou seja, duas pesquisas eram realizadas
em paralelo para pares diferentes) e nem *recursivo* nem *iterativo* o
roteamento para pesquisas foi implementado. As consultas foram enviadas
por *várias rotas simultaneamente* para *reduzir a chance de falha da
consulta*.

A partir da versão 0.8.9, *pesquisas iterativas* são implementadas sem
redundância de pesquisa. Esta é uma pesquisa mais eficiente e confiável
que funcionará muito melhor quando nem todos os pares de floodfill forem
conhecidos, e remove uma séria limitação ao crescimento da rede. À
medida que a rede cresce e cada roteador conhece apenas um pequeno
subconjunto dos pares de floodfill, as pesquisas se tornarão O(log n).
Mesmo que o par não retorne referências mais próximas da chave, a
pesquisa continua com o próximo par mais próximo, para maior robustez e
para evitar que um floodfill malicioso faça um black-hole em uma parte
do espaço da chave. As pesquisas continuam até que o tempo limite total
de pesquisa seja atingido, ou o número máximo de pares seja consultado.

*IDs de nó* são *verificáveis* porque usamos o hash do roteador
diretamente como ID de nó e chave Kademlia. Respostas incorretas que não
estão mais próximas da chave de pesquisa são geralmente ignoradas. Dado
o tamanho atual da rede, um roteador tem *conhecimento detalhado da
vizinhança do espaço de ID de destino*.

### Verificação de armazenamento RouterInfo

Note: RouterInfo verification is disabled as of release 0.9.7.1 to
prevent the attack described in the paper [Practical Attacks Against the
I2P Network](). It is not clear if
verification can be redesigned to be done safely.

Para verificar se um armazenamento foi bem-sucedido, um roteador
simplesmente espera cerca de 10 segundos, e então envia uma pesquisa
para outro roteador de floodfill próximo à chave (mas não para aquele
para o qual o armazenamento foi enviado). As pesquisas são enviadas para
um dos túneis exploratórios de saída do roteador. As pesquisas são
criptografadas de ponta a ponta para evitar espionagem pelo ponto de
extremidade de saída (OBEP).

### Verificação de armazenamento LeaseSet

Para verificar se um armazenamento foi bem-sucedido, um roteador
simplesmente espera cerca de 10 segundos, então envia uma consulta para
outro roteador de floodfill próximo à chave (mas não aquela para a qual
o armazenamento foi enviado). As consultas enviam um dos túneis de saída
do cliente para o destino do LeaseSet que está sendo verificado. Para
evitar espionagem pelo OBEP do túnel de saída, as consultas são
criptografadas de ponta a ponta. As respostas são especificadas para
retornar por meio de um dos túneis de entrada do cliente.

A partir da versão 0.9.7, as respostas para pesquisas RouterInfo e
LeaseSet (uma DatabaseStoreMessage ou uma DatabaseSearchReplyMessage)
serão criptografadas, para ocultar a resposta do gateway de entrada
(IBGW) do túnel de resposta.

### Exploração

*Exploration* is a special form of netdb lookup, where a router attempts
to learn about new routers. It does this by sending a floodfill router a
[I2NP]() DatabaseLookup Message, looking for a
random key. As this lookup will fail, the floodfill would normally
respond with a [I2NP]() DatabaseSearchReplyMessage
containing hashes of floodfill routers close to the key. This would not
be helpful, as the requesting router probably already knows those
floodfills, and it would be impractical to add all floodfill routers to
the \"don\'t include\" field of the DatabaseLookup Message. For an
exploration query, the requesting router sets a special flag in the
DatabaseLookup Message. The floodfill will then respond only with
non-floodfill routers close to the requested key.

### Notas sobre respostas de pesquisa

A resposta a uma solicitação de pesquisa é uma Database Store Message
(em caso de sucesso) ou uma Database Search Reply Message (em caso de
falha). O DSRM contém um campo hash do roteador \'from\' para indicar a
origem da resposta; o DSM não. O campo \'from\' do DSRM não é
autenticado e pode ser falsificado ou inválido. Não há outras tags de
resposta. Portanto, ao fazer várias solicitações em paralelo, é difícil
monitorar o desempenho dos vários roteadores floodfill.

## MultiHoming {#multihome}

Os destinos podem ser hospedados em vários roteadores simultaneamente,
usando as mesmas chaves privadas e públicas (tradicionalmente
armazenadas em arquivos eepPriv.dat). Como ambas as instâncias
publicarão periodicamente seus LeaseSets assinados para os pares de
floodfill, o LeaseSet publicado mais recentemente será retornado a um
par que solicitou uma consulta ao banco de dados. Como os LeaseSets têm
(no máximo) uma vida útil de 10 minutos, se uma instância específica
cair, a interrupção será de 10 minutos no máximo, e geralmente muito
menos que isso. A função multihoming foi verificada e está em uso por
vários serviços na rede.

A partir da versão 0.9.38, os floodfills suportam uma nova estrutura
Meta LeaseSet. Esta estrutura fornece uma estrutura semelhante a uma
árvore no DHT, para se referir a outros LeaseSets. Usando Meta
LeaseSets, um site pode implementar grandes serviços multihomed, onde
vários Destinos diferentes são usados para fornecer um serviço comum. As
entradas em um Meta LeaseSet são Destinos ou outros Meta LeaseSets, e
podem ter expirações longas, de até 18,2 horas. Usando este recurso,
deve ser possível executar centenas ou milhares de Destinos hospedando
um serviço comum. Veja a proposta 123 para detalhes.

## Análise de ameaças {#threat}

Also discussed on [the threat model
page](#floodfill).

Um usuário hostil pode tentar prejudicar a rede criando um ou mais
roteadores de floodfill e adaptando-os para oferecer respostas ruins,
lentas ou nenhuma resposta. Alguns cenários são discutidos abaixo.

### Mitigação Geral Através do Crescimento

There are currently around floodfill routers in the
network. Most of the following attacks will become more difficult, or
have less impact, as the network size and number of floodfill routers
increase.

### Mitigação geral por meio de redundância

Via flooding, all netdb entries are stored on the 
floodfill routers closest to the key.

### Falsificações

Todas as entradas netdb são assinadas por seus criadores, portanto
nenhum roteador pode falsificar um RouterInfo ou LeaseSet.

### Lento ou sem resposta

Each router maintains an expanded set of statistics in the [peer
profile]() for each floodfill router,
covering various quality metrics for that peer. The set includes:

- Tempo médio de resposta
- Porcentagem de consultas respondidas com os dados solicitados
- Porcentagem de lojas que foram verificadas com sucesso
- Última loja de sucesso
- Última pesquisa bem-sucedida
- Última resposta

Cada vez que um roteador precisa determinar qual roteador de floodfill
está mais próximo de uma chave, ele usa essas métricas para determinar
quais roteadores de floodfill são \"bons\". Os métodos e limites usados
para determinar a \"bondade\" são relativamente novos, e estão sujeitos
a análises e melhorias adicionais. Enquanto um roteador completamente
sem resposta será rapidamente identificado e evitado, roteadores que são
apenas algumas vezes maliciosos podem ser muito mais difíceis de lidar.

### Ataque Sybil (Keyspace Completo) {#sybil}

An attacker may mount a [Sybil attack]() by
creating a large number of floodfill routers spread throughout the
keyspace.

(In a related example, a researcher recently created a [large number of
Tor relays]().) If successful, this could be an
effective DOS attack on the entire network.

Se os floodfills não estiverem se comportando mal o suficiente para
serem marcados como \"ruins\" usando as métricas de perfil de pares
descritas acima, este é um cenário difícil de lidar. A resposta do Tor
pode ser muito mais ágil no caso de retransmissão, pois os
retransmissores suspeitos podem ser removidos manualmente do consenso.
Algumas respostas possíveis para a rede I2P estão listadas abaixo, no
entanto, nenhuma delas é completamente satisfatória:

- Compile uma lista de hashes ou IPs de roteadores ruins e anuncie a
 lista por vários meios (notícias do console, site, fórum, etc.); os
 usuários teriam que baixar manualmente a lista e adicioná-la à sua
 \"lista negra\" local.
- Peça a todos na rede para habilitar o floodfill manualmente (lute
 contra Sybil com mais Sybil)
- Lançar uma nova versão de software que inclua a lista \"ruim\"
 codificada
- Lançar uma nova versão de software que melhora as métricas e limites
 do perfil dos pares, , em uma tentativa de identificar
 automaticamente os pares \"ruins\".
- Adicione software que desqualifique floodfills se muitos deles
 estiverem em um único bloco de IP
- Implementar uma lista negra automática baseada em assinatura
 controlada por um único indivíduo ou grupo. Isso implementaria
 essencialmente uma parte do modelo de \"consenso\" do Tor.
 Infelizmente, isso também daria a um único indivíduo ou grupo o
 poder de bloquear a participação de qualquer roteador ou IP
 específico na rede, ou até mesmo desligar ou destruir completamente
 a rede inteira.

Esse ataque se torna mais difícil à medida que o tamanho da rede
aumenta.

### Ataque Sybil (Keyspace Parcial) {#sybil-partial}

An attacker may mount a [Sybil attack]() by
creating a small number (8-15) of floodfill routers clustered closely in
the keyspace, and distribute the RouterInfos for these routers widely.
Then, all lookups and stores for a key in that keyspace would be
directed to one of the attacker\'s routers. If successful, this could be
an effective DOS attack on a particular I2P Site, for example.

Como o keyspace é indexado pelo hash criptográfico (SHA256) da chave, um
invasor deve usar um método de força bruta para gerar repetidamente
hashes de roteador até que ele tenha o suficiente que esteja
suficientemente próximo da chave. A quantidade de poder computacional
necessária para isso, que depende do tamanho da rede , é desconhecida.

Como uma defesa parcial contra esse ataque, o algoritmo usado para
determinar a \"proximidade\" do Kademlia varia ao longo do tempo. Em vez
de usar o Hash da chave (ou seja, H(k)) para determinar a proximidade,
usamos o Hash da chave anexado com a sequência de data atual, ou seja,
H(k + AAAAMMDD). Uma função chamada \"gerador de chave de roteamento\"
faz isso, o que transforma a chave original em uma \"chave de
roteamento\". Em outras palavras, todo o keyspace netdb \"gira\" todos
os dias à meia-noite UTC. Qualquer ataque de keyspace parcial teria que
ser regenerado todos os dias, pois após a rotação, os roteadores
atacantes não estariam mais próximos da chave alvo ou entre si.

Esse ataque se torna mais difícil à medida que o tamanho da rede
aumenta. No entanto, pesquisas recentes demonstram que a rotação do
espaço de chaves não é particularmente eficaz. Um invasor pode
pré-computar vários hashes de roteador com antecedência, e apenas alguns
roteadores são suficientes para \"eclipsar\" uma parte do espaço de
chaves em meia hora após a rotação.

Uma consequência da rotação diária do espaço de chaves é que o banco de
dados de rede distribuído pode se tornar não confiável por alguns
minutos após a rotação \-- as pesquisas falharão porque o novo roteador
\"mais próximo\" ainda não recebeu um armazenamento. A extensão do
problema e os métodos de mitigação (por exemplo, \"transferências\" do
netdb à meia-noite) são um tópico para estudo posterior.

### Ataques Bootstrap

Um invasor pode tentar inicializar novos roteadores em uma rede isolada
ou controlada pela maioria, assumindo o controle de um site de reseed,
ou enganando os desenvolvedores para adicionar seu site de reseed à
lista codificada no roteador.

Várias defesas são possíveis, e a maioria delas são planejadas:

- Não permitir fallback de HTTPS para HTTP para repropagação. Um
 invasor MITM poderia simplesmente bloquear o HTTPS e então responder
 ao HTTP.
- Agrupando dados de reseed no instalador

Defesas que são implementadas:

- Alterar a tarefa de reseed para buscar um subconjunto de RouterInfos
 de cada um dos vários sites de reseed em vez de usar apenas um único
 site
- Criação de um serviço de monitoramento de reseed fora da rede que
 periodicamente pesquisa sites de reseed e verifica se os dados não
 estão desatualizados ou inconsistentes com outras visões da rede
- A partir da versão 0.9.14, os dados de reseed são agrupados em um
 arquivo zip assinado e a assinatura é verificada quando baixada. See
 [the su3
 specification](#su3)
 for details.

### Captura de consulta

See also [lookup](#lookup) (Reference: [Hashing it out in
Public]() Sections 2.2-2.3 for terms below in
italics)

Semelhante a um ataque bootstrap, um invasor usando um roteador
floodfill poderia tentar \"direcionar\" pares para um subconjunto de
roteadores controlados por ele retornando suas referências.

É improvável que isso funcione por meio de exploração, porque a
exploração é uma tarefa de baixa frequência. Os roteadores adquirem a
maioria de suas referências de pares por meio da atividade normal de
construção de túneis. Os resultados da exploração são geralmente
limitados a alguns hashes de roteador, e cada consulta de exploração é
direcionada a um roteador de inundação aleatório.

As of release 0.8.9, *iterative lookups* are implemented. For floodfill
router references returned in a [I2NP]()
DatabaseSearchReplyMessage response to a lookup, these references are
followed if they are closer (or the next closest) to the lookup key. The
requesting router does not trust that the references are closer to the
key (i.e. they are *verifiably correct*. The lookup also does not stop
when no closer key is found, but continues by querying the next-closet
node, until the timeout or maximum number of queries is reached. This
prevents a malicious floodfill from black-holing a part of the key
space. Also, the daily keyspace rotation requires an attacker to
regenerate a router info within the desired key space region. This
design ensures that the query capture attack described in [Hashing it
out in Public]() is much more difficult.

### Seleção de relé baseada em DHT

(Reference: [Hashing it out in Public]() Section 3)

This doesn\'t have much to do with floodfill, but see the [peer
selection page]() for a discussion of the
vulnerabilities of peer selection for tunnels.

### Vazamentos de informação

(Reference: [In Search of an Anonymous and Secure
Lookup]() Section 3)

This paper addresses weaknesses in the \"Finger Table\" DHT lookups used
by Torsk and NISAN. At first glance, these do not appear to apply to
I2P. First, the use of DHT by Torsk and NISAN is significantly different
from that in I2P. Second, I2P\'s network database lookups are only
loosely correlated to the [peer
selection]() and [tunnel
building]() processes; only
previously-known peers are used for tunnels. Also, peer selection is
unrelated to any notion of DHT key-closeness.

Parte disso pode ser realmente mais interessante quando a rede I2P ficar
muito maior. No momento, cada roteador conhece uma grande proporção da
rede, então procurar por uma Router Info específica no banco de dados da
rede não é fortemente indicativo de uma intenção futura de usar aquele
roteador em um túnel. Talvez quando a rede for 100 vezes maior, a
pesquisa pode ser mais correlativa. Claro, uma rede maior torna um
ataque Sybil muito mais difícil.

However, the general issue of DHT information leakage in I2P needs
further investigation. The floodfill routers are in a position to
observe queries and gather information. Certainly, at a level of *f* =
0.2 (20% malicious nodes, as specifed in the paper) we expect that many
of the Sybil threats we describe
([here](#sybil), [here](#sybil) and
[here](#sybil-partial)) become problematic for several reasons.

## História {#history}

[Movido para a página de discussão do
netdb]().

## Trabalho futuro {#future}

Criptografia de ponta a ponta de pesquisas e respostas adicionais do
netDb.

Melhores métodos para rastrear respostas de pesquisa.


