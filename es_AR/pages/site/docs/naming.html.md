 Libreta de nombres
y direcciones 2025-01
0.9.65 

## Información general {#overview}

I2P viene con una librería genérica de asignación de nombres y una
implementación base diseñada para entregar un mapeado desde nombre local
a destino, además de una aplicación add-on llamada [libreta de
direcciones](#addressbook) (\`adressbook\`). I2P también soporta
[nombres de servidor Base32](#base32) similares a las direcciones .onion
de Tor.

La libreta de direcciones es un sistema de nombres asegurado mediante
web-of-trust, distribuido, y legible por humanos, que tan solo sacrifica
el que los nombres sean globalmente únicos, obligando a que sólo lo sean
localmente. Mientras todos los mensajes en I2P son criptográficamente
direccionados por su destino, diferentes personas puede tener diferentes
entradas \"Alice\" en sus libros de direcciones locales que se refieran
a diferentes destinos. El público aún puede descubrir nuevos nombres
importando libros de direcciones publicados, de pares (\`peers\`)
especificados en sus web-of-trust, incorporando las entradas provistas
por terceros, o (si algunas personas organizan series de libros de
direcciones publicados usando un sistema de registro tipo \`primero en
venir primero en ser servido\`) la gente puede elegir tratar estos
libros de direcciones como servidores de nombres, emulando al
tradicional DNS.

NOTE: For the reasoning behind the I2P naming system, common arguments
against it and possible alternatives see the [naming
discussion]() page.

## Componentes del sistema de nombres {#components}

No hay una autoridad central de nombres en I2P. Todos los nombres de
servidor están en local.

El sistema de nombres es bastante simple, y la mayoria de él está
implementado en aplicaciones externas al router pero empaquetadas con la
distribución I2P. Los componentes son:

1. El [servicio de nombres](#lookup) local que hace búsquedas y también
 maneja los [nombres de equipos Base32](#base32).
2. El [proxy HTTP](#httpproxy) que realiza consultas al router I2P y
 dirige al usuario a servicios de salto (jump, de direccionamiento
 distribuido) remotos para asistirle con las consultas fallidas.
3. [Formularios de añadido de servidores](#add-services) HTTP que
 permiten a los usuarios añadir servidores a su hosts.txt local.
4. [Servicios de salto (jump)](#jump-services) HTTP que proporcionan
 sus propias búsquedas y redireccionamiento distribuido.
5. La aplicación de [libreta de direcciones](#addressbook) que fusiona
 listas externas de servidores, con la lista local.
6. La aplicación [SusiDNS](#susidns) que es un sencillo frontal web
 para la configuración de la libreta de direcciones y el visionado de
 las listas locales de servidores.

## Naming Services {#lookup}

All destinations in I2P are 516-byte (or longer) keys. (To be more
precise, it is a 256-byte public key plus a 128-byte signing key plus a
3-or-more byte certificate, which in Base64 representation is 516 or
more bytes. Non-null
[Certificates](#certificates) are in
use now for signature type indication. Therefore, certificates in
recently-generated destinations are more than 3 bytes.

Si una aplicación (i2ptunnel o el proxy HTTP) quiere acceder a un
destino mediante el nombre, el router hace una búsqueda local muy simple
para resolver ese nombre.

### Hosts.txt Naming Service

El servicio de nombres hosts.txt hace una búsqueda lineal simple a
través de ficheros de texto. Este servicio de nombres fue la norma hasta
la versión 0.8.8 cuando fue reemplazado por el servicio de nombres
blockfile (fichero de bloques). El formato de hosts.txt ha llegado a ser
demasiado lento después de que el fichero creciera hasta las miles de
entradas.

It does a linear search through three local files, in order, to look up
host names and convert them to a 516-byte destination key. Each file is
in a simple [configuration file
format](), with hostname=base64, one per
line. The files are:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile Naming Service

El servicio de nombres blockfile (fichero de bloques) almacena múltiples
\"addressbooks\" (libretas de direcciones) en un único fichero de base
de datos llamado hostsdb.blockfile. Este servicio de nombres es el
predeterminado desde la versión 0.8.8.

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

Al crearse, el servicio de nombres importa entradas desde los tres
ficheros usados por el servicio de nombres hosts.txt. El blockfile imita
la anterior implementación al mantener tres mapeados que se buscan
en-orden, llamados privatehosts.txt, userhosts.txt, y hosts.txt. También
mantiene un mapeado de búsqueda-inversa para implementar búsquedas
inversas rápidas.

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

The HTTP proxy does a lookup via the router for all hostnames ending in
\'.i2p\'. Otherwise, it forwards the request to a configured HTTP
outproxy. Thus, in practice, all HTTP (I2P Site) hostnames must end in
the pseudo-Top Level Domain \'.i2p\'.

Si el router I2P falla al resolver el nombre del servidor, el proxy HTTP
devuelve una página de error al usuario con enlaces a varios servicios
de salto (jump, direccionamiento distribuido). Más detalles debajo.

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

## Libreta de direcciones {#addressbook}

### Suscripciones entrantes y fusionado

La aplicación de la libreta de direcciones obtiene periódicamente los
ficheros hosts.txt de otros usuarios y los fusiona con el fichero
hosts.txt local tras varias comprobaciones. Los conflictos de nombres se
resuelven en base al criterio \`el primero en venir es el primero en ser
servido\`.

Suscribirse al fichero hosts.txt de otros usuarios implica darles un
cierto nivel de confianza. No querrá que ellos, por ejemplo,
\'secuestren\' un sitio nuevo introduciendo rápidamente su propia clave
para el nuevo sitio antes de pasarle el nuevo servidor/clave a usted.

Por esta razón, el único suscriptor configurado por defecto es
`http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`,
que contiene una copia del hosts.txt incluido en la versión de I2P. Los
usuarios tienen que configurar suscripciones adicionales en sus
aplicaciones de libreta de direcciones (vía suscriptions.txt o
[SusiDNS](#susidns)).

Some other public address book subscription links:

- [http:///cgi-bin/i2hostetag](http:///cgi-bin/i2hostetag)
- [http:///cgi-bin/newhosts.txt](http:///cgi-bin/newhosts.txt)

Los operadores de estos servicios pueden tener diferentes políticas para
listar servidores. La presencia en esta lista no implica su respaldo.

### Reglas de nombres

Aunque afortunadamente no hay limitación técnica alguna en I2P para los
nombres de servidor, la libreta de direcciones impone varias
restricciones sobre los nombres de servidor importados desde
suscripciones. Hace esto por higiene tipográfica básica y compatibilidad
con navegadores, y por seguridad. Las reglas son esencialmente las
mismas que aquellas de la Sección 3.2.2. en el RFC2396. Cualquier nombre
de servidor que viole esas reglas puede no ser propagado a otros
routers.

Reglas de nombres:

- Los nombres se convierten a minúsculas al importarlos.
- Se comprueban los conflictos entre los nombres y los nombres
 existentes en userhosts.txt y hosts.txt (pero no privatehosts.txt)
 tras su conversión a minúsculas.
- Sólo deben contener \[a-z\] \[0-9\] \'.\' y \'-\' tras su conversión
 a minúsculas.
- No deben comenzar con \'.\' o \'-\'.
- Debe terminar en «.i2p».
- Máximo 67 caracteres, incluyendo el \'.i2p\'.
- No puede contener «..».
- No deben contener \'.-\' o \'-.\' (a partir de la 0.6.1.33).
- No deben contener \'\--\' excepto en \'xn\--\' para IDN.
- Los nombres de equipo Base32 (\*.b32.i2p) están reservados para el
 uso de base 32 y por tanto no está permitida su importación.
- Certain hostnames reserved for project use are not allowed
 (proxy.i2p, router.i2p, console.i2p, mail.i2p, \*.proxy.i2p,
 \*.router.i2p, \*.console.i2p, \*.mail.i2p, and others)
- Hostnames starting with \'www.\' are discouraged and are rejected by
 some registration services. Some addressbook implementations
 automatically strip \'www.\' prefixes from lookups. So registring
 \'www.example.i2p\' is unnecessary, and registering a different
 destination for \'www.example.i2p\' and \'example.i2p\' will make
 \'www.example.i2p\' unreachable for some users.
- Se comprueba la validez base64 de las claves.
- Se comprueba si las claves tienen conflictos con claves existentes
 en hosts.txt (pero no privatehosts.txt).
- La longitud mínima de clave es 516 bytes.
- La longitud máxima de clave es 616 bytes (para contar con
 certificados de hasta 100 bytes).

Cualquier nombre recibido vía suscripción que pase todas las
comprobaciones, se añade a través del servicio de nombres local.

Observe que los símbolos \'.\' en el nombre de servidor no tienen
significado, y no denotan jerarquía de confianza o de nombres alguna. Si
el nombre \'host.i2p\' ya existe, no hay nada que evite que alguien
añada un nombre \'a.host.i2p\' a su(s) hosts.txt, y este nombre pueda
ser importado por las libretas de direcciones de otros. Los métodos para
denegar subdominios a propietarios de no-dominios (¿certificados?), y lo
deseable y factible de estos métodos, son temas para futura discusión.

Los Nombres de Dominio Internacionales (IDN) también funcionan con I2P
(usando la forma punycode \'xn\--\'). Para ver nombres de dominio .i2p
IDN correctamente formados en la barra de direcciones de Firefox, añada
\'network.IDN.whitelist.i2p (boolean) = true\' en about:config

Como la aplicación libreta de direcciones no usa privatehosts.txt para
nada, en la práctica este fichero es el único lugar donde es apropiado
emplazar alias privados o \"nombres de mascota\" para sitios ya
existentes en hosts.txt

### Formato de suscripción (feed) avanzado

As of release 0.9.26, subscription sites and clients may support an
advanced hosts.txt feed protocol that includes metadata including
signatures. This format is backwards-compatible with the standard
hosts.txt hostname=base64destination format. See [the
specification](/spec/subscription) for details.

### Suscripciones salientes

Address Book will publish the merged hosts.txt to a location
(traditionally hosts.txt in the local I2P Site\'s home directory) to be
accessed by others for their subscriptions. This step is optional and is
disabled by default.

### Hosting and HTTP Transport Issues

La aplicación libreta de direcciones, junto con eepget, previene que la
información del Etag y/o la de Última-modificación sea devuelta por el
servidor web de la suscripción. Esto reduce enormemente el ancho de
banda requerido ya que el servidor web devolverá un \'304 No
Modificado\' en la la siguiente toma de datos (\`fetch\`) si nada ha
cambiado.

Sin embargo, si ha cambiado se descarga el hosts.txt completo. Mire
debajo las discusiones sobre este asunto.

Se recomienda que los servidores que sirven un archivo host.txt o una
aplicación CGI equivalente, lleven una cabecera con el tqmaño del
contenido, Content-Length header, y una Etag o la última cabecera
modificada, Last-Modified header. Además asegúrese de que el servidor
muestra el aviso \'304 Not Modified\' cuando sea apropiado. Esto
reducirá dramáticamente el ancho de banda usado, y reducirá las
posibilidades de corrupción.

## Servicio de gestión de dominios {#add-services}

Un servicio de gestión de dominios es una aplicación CGI simple que toma
un nombre de dominio y una clave Base64 como parámetros y loa añade a su
hosts.txt local. SI otros ruters se suscriben a ese host.txt, el nuevo
nombre de domino/clave serán propagados a través de la red.

Se recomienda que los servicios de gestión de dominios impongan, como
mínimo, las restricciones impuestas por la aplicación libreta de
direcciones listadas anteriormente. Los servicios de gestión de dominios
deben imponer restricciones adicionales en los nombres de dominio y en
las claves, por ejemplo:

- Un \'límite\' en el número de \'subdominios\'.
- Autorización para los \'subdominios\' a través de varios métodos.
- Hashcash o certificados firmados.
- Revisión editorial de los nombres de dominio y/o su contenido.
- Clasificación de los dominios según su contenido.
- Reserva o rechazo de ciertos dominios.
- Restricciones en el número de dominios registrados en un determinado
 periodo de tiempo.
- Intervalos entre los registros y las publicaciones.
- Exigir que el servidor esté funcionando para su verificaión.
- Expiración y/o revocación.
- Denegación de IDN spoof.

## Servicios de salto (jump) {#jump-services}

Un servicio de salto (jump), es una simple aplicación CGI que toma un
nombre de servidor como parámetro y devuelve un redireccionamiento 301
hacia la URL adecuada con una cadena de texto `?i2paddresshelper=clave`
anexa. El proxy HTTP interpretará la cadena de texto anexa y usará esa
clave como el destino I2P de facto. Además, el proxy guardará en caché
esa clave de forma que el ayudante de direccionamiento (address helper)
no sea necesario hasta reiniciar.

Dese cuenta que, al igual que con las suscripciones, usar un servicio de
salto (jum p, direccionamiento distribuido) implica una cierta dosis de
confianza, ya que un servicio de salto podría redirigir maliciosamente a
un usuario a un destino I2P incorrecto.

Para proporcionar el mejor servicio, un servicio de salto (jump,
direccionamiento distribuido) debe estar suscrito a varios proveedores
de ficheros hosts.txt para que su lista local de servidores esté al día.

## SusiDNS

SusiDNS is simply a web interface front-end to configuring address book
subscriptions and accessing the four address book files. All the real
work is done by the \'address book\' application.

Currently, there is little enforcement of address book naming rules
within SusiDNS, so a user may enter hostnames locally that would be
rejected by the address book subscription rules.

## Dominios Base32 {#base32}

I2P soporta nombres de dominios Base32 similares a las direcciones
.onion de Tor. Las direcciones Base32 son mucho más fáciles de manejar y
mucho más cortas que los addresshelpers o las Destinaciones Base64 de
516 caracteres. Ejemplo:
`ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

In Tor, the address is 16 characters (80 bits), or half of the SHA-1
hash. I2P uses 52 characters (256 bits) to represent the full SHA-256
hash. The form is {52 chars}.b32.i2p. Tor has a
[proposal](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013)
to convert to an identical format of {52 chars}.onion for their hidden
services. Base32 is implemented in the naming service, which queries the
router over I2CP to lookup the LeaseSet to get the full Destination.
Base32 lookups will only be successful when the Destination is up and
publishing a LeaseSet. Because resolution may require a network database
lookup, it may take significantly longer than a local address book
lookup.

Las direcciones Base32 pueden ser usadas en la mayoría de sitios donde
se puedan usar los nombres de dominios o la Destinación completa, aunque
hay algunas excepciones donde podría fallar sin el dominio no se
resuelve inmediatamente, Por ejemplo, I2PTunnel fallará si el domino no
resuelve una destinación.

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


