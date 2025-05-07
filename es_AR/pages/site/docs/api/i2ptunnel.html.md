 I2PTunnel 2023-10 0.9.59 

## Información general {#overview}

I2PTunnel is a tool for interfacing with and providing services on I2P.
Destination of an I2PTunnel can be defined using a
[hostname](),
[Base32](#base32), or a full 516-byte
destination key. An established I2PTunnel will be available on your
client machine as localhost:port. If you wish to provide a service on
I2P network, you simply create I2PTunnel to the appropriate
ip_address:port. A corresponding 516-byte destination key will be
generated for the service and it will become avaliable throughout I2P. A
web interface for I2PTunnel management is avaliable on
[localhost:7657/i2ptunnel/](http://localhost:7657/i2ptunnel/).

## Servicios predeterminados {#default-services}

### Túneles de servidor {#default-server-tunnels}

- **I2P Webserver** - A tunnel pointed to a Jetty webserver run on
 [localhost:7658](http://localhost:7658) for convenient and quick
 hosting on I2P.\
 The document root is:\
 **Unix** - \$HOME/.i2p/eepsite/docroot\
 **Windows** - %LOCALAPPDATA%\\I2P\\I2P Site\\docroot, which expands
 to: C:\\Users\*\*username\*\*\\AppData\\Local\\I2P\\I2P
 Site\\docroot

### Túneles de cliente {#default-client-tunnels}

- **I2P HTTP Proxy** - *localhost:4444* - A HTTP proxy
 used for browsing I2P and the regular internet anonymously through
 I2P. Browsing internet through I2P uses a random proxy specified by
 the \"Outproxies:\" option.
- **Irc2P** - *localhost:6668* - Un túnel IRC hasta la red IRC anónima
 por defecto, Irc2P.
- **gitssh.idk.i2p** - *localhost:7670* - SSH access to the project
 Git repository
- **smtp.postman.i2p** - *localhost:7659* - A SMTP service provided by
 postman at [](http:///?page_id=16)
- **pop3.postman.i2p** - *localhost:7660* - The accompanying POP
 sevice of postman at [](http:///?page_id=16)

## Configuración {#client-modes}

[I2PTunnel
Configuration]()

## Modos de cliente {#client-modes}

### Estándar {#client-modes-standard}

Abre un puerto TCP local que conecta con un servicio (como HTTP, FTP o
SMTP) en un destino dentro de I2P. El túnel es dirigido a un servidor
aleatorio desde la lista de destinos separados por comas (\", \").

### HTTP {#client-mode-http}

Un túnel de cliente-HTTP. El túnel conecta con el destino especificado
por la URL en una petición HTTP. Soporta proxificación en Internet si se
proporciona un proxy externo (\`outproxy\`). Desnuda las conexiones HTTP
de las siguientes cabeceras:

- **Accept\*:** (not including \"Accept\" and \"Accept-Encoding\") as
 they vary greatly between browsers and can be used as an identifier.
- **Referer:**
- **Via:**
- **From:**

The HTTP client proxy provides a number of services to protect the user
and to provide a better user experience.

- Request header processing:
 - Strip privacy-problematic headers
 - Routing to local or remote outproxy
 - Outproxy selection, caching, and reachability tracking
 - Hostname to destination lookups
 - Host header replacement to b32
 - Add header to indicate support for transparent decompression
 - Force connection: close
 - RFC-compliant proxy support
 - RFC-compliant hop-by-hop header processing and stripping
 - Optional digest and basic username/password authentication
 - Optional outproxy digest and basic username/password
 authentication
 - Buffering of all headers before passing through for efficiency
 - Jump server links
 - Jump response processing and forms (address helper)
 - Blinded b32 processing and credential forms
 - Supports standard HTTP and HTTPS (CONNECT) requests
- Response header processing:
 - Check for whether to decompress response
 - Force connection: close
 - RFC-compliant hop-by-hop header processing and stripping
 - Buffering of all headers before passing through for efficiency
- HTTP error responses:
 - For many common and not-so-common errors, so the user knows what
 happened
 - Over 20 unique translated, styled, and formatted error pages for
 various errors
 - Internal web server to serve forms, CSS, images, and errors

#### Transparent Response Compression

The i2ptunnel response compression is requested with the HTTP header:

- **X-Accept-Encoding:** x-i2p-gzip;q=1.0, identity;q=0.5,
 deflate;q=0, gzip;q=0, \*;q=0

The server side strips this hop-by-hop header before sending the request
to the web server. The elaborate header with all the q values is not
necessary; servers should just look for \"x-i2p-gzip\" anywhere in the
header.

The server side determines whether to compress the response based on the
headers received from the webserver, including Content-Type,
Content-Length, and Content-Encoding, to assess if the response is
compressible and is worth the additional CPU required. If the server
side compresses the response, it adds the following HTTP header:

- **Content-Encoding:** x-i2p-gzip

If this header is present in the response, the HTTP client proxy
transparently decompresses it. The client side strips this header and
gunzips before sending the response to the browser. Note that we still
have the underlying gzip compression at the I2CP layer, which is still
effective if the response is not compressed at the HTTP layer.

This design and the current implementation violate RFC 2616 in several
ways:

- X-Accept-Encoding is not a standard header
- Does not dechunk/chunk per-hop; it passes through chunking
 end-to-end
- Passes Transfer-Encoding header through end-to-end
- Uses Content-Encoding, not Transfer-Encoding, to specify the per-hop
 encoding
- Prohibits x-i2p gzipping when Content-Encoding is set (but we
 probably don\'t want to do that anyway)
- The server side gzips the server-sent chunking, rather than doing
 dechunk-gzip-rechunk and dechunk-gunzip-rechunk
- The gzipped content is not chunked afterwards. RFC 2616 requires
 that all Transfer-Encoding other than \"identity\" is chunked.
- Because there is no chunking outside (after) the gzip, it is more
 difficult to find the end of the data, making any implementation of
 keepalive harder.
- RFC 2616 says Content-Length must not be sent if Transfer-Encoding
 is present, but we do. The spec says ignore Content-Length if
 Transfer-Encoding is present, which the browsers do, so it works for
 us.

Changes to implement a standards-compliant hop-by-hop compression in a
backward-compatible manner are a topic for further study. Any change to
dechunk-gzip-rechunk would require a new encoding type, perhaps
x-i2p-gzchunked. This would be identical to Transfer-Encoding: gzip, but
would have to be signalled differently for compatibility reasons. Any
change would require a formal proposal.

#### Transparent Request Compression

Not supported, although POST would benefit. Note that we still have the
underlying gzip compression at the I2CP layer.

#### Persistence

The client and server proxies do not currently support RFC 2616 HTTP
persistent sockets on any of the three hops (browser socket, I2P socket,
server socket). Connection: close headers are injected at every hop.
Changes to implement a persistence are under investigation. These
changes should be standards-complaint and backwards-compatible, and
would not require a formal proposal.

#### Pipelining

The client and server proxies do not currently support RFC 2616 HTTP
pipelining and there are no plans to do so. Modern browswers do not
support pipelining through proxies because most proxies cannot implement
it correctly.

#### Compatibility

Proxy implementations must work correctly with other implementations on
the other side. Client proxies should work without a HTTP-aware server
proxy (i.e. a standard tunnel) on the server side. Not all
implementations support x-i2p-gzip.

#### User Agent

Dependiendo de si el túnel está usando un proxy externo (\`outproxy\`) o
no, adherirá el siguiente Agente de Usuario (\`User-Agent\`):

- *Proxy de salida:* **User-Agent:** Uses the user agent from a recent
 Firefox release on Windows
- *Uso interno de I2P:* **User-Agent:** MYOB/6.66 (AN/ON)

### IRC Client {#client-mode-irc}

Crea una conexión a un servidor IRC aleatorio especificado por una lista
de destinos separados por coma (\", \"). Sólo un subconjunto de comandos
IRC de la lista blanca están permitidos debido a cuestiones de
anonimato. The following allow list is for commands inbound from the IRC
server to the IRC client.\
Allow list:

- AUTHENTICATE
- CAP
- ERROR
- H
- JOIN
- KICK
- MODE
- NICK
- PART
- PING
- PROTOCTL
- QUIT
- TOPIC
- WALLOPS

There is also an allow list is for commands outbound from the IRC client
to the IRC server. It is quite large due to the number of IRC
administrative commands. See the IRCFilter.java source for details. The
outbound filter also modifies the following commands to strip
identifying information:

- NOTICE
- PART
- PING
- PRIVMSG
- QUIT
- USER

### SOCKS 4/4a/5 {#client-mode-socks}

Habilita el uso del router I2P como un proxy SOCKS.

### SOCKS IRC {#client-mode-socks-irc}

Habilita el uso de un router I2P como un proxy SOCKS con la lista blanca
de comandos especificada por el modo cliente del
[IRC](#client-mode-irc).

### CONNECT {#client-mode-connect}

Crea un túnel HTTP y usa el método de petición HTTP \"CONNECT\" para
construir un túnel TCP que normalmente se usa para SSL y HTTPS.

### Streamr {#client-mode-streamr}

Crea un servidor-UDP adosado a un I2PTunnel de cliente \`Streamr\`. El
túnel del cliente streamr se suscribirá a un túnel de servidor streamr.

![](images/I2PTunnel-streamr.png)\

## Modos de servidor {#server-modes}

### Estándar {#server-mode-standard}

Crea un destino hacia una dirección IP:puerto local con un puerto TCP
abierto.

### HTTP {#server-mode-http}

Crea un destino a un servidor HTTP local IP:puerto Soporta gzip para las
peticiones con \`Accept-encoding: x-i2p-gzip\`, responde con
\`Content-encoding: x-i2p-gzip\` a tal petición.

The HTTP server proxy provides a number of services to make hosting a
website easier and more secure, and to provide a better user experience
on the client side.

- Request header processing:
 - Header validation
 - Header spoof protection
 - Header size checks
 - Optional inproxy and user-agent rejection
 - Add X-I2P headers so the webserver knows where the request came
 from
 - Host header replacement to make webserver vhosts easier
 - Force connection: close
 - RFC-compliant hop-by-hop header processing and stripping
 - Buffering of all headers before passing through for efficiency
- DDoS protection:
 - POST throttling
 - Timeouts and slowloris protection
 - Additional throttling happens in streaming for all tunnel types
- Response header processing:
 - Stripping of some privacy-problematic headers
 - Mime type and other headers check for whether to compress
 response
 - Force connection: close
 - RFC-compliant hop-by-hop header processing and stripping
 - Buffering of all headers before passing through for efficiency
- HTTP error responses:
 - For many common and not-so-common errors and on throttling, so
 the client-side user knows what happened
- Transparent response compression:
 - The web server and/or the I2CP layer may compress, but the web
 server often does not, and it\'s most efficient to compress at a
 high layer, even if I2CP also compresses. The HTTP server proxy
 works cooperatively with the client-side proxy to transparently
 compress responses.

### HTTP Bidirectional {#server-mode-http-bidir}

*Deprecated*

Functions as both a I2PTunnel HTTP Server, and a I2PTunnel HTTP client
with no outproxying capabilities. An example application would be a web
application that does client-type requests, or loopback-testing an I2P
Site as a diagnostic tool.

### IRC Server {#server-mode-irc}

Crea un destino que filtra la secuencia de registro de un cliente y pasa
la clave de destino de los clientes como un nombre de servidor al
servidor-IRC.

### Streamr {#server-mode-streamr}

Se crea un cliente-UDP que conecta a los servidores de medios. El
cliente-UDP está emparejado con el I2PTunnel de servidor Streamr.


