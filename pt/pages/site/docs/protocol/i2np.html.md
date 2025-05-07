 Protocolo de rede
I2P (I2NP) Outubro de 2018 0.9.37 

O Protocolo de Rede I2P (I2NP), que fica entre o I2CP e os vários
protocolos de transporte I2P, gerencia o roteamento e a mistura de
mensagens entre roteadores, bem como a seleção de quais transportes usar
ao se comunicar com um par para o qual há vários transportes comuns
suportados.

### Definição do I2NP

As mensagens I2NP (I2P Network Protocol) podem ser usadas para mensagens
de um salto, de roteador para roteador, ponto a ponto. Ao criptografar e
encapsular mensagens em outras mensagens, elas podem ser enviadas de
forma segura por vários saltos até o destino final. A prioridade é usada
apenas localmente na origem, ou seja, ao enfileirar para entrega de
saída.

The priorities listed below may not be current and are subject to
change. See the [OutNetMessage
Javadocs]() for the current priority
settings. Priority queueing implementation may vary.

### Formato de mensagem

A tabela a seguir especifica o cabeçalho tradicional de 16 bytes usado
no NTCP. Os transportes SSU e NTCP2 usam cabeçalhos modificados.

 Campo Bytes
 --------------------------- ------------
 Tipo 1
 ID único 4
 Expiração 8
 Comprimento da carga útil 2
 Checksum 1
 Carga útil 0 - 61.2KB

While the maximum payload size is nominally 64KB, the size is further
constrained by the method of fragmenting I2NP messages into multiple 1KB
tunnel messages as described on [the tunnel implementation
page](). The maximum number of fragments is
64, and the message may not be perfectly aligned, So the message must
nominally fit in 63 fragments.

O tamanho máximo de um fragmento inicial é 956 bytes (assumindo o modo
de entrega TUNNEL); o tamanho máximo de um fragmento subsequente é 996
bytes. Portanto, o tamanho máximo é aproximadamente 956 + (62 \* 996) =
62708 bytes, ou 61,2 KB.

Além disso, os transportes podem ter restrições adicionais. O limite
NTCP é 16 KB - 6 = 16378 bytes. O limite SSU é aproximadamente 32 KB. O
limite NTCP2 é aproximadamente 64 KB - 20 = 65516 bytes, o que é maior
do que um túnel pode suportar.

Note que estes não são os limites para datagramas que o cliente vê, pois
o roteador pode agrupar um leaseset de resposta e/ou tags de sessão
junto com a mensagem do cliente em uma mensagem garlic. O leaseset e as
tags juntos podem adicionar cerca de 5,5 KB. Portanto, o limite atual de
datagramas é de cerca de 10 KB. Este limite será aumentado em uma versão
futura.

### Tipos de mensagens

Prioridade de número mais alto é prioridade mais alta. A maioria do
tráfego é TunnelDataMessages (prioridade 400), então qualquer coisa
acima de 400 é essencialmente alta prioridade, e qualquer coisa abaixo é
baixa prioridade. Observe também que muitas das mensagens são geralmente
roteadas através de túneis exploratórios, não túneis de cliente, e
portanto podem não estar na mesma fila, a menos que os primeiros saltos
estejam no mesmo peer.

Além disso, nem todos os tipos de mensagens são enviados sem
criptografia. Por exemplo, ao testar um túnel, o roteador encapsula uma
DeliveryStatusMessage, que é encapsulada em uma GarlicMessage, que é
encapsulada em uma DataMessage.

Mensagem

Tipo

Comprimento da carga útil

Prioridade

Comentários

DatabaseLookupMessage

2

 

500

Pode variar

DatabaseSearchReplyMessage

3

Typ. 161

300

O tamanho é 65 + 32\*(número de hashes), onde normalmente são retornados
os hashes para três roteadores de floodfill.

DatabaseStoreMessage

1

Varia

460

A prioridade pode variar. O tamanho é 898 bytes para um leaseSet típico
de 2 arrendamentos. As estruturas RouterInfo são compactadas e o tamanho
varia; no entanto há um esforço contínuo para reduzir a quantidade de
dados publicados em um RouterInfo à medida que nos aproximamos da versão
1.0.

DataMessage

20

4 - 62080

425

A prioridade pode variar dependendo do destino

DeliveryStatusMessage

10

12

 

Usado para respostas de mensagens e para testar túneis - geralmente
encapsulado em um GarlicMessage

[GarlicMessage](#op.garlic)

11

 

 

Geralmente encapsulado em um DataMessage - , mas quando descompactado,
recebe uma prioridade de 100 do roteador de encaminhamento

[TunnelBuildMessage](#tunnelCreate.requestRecord)

21

4224

500

[TunnelBuildReplyMessage](#tunnelCreate.replyRecord)

22

4224

300

TunnelDataMessage

18

1028

400

A mensagem mais comum. A prioridade para participantes do túnel,
endpoints de saída e gateways de entrada foi reduzida para 200 a partir
da versão 0.6.1.33. Mensagens de gateway de saída (ou seja, aquelas
originadas localmente) permanecem em 400.

TunnelGatewayMessage

19

 

300/400

VariableTunnelBuildMessage

23

1057 - 4225

500

TunnelBuildMessage mais curto a partir de 0.7.12

VariableTunnelBuildReplyMessage

24

1057 - 4225

300

TunnelBuildReplyMessage mais curto a partir de 0.7.12

Others listed in [2003 Spec]()

0,4-9,12

 

 

Obsoleto, Desusado

### Especificação completa do protocolo

[On the I2NP Specification page](). See also
the [Common Data Structure Specification
page]().

### Trabalho futuro

Não está claro se o esquema de prioridade atual é geralmente eficaz, e
se as prioridades para várias mensagens devem ser ajustadas ainda mais.
Este é um tópico para pesquisas, análises e testes adicionais.


