 Modelo de Risco da
I2P Novembro de 2010
0.8.1 
low medium high ERR_INVALID 
 
 

- **Damage Potential**: **
- **Reliability**: **
- **Exploitability**: **
- **Affected Users**: **
- **Discoverability**: **
- **Severity**: */5*
- **Priority**: */9*

 

### Ataques - Índice

- [Ataques de força bruta](#bruteforce)
- [Ataques de tempo](#timing)
- [Ataques de intersecção](#intersection)
- [Ataques de negação de serviço](#dos)
- [Ataques de marcação](#tagging)
- [Ataques de particionamento](#partitioning)
- [Ataques predecessores](#predecessor)
- [Ataques de colheita](#harvesting)
- [Identificação por meio de análise de tráfego](#traffic)
- [Ataques de Sybil](#sybil)
- [Ataques de exaustão de amigos](#buddy)
- [Ataques criptográficos](#crypto)
- [Ataques de inundação](#floodfill)
- [Outros ataques de banco de dados de rede](#netdb)
- [Ataques a recursos centralizados](#central)
- [Ataques de desenvolvimento](#dev)
- [Ataques via falhas de implementação](#impl)
- [Outras defesas](#blocklist)

 

## O que entendemos por \"anônimo\"?

Seu nível de anonimato pode ser descrito como \"quão difícil é para
alguém descobrir informações que você não quer que eles saibam?\" - quem
você é, onde você está localizado, com quem você se comunica, ou mesmo
quando você se comunica. O anonimato \"perfeito\" não é um conceito útil
aqui - o software não tornará você indistinguível de pessoas que não
usam computadores ou que não estão na Internet. Em vez disso, estamos
trabalhando para fornecer anonimato suficiente para atender às
necessidades reais de quem pudermos - desde aqueles que simplesmente
navegam em sites, até aqueles que trocam dados, até aqueles com medo de
serem descobertos por organizações ou estados poderosos.

A questão de saber se o I2P fornece anonimato suficiente para suas
necessidades específicas é difícil, mas esta página espera ajudar a
responder a essa pergunta explorando como o I2P opera sob vários ataques
para que você possa decidir se ele atende às suas necessidades.

Agradecemos mais pesquisas e análises sobre a resistência do I2P às
ameaças descritas abaixo. Mais revisões da literatura existente (grande
parte dela focada no Tor) e trabalhos originais focados no I2P são
necessários.

## Síntese da Topologia da Rede

I2P builds off the ideas of many [other]()
[systems](), but a few key points should be kept
in mind when reviewing related literature:

- **I2P é uma mixnet de rota livre** - o criador da mensagem define
 explicitamente o caminho pelo qual as mensagens serão enviadas (o
 túnel de saída), e o destinatário da mensagem define explicitamente
 o caminho pelo qual as mensagens serão recebidas (o túnel de
 entrada).
- **I2P não tem pontos de entrada e saída oficiais** - todos os pares
 participam totalmente da mistura e não há proxies de entrada ou
 saída na camada de rede (no entanto, na camada de aplicação ,
 existem alguns proxies)
- **O I2P é totalmente distribuído** - não há controles ou autoridades
 centrais. Alguém poderia modificar alguns roteadores para operar
 cascatas mistas (construindo túneis e fornecendo as chaves
 necessárias para controlar o encaminhamento no ponto final do túnel)
 ou criação de perfil e seleção baseados em diretório , tudo sem
 quebrar a compatibilidade com o resto da rede, mas fazer isso
 obviamente não é necessário (e pode até prejudicar o anonimato).

We have documented plans to implement [nontrivial
delays](#stop) and [batching
strategies](#batching) whose existence is only
known to the particular hop or tunnel gateway that receives the message,
allowing a mostly low latency mixnet to provide cover traffic for higher
latency communication (e.g. email). However we are aware that
significant delays are required to provide meaningful protection, and
that implementation of such delays will be a significant challenge. It
is not clear at this time whether we will actually implement these delay
features.

Em teoria, os roteadores ao longo do caminho da mensagem podem injetar
um número arbitrário de saltos antes de encaminhar a mensagem para o
próximo par, embora a implementação atual não o faça.

## O modelo de risco

O design do I2P começou em 2003, pouco depois do advento do [\[Onion
Routing\]](http://www.onion-router.net),
[\[Freenet\]](http://freenetproject.org/)e
[\[Tor\]](https://www.torproject.org/). Nosso design se beneficia
substancialmente da pesquisa publicada naquela época. O I2P usa várias
técnicas de roteamento onion, então continuamos a nos beneficiar do
significativo interesse acadêmico no Tor.

Tomando como base os ataques e análises apresentados na literatura de
anonimato [](http://freehaven.net/anonbib/topic.html) (em grande parte
[Análise de Tráfego: Protocolos, Ataques, Design Problemas e Problemas
Abertos](http://citeseer.ist.psu.edu/454354.html)), o seguinte descreve
brevemente uma ampla variedade de ataques, bem como muitas das defesas
do I2P. Atualizamos esta lista para incluir novos ataques à medida que
são identificados.

Estão incluídos alguns ataques que podem ser exclusivos do I2P. Não
temos boas respostas para todos esses ataques, no entanto continuamos
pesquisando e melhorando nossas defesas.

Além disso, muitos desses ataques são significativamente mais fáceis do
que deveriam ser, devido ao tamanho modesto da rede atual. Embora
estejamos cientes de algumas limitações que precisam ser abordadas, o
I2P foi projetado para suportar centenas de milhares, ou milhões, de
participantes. À medida que continuamos a espalhar a palavra e a
expandir a rede, esses ataques se tornarão muito mais difíceis.

The [network comparisons]() and [\"garlic\"
terminology]() pages may also be helpful
to review.

{# Hide DREAD ratings until we know how we want to use them

Attacks are judged using the [modified **DREAD**
model]():

- **Damage Potential**: If a threat exploit occurs, how much damage
 will be caused?
- **Reliability**: How reliable is the attack?
- **Exploitability**: What is needed to exploit this threat?
- **Affected Users**: How many users will be affected?
- **Discoverability**: How easy is it to discover this threat?

Each category is given a rating of low, medium or high. The severity and
priority scores are calculated using the equations outlined
[here]().

#}

### Ataques de força bruta {#bruteforce}

{# DREAD_score(2, 1, 1, 1, 3) #}

Um ataque de força bruta pode ser montado por um adversário global
passivo ou ativo, observando todas as mensagens passando entre todos os
nós e tentando correlacionar qual mensagem segue qual caminho. Montar
esse ataque contra I2P deve ser não trivial, já que todos os pares na
rede estão enviando mensagens com frequência (tanto mensagens de ponta a
ponta quanto de manutenção de rede), além de uma mensagem de ponta a
ponta mudar de tamanho e dados ao longo de seu caminho. Além disso, o
adversário externo também não tem acesso às mensagens, já que a
comunicação entre roteadores é criptografada e transmitida (tornando
duas mensagens de 1024 bytes indistinguíveis de uma mensagem de 2048
bytes ).

No entanto, um invasor poderoso pode usar força bruta para detectar
tendências - se eles podem enviar 5 GB para um destino I2P e monitorar a
conexão de rede de todos, eles podem eliminar todos os pares que não
receberam 5 GB de dados. Técnicas para derrotar esse ataque existem, mas
podem ser proibitivamente caras (veja:
[Tarzan](http://citeseer.ist.psu.edu/freedman02tarzan.html)imita ou
tráfego de taxa constante). A maioria dos usuários não está preocupada
com esse ataque, pois o custo de montá-lo é extremo (e geralmente requer
atividade ilegal). No entanto, o ataque ainda é possível, por exemplo,
por um observador em um grande ISP ou um ponto de troca de Internet.
Aqueles que querem se defender contra isso gostariam de tomar
contramedidas apropriadas, como definir limites baixos de largura de
banda e usar conjuntos de arrendamento não publicados ou criptografados
para sites I2P. Outras contramedidas, como atrasos não triviais e rotas
restritas, não estão implementadas atualmente.

As a partial defense against a single router or group of routers trying
to route all the network\'s traffic, routers contain limits as to how
many tunnels can be routed through a single peer. As the network grows,
these limits are subject to further adjustment. Other mechanisms for
peer rating, selection and avoidance are discussed on the [peer
selection page]().

### Ataques de tempo {#timing}

{# DREAD_score(2, 2, 2, 3, 2) #}

As mensagens do I2P são unidirecionais e não necessariamente implicam
que uma resposta será enviada. No entanto, os aplicativos sobre o I2P
provavelmente terão padrões reconhecíveis dentro da frequência de suas
mensagens - por exemplo, uma solicitação HTTP será uma pequena mensagem
com uma grande sequência de mensagens de resposta contendo a resposta
HTTP. Usando esses dados, bem como uma visão ampla da topologia de rede,
um invasor pode ser capaz de desqualificar alguns links como sendo muito
lentos para terem passado a mensagem adiante.

Esse tipo de ataque é poderoso, mas sua aplicabilidade ao I2P não é
óbvia, já que a variação nos atrasos de mensagens devido ao
enfileiramento, processamento de mensagens e limitação frequentemente
atenderá ou excederá o tempo de passagem de uma mensagem por um único
link - mesmo quando o invasor sabe que uma resposta será enviada assim
que a mensagem for recebida. Existem alguns cenários que exporão
razoavelmente respostas automáticas - a biblioteca de streaming faz (com
SYN+ACK) assim como o modo de mensagem de entrega garantida (com
DataMessage+DeliveryStatusMessage).

Without protocol scrubbing or higher latency, global active adversaries
can gain substantial information. As such, people concerned with these
attacks could increase the latency (using [nontrivial
delays](#stop) or [batching
strategies](#batching)), include protocol
scrubbing, or other advanced tunnel routing
[techniques](#batching), but these are
unimplemented in I2P.

References: [Low-Resource Routing Attacks Against Anonymous
Systems]()

### Ataques de intersecção {#intersection}

{# DREAD_score(3, 2, 2, 3, 3) #}

Ataques de interseção contra sistemas de baixa latência são extremamente
poderosos - periodicamente fazem contato com o alvo e rastreiam quais
pares estão na rede. Com o tempo, conforme a rotatividade de nós ocorre,
o invasor obterá informações significativas sobre o alvo simplesmente
cruzando os conjuntos de pares que estão online quando uma mensagem
passa com sucesso. O custo desse ataque é significativo conforme a rede
cresce, mas pode ser viável em alguns cenários.

In summary, if an attacker is at both ends of your tunnel at the same
time, he may be successful. I2P does not have a full defense to this for
low latency communication. This is an inherent weakness of low-latency
onion routing. Tor provides a [similar
disclaimer]().

Defesas parciais implementadas no I2P:

- [strict ordering](#ordering) of peers
- [peer profiling and selection]() from
 a small group that changes slowly
- Limites no número de túneis roteados por um único peer
- Prevenção de pares do mesmo intervalo de IP /16 de serem membros de
 um único túnel
- Para sites I2P ou outros serviços hospedados, oferecemos suporte
 para hospedagem simultânea em vários roteadores ou
 [multihoming](#intersection)

Mesmo no total, essas defesas não são uma solução completa. Além disso,
fizemos algumas escolhas de design que podem aumentar significativamente
nossa vulnerabilidade:

- Nós não utilizamos \"nodos de proteção\" de baixa largura de banda
- Usamos pools de túneis compostos por vários túneis, e o tráfego pode
 mudar de túnel para túnel.
- Os túneis não duram muito; novos túneis são construídos a cada 10
 minutos.
- Os comprimentos dos túneis são configuráveis. Embora túneis de 3
 saltos sejam recomendados para proteção total, vários aplicativos e
 serviços usam túneis de 2 saltos por padrão.

In the future, it could for peers who can afford significant delays (per
[nontrivial delays](#stop) and [batching
strategies](#batching)). In addition, this is only
relevant for destinations that other people know about - a private group
whose destination is only known to trusted peers does not have to worry,
as an adversary can\'t \"ping\" them to mount the attack.

Reference: [One Cell Enough]()

### Ataques de negação de serviço {#dos}

Há uma série de ataques de negação de serviço disponíveis contra I2P,
cada um com custos e consequências diferentes:

{# DREAD_score(1, 1, 2, 1, 3) #}

**Ataque de usuário ganancioso:** Isso é simplesmente pessoas tentando
consumir significativamente mais recursos do que estão dispostas a
contribuir. A defesa contra isso é:

- Set defaults so that most users provide resources to the network. In
 I2P, users route traffic by default. In sharp distinction to [other
 networks](), over 95% of I2P users
 relay traffic for others.
- Forneça opções de configuração fáceis para que os usuários possam
 aumentar sua contribuição de (porcentagem de compartilhamento) para
 a rede. Exiba métricas de fáceis de entender, como \"taxa de
 compartilhamento\", para que os usuários possam ver o que estão
 contribuindo.
- Mantenha uma comunidade forte com blogs, fóruns, IRC e outros meios
 de comunicação.

::: {style="clear:both"}
:::

{# DREAD_score(2, 1, 1, 2, 3) #}

**Starvation attack:** A hostile user may attempt to harm the network by
creating a significant number of peers in the network who are not
identified as being under control of the same entity (as with Sybil).
These nodes then decide not to provide any resources to the network,
causing existing peers to search through a larger network database or
request more tunnels than should be necessary. Alternatively, the nodes
may provide intermittent service by periodically dropping selected
traffic, or refusing connections to certain peers. This behavior may be
indistinguishable from that of a heavily-loaded or failing node. I2P
addresses these issues by maintaining
[profiles]() on the peers, attempting to
identify underperforming ones and simply ignoring them, or using them
rarely. We have significantly enhanced the ability to recognize and
avoid troublesome peers; however there are still significant efforts
required in this area.

::: {style="clear:both"}
:::

{# DREAD_score(1, 2, 2, 2, 3) #}

**Flooding attack:** A hostile user may attempt to flood the network, a
peer, a destination, or a tunnel. Network and peer flooding is possible,
and I2P does nothing to prevent standard IP layer flooding. The flooding
of a destination with messages by sending a large number to the
target\'s various inbound tunnel gateways is possible, but the
destination will know this both by the contents of the message and
because the tunnel\'s tests will fail. The same goes for flooding just a
single tunnel. I2P has no defenses for a network flooding attack. For a
destination and tunnel flooding attack, the target identifies which
tunnels are unresponsive and builds new ones. New code could also be
written to add even more tunnels if the client wishes to handle the
larger load. If, on the other hand, the load is more than the client can
deal with, they can instruct the tunnels to throttle the number of
messages or bytes they should pass on (once the [advanced tunnel
operation](#batching) is implemented).

::: {style="clear:both"}
:::

{# DREAD_score(1, 1, 1, 1, 1) #}

**Ataque de carga de CPU:** Atualmente, existem alguns métodos para as
pessoas solicitarem remotamente que um peer execute alguma operação
criptograficamente cara , e um invasor hostil poderia usá-los para
inundar esse peer com um grande número deles em uma tentativa de
sobrecarregar a CPU. Tanto usar boas práticas de engenharia quanto
potencialmente exigir que certificados não triviais (por exemplo,
HashCash) sejam anexados a essas solicitações caras deve mitigar o
problema, embora possa haver espaço para um invasor explorar vários bugs
na implementação.

::: {style="clear:both"}
:::

{# DREAD_score(2, 2, 3, 2, 3) #}

**Floodfill DOS attack:** A hostile user may attempt to harm the network
by becoming a floodfill router. The current defenses against unreliable,
intermittent, or malicious floodfill routers are poor. A floodfill
router may provide bad or no response to lookups, and it may also
interfere with inter-floodfill communication. Some defenses and [peer
profiling]() are implemented, however
there is much more to do. For more information see the [network database
page](#threat).

::: {style="clear:both"}
:::

### Ataques de marcação {#tagging}

{# DREAD_score(1, 3, 1, 1, 1) #}

Tagging attacks - modifying a message so that it can later be identified
further along the path - are by themselves impossible in I2P, as
messages passed through tunnels are signed. However, if an attacker is
the inbound tunnel gateway as well as a participant further along in
that tunnel, with collusion they can identify the fact that they are in
the same tunnel (and prior to adding [unique hop
ids](#tunnelId) and other updates, colluding peers
within the same tunnel can recognize that fact without any effort). An
attacker in an outbound tunnel and any part of an inbound tunnel cannot
collude however, as the tunnel encryption pads and modifies the data
separately for the inbound and outbound tunnels. External attackers
cannot do anything, as the links are encrypted and messages signed.

### Ataques de particionamento {#partitioning}

{# DREAD_score(3, 1, 1, 1, 2) #}

Ataques de particionamento - encontrar maneiras de segregar (técnica ou
analiticamente) os pares em uma rede - são importantes para se ter em
mente ao lidar com um adversário poderoso, já que o tamanho da rede
desempenha um papel fundamental na determinação do seu anonimato. O
particionamento técnico cortando links entre pares para criar redes
fragmentadas é abordado pelo banco de dados de rede integrado do I2P,
que mantém estatísticas sobre vários pares para permitir que quaisquer
conexões existentes com outras seções fragmentadas sejam exploradas para
curar a rede. No entanto, se o invasor desconectar todos os links para
pares não controlados, essencialmente isolando o alvo, nenhuma
quantidade de cura do banco de dados de rede consertará isso. Em esse
ponto, a única coisa que o roteador pode esperar fazer é perceber que um
número significativo de pares anteriormente confiáveis ficaram
indisponíveis e alertar o cliente que ele está temporariamente
desconectado (este código de detecção não está implementado em o
momento).

Partitioning the network analytically by looking for differences in how
routers and destinations behave and grouping them accordingly is also a
very powerful attack. For instance, an attacker
[harvesting](#harvesting) the network database will know when a
particular destination has 5 inbound tunnels in their LeaseSet while
others have only 2 or 3, allowing the adversary to potentially partition
clients by the number of tunnels selected. Another partition is possible
when dealing with the [nontrivial delays](#stop)
and [batching strategies](#batching), as the
tunnel gateways and the particular hops with non-zero delays will likely
stand out. However, this data is only exposed to those specific hops, so
to partition effectively on that matter, the attacker would need to
control a significant portion of the network (and still that would only
be a probabilistic partition, as they wouldn\'t know which other tunnels
or messages have those delays).

Also discussed on the [network database
page](#threat) (bootstrap attack).

### Ataques predecessores {#predecessor}

{# DREAD_score(1, 1, 1, 1, 3) #}

O ataque predecessor está coletando estatísticas passivamente em uma
tentativa de ver quais pares estão \'próximos\' do destino participando
de seus túneis e mantendo o controle do salto anterior ou seguinte (para
túneis de saída ou entrada, respectivamente). Com o tempo, usando uma
amostra perfeitamente aleatória de pares e ordenação aleatória , um
invasor seria capaz de ver qual par aparece como \'mais próximo\'
estatisticamente mais do que o resto, e esse par estaria, por sua vez,
onde o alvo está localizado.

I2P avoids this in four ways: first, the peers selected to participate
in tunnels are not randomly sampled throughout the network - they are
derived from the [peer selection]()
algorithm which breaks them into tiers. Second, with [strict
ordering](#ordering) of peers in a tunnel,
the fact that a peer shows up more frequently does not mean they\'re the
source. Third, with [permuted tunnel
length](#length) (not enabled by default)
even 0 hop tunnels can provide plausible deniability as the occasional
variation of the gateway will look like normal tunnels. Fourth, with
[restricted routes](#fullRestrictedRoutes)
(unimplemented), only the peer with a restricted connection to the
target will ever contact the target, while attackers will merely run
into that gateway.

The current [tunnel build method]() was
specifically designed to combat the predecessor attack. See also [the
intersection attack](#intersection).

References: []() which is an
update to the 2004 predecessor attack paper []().

### Ataques de colheita {#harvesting}

{# DREAD_score(1, 1, 2, 2, 3) #}

\"Colheita\" significa compilar uma lista de usuários executando o I2P.
Ele pode ser usado para ataques legais e para ajudar outros ataques,
simplesmente executando um peer, vendo com quem ele se conecta e
coletando quaisquer referências a outros peers que puder encontrar.

O I2P em si não foi projetado com defesas eficazes contra esse ataque,
já que há um banco de dados de rede distribuído contendo apenas essas
informações. Os seguintes fatores tornam o ataque um pouco mais difícil
na prática:

- O crescimento da rede tornará mais difícil obter uma determinada
 proporção da rede
- Os roteadores Floodfill implementam limites de consulta como
 proteção DOS
- O \"modo oculto\", que impede um roteador de publicar suas
 informações no netDb, (mas também o impede de retransmitir dados),
 não é amplamente utilizado atualmente, mas poderia ser.

In future implementations, [basic](#nat) and
[comprehensive](#fullRestrictedRoutes) restricted
routes, this attack loses much of its power, as the \"hidden\" peers do
not publish their contact addresses in the network database - only the
tunnels through which they can be reached (as well as their public keys,
etc).

No futuro, os roteadores poderão usar o GeoIP para identificar se estão
em um país específico onde a identificação como um nó I2P seria
arriscada. Nesse caso, o roteador poderá habilitar automaticamente o
modo oculto ou promulgar outros métodos de rota restritos.

### Identificação por meio de análise de tráfego {#traffic}

{# DREAD_score(1, 1, 2, 3, 3) #}

By inspecting the traffic into and out of a router, a malicious ISP or
state-level firewall could identify that a computer is running I2P. As
discussed [above](#harvesting), I2P is not specifically designed to hide
that a computer is running I2P. However, several design decisions made
in the design of the [transport layer and
protocols]() make it somewhat difficult to
identify I2P traffic:

- Seleção aleatória de porta
- Criptografia ponto a ponto de todo o tráfego
- Troca de chaves DH sem bytes de protocolo ou outros campos
 constantes não criptografados
- Simultaneous use of both [TCP]() and
 [UDP]() transports. UDP may be much harder for
 some Deep Packet Inspection (DPI) equipment to track.

Em um futuro próximo, planejamos abordar diretamente os problemas de
análise de tráfego por meio de maior ofuscação dos protocolos de
transporte I2P, possivelmente incluindo:

- Preenchimento na camada de transporte para comprimentos aleatórios,
 especialmente durante o handshake de conexão
- Estudo de assinaturas de distribuição de tamanho de pacote e
 preenchimento adicional conforme necessário
- Desenvolvimento de métodos de transporte adicionais que imitam SSL
 ou outros protocolos comuns
- Revisão das estratégias de preenchimento em camadas superiores para
 ver como elas afetam os tamanhos dos pacotes na camada de transporte
- Revisão dos métodos implementados por vários firewalls de nível
 estadual para bloquear o Tor
- Trabalhando diretamente com especialistas em DPI e ofuscação

Reference: [Breaking and Improving Protocol
Obfuscation]()

### Ataques de Sybil {#sybil}

{# DREAD_score(3, 2, 1, 3, 3) #}

Sybil descreve uma categoria de ataques onde o adversário cria
arbitrariamente um grande número de nós coniventes e usa os números
aumentados para ajudar a montar outros ataques. Por exemplo, se um
invasor estiver em uma rede onde os pares são selecionados
aleatoriamente e eles querem uma chance de 80% de ser um desses pares,
eles simplesmente criam cinco vezes o número de nós que estão na rede e
rolam os dados. Quando a identidade é livre, Sybil pode ser uma técnica
muito potente para um adversário poderoso. A técnica primária para
resolver isso é simplesmente tornar a identidade \'não livre\' -
[Tarzan](http://www.pdos.lcs.mit.edu/tarzan/) (entre outros) usa o fato
de que endereços IP são limitados, enquanto IIP usou
[HashCash](http://www.hashcash.org/) para \'cobrar\' pela criação de uma
nova identidade . Atualmente, não implementamos nenhuma técnica
específica para resolver Sybil, mas incluímos certificados de espaço
reservado nas estruturas de dados do roteador e destino que podem conter
um certificado HashCash de valor apropriado quando necessário (ou algum
outro certificado que comprove escassez).

Exigir certificados HashCash em vários lugares tem dois grandes
problemas:

- Manter compatibilidade com versões anteriores
- O problema clássico do HashCash - selecionar valores de HashCash que
 sejam provas de trabalho significativas em máquinas de ponta, embora
 ainda sejam viáveis em máquinas de baixo custo, como dispositivos
 móveis.

Várias limitações no número de roteadores em um determinado intervalo de
IP restringem a vulnerabilidade a invasores que não têm a capacidade de
colocar máquinas em vários blocos de IP. No entanto, esta não é uma
defesa significativa contra um adversário poderoso.

See the [network database page](#threat) for more
Sybil discussion.

### Ataques de exaustão de amigos {#buddy}

{# DREAD_score(3, 2, 2, 1, 3) #}

(Reference: [In Search of an Anonymous and Secure
Lookup]() Section 5.2)

By refusing to accept or forward tunnel build requests, except to a
colluding peer, a router could ensure that a tunnel is formed wholly
from its set of colluding routers. The chances of success are enhanced
if there is a large number of colluding routers, i.e. a [Sybil
attack](#sybil). This is somewhat mitigated by our [peer
profiling]() methods used to monitor the
performance of peers. However, this is a powerful attack as the number
of routers approaches *f* = 0.2, or 20% malicious nodes, as specifed in
the paper. The malicous routers could also maintain connections to the
target router and provide excellent forwarding bandwidth for traffic
over those connections, in an attempt to manipulate the profiles managed
by the target and appear attractive. Further research and defenses may
be necessary.

### Ataques criptográficos {#crypto}

{# DREAD_score(3, 2, 1, 3, 1) #}

We use strong cryptography with long keys, and we assume the security of
the industry-standard cryptographic primitives used in I2P, as
documented [on the low-level cryptography
page](). Security features include the
immediate detection of altered messages along the path, the inability to
decrypt messages not addressed to you, and defense against
man-in-the-middle attacks. The key sizes chosen in 2003 were quite
conservative at the time, and are still longer than those used in [other
anonymity networks](https://torproject.org/). We don\'t think the
current key lengths are our biggest weakness, especially for
traditional, non-state-level adversaries; bugs and the small size of the
network are much more worrisome. Of course, all cryptographic algorithms
eventually become obsolete due to the advent of faster processors,
cryptographic research, and advancements in methods such as rainbow
tables, clusters of video game hardware, etc. Unfortunately, I2P was not
designed with easy mechanisms to lengthen keys or change shared secret
values while maintaining backward compatibility.

Upgrading the various data structures and protocols to support longer
keys will have to be tackled eventually, and this will be a [major
undertaking](), just as it will be for
[others](https://torproject.org/). Hopefully, through careful planning,
we can minimize the disruption, and implement mechanisms to make it
easier for future transitions.

No futuro, vários protocolos I2P e estruturas de dados suportam
mensagens de preenchimento seguro para tamanhos arbitrários, então as
mensagens poderiam ser tornadas constantes ou mensagens de alho poderiam
ser modificadas aleatoriamente para que alguns dentes parecessem conter
mais subdentes do que realmente contêm. No momento, no entanto,
mensagens de alho, túnel e ponta a ponta incluem preenchimento aleatório
simples.

### Ataques de anonimato de inundação {#floodfill}

{# DREAD_score(3, 2, 1, 2, 2) #}

In addition to the floodfill DOS attacks described [above](#ffdos),
floodfill routers are uniquely positioned to learn about network
participants, due to their role in the netDb, and the high frequency of
communication with those participants. This is somewhat mitigated
because floodfill routers only manage a portion of the total keyspace,
and the keyspace rotates daily, as explained on the [network database
page](#threat). The specific mechanisms by which
routers communicate with floodfills have been [carefully
designed](#delivery). However, these threats
should be studied further. The specific potential threats and
corresponding defenses are a topic for future research.

### Outros ataques de banco de dados de rede {#netdb}

A hostile user may attempt to harm the network by creating one or more
floodfill routers and crafting them to offer bad, slow, or no responses.
Several scenarios are discussed on the [network database
page](#threat).

### Ataques de recursos centrais {#central}

{# DREAD_score(1, 1, 1, 3, 3) #}

Existem alguns recursos centralizados ou limitados (alguns dentro do
I2P, outros não) que podem ser atacados ou usados como um vetor para
ataques. A ausência do jrandom a partir de novembro de 2007, seguida
pela perda do serviço de hospedagem i2p.net em janeiro de 2008, destacou
vários recursos centralizados no desenvolvimento e operação da rede I2P,
a maioria dos quais agora estão distribuídos. Ataques a recursos
acessíveis externamente afetam principalmente a capacidade de novos
usuários nos encontrarem, não a operação da rede em si.

- The [website]() is mirrored and uses DNS
 round-robin for external public access.
- Routers now support [multiple external reseed
 locations](#reseed), however more reseed hosts
 may be needed, and the handling of unreliable or malicious reseed
 hosts may need improvement.
- Os roteadores agora oferecem suporte a vários locais de arquivos de
 atualização. Um host de atualização malicioso pode alimentar um
 arquivo enorme, é necessário limitar o tamanho.
- Os roteadores agora oferecem suporte a vários signatários de
 atualização confiáveis padrão.
- Os roteadores agora lidam melhor com [vários pares de floodfill não
 confiáveis](#ffdos). Floodfills maliciosos [precisam de](#ffdos)
 [mais](#floodfill) estudo.
- The code is now stored in a [distributed source control
 system]().
- Os roteadores dependem de um único host de notícias, mas há uma URL
 de backup codificada apontando para um host diferente. Um host de
 notícias malicioso pode alimentar um arquivo enorme, é preciso
 limitar o tamanho.
- [Naming system services](), including
 address book subscription providers, add-host services, and jump
 services, could be malicious. Substantial protections for
 subscriptions were implemented in release 0.6.1.31, with additional
 enhancements in subsequent releases. However, all naming services
 require some measure of trust, see [the naming
 page]() for details.
- Continuamos dependentes do serviço DNS para i2p2.de. Perdê-lo
 causaria uma interrupção substancial em nossa capacidade de atrair
 novos usuários, e reduziria a rede (no curto a médio prazo), assim
 como ocorreu com a perda do i2p.net.

### Ataques de desenvolvimento {#dev}

{# DREAD_score(2, 1, 1, 3, 1) #}

Esses ataques não são diretamente na rede, mas vão atrás de sua equipe
de desenvolvimento introduzindo obstáculos legais a qualquer um que
contribua para o desenvolvimento do software, ou usando quaisquer meios
disponíveis para fazer os desenvolvedores subverterem o software.
Medidas técnicas tradicionais não podem derrotar esses ataques, e se
alguém ameaçasse a vida ou o sustento de um desenvolvedor (ou mesmo
apenas emitindo uma ordem judicial junto com uma ordem de silêncio, sob
ameaça de prisão), teríamos um grande problema.

No entanto, duas técnicas ajudam a se defender contra esses ataques:

- All components of the network must be open source to enable
 inspection, verification, modification, and improvement. If a
 developer is compromised, once it is noticed the community should
 demand explanation and cease to accept that developer\'s work. All
 checkins to our [distributed source control
 system]() are cryptographically signed,
 and the release packagers use a trust-list system to restrict
 modifications to those previously approved.
- Development over the network itself, allowing developers to stay
 anonymous but still secure the development process. All I2P
 development can occur through I2P - using a [distributed source
 control system](), a distributed source
 control system, IRC chat, public web servers, discussion forums
 (forum.i2p), and the software distribution sites, all available
 within I2P.

Também mantemos relacionamentos com diversas organizações que oferecem
aconselhamento jurídico, caso seja necessária alguma defesa.

### Ataques via falhas de implementação (bugs) {#impl}

{# DREAD_score(2, 2, 1, 3, 1) #}

Por mais que tentemos, a maioria dos aplicativos não triviais inclui
erros no design ou na implementação , e o I2P não é exceção. Pode haver
bugs que podem ser explorados para atacar o anonimato ou a segurança da
comunicação que roda sobre o I2P de maneiras inesperadas . Para ajudar a
resistir a ataques contra o design ou protocolos em uso, publicamos
todos os designs e documentação e solicitamos revisão e crítica com a
esperança de que muitos olhos melhorem o sistema. Não acreditamos em
[segurança através da obscuridade](http://www.haystacknetwork.com/).

Além disso, o código está sendo tratado da mesma forma, com pouca
aversão a retrabalhar ou jogar fora algo que não atende às necessidades
do sistema de software (incluindo facilidade de modificação). A
documentação para o design e implementação da rede e os componentes de
software são uma parte essencial da segurança, pois sem eles é
improvável que os desenvolvedores estejam dispostos a gastar tempo para
aprender o software o suficiente para identificar deficiências e bugs.

Nosso software provavelmente contém, em particular, bugs relacionados à
negação de serviço por meio de erros de falta de memória (OOMs),
problemas de script entre sites (XSS) no console do roteador, e outras
vulnerabilidades a entradas não padronizadas por meio de vários
protocolos.

I2P is still a small network with a small development community and
almost no interest from academic or research groups. Therefore we lack
the analysis that [other anonymity networks](https://torproject.org/)
may have received. We continue to recruit people to [get
involved]() and help.

## Outras defesas

### Listas de bloqueios {#blocklist}

Até certo ponto, o I2P poderia ser aprimorado para evitar que pares
operem em endereços IP listados em uma lista de bloqueio. Várias listas
de bloqueio estão comumente disponíveis em formatos padrão, listando
organizações anti-P2P, potenciais adversários de nível estadual e
outros.

Na medida em que os pares ativos realmente aparecem na lista de bloqueio
real, o bloqueio por apenas um subconjunto de pares tenderia a segmentar
a rede, agravaria os problemas de acessibilidade e diminuiria a
confiabilidade geral. Portanto, gostaríamos de concordar com uma lista
de bloqueio específica e habilitá-la por padrão.

As listas de bloqueio são apenas uma parte (talvez uma pequena parte) de
uma série de defesas contra malícia. Em grande parte, o sistema de
criação de perfil faz um bom trabalho ao medir o comportamento do
roteador para que não precisemos confiar em nada no netDb. No entanto,
há mais que pode ser feito. Para cada uma das áreas na lista acima, há
melhorias que podemos fazer na detecção de maldade.

Se uma lista de bloqueio for hospedada em um local central com
atualizações automáticas a rede fica vulnerável a um [ataque de recurso
central](#central). A assinatura automática de uma lista dá ao provedor
da lista o poder de desligar a rede i2p. Completamente.

Atualmente, uma lista de bloqueio padrão é distribuída com nosso
software, listando apenas os IPs de fontes DOS anteriores. Não há
mecanismo de atualização automática. Caso um intervalo de IP específico
implemente ataques sérios na rede I2P, teríamos que pedir às pessoas que
atualizassem sua lista de bloqueio manualmente por meio de mecanismos
fora de banda, como fóruns, blogs, etc.


