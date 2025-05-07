 Protocolo de
streaming 2024-09 0.9.64 

## Visão geral

The streaming library is technically part of the \"application\" layer,
as it is not a core router function. In practice, however, it provides a
vital function for almost all existing I2P applications, by providing a
TCP-like streams over I2P, and allowing existing apps to be easily
ported to I2P. The other end-to-end transport library for client
communication is the [datagram library]().

The streaming library is a layer on top of the core [I2CP
API]() that allows reliable, in-order, and
authenticated streams of messages to operate across an unreliable,
unordered, and unauthenticated message layer. Just like the TCP to IP
relationship, this streaming functionality has a whole series of
tradeoffs and optimizations available, but rather than embed that
functionality into the base I2P code, it has been factored off into its
own library both to keep the TCP-esque complexities separate and to
allow alternative optimized implementations.

Considerando o custo relativamente alto das mensagens, o protocolo da
biblioteca de streaming para agendamento e entrega dessas mensagens foi
otimizado para permitir que mensagens individuais passadas contenham o
máximo de informações disponíveis. Por exemplo, uma pequena transação
HTTP com proxy através da biblioteca de streaming pode ser concluída em
uma única viagem de ida e volta - as primeiras mensagens agrupam um SYN,
FIN e a pequena carga útil da solicitação HTTP, e a resposta agrupa o
SYN, FIN, ACK e a carga útil da resposta HTTP. Enquanto um ACK adicional
deve ser transmitido para informar ao servidor HTTP que o SYN/FIN/ACK
foi recebido, o proxy HTTP local pode frequentemente entregar a resposta
completa ao navegador imediatamente.

A biblioteca de streaming tem muita semelhança com uma abstração do TCP,
com suas janelas deslizantes, algoritmos de controle de congestionamento
(início lento e prevenção de congestionamento) e comportamento geral dos
pacotes (ACK, SYN, FIN, RST, cálculo de rto, etc.).

A biblioteca de streaming é uma biblioteca robusta que é otimizada para
operação sobre I2P. Ela tem uma configuração de uma fase e contém uma
implementação de janela completa.

## API

The streaming library API provides a standard socket paradigm to Java
applications. The lower-level [I2CP]() API is
completely hidden, except that applications may pass [I2CP
parameters](#options) through the streaming
library, to be interpreted by I2CP.

The standard interface to the streaming lib is for the application to
use the [I2PSocketManagerFactory]() to create
an [I2PSocketManager](). The application then
asks the socket manager for an [I2PSession](),
which will cause a connection to the router via
[I2CP](). The application can then setup
connections with an [I2PSocket]() or receive
connections with an [I2PServerSocket]().

Here are the [full streaming library Javadocs]().

Para um bom exemplo de uso, olhe o código do i2psnark.

### Opções e Padrões {#options}

The options and current default values are listed below. Options are
case-sensitive and may be set for the whole router, for a particular
client, or for an individual socket on a per-connection basis. Many
values are tuned for HTTP performance over typical I2P conditions. Other
applications such as peer-to-peer services are strongly encouraged to
modify as necessary, by setting the options and passing them via the
call to
[I2PSocketManagerFactory]().createManager(\_i2cpHost,
\_i2cpPort, opts). Time values are in ms.

Note that higher-layer APIs, such as [SAM](),
[BOB](), and
[I2PTunnel](), may override these defaults
with their own defaults. Also note that many options only apply to
servers listening for incoming connections.

A partir da versão 0.9.1, a maioria, mas não todas, as opções podem ser
alteradas em um gerenciador de soquete ou sessão ativa. Veja os javadocs
para mais detalhes.

 Option Default Notes
 --------------------------------------------------- ------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 i2cp.accessList null Lista separada por vírgulas ou espaços de hashes de pares Base64 usados para lista de acesso ou lista negra. As of release .
 i2cp.destination.sigType DSA_SHA1 Use a lista de acesso como uma lista de permissões para conexões de entrada. O nome ou número do tipo de assinatura para um destino temporário. As of release .
 i2cp.enableAccessList false Use a lista de acesso como uma lista de permissões para conexões de entrada. As of release .
 i2cp.enableBlackList false Use a lista de acesso como uma lista negra para conexões de entrada. As of release .
 i2p.streaming.answerPings true Se deve responder a pings recebidos
 i2p.streaming.blacklist null Lista separada por vírgula ou espaço de hashes de pares Base64 a serem colocados na lista negra para conexões de entrada para TODOS os destinos no contexto. Esta opção deve ser definida nas propriedades do contexto, NÃO no argumento de opções createManager(). Observe que definir isso no contexto do roteador não afetará clientes fora do roteador em uma JVM e contexto separados. As of release .
 i2p.streaming.bufferSize 64K Quantos dados de transmissão (em bytes) serão aceitos e ainda não foram gravados.
 i2p.streaming.congestionAvoidanceGrowthRateFactor 1 Quando estamos em prevenção de congestionamento, aumentamos o tamanho da janela na taxa de `1/(windowSize*factor)`. No TCP padrão, os tamanhos das janelas estão em bytes, enquanto no I2P, os tamanhos das janelas estão em mensagens. Um número maior significa crescimento mais lento.
 i2p.streaming.connectDelay -1 Quanto tempo esperar após instanciar um novo con antes de realmente tentar conectar. Se for \<= 0, conecte imediatamente sem dados iniciais. Se for maior que 0, espere até que o fluxo de saída seja liberado, o buffer seja preenchido, ou tantos milissegundos passem, e inclua quaisquer dados iniciais com o SYN.
 i2p.streaming.connectTimeout 5\*60\*1000 Quanto tempo bloquear na conexão, em milissegundos. Negativo significa indefinidamente. O padrão é 5 minutos.
 i2p.streaming.disableRejectLogging false Se deseja desabilitar avisos nos logs quando uma conexão de entrada é rejeitada devido aos limites de conexão. As of release .
 i2p.streaming.dsalist null Lista separada por vírgula ou espaço de Hashes de pares Base64 ou nomes de host a serem contatados usando um destino DSA alternativo. Aplica-se somente se a multissessão estiver habilitada e a sessão primária não for DSA (geralmente somente para clientes compartilhados). Esta opção deve ser definida nas propriedades de contexto, NÃO no argumento de opções createManager(). Observe que definir isso no contexto do roteador não afetará clientes fora do roteador em uma JVM e contexto separados. As of release .
 i2p.streaming.enforceProtocol true Se deve escutar somente o protocolo de streaming. Definir como true proibirá a comunicação com Destinos anteriores à versão 0.7.1 (lançada em março de 2009). Defina como true se estiver executando vários protocolos neste Destino. As of release . Default true as of release 0.9.36.
 i2p.streaming.inactivityAction 2 (send) (0=noop, 1=desconectar) O que fazer em um tempo limite de inatividade - não fazer nada, desconectar ou enviar uma confirmação duplicada.
 i2p.streaming.inactivityTimeout 90\*1000 Tempo ocioso antes de enviar um keepalive
 i2p.streaming.initialAckDelay 750 Atraso antes de enviar um ack
 i2p.streaming.initialResendDelay 1000 O valor inicial do campo de atraso de reenvio no cabeçalho do pacote, vezes 1000. Não totalmente implementado; veja abaixo.
 i2p.streaming.initialRTO 9000 Tempo limite inicial (se nenhum [compartilhamento de dados](#sharing) estiver disponível). As of release .
 i2p.streaming.initialRTT 8000 Estimativa inicial de tempo de ida e volta (se nenhum [compartilhamento de dados](#sharing) estiver disponível). Desativado a partir da versão 0.9.8; usa RTT real.
 i2p.streaming.initialWindowSize 6 (Se nenhum [dado de compartilhamento](#sharing) disponível) No TCP padrão, os tamanhos das janelas estão em bytes, enquanto no I2P, os tamanhos das janelas estão em mensagens.
 i2p.streaming.limitAction reset What action to take when an incoming connection exceeds limits. Valid values are: reset (reset the connection); drop (drop the connection); or http (send a hardcoded HTTP 429 response). Any other value is a custom response to be sent. backslash-r and backslash-n will be replaced with CR and LF. As of release .
 i2p.streaming.maxConcurrentStreams -1 (0 ou valor negativo significa ilimitado) Este é um limite total para entradas e saídas combinadas.
 i2p.streaming.maxConnsPerMinute 0 Limite de conexão de entrada (por par; 0 significa desabilitado) As of release .
 i2p.streaming.maxConnsPerHour 0 (por par; 0 significa desabilitado) As of release .
 i2p.streaming.maxConnsPerDay 0 (por par; 0 significa desabilitado) As of release .
 i2p.streaming.maxMessageSize 1730 O tamanho máximo da carga útil, ou seja, a MTU em bytes.
 i2p.streaming.maxResends 8 Número máximo de retransmissões antes da falha.
 i2p.streaming.maxTotalConnsPerMinute 0 Limite de conexão de entrada (todos os pares; 0 significa desabilitado) As of release .
 i2p.streaming.maxTotalConnsPerHour 0 (todos os pares; 0 significa desabilitado) Use com cuidado, pois exceder isso desabilitará o servidor por um longo tempo. As of release .
 i2p.streaming.maxTotalConnsPerDay 0 (todos os pares; 0 significa desabilitado) Use com cuidado, pois exceder isso desabilitará o servidor por um longo tempo. As of release .
 i2p.streaming.maxWindowSize 128 
 i2p.streaming.profile 1 (bulk) 1=bulk; 2=interactive; see important notes [below](#profile).
 i2p.streaming.readTimeout -1 Quanto tempo bloquear na leitura, em milissegundos. Negativo significa indefinidamente.
 i2p.streaming.slowStartGrowthRateFactor 1 Quando estamos em início lento, aumentamos o tamanho da janela na taxa de 1/(fator). No TCP padrão, os tamanhos das janelas estão em bytes, enquanto no I2P, os tamanhos das janelas estão em mensagens. Um número maior significa crescimento mais lento.
 i2p.streaming.tcbcache.rttDampening 0.75 Ref: RFC 2140. Valor de ponto flutuante. Pode ser definido somente por meio de propriedades de contexto, não de opções de conexão. As of release .
 i2p.streaming.tcbcache.rttdevDampening 0.75 Ref: RFC 2140. Valor de ponto flutuante. Pode ser definido somente por meio de propriedades de contexto, não de opções de conexão. As of release .
 i2p.streaming.tcbcache.wdwDampening 0.75 Ref: RFC 2140. Valor de ponto flutuante. Pode ser definido somente por meio de propriedades de contexto, não de opções de conexão. As of release .
 i2p.streaming.writeTimeout -1 Quanto tempo bloquear em write/flush, em milissegundos. Negativo significa indefinidamente.

## Especificação de Protocolo

[Ver a página da especificação da biblioteca de
streaming.]()

## Detalhes da implementação

### Configurações

O iniciador envia um pacote com o sinalizador SYNCHRONIZE definido. Este
pacote pode conter os dados iniciais também. O peer responde com um
pacote com o sinalizador SYNCHRONIZE definido. Este pacote pode conter
os dados de resposta inicial também.

O iniciador pode enviar pacotes de dados adicionais, até o tamanho da
janela inicial, antes de receber a resposta SYNCHRONIZE. Esses pacotes
também terão o campo ID do fluxo de envio definido como 0. Os
destinatários devem armazenar em buffer os pacotes recebidos em fluxos
desconhecidos por um curto período de tempo, pois eles podem chegar fora
de ordem, antes do pacote SYNCHRONIZE.

### Seleção e Negociação da MTU

O tamanho máximo da mensagem (também chamado de MTU / MRU) é negociado
para o menor valor suportado por os dois pares. Como as mensagens de
túnel são preenchidas para 1 KB, uma seleção de MTU ruim levará a uma
grande quantidade de sobrecarga. A MTU é especificada pela opção
i2p.streaming.maxMessageSize. A MTU padrão atual de 1730 foi escolhida
para caber precisamente em duas mensagens de túnel I2NP de 1K, incluindo
sobrecarga para o caso típico. Note: This is the maximum size of the
payload only, not including the header.

Note: For ECIES connections, which have reduced overhead, the
recommended MTU is 1812. The default MTU remains 1730 for all
connections, no matter what key type is used. Clients must use the
minimum of the sent and received MTU, as usual. See proposal 155.

A primeira mensagem em uma conexão inclui um Destino de 387 bytes
(típico) adicionado pela camada de streaming, e geralmente um LeaseSet
de 898 bytes (típico) e chaves de Sessão, agrupados na mensagem Garlic
pelo roteador. (O LeaseSet e as Chaves de Sessão não serão agrupados se
uma Sessão ElGamal tiver sido estabelecida anteriormente). Portanto, o
objetivo de encaixar uma solicitação HTTP completa em uma única mensagem
I2NP de 1 KB nem sempre é atingível. No entanto, a seleção da MTU,
juntamente com a implementação cuidadosa de estratégias de fragmentação
e de loteamento no processador de gateway de túnel, são fatores
importantes na largura de banda da rede, latência, confiabilidade e
eficiência, especialmente para conexões de longa duração.

### Integridade dos dados

Data integrity is assured by the gzip CRC-32 checksum implemented in
[the I2CP layer](#format). There is no checksum
field in the streaming protocol.

### Encapsulamento de pacotes

Each packet is sent through I2P as a single message (or as an individual
clove in a [Garlic Message]()). Message
encapsulation is implemented in the underlying
[I2CP](), [I2NP](), and
[tunnel message]() layers. There is no
packet delimiter mechanism or payload length field in the streaming
protocol.

### Atraso opcional

Pacotes de dados podem incluir um campo de atraso opcional especificando
o atraso solicitado, em ms, antes que o receptor reconheça o pacote. Os
valores válidos são de 0 a 60000, inclusive. Um valor de 0 solicita um
reconhecimento imediato. Isso é apenas consultivo, e os receptores devem
atrasar um pouco para que pacotes adicionais possam ser reconhecidos com
um único reconhecimento. Algumas implementações podem incluir um valor
consultivo de (RTT medido / 2) neste campo. Para valores de atraso
opcionais diferentes de zero, os receptores devem limitar o atraso
máximo antes de enviar um reconhecimento para alguns segundos, no
máximo. Valores de atraso opcionais maiores que 60000 indicam
estrangulamento, veja abaixo.

### Janela de recepção e asfixia

Os cabeçalhos TCP incluem a janela de recebimento em bytes. O protocolo
de streaming não contém uma janela de recebimento, ele usa apenas uma
indicação simples de choke/unchoke. Cada ponto final deve manter sua
própria estimativa da janela de recebimento do ponto final, em bytes ou
pacotes. O tamanho mínimo de buffer recomendado para implementações de
receptor é 128 pacotes ou 217 KB (aproximadamente 128x1730). Devido à
latência da rede I2P, quedas de pacotes e o controle de congestionamento
resultante, um buffer desse tamanho raramente é preenchido. No entanto,
é provável que ocorra estouro em conexões de \"loopback local\" (mesmo
roteador) de alta largura de banda.

Para indicar rapidamente e recuperar-se suavemente de condições de
estouro, há um mecanismo simples para pushback no protocolo de
streaming. Se um pacote for recebido com um campo de atraso opcional de
valor de 60001 ou superior, isso indica \"estrangulamento\" ou uma
janela de recebimento de zero. Um pacote com um campo de atraso opcional
de valor de 60000 ou menos indica \"desestrangulamento\". Pacotes sem um
campo de atraso opcional não afetam o estado de
estrangulamento/desestrangulamento.

Após ser bloqueado, nenhum outro pacote com dados deve ser enviado até
que o transmissor seja desbloqueado, exceto para pacotes de dados de
\"sondagem\" ocasionais para compensar possíveis pacotes desbloqueados
perdidos. O ponto final bloqueado deve iniciar um \"temporizador de
persistência\" para controlar a sondagem, como no TCP. O ponto final
desbloqueado deve enviar vários pacotes com este campo definido, ou
continuar enviando-os periodicamente até que os pacotes de dados sejam
recebidos novamente. O tempo máximo de espera para o desbloqueio depende
da implementação. O tamanho da janela do transmissor e a estratégia de
controle de congestionamento após ser desbloqueado dependem da
implementação.

### Controle de Congestionamento

A biblioteca de streaming usa fases padrão de início lento (crescimento
exponencial da janela) e prevenção de congestionamento (crescimento
linear da janela) , com recuo exponencial. O janelamento e as
confirmações usam a contagem de pacotes, não a contagem de bytes.

### Fechar

Qualquer pacote, incluindo um com o sinalizador SYNCHRONIZE definido,
pode ter o sinalizador CLOSE enviado também. A conexão não é fechada até
que o peer responda com o sinalizador CLOSE. Os pacotes CLOSE também
podem conter dados.

### Ping / Pong

Não há função ping na camada I2CP (equivalente ao eco ICMP) ou em
datagramas. Esta função é fornecida em streaming. Pings e pongs não
podem ser combinados com um pacote de streaming padrão; se a opção ECHO
estiver definida, então a maioria dos outros sinalizadores, opções,
ackThrough, sequenceNum, NACKs, etc. são ignorados.

Um pacote ping deve ter os sinalizadores ECHO, SIGNATURE_INCLUDED e
FROM_INCLUDED definidos. O sendStreamId deve ser maior que zero, e o
receiveStreamId é ignorado. O sendStreamId pode ou não corresponder a
uma conexão existente.

Um pacote pong deve ter o sinalizador ECHO definido. O sendStreamId deve
ser zero, e o receiveStreamId é o sendStreamId do ping. Antes da versão
0.9.18, o pacote pong não incluía nenhuma carga útil contida no ping.

A partir da versão 0.9.18, pings e pongs podem conter uma carga útil. A
carga útil no ping, até um máximo de 32 bytes, é retornada no pong.

O streaming pode ser configurado para desabilitar o envio de pongs com a
configuração i2p.streaming.answerPings=false.

### i2p.streaming.profile Notes {#profile}

This option supports two values; 1=bulk and 2=interactive. The option
provides a hint to the streaming library and/or router as to the traffic
pattern that is expected.

\"Bulk\" means to optimize for high bandwidth, possibly at the expense
of latency. This is the default. \"Interactive\" means to optimize for
low latency, possibly at the expense of bandwidth or efficiency.
Optimization strategies, if any, are implementation-dependent, and may
include changes outside of the streaming protocol.

Through API version 0.9.63, Java I2P would return an error for any value
other than 1 (bulk) and the tunnel would fail to start. As of API
0.9.64, Java I2P ignores the value. Through API version 0.9.63, i2pd
ignored this option; it is implemented in i2pd as of API 0.9.64.

While the streaming protocol includes a flag field to pass the profile
setting to the other end, this is not implemented in any known router.

### Compartilhamento de bloco de controle {#sharing}

A biblioteca de streaming suporta compartilhamento de bloco de controle
\"TCP\". Isso compartilha três parâmetros importantes da biblioteca de
streaming (tamanho da janela, tempo de ida e volta, variação do tempo de
ida e volta) entre conexões com o mesmo peer remoto. Isso é usado para
compartilhamento \"temporal\" no momento de abertura/fechamento da
conexão, não para compartilhamento de \"conjunto\" durante uma conexão
(consulte [RFC 2140](http://www.ietf.org/rfc/rfc2140.txt)). Há um
compartilhamento separado por ConnectionManager (ou seja, por destino
local) para que não haja vazamento de informações para outros destinos
no mesmo roteador. Os dados compartilhados para um determinado peer
expiram após alguns minutos. Os seguintes parâmetros de Compartilhamento
de Bloco de Controle podem ser definidos por roteador:

- RTT_DAMPENING = 0.75
- RTTDEV_DAMPENING = 0.75
- WINDOW_DAMPENING = 0.75

### Outros parâmetros {#other}

Os seguintes parâmetros são codificados, mas podem ser de interesse para
análise:

- MIN_RESEND_DELAY = 100 ms (minimum RTO)
- MAX_RESEND_DELAY = 45 sec (maximum RTO)
- MIN_WINDOW_SIZE = 1
- TREND_COUNT = 3
- MIN_MESSAGE_SIZE = 512 (minimum MTU)
- INBOUND_BUFFER_SIZE = maxMessageSize \* (maxWindowSize + 2)
- INITIAL_TIMEOUT (valid only before RTT is sampled) = 9 sec
- \"alpha\" ( RTT dampening factor as per RFC 6298 ) = 0.125
- \"beta\" ( RTTDEV dampening factor as per RFC 6298 ) = 0.25
- \"K\" ( RTDEV multiplier as per RFC 6298 ) = 4
- PASSIVE_FLUSH_DELAY = 175 ms
- Maximum RTT estimate: 60 sec

### Histórico

A biblioteca de streaming cresceu organicamente para I2P - primeiro mihi
implementou a \"mini biblioteca de streaming\" como parte do I2PTunnel,
que foi limitada a uma janela tamanho de 1 mensagem (exigindo um ACK
antes de enviar a próxima), e então foi refatorada em uma interface de
streaming genérica (espelhamento de soquetes TCP) e a implementação de
streaming completa foi implantada com um protocolo de janela deslizante
e otimizações para levar em conta o produto de alta largura de banda x
atraso. Os fluxos individuais podem ajustar o tamanho máximo do pacote e
outras opções. O tamanho de mensagem padrão é selecionado para caber
precisamente em duas mensagens de túnel I2NP de 1K, e é uma compensação
razoável entre os custos de largura de banda de retransmissão de
mensagens perdidas e a latência e sobrecarga de múltiplas mensagens.

## Trabalho futuro {#future}

O comportamento da biblioteca de streaming tem um impacto profundo no
desempenho do nível do aplicativo e, como tal, é uma área importante
para análise posterior.

- Pode ser necessário um ajuste adicional dos parâmetros da biblioteca
 de streaming.
- Another area for research is the interaction of the streaming lib
 with the NTCP and SSU transport layers. See [the NTCP discussion
 page]() for details.
- A interação dos algoritmos de roteamento com a biblioteca de
 streaming afeta fortemente o desempenho. Em particular, a
 distribuição aleatória de mensagens para vários túneis em um pool
 leva a um alto grau de entrega fora de ordem, o que resulta em
 tamanhos de janela menores do que seria o caso de outra forma. O
 roteador atualmente roteia mensagens para um único par de destino
 de/para por meio de um conjunto consistente de túneis, até a
 expiração do túnel ou falha na entrega. Os algoritmos de seleção de
 túnel e falha do roteador devem ser revisados para possíveis
 melhorias.
- Os dados no primeiro pacote SYN podem exceder a MTU do receptor.
- O campo DELAY_REQUESTED poderia ser mais utilizado.
- Pacotes SYNCHRONIZE iniciais duplicados em fluxos de curta duração
 podem não ser reconhecidos e removidos.
- Não mandar o MTU na retransmissão.
- Os dados são enviados a menos que a janela de saída esteja cheia.
 (ou seja, sem Nagle ou TCP_NODELAY) Provavelmente deve haver uma
 opção de configuração para isso.
- O zzz adicionou código de depuração à biblioteca de streaming para
 registrar pacotes em um formato (pcap) compatível com o Wireshark;
 Use isso para analisar melhor o desempenho. O formato pode exigir
 aprimoramento para mapear mais parâmetros da biblioteca de streaming
 para campos TCP.
- Há propostas para substituir a biblioteca de streaming pelo TCP
 padrão (ou talvez uma camada nula junto com soquetes brutos).
 Infelizmente, isso seria incompatível com a biblioteca de streaming
 , mas seria bom comparar o desempenho dos dois.


