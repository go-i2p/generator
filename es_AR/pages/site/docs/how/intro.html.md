 Una breve
introducción de cómo funciona I2P 

I2P es un proyecto para construir, desplegar y mantener una red que
soporte comunicación segura y anónima. Los usuarios de I2P pueden
administrar el balance entre el anonimato, fiabilidad, uso de ancho de
banda y latencia. No hay un punto central en la red sobre el cual se
pueda ejercer presión para comprometer la integridad, seguridad y
anonimato del sistema. La red soporta reconfiguración dinámica en
respuesta a diversos ataques, y ha sido diseñada para hacer uso de
recursos adicionales según vayan estando disponibles. Por supuesto,
todos los aspectos de la red son abiertos y están a libre disposición.

A diferencia de la mayoría de las redes anónimas, I2P no intenta
proporcionar anonimato ocultando al autor de una comunicación y no al
destinatario, o vice versa. Al contrario: I2P está diseñada para
permitir a los pares comunicarse unos con otros anónimamente - ambos,
quien envía y quien recibe, no son identificables entre ellos y tampoco
por terceras partes. Por ejemplo, actualmente hay sitios web I2P
internos (permitiendo publicación y hospedaje anónimo) además de proxies
HTTP hacia la web normal (permitiendo navegación anónima). Disponer de
la posibilidad de correr servidores internamente en I2p es esencial, ya
que es bastante probable que cualquier proxy de salida hacia el Internet
normal pueda ser monitorizado, desactivado o incluso comprometido para
luego intentar más ataques maliciosos.

The network itself is message oriented - it is essentially a secure and
anonymous IP layer, where messages are addressed to cryptographic keys
(Destinations) and can be significantly larger than IP packets. Some
example uses of the network include \"I2P Sites\" (webservers hosting
normal web applications within I2P), a BitTorrent client (\"I2PSnark\"),
or a distributed data store. With the help of the
[I2PTunnel]() application, we are able to
stream traditional TCP/IP applications over I2P, such as SSH, IRC, a
squid proxy, and even streaming audio. Most people will not use I2P
directly, or even need to know they\'re using it. Instead their view
will be of one of the I2P enabled applications, or perhaps as a little
controller app to turn on and off various proxies to enable the
anonymizing functionality.

An essential part of designing, developing, and testing an anonymizing
network is to define the [threat model](),
since there is no such thing as \"true\" anonymity, just increasingly
expensive costs to identify someone. Briefly, I2P\'s intent is to allow
people to communicate in arbitrarily hostile environments by providing
good anonymity, mixed in with sufficient cover traffic provided by the
activity of people who require less anonymity. This way, some users can
avoid detection by a very powerful adversary, while others will try to
evade a weaker entity, *all on the same network*, where each one\'s
messages are essentially indistinguishable from the others.

## ¿Por qué?

There are a multitude of reasons why we need a system to support
anonymous communication, and everyone has their own personal rationale.
There are many [other efforts]() working on
finding ways to provide varying degrees of anonymity to people through
the Internet, but we could not find any that met our needs or threat
model.

## ¿Cómo?

The network at a glance is made up of a set of nodes (\"routers\") with
a number of unidirectional inbound and outbound virtual paths
(\"tunnels\", as outlined on the [tunnel
routing]() page). Each router is
identified by a cryptographic RouterIdentity which is typically long
lived. These routers communicate with each other through existing
transport mechanisms (TCP, UDP, etc), passing various messages. Client
applications have their own cryptographic identifier (\"Destination\")
which enables it to send and receive messages. These clients can connect
to any router and authorize the temporary allocation (\"lease\") of some
tunnels that will be used for sending and receiving messages through the
network. I2P has its own internal [network
database]() (using a modification of the Kademlia
algorithm) for distributing routing and contact information securely.

::: {.box style="text-align:center;"}
![Ejemplo de topología de
red](images/net.png "Ejemplo de topología de red")
:::

En la imagen, Alice, Bob, Charlie y Dave están corriendo ruters con una
simple Destinación en su ruter local. Cada uno de ellos tiene un par de
túneles de dos saltos entrantes por destino (etiquetados como 1, 2, 3,
4, 5 y 6), y una pequeña parte del grupo de los túneles de salida de
esos ruters se representa con túneles de salida de dos saltos. Para
simplificar, los túneles entrantes de Charlie y los de salida de Dave no
se muestran, tampoco está el resto del grupo de túneles de salida de
cada ruter (típicamente compuesto por varios túneles a la vez). Cuando
Alice y Bob se comunican entre ellos, Alice envía un mensaje por uno de
sus túneles de salida (rosa) en dirección a uno de los túneles entrantes
(verde) de Bob (túnel 3 o 4). Ella sabe cómo enviar a los túneles del
ruter correcto mediante consultas a la base de datos de red, que está
constantemente actualizándose tan pronto cómo son autorizados nuevos
contactos y expiran los viejos.

If Bob wants to reply to Alice, he simply goes through the same
process - send a message out one of his outbound tunnels targeting one
of Alice\'s inbound tunnels (tunnel 1 or 2). To make things easier, most
messages sent between Alice and Bob are
[garlic]() wrapped, bundling the
sender\'s own current lease information so that the recipient can reply
immediately without having to look in the network database for the
current data.

To deal with a wide range of attacks, I2P is fully distributed with no
centralized resources - and hence there are no directory servers keeping
statistics regarding the performance and reliability of routers within
the network. As such, each router must keep and maintain profiles of
various routers and is responsible for selecting appropriate peers to
meet the anonymity, performance, and reliability needs of the users, as
described in the [peer selection]() page.

The network itself makes use of a significant number of [cryptographic
techniques and algorithms]() - a full
laundry list includes 2048bit ElGamal encryption, 256bit AES in CBC mode
with PKCS#5 padding, 1024bit DSA signatures, SHA256 hashes, 2048bit
Diffie-Hellman negotiated connections with station to station
authentication, and [ElGamal /
AES+SessionTag]().

El contenido enviado sobre I2P está cifrado a través del cifrado garlic
de tres capas (usado para verificar la entrega del mensaje a
destinatario), cifrado de túnel (todos los mensajes cruzando a través de
un túnel están cifrados desde el túnel de salida hasta el túnel de
destino final) y cifrado de la capa de transporte inter-router (e. g. el
transporte TCP usa AES256 con claves efímeras).

End-to-end (I2CP) encryption (client application to server application)
was disabled in I2P release 0.6; end-to-end (garlic) encryption (I2P
client router to I2P server router) from Alice\'s router \"a\" to Bob\'s
router \"h\" remains. Notice the different use of terms! All data from a
to h is end-to-end encrypted, but the I2CP connection between the I2P
router and the applications is not end-to-end encrypted! A and h are the
routers of Alice and Bob, while Alice and Bob in following chart are the
applications running atop of I2P.

::: {.box style="text-align:center;"}
![Cifrado por capas de punto a
punto](images/endToEndEncryption.png "Cifrado por capas de punto a punto")
:::

The specific use of these algorithms are outlined
[elsewhere]().

Los dos mecanismos principales que permiten usar la red a gente que
necesita un fuerte anonimato son explícitamente mensajes enrutados
garlic con retardo y túneles más completos que incluyan agrupamiento y
mezcla de mensajes. Estos están actualmente planeados para la release
3.0, pero los mensajes enrutados garlic sin retardo y túneles FIFO están
ya implementados. Adicionalmente la versión 2.0 permitirá a los usuarios
establecerse y operar detrás de ruters restrictivos (puede que con pares
de confianza), así como el despliegue de transportes más flexibles y
anónimos.

Some questions have been raised with regards to the scalability of I2P,
and reasonably so. There will certainly be more analysis over time, but
peer lookup and integration should be bounded by `O(log(N))` due to the
[network database]()\'s algorithm, while end to
end messages should be `O(1)` (scale free), since messages go out K hops
through the outbound tunnel and another K hops through the inbound
tunnel, with K no longer than 3. The size of the network (N) bears no
impact.

## ¿Cuándo?

I2P initially began in Feb 2003 as a proposed modification to
[Freenet](http://freenetproject.org) to allow it to use alternate
transports, such as [JMS](), then grew into its own
as an \'anonCommFramework\' in April 2003, turning into I2P in July,
with code being written in earnest starting in August \'03. I2P is
currently under development, following the
[roadmap]().

## ¿Quiénes?

We have a small [team]() spread around several
continents, working to advance different aspects of the project. We are
very open to other developers who want to get involved and anyone else
who would like to contribute in other ways, such as critiques, peer
review, testing, writing I2P enabled applications, or documentation. The
entire system is open source - the router and most of the SDK are
outright public domain with some BSD and Cryptix licensed code, while
some applications like I2PTunnel and I2PSnark are GPL. Almost everything
is written in Java (1.5+), though some third party applications are
being written in Python and other languages. The code works on [Sun Java
SE](http://java.com/en/) and other Java Virtual Machines.

## ¿Dónde?

Anyone interested should join us on the IRC channel #i2p-dev (hosted
concurrently on irc.freenode.net, irc.postman.i2p, irc.echelon.i2p,
irc.dg.i2p and irc.oftc.net). There are currently no scheduled
development meetings, however [archives are
available]().

The current source is available in [git]().

## Información adicional

See [the Index to Technical Documentation]().


