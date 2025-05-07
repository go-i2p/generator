 Implementación de
túnel July 2019 0.9.41 Esta página
documenta la implementación actual del túnel.

## Introducción a los túneles {#tunnel.overview}

Dentro de I2P, los mensajes se pasan en una dirección a través de un
túnel virtual de pares (\`peers\`), usando cualquier medio que esté
disponible para pasar el mensaje al siguiente salto. Los mensajes llegan
a la pasarela (\`gateway\`) del túnel, son empaquetados y/o fragmentados
en mensajes de túnel de tamaño-fijo, y son reenviados hacia el siguiente
salto en el túnel, que procesa y verifica la validez del mensaje y lo
envía al siguiente salto, y así sucesivamente, hasta que alcanza el
extremo del túnel. Ese *extremo* toma los mensajes empaquetados por la
pasarela y los reenvía como se se le ha indicado - bien hacia otro
router, bien hacia otro túnel en otro router, o bien localmente.

Los túneles funcionan todos de la misma forma, pero pueden estar
segmentados en dos diferentes grupos - túneles de entrada o túneles de
salida. Los túneles de entrada tienen una pasarela (\`gateway\`) no
confiable que pasa mensajes hacia el creador del túnel, que sirve como
extremo del túnel. Para túneles de salida, el creador del túnel hace de
pasarela pasando mensajes al exterior hacia el extremo remoto.

El creador del túnel selecciona exactamente qué pares (\`peers\`)
participarán en el túnel, y proporciona a cada uno los datos de
configuración necesarios. Pueden tener cualquier número de saltos. La
intención es hacer difícil, tanto a los partícipantes en el túnel como a
terceros, determinar la longitud de un túnel, o incluso que unos
participantes compinchados determinen si ellos forman parte de un mismo
túnel (impidiendo la situación en la que pares compinchados estén
próximos unos de otros en el túnel).

En la práctica, una serie de depósitos (\`pools\`) de túneles se usan
para diferentes propósitos - cada destino de cliente local tiene su
propio conjunto de túneles de entrada configurados para alcanzar sus
necesidades de anonimato y rendimiento. Además, el propio router
mantiene una serie de depósitos para participar en la base de datos de
red y para administrar los propios túneles.

I2P es inherentemente una red de paquetes conmutados, incluso con estos
túneles, lo que le permite aprovechar la ventaja de múltiples túneles
ejecutándose en paralelo, incrementando la flexibilidad y el equilibrado
de la carga. Fuera del núcleo de la capa I2P, hay una librería streaming
(de flujo) extremo a extremo opcional disponible para aplicaciones
cliente, que ofrece operaciones estilo-TCP, incluyendo reordenamiento de
mensajes, retransmisión, control de congestión, etc.

An overview of I2P tunnel terminology is [on the tunnel overview
page]().

## Operaciones de los túneles (procesamiento de mensajes) {#tunnel.operation}

### Vista general

After a tunnel is built, [I2NP messages]() are
processed and passed through it. Tunnel operation has four distinct
processes, taken on by various peers in the tunnel.

1. Primero, la pasarela (\`gateway\`) del túnel acumula un número de
 mensajes I2NP y los preprocesa en mensajes de túnel para su entrega.
2. Después, esa pasarela cifra los datos preprocesados, luego los
 reenvía al primer salto.
3. Ese par (\`peer\`), y los subsiguientes participantes en el túnel,
 desenvuelven una capa del cifrado, verificando que no esté
 duplicada, y luego la reenvían hacia el siguiente par.
4. Eventualmente, los mensajes de túnel llegan al extremo donde los
 mensajes I2NP fueron originalmente empaquetados por la pasarela,
 entonces son reensamblados y reenviados de la forma requerida.

Los participantes intermedios del túnel no saben si ellos están en un
túnel de entrada o de salida; ellos siempre \"cifran\" para el siguiente
salto. Por lo tanto, aprovechamos la ventaja del cifrado AES simétrico
para \"descifrar\" en la pasarela (\`gateway\`) del túnel de salida, así
que el texto plano se revela en el extremo de salida.

![Inbound and outbound tunnel
schematic](images/tunnels.png "Inbound and outbound tunnel schematic")

+-----------------+-----------------+-----------------+-----------------+
| Rol | Preprocesado | Operación de | Posprocesado |
| | | cifrado | |
+=================+=================+=================+=================+
| Pasarela | Fragmento, | Cifrar | Reenvíar al |
| (\`gateway\`) | lote, y fardo | iterativamente | siguiente salto |
| saliente | | (usando | |
| (Creador) | | operaciones de | |
| | | descifrado) | |
+-----------------+-----------------+-----------------+-----------------+
| Participante |   | Descifrar | Reenvíar al |
| | | (usando una | siguiente salto |
| | | operación de | |
| | | cifrado) | |
+-----------------+-----------------+-----------------+-----------------+
| Punto final de |   | Descifrar | Reensamblar |
| salida | | (usando una | fragmentos, |
| | | operación de | reenviar hacia |
| | | cifrado) para | la pasarela |
| | | revelar el | (\`gateway\`) o |
| | | mensaje de | router entrante |
| | | túnel de texto | tal como se |
| | | plano | indicó |
+-----------------+-----------------+-----------------+-----------------+
| ------------- | | | |
+-----------------+-----------------+-----------------+-----------------+
| Puerta de | Fragmento, | Cifrar | Reenvíar al |
| salida de | lote, y fardo | | siguiente salto |
| entrada | | | |
+-----------------+-----------------+-----------------+-----------------+
| Participante |   | Cifrar | Reenvíar al |
| | | | siguiente salto |
+-----------------+-----------------+-----------------+-----------------+
| Extremo de |   | Descifrar | Reensamblar |
| entrada | | iterativamente | fragmentos, |
| (Creador) | | para revelar | recibir datos |
| | | mensajes de | |
| | | túnel de texto | |
| | | plano | |
+-----------------+-----------------+-----------------+-----------------+

### Procesado de la pasarela (\`gateway\`) {#tunnel.gateway}

#### Preprocesado de mensaje {#tunnel.preprocessing}

A tunnel gateway\'s function is to fragment and pack [I2NP
messages]() into fixed-size [tunnel
messages]() and encrypt the tunnel
messages. Tunnel messages contain the following:

- Un identificador (\`ID\`) de túnel de 4 bytes
- Un IV (vector de inicialización) de 16 bytes
- Un identificador criptográfico (\`checksum\`)
- Relleno (datos inútiles desechables criptográficamente), si fuera
 necesario
- Uno o más pares { instrucción de entrega, fragmento de mensaje I2NP
 }

Los identificadores (\`IDs\`) de túnel tienen números de 4 bytes usados
en cada salto - los participantes saben con qué identificadores (\`ID\`)
de túnel escuchar mensajes y sobre qué túneles deben ser reenviados
hacia el siguiente salto, y cada salto elije el identificador (\`ID\`)
de túnel sobre el cual recibe los mensajes. Los propios túneles son de
vida-corta (10 minutos). Incluso si los subsiguientes túneles se erigen
usando la misma secuencia de pares (\`peers\`), el identificador
(\`ID\`) de túnel de cada salto cambiará.

Para evitar que los adversarios marquen los mensajes a través de la ruta
ajustando el tamaño del mensaje, todos los mensajes de túnel tienen un
tamaño fijo de 1024 bytes. Para acomodar mensajes I2NP (protocolo de red
I2P) más grandes así como para dar soporte a los más pequeños de forma
más eficiente, la pasarela (\`gateway\`) divide los mensajes I2NP más
grandes en fragmentos contenibles en cada mensaje de túnel. El extremo
del túnel intentará reconstruir el mensaje I2NP partiendo de los
fragmentos durante un corto periodo de tiempo, pero los descartará
cuando sea necesario.

Details are in the [tunnel message
specification]().

### Cifrado de la pasarela (\`gateway\`)

Después del preprocesado de mensajes hacia una carga con datos de
relleno, la pasarela (\`gateway\`) construye un valor de IV (vector de
inicialización) aleatorio de 16 bytes, cifrando a este y al mensaje de
túnel iterativamente tanto como se necesite, y reenvía la tupla {
tunnelID, IV, mensaje de túnel cifrado } al siguiente salto.

Cómo se hace el cifrado en la pasarela (\`gateway\`) depende de si el
túnel es de entrada o de salida. Para los túneles entrantes, simplemente
eligen un IV (vector de inicialización) aleatorio, posprocesándolo y
actualizándolo para generar el IV para la pasarela y usar ese IV junto
con su propia clave de capa para cifrar los datos preprocesados. Para
túneles salientes deben descifrar iterativamente el (no cifrado) IV y
los datos preprocesados, con el IV y las claves de capa para todos los
saltos en el túnel. El resultado del cifrado del túnel de salida es que
cuando cada par (\`peer\`) lo cifra, el extremo recuperará los datos
preprocesados iniciales.

### Procesado de los participantes {#tunnel.participant}

Cuando un par (\`peer\`) recibe un mensaje de túnel, comprueba que el
mensaje venga desde el mismo salto previo que antes (inicializado cuando
el primer mensaje atraviesa el túnel). Si el par previo está en un
router diferente, o si el mensaje ha sido visto ya, el mensaje es
descartado. Entonces el participante cifra el IV (vector de
inicialización) recibido con AES256/ECB usando su clave IV para
determinar el IV actual, usa ese IV con la clave de capa del
participante para cifrar los datos, cifra el actual IV con AES256/ECB
usando la clave IV otra vez, y luego reenvía la tupla {nextTunnelId,
nextIV, encryptedData} (siguiente identificador de túnel, siguiente IV,
datos cifrados) al siguiente salto. Este doble cifrado del IV (tanto
antes como después de su uso) ayuda a afrontar una cierta clase de
ataques de confirmación. See [this
email](http://zzz.i2p/archive/2005-07/msg00031.html) and the surrounding
thread for more information.

La detección de mensajes duplicados es gestionada por un filtro Bloom
decadente (en el tiempo) sobre los IVs (vectores de inicialización) de
los mensajes. Cada router mantiene un único filtro Bloom para guardar el
XOR del IV con el primer bloque del mensaje recibido para todos los
túneles en los que está participando, modificado (decadencia) para
descartar entradas vistas después de 10-20 minutos (cuando los túneles
habrán expirado). El tamaño del filtro Bloom y los parámetros usados son
suficientes para más que saturar la conexión de red del router con una
insignificante posibilidad de falso positivo. El único valor añadido en
el filtro Bloom es el XOR del IV y el primer bloque como forma de
prevenir que pares (\`peers\`) compinchados no secuenciales en el túnel,
marquen un mensaje reenviándolo con el IV y el primer bloque cambiados.

### Procesado en el extremo {#tunnel.endpoint}

Después de recibir y validar un mensaje de túnel en el último salto del
túnel, la forma en la que el extremo recupera los datos codificados por
la pasarela (\`gateway\`) depende de si el túnel es de entrada o de
salida. Para túneles salientes, el extremo cifra el mensaje con su clave
de capa tal como lo hace cualquier otro participante (en el túnel),
exponiendo los datos preprocesados. Para túneles entrantes, el extremo
también es el creador del túnel, así que pueden meramente descifrar
iterativamente el IV (vector de inicialización) y el mensaje usando las
claves de capa e IV de cada paso en orden inverso.

En este punto, el extremo del túnel tiene los datos preprocesados
enviados por la pasarela (\`gateway\`), que pueden entonces ser
separados en los mensajes I2NP incluidos, y reenviarlos tal como se
requería en sus instrucciones de entrega.

## Construcción del túnel {#tunnel.building}

Cuando se construye un túnel, el creador debe enviar una solicitud con
los datos de configuración necesarios a cada uno de los saltos, y
esperar que todos ellos accedan antes de habilitar el túnel. Las
solicitudes se cifran de forma que sólo los pares (\`peers\`) que
necesiten conocer un pedazo de la información (tales como las claves de
capa del túnel o de IV (vector de inicialización)) tienen esos datos.
Además, sólo el creador del túnel tendrá acceso a la respuesta del par.
Hay tres dimensiones importantes a tener en cuenta al generar los
túneles: qué pares se usan (y dónde), cómo se envían las solicitudes (y
las respuestas recibidas), y cómo son mantenidas.

### Selección de pares {#tunnel.peerselection}

Más allá de los dos tipos de túneles - entrante y saliente - hay dos
estilos de selección del par (\`peer\`) usados por diferentes túneles -
exploratorio y cliente. Los túneles exploratorios se usan tanto para el
mantenimiento de la base de datos de red como para el mantenimiento del
túnel, mientras los túneles de cliente se usan para mensajes de cliente
extremo-a-extremo.

#### Selección de par de túnel exploratorio {#tunnel.selection.exploratory}

Los túneles exploratorios son construidos de una selección de pares
aleatorios de un subconjunto de la red. Los subconjuntos varían en cada
ruter local y según sean las necesidades de ese túnel. En general, los
túneles exploratorios se construyen a partir de pares seleccionados
aleatoriamente que están en categoría del perfil de par \'no se cae,
está activo\' . El segundo fin de los túneles, además de simplemente
enrutar, es encontrar pares de alta capacidad libres para poder usarlos
para los túneles clientes.

Exploratory peer selection is discussed further on the [Peer Profiling
and Selection page]().

#### Selección del par para el túnel cliente {#tunnel.selection.client}

Los túneles cliente son construidos con unos requerimientos más
rigurosos - el ruter local selecciona los pares de la categoría de
perfil \"rápidos y de gran capacidad\" para que el rendimiento y la
fiabilidad se ajusten a las necesidades de la aplicación cliente. Aunque
hay varios detalles importantes más allá de la selección básica que
deben ser tomados en cuenta, dependiendo de las necesidades de anonimato
que necesite el cliente.

Client peer selection is discussed further on the [Peer Profiling and
Selection page]().

#### Orden de los pares dentro del túnel {#ordering}

Peers are ordered within tunnels to deal with the [predecessor
attack]() [(2008
update)]().

Para evitar el ataque del predecesor, la selección del túnel mantiene a
los pares seleccionados en estricto orden - si A, B, y C están en un
túnel determinado para un grupo de túneles en particular, el salto
después de A es siempre B, y el salto después de B siempre es C.

El orden está implementado generando una clave aleatoria de 32 bytes
para cada grupo de túneles al inicio. Los pares no deberían ser capaces
de adivinar el orden, un atacante podría elaborar aparte dos hashes de
ruter para maximizar las posibilidades de ser las dos puntas del túnel.
Los pares están ordenados por la distancia XOR del hash SHA256 de (el
hash del par concatenado con la clave aleatoria) de la clave aleatoria .

 p = peer hash
 k = random key
 d = XOR(H(p+k), k)

Ya que cada grupo de túneles utiliza una clave aleatoria diferente, el
orden es consistente dentro de un mismo grupo pero no entre grupos. Las
claves son generadas al reinicio de cada ruter.

### Solicitud de entrega {#tunnel.request}

A multi-hop tunnel is built using a single build message which is
repeatedly decrypted and forwarded. In the terminology of [Hashing it
out in Public](), this is \"non-interactive\"
telescopic tunnel building.

This tunnel request preparation, delivery, and response method is
[designed]() to reduce the number of
predecessors exposed, cuts the number of messages transmitted, verifies
proper connectivity, and avoids the message counting attack of
traditional telescopic tunnel creation. (This method, which sends
messages to extend a tunnel through the already-established part of the
tunnel, is termed \"interactive\" telescopic tunnel building in the
\"Hashing it out\" paper.)

The details of tunnel request and response messages, and their
encryption, [are specified here]().

Los pares pueden denegar las peticiones de creación de túnel por varias
razones, a través de una serie de cuatro rechazos cada vez más graves:
rechazo propabilístico (debido a que le ruter se acerca al límite de su
capacidad, o en respuesta de una riada de peticiones), sobrecarga
transitoria, sobrecarga del ancho de banda, y fallo crítico. Cundo son
recibidos, estos cuatro son interpretados por el creador del túnel para
ayudar a ajustar su perfil a la petición del ruter.

For more information on peer profiling, see the [Peer Profiling and
Selection page]().

### Grupos de túneles {#tunnel.pooling}

To allow efficient operation, the router maintains a series of tunnel
pools, each managing a group of tunnels used for a specific purpose with
their own configuration. When a tunnel is needed for that purpose, the
router selects one out of the appropriate pool at random. Overall, there
are two exploratory tunnel pools - one inbound and one outbound - each
using the router\'s default configuration. In addition, there is a pair
of pools for each local destination - one inbound and one outbound
tunnel pool. Those pools use the configuration specified when the local
destination connects to the router via [I2CP](),
or the router\'s defaults if not specified.

Each pool has within its configuration a few key settings, defining how
many tunnels to keep active, how many backup tunnels to maintain in case
of failure, how long the tunnels should be, whether those lengths should
be randomized, as well as any of the other settings allowed when
configuring individual tunnels. Configuration options are specified on
the [I2CP page]().

### Longitud de los túneles y valores por defecto {#length}

[En la página de introducción al
túnel](#length).

### Estrategia de construcción anticipatoria y prioridad {#strategy}

La construcción de un túnel es cara, y los túneles expiran después de un
tiempo fijo de haber sido creados. Sin embargo, el éxito de construcción
de túnel puede variar enormemente según las condiciones de la red local
y global. Por esto, es importante mantener una estrategia de
construcción anticipatoria y adaptativa para asegurarse de que los
túneles nuevos, antes de ser usados, son construidos exitosamente, no se
construyen en exceso, no se construyen demasiado pronto, o consumen
demasiada CPU o ancho de banda al crear y enviar los mensajes de
construcción cifrados.

Por cada tupla {esploratorio/cliente, entrada/salida, longitud,
diferencia de longitud} el ruter mantiene estadísticas del tiempo
necesario para la construcción con éxito de un túnel. Usando estas
estadísticas, calcula cuando debe comenzar a intentar crear un reemplazo
antes de la expiración del túnel. Cuando el tiempo de expiración se
acerca sin un reemplazo exitoso, comienza a hacer múltiples intentos de
construcción en paralelo, y entonces aumentará el número de intentos en
paralelo si es necesario.

Para limitar el uso de CPU y ancho de banda, el ruter también limita el
número máximo de intentos de construcción pendientes a través de todos
los grupos. Las construcciones críticas (aquellas para los túneles
exploratorios, y para los grupos que se han quedado sin túneles) son
priorizadas.

## Límites de los mensajes de túnel {#tunnel.throttling}

Aunque los túneles dentro de I2P son parecidos a una red conmutada de
circuito, todo dentro de I2P está basado en mensajes - los túneles no
son más que trucos contables para ayudar a organizar el envío de
mensajes. No se toman suposiciones con respecto a el orden o fiabilidad
de los mensajes, y la retransmisiones son dejadas para los niveles
superiores (por ejemplo para la capa cliente de la librería de streaming
de I2P) . Esto permite a I2P aprovechar las técnicas de limitaciones
disponibles en las redes conmutadas de paquetes y en las redes
conmutadas de circuito. Por ejemplo, cada ruter puede hacer un
seguimiento de la media cambiante de cuantos datos usa cada túnel,
combinar eso con todas medias usadas poro otros túneles en los que
participa el ruter, y ser capaz de aceptar o denegar las peticiones de
participación adicional de túnel basándose en su capacidad y
utilización. Por otro lado, cada ruter puede simplemente denegar los
mensajes que están más allá de su capacidad.

En la implementación actual, los ruters implementan una estrategia de
rechazo temprano ponderada aleatoria, weighted random early discard
(WRED) strategy. Para todos los túneles participantes (participante
interno, puerta de salida de entrada y punto final de salida), el ruter
empezará a denegar una parte de los mensajes según llegue a los límites
del ancho de banda. Cuando el tráfico llega cerca, o excede los límites,
se rechazan más mensajes. Para un participante interno, todos los
mensajes están fragmentados y rellenados y por lo tanto son del mismo
tamaño. En la puerta de salida de entrara y en el punto final de salida,
sin embargo, la decisión de rechazo se hace en el mensaje completo
(junto), y el tamaño del mensaje es tomado en cuenta. Es más fácil que
sean eliminados los mensajes más largos. Además, es más fácil que los
mensajes sean rechazados en el punto final de salida que en la puerta de
salida de entrada, ya que esos mensajes no están tan \"a lo lejos\" en
su camino y el coste del rechazo de esos mensajes es menor.

## Trabajo futuro {#future}

### Mezcla/lotes {#tunnel.mixing}

¿Qué estrategias pueden usarse en la puerta de salida y en cada salto
para retrasar, re-ordenar, re-enrutar o rellenar los mensajes? ¿En qué
medida debe hacerse esto automáticamente, que configuraciones debemos
poner por túnel o por salto, y cómo debe controlar esta operación el
creador del túnel (y por lo tanto el usuario)? Todo esto se queda en el
aire, para ser estudiado en una versión futura distante.

### Relleno

Las estrategias de relleno pueden ser usadas en varios niveles, evitando
la exposición del tamaño de los mensajes a los adversarios. El tamaño
actual fijo del túnel es de 1024 bytes. Pero los propios mensajes
fragmentados no están rellenados por el túnel, por lo que en lo mensajes
de fin a fin, deben ser rellenados como parte del envase garlic.

### WRED

Las estrategias WRED tienen un impacto importante en el rendimiento de
fin a fin, y en la prevención del colapso de la congestión de la red.
Esta estrategia WRED actual debería ser evaluada cuidadosamente y
mejorada.


