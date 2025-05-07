 Cifrado
ElGamal/AES + SessionTag April
2020 0.9.46 

## Información general

ElGamal/AES+SessionTags es usado para los cifrados de fin a fin.

Como el sistema basado en mensajes no ordenados y no fiable que es, I2P
usa una combinación simple de algoritmos de cifrados simétricos y
asimétricos para proporcionar la confidencialidad de los datos y la
integridad de los mensajes garlic. En conjunto, la combinación es
llamada ElGamal/AES+SessionTags, pero es una forma excesivamente larga
de describir el uso de ElGamal de 2048 bits, AES256, SHA256 y nonces
(números de un sólo uso) de 32 bytes.

La primera vez que un ruter quiere cifrar un mensaje para otro ruter,
estos cifran las claves para una clave de sesión AES256 con ElGamal y
adjunta la payload ya cifrado AES256/CBC después del bloque cifrado
ElGamal. Además del payload cifrado, las sección del cifrado AES
contiene el tamaño de la carga, el hash SHA256 del payload no cifrado,
así como el número de \"etiquetas de sesión\" - nonces aleatorios de 32
bits. La siguiente vez que el remitente desea cifrar un mensaje garlic
para otro ruter, en vez de de cifrar una nueva clave de sesión con
ElGamal, simplemente elijen una de las etiquetas enviadas de la sesión
anterior y cifran con AES el payload como anteriormente, usando la clave
de sesión usada con la etiqueta de la sesión, antepuesto con la misma
etiqueta de sesión. Cuando un ruter recibe un mensaje cifrado garlic,
comprueba los primeros 32 bytes para ver si coinciden con una etiqueta
de sesión disponible - si lo hace, simplemente descifran el mensaje con
AES, pero si no, descifran el primer bloque con ElGamal

Cada etiqueta de sesión puede usarse sólo una vez para evitar que
adversarios internos puedan relacionar diferentes mensajes al enviarse
estos entre los mismos ruters. El remitente de un mensaje cifrado con
etiqueta de sesión + ElGamal/AES elije cuando y cuantas etiquetas a
enviar, poniendo a disposición del que recibe suficientes etiquetas para
trabajar con un buen número de mensajes. Los mensajes Garlic pueden
detectar la llegada exitosas de las etiquetas construyendo un mensaje
adicional tipo clove (un \"mensaje de estado de entrega\") - cuando el
mensaje llega al destinatario elegido y es descifrado correctamente,
este pequeño mensaje de estado de entrega es uno de los dientes
expuestos y tiene instrucciones para el destinatario para que retorne al
remitente original (a través de un túnel de entrada, claro). Cuando el
remitente original recibe el mensaje de estado de envío, sabe que la
etiqueta de sesión incluida en el mensaje garlic ha sido enviada
exitosamente.

Las etiquetas de sesión tienen un vida muy corta, después de la cual son
descartadas y no se usan más. Además, el número almacenado de ellas por
cada clave es limitado, como también está limitado el número de claves -
si llegan demasiadas, serán descartados los mensajes nuevos o los
viejos. El remitente lleva el seguimiento de los mensajes con etiquetas
de sesión que pasan a través suyo, y si no hay comunicación suficiente
podría descartar los mensajes supuestamente enviados correctamente,
volviendo al costoso cifrado ElGamal. Una sesión continuará existiendo
hasta que todas las etiquetas hayan expirado.

Las sesiones son unidireccionales. Las etiquetas son enviadas desde
Alice a Bob, y Alice entonces utiliza las etiquetas, una a una, en los
siguientes mensajes hacia Bob.

Las sesiones puede establecerse entre Destinaciones, entre Ruters o
entre Ruters y Destinaciones. Cada ruter y destinación mantiene su
administrador de claves de sesión para hacer el seguimiento de las
claves de sesión y las etiquetas de sesión. Al haber administradores de
claves de sesión separados se previene que los adversarios puedan hacer
correlación de las múltiples destinaciones que hay entre cada uno o
entre ruters.

## Recepción del Mensaje

Cada mensaje recibido tiene una de estas dos posibles condiciones:

1. Es parte de una sesión ya existente y contiene una etiqueta de
 sesión y un bloque cifrado AES.
2. Es para una nueva sesión y contiene los bloques cifrados ElGamal y
 AES.

Cuando un ruter recibe un mensaje, primero asumirá que es de una sesión
ya existente e intentará buscar la etiqueta de sesión y descifrar los
datos usando AES. Si esto falla, asumirá que es para una nueva sesión e
intentará descifrarlo usando ElGamal.

## Especificaciones de los mensajes de nueva sesión. {#new}

Un mensaje de nueva sesión ElGamal contiene dos partes, un bloque
cifrado ElGamal y un bloque cifrado AES.

El mensaje cifrado contiene:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| ElGamal Encrypted Block \| \~ \~ \| \| +
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| \| \|
+\-\-\--+\-\-\--+ + \| \| + + \| AES Encrypted Block \| \~ \~ \| \| +
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| + +\-\-\--+\-\-\--+


### Bloque ElGamal

El bloque cifrado ElGamal es siempre de 514 bytes.

Los datos no cifrados ElGamal son de 222 bytes de largo, y contienen:


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

### Bloque AES {#aes}

Los datos sin cifrar en el bloque AES contienen los siguiente:


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
more than the minimum required padding. Tamaño mínimo
: 48 bytes

The data is then [AES Encrypted](), using
the session key and IV (calculated from the pre-IV) from the ElGamal
section. The encrypted AES Block length is variable but is always a
multiple of 16 bytes.

#### Notas

- Actual max payload length, and max block length, is less than 64 KB;
 see the [I2NP Overview]().
- La nueva clave de sesión actualmente está en desuso y nunca está
 presente.

## Especificación de mensaje de sesión existente. {#existing}

Las etiquetas de sesión entregadas exitosamente son recordadas durante
un periodo breve (actualmente 15 minutos) hasta que se usan o se
descartan. Se usa una etiqueta empaquetándola en un mensaje de sesión
existente que sólo contiene un bloque cifrado con AES, y no está
precedido por un bloque ElGamal.

El mensaje de sesión existente es como sigue:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| Session Tag \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| AES Encrypted Block \| \~ \~ \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 

#### Definition

 Session Tag: A 32-byte \`SessionTag\`
previously delivered in an AES block AES Encrypyted Block: As specified
above. 

La etiqueta de sesión también sirve como pre-IV. El IV (Vector de
Inicialización) son los primeros 16 bytes del hash SHA-256 de la
sessionTag (etiqueta de sesión).

Para decodificar un mensaje desde una sesión existente, un router
consulta la etiqueta de sesión para encontrar una clave de sesión
asociada. Si se encuentra la etiqueta de sesión, el bloque AES es
descifrado usando la clave de sesión asociada. Si no se encuentra la
etiqueta, se asume que el mensaje es un [nuevo mensaje de sesión](#new).

## Opciones de configuración de identificador de sesión {#config}

As of release 0.9.2, the client may configure the default number of
Session Tags to send and the low tag threshold for the current session.
For brief streaming connections or datagrams, these options may be used
to significantly reduce bandwidth. See the [I2CP options
specification](#options) for details. The session
settings may also be overridden on a per-message basis. See the [I2CP
Send Message Expires
specification](#msg_SendMessageExpires) for
details.

## Trabajo futuro {#future}

**Note:** ElGamal/AES+SessionTags is being replaced with
ECIES-X25519-AEAD-Ratchet (Proposal 144). The issues and ideas
referenced below have been incorporated into the design of the new
protocol. The following items will not be addressed in
ElGamal/AES+SessionTags.

Hay muchas áreas posibles para ajustar los algoritmos del administrador
de claves de sesión; algunos pueden interactuar con el comportamiento de
la librería streaming, o tener un impacto significativo en el
rendimiento conjunto.

- El número de etiquetas entregadas podría depender del tamaño del
 mensaje, teniendo en cuenta el eventual esquema de relleno de 1KB en
 la capa de mensaje de túnel.
- Los clientes podrían enviar una estimación del tiempo de vida de la
 sesión al router, a modo de aviso del número de etiquetas
 solicitado.
- La entrega de demasiado pocas etiquetas provoca que el ruter regrese
 al costoso cifrado de respaldo ElGamal.
- El router puede asumir como un hecho la entrega de etiquetas de
 sesión, o esperar acuse de recibo (\'acknowledgement\') antes de
 usarlas; cada estrategia tiene sus propios sacrificios.
- Para mensajes muy breves, casi la totalidad de los 222 bytes del
 pre-IV (pre-Vector de Inicialización) y los campos de esquemas de
 relleno en el bloque ElGamal podrían usarse para el mensaje
 completo, en lugar de para establecer una sesión.
- Evaluar la estrategia de esquema de relleno; actualmente rellenamos
 hasta un mínimo de 128 bytes. Para los mensajes pequeños sería mejor
 añadirles unas pocas etiquetas que rellenarlos.
- Quizá las cosas podrían ser más eficientes si el sistema de etiqueta
 de sesión fuera bidireccional, así las etiquetas entregadas en la
 ruta \'forward\' (directa) podrían usarse en la ruta \'reverse\'
 (inversa), evitando así ElGamal en la respuesta inicial. El router
 actualmente usa algunos trucos como este cuando se envían mensajes
 de prueba de túnel a si mismo.
- Change from Session Tags to [a synchronized
 PRNG](#prng).
- Several of these ideas may require a new I2NP message type, or set a
 flag in the [Delivery
 Instructions](#struct_TunnelMessageDeliveryInstructions),
 or set a magic number in the first few bytes of the Session Key
 field and accept a small risk of the random Session Key matching the
 magic number.


