 NTCP (TCP
basado-en-NIO) 2021-10 0.9.52 

DEPRECATED, NO LONGER SUPPORTED. Disabled by default as of 0.9.40
2019-05. Support removed as of 0.9.50 2021-05. Replaced by
[NTCP2](). NTCP is a Java NIO-based transport
introduced in I2P release 0.6.1.22. Java NIO (new I/O) does not suffer
from the 1 thread per connection issues of the old TCP transport.
NTCP-over-IPv6 is supported as of version 0.9.8.

Por defecto, NTCP usa la IP/puerto autodetectados por SSU. Cuando esté
habilitado en config.jsp, SSU notificará/reiniciará NTCP cuando cambie
una dirección externa o cuando cambie el estado del cortafuegos
(\`firewall\`). Ahora puede habilitar la conexión TCP entrante sin una
IP estática o un servicio DynDNS.

El código de NTCP dentro de I2P es relativamente ligero (1/4 del tamaño
del código de SSU) porque usa el transporte TCP Java subyacente para una
entrega fiable.

## [Especificación de dirección de router]{#ra}

Las siguientes propiedades se almacenan en la base de datos de red.

- **Transport name:** NTCP
- **host:** IP (IPv4 or IPv6). Shortened IPv6 address (with \"::\") is
 allowed. Host names were previously allowed, but are deprecated as
 of release 0.9.32. See proposal 141.
- **port:** 1024 - 65535

## Especificación del protocolo NTCP

### Formato de mensaje estándar

Después del establecimiento, el trasporte NTCP envía mensajes
individuales I2NP (protocolo de red I2P), con un identificador
criptográfico (\`checksum\`). El mensaje no cifrado está codificado de
la siguiente manera:


+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+
\| sizeof(data) \| \| +\-\-\-\-\-\--+\-\-\-\-\-\--+ + \| data \| \~ \~
\| \| + +\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+ \| \| padding
+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+
\| Adler checksum of sz+data+pad \|
+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+


Los datos entonces son cifrados con AES/256/CBC (cadena de cifrado por
bloques con el estándar avanzado de cifrado de 256 bits). La clave de
sesión para el cifrado se negocia durante el establecimiento (usando
Diffie-Hellman de 2048 bits). El establecimiento entre dos routers
(enrutadores) está implementado en la clase EstablishState (estado del
establecimiento) y detallado debajo. El IV (vector de inicialización)
para el cifrado AES/256/CBC son los últimos 16 bytes del anterior
mensaje cifrado.

Son necesarios datos de relleno (desechables criptográficamente) de
entre 0-15 bytes para llevar el tamaño total del mensaje (incluyendo el
\`tamaño seis\` y los bytes del identificador criptográfico
(\`checksum\`)) a un múltiplo de 16. El tamaño máximo de mensaje
actualmente es de 16 KB. Por lo tanto el tamaño de dato máximo
actualmente es de 16 KB - 6, o lo que es lo mismo 16378 bytes. El tamaño
mínimo de dato es de 1 byte.

### Formato de mensaje de sincronización de horaria

Un caso especial es un mensaje de metadatos donde el \`sizeof(data)\`
(tamañode(dato)) sea 0. En ese caso, el mensaje no cifrado esta
codificado como:


+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+
\| 0 \| timestamp in seconds \| uninterpreted
+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+
uninterpreted \| Adler checksum of bytes 0-11 \|
+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+


Longitud total: 16 bytes. El mensaje de sincronización horaria se envía
aproximadamente en intervalos de 15 minutos. El mensaje se cifra tal
como se hace con los mensajes estándar.

### Identificadores criptográficos (\`checksums\`)

The standard and time sync messages use the Adler-32 checksum as defined
in the [ZLIB Specification]().

### Periodo de inactividad

El periodo de inactividad y cierre de conexión se establece a discreción
de cada extremo, y puede variar. La actual implementación reduce el
periodo cuando el número de conexiones se aproxima al máximo
configurado, y eleva el periodo cuando el recuento de conexiones es
bajo. El periodo mínimo recomendado es de dos minutos o más, y el
periodo máximo recomendado es de diez minutos o más.

### Intercambio de RouterInfo

Después del establecimiento, y cada 30-60 minutos en adelante, los dos
routers I2P generalmente deben intercambiar sus RouterInfos usando un
DatabaseStoreMessage. Sin embargo, Alice debe comprobar si el primer
mensaje en la cola es un DatabaseStoreMessage para no enviar un mensaje
duplicado; a menudo este es el caso al conectar a un router I2P de
inundación (floodfill).

### Secuencia de establecimiento

En el estado de establecimiento, hay una secuencia de mensaje de 4-fases
para intercambiar claves DH y firmas. En los dos primeros mensajes hay
un intercambio Diffie Hellman de 2048-bits. Luego, las firmas de los
datos críticos se intercambian para confirmar la conexión.

 Alice contacts Bob
========================================================= X+(H(X) xor
Bob.identHash)\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--Y+E(H(X+Y)+tsB+padding,
sk, Y\[239:255\])
E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk,
hX_xor_Bob.identHash\[16:31\])\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--E(S(X+Y+Alice.identHash+tsA+tsB)+padding,
sk, prev) 


 Leyenda:
 X, Y: Claves públicas DH de 256 bytes
 H(): 32 byte SHA256 Hash
 E(data, session key, IV): AES256 Encrypt
 S(): Signature
 tsA, tsB: Marcas de tiempo (4 bytes, segundos desde epoch (época, origen de tiempo UNIX))
 sk: Clave de sesión de 32 bytes
 sz: Identidad Alice de 2 bytes de tamaño a seguir

#### Intercambio de clave DH {#DH}

The initial 2048-bit DH key exchange uses the same shared prime (p) and
generator (g) as that used for I2P\'s [ElGamal
encryption](#elgamal).

El intercambio de clave DH consiste en un determinado número de pasos,
mostrados debajo. El mapeado entre estos pasos y los mensajes enviados
entre los routers (enrutadores) I2P, está marcado en negrita.

1. Alice genera un entero secreto . Ella entonces calcula
 `X = g^x mod p`.
2. Alice envía X a Bob **(mensaje 1)**.
3. Bob genera un entero secreto y. Él entonces calcula `Y = g^y mod p`.
4. Bob envía Y a Alice **(mensaje 2)**.
5. Alice puede ahora calcular `sessionKey = Y^x mod p`.
6. Bob puede ahora calcular `sessionKey = X^y mod p`.
7. Ambos, Alice y Bob, tienen una clave compartida
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

#### Mensaje 1 (solicitud de sesión)

This is the DH request. Alice already has Bob\'s [Router
Identity](#struct_RouterIdentity), IP
address, and port, as contained in his [Router
Info](#struct_RouterInfo), which was
published to the [network database](). Alice
sends Bob:

 X+(H(X) xor
Bob.identHash)\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
Tamaño: 288 bytes 

Contenidos:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| X,
as calculated from DH \| + + \| \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| HXxorHI \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ X :: X
de 256 bytes desde Diffie Hellman HXxorHI :: SHA256 Hash(X) XOReado con
SHA256 Hash(\`RouterIdentity\` de Bob) (32 bytes) 

**Notas:**

- Bob verifica HXxorHI usando su propio hash de router. Si no se
 verifica, Alice ha contactado el router equivocado, y Bob corta la
 conexión.

#### Mensaje 2 (sesión creada)

Esta es la respuesta DH. Bob envía a Alice:


\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--Y+E(H(X+Y)+tsB+padding,
sk, Y\[239:255\]) Tamaño: 304 bytes 

Contenidos no cifrados:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| Y
as calculated from DH \| + + \| \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| HXY \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| tsB
\| padding \| +\-\-\--+\-\-\--+\-\-\--+\-\-\--+ + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ Y :: Y
de 256 bytes desde Diffie Hellman HXY :: SHA256 Hash(X concatenado con
Y). (32 bytes) tsB :: Marca de tiempo de 4 bytes (segundos desde epoch
(época, origen de tiempo UNIX)) padding :: 12 bytes datos aleatorios 

Contenidos cifrados:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| Y
as calculated from DH \| + + \| \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| encrypted data \| + + \| \| + + \| \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 


 Y: Y de 256 bytes desde Diffie Hellman

 encrypted data: 48 bytes AES encrypted using the DH session key and
 the last 16 bytes of Y as the IV

**Notas:**

- Alice may drop the connection if the clock skew with
 Bob is too high as calculated using tsB.

#### Mensaje 3 (Confirmar Sesión A)

Esto contiene la identificación del router I2P de Alice, y una firma de
los datos críticos. Alice le envía a Bob:


E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk,
hX_xor_Bob.identHash\[16:31\])\-\--\> Tamaño: 448 bytes (typ. for 387
byte identity and DSA signature), see notes below 

Contenidos no cifrados:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| sz
\| Alice\'s Router Identity \| +\-\-\--+\-\-\--+ + \| \| \~ . . . \~ \|
\| + +\-\-\--+\-\-\--+\-\-\--+ \| \| tsA
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
padding \| +\-\-\--+ + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| signature \| + + \| \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ sz ::
2 bytes de tamaño de la identificación del router I2P de Alice a seguir
(387+) ident :: \'RouterIdentity\' (identificación de router I2P) de
387+ bytes de Alice tsA :: Marca de tiempo de 4 bytes (segundos desde
epoch (época, origen de tiempo UNIX)) padding :: 0-15 bytes de datos
aleatorios signature :: la \`Signature\` (firma) de los siguientes datos
concatenados: X, Y, \`RouterIdentity\` (identificación de router I2P) de
Bob, tsA, tsB (marcas de tiempo A y B). Alice los firma con la
\`SigningPrivateKey\` (clave privada de firmante) asociada con la
\`SigningPublicKey\` (clave pública firmante) en su \`RouterIdentity\`


Contenidos cifrados:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| encrypted data \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 


 encrypted data: 448 bytes AES encrypted using the DH session key and
 the last 16 bytes of HXxorHI (i.e., the last 16 bytes of message #1) as the IV
 448 is the typical length, but it could be longer, see below.

**Notas:**

- Bob verifica la firma, y si falla, rechaza la conexión.
- Bob puede rechazar la conexión si si el desfase horario con el reloj
 de Alice es demasiado alto al calcularse usando tsA.
- Alice usará los últimos 16 bytes de los contenidos cifrados de este
 mensaje como IV (vector de inicialización) para el siguiente
 mensaje.
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

#### Mensaje 4 (Confirmar Sesión B)

Esta es una firma de los datos críticos. Bob le envía a Alice:

 \*
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--E(S(X+Y+Alice.identHash+tsA+tsB)+padding,
sk, prev) Tamaño: 48 bytes (typ. for DSA signature), see notes below 

Contenidos no cifrados:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| signature \| + + \| \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
padding \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+
signature :: la \`Signature\` (firma) de los siguientes datos
concatenados: X, Y, \`RouterIdentity\` (identificación de router I2P) de
Alice, tsA, tsB (marcas de tiempo A y B). Bob lo firma con la
\`SigningPrivateKey\` (clave privada firmante) asociada con la
\`SigningPublicKey\` (clave pública firmante) en su \`RouterIdentity\`
padding :: 0-15 bytes de datos aleatorios 

Contenidos cifrados:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| encrypted data \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 


 encrypted data: Data AES encrypted using the DH session key and
 the last 16 bytes of the encrypted contents of message #2 as the IV
 48 bytes for a DSA signature, may vary for other signature types

**Notes:**

- Alice verifica la firma, y en caso de fallo, rechaza la conexión.
- Bob usará los últimos 16 bytes de los contenidos cifrados de este
 mensaje como IV (vector de inicialización) para el siguiente
 mensaje.
- Through release 0.9.15, the signature was always a 40 byte DSA
 signature and the padding was always 8 bytes. As of release 0.9.16,
 the signature type and length are implied by the type of the
 [Signing Public
 Key](#type_SigningPublicKey)
 in Bob\'s [Router
 Identity](#struct_RouterIdentity).
 The padding is as necessary to a multiple of 16 bytes for the entire
 unencrypted contents.

#### Después del establecimiento

La conexión está establecida, y pueden intercambiarse mensajes normales
o mensajes de sincronización de tiempo. Todos los mensajes siguientes
están cifrados con AES usado la clave de sesión DH antes acordada. Alice
usará los últimos 16 bytes del contenido cifrado del mensaje #3 como el
siguiente IV. Bob usará los últimos 16 bytes del contenido cifrado del
mensaje #4 como el siguiente IV.

### Mensaje de conexión del reloj

Alternativamente, cuando Bob recibe una conexión, puede ser una conexión
de prueba (quizás mostrada por Bob al preguntar a alguien para verificar
a su interlocutor). Las conexiones de prueba no se usan actualmente.
Aunque, para que quede en el registro, las conexiones de prueba son
formateadas como sigue. Una conexión de prueba de información recibirá
256 bytes que contienen:

- 32 bytes sin interpretar, datos ignorados
- tamaño de 1 byte
- el número de bytes que componen la dirección IP del ruter local
 (como haya sido contactado por la parte remota)
- el número de puerto de 2 bytes, en donde ha sido contactado el ruter
 local
- la hora de la red i2p de 4 bytes según la parte remota (segundos
 desde la \'época\')
- datos de relleno sin interpretar, hasta 223 bytes
- xor del hash de la identidad del ruter local y el SHA256 de los
 bytes desde el 32 hasta el 223

La comprobación de la conexión está completamente deshabilitada desde la
versión 0.9.12.

## Debate

Now on the [NTCP Discussion Page]().

## [Trabajo futuro]{#future}

- El tamaño máximo del mensaje debería aumentarse hasta
 aproximadamente 32 KB
- Un conjunto de tamaños de paquetes fijos podría ser apropiado para
 ocultar aún más la fragmentación de los datos a adversarios
 externos, pero el túnel garlic y el relleno de fin a fin deberían
 ser suficientes para la mayoría de las necesidades hasta entonces.
 Sin embargo, actualmente no se realiza el relleno más allá del
 límite de 16 bytes, para crear un número limitado de tamaños de
 mensajes.
- La utilización de la memoria (incluyendo la del kerne) para NTCP
 debería compararse con la del SSU.
- ¿Pueden ser rellenado aleatoriamente de alguna forma el mensaje
 establecido, para evitar la identificación del tráfico I2P basado en
 el tamaño del paquete inicial?


