 Implementação do
Túnel Julho de 2019
0.9.41 Esta
página documenta a implementação atual do túnel.

## Visão geral do túnel {#tunnel.overview}

Dentro do I2P, as mensagens são passadas em uma direção através de um
túnel virtual de pares, usando quaisquer meios disponíveis para passar a
mensagem para o próximo salto. As mensagens chegam ao gateway do túnel,
são agrupadas e/ou fragmentadas em mensagens de túnel de tamanho fixo, e
são encaminhadas para o próximo salto no túnel, que processa e verifica
a validade da mensagem e a envia para o próximo salto, e assim por
diante, até atingir o ponto final do túnel. O ponto de extremidade pega
as mensagens agrupadas pelo gateway e as encaminha conforme as
instruções - para outro roteador, para outro túnel em outro roteador ou
localmente.

Os túneis funcionam todos da mesma forma, mas podem ser segmentados em
dois grupos diferentes - túneis de entrada e túneis de saída. Os túneis
de entrada têm um gateway não confiável que passa mensagens para o
criador do túnel , que serve como ponto final do túnel. Para túneis de
saída , o criador do túnel serve como gateway, passando mensagens para o
ponto final remoto.

O criador do túnel seleciona exatamente quais pares participarão do
túnel e fornece a cada um os dados de configuração necessários. Eles
podem ter qualquer número de saltos. A intenção é tornar difícil para os
participantes ou terceiros determinarem o comprimento de um túnel, ou
mesmo para os participantes em conluio determinarem se eles são uma
parte do mesmo túnel (exceto na situação em que os pares em conluio
estão próximos um do outro no túnel).

Na prática, uma série de pools de túneis são usados para diferentes
propósitos - cada destino de cliente local tem seu próprio conjunto de
túneis de entrada e túneis de saída, configurados para atender às suas
necessidades de anonimato e desempenho. Além disso, o próprio roteador
mantém uma série de pools para participar do banco de dados da rede e
para gerenciar os próprios túneis.

I2P é uma rede inerentemente comutada por pacotes, mesmo com esses
túneis , permitindo que ela aproveite múltiplos túneis rodando em
paralelo, aumentando a resiliência e balanceando a carga. Fora da camada
I2P principal, há uma biblioteca de streaming ponta a ponta opcional
disponível para aplicativos clientes, expondo operação TCP-esque,
incluindo reordenação de mensagens, retransmissão, controle de
congestionamento, etc.

An overview of I2P tunnel terminology is [on the tunnel overview
page]().

## Operação de Túnel (Processamento de Mensagens) {#tunnel.operation}

### Visão geral

After a tunnel is built, [I2NP messages]() are
processed and passed through it. Tunnel operation has four distinct
processes, taken on by various peers in the tunnel.

1. Primeiro, o gateway de túnel acumula um número de mensagens I2NP e
 as pré-processa em mensagens de túnel para entrega .
2. Em seguida, esse gateway criptografa os dados pré-processados e,
 então, os encaminha para o primeiro salto.
3. Esse peer e os participantes subsequentes do túnel desvendam uma
 camada de criptografia, verificando se não é uma duplicata e, então,
 a encaminham para o próximo peer.
4. Por fim, as mensagens do túnel chegam ao ponto final, onde as
 mensagens I2NP originalmente agrupadas pelo gateway são remontadas e
 encaminhadas conforme solicitado.

Os participantes do túnel intermediário não sabem se estão em um túnel
de entrada ou de saída ; eles sempre \"criptografam\" para o próximo
salto. Portanto, aproveitamos a criptografia AES simétrica para
\"descriptografar\" no gateway do túnel de saída, para que o texto
simples seja revelado no ponto de extremidade de saída.

![Inbound and outbound tunnel
schematic](images/tunnels.png "Inbound and outbound tunnel schematic")

+-----------------+-----------------+-----------------+-----------------+
| Função | Pr | Operação de | Pó |
| | é-processamento | Criptografia | s-processamento |
+=================+=================+=================+=================+
| Gateway de | Fragmento, Lote | Criptografar | Encaminhar para |
| saída (criador) | e Pad | iterativamente | o próximo pulo |
| | | (usando | |
| | | operações de | |
| | | d | |
| | | escriptografia) | |
+-----------------+-----------------+-----------------+-----------------+
| Participante |   | Descriptografar | Encaminhar para |
| | | (usando uma | o próximo pulo |
| | | operação de | |
| | | criptografia) | |
+-----------------+-----------------+-----------------+-----------------+
| Ponto de saída |   | Descriptografar | Remontar |
| | | (usando uma | fragmentos, |
| | | operação de | encaminhar |
| | | criptografia) | conforme as |
| | | para revelar a | instruções para |
| | | mensagem do | o gateway de |
| | | túnel em texto | entrada ou |
| | | simples | roteador |
+-----------------+-----------------+-----------------+-----------------+
| ------------- | | | |
+-----------------+-----------------+-----------------+-----------------+
| Gateway | Fragmento, Lote | Encriptar | Encaminhar para |
| entrante | e Pad | | o próximo pulo |
+-----------------+-----------------+-----------------+-----------------+
| Participante |   | Encriptar | Encaminhar para |
| | | | o próximo pulo |
+-----------------+-----------------+-----------------+-----------------+
| Ponto de |   | Descriptografar | Remontar |
| extremidade de | | iterativamente | fragmentos, |
| entrada | | para revelar | receber dados |
| (criador) | | mensagem de | |
| | | túnel em texto | |
| | | simples | |
+-----------------+-----------------+-----------------+-----------------+

### Processamento de Gateway {#tunnel.gateway}

#### Pré-processamento de mensagens {#tunnel.preprocessing}

A tunnel gateway\'s function is to fragment and pack [I2NP
messages]() into fixed-size [tunnel
messages]() and encrypt the tunnel
messages. Tunnel messages contain the following:

- Um ID de túnel de 4 bytes
- Um IV de 16 bytes (vetor de inicialização)
- Uma soma de verificação
- Preenchimento, se necessário
- Um ou mais pares { delivery instruction, I2NP message fragment }

IDs de túnel são números de 4 bytes usados em cada salto - os
participantes sabem qual ID de túnel ouvir mensagens e qual ID de túnel
eles devem ser encaminhados para o próximo salto, e cada salto escolhe a
ID de túnel na qual eles recebem mensagens . Os túneis em si têm vida
curta (10 minutos). Mesmo se os túneis subsequentes forem construídos
usando a mesma sequência de pares, a ID de túnel de cada salto mudará.

Para evitar que adversários marquem as mensagens ao longo do caminho
ajustando o tamanho da mensagem, todas as mensagens de túnel têm um
tamanho fixo de 1024 bytes. Para acomodar mensagens I2NP maiores, bem
como para suportar as menores de forma mais eficiente, o gateway divide
as mensagens I2NP maiores em fragmentos contidos em cada mensagem de
túnel. O ponto final tentará reconstruir a mensagem I2NP a partir dos
fragmentos por um curto período de tempo, mas os descartará conforme
necessário.

Details are in the [tunnel message
specification]().

### Criptografia de Gateway

Após o pré-processamento das mensagens em uma carga útil preenchida, o
gateway cria um valor IV aleatório de 16 bytes, criptografando-o
iterativamente e a mensagem do túnel conforme necessário, e encaminha a
tupla {tunnelID, IV, encrypted tunnel message} para o próximo salto.

A forma como a criptografia no gateway é feita depende se o túnel é um
túnel de entrada ou de saída. Para túneis de entrada, eles simplesmente
selecionam um IV aleatório, pós-processando e atualizando-o para gerar o
IV para o gateway e usando esse IV junto com sua própria chave de camada
para criptografar os dados pré-processados. Para túneis de saída , eles
devem descriptografar iterativamente o IV (não criptografado) e os dados
pré-processados com o IV e as chaves de camada para todos os saltos no
túnel. O resultado da criptografia do túnel de saída é que quando cada
par o criptografa, o ponto final recuperará os dados pré-processados
iniciais.

### Processamento de Participantes {#tunnel.participant}

Quando um peer recebe uma mensagem de túnel, ele verifica se a mensagem
veio de o mesmo salto anterior de antes (inicializado quando a primeira
mensagem chega através de o túnel). Se o peer anterior for um roteador
diferente, ou se a mensagem já tiver sido vista, a mensagem é
descartada. O participante então criptografa o IV recebido com
AES256/ECB usando sua chave IV para determinar o IV atual, usa aquele IV
com a chave de camada do participante para criptografar os dados,
criptografa o IV atual com AES256/ECB usando sua chave IV novamente,
então encaminha a tupla {nextTunnelId, nextIV, encryptedData} para o
próximo salto. Essa criptografia dupla do IV (antes e depois do uso)
ajuda a lidar com uma certa classe de ataques de confirmação . See [this
email](http://zzz.i2p/archive/2005-07/msg00031.html) and the surrounding
thread for more information.

A detecção de mensagens duplicadas é tratada por um filtro Bloom
decadente em IVs de mensagem . Cada roteador mantém um único filtro
Bloom para conter o XOR do IV e o primeiro bloco da mensagem recebida
para todos os túneis dos quais ele participa , modificado para descartar
entradas vistas após 10-20 minutos (quando os túneis terão expirado). O
tamanho do filtro Bloom e os parâmetros usados são suficientes para mais
do que saturar a conexão de rede do roteador com uma chance
insignificante de falso positivo. O valor exclusivo alimentado no filtro
Bloom é o XOR do IV e do primeiro bloco, de modo a evitar que pares em
conluio não sequenciais no túnel marquem uma mensagem reenviando-a com o
IV e o primeiro bloco trocados.

### Processamento de ponto final {#tunnel.endpoint}

Após receber e validar uma mensagem de túnel no último salto no túnel,
como o ponto final recupera os dados codificados pelo gateway depende se
o túnel é um túnel de entrada ou de saída. Para túneis de saída, o ponto
final criptografa a mensagem com sua chave de camada, assim como
qualquer outro participante, expondo os dados pré-processados. Para
túneis de entrada, o ponto final também é o criador do túnel, então eles
podem apenas descriptografar iterativamente o IV e a mensagem, usando as
chaves de camada e IV de cada etapa na ordem inversa.

Neste ponto, o ponto final do túnel tem os dados pré-processados
enviados pelo gateway, , que ele pode então analisar nas mensagens I2NP
incluídas e encaminhá-las conforme solicitado em suas instruções de
entrega.

## Construção de Túnel {#tunnel.building}

Ao construir um túnel, o criador deve enviar uma solicitação com os
dados de configuração necessários para cada um dos saltos e esperar que
todos eles concordem antes de habilitar o túnel. As solicitações são
criptografadas para que apenas os pares que precisam saber uma
informação (como a camada do túnel ou a chave IV) tenham esses dados.
Além disso, apenas o criador do túnel terá acesso à resposta do par. Há
três dimensões importantes a serem lembradas ao produzir os túneis:
quais pares são usados (e onde), como as solicitações são enviadas (e as
respostas são recebidas) e como são mantidas.

### Seleção de Pares {#tunnel.peerselection}

Além dos dois tipos de túneis - de entrada e de saída - há dois estilos
de seleção de pares usados para diferentes túneis - exploratório e
cliente. Os túneis exploratórios são usados para manutenção de banco de
dados de rede e manutenção de túneis , enquanto os túneis de cliente são
usados para mensagens de cliente de ponta a ponta.

#### Seleção de pares de túneis exploratórios {#tunnel.selection.exploratory}

Túneis exploratórios são construídos a partir de uma seleção aleatória
de pares de um subconjunto da rede. O subconjunto específico varia no
roteador local e em quais são suas necessidades de roteamento de túnel.
Em geral, os túneis exploratórios são construídos a partir de pares
selecionados aleatoriamente que estão na categoria de perfil \"não
falhando, mas ativo\" do par. O propósito secundário dos túneis, além do
mero roteamento de túnel, é encontrar pares de alta capacidade
subutilizados para que eles possam ser promovidos para uso em túneis de
cliente.

Exploratory peer selection is discussed further on the [Peer Profiling
and Selection page]().

#### Seleção de pares de túnel do cliente {#tunnel.selection.client}

Os túneis do cliente são construídos com um conjunto mais rigoroso de
requisitos - o roteador local selecionará pares de sua categoria de
perfil \"rápido e de alta capacidade\" para que o desempenho e a
confiabilidade atendam às necessidades do aplicativo cliente. No
entanto, há vários detalhes importantes além dessa seleção básica que
devem ser respeitados, dependendo das necessidades de anonimato do
cliente.

Client peer selection is discussed further on the [Peer Profiling and
Selection page]().

#### Ordenação por pares dentro de túneis {#ordering}

Peers are ordered within tunnels to deal with the [predecessor
attack]() [(2008
update)]().

Para frustrar o ataque predecessor , a seleção de túnel mantém os pares
selecionados em uma ordem estrita - se A, B e C estiverem em um túnel
para um pool de túneis específico, o salto após A é sempre B, e o salto
após B é sempre C.

A ordenação é implementada gerando uma chave aleatória de 32 bytes para
cada pool de túneis na inicialização. Os pares não devem ser capazes de
adivinhar a ordenação, ou um invasor pode criar dois hashes de roteador
bem separados para maximizar a chance de estar em ambas as extremidades
de um túnel. Os pares são classificados pela distância XOR do Hash
SHA256 (o hash do par concatenado com a chave aleatória) da chave
aleatória

 p = peer hash
 k = random key
 d = XOR(H(p+k), k)

Como cada pool de túneis usa uma chave aleatória diferente, a ordenação
é consistente dentro de um único pool, mas não entre pools diferentes.
Novas chaves são geradas a cada reinicialização do roteador.

### Entrega de requisição {#tunnel.request}

A multi-hop tunnel is built using a single build message which is
repeatedly decrypted and forwarded. In the terminology of [Hashing it
out in Public](), this is \"non-interactive\"
telescopic tunnel building.

This tunnel request preparation, delivery, and response method is
[designed]() to reduce the number of
predecessors exposed, cuts the number of messages transmitted, verifies
proper connectivity, and avoids the message counting attack of
traditional telescopic tunnel creation. (This method, which sends
messages to extend a tunnel through the already-established part of the
tunnel, is termed \"interactive\" telescopic tunnel building in the
\"Hashing it out\" paper.)

The details of tunnel request and response messages, and their
encryption, [are specified here]().

Os pares podem rejeitar solicitações de criação de túneis por uma
variedade de razões, embora uma série de quatro rejeições cada vez mais
severas sejam conhecidas: rejeição probabilística (devido à aproximação
da capacidade do roteador ou em resposta a uma enxurrada de
solicitações), sobrecarga transitória, sobrecarga de largura de banda e
falha crítica. Quando recebidas, essas quatro são interpretadas pelo
criador do túnel para ajudar a ajustar seu perfil do roteador em
questão.

For more information on peer profiling, see the [Peer Profiling and
Selection page]().

### Piscinas de Túnel {#tunnel.pooling}

To allow efficient operation, the router maintains a series of tunnel
pools, each managing a group of tunnels used for a specific purpose with
their own configuration. When a tunnel is needed for that purpose, the
router selects one out of the appropriate pool at random. Overall, there
are two exploratory tunnel pools - one inbound and one outbound - each
using the router\'s default configuration. In addition, there is a pair
of pools for each local destination - one inbound and one outbound
tunnel pool. Those pools use the configuration specified when the local
destination connects to the router via [I2CP](),
or the router\'s defaults if not specified.

Each pool has within its configuration a few key settings, defining how
many tunnels to keep active, how many backup tunnels to maintain in case
of failure, how long the tunnels should be, whether those lengths should
be randomized, as well as any of the other settings allowed when
configuring individual tunnels. Configuration options are specified on
the [I2CP page]().

### Comprimentos e padrões do túnel {#length}

[Na página de visão geral do
túnel](#length).

### Estratégia e prioridade de construção antecipatória {#strategy}

Construir túneis é caro, e os túneis têm um tempo fixo de expiração após
serem construídos. No entanto, quando uma piscina fica sem túneis, o
Destino está essencialmente morto. Além disso, a taxa de sucesso da
construção de túneis pode variar muito, tanto com condições locais
quanto globais da rede. Portanto, é importante manter uma estratégia de
construção antecipatória e adaptativa para garantir que novos túneis
sejam construídos com sucesso antes que sejam necessários, sendo
cuidadoso para não construir um excesso de túneis, construí-los muito
cedo, ou consumir muito CPU ou largura de banda criando e enviando as
mensagens de construção criptografadas.

Para cada tupla {exploratory/client, in/out, length, length variance} o
roteador mantém estatísticas sobre o tempo necessário para uma
construção de túnel bem-sucedida. Usando essas estatísticas, ele calcula
quanto tempo antes da expiração de um túnel ele deve começar a tentar
construir uma substituição. À medida que o tempo de expiração se
aproxima sem uma substituição bem-sucedida, ele inicia várias tentativas
de construção em paralelo e, então, aumentará o número de tentativas
paralelas, se necessário.

Para limitar a largura de banda e o uso da CPU, o roteador também limita
o número máximo de tentativas de compilação pendentes em todos os pools.
As compilações críticas (aquelas para túneis exploratórios e para pools
que ficaram sem túneis) são priorizadas.

## Limitação de mensagens de túnel {#tunnel.throttling}

Embora os túneis dentro do I2P tenham semelhança com uma rede de
comutação de circuitos , tudo dentro do I2P é estritamente baseado em
mensagens - os túneis são meramente truques de contabilidade para ajudar
a organizar a entrega de mensagens. Nenhuma suposição é feita em relação
à confiabilidade ou ordenação de mensagens, e as retransmissões são
deixadas para níveis mais altos (por exemplo, a biblioteca de streaming
da camada cliente do I2P). Isso permite que o I2P aproveite as técnicas
de limitação disponíveis para redes de comutação de pacotes e de
circuitos. Por exemplo, cada roteador pode manter o controle da média
móvel de quantos dados cada túnel está usando, combinar isso com todas
as médias usadas por outros túneis dos quais o roteador está
participando e ser capaz de aceitar ou rejeitar solicitações adicionais
de participação no túnel com base em sua capacidade e utilização. Por
outro lado, cada roteador pode simplesmente descartar mensagens que
estão além de sua capacidade, explorando a pesquisa usada na Internet
normal.

Na implementação atual, os roteadores implementam uma estratégia de
descarte antecipado aleatório ponderado (WRED) . Para todos os
roteadores participantes (participante interno, gateway de entrada e
ponto de extremidade de saída), o roteador começará a descartar
aleatoriamente uma parte das mensagens conforme os limites de largura de
banda forem atingidos. Conforme o tráfego se aproxima ou excede os
limites, mais mensagens são descartadas. Para um participante interno,
todas as mensagens são fragmentadas e preenchidas e, portanto, têm o
mesmo tamanho. No gateway de entrada e no ponto de extremidade de saída,
no entanto, a decisão de descarte é tomada na mensagem completa
(coalescida), e o tamanho da mensagem é levado em consideração.
Mensagens maiores têm maior probabilidade de serem descartadas. Além
disso, é mais provável que as mensagens sejam descartadas no ponto de
extremidade de saída do que no gateway de entrada, pois essas mensagens
não estão tão \"avançadas\" em sua jornada e, portanto, o custo de rede
de descartar essas mensagens é menor.

## Trabalho futuro {#future}

### Mistura/dosagem {#tunnel.mixing}

Quais estratégias poderiam ser usadas no gateway e em cada salto para
atrasar, reordenar, redirecionar ou preencher mensagens? Até que ponto
isso deve ser feito automaticamente, quanto deve ser configurado como
uma configuração por túnel ou por salto, e como o criador do túnel (e,
por sua vez, o usuário) deve controlar essa operação? Tudo isso é
deixado como desconhecido, a ser trabalhado para uma versão futura
distante.

### Acolchoamento

As estratégias de preenchimento podem ser usadas em vários níveis,
abordando a exposição de informações de tamanho de mensagem para
diferentes adversários. O tamanho atual da mensagem de túnel fixo é de
1024 bytes. Dentro disso, no entanto, as mensagens fragmentadas em si
não são preenchidas pelo túnel, embora para mensagens de ponta a ponta ,
elas possam ser preenchidas como parte do envoltório de alho.

### WRED

As estratégias WRED têm um impacto significativo no desempenho de ponta
a ponta, e na prevenção do colapso do congestionamento da rede. A
estratégia WRED atual deve ser cuidadosamente avaliada e aprimorada.


