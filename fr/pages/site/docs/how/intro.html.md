 Une présentation
allégée du fonctionnement d'I2P 

I2P est un projet dont le but est de construire, déployer, et maintenir
un réseau fournissant des communications sécurisées et anonymes. Les
gens utilisant I2P ont le contrôle de l'arbitrage entre l'anonymat, la
fiabilité, l'utilisation de la bande passante, et la latence. Il n'y a
dans ce réseau, pas de centre sur lequel pourrait être exercée une
pression en vue de compromettre l'intégrité, la sécurité, ou l'anonymat
du système. Le réseau intègre sa propre reconfiguration dynamique en
réponse aux diverses attaques, et a été conçu pour utiliser de nouvelles
ressources au fur et à mesure de leur disponibilité. Bien entendu, tous
les aspects du réseau sont publics et disponibles gratuitement.

Contrairement à de nombreux autres réseaux anonymisants, I2P n'essaie
pas d'assurer l'anonymat en cachant l'expéditeur d'une communication,
mais pas le destinataire, ou le contraire. I2P est conçu afin de
permettre aux pairs qui l'utilisent de communiquer anonymement ; ni
l'expéditeur ni le destinataire ne peut être identifié par l'autre, ni
par un tiers. Par exemple, il y a aujourd'hui des sites Web intra-I2P
(qui permettent la publication et l'hébergement anonymes), mais aussi
des mandataires HTTP vers le Web normal (qui permettent une navigation
anonyme sur la Toile). Il est essentiel d'avoir la capacité d'exécuter
des serveurs dans I2P, car il est fort probable que tout mandataire
sortant vers l'Internet normal sera surveillé, désactivé ou qu'il sera
même piraté pour tenter des attaques encore plus malveillantes.

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

## Pourquoi ?

There are a multitude of reasons why we need a system to support
anonymous communication, and everyone has their own personal rationale.
There are many [other efforts]() working on
finding ways to provide varying degrees of anonymity to people through
the Internet, but we could not find any that met our needs or threat
model.

## Comment ?

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
![Exemple de topologie du
réseau](images/net.png "Exemple de topologie du réseau")
:::

Ci-dessus, Alice, Bob, Charlie, et Dave ont tous leur routeur, avec une
seule Destination locale. Ils ont chacun une paire de tunnels entrants
ayant deux sauts par destination (repérés 1, 2, 3, 4, 5 et 6), et une
petite partie des tunnels sortants de chacun de ces routeurs est montré
avec des tunnels sortants ayant deux sauts. Pour simplifier, ne sont
représentés ni les tunnels entrants de Charlie et les tunnels sortants
de Dave, ni le reste du groupe de tunnels sortants de chaque routeur
(fourni par défaut avec quelques tunnels). Quand Alice et Bob discutent
ensemble, Alice envoie un message vers un de ses tunnels sortants (en
rose) avec pour cible un des tunnels entrants de Bob (3 ou 4, en vert).
Elle sait qu'elle doit envoyer vers ces tunnels sur le bon routeur en
interrogeant la base de donnée du réseau qui est actualisée en
permanence au fur et à mesure que les nouveaux baux sont autorisés et
que les anciens expirent.

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

Les contenus envoyés sur I2P sont chiffrés à travers trois couches de
chiffrement en ail (utilisées pour vérifier la réception du message par
le destinataire), par le chiffrement de tunnel (tous les messages
traversant un tunnel sont chiffrés par la passerelle du tunnel jusqu'au
point de sortie du tunnel), et par un chiffrement de la couche de
transport inter routeurs (p.e. le transport TCP utilise des clés AES256
éphémères).

End-to-end (I2CP) encryption (client application to server application)
was disabled in I2P release 0.6; end-to-end (garlic) encryption (I2P
client router to I2P server router) from Alice\'s router \"a\" to Bob\'s
router \"h\" remains. Notice the different use of terms! All data from a
to h is end-to-end encrypted, but the I2CP connection between the I2P
router and the applications is not end-to-end encrypted! A and h are the
routers of Alice and Bob, while Alice and Bob in following chart are the
applications running atop of I2P.

::: {.box style="text-align:center;"}
![Chiffrement en couches de bout en
bout](images/endToEndEncryption.png "Chiffrement en couches de bout en bout")
:::

The specific use of these algorithms are outlined
[elsewhere]().

Les deux mécanismes principaux pour permettre à ceux qui ont besoin d'un
anonymat renforcer d'utiliser le réseau sont les messages à routage en
ail explicitement retardés et des tunnels plus complets pour prendre en
charge le regroupement et le mélange des messages. Ils sont actuellement
prévus pour la version 3.0, mais les messages à routage en ail sans
retard et les tunnels premiers entrés, premiers sortis (FIFO) sont déjà
en place. De plus, la version 2.0 permettra aux utilisateurs de mettre
en place un système et de le faire fonctionner dans des routes
restreintes (peut-être avec des pairs de confiance), et permettra aussi
le déploiement de transports anonymes plus souples.

Some questions have been raised with regards to the scalability of I2P,
and reasonably so. There will certainly be more analysis over time, but
peer lookup and integration should be bounded by `O(log(N))` due to the
[network database]()\'s algorithm, while end to
end messages should be `O(1)` (scale free), since messages go out K hops
through the outbound tunnel and another K hops through the inbound
tunnel, with K no longer than 3. The size of the network (N) bears no
impact.

## Quand ?

I2P initially began in Feb 2003 as a proposed modification to
[Freenet](http://freenetproject.org) to allow it to use alternate
transports, such as [JMS](), then grew into its own
as an \'anonCommFramework\' in April 2003, turning into I2P in July,
with code being written in earnest starting in August \'03. I2P is
currently under development, following the
[roadmap]().

## Qui ?

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

## Où ?

Anyone interested should join us on the IRC channel #i2p-dev (hosted
concurrently on irc.freenode.net, irc.postman.i2p, irc.echelon.i2p,
irc.dg.i2p and irc.oftc.net). There are currently no scheduled
development meetings, however [archives are
available]().

The current source is available in [git]().

## Renseignements complémentaires

See [the Index to Technical Documentation]().


