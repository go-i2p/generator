 UDP seguro
semiconfiável (SSU) 2025-01 0.9.64 

**DEPRECATED** - SSU has been replaced by SSU2. SSU support was removed
from i2pd in release 2.44.0 (API 0.9.56) 2022-11. SSU support was
removed from Java I2P in release 2.4.0 (API 0.9.61) 2023-12.

SSU (also called \"UDP\" in much of the I2P documentation and user
interfaces) was one of two [transports]()
implemented in I2P. The other is [NTCP2]().
Support for [NTCP]() has been removed.

O SSU foi introduzido na versão 0.6 do I2P. Em uma instalação I2P
padrão, o roteador usa NTCP e SSU para conexões de saída. O SSU sobre
IPv6 é suportado a partir da versão 0.9.8.

O SSU é chamado de \"semiconfiável\" porque ele retransmite
repetidamente mensagens não confirmadas, mas apenas até um número máximo
de vezes. Depois disso, a mensagem é descartada.

## Serviços SSU

Assim como o transporte NTCP, o SSU fornece transporte de dados ponto a
ponto, confiável, criptografado e orientado à conexão. Exclusivo do SSU,
ele também fornece serviços de detecção de IP e travessia de NAT,
incluindo:

- Travessia cooperativa de NAT/Firewall usando
 [introdutores](#introduction)
- Detecção de IP local por inspeção de pacotes de entrada e [teste de
 pares](#peerTesting)
- Comunicação do status do firewall e IP local, e alterações para NTCP
- Comunicação do status do firewall e do IP local, e alterações em
 ambos, no roteador e na interface do usuário

## [Especificação do Endereço do Roteador]{#ra}

As propriedades a seguir são armazenadas no banco de dados da rede.

**Transport name:** SSU

**caps:** \[B,C,4,6\] [See below](#capabilities).

**host:** IP (IPv4 or IPv6). Shortened IPv6 address (with \"::\") is
allowed. May or may not be present if firewalled. Host names were
previously allowed, but are deprecated as of release 0.9.32. See
proposal 141.

**iexp\[0-2\]:** Expiration of this introducer. ASCII digits, in seconds
since the epoch. Only present if firewalled, and introducers are
required. Optional (even if other properties for this introducer are
present). As of release 0.9.30, proposal 133.

**ihost\[0-2\]:** Introducer\'s IP (IPv4 or IPv6). Host names were
previously allowed, but are deprecated as of release 0.9.32. See
proposal 141. Shortened IPv6 address (with \"::\") is allowed. Only
present if firewalled, and introducers are required.

A necessidade do SSU por apenas entrega semiconfiável, operação amigável
ao TCP, e a capacidade para alto rendimento permite uma grande latitude
no controle de congestionamento . O algoritmo de controle de
congestionamento descrito abaixo é destinado a ser eficiente em largura
de banda e também simples de implementar.

Os pacotes são agendados de acordo com a política do roteador, tomando
cuidado para não exceder a capacidade de saída do roteador ou exceder a
capacidade medida de do peer remoto. A capacidade medida opera ao longo
das linhas de início lento do TCP e prevenção de congestionamento, com
aumentos aditivos de para a capacidade de envio e diminuições
multiplicativas em face do congestionamento. Ao contrário do TCP, os
roteadores podem desistir de algumas mensagens após um determinado
período ou número de retransmissões enquanto continuam a transmitir
outras mensagens.

As técnicas de detecção de congestionamento também variam do TCP, já que
cada mensagem tem seu próprio identificador único e não sequencial, e
cada mensagem tem um tamanho limitado - no máximo, 32 KB. Para
transmitir esse feedback de forma eficiente para o remetente, o receptor
inclui periodicamente uma lista de identificadores de mensagem
totalmente ACKed e também pode incluir campos de bits para mensagens
parcialmente recebidas, onde cada bit representa a recepção de um
fragmento. Se fragmentos duplicados chegarem, a mensagem deve ser ACKed
novamente, ou se a mensagem ainda não tiver sido totalmente recebida, o
campo de bits deve ser retransmitido com quaisquer novas atualizações.

A implementação atual não preenche os pacotes com nenhum tamanho
específico, mas apenas coloca um único fragmento de mensagem em um
pacote e o envia (cuidado para não exceder o MTU).

### [MTU]{#mtu}

A partir da versão 0.8.12 do roteador, dois valores de MTU são usados
para IPv4: 620 e 1484. O valor de MTU é ajustado com base na porcentagem
de pacotes que são retransmitidos.

Para ambos os valores de MTU, é desejável que (MTU % 16) == 12, de modo
que a porção de carga útil após o cabeçalho IP/UDP de 28 bytes seja um
múltiplo de 16 bytes, para fins de criptografia.

Para um valor de MTU pequeno, é desejável empacotar uma Mensagem de
Construção de Túnel Variável de 2646 bytes de forma eficiente em vários
pacotes; com uma MTU de 620 bytes, ela cabe perfeitamente em 5 pacotes.

Com base nas medições, 1492 acomoda quase todas as mensagens I2NP
razoavelmente pequenas (mensagens I2NP maiores podem ter de 1900 a 4500
bytes, o que não acomodaria em uma MTU de rede ativa de qualquer
maneira).

Os valores de MTU foram 608 e 1492 para as versões 0.8.9 - 0.8.11. A MTU
grande era 1350 antes da versão 0.8.9.

O tamanho máximo do pacote de recebimento é de 1571 bytes a partir da
versão 0.8.12. Para as versões 0.8.9 - 0.8.11, era de 1535 bytes. Antes
da versão 0.8.9, era de 2048 bytes.

A partir da versão 0.9.2, se a MTU da interface de rede de um roteador
for menor que 1484, ele publicará isso no banco de dados da rede, e
outros roteadores deverão respeitar isso quando uma conexão for
estabelecida.

Para IPv6, a MTU mínima é 1280. O cabeçalho IPv6 IP/UDP tem 48 bytes,
então usamos uma MTU onde (MTN % 16 == 0), o que é verdadeiro para 1280.
A MTU máxima do IPv6 é 1488. (o máximo era 1472 antes da versão 0.9.28).

### [Limites do Tamanho da Mensagem]{#max}

Embora o tamanho máximo da mensagem seja nominalmente 32 KB, o limite
prático é diferente. O protocolo limita o número de fragmentos a 7 bits,
ou 128. A implementação atual, no entanto, limita cada mensagem a um
máximo de 64 fragmentos, o que é suficiente para 64 \* 534 = 33,3 KB ao
usar a MTU 608. Devido à sobrecarga para LeaseSets e chaves de sessão
agrupados, o limite prático no nível do aplicativo é cerca de 6 KB
menor, ou cerca de 26 KB. Mais trabalho é necessário para aumentar o
limite de transporte UDP acima de 32 KB. Para conexões usando a MTU
maior, mensagens maiores são possíveis.

## Tempo limite ocioso

O tempo limite de inatividade e o fechamento da conexão ficam a critério
de cada ponto de extremidade e podem variar. A implementação atual
diminui o tempo limite à medida que o número de conexões se aproxima do
máximo configurado e aumenta o tempo limite quando a contagem de
conexões é baixa. O tempo limite mínimo recomendado é de dois minutos ou
mais, e o tempo limite máximo recomendado é de dez minutos ou mais.

## [Chaves]{#keys}

Toda a criptografia usada é AES256/CBC com chaves de 32 bytes e IVs de
16 bytes. Quando Alice origina uma sessão com Bob, as chaves MAC e de
sessão são negociadas como parte da troca DH e são então usadas para o
HMAC e criptografia, respectivamente. Durante a troca DH, a introKey
publicamente conhecida de Bob é usada para o MAC e criptografia.

Tanto a mensagem inicial quanto a resposta subsequente usam a introKey
do respondente (Bob) - o respondente não precisa saber a introKey do
solicitante (Alice). A chave de assinatura DSA usada por Bob já deve ser
conhecida por Alice quando ela o contata, embora a chave DSA de Alice
possa não ser conhecida por Bob.

Ao receber uma mensagem, o receptor verifica o endereço IP \"de\" e a
porta com todas as sessões estabelecidas - se houver correspondências,
as chaves MAC dessa sessão são testadas no HMAC. Se nenhuma delas
verificar ou se não houver endereços IP correspondentes, o receptor
tenta sua introKey no MAC. Se isso não verificar, o pacote é descartado.
Se verificar, ele é interpretado de acordo com o tipo de mensagem,
embora se o receptor estiver sobrecarregado, ele pode ser descartado de
qualquer maneira.

Se Alice e Bob tiverem uma sessão estabelecida, mas Alice perder as
chaves por algum motivo e quiser contatar Bob, ela pode a qualquer
momento simplesmente estabelecer uma nova sessão por meio do
SessionRequest e mensagens relacionadas. Se Bob perdeu a chave, mas
Alice não sabe disso, ela primeiro tentará incitá-lo a responder,
enviando uma DataMessage com o sinalizador wantReply definido, e se Bob
continuamente falhar em responder, ela assumirá que a chave está perdida
e restabelecerá uma nova.

For the DH key agreement, [RFC3526]() 2048bit
MODP group (#14) is used:

 p = 2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
 g = 2

These are the same p and g used for I2P\'s [ElGamal
encryption](#elgamal).

## [Prevenção de repetição]{#replay}

A prevenção de repetição na camada SSU ocorre pela rejeição de pacotes
com timestamps excessivamente antigos ou aqueles que reutilizam um IV.
Para detectar IVs duplicados, uma sequência de filtros Bloom é empregada
para \"decair\" periodicamente para que apenas IVs adicionados
recentemente sejam detectados.

Os messageIds usados em DataMessages são definidos em camadas acima de o
transporte SSU e são passados transparentemente. Esses IDs não estão em
nenhuma ordem específica - na verdade, eles provavelmente são
inteiramente aleatórios. A camada SSU não faz nenhuma tentativa de
messageId prevenção de repetição - camadas mais altas devem levar isso
em consideração.

## Endereçamento {#addressing}

Para entrar em contato com um peer SSU, um dos dois conjuntos de
informações é necessário: um endereço direto, para quando o peer estiver
publicamente acessível, ou um endereço indireto, para usar um terceiro
para apresentar o peer. Não há restrição quanto ao número de endereços
que um peer pode ter.

 Direct: host, port, introKey, options Indirect: tag,
relayhost, port, relayIntroKey, targetIntroKey, options 

Cada um dos endereços também pode expor uma série de opções -
capacidades especiais daquele peer em particular. Para uma lista de
capacidades disponíveis, veja [abaixo](#capabilities).

The addresses, options, and capabilities are published in the [network
database]().

## [Estabelecimento de Sessão Direta]{#direct}

O estabelecimento de sessão direta é usado quando nenhum terceiro é
necessário para a travessia do NAT. A sequência de mensagens é a
seguinte:

### [Estabelecimento de conexão (direto)]{#establishDirect}

Alice conecta diretamente ao Bob. IPv6 é suportado desde a versão 0.9.8.

 Alice Bob SessionRequest
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-- SessionCreated
SessionConfirmed \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-- DeliveryStatusMessage
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-- DatabaseStoreMessage
DatabaseStoreMessage \-\-\-\-\-\-\-\-\-\-\-\-\-\--\> Data
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\> Data 

After the SessionConfirmed message is received, Bob sends a small
[DeliveryStatus message](#msg_DeliveryStatus)
as a confirmation. In this message, the 4-byte message ID is set to a
random number, and the 8-byte \"arrival time\" is set to the current
network-wide ID, which is 2 (i.e. 0x0000000000000002).

After the status message is sent, the peers usually exchange
[DatabaseStore messages](#msg_DatabaseStore)
containing their
[RouterInfos](#struct_RouterInfo),
however, this is not required.

Não parece que o tipo da mensagem de status ou seu conteúdo importem.
Ela foi adicionada originalmente porque a mensagem DatabaseStore estava
atrasada vários segundos; como o armazenamento agora é enviado
imediatamente, talvez a mensagem de status possa ser eliminada.

## [Introdução]{#introduction}

As chaves de introdução são entregues por meio de um canal externo (o
banco de dados da rede), onde tradicionalmente são idênticas ao Hash do
roteador até a versão 0.9.47, mas podem ser aleatórias a partir da
versão 0.9.48. Elas devem ser usadas ao estabelecer uma chave de sessão.
Para o endereço indireto , o peer deve primeiro entrar em contato com o
relayhost e pedir a eles uma introdução ao peer conhecido naquele
relayhost sob a tag fornecida. Se possível, o relayhost envia uma
mensagem ao peer endereçado dizendo para entrar em contato com o peer
solicitante e também fornece ao peer solicitante o IP e a porta em que o
peer endereçado está localizado. Além disso, o par que estabelece a
conexão deve já conhecer as chaves públicas do par ao qual está se
conectando (mas não é necessário para nenhum par de retransmissão
intermediário).

O estabelecimento indireto de sessão por meio de uma introdução de
terceiros é necessário para uma travessia NAT eficiente. Charlie, um
roteador atrás de um NAT ou firewall que não permite pacotes UDP de
entrada não solicitados, primeiro contata alguns pares, escolhendo
alguns para servir como apresentadores. Cada desses pares (Bob, Bill,
Betty, etc) fornece a Charlie uma tag de introdução - um número
aleatório de 4 bytes - que ele então disponibiliza ao público como
métodos de contato com ele. Alice, uma roteadora que tem os métodos de
contato publicados de Charlie, primeiro envia um pacote RelayRequest
para um ou mais dos apresentadores, pedindo a cada um para apresentá-la
a Charlie (oferecendo a tag de introdução para identificar Charlie). Bob
então encaminha um pacote RelayIntro para Charlie incluindo o IP público
e o número da porta de Alice, então envia Alice de volta um pacote
RelayResponse contendo o IP público e o número da porta de Charlie.
Quando Charlie recebe o pacote RelayIntro, ele envia um pequeno pacote
aleatório para o IP e porta de Alice (abrindo um buraco em seu
NAT/firewall), e quando Alice recebe o pacote RelayResponse de Bob, ela
inicia um novo estabelecimento de sessão de direção completa com o IP e
porta especificados.

### [Estabelecimento de conexão (indireto usando um introdutor)]{#establishIndirect}

Alice primeiro se conecta com o apresentador Bob, que repassa o pedido a
Charlie.

 Alice Bob Charlie RelayRequest
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-- RelayResponse RelayIntro
\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
HolePunch (data ignored) SessionRequest
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
SessionCreated SessionConfirmed
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
DeliveryStatusMessage
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
DatabaseStoreMessage DatabaseStoreMessage
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
Data
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
Data 

Após o furador, a sessão é estabelecida entre Alice e Charlie como em um
estabelecimento direto.

### IPv6 Notes

IPv6 is supported as of version 0.9.8. Published relay addresses may be
IPv4 or IPv6, and Alice-Bob communication may be via IPv4 or IPv6.
Through release 0.9.49, Bob-Charlie and Alice-Charlie communication is
via IPv4 only. Relaying for IPv6 is supported as of release 0.9.50. See
the specification for details.

While the specification was changed as of version 0.9.8, Alice-Bob
communication via IPv6 was not actually supported until version 0.9.50.
Earlier versions of Java routers erroneously published the \'C\'
capability for IPv6 addresses, even though they did not actually act as
an introducer via IPv6. Therefore, routers should only trust the \'C\'
capability on an IPv6 address if the router version is 0.9.50 or higher.

## [Testando o Par]{#peerTesting}

A automação de testes de alcançabilidade colaborativa para pares é
habilitada por uma sequência de mensagens PeerTest. Com sua execução
adequada, um par será capaz de determinar sua própria alcançabilidade e
pode atualizar seu comportamento de acordo. O processo de teste é bem
simples:

 Alice Bob Charlie PeerTest
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
PeerTest\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--PeerTest
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--PeerTest
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--PeerTest
PeerTest\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--PeerTest


Cada uma das mensagens PeerTest carrega um nonce identificando a própria
série de testes , conforme inicializada por Alice. Se Alice não receber
uma mensagem específica que ela espera, ela retransmitirá adequadamente,
e com base nos dados recebidos ou nas mensagens ausentes, ela saberá sua
alcançabilidade. Os vários estados finais que podem ser alcançados são
os seguintes:

- Se ela não receber uma resposta de Bob, ela retransmitirá até um
 certo número de vezes, mas se nenhuma resposta chegar, ela saberá
 que seu firewall ou NAT está de alguma forma mal configurado,
 rejeitando todos os pacotes UDP de entrada, mesmo em resposta direta
 a um pacote de saída. Alternativamente, Bob pode estar inativo ou
 incapaz de fazer Charlie responder.
- Se Alice não receber uma mensagem PeerTest com o nonce esperado de
 um terceiro (Charlie), ela retransmitirá sua solicitação inicial
 para Bob até um certo número de vezes, mesmo se ela já tiver
 recebido a resposta de Bob. Se a primeira mensagem de Charlie ainda
 não for enviada, mas a de Bob for, ela sabe que está atrás de um NAT
 ou firewall que está rejeitando tentativas de conexão não
 solicitadas e que o encaminhamento de porta não está operando
 corretamente (o IP e a porta que Bob ofereceu devem ser
 encaminhados).
- Se Alice receber a mensagem PeerTest de Bob e ambas as mensagens
 PeerTest de Charlie, mas os números de IP e porta incluídos nas
 mensagens de Bob e Charlie não corresponderem, ela sabe que está
 atrás de um NAT simétrico, reescrevendo todos os seus pacotes de
 saída com portas \'de\' diferentes para cada peer contatado. Ela
 precisará encaminhar explicitamente uma porta e sempre ter essa
 porta exposta para conectividade remota, ignorando a descoberta de
 portas posteriores.
- Se Alice receber a primeira mensagem de Charlie, mas não a segunda,
 ela retransmitirá sua mensagem PeerTest para Charlie até um certo
 número de vezes, mas se nenhuma resposta for recebida, ela saberá
 que Charlie está confuso ou não está mais online.

Alice deve escolher Bob arbitrariamente entre pares conhecidos que
parecem ser capazes de participar de testes de pares. Bob, por sua vez,
deve escolher Charlie arbitrariamente entre pares que ele conhece que
parecem ser capazes de participar de testes de pares e que estão em um
IP diferente de Bob e Alice. Se a primeira condição de erro ocorrer
(Alice não recebe mensagens PeerTest de Bob), Alice pode decidir
designar um novo par como Bob e tentar novamente com um nonce diferente.

A chave de introdução de Alice está incluída em todas as mensagens do
PeerTest para que Charlie possa contatá-la sem saber nenhuma informação
adicional. A partir da versão 0.9.15, Alice deve ter uma sessão
estabelecida com Bob, para evitar ataques de falsificação. Alice não
deve ter uma sessão estabelecida com Charlie para que o teste de pares
seja válido. Alice pode estabelecer uma sessão com Charlie, mas isso não
é obrigatório.

### IPv6 Notes

Through release 0.9.26, only testing of IPv4 addresses is supported.
Only testing of IPv4 addresses is supported. Therefore, all Alice-Bob
and Alice-Charlie communication must be via IPv4. Bob-Charlie
communication, however, may be via IPv4 or IPv6. Alice\'s address, when
specified in the PeerTest message, must be 4 bytes. As of release
0.9.27, testing of IPv6 addresses is supported, and Alice-Bob and
Alice-Charlie communication may be via IPv6, if Bob and Charlie indicate
support with a \'B\' capability in their published IPv6 address. See
[Proposal 126](/spec/proposals/126-ipv6-peer-testing) for details.

Prior to release 0.9.50, Alice sends the request to Bob using an
existing session over the transport (IPv4 or IPv6) that she wishes to
test. When Bob receives a request from Alice via IPv4, Bob must select a
Charlie that advertises an IPv4 address. When Bob receives a request
from Alice via IPv6, Bob must select a Charlie that advertises an IPv6
address. The actual Bob-Charlie communication may be via IPv4 or IPv6
(i.e., independent of Alice\'s address type).

As of release 0.9.50, If the message is over IPv6 for an IPv4 peer test,
or (as of release 0.9.50) over IPv4 for an IPv6 peer test, Alice must
include her introduction address and port. See [Proposal
158](/spec/proposals/158) for details.

## [Janela de transmissão, ACKs e retransmissões]{#acks}

The DATA message may contain ACKs of full messages and partial ACKs of
individual fragments of a message. See the data message section of [the
protocol specification page]() for details.

The details of windowing, ACK, and retransmission strategies are not
specified here. See the Java code for the current implementation. During
the establishment phase, and for peer testing, routers should implement
exponential backoff for retransmission. For an established connection,
routers should implement an adjustable transmission window, RTT estimate
and timeout, similar to TCP or [streaming]().
See the code for initial, min and max parameters.

## [Segurança]{#security}

Endereços de origem UDP podem, é claro, ser falsificados. Além disso, os
IPs e portas contidos em mensagens SSU específicas (RelayRequest,
RelayResponse, RelayIntro, PeerTest) podem não ser legítimos. Além
disso, certas ações e respostas podem precisar de limitação de taxa.

Os detalhes da validação não são especificados aqui. Os implementadores
devem adicionar defesas quando apropriado.

## [Capacidades do Par]{#capabilities}

One or more capabilities may be published in the \"caps\" option.
Capabilities may be in any order, but \"BC46\" is the recommended order,
for consistency across implementations.

B
: Se o endereço do par contiver a capacidade \'B\', isso significa que
 eles estão dispostos e são capazes de participar de testes de pares
 como um \'Bob\' ou \'Charlie\'. Through 0.9.26, peer testing was not
 supported for IPv6 addresses, and the \'B\' capability, if present
 for an IPv6 address, must be ignored. As of 0.9.27, peer testing is
 supported for IPv6 addresses, and the presence or absense of the
 \'B\' capability in an IPv6 address indicates actual support (or
 lack of support).

C
: If the peer address contains the \'C\' capability, that means they
 are willing and able to serve as an introducer via that address -
 serving as an introducer Bob for an otherwise unreachable Charlie.
 Prior to release 0.9.50, Java routers incorrectly published the
 \'C\' capability for IPv6 addresses, even though IPv6 introducers
 was not fully implemented. Therefore, routers should assume that
 versions prior to 0.9.50 cannot act as an introducer over IPv6, even
 if the \'C\' capability is advertised.

4
: As of 0.9.50, indicates outbound IPv4 capability. If an IP is
 published in the host field, this capability is not necessary. If
 this is an address with introducers for IPv4 introductions, \'4\'
 should be included. If the router is hidden, \'4\' and \'6\' may be
 combined in a single address.

6
: As of 0.9.50, indicates outbound IPv6 capability. If an IP is
 published in the host field, this capability is not necessary. If
 this is an address with introducers for IPv6 introductions, \'6\'
 should be included (not currently supported). If the router is
 hidden, \'4\' and \'6\' may be combined in a single address.

# [Trabalho futuro]{#future}

Note: These issues will be addressed in the development of SSU2.

- A análise do desempenho atual do SSU, incluindo a avaliação do
 ajuste do tamanho da janela e outros parâmetros, e o ajuste da
 implementação do protocolo para melhorar o desempenho , é um tópico
 para trabalho futuro.
- A implementação atual envia repetidamente confirmações para os
 mesmos pacotes, o que aumenta desnecessariamente a sobrecarga.
- O valor padrão de MTU pequeno de 620 deve ser analisado e
 possivelmente aumentado. A estratégia atual de ajuste de MTU deve
 ser avaliada. Um pacote de 1730 bytes de streaming lib cabe em 3
 pacotes SSU pequenos? Provavelmente não.
- O protocolo deve ser estendido para trocar MTUs durante a
 configuração.
- A recodificação não está implementada no momento e nunca estará.
- O uso potencial dos campos \'challenge\' em RelayIntro e
 RelayResponse, e o uso do campo padding em SessionRequest e
 SessionCreated, não são documentados.
- Um conjunto de tamanhos de pacotes fixos pode ser apropriado para
 ocultar ainda mais a fragmentação de dados para adversários
 externos, mas o túnel, o alho e o preenchimento de ponta a ponta
 devem ser suficientes para a maioria das necessidades até então.
- Os horários de login em SessionCreated e SessionConfirmed parecem
 não ser utilizados ou não foram verificados.

# Diagrama de Implementação

Este diagrama deve refletir com precisão a implementação atual, no
entanto pode haver pequenas diferenças.

![](images/udp.png)

# [Especificação]{#spec}

[Agora na página de especificações do
SSU](). 
