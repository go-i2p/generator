 Roteamento de
Túnel Julho de 2011
0.8.7 

## Visão geral

Esta página contém uma visão geral da terminologia e operação do túnel
I2P, com links para mais páginas técnicas, detalhes e especificações.

As briefly explained in the [introduction](), I2P
builds virtual \"tunnels\" - temporary and unidirectional paths through
a sequence of routers. These tunnels are classified as either inbound
tunnels (where everything given to it goes towards the creator of the
tunnel) or outbound tunnels (where the tunnel creator shoves messages
away from them). When Alice wants to send a message to Bob, she will
(typically) send it out one of her existing outbound tunnels with
instructions for that tunnel\'s endpoint to forward it to the gateway
router for one of Bob\'s current inbound tunnels, which in turn passes
it to Bob.

![Alice connecting through her outbound tunnel to Bob via his inbound
tunnel](images/tunnelSending.png "Alice connecting through her outbound tunnel to Bob via his inbound tunnel")

 A: Gateway de saída (Alice)
 B: Participante de saída
 C: Ponto de saída
 D: Gateway entrante
 E: Participante de entrada
 F: Ponto de extremidade de entrada (Bob)

## Vocabulário do túnel

- **Tunnel gateway** - the first router in a tunnel. For inbound
 tunnels, this is the one mentioned in the LeaseSet published in the
 [network database](). For outbound tunnels,
 the gateway is the originating router. (e.g. both A and D above)
- **Ponto final do túnel** - o último roteador em um túnel. (por
 exemplo, C e F acima)
- **Participante do túnel** - todos os roteadores em um túnel, exceto
 o gateway ou o ponto final (por exemplo, B e E acima)
- **túnel n-Hop** - um túnel com um número específico de saltos entre
 roteadores, por exemplo:
 - **túnel de 0 saltos** - um túnel onde o gateway também é o ponto
 final
 - **Túnel de 1 salto** - um túnel onde o gateway fala diretamente
 com o ponto final
 - **túnel de 2 (ou mais) saltos** - um túnel onde há pelo menos um
 participante intermediário do túnel . (o diagrama acima inclui
 dois túneis de 2 saltos - um saindo de Alice, um entrando em
 Bob)
- **Tunnel ID** - A [4 byte
 integer](#type_TunnelId) different
 for each hop in a tunnel, and unique among all tunnels on a router.
 Chosen randomly by the tunnel creator.

## Informações sobre a construção do túnel

Routers performing the three roles (gateway, participant, endpoint) are
given different pieces of data in the initial [Tunnel Build
Message]() to accomplish their tasks:

- **O gateway do túnel obtém:**
 - **tunnel encryption key** - an [AES private
 key](#type_SessionKey) for
 encrypting messages and instructions to the next hop
 - **tunnel IV key** - an [AES private
 key](#type_SessionKey) for
 double-encrypting the IV to the next hop
 - **reply key** - an [AES public
 key](#type_SessionKey) for
 encrypting the reply to the tunnel build request
 - **resposta IV** - o IV para criptografar a resposta à
 solicitação de construção do túnel
 - **id do túnel** - inteiro de 4 bytes (somente gateways de
 entrada)
 - **próximo salto** - qual roteador é o próximo no caminho (a
 menos que este seja um túnel de 0 saltos e o gateway também seja
 o ponto final)
 - **próximo id do túnel** - O ID do túnel no próximo salto
- **Todos os participantes do túnel intermediário recebem:**
 - **tunnel encryption key** - an [AES private
 key](#type_SessionKey) for
 encrypting messages and instructions to the next hop
 - **tunnel IV key** - an [AES private
 key](#type_SessionKey) for
 double-encrypting the IV to the next hop
 - **reply key** - an [AES public
 key](#type_SessionKey) for
 encrypting the reply to the tunnel build request
 - **resposta IV** - o IV para criptografar a resposta à
 solicitação de construção do túnel
 - **id do túnel** - inteiro de 4 bytes
 - **próximo salto** - qual roteador é o próximo no caminho
 - **próximo id do túnel** - O ID do túnel no próximo salto
- **O ponto final do túnel obtém:**
 - **tunnel encryption key** - an [AES private
 key](#type_SessionKey) for
 encrypting messages and instructions to the the endpoint
 (itself)
 - **tunnel IV key** - an [AES private
 key](#type_SessionKey) for
 double-encrypting the IV to the endpoint (itself)
 - **reply key** - an [AES public
 key](#type_SessionKey) for
 encrypting the reply to the tunnel build request (outbound
 endpoints only)
 - **resposta IV** - o IV para criptografar a resposta à
 solicitação de construção do túnel (somente endpoints de saída)
 - **id do túnel** - inteiro de 4 bytes (somente pontos de
 extremidade de saída)
 - **roteador de resposta** - o gateway de entrada do túnel para
 enviar a resposta (somente pontos de extremidade de saída)
 - **ID do túnel de resposta** - O ID do túnel do roteador de
 resposta (somente pontos de extremidade de saída)

Details are in the [tunnel creation
specification]().

## Túnel de agrupamento

Several tunnels for a particular purpose may be grouped into a \"tunnel
pool\", as described in the [tunnel
specification](#tunnel.pooling). This
provides redundancy and additional bandwidth. The pools used by the
router itself are called \"exploratory tunnels\". The pools used by
applications are called \"client tunnels\".

## Comprimento do túnel {#length}

As mentioned above, each client requests that their router provide
tunnels to include at least a certain number of hops. The decision as to
how many routers to have in one\'s outbound and inbound tunnels has an
important effect upon the latency, throughput, reliability, and
anonymity provided by I2P - the more peers that messages have to go
through, the longer it takes to get there and the more likely that one
of those routers will fail prematurely. The less routers in a tunnel,
the easier it is for an adversary to mount traffic analysis attacks and
pierce someone\'s anonymity. Tunnel lengths are specified by clients via
[I2CP options](#options). The maximum number of
hops in a tunnel is 7.

### túneis de 0-pulo

Sem roteadores remotos em um túnel, o usuário tem uma negação plausível
muito básica (já que ninguém sabe ao certo se o peer que enviou a
mensagem não estava simplesmente encaminhando-a como parte do túnel). No
entanto, seria bastante fácil montar um ataque de análise estatística e
perceber que mensagens direcionadas a um destino específico são sempre
enviadas por um único gateway. A análise estatística contra túneis de
saída de 0 saltos é mais complexa, mas poderia mostrar informações
semelhantes (embora fosse um pouco mais difícil de montar).

### túneis de 1-pulo

With only one remote router in a tunnel, the user has both plausible
deniability and basic anonymity, as long as they are not up against an
internal adversary (as described on [threat
model]()). However, if the adversary ran a
sufficient number of routers such that the single remote router in the
tunnel is often one of those compromised ones, they would be able to
mount the above statistical traffic analysis attack.

### túnel de 2-pulos

Com dois ou mais roteadores remotos, o custo da montagem de ataque de
análise de tráfego aumenta, uma vez que vários roteadores remotos devem
ser comprometidos para montar isto.

### túnel de 3-nós (ou mais)

To reduce the susceptibility to [some attacks](), 3
or more hops are recommended for the highest level of protection.
[Recent studies]() also conclude that more than 3
hops does not provide additional protection.

### Tamanhos padrões de túnel

The router uses 2-hop tunnels by default for its exploratory tunnels.
Client tunnel defaults are set by the application, using [I2CP
options](#options). Most applications use 2 or 3
hops as their default.

## Teste de túnel {#testing}

All tunnels are periodically tested by their creator by sending a
DeliveryStatusMessage out an outbound tunnel and bound for another
inbound tunnel (testing both tunnels at once). If either fails a number
of consecutive tests, it is marked as no longer functional. If it was
used for a client\'s inbound tunnel, a new leaseSet is created. Tunnel
test failures are also reflected in the [capacity rating in the peer
profile](#capacity).

## Criação de túnel

Tunnel creation is handled by [garlic
routing]() a Tunnel Build Message to a
router, requesting that they participate in the tunnel (providing them
with all of the appropriate information, as above, along with a
certificate, which right now is a \'null\' cert, but will support
hashcash or other non-free certificates when necessary). That router
forwards the message to the next hop in the tunnel. Details are in the
[tunnel creation specification]().

## Tunnel encryption

Multi-layer encryption is handled by [garlic
encryption]() of tunnel messages. Details
are in the [tunnel specification](). The IV
of each hop is encrypted with a separate key as explained there.

## Trabalho futuro

- Outras técnicas de teste de túnel podem ser usadas, como alho
 envolvendo uma série de testes em dentes, testando participantes
 individuais do túnel separadamente, etc.
- Mudar para os padrões de túneis exploratórios de 3 saltos.
- Em uma versão futura distante, as opções especificando as
 configurações de agrupamento, mistura e geração de palha podem ser
 implementadas.
- Em uma versão futura distante, limites de na quantidade e tamanho de
 mensagens permitidas durante a vida útil do túnel podem ser
 implementados (por exemplo, não mais que 300 mensagens ou 1 MB por
 minuto).

## Ver também

- [Especificação do
 Túnel]()
- [Especificação de criação de
 túnel]()
- [Túneis
 unidirecionais]()
- [Especificação de mensagem de
 túnel]()
- [Roteamento
 alho]()
- [ElGamal/AES+SessionTag]()
- [opções
 I2CP](#options)


