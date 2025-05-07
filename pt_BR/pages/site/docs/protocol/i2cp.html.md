 I2CP
2025-04 0.9.66 

O I2P Client Protocol (I2CP) expõe uma forte separação de preocupações
entre o roteador e qualquer cliente que deseja se comunicar pela rede.
Ele permite mensagens seguras e assíncronas enviando e recebendo
mensagens por um único soquete TCP. Com o I2CP, um aplicativo cliente
informa ao roteador quem eles são (seu \"destino\"), quais compensações
de anonimato, confiabilidade e latência fazer e para onde enviar
mensagens. Por sua vez, o roteador usa I2CP para informar ao cliente
quando alguma mensagem chegou e para solicitar autorização para que
alguns túneis sejam usados.

The protocol itself is implemented in Java, to provide the [Client
SDK](). This SDK is exposed in the i2p.jar package,
which implements the client-side of I2CP. Clients should never need to
access the router.jar package, which contains the router itself and the
router-side of I2CP. There is also a [C library
implementation](). A non-Java client would also
have to implement the [streaming library]()
for TCP-style connections.

Applications can take advantage of the base I2CP plus the
[streaming]() and
[datagram]() libraries by using the [Simple
Anonymous Messaging]() or
[BOB]() protocols, which do not require clients to
deal with any sort of cryptography. Also, clients may access the network
by one of several proxies - HTTP, CONNECT, and SOCKS 4/4a/5.
Alternatively, Java clients may access those libraries in
ministreaming.jar and streaming.jar. So there are several options for
both Java and non-Java applications.

Client-side end-to-end encryption (encrypting the data over the I2CP
connection) was disabled in I2P release 0.6, leaving in place the
[ElGamal/AES end-to-end encryption]() which
is implemented in the router. The only cryptography that client
libraries must still implement is [DSA public/private key
signing](#DSA) for
[LeaseSets](#msg_CreateLeaseSet) and [Session
Configurations](#struct_SessionConfig), and
management of those keys.

Em uma instalação I2P padrão, a porta 7654 é usada por clientes Java
externos para se comunicar com o roteador local via I2CP. Por padrão, o
roteador se vincula ao endereço 127.0.0.1. Para se vincular a 0.0.0.0,
defina a opção de configuração avançada do roteador
`i2cp.tcp.bindAllInterfaces=true` e reinicie. Os clientes na mesma JVM
que o roteador passam mensagens diretamente para o roteador por meio de
uma interface JVM interna.

Some router and client implementations may also support external
connections over SSL, as configured by the i2cp.SSL=true option. While
SSL is not the default, it is strongly recommended for any traffic that
may be exposed to the open Internet. The authorization user/password (if
any), the [Private
Key](#type_PrivateKey) and [Signing
Private Key](#type_SigningPrivateKey)
for the
[Destination](#struct_Destination) are
all transmitted in-the-clear unless SSL is enabled. Some router and
client implementations may also support external connections over domain
sockets.

## Especificação do Protocolo I2CP

Now on the [I2CP Specification page]().

## Inicialização do I2CP

When a client connects to the router, it first sends a single protocol
version byte (0x2A). Then it sends a [GetDate
Message](#msg_GetDate) and waits for the [SetDate
Message](#msg_SetDate) response. Next, it sends a
[CreateSession Message](#msg_CreateSession)
containing the session configuration. It next awaits a [RequestLeaseSet
Message](#msg_RequestLeaseSet) from the router,
indicating that inbound tunnels have been built, and responds with a
CreateLeaseSetMessage containing the signed LeaseSet. The client may now
initiate or receive connections from other I2P destinations.

## Opções I2CP {#options}

### Opções do Roteador

The following options are traditionally passed to the router via a
[SessionConfig](#struct_SessionConfig) contained
in a [CreateSession Message](#msg_CreateSession)
or a [ReconfigureSession
Message](#msg_ReconfigureSession).

Opções do Roteador

Opção

Como Liberado

Argumentos recomendados

Faixa permitida

Padrão

Descrição

clientMessageTimeout

 

 

8\*1000 - 120\*1000

60\*1000

O tempo limite (ms) para todas as mensagens enviadas. Não utilizado.
Veja a especificação do protocolo para configurações por mensagem.

crypto.lowTagThreshold

0.9.2

 

1-128

30

Número mínimo de tags de sessão ElGamal/AES antes de enviarmos mais.
Recomendado: aproximadamente tagsToSend \* 2/3

crypto.ratchet.inboundTags

0.9.47

 

1-?

160

Inbound tag window for ECIES-X25519-AEAD-Ratchet. Local inbound tagset
size. See proposal 144.

crypto.ratchet.outboundTags

0.9.47

 

1-?

160

Outbound tag window for ECIES-X25519-AEAD-Ratchet. Advisory to send to
the far-end in the options block. See proposal 144.

crypto.tagsToSend

0.9.2

 

1-128

40

Número de tags de sessão ElGamal/AES a serem enviadas por vez. Para
clientes com largura de banda relativamente baixa por par de clientes
(IRC, alguns aplicativos UDP), isso pode ser definido como um valor
menor.

explicitPeers

 

 

 

null

Lista separada por vírgulas de Hashes Base 64 de pares para construir
túneis; somente para depuração

i2cp.dontPublishLeaseSet

 

true, false

 

false

Geralmente deve ser definido como verdadeiro para clientes e falso para
servidores

i2cp.fastReceive

0.9.4

 

true, false

false

Se verdadeiro, o roteador apenas envia o MessagePayload em vez de enviar
um MessageStatus e aguardar um ReceiveMessageBegin.

i2cp.leaseSetAuthType

0.9.41

0

0-2

0

The type of authentication for encrypted LS2. 0 for no per-client
authentication (the default); 1 for DH per-client authentication; 2 for
PSK per-client authentication. See proposal 123.

i2cp.leaseSetEncType

0.9.38

4,0

0-65535,\...

0

The encryption type to be used, as of 0.9.38. Interpreted client-side,
but also passed to the router in the SessionConfig, to declare intent
and check support. As of 0.9.39, may be comma-separated values for
multiple types. See PublicKey in common strutures spec for values. See
proposals 123, 144, and 145.

i2cp.leaseSetOfflineExpiration

0.9.38

 

 

 

The expiration of the offline signature, 4 bytes, seconds since the
epoch. See proposal 123.

i2cp.leaseSetOfflineSignature

0.9.38

 

 

 

The base 64 of the offline signature. See proposal 123.

i2cp.leaseSetPrivKey

0.9.41

 

 

 

A base 64 X25519 private key for the router to use to decrypt the
encrypted LS2 locally, only if per-client authentication is enabled.
Optionally preceded by the key type and \':\'. Only \"ECIES_X25519:\" is
supported, which is the default. See proposal 123. Do not confuse with
i2cp.leaseSetPrivateKey which is for the leaseset encryption keys.

i2cp.leaseSetSecret

0.9.39

 

 

\"\"

Base 64 encoded UTF-8 secret used to blind the leaseset address. See
proposal 123.

i2cp.leaseSetTransientPublicKey

0.9.38

 

 

 

\[type:\]b64 The base 64 of the transient private key, prefixed by an
optional sig type number or name, default DSA_SHA1. See proposal 123.

i2cp.leaseSetType

0.9.38

1,3,5,7

1-255

1

The type of leaseset to be sent in the CreateLeaseSet2 Message.
Interpreted client-side, but also passed to the router in the
SessionConfig, to declare intent and check support. See proposal 123.

i2cp.messageReliability

 

 

BestEffort, None

BestEffort

Garantido está desabilitado; Nenhum implementado em 0.8.1; o padrão da
biblioteca de streaming é Nenhum a partir de 0.8.1, o padrão do lado do
cliente é Nenhum a partir de 0.9.4

i2cp.password

0.8.2

string

 

 

Para autorização, se exigido pelo roteador. Se o cliente estiver sendo
executado na mesma JVM que um roteador, esta opção não será necessária.
Aviso - o nome de usuário e a senha são enviados em texto simples para o
roteador, a menos que esteja usando SSL (i2cp.SSL=true). A autorização
só é recomendada ao usar SSL.

i2cp.username

0.8.2

string

 

 

inbound.allowZeroHop

 

true, false

 

true

Se a chegada de túneis de zero pulo é permitida

outbound.allowZeroHop

 

true, false

 

true

Se a saída de túneis de zero pulo é permitida

inbound.backupQuantity

 

Número de bytes IP a serem correspondidos para determinar se dois
roteadores não devem estar no mesmo túnel. 0 para desabilitar.

outbound.IPRestriction

 

Número de bytes IP a serem correspondidos para determinar se dois
roteadores não devem estar no mesmo túnel. 0 para desabilitar.

inbound.length

 

Quantidade aleatória para adicionar ou subtrair ao comprimento dos
túneis. Um número positivo x significa adicionar uma quantidade
aleatória de 0 a x, inclusive. Um número negativo -x significa adicionar
uma quantidade aleatória de -x a x, inclusive. O roteador limitará o
comprimento total do túnel de 0 a 7, inclusive. A variação padrão era 1
antes da versão 0.7.6.

outbound.lengthVariance

 

Quantidade aleatória para adicionar ou subtrair do comprimento dos
túneis de saída. Um número positivo x significa adicionar uma quantidade
aleatória de 0 a x inclusive. Um número negativo -x significa adicionar
uma quantidade aleatória de -x a x inclusive. O roteador limitará o
comprimento total do túnel de 0 a 7 inclusive. A variação padrão era 1
antes da versão 0.7.6.

inbound.nickname

 

string

 

 

Nome do túnel - geralmente usado no console do roteador, que usará os
primeiros caracteres do hash Base64 do destino por padrão.

outbound.nickname

 

string

 

 

Nome do túnel - geralmente ignorado, a menos que inbound.nickname não
esteja definido.

outbound.priority

0.9.4

Ajuste de prioridade para mensagens de saída. Quanto maior, maior a
prioridade.

inbound.quantity

 

Número de túneis em. O limite foi aumentado de 6 para 16 na versão 0.9;
no entanto, números maiores que 6 são incompatíveis com versões mais
antigas.

outbound.quantity

 

Usado para ordenação consistente de pares em reinicializações.

outbound.randomKey

0.9.17

Base 64 encoding of 32 random bytes

 

 

inbound.\*

 

 

 

 

Quaisquer outras opções prefixadas com \"inbound\" são armazenadas nas
propriedades \"unknown options\" das configurações do pool de túneis de
entrada.

outbound.\*

 

 

 

 

Quaisquer outras opções prefixadas com \"outbound\" são armazenadas nas
propriedades \"opções desconhecidas\" das configurações do pool de
túneis de saída.

shouldBundleReplyInfo

0.9.2

true, false

 

true

Defina como falso para desabilitar o agrupamento de um LeaseSet de
resposta. Para clientes que não publicam seu LeaseSet, esta opção deve
ser verdadeira para que qualquer resposta seja possível. \"true\" também
é recomendado para servidores multihomed com tempos de conexão longos.

Definir como \"false\" pode economizar largura de banda de saída
significativa, especialmente se o cliente estiver configurado com um
grande número de túneis de entrada (Leases). Se as respostas ainda forem
necessárias, isso pode transferir a carga de largura de banda para o
cliente remoto e o floodfill. Há vários casos em que \"false\" pode ser
apropriado:

- Comunicação unidirecional, sem necessidade de resposta
- LeaseSet é publicado e uma latência de resposta mais alta é
 aceitável
- O LeaseSet é publicado, o cliente é um \"servidor\", todas as
 conexões são de entrada então o destino remoto da conexão obviamente
 já tem o leaseset. As conexões são curtas ou é aceitável que a
 latência em uma conexão de longa duração aumente temporariamente
 enquanto a outra extremidade busca novamente o LeaseSet após a
 expiração. Os servidores HTTP podem atender a esses requisitos.

Observação: grandes configurações de quantidade, comprimento ou variação
podem causar problemas significativos de desempenho ou confiabilidade.

Note: As of release 0.7.7, option names and values must use UTF-8
encoding. This is primarily useful for nicknames. Prior to that release,
options with multi-byte characters were corrupted. Since options are
encoded in a [Mapping](#type_Mapping),
all option names and values are limited to 255 bytes (not characters)
maximum.

### Opções do Cliente

As seguintes opções são interpretadas no lado do cliente, e serão
interpretadas se passadas para o I2PSession por meio da chamada
I2PClient.createSession(). A biblioteca de streaming também deve passar
essas opções para o I2CP. Outras implementações podem ter padrões
diferentes.

Opções do Cliente

Opção

Como Liberado

Argumentos recomendados

Faixa permitida

Padrão

Descrição

i2cp.closeIdleTime

0.7.1

1800000

Se verdadeiro, o roteador apenas envia o MessagePayload em vez de enviar
um MessageStatus e aguardar um ReceiveMessageBegin.

i2cp.gzip

0.6.5

true, false

 

true

Dados de saída Gzip

i2cp.leaseSetAuthType

0.9.41

0

0-2

0

The type of authentication for encrypted LS2. 0 for no per-client
authentication (the default); 1 for DH per-client authentication; 2 for
PSK per-client authentication. See proposal 123.

i2cp.leaseSetBlindedType

0.9.39

 

0-65535

See prop. 123

The sig type of the blinded key for encrypted LS2. Default depends on
the destination sig type. See proposal 123.

i2cp.leaseSetClient.dh.nnn

0.9.41

b64name:b64pubkey

 

 

The base 64 of the client name (ignored, UI use only), followed by a
\':\', followed by the base 64 of the public key to use for DH
per-client auth. nnn starts with 0 See proposal 123.

i2cp.leaseSetClient.psk.nnn

0.9.41

b64name:b64privkey

 

 

The base 64 of the client name (ignored, UI use only), followed by a
\':\', followed by the base 64 of the private key to use for PSK
per-client auth. nnn starts with 0. See proposal 123.

i2cp.leaseSetEncType

0.9.38

0

0-65535,\...

0

The encryption type to be used, as of 0.9.38. Interpreted client-side,
but also passed to the router in the SessionConfig, to declare intent
and check support. As of 0.9.39, may be comma-separated values for
multiple types. See also i2cp.leaseSetPrivateKey. See PublicKey in
common strutures spec for values. See proposals 123, 144, and 145.

i2cp.leaseSetKey

0.7.1

 

 

 

Para leasesets criptografados. Base 64 SessionKey (44 caracteres)

i2cp.leaseSetOption.nnn

0.9.66

srvKey=srvValue

 

 

A service record to be placed in the LeaseSet2 options. Example:
\"\_smtp.\_tcp=1 86400 0 0 25 \...b32.i2p\" nnn starts with 0. See
proposal 167.

i2cp.leaseSetPrivateKey

0.9.18

 

 

 

Chaves privadas de base 64 para criptografia. Opcionalmente precedido
pelo nome ou número do tipo de criptografia e \':\'. Para LS1, apenas
uma chave é suportada, e apenas \"0:\" ou \"ELGAMAL_2048:\" é suportado,
que é o padrão. A partir da versão 0.9.39, para LS2, várias chaves podem
ser separadas por vírgulas, e cada chave deve ser de um tipo de
criptografia diferente. O I2CP gerará a chave pública a partir da chave
privada. Use para chaves de leaseset persistentes em reinicializações.
Veja as propostas 123, 144 e 145. Veja também i2cp.leaseSetEncType. Do
not confuse with i2cp.leaseSetPrivKey which is for encrypted LS2.

i2cp.leaseSetSecret

0.9.39

 

 

\"\"

Base 64 encoded UTF-8 secret used to blind the leaseset address. See
proposal 123.

i2cp.leaseSetSigningPrivateKey

0.9.18

 

 

 

Chave privada base 64 para assinaturas. Opcionalmente precedido pelo
tipo de chave e \':\'. DSA_SHA1 é o padrão. O tipo de chave deve
corresponder ao tipo de assinatura no destino. O I2CP gerará a chave
pública a partir da chave privada. Use para chaves de leaseset
persistentes em reinicializações.

i2cp.leaseSetType

0.9.38

1,3,5,7

1-255

1

The type of leaseset to be sent in the CreateLeaseSet2 Message.
Interpreted client-side, but also passed to the router in the
SessionConfig, to declare intent and check support. See proposal 123.

i2cp.messageReliability

 

 

BestEffort, None

None

Garantido está desabilitado; Nenhum implementado em 0.8.1; Nenhum é o
padrão a partir de 0.9.4

i2cp.reduceIdleTime

0.7.1

1200000

Conecte-se ao roteador usando SSL. Se o cliente estiver sendo executado
na mesma JVM que um roteador, esta opção será ignorada e o cliente se
conectará a esse roteador internamente.

i2cp.tcp.host

 

 

 

127.0.0.1

Nome do host do roteador. Se o cliente estiver sendo executado na mesma
JVM que um roteador, esta opção será ignorada e o cliente se conectará a
esse roteador internamente.

i2cp.tcp.port

 

 

1-65535

7654

Porta I2CP do roteador. Se o cliente estiver sendo executado na mesma
JVM que um roteador, esta opção será ignorada e o cliente se conectará a
esse roteador internamente.

Nota: Todos os argumentos, incluindo números, são strings. Valores
true/false são strings que não diferenciam maiúsculas de minúsculas.
Qualquer coisa diferente de \"true\" que não diferencia maiúsculas de
minúsculas é interpretada como false. Todos os nomes de opções
diferenciam maiúsculas de minúsculas.

## Formato de dados de carga útil I2CP e multiplexação {#format}

The end-to-end messages handled by I2CP (i.e. the data sent by the
client in a [SendMessageMessage](#msg_SendMessage)
and received by the client in a
[MessagePayloadMessage](#msg_MessagePayload)) are
gzipped with a standard 10-byte gzip header beginning with 0x1F 0x8B
0x08 as specified by [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt). As
of release 0.7.1, I2P uses ignored portions of the gzip header to
include protocol, from-port, and to-port information, thus supporting
streaming and datagrams on the same destination, and allowing
query/response using datagrams to work reliably in the presence of
multiple channels.

A função gzip não pode ser completamente desativada, no entanto, definir
i2cp.gzip=false transforma a configuração de esforço do gzip em 0, o que
pode economizar um pouco de CPU. Implementations may select different
gzip efforts on a per-socket or per-message basis, depending on an
assessment of the compressibility of the contents. Due to the
compressibility of destination padding implemented in API 0.9.57
(proposal 161), compression of the streaming SYN packets in each
direction, and of repliable datagrams, is recommended even if the
payload is not compressible. Implementations may wish to write a trivial
gzip/gunzip function for a gzip effort of 0, which will provide large
efficiency gains over a gzip library for this case.

Bytes

Conteúdo

0-2

Cabeçalho Gzip 0x1F 0x8B 0x08

3

Bandeiras Gzip

4-5

Porta de origem I2P (Gzip mtime)

6-7

Porta de Destino I2P (Gzip mtime)

8

Gzip xflags (set to 2 to be indistinguishable from the Java
implementation)

9

Protocolo I2P (6 = Streaming, 17 = Datagrama, 18 = Datagramas brutos)
(Gzip OS)

Note: I2P protocol numbers 224-254 are reserved for experimental
protocols. I2P protocol number 255 is reserved for future expansion.

A integridade dos dados é verificada com o padrão gzip CRC-32 como
especificado por [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt).

## Important Differences from Standard IP

I2CP ports are for I2P sockets and datagrams. They are unrelated to your
local sockets or ports. Because I2P did not support ports and protocol
numbers prior to release 0.7.1, ports and protocol numbers are somewhat
different from that in standard IP, for backward compatibility:

- Port 0 is valid and has special meaning.
- Ports 1-1023 are not special or privileged.
- Servers listen on port 0 by default, which means \"all ports\".
- Clients send to port 0 by default, which means \"any port\".
- Clients send from port 0 by default, which means \"unspecified\".
- Servers may have a service listening on port 0 and other services
 listening on higher ports. If so, the port 0 service is the default,
 and will be connected to if the incoming socket or datagram port
 does not match another service.
- Most I2P destinations only have one service running on them, so you
 may use the defaults, and ignore I2CP port configuration.
- Protocol 0 is valid and means \"any protocol\". However, this is not
 recommended, and probably will not work. Streaming requires that the
 protocol number is set to 6.
- Streaming sockets are tracked by an internal connection ID.
 Therefore, there is no requirement that the 5-tuple of
 dest:port:dest:port:protocol be unique. For example, there may be
 multiple sockets with the same ports between two destinations.
 Clients do not need to pick a \"free port\" for an outbound
 connection.

## Trabalho futuro {#future}

- O mecanismo de autorização atual pode ser modificado para usar
 senhas com hash.
- As Chaves Privadas de Assinatura estão incluídas na mensagem Criar
 Conjunto de Locação, não é necessário. A revogação não foi
 implementada. Deve ser substituído por dados aleatórios ou removido.
- Some improvements may be able to use messages previously defined but
 not implemented. For reference, here is the [I2CP Protocol
 Specification Version 0.9]() (PDF) dated
 August 28, 2003. That document also references the [Common Data
 Structures Specification Version 0.9]().

## See Also {#links}

[C library implementation](http://git.repo.i2p/w/libi2cp.git) 
