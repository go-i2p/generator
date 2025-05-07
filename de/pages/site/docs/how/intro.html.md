 Einführung in die
Arbeitsweise von I2P 

I2P ist ein Projekt, welches ein Netzwerk zum sicheren und anonymen
Kommunizieren planen, aufbauen und betreuen wird. Nutzer von I2P haben
die Kontrolle über die Verteilung zwischen Anonymität, Verlässlichkeit,
genutzter Bandbreite und Verzögerung. Es gibt keinen zentralen Punkt im
Netzwerk, welcher übernommen werden kann um die Integrität, Sicherheit
oder Anonymität des Systems zu komprimieren. Das Netzwerk kann sich in
einer Reaktion auf Angriffe selber rekonfiguriern und wurde so geplant,
das es zusätzliche Ressourcen bei deren Verfügbarkeit nutzen wird.
Selbstverständlich sind alle Aspekte des Netzwerkes offen und frei
verfügbar.

Im Gegensatz zu vielen anderen anonymen Netzwerken versucht I2P nicht
die Anonymität durch verstecken eines Teils einer Kommunikation, der
Sender oder der Empfänger, herzustellen. I2P wurde so geplant, das
Nutzer von I2P untereinander anonym kommunizieren können - Sender und
Empfänger sind für den jeweils anderen anonym als auch für nicht
beteiligte dritte. Zum Beispiel gibt es zur Zeit I2P interne Webseiten
(die anonymes Publizieren/hosten erlauben) und einen HTTP Proxy in das
normale Internet (der anonymes Browsing bietet). Server im I2P Netz
betreiben zu können ist eine essentielle Angelegenheit, da angenommen
werden kann, das die Proxis ins normale Internet überwacht werden,
abgeschaltet werden oder gar zu schlimmeren Angriffen genutzt werden.

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

## Warum?

There are a multitude of reasons why we need a system to support
anonymous communication, and everyone has their own personal rationale.
There are many [other efforts]() working on
finding ways to provide varying degrees of anonymity to people through
the Internet, but we could not find any that met our needs or threat
model.

## Wie?

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
![Network topology
example](images/net.png "Network topology example")
:::

Im oberen Bild betreiben Alice, Bob, Charlie und Dave je einen Router
mit einer einzigen Destination auf ihren lokalen Router. Sie haben alle
ein paar 2-Hop Eingangstunnel je Destination (mit 1, 2, 3, 4, 5 und 6
bezeichnet) und ein paar haben 2-Hop Ausgangstunnel. Zur Vereinfachung
sind Charlies Eingangstunnel und Daves Ausgangstunnel nicht
eingezeichnet, ebenso wie weitere Ausgangstunnel der Router
(normalerweise so 5-10 Tunnel gleichzeitig). Sobald Alice und Bob
miteiander reden, sendet Alice eine Nachricht über ihren (pinken)
Ausgangstunnel in Richtung eines vons Bobs Eingangstunneln (grün, Tunnel
3 oder 4). Sie lernt den Eingangstunnel durch eine Abfrage der Netzwerk
Datenbank kennen, diese Datenbank wird dauerhaft aktualisiert sobald
neue Leases authorisiert sind und ältere auslaufen.

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

Daten die über I2P gesendet werden, durchlaufen 3 Verschlüsselungen:
garlic Verschlüsselung (zur überprüfung ob die Nachrichten beim
Empfänger angekommen ist), Tunnelverschlüsselung (alle Nachrichten, die
durch einen Tunnel gehen, sind vom Tunnel-Gateway bis zum Tunnelendpunkt
verschlüsselt) und Zwischen-den-Routern-Übertragungsschicht
Verschlüsselung (z.B. benutzt die TCP-Übertragung AES256 mit Ephemeral
Schlüssel).

End-to-end (I2CP) encryption (client application to server application)
was disabled in I2P release 0.6; end-to-end (garlic) encryption (I2P
client router to I2P server router) from Alice\'s router \"a\" to Bob\'s
router \"h\" remains. Notice the different use of terms! All data from a
to h is end-to-end encrypted, but the I2CP connection between the I2P
router and the applications is not end-to-end encrypted! A and h are the
routers of Alice and Bob, while Alice and Bob in following chart are the
applications running atop of I2P.

::: {.box style="text-align:center;"}
![End to end layered
encryption](images/endToEndEncryption.png "End to end layered encryption")
:::

The specific use of these algorithms are outlined
[elsewhere]().

Die zwei Hauptbestandteile für den militärischen Grad der Anonymität
sind explizite, verzögerte garlic geroutete Nachrichten und mehr
umfassende Tunnel mit Unterstützung von Pooling und Mixen von
Nachrichten. Diese Funktionen sind zur Zeit für Version 3.0 geplant,
aber garlic geroutete Nachrichten mit keiner Verzögerung und FIFO
Tunnels sind schon implementiert. Zusätzlich wird die Version 2.0 den
Leuten erlauben, I2P hinter beschränkten Routen (möglicherweise mit
vertrauten Knoten) aufzusetzen und zu betreiben; ebenso werden die
flexiblere und anonymere Übertragungen eingebaut werden.

Some questions have been raised with regards to the scalability of I2P,
and reasonably so. There will certainly be more analysis over time, but
peer lookup and integration should be bounded by `O(log(N))` due to the
[network database]()\'s algorithm, while end to
end messages should be `O(1)` (scale free), since messages go out K hops
through the outbound tunnel and another K hops through the inbound
tunnel, with K no longer than 3. The size of the network (N) bears no
impact.

## Wann?

I2P initially began in Feb 2003 as a proposed modification to
[Freenet](http://freenetproject.org) to allow it to use alternate
transports, such as [JMS](), then grew into its own
as an \'anonCommFramework\' in April 2003, turning into I2P in July,
with code being written in earnest starting in August \'03. I2P is
currently under development, following the
[roadmap]().

## Wer?

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

## Wo?

Anyone interested should join us on the IRC channel #i2p-dev (hosted
concurrently on irc.freenode.net, irc.postman.i2p, irc.echelon.i2p,
irc.dg.i2p and irc.oftc.net). There are currently no scheduled
development meetings, however [archives are
available]().

The current source is available in [git]().

## Weitere Informationen

See [the Index to Technical Documentation]().


