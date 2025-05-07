 Bittorrent sob
I2P 2024-11 0.9.64 

Existem vários clientes e rastreadores de bittorrent no I2P. Como o
endereçamento I2P usa um destino em vez de um IP e porta, pequenas
alterações são necessárias no software do rastreador e do cliente para
operação no I2P. Essas alterações são especificadas abaixo. Observe
cuidadosamente as diretrizes de compatibilidade com clientes e
rastreadores I2P mais antigos.

Esta página especifica detalhes do protocolo comuns a todos os clientes
e rastreadores. Clientes e rastreadores específicos podem implementar
outros recursos ou protocolos exclusivos.

Aceitamos portas adicionais de software cliente e rastreador para o I2P.

## General Guidance for Developers

Most non-Java bittorrent clients will connect to I2P via
[SAMv3](). SAM sessions (or
inside I2P, tunnel pools or sets of tunnels) are designed to be
long-lived. Most bittorrent clients will only need one session, created
at startup and closed on exit. I2P is different from Tor, where circuits
may be rapidly created and discarded. Think carefully and consult with
I2P developers before designing your application to use more than one or
two simultaneous sessions, or to rapidly create and discard them.
Bittorrent clients must not create a unique session for every
connection. Design your client to use the same session for announces and
client connections.

Also, please ensure your client settings (and guidance to users about
router settings, or router defaults if you bundle a router) will result
in your users contributing more resources to the network than they
consume. I2P is a peer-to-peer network, and the network cannot survive
if a popular application drives the network into permanent congestion.

Do not provide support for bittorrent through an I2P outproxy to the
clearnet as it will probably be blocked. Consult with outproxy operators
for guidance.

The Java I2P and i2pd router implementations are independent and have
minor differences in behavior, feature support, and defaults. Please
test your application with the latest version of both routers.

i2pd SAM is enabled by default; Java I2P SAM is not. Provide
instructions to your users on how to enable SAM in Java I2P (via
/configclients in the router console), and/or provide a good error
message to the user if the initial connect fails, e.g. \"ensure that I2P
is running and the SAM interface is enabled\".

The Java I2P and i2pd routers have different defaults for tunnel
quantities. The Java default is 2 and the i2pd default is 5. For most
low- to medium-bandwidth and low- to medium-connection counts, 3 is
sufficient. Please specify the tunnel quantity in the SESSION CREATE
message to get consistent performance with the Java I2P and i2pd
routers.

I2P supports multiple signature and encryption types. For compatibility,
I2P defaults to old and inefficient types, so all clients should specify
newer types.

If using SAM, the signature type is specified in the DEST GENERATE and
SESSION CREATE (for transient) commands. All clients should set
SIGNATURE_TYPE=7 (Ed25519).

The encryption type is specified in the SAM SESSION CREATE command or in
i2cp options. Multiple encryption types are allowed. Some trackers
support ECIES-X25519, some support ElGamal, and some support both.
Clients should set i2cp.leaseSetEncType=4,0 (for ECIES-X25519 and
ElGamal) so that they may connect to both.

DHT support requires SAM v3.3 PRIMARY and SUBSESSIONS for TCP and UDP
over the same session. This will require substantial development effort
on the client side, unless the client is written in Java. i2pd does not
currently support SAM v3.3. libtorrent does not currently support SAM
v3.3.

Without DHT support, you may wish to automatically announce to a
configurable list of known open trackers so that magnet links will work.
Consult with I2P users for information on currently-up open trackers and
keep your defaults up-to-date. Supporting the i2p_pex extension will
also help alleviate the lack of DHT support.

For more guidance to developers on ensuring your application uses only
the resources it needs, please see the [SAMv3
specification]() and [our
guide to bundling I2P with your
application]().
Contact I2P or i2pd developers for further assistance.

## Anúncios

Os clientes geralmente incluem um parâmetro falso port=6881 no anúncio,
para compatibilidade com rastreadores mais antigos. Os rastreadores
podem ignorar o parâmetro port e não devem exigi-lo.

The ip parameter is the base 64 of the client\'s
[Destination](#struct_Destination),
using the I2P Base 64 alphabet \[A-Z\]\[a-z\]\[0-9\]-\~.
[Destinations](#struct_Destination)
are 387+ bytes, so the Base 64 is 516+ bytes. Clients generally append
\".i2p\" to the Base 64 Destination for compatibility with older
trackers. Trackers should not require an appended \".i2p\".

Outros parâmetros são os mesmos do bittorrent padrão.

Os destinos atuais para clientes são 387 ou mais bytes (516 ou mais na
codificação Base 64). Um máximo razoável para assumir, por enquanto, é
475 bytes. Como o rastreador deve decodificar o Base64 para entregar
respostas compactas (veja abaixo), o rastreador provavelmente deve
decodificar e rejeitar o Base64 ruim quando anunciado.

O tipo de resposta padrão é não compacto. Os clientes podem solicitar
uma resposta compacta com o parâmetro compact=1. Um rastreador pode, mas
não é obrigado a, retornar uma resposta compacta quando solicitado.
Note: All popular trackers now support compact responses and at least
one requires compact=1 in the announce. All clients should request and
support compact responses.

Desenvolvedores de novos clientes I2P são fortemente encorajados a
implementar anúncios em seu próprio túnel em vez de o proxy do cliente
HTTP na porta 4444. Fazer isso é mais eficiente e permite a aplicação do
destino pelo rastreador (veja abaixo).

Não há clientes ou rastreadores I2P conhecidos que atualmente suportem
anúncios/respostas UDP.

## Respostas do rastreador não compacto

A resposta não compacta é igual à do bittorrent padrão, com um \"ip\"
I2P. This is a long base64-encoded \"DNS string\", probably with a
\".i2p\" suffix.

Os rastreadores geralmente incluem uma chave de porta falsa ou usam a
porta do anúncio para compatibilidade com clientes mais antigos. Os
clientes devem ignorar o parâmetro de porta e não devem exigi-lo.

The value of the ip key is the base 64 of the client\'s
[Destination](#struct_Destination), as
described above. Trackers generally append \".i2p\" to the Base 64
Destination if it wasn\'t in the announce ip, for compatibility with
older clients. Clients should not require an appended \".i2p\" in the
responses.

Outras chaves de resposta e valores são os mesmos do bittorrent padrão.

## Respostas do Compact Tracker

In the compact response, the value of the \"peers\" dictionary key is a
single byte string, whose length is a multiple of 32 bytes. This string
contains the concatenated [32-byte SHA-256
Hashes](#type_Hash) of the binary
[Destinations](#struct_Destination) of
the peers. This hash must be computed by the tracker, unless destination
enforcement (see below) is used, in which case the hash delivered in the
X-I2P-DestHash or X-I2P-DestB32 HTTP headers may be converted to binary
and stored. The peers key may be absent, or the peers value may be
zero-length.

Embora o suporte de resposta compacta seja opcional para clientes e
rastreadores, ele é altamente recomendado, pois reduz o tamanho nominal
da resposta em mais de 90%.

## Aplicação do Destino

Some, but not all, I2P bittorrent clients announce over their own
tunnels. Trackers may choose to prevent spoofing by requiring this, and
verifying the client\'s
[Destination](#struct_Destination)
using HTTP headers added by the I2PTunnel HTTP Server tunnel. The
headers are X-I2P-DestHash, X-I2P-DestB64, and X-I2P-DestB32, which are
different formats for the same information. These headers cannot be
spoofed by the client. A tracker enforcing destinations need not require
the ip announce parameter at all.

Como vários clientes usam o proxy HTTP em vez de seu próprio túnel para
anúncios, a imposição de destino impedirá o uso por esses clientes, a
menos que ou até que esses clientes sejam convertidos para anúncios em
seu próprio túnel.

Infelizmente, à medida que a rede cresce, a quantidade de malícia também
cresce, então esperamos que todos os rastreadores eventualmente imponham
destinos. Tanto os desenvolvedores de rastreadores quanto os de clientes
devem prever isso.

## Anunciar nomes de anfitriões

Announce URL host names in torrent files generally follow the [I2P
naming standards](). In addition to host names
from address books and \".b32.i2p\" Base 32 hostnames, the full Base 64
Destination (with \[or without?\] \".i2p\" appended) should be
supported. Non-open trackers should recognize their own host name in any
of these formats.

Para preservar o anonimato, os clientes geralmente devem ignorar URLs de
anúncios não-I2P em arquivos torrent.

## Conexões dos Clientes

As conexões cliente-cliente usam o protocolo padrão sobre TCP. Não há
clientes I2P conhecidos que atualmente suportem comunicação uTP.

I2P uses 387+ byte
[Destinations](#struct_Destination)
for addresses, as explained above.

Se o cliente tiver apenas o hash do destino (como de uma resposta
compacta ou PEX), ele deverá executar uma pesquisa codificando-o com
Base 32, anexando \".b32.i2p\" e consultando o Serviço de Nomenclatura,
, que retornará o Destino completo, se disponível.

Se o cliente tiver o Destino completo de um peer recebido em uma
resposta não compacta, ele deverá usá-lo diretamente na configuração da
conexão. Não converta um Destino de volta para um hash Base 32 para
pesquisa, isso é bastante ineficiente.

## Prevenção entre redes

Para preservar o anonimato, clientes bittorrent I2P geralmente não
suportam anúncios não-I2P ou conexões de pares. Os outproxies HTTP I2P
geralmente bloqueiam anúncios. Não há outproxies SOCKS conhecidos que
suportem tráfego bittorrent.

Para evitar o uso por clientes não I2P por meio de um proxy HTTP, os
rastreadores I2P geralmente bloqueiam acessos ou anúncios que contêm um
cabeçalho HTTP X-Forwarded-For. Os rastreadores devem rejeitar anúncios
de rede padrão com IPs IPv4 ou IPv6 e não entregá-los em respostas.

## PEX

I2P PEX is based on ut_pex. As there does not appear to be a formal
specification of ut_pex available, it may be necessary to review the
libtorrent source for assistance. It is an extension message, identified
as \"i2p_pex\" in [the extension
handshake](http://www.bittorrent.org/beps/bep_0010.html). It contains a
bencoded dictionary with up to 3 keys, \"added\", \"added.f\", and
\"dropped\". The added and dropped values are each a single byte string,
whose length is a multiple of 32 bytes. These byte strings are the
concatenated SHA-256 Hashes of the binary
[Destinations](#struct_Destination) of
the peers. This is the same format as the peers dictionary value in the
i2p compact response format specified above. The added.f value, if
present, is the same as in ut_pex.

## DHT

O suporte a DHT está incluído no cliente i2psnark a partir da versão
0.9.2. As diferenças preliminares de [BEP
5](http://www.bittorrent.org/beps/bep_0005.html) são descritas abaixo e
estão sujeitas a alterações. Entre em contato com os desenvolvedores do
I2P se desejar desenvolver um cliente com suporte a DHT.

Diferentemente do DHT padrão, o I2P DHT não usa um bit no handshake de
opções ou na mensagem PORT. Ele é anunciado com uma mensagem de
extensão, identificada como \"i2p_dht\" em [o handshake de
extensão](http://www.bittorrent.org/beps/bep_0010.html). Ele contém um
dicionário codificado com duas chaves, \"port\" e \"rport\", ambas
inteiras.



The UDP (datagram) port listed in the compact node info is used to
receive repliable (signed) datagrams. This is used for queries, except
for announces. We call this the \"query port\". This is the \"port\"
value from the extension message. Queries use
[I2CP]() protocol number 17.

In addition to that UDP port, we use a second datagram port equal to the
query port + 1. This is used to receive unsigned (raw) datagrams for
replies, errors, and announces. This port provides increased efficiency
since replies contain tokens sent in the query, and need not be signed.
We call this the \"response port\". This is the \"rport\" value from the
extension message. It must be 1 + the query port. Responses and
announces use [I2CP]() protocol number 18.

As informações compactas de peer são 32 bytes (hash SHA256 de 32 bytes)
em vez de 4 bytes de IP + 2 bytes de porta. Não há porta de peer. Em uma
resposta, a chave \"values\" é uma lista de strings, cada uma contendo
uma única informação compacta de peer.

As informações do nó compacto têm 54 bytes (ID do nó de 20 bytes + Hash
SHA256 de 32 bytes + porta de 2 bytes) em vez de ID do nó de 20 bytes +
IP de 4 bytes + porta de 2 bytes. Em uma resposta, a chave \"nodes\" é
uma string de byte único com informações do nó compacto concatenadas.

Requisito de ID de nó seguro: para dificultar vários ataques DHT, os
primeiros 4 bytes do ID do nó devem corresponder aos primeiros 4 bytes
do hash de destino, e os próximos dois bytes do ID do nó devem
corresponder aos próximos dois bytes do hash de destino em OR exclusivo
com a porta.

Em um arquivo torrent, a chave \"nodes\" do dicionário torrent sem
rastreador é TBD. Poderia ser uma lista de strings binárias de 32 bytes
(hashes SHA256) em vez de uma lista de listas contendo uma string de
host e um inteiro de porta. Alternativas: Uma string de byte único com
hashes concatenados, ou uma lista de strings sozinhas.

## Rastreadores de Datagrama (UDP)

O suporte ao rastreador UDP em clientes e rastreadores ainda não está
disponível. As diferenças preliminares de [BEP
15](http://www.bittorrent.org/beps/bep_0015.html) são descritas abaixo e
estão sujeitas a alterações. Entre em contato com os desenvolvedores do
I2P se desejar desenvolver um cliente ou rastreador que suporte anúncios
de datagramas.

See [Proposal 160]().

## Informação Adicional

- I2P bittorrent standards are generally discussed on [](http:///).
- A chart of current tracker software capabilities is [also available
 there](http:///files/trackers.html).
- The [I2P bittorrent
 FAQ](http:///viewtopic.php?t=2068)
- [DHT on I2P discussion](http:///topics/812)


