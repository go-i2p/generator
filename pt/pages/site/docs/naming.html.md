 Nomenclatura e
Catálogo de Endereços 2025-01 0.9.65 

## Sinopse {#overview}

O I2P vem com uma biblioteca de nomenclatura genérica e uma
implementação base projetada para trabalhar com um mapeamento de nome
local para destino, bem como um aplicativo complementar chamado de
[catálogo de endereços](#addressbook). O I2P também oferece suporte a
[nomes de host Base32](#base32) semelhantes aos endereços .onion do Tor.

O catálogo de endereços é um sistema de nomenclatura seguro, distribuído
e legível por humanos, conduzido por uma rede de confiança ,
sacrificando apenas a chamada para que todos os nomes legíveis por
humanos sejam globalmente únicos, exigindo apenas a exclusividade local.
Enquanto todas as mensagens no I2P são criptograficamente endereçadas
por seu destino, pessoas diferentes podem ter entradas no catálogo de
endereços local para \"Alice\" que se referem a destinos diferentes. As
pessoas ainda podem descobrir novos nomes importando catálogos de
endereços publicados de pares especificados em sua rede de confiança,
adicionando as entradas fornecidas por terceiros ou (se algumas pessoas
organizarem uma série de catálogos de endereços publicados usando um
sistema de registro por ordem de chegada ) as pessoas podem escolher
tratar esses catálogos de endereços como servidores de nomes, emulando o
DNS tradicional.

NOTE: For the reasoning behind the I2P naming system, common arguments
against it and possible alternatives see the [naming
discussion]() page.

## Componentes do Sistema de nomes {#components}

Não há qualquer autoridade de nomes centralizada na I2P. Todos os nomes
de hosts são locais.

O sistema de nomenclatura é bem simples e a maioria disso é implementada
em aplicações externas ao roteador, mas empacotada com o distribuidor
I2P. Os componentes são:

1. O serviço de nomenclatura local [](#lookup) que faz pesquisas e
 também manipula [nomes de host Base32](#base32).
2. O proxy HTTP [](#httpproxy) que solicita pesquisas ao roteador e
 aponta o usuário para serviços de salto remoto para auxiliar com
 pesquisas com falha.
3. HTTP [formulários de adição de host](#add-services) que permitem que
 os usuários adicionem hosts ao seu hosts.txt local
4. Serviços de salto HTTP [](#jump-services) que fornecem suas próprias
 pesquisas e redirecionamentos.
5. O aplicativo [do catálogo de endereços](#addressbook) que mescla
 listas de hosts externos , recuperadas via HTTP, com a lista local.
6. O aplicativo [SusiDNS](#susidns) que é um front-end web simples para
 configuração do catálogo de endereços e visualização das listas de
 hosts locais.

## Naming Services {#lookup}

All destinations in I2P are 516-byte (or longer) keys. (To be more
precise, it is a 256-byte public key plus a 128-byte signing key plus a
3-or-more byte certificate, which in Base64 representation is 516 or
more bytes. Non-null
[Certificates](#certificates) are in
use now for signature type indication. Therefore, certificates in
recently-generated destinations are more than 3 bytes.

Se um aplicativo (i2ptunnel ou proxy HTTP) deseja acessar um destino
pelo nome, o roteador faz uma pesquisa local muito simples para resolver
esse nome.

### Hosts.txt Naming Service

O serviço de nomenclatura hosts.txt faz uma busca linear simples por
arquivos de texto. Esse serviço de nomenclatura era o padrão até release
0.8.8 quando foi substituído pelo serviço de nomenclatura Blockfile. O
formato hosts.txt ficou muito lento depois que o arquivo cresceu para
milhares de entradas.

It does a linear search through three local files, in order, to look up
host names and convert them to a 516-byte destination key. Each file is
in a simple [configuration file
format](), with hostname=base64, one per
line. The files are:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile Naming Service

O Blockfile Naming Service armazena vários \"catálogos de endereços\" em
um único arquivo de banco de dados chamado hostsdb.blockfile. Este
Naming Service é o padrão desde a versão 0.8.8.

A blockfile is simply on-disk storage of multiple sorted maps (key-value
pairs), implemented as skiplists. The blockfile format is specified on
the [Blockfile page](). It provides fast
Destination lookup in a compact format. While the blockfile overhead is
substantial, the destinations are stored in binary rather than in Base
64 as in the hosts.txt format. In addition, the blockfile provides the
capability of arbitrary metadata storage (such as added date, source,
and comments) for each entry to implement advanced address book
features. The blockfile storage requirement is a modest increase over
the hosts.txt format, and the blockfile provides approximately 10x
reduction in lookup times.

Na criação, o serviço de nomenclatura importa entradas dos três arquivos
usados pelo serviço de nomenclatura hosts.txt. O arquivo de bloco imita
a implementação anterior, mantendo três mapas que são pesquisados em
ordem, chamados privatehosts.txt, userhosts.txt e hosts.txt. Ele também
mantém um mapa de pesquisa reversa para implementar pesquisas reversas
rápidas.

### Other Naming Service Facilities

The lookup is case-insensitive. The first match is used, and conflicts
are not detected. There is no enforcement of naming rules in lookups.
Lookups are cached for a few minutes. Base 32 resolution is [described
below](#base32). For a full description of the Naming Service API see
the [Naming Service Javadocs](). This API
was significantly expanded in release 0.8.7 to provide adds and removes,
storage of arbitrary properties with the hostname, and other features.

### Alternatives and Experimental Naming Services

The naming service is specified with the configuration property
`i2p.naming.impl=class`. Other implementations are possible. For
example, there is an experimental facility for real-time lookups (a la
DNS) over the network within the router. For more information see the
[alternatives on the discussion
page](#alternatives).

O proxy HTTP faz uma pesquisa por meio do roteador para todos os nomes
de host que terminam em \'.i2p\'. Caso contrário, ele encaminha a
solicitação para um proxy HTTP configurado. Assim, na prática, todos os
nomes de host HTTP (Site I2P) devem terminar no pseudo-Domínio de Nível
Superior \'.i2p\'.

Se o roteador não conseguir resolver o nome do host, o proxy HTTP
retornará uma página de erro ao usuário com links para vários serviços
de \"jump\". Veja abaixo os detalhes.

## .i2p.alt Domain {#alt}

We previously [applied to reserve the .i2p
TLD](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/)
following the procedures specified in [RFC
6761](https://www.rfc-editor.org/rfc/rfc6761.html). However, this
application and all others were rejected, and RFC 6761 was declared a
\"mistake\".

After many years of work by the GNUnet team and others, the .alt domain
was reserved as a special-use TLD in [RFC
9476](https://www.rfc-editor.org/rfc/rfc9476.html) as of late 2023.
While there are no official registrars sanctioned by IANA, we have
registered the .i2p.alt domain with the primary unofficial registrar
[GANA](https://gana.gnunet.org/dot-alt/dot_alt.html). This does not
prevent others from using the domain, but it should help discourage it.

One benefit to the .alt domain is that, in theory, DNS resolvers will
not forward .alt requests once they update to comply with RFC 9476, and
that will prevent DNS leaks. For compatibility with .i2p.alt hostnames,
I2P software and services should be updated to handle these hostnames by
stripping off the .alt TLD. These updates are scheduled for the first
half of 2024.

At this time, there are no plans to make .i2p.alt the preferred form for
display and interchange of I2P hostnames. This is a topic for further
research and discussion.

## Lista de Endereços {#addressbook}

### Assinaturas de entrada e fusão

O aplicativo de catálogo de endereços periodicamente recupera os
arquivos hosts.txt de outros usuários e os mescla com o hosts.txt local,
após várias verificações. Os conflitos de nomenclatura são resolvidos
por ordem de chegada .

Assinar o arquivo hosts.txt de outro usuário envolve dar a ele uma certa
quantidade de confiança. Você não quer que eles, por exemplo,
\'sequestrem\' um novo site inserindo rapidamente sua própria chave para
um novo site antes de passar a nova entrada de host/chave para você.

Por esse motivo, a única assinatura configurada por padrão é
`http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`,
que contém uma cópia do hosts.txt incluído na versão I2P. Os usuários
devem configurar assinaturas adicionais em seu aplicativo de catálogo de
endereços local (via subscriptions.txt ou [SusiDNS](#susidns)).

Alguns outros links de assinatura do catálogo de endereços público:

- [http:///cgi-bin/i2hostetag](http:///cgi-bin/i2hostetag)
- [http:///cgi-bin/newhosts.txt](http:///cgi-bin/newhosts.txt)

Os operadores desses serviços podem ter várias políticas para listar
hosts. A presença nesta lista não implica endosso.

### Regras de atribuição de nomes

Embora não haja nenhuma limitação técnica no I2P em nomes de host, o
catálogo de endereços impõe várias restrições em nomes de host
importados de assinaturas. Ele faz isso para sanidade tipográfica básica
e compatibilidade com navegadores, e por segurança. As regras são
essencialmente as mesmas da Seção 3.2.2 do RFC2396. Quaisquer nomes de
host que violem essas regras não podem ser propagados para outros
roteadores.

Regras de atribuição de nomes:

- Nomes são convertidos para caixa baixa na importação.
- Os nomes são verificados quanto a conflitos com nomes existentes nos
 arquivos userhosts.txt e hosts.txt (mas não privatehosts.txt) após a
 conversão para letras minúsculas.
- Deve conter apenas \[a-z\] \[0-9\] \'.\' e \'-\' após conversão para
 caixa baixa
- Não pode começar com \'.\' ou \'-\'
- Deve terminar com \'.i2p\'.
- No máximo 67 caractéres, incluindo o \'.i2p\'.
- Não pode conter \'..\'.
- Não pode conter \'.-\' ou \'-.\' (tal como 0.6.1.33).
- Não pode conter \'\--\' exceto em \'xn\--\' para IDN.
- Nomes de host Base32 (\*.b32.i2p) são reservados para uso em base 32
 e, portanto, não podem ser importados.
- Certain hostnames reserved for project use are not allowed
 (proxy.i2p, router.i2p, console.i2p, mail.i2p, \*.proxy.i2p,
 \*.router.i2p, \*.console.i2p, \*.mail.i2p, and others)
- Hostnames starting with \'www.\' are discouraged and are rejected by
 some registration services. Some addressbook implementations
 automatically strip \'www.\' prefixes from lookups. So registring
 \'www.example.i2p\' is unnecessary, and registering a different
 destination for \'www.example.i2p\' and \'example.i2p\' will make
 \'www.example.i2p\' unreachable for some users.
- Chaves são verificadas para validação base64.
- As chaves são verificadas quanto a conflitos com chaves existentes
 em hosts.txt (mas não em privatehosts.txt).
- Tamanho mínimo da chave é 516 bytes.
- Comprimento máximo da chave: 616 bytes (para contabilizar
 certificados de até 100 bytes).

Qualquer nome recebido por assinatura que passe em todas as verificações
é adicionado por meio do serviço de nomenclatura local.

Observe que os símbolos \'.\' em um nome de host não têm importância, e
não denotam nenhuma nomenclatura real ou hierarquia de confiança. Se o
nome \'host.i2p\' já existir, não há nada que impeça alguém de adicionar
um nome \'a.host.i2p\' ao seu hosts.txt, e esse nome pode ser importado
pelo catálogo de endereços de outras pessoas. Métodos para negar
subdomínios a \'proprietários\' não pertencentes ao domínio
(certificados?), e a conveniência e viabilidade desses métodos, são
tópicos para discussão futura.

Nomes de Domínio Internacionais (IDN) também funcionam em i2p (usando o
formato punycode \'xn\--\'). Para ver nomes de domínio IDN .i2p
renderizados corretamente na barra de localização do Firefox, adicione
\'network.IDN.whitelist.i2p (boolean) = true\' em about:config.

Como o aplicativo de catálogo de endereços não usa privatehosts.txt, na
prática este arquivo é o único lugar onde é apropriado colocar aliases
privados ou \"nomes de estimação\" para sites que já estejam em
hosts.txt.

### Formato de feed de assinatura avançado

As of release 0.9.26, subscription sites and clients may support an
advanced hosts.txt feed protocol that includes metadata including
signatures. This format is backwards-compatible with the standard
hosts.txt hostname=base64destination format. See [the
specification](/spec/subscription) for details.

### Assinaturas de saída

O Catálogo de Endereços publicará o hosts.txt mesclado em um local
(tradicionalmente hosts.txt no diretório inicial do site I2P local) para
ser acessado por outros para suas assinaturas. Esta etapa é opcional e
está desabilitada por padrão.

### Hosting and HTTP Transport Issues

O aplicativo de catálogo de endereços, juntamente com o eepget, salva as
informações de Etag e/ou Última modificação retornadas pelo servidor web
da assinatura. Isso reduz muito a largura de banda necessária, pois o
servidor web retornará um \'304 Não modificado\' na próxima busca se
nada tiver sido alterado.

No entanto, todo o arquivo hosts.txt será baixado caso tenha sido
alterado. Veja abaixo a discussão sobre esse problema.

Hosts que servem um hosts.txt estático ou um aplicativo CGI equivalente
são fortemente encorajados a entregar um cabeçalho Content-Length e um
cabeçalho Etag ou Last-Modified. Certifique-se também de que o servidor
entregue um \'304 Not Modified\' quando apropriado. Isso reduzirá
drasticamente a largura de banda da rede e reduzirá as chances de
corrupção.

## Serviços de Adição de Anfitrião {#add-services}

Um serviço de adição de host é um aplicativo CGI simples que recebe um
nome de host e uma chave Base64 como parâmetros e os adiciona ao seu
hosts.txt local. Se outros roteadores assinarem esse hosts.txt, o novo
nome de host/chave será propagado pela rede.

É recomendável que os serviços de adição de host imponham, no mínimo, as
restrições impostas pelo aplicativo de catálogo de endereços listado
acima. Os serviços de adição de host podem impor restrições adicionais
em nomes de host e chaves, por exemplo:

- Um limite para o número de \'subdomínios\'.
- Autorização para \'subdomínios\' através de diversos metódos.
- Hashcash ou certificados assinados.
- Revisão editorial de nomes de hosts e/ou conteúdo.
- Categorização de anfitriões por conteúdo.
- Reserva ou rejeição de determinados nomes de hosts.
- Restrições quanto ao número de nomes registrados em um dado período
 de tempo.
- Intervalos entre o registro e a publicação.
- Exigência de que o host esteja disponível para verificação.
- Expiração e/ou revogação.
- Rejeição de falsificação de IDN.

## Serviços de saltos {#jump-services}

Um serviço de salto é um aplicativo CGI simples que recebe um nome de
host como parâmetro e retorna um redirecionamento 301 para a URL
adequada com uma string `?i2paddresshelper=key` anexada. O proxy HTTP
interpretará a string anexada e usará essa chave como o destino real.
Além disso, o proxy armazenará em cache essa chave para que o auxiliar
de endereço não seja necessário até a reinicialização.

Observe que, assim como acontece com as assinaturas, usar um serviço de
salto implica um certo nível de confiança, pois um serviço de salto
poderia maliciosamente redirecionar um usuário para um destino
incorreto.

Para fornecer o melhor serviço, um serviço de salto deve ser assinado em
vários provedores hosts.txt para que sua lista de hosts locais esteja
atualizada.

## SusiDNS

SusiDNS é simplesmente uma interface web front-end para configurar
assinaturas do catálogo de endereços e acessar os quatro arquivos do
catálogo de endereços. Todo o trabalho real é feito pelo aplicativo
\'catálogo de endereços\'.

Atualmente, há pouca aplicação de regras de nomenclatura de catálogo de
endereços no SusiDNS, então um usuário pode inserir nomes de host
localmente que seriam rejeitados pelas regras de assinatura do catálogo
de endereços.

## Nomes de Base32 {#base32}

O I2P suporta nomes de host Base32 semelhantes aos endereços .onion do
Tor. Os endereços Base32 são muito mais curtos e fáceis de manusear do
que os Destinos Base64 completos de 516 caracteres ou addresshelpers.
Exemplo: `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

No Tor, o endereço tem 16 caracteres (80 bits), ou metade do hash SHA-1.
O I2P usa 52 caracteres (256 bits) para representar o hash SHA-256
completo. O formato é {52 chars}.b32.i2p. O Tor tem uma
[proposta](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013)
para converter para um formato idêntico de {52 chars}.onion para seus
serviços ocultos. O Base32 é implementado no serviço de nomenclatura,
que consulta o roteador pelo I2CP para procurar o LeaseSet e obter o
Destino completo. As pesquisas em Base32 só serão bem-sucedidas quando o
Destino estiver ativo e publicando um LeaseSet. Como a resolução pode
exigir uma pesquisa no banco de dados de rede, ela pode levar
significativamente mais tempo do que uma pesquisa no catálogo de
endereços local.

Endereços Base32 podem ser usados na maioria dos lugares onde nomes de
host ou destinos completos são usados, no entanto, há algumas exceções
onde eles podem falhar se o nome não for resolvido imediatamente. O
I2PTunnel falhará, por exemplo, se o nome não for resolvido para um
destino.

## Extended Base32 Names {#newbase32}

Extended base 32 names were introduced in release 0.9.40 to support
encrypted lease sets. Addresses for encrypted leasesets are identified
by 56 or more encoded characters, not including the \".b32.i2p\" (35 or
more decoded bytes), compared to 52 characters (32 bytes) for
traditional base 32 addresses. See proposals 123 and 149 for additional
information.

Standard Base 32 (\"b32\") addresses contain the hash of the
destination. This will not work for encrypted ls2 (proposal 123).

You can\'t use a traditional base 32 address for an encrypted LS2
(proposal 123), as it contains only the hash of the destination. It does
not provide the non-blinded public key. Clients must know the
destination\'s public key, sig type, the blinded sig type, and an
optional secret or private key to fetch and decrypt the leaseset.
Therefore, a base 32 address alone is insufficient. The client needs
either the full destination (which contains the public key), or the
public key by itself. If the client has the full destination in an
address book, and the address book supports reverse lookup by hash, then
the public key may be retrieved.

So we need a new format that puts the public key instead of the hash
into a base32 address. This format must also contain the signature type
of the public key, and the signature type of the blinding scheme.

This section documents a new b32 format for these addresses. While we
have referred to this new format during discussions as a \"b33\"
address, the actual new format retains the usual \".b32.i2p\" suffix.

### Creation and encoding

Construct a hostname of {56+ chars}.b32.i2p (35+ chars in binary) as
follows. First, construct the binary data to be base 32 encoded:

 flag (1 byte)
 bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
 bit 1: 0 for no secret, 1 if secret is required
 bit 2: 0 for no per-client auth,
 1 if client private key is required
 bits 7-3: Unused, set to 0

 public key sigtype (1 or 2 bytes as indicated in flags)
 If 1 byte, the upper byte is assumed zero

 blinded key sigtype (1 or 2 bytes as indicated in flags)
 If 1 byte, the upper byte is assumed zero

 public key
 Number of bytes as implied by sigtype

Post-processing and checksum:

 Construct the binary data as above.
 Treat checksum as little-endian.
 Calculate checksum = CRC-32(data[3:end])
 data[0] ^= (byte) checksum
 data[1] ^= (byte) (checksum >> 8)
 data[2] ^= (byte) (checksum >> 16)

 hostname = Base32.encode(data) || ".b32.i2p"

Any unused bits at the end of the b32 must be 0. There are no unused
bits for a standard 56 character (35 byte) address.

### Decoding and Verification

 Strip the ".b32.i2p" from the hostname
 data = Base32.decode(hostname)
 Calculate checksum = CRC-32(data[3:end])
 Treat checksum as little-endian.
 flags = data[0] ^ (byte) checksum
 if 1 byte sigtypes:
 pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
 blinded sigtype = data[2] ^ (byte) (checksum >> 16)
 else (2 byte sigtypes) :
 pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
 blinded sigtype = data[3] || data[4]
 parse the remainder based on the flags to get the public key

### Secret and Private Key Bits

The secret and private key bits are used to indicate to clients,
proxies, or other client-side code that the secret and/or private key
will be required to decrypt the leaseset. Particular implementations may
prompt the user to supply the required data, or reject connection
attempts if the required data is missing.

### Notes

- XORing first 3 bytes with the hash provides a limited checksum
 capability, and ensures that all base32 chars at the beginning are
 randomized. Only a few flag and sigtype combinations are valid, so
 any typo is likely to create an invalid combination and will be
 rejected.
- In the usual case (1 byte sigtypes, no secret, no per-client auth),
 the hostname will be {56 chars}.b32.i2p, decoding to 35 bytes, same
 as Tor.
- Tor 2-byte checksum has a 1/64K false negative rate. With 3 bytes,
 minus a few ignored bytes, ours is approaching 1 in a million, since
 most flag/sigtype combinations are invalid.
- Adler-32 is a poor choice for small inputs, and for detecting small
 changes. We use CRC-32 instead. CRC-32 is fast and is widely
 available.
- While outside the scope of this specification, routers and/or
 clients must remember and cache (probably persistently) the mapping
 of public key to destination, and vice versa.
- Distinguish old from new flavors by length. Old b32 addresses are
 always {52 chars}.b32.i2p. New ones are {56+ chars}.b32.i2p
- Tor discussion thread [is
 here](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- Don\'t expect 2-byte sigtypes to ever happen, we\'re only up to 13.
 No need to implement now.
- New format can be used in jump links (and served by jump servers) if
 desired, just like b32.
- Any secret, private key, or public key longer than 32 bytes would
 exceed the DNS max label length of 63 chars. Browsers probably do
 not care.
- No backward compatibility issues. Longer b32 addresses will fail to
 be converted to 32-byte hashes in old software.


