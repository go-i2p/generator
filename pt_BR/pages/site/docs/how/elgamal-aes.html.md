 Criptografia
ElGamal/AES + SessionTag April
2020 0.9.46 

## Visão geral

Usa-se ElGamal/AES+SessionTags para criptografia de ponta a ponta.

Como um sistema não confiável, não ordenado e baseado em mensagens, o
I2P usa uma combinação simples de algoritmos de criptografia assimétrica
e simétrica para fornecer confidencialidade de dados e integridade para
mensagens garlic. Como um todo, a combinação é referida como
ElGamal/AES+SessionTags, mas essa é uma maneira excessivamente prolixa
de descrever o uso de ElGamal de 2048 bits, AES256, SHA256 e nonces de
32 bytes.

Na primeira vez que um roteador deseja criptografar uma mensagem de alho
para outro roteador, ele criptografa o material de chaveamento para uma
chave de sessão AES256 com ElGamal e anexa a carga criptografada
AES256/CBC após o bloco ElGamal criptografado. Além da carga
criptografada, a seção criptografada AES contém o comprimento da carga ,
o hash SHA256 da carga não criptografada, bem como um número de
\"etiquetas de sessão\" - nonces aleatórios de 32 bytes. Na próxima vez
que o remetente quiser criptografar uma mensagem garlic para outro
roteador, em vez de ElGamal criptografar uma nova chave de sessão, eles
simplesmente escolhem uma das tags de sessão entregues anteriormente e
criptografam o payload com AES como antes, usando a chave de sessão
usada com aquela tag de sessão, prefixada com a própria tag de sessão.
Quando um roteador recebe uma mensagem criptografada garlic, eles
verificam os primeiros 32 bytes para ver se ela corresponde a uma tag de
sessão disponível - se corresponder, eles simplesmente descriptografam a
mensagem com AES, mas se não corresponder, eles descriptografam o
primeiro bloco com ElGamal.

Cada tag de sessão pode ser usada apenas uma vez para evitar que
adversários internos correlacionem desnecessariamente mensagens
diferentes como sendo entre os mesmos roteadores . O remetente de uma
mensagem criptografada ElGamal/AES+SessionTag escolhe quando e quantas
tags entregar, pré-estocando o destinatário com tags suficientes para
cobrir uma saraivada de mensagens. Mensagens de alho podem detectar a
entrega bem-sucedida da tag ao agrupar uma pequena mensagem adicional
como um cravo (uma \"mensagem de status de entrega \") - quando a
mensagem de alho chega ao destinatário pretendido e é descriptografada
com sucesso, esta pequena mensagem de status de entrega é um dos cravos
expostos e tem instruções para o destinatário enviar o cravo de volta ao
remetente original (por meio de um túnel de entrada, é claro). Quando o
remetente original recebe esta mensagem de status de entrega, ele sabe
que as tags de sessão agrupadas na mensagem de alho foram entregues com
sucesso.

As próprias tags de sessão têm uma vida útil curta, após a qual são
descartadas se não forem usadas. Além disso, a quantidade armazenada
para cada chave é limitada, assim como o número de chaves em si - se
muitas chegarem, mensagens novas ou antigas podem ser descartadas. O
remetente monitora se as mensagens que usam as tags de sessão estão
sendo transmitidas e, se não houver comunicação suficiente, ele pode
descartar aquelas que antes eram consideradas entregues corretamente,
revertendo para a criptografia ElGamal cara e completa. Uma sessão
continuará existindo até que todas as suas tags sejam esgotadas ou
expirem.

As sessões são unidirecionais. As tags são entregues de Alice para Bob,
e Alice então usa as tags, uma por uma, em mensagens subsequentes para
Bob.

As sessões podem ser estabelecidas entre destinos, entre roteadores ou
entre um roteador e um destino. Cada roteador e destino mantém seu
próprio gerenciador de chaves de sessão para controlar chaves de sessão
e tags de sessão. Gerenciadores de chaves de sessão separados impedem a
correlação de vários destinos entre si ou com um roteador por
adversários.

## Recepção de mensagens

Cada mensagem recebida tem uma das duas as duas condições possíveis:

1. Faz parte de uma sessão existente e contém uma etiqueta de sessão e
 um bloco criptografado AES
2. É para uma nova sessão e contém blocos criptografados ElGamal e AES

Quando um roteador recebe uma mensagem, ele primeiro assume que é de uma
sessão existente e tenta consultar a etiqueta de sessão e
descriptografar os seguintes dados usando AES. Se isso falhar, ele
assume que é para uma nova sessão e tenta descriptografá-la usando
ElGamal.

## Especificação de Nova Mensagem de Sessão {#new}

Uma nova mensagem ElGamal de sessão contém duas partes, um bloco ElGamal
criptografado e um bloco AES criptografado.

A mensagem criptografada contém:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| ElGamal Encrypted Block \| \~ \~ \| \| +
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| \| \|
+\-\-\--+\-\-\--+ + \| \| + + \| AES Encrypted Block \| \~ \~ \| \| +
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| + +\-\-\--+\-\-\--+


### Bloco ElGamal

O bloco ElGamal criptografado tem sempre 514 bytes de comprimento.

Os dados não criptografados do ElGamal têm 222 bytes de comprimento e
contêm:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| Session Key \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| Pre-IV \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ + + \|
\| + + \| 158 bytes random padding \| \~ \~ \| \| + +\-\-\--+\-\-\--+ \|
\| +\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 

The 32-byte [Session
Key](#type_SessionKey) is the
identifier for the session. The 32-byte Pre-IV will be used to generate
the IV for the AES block that follows; the IV is the first 16 bytes of
the SHA-256 Hash of the Pre-IV.

The 222 byte payload is encrypted [using
ElGamal](#elgamal) and the encrypted block
is 514 bytes long.

### Bloco AES {#aes}

Os dados não criptografados no bloco AES contêm o seguinte:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|tag
count\| \| +\-\-\--+\-\-\--+ + \| \| + + \| Session Tags \| \~ \~ \|
\| + + \| \| + +\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| \|
payload size \| \| +\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ +
\| \| + + \| Payload Hash \| + + \| \| + +\-\-\--+\-\-\--+ \| \|flag\|
\| +\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ + \| \| + +
\| New Session Key (opt.) \| + + \| \| + +\-\-\--+ \| \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ + \| \| + + \|
Payload \| \~ \~ \| \| + +\-\-\--//\-\--+\-\-\--+ \| \| \|
+\-\-\--+\-\-\--+\-\-\--//\-\--+\-\-\--+ + \| Padding to 16 bytes \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 

#### Definition

 tag count: 2-byte \`Integer\`, 0-200
Session Tags: That many 32-byte \`SessionTag\`s payload size: 4-byte
\`Integer\` Payload Hash: The 32-byte SHA256 \`Hash\` of the payload
flag: A one-byte value. Normally == 0. If == 0x01, a Session Key follows
New Session Key: A 32-byte \`SessionKey\`, to replace the old key, and
is only present if preceding flag is 0x01 Payload: the data Padding:
Random data to a multiple of 16 bytes for the total length. May contain
more than the minimum required padding. Comprimento
mínimo: 48 bytes

The data is then [AES Encrypted](), using
the session key and IV (calculated from the pre-IV) from the ElGamal
section. The encrypted AES Block length is variable but is always a
multiple of 16 bytes.

#### Notas

- Actual max payload length, and max block length, is less than 64 KB;
 see the [I2NP Overview]().
- A nova chave de sessão não está sendo usada no momento e nunca está
 presente.

## Especificação de mensagem de sessão existente {#existing}

As tags de sessão entregues com sucesso são lembradas por um breve
período de (atualmente 15 minutos) até serem usadas ou descartadas. Uma
tag é usada empacotando uma em uma Mensagem de Sessão Existente que
contém apenas um bloco criptografado AES e não é precedida por um bloco
ElGamal.

A mensagem da sessão existente é como segue:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| Session Tag \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| AES Encrypted Block \| \~ \~ \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 

#### Definition

 Session Tag: A 32-byte \`SessionTag\`
previously delivered in an AES block AES Encrypyted Block: As specified
above. 

A tag de sessão também serve como o pré-IV. O IV são os primeiros 16
bytes do Hash SHA-256 da sessionTag.

Para decodificar uma mensagem de uma sessão existente, um roteador
procura a Tag de Sessão para encontrar uma Chave de Sessão associada .
Se a Tag de Sessão for encontrada, o bloco AES é descriptografado usando
a Chave de Sessão associada. Se a tag não for encontrada, a mensagem é
assumida como uma [Nova Mensagem de Sessão](#new).

## Opções de configuração de tag de sessão {#config}

As of release 0.9.2, the client may configure the default number of
Session Tags to send and the low tag threshold for the current session.
For brief streaming connections or datagrams, these options may be used
to significantly reduce bandwidth. See the [I2CP options
specification](#options) for details. The session
settings may also be overridden on a per-message basis. See the [I2CP
Send Message Expires
specification](#msg_SendMessageExpires) for
details.

## Trabalho futuro {#future}

**Note:** ElGamal/AES+SessionTags is being replaced with
ECIES-X25519-AEAD-Ratchet (Proposal 144). The issues and ideas
referenced below have been incorporated into the design of the new
protocol. The following items will not be addressed in
ElGamal/AES+SessionTags.

Há muitas áreas possíveis para ajustar os algoritmos do Session Key
Manager; alguns podem interagir com o comportamento da biblioteca de
streaming ou ter impacto significativo no desempenho geral.

- O número de tags entregues pode depender do tamanho da mensagem,
 tendo em mente o eventual preenchimento para 1 KB na camada de
 mensagem do túnel.
- Os clientes podem enviar uma estimativa da duração da sessão ao
 roteador, como um aviso sobre o número de tags necessárias.
- A entrega de poucas tags faz com que o roteador recorra a uma
 criptografia ElGamal cara.
- O roteador pode assumir a entrega de tags de sessão ou aguardar o
 reconhecimento antes de usá-las; há compensações para cada
 estratégia.
- Para mensagens muito breves, quase todos os 222 bytes dos campos
 pré-IV e de preenchimento no bloco ElGamal poderiam ser usados para
 a mensagem inteira, em vez de estabelecer uma sessão.
- Avalie a estratégia de preenchimento; atualmente, preenchemos com um
 mínimo de 128 bytes. Seria melhor adicionar algumas tags a mensagens
 pequenas do que preencher.
- Talvez as coisas pudessem ser mais eficientes se o sistema de tags
 de sessão fosse bidirecional, para que as tags entregues no caminho
 \"direto\" pudessem ser usadas no caminho \"reverso\", evitando
 assim o ElGamal na resposta inicial. Atualmente, o roteador faz
 alguns truques como esse ao enviar mensagens de teste de túnel para
 si mesmo.
- Change from Session Tags to [a synchronized
 PRNG](#prng).
- Several of these ideas may require a new I2NP message type, or set a
 flag in the [Delivery
 Instructions](#struct_TunnelMessageDeliveryInstructions),
 or set a magic number in the first few bytes of the Session Key
 field and accept a small risk of the random Session Key matching the
 magic number.


