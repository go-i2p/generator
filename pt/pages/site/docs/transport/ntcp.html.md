 NTCP (TCP baseado
em NIO) 2021-10 0.9.52 

DEPRECATED, NO LONGER SUPPORTED. Disabled by default as of 0.9.40
2019-05. Support removed as of 0.9.50 2021-05. Replaced by
[NTCP2](). NTCP is a Java NIO-based transport
introduced in I2P release 0.6.1.22. Java NIO (new I/O) does not suffer
from the 1 thread per connection issues of the old TCP transport.
NTCP-over-IPv6 is supported as of version 0.9.8.

Por padrão, o NTCP usa o IP/Porta detectado automaticamente pelo SSU.
Quando habilitado no config.jsp, o SSU notificará/reiniciará o NTCP
quando o endereço externo mudar ou quando o status do firewall mudar.
Agora você pode habilitar o TCP de entrada sem um IP estático ou serviço
dyndns.

O código NTCP dentro do I2P é relativamente leve (1/4 do tamanho do
código SSU) porque ele usa o transporte Java TCP subjacente para entrega
confiável.

## [Especificação do Endereço do Roteador]{#ra}

As propriedades a seguir são armazenadas no banco de dados da rede.

- **Transport name:** NTCP
- **host:** IP (IPv4 or IPv6). Shortened IPv6 address (with \"::\") is
 allowed. Host names were previously allowed, but are deprecated as
 of release 0.9.32. See proposal 141.
- **port:** 1024 - 65535

## Especificação do Protocolo NTCP

### Formato de Mensagem Padrão

Após o estabelecimento, o transporte NTCP envia mensagens I2NP
individuais, com uma soma de verificação simples. A mensagem não
criptografada é codificada da seguinte forma:


+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+
\| sizeof(data) \| \| +\-\-\-\-\-\--+\-\-\-\-\-\--+ + \| data \| \~ \~
\| \| + +\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+ \| \| padding
+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+
\| Adler checksum of sz+data+pad \|
+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+


Os dados são então criptografados AES/256/CBC. A chave de sessão para a
criptografia é negociada durante o estabelecimento (usando
Diffie-Hellman 2048 bits). O estabelecimento entre dois roteadores é
implementado na classe EstablishState e detalhado abaixo. O IV para
criptografia AES/256/CBC são os últimos 16 bytes da mensagem
criptografada anterior.

São necessários 0 a 15 bytes de preenchimento para levar o comprimento
total da mensagem (incluindo os seis bytes de tamanho e soma de
verificação) a um múltiplo de 16. O tamanho máximo da mensagem
atualmente é 16 KB. Portanto, o tamanho máximo dos dados atualmente é 16
KB - 6, ou 16378 bytes. O tamanho mínimo dos dados é 1.

### Formato de mensagem de sincronização de tempo

Um caso especial é uma mensagem de metadados onde o sizeof(data) é 0.
Nesse caso, a mensagem não criptografada é codificada como:


+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+
\| 0 \| timestamp in seconds \| uninterpreted
+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+
uninterpreted \| Adler checksum of bytes 0-11 \|
+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+


Comprimento total: 16 bytes. A mensagem de sincronização de tempo é
enviada em intervalos de aproximadamente 15 minutos. A mensagem é
criptografada assim como as mensagens padrão.

### Checksums

The standard and time sync messages use the Adler-32 checksum as defined
in the [ZLIB Specification]().

### Tempo limite ocioso

O tempo limite de inatividade e o fechamento da conexão ficam a critério
de cada ponto de extremidade e podem variar. A implementação atual
diminui o tempo limite à medida que o número de conexões se aproxima do
máximo configurado e aumenta o tempo limite quando a contagem de
conexões é baixa. O tempo limite mínimo recomendado é de dois minutos ou
mais, e o tempo limite máximo recomendado é de dez minutos ou mais.

### Troca de informações do roteador

Após o estabelecimento, e a cada 30-60 minutos depois disso, os dois
roteadores geralmente devem trocar RouterInfos usando uma
DatabaseStoreMessage. No entanto, Alice deve verificar se a primeira
mensagem na fila é uma DatabaseStoreMessage para não enviar uma mensagem
duplicada; esse geralmente é o caso ao se conectar a um roteador
floodfill.

### Sequência de Estabelecimento

No estado estabelecido, há uma sequência de mensagens de 4 fases para
trocar chaves DH e assinaturas. Nas duas primeiras mensagens, há uma
troca Diffie Hellman de 2048 bits. Então, as assinaturas dos dados
críticos são trocadas para confirmar a conexão.

 Alice contacts Bob
========================================================= X+(H(X) xor
Bob.identHash)\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--Y+E(H(X+Y)+tsB+padding,
sk, Y\[239:255\])
E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk,
hX_xor_Bob.identHash\[16:31\])\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--E(S(X+Y+Alice.identHash+tsA+tsB)+padding,
sk, prev) 


 Legenda:
 X, Y: chave pública DH de 256 byte
 H(): 32 byte SHA256 Hash
 E(data, session key, IV): AES256 Encrypt
 S(): Signature
 tsA, tsB: carimbos de data/hora (4 bytes, segundos desde a época)
 sk: Chave de Sessão de 32 byte
 sz: Tamanho de 2 bytes da identidade de Alice a seguir

#### Troca de Chave DH {#DH}

The initial 2048-bit DH key exchange uses the same shared prime (p) and
generator (g) as that used for I2P\'s [ElGamal
encryption](#elgamal).

A troca de chaves DH consiste em uma série de etapas, exibidas abaixo. O
mapeamento entre essas etapas e as mensagens enviadas entre roteadores
I2P, está marcado em negrito.

1. Alice gera um inteiro secreto x. Ela então calcula `X = g^x mod p`.
2. Alice envia X para Bob **(Mensagem 1)**.
3. Bob gera um numeral secreto y. Ele então calcula `Y = g^y mod p`.
4. Bob envia Y para Alice **(Mensagem 2)**.
5. Alice agora pode calcular `sessionKey = Y^x mod p`.
6. Bob agora pode calcular `sessionKey = X^y mod p`.
7. Agora Alice e Bob tem uma chave compartilhada
 `sessionKey = g^(x*y) mod p`.

The sessionKey is then used to exchange identities in **Message 3** and
**Message 4**. The exponent (x and y) length for the DH exchange is
documented on the [cryptography
page](#exponent).

#### Session Key Details

The 32-byte session key is created as follows:

1. Take the exchanged DH key, represented as a positive minimal-length
 BigInteger byte array (two\'s complement big-endian)
2. If the most significant bit is 1 (i.e. array\[0\] & 0x80 != 0),
 prepend a 0x00 byte, as in Java\'s BigInteger.toByteArray()
 representation
3. If that byte array is greater than or equal to 32 bytes, use the
 first (most significant) 32 bytes
4. If that byte array is less than 32 bytes, append 0x00 bytes to
 extend to 32 bytes. *(vanishingly unlikely)*

#### Mensagem 1 (Requisição de Sessão)

This is the DH request. Alice already has Bob\'s [Router
Identity](#struct_RouterIdentity), IP
address, and port, as contained in his [Router
Info](#struct_RouterInfo), which was
published to the [network database](). Alice
sends Bob:

 X+(H(X) xor
Bob.identHash)\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
Tamanho: 288 bytes 

Conteúdo:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| X,
as calculated from DH \| + + \| \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| HXxorHI \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ X ::
256 byte X de Diffie Hellman HXxorHI :: SHA256 Hash(X) \'xor\'arizado
com SHA256 Hash(\'Identidade do Roteador\'de Bob) (32 bytes) 

**Notas:**

- Bob verifica HXxorHI usando seu próprio hash de roteador. Se não
 verificar, Alice contatou o roteador errado, e Bob interrompe a
 conexão.

#### Mensagem 2 (Sessão Criada)

Esta é a resposta DH. Bob manda para Alice:


\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--Y+E(H(X+Y)+tsB+padding,
sk, Y\[239:255\]) Tamanho: 304 bytes 

Conteúdo Não Criptografado:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| Y
as calculated from DH \| + + \| \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| HXY \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| tsB
\| padding \| +\-\-\--+\-\-\--+\-\-\--+\-\-\--+ + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ Y ::
256 byte Y de Diffie Hellman HXY :: SHA256 Hash(X concatenado com Y) (32
bytes) tsB :: Carimbo de data/hora de 4 bytes (segundos desde a época)
padding :: 12 bytes de dados rand6omicos 

Conteúdo Criptografado:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| Y
as calculated from DH \| + + \| \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| encrypted data \| + + \| \| + + \| \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 


 Y: 256 byte Y de Diffie Hellman

 encrypted data: 48 bytes AES encrypted using the DH session key and
 the last 16 bytes of Y as the IV

**Notas:**

- Alice may drop the connection if the clock skew with
 Bob is too high as calculated using tsB.

#### Mensagem 3 (Confirmação de Sessão A)

Isto contém a identidade do roteador de Alice e uma assinatura dos dados
críticos. Alice envia a Bob:


E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk,
hX_xor_Bob.identHash\[16:31\])\-\--\> Tamanho: 448 bytes (typ. for 387
byte identity and DSA signature), see notes below 

Conteúdo Não Criptografado:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| sz
\| Alice\'s Router Identity \| +\-\-\--+\-\-\--+ + \| \| \~ . . . \~ \|
\| + +\-\-\--+\-\-\--+\-\-\--+ \| \| tsA
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
padding \| +\-\-\--+ + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| signature \| + + \| \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ sz ::
Tamanho de 2 bytes da identidade do roteador de Alice a seguir (387+)
ident :: \`RouterIdentity\` de 387+ bytes de Alice tsA :: Carimbo de
data/hora de 4 bytes (segundos desde a época) padding :: 0-15 bytes de
dados aleatórios signature :: a \`Assinatura\` dos seguintes dados
concatenados: X, Y, \`RouterIdentity\` de Bob, tsA, tsB. Alice assina
com a \`SigningPrivateKey\` associada à \`SigningPublicKey\` em sua
\`RouterIdentity\` 

Conteúdo Criptografado:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| encrypted data \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 


 encrypted data: 448 bytes AES encrypted using the DH session key and
 the last 16 bytes of HXxorHI (i.e., the last 16 bytes of message #1) as the IV
 448 is the typical length, but it could be longer, see below.

**Notas:**

- Bob verifica a assinatura e, em caso de falha, interrompe a conexão.
- Bob pode interromper a conexão se o desvio de clock com Alice for
 muito alto, conforme calculado usando tsA.
- Alice usará os últimos 16 bytes do conteúdo criptografado desta
 mensagem como IV para a próxima mensagem.
- Through release 0.9.15, the router identity was always 387 bytes,
 the signature was always a 40 byte DSA signature, and the padding
 was always 15 bytes. As of release 0.9.16, the router identity may
 be longer than 387 bytes, and the signature type and length are
 implied by the type of the [Signing Public
 Key](#type_SigningPublicKey)
 in Alice\'s [Router
 Identity](#struct_RouterIdentity).
 The padding is as necessary to a multiple of 16 bytes for the entire
 unencrypted contents.
- The total length of the message cannot be determined without
 partially decrypting it to read the Router Identity. As the minimum
 length of the Router Identity is 387 bytes, and the minimum
 Signature length is 40 (for DSA), the minimum total message size is
 2 + 387 + 4 + (signature length) + (padding to 16 bytes), or 2 +
 387 + 4 + 40 + 15 = 448 for DSA. The receiver could read that
 minimum amount before decrypting to determine the actual Router
 Identity length. For small Certificates in the Router Identity, that
 will probably be the entire message, and there will not be any more
 bytes in the message to require an additional decryption operation.

#### Mensagem 4 (Confirmação de Sessão B)

Esta é uma assinatura dos dados críticos. Bob envia para Alice:

 \*
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--E(S(X+Y+Alice.identHash+tsA+tsB)+padding,
sk, prev) Tamanho: 48 bytes (typ. for DSA signature), see notes below 

Conteúdo Não Criptografado:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| signature \| + + \| \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
padding \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+
signature :: a \`Assinatura\` dos seguintes dados concatenados: X, Y,
\`RouterIdentity\` de Alice, tsA, tsB. Bob assina com a
\`SigningPrivateKey\` associada à \`SigningPublicKey\` em sua
\`RouterIdentity\` padding :: 0-15 bytes de dados aleatórios 

Conteúdo Criptografado:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| encrypted data \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 


 encrypted data: Data AES encrypted using the DH session key and
 the last 16 bytes of the encrypted contents of message #2 as the IV
 48 bytes for a DSA signature, may vary for other signature types

**Notes:**

- Alice verifica a assinatura e, em caso de falha, interrompe a
 conexão.
- Bob usará os últimos 16 bytes do conteúdo criptografado desta
 mensagem como IV para a próxima mensagem.
- Through release 0.9.15, the signature was always a 40 byte DSA
 signature and the padding was always 8 bytes. As of release 0.9.16,
 the signature type and length are implied by the type of the
 [Signing Public
 Key](#type_SigningPublicKey)
 in Bob\'s [Router
 Identity](#struct_RouterIdentity).
 The padding is as necessary to a multiple of 16 bytes for the entire
 unencrypted contents.

#### Após o estabelecimento

A conexão é estabelecida e mensagens de sincronização padrão ou de tempo
podem ser trocadas. Todas as mensagens subsequentes são criptografadas
com AES usando a chave de sessão DH negociada. Alice usará os últimos 16
bytes do conteúdo criptografado da mensagem nº 3 como o próximo IV. Bob
usará os últimos 16 bytes do conteúdo criptografado da mensagem nº 4
como o próximo IV.

### Verificar Mensagem de Conexão

Alternativamente, quando Bob recebe uma conexão, pode ser uma conexão de
verificação (talvez solicitada por Bob pedindo para alguém verificar seu
ouvinte). A conexão de verificação não está sendo usada no momento. No
entanto, para registro, as conexões de verificação são formatadas da
seguinte forma. Uma conexão de informações de verificação receberá 256
bytes contendo:

- 32 bytes de dado não interpretada, ignorado
- Tamanho de 1 byte
- que muitos bytes compõem o endereço IP do roteador local (conforme
 alcançado pelo lado remoto)
- Número de porta de 2 bytes em que o roteador local foi alcançado
- Tempo de rede i2p de 4 bytes conforme conhecido pelo lado remoto
 (segundos desde a época)
- dados de preenchimento não interpretados, até o byte 223
- xor do hash de identidade do roteador local e o SHA256 dos bytes 32
 a bytes 223

A verificação de conexão está completamente desabilitada a partir da
versão 0.9.12.

## Discussão

Now on the [NTCP Discussion Page]().

## [Trabalho futuro]{#future}

- O tamanho máximo da mensagem deve ser aumentado para aproximadamente
 32 KB.
- Um conjunto de tamanhos de pacotes fixos pode ser apropriado para
 ocultar ainda mais a fragmentação de dados para adversários
 externos, mas o túnel, o alho e o preenchimento de ponta a ponta
 devem ser suficientes para a maioria das necessidades até então. No
 entanto, atualmente não há nenhuma provisão para preenchimento além
 do próximo limite de 16 bytes, para criar um número limitado de
 tamanhos de mensagem.
- A utilização de memória (incluindo a do kernel) para NTCP deve ser
 comparada à do SSU.
- As mensagens de estabelecimento podem ser preenchidas aleatoriamente
 de alguma forma, para frustrar a identificação do tráfego I2P com
 base nos tamanhos iniciais dos pacotes?


