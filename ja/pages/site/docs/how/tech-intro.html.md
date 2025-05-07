 I2P: A scalable
framework for anonymous communication 2025-01 0.9.65 

- [序章](#intro)
- [I2P Operation](#op)
 - [概観](#op.overview)
 - [トンネル](#op.tunnels)
 - [ネットワークデータベース検索ツール](#op.netdb)
 - [Transport protocols](#op.transport)
 - [暗号法](#op.crypto)
- [Future](#future)
 - [Restricted Routes](#future.restricted)
 - [Variable Latency](#future.variablelatency)
- [Similar Networks](#similar)
 - [Tor](#similar.tor)
 - [Freenet](#similar.freenet)
- [Application Layer](#app)
 - [Streaming](#app.streaming)
 - [Naming and Addressbook](#app.naming)
 - [I2PSnark](#app.i2psnark)
 - [I2PTunnel](#app.i2ptunnel)
 - [I2P Email](#app.i2pmail)

 

NOTE: This document was originally written by jrandom in 2003. While we
strive to keep it current, some information may be obsolete or
incomplete. The transport and cryptography sections are current as of
2025-01.

# 序章 {#intro}

I2P is a scalable, self organizing, resilient packet switched anonymous
network layer, upon which any number of different anonymity or security
conscious applications can operate. Each of these applications may make
their own anonymity, latency, and throughput tradeoffs without worrying
about the proper implementation of a free route mixnet, allowing them to
blend their activity with the larger anonymity set of users already
running on top of I2P.

Applications available already provide the full range of typical
Internet activities - **anonymous** web browsing, web hosting, chat,
file sharing, e-mail, blogging and content syndication, as well as
several other applications under development.

- Web browsing: using any existing browser that supports using a
 proxy.
- Chat: IRC and other protocols
- File sharing: [I2PSnark](#app.i2psnark) and other applications
- E-mail: [susimail](#app.i2pmail) and other applications
- Blog: using any local web server, or available plugins

Unlike web sites hosted within content distribution networks like
[Freenet](#similar.freenet) or [GNUnet](https://www.gnunet.org/en/), the
services hosted on I2P are fully interactive - there are traditional
web-style search engines, bulletin boards, blogs you can comment on,
database driven sites, and bridges to query static systems like Freenet
without needing to install it locally.

With all of these anonymity enabled applications, I2P takes on the role
of the message oriented middleware - applications say that they want to
send some data to a cryptographic identifier (a \"destination\") and I2P
takes care of making sure it gets there securely and anonymously. I2P
also bundles a simple [streaming](#app.streaming) library to allow
I2P\'s anonymous best-effort messages to transfer as reliable, in-order
streams, transparently offering a TCP based congestion control algorithm
tuned for the high bandwidth delay product of the network. While there
have been several simple SOCKS proxies available to tie existing
applications into the network, their value has been limited as nearly
every application routinely exposes what, in an anonymous context, is
sensitive information. The only safe way to go is to fully audit an
application to ensure proper operation and to assist in that we provide
a series of APIs in various languages which can be used to make the most
out of the network.

I2P is not a research project - academic, commercial, or governmental,
but is instead an engineering effort aimed at doing whatever is
necessary to provide a sufficient level of anonymity to those who need
it. It has been in active development since early 2003 with one full
time developer and a dedicated group of part time contributors from all
over the world. All of the work done on I2P is open source and freely
available on the [website](), with the majority of
the code released outright into the public domain, though making use of
a few cryptographic routines under BSD-style licenses. The people
working on I2P do not control what people release client applications
under, and there are several GPL\'ed applications available
([I2PTunnel](#app.i2ptunnel), [susimail](#app.i2pmail),
[I2PSnark](#app.i2psnark), [I2P-Bote](#app.i2pbote),
[I2Phex](#app.i2phex) and others.).
[Funding]() for I2P comes entirely from
donations, and does not receive any tax breaks in any jurisdiction at
this time, as many of the developers are themselves anonymous.

# Operation {#op}

## 概観 {#op.overview}

To understand I2P\'s operation, it is essential to understand a few key
concepts. First, I2P makes a strict separation between the software
participating in the network (a \"router\") and the anonymous endpoints
(\"destinations\") associated with individual applications. The fact
that someone is running I2P is not usually a secret. What is hidden is
information on what the user is doing, if anything at all, as well as
what router a particular destination is connected to. End users will
typically have several local destinations on their router - for
instance, one proxying in to IRC servers, another supporting the user\'s
anonymous webserver (\"I2P Site\"), another for an I2Phex instance,
another for torrents, etc.

Another critical concept to understand is the \"tunnel\". A tunnel is a
directed path through an explicitly selected list of routers. Layered
encryption is used, so each of the routers can only decrypt a single
layer. The decrypted information contains the IP of the next router,
along with the encrypted information to be forwarded. Each tunnel has a
starting point (the first router, also known as \"gateway\") and an end
point. Messages can be sent only in one way. To send messages back,
another tunnel is required.

::: {.box style="text-align:center;"}
\
\
![Inbound and outbound tunnel
schematic](images/tunnels.png "Inbound and outbound tunnel schematic")\
\
Figure 1: Two types of tunnels exist: inbound and outbound.
:::

Two types of tunnels exist: **\"outbound\" tunnels** send messages away
from the tunnel creator, while **\"inbound\" tunnels** bring messages to
the tunnel creator. Combining these two tunnels allows users to send
messages to each other. The sender (\"Alice\" in the above image) sets
up an outbound tunnel, while the receiver (\"Bob\" in the above image)
creates an inbound tunnel. The gateway of an inbound tunnel can receive
messages from any other user and will send them on until the endpoint
(\"Bob\"). The endpoint of the outbound tunnel will need to send the
message on to the gateway of the inbound tunnel. To do this, the sender
(\"Alice\") adds instructions to her encrypted message. Once the
endpoint of the outbound tunnel decrypts the message, it will have
instructions to forward the message to the correct inbound gateway (the
gateway to \"Bob\").

A third critical concept to understand is I2P\'s **\"network
database\"** (or \"netDb\") - a pair of algorithms used to share network
metadata. The two types of metadata carried are **\"routerInfo\"** and
**\"leaseSets\"** - the routerInfo gives routers the data necessary for
contacting a particular router (their public keys, transport addresses,
etc), while the leaseSet gives routers the information necessary for
contacting a particular destination. A leaseSet contains a number of
\"leases\". Each of this leases specifies a tunnel gateway, which allows
reaching a specific destination. The full information contained in a
lease:

- Inbound gateway for a tunnel that allows reaching a specific
 destination.
- Time when a tunnel expires.
- Pair of public keys to be able to encrypt messages (to send through
 the tunnel and reach the destination).

Routers themselves send their routerInfo to the netDb directly, while
leaseSets are sent through outbound tunnels (leaseSets need to be sent
anonymously, to avoid correlating a router with his leaseSets).

We can combine the above concepts to build successful connections in the
network.

To build up her own inbound and outbound tunnels, Alice does a lookup in
the netDb to collect routerInfo. This way, she gathers lists of peers
she can use as hops in her tunnels. She can then send a build message to
the first hop, requesting the construction of a tunnel and asking that
router to send the construction message onward, until the tunnel has
been constructed.

::: {.box style="text-align:center;"}
\
\
![Request information on other
routers](images/netdb_get_routerinfo_1.png "Request information on other routers")
                   \
\
![Build tunnel using router
information](images/netdb_get_routerinfo_2.png "Build tunnel using router information")\
\
Figure 2: Router information is used to build tunnels.
:::

\

When Alice wants to send a message to Bob, she first does a lookup in
the netDb to find Bob\'s leaseSet, giving her his current inbound tunnel
gateways. She then picks one of her outbound tunnels and sends the
message down it with instructions for the outbound tunnel\'s endpoint to
forward the message on to one of Bob\'s inbound tunnel gateways. When
the outbound tunnel endpoint receives those instructions, it forwards
the message as requested, and when Bob\'s inbound tunnel gateway
receives it, it is forwarded down the tunnel to Bob\'s router. If Alice
wants Bob to be able to reply to the message, she needs to transmit her
own destination explicitly as part of the message itself. This can be
done by introducing a higher-level layer, which is done in the
[streaming](#app.streaming) library. Alice may also cut down on the
response time by bundling her most recent LeaseSet with the message so
that Bob doesn\'t need to do a netDb lookup for it when he wants to
reply, but this is optional.

::: {.box style="text-align:center;"}
\
\
![Connect tunnels using
LeaseSets](images/netdb_get_leaseset.png "Connect tunnels using leaseSets")\
\
Figure 3: LeaseSets are used to connect outbound and inbound tunnels.
:::

\

While the tunnels themselves have layered encryption to prevent
unauthorized disclosure to peers inside the network (as the transport
layer itself does to prevent unauthorized disclosure to peers outside
the network), it is necessary to add an additional end to end layer of
encryption to hide the message from the outbound tunnel endpoint and the
inbound tunnel gateway. This \"[garlic encryption](#op.garlic)\" lets
Alice\'s router wrap up multiple messages into a single \"garlic
message\", encrypted to a particular public key so that intermediary
peers cannot determine either how many messages are within the garlic,
what those messages say, or where those individual cloves are destined.
For typical end to end communication between Alice and Bob, the garlic
will be encrypted to the public key published in Bob\'s leaseSet,
allowing the message to be encrypted without giving out the public key
to Bob\'s own router.

Another important fact to keep in mind is that I2P is entirely message
based and that some messages may be lost along the way. Applications
using I2P can use the message oriented interfaces and take care of their
own congestion control and reliability needs, but most would be best
served by reusing the provided [streaming](#app.streaming) library to
view I2P as a streams based network.

## トンネル {#op.tunnels}

Both inbound and outbound tunnels work along similar principles. The
tunnel gateway accumulates a number of tunnel messages, eventually
preprocessing them into something for tunnel delivery. Next, the gateway
encrypts that preprocessed data and forwards it to the first hop. That
peer and subsequent tunnel participants add on a layer of encryption
after verifying that it isn\'t a duplicate before forward it on to the
next peer. Eventually, the message arrives at the endpoint where the
messages are split out again and forwarded on as requested. The
difference arises in what the tunnel\'s creator does - for inbound
tunnels, the creator is the endpoint and they simply decrypt all of the
layers added, while for outbound tunnels, the creator is the gateway and
they pre-decrypt all of the layers so that after all of the layers of
per-hop encryption are added, the message arrives in the clear at the
tunnel endpoint.

The choice of specific peers to pass on messages as well as their
particular ordering is important to understanding both I2P\'s anonymity
and performance characteristics. While the network database (below) has
its own criteria for picking what peers to query and store entries on,
tunnel creators may use any peers in the network in any order (and even
any number of times) in a single tunnel. If perfect latency and capacity
data were globally known, selection and ordering would be driven by the
particular needs of the client in tandem with their threat model.
Unfortunately, latency and capacity data is not trivial to gather
anonymously, and depending upon untrusted peers to provide this
information has its own serious anonymity implications.

From an anonymity perspective, the simplest technique would be to pick
peers randomly from the entire network, order them randomly and use
those peers in that order for all eternity. From a performance
perspective, the simplest technique would be to pick the fastest peers
with the necessary spare capacity, spreading the load across different
peers to handle transparent failover, and to rebuild the tunnel whenever
capacity information changes. While the former is both brittle and
inefficient, the later requires inaccessible information and offers
insufficient anonymity. I2P is instead working on offering a range of
peer selection strategies, coupled with anonymity aware measurement code
to organize the peers by their profiles.

As a base, I2P is constantly profiling the peers with which it interacts
with by measuring their indirect behavior - for instance, when a peer
responds to a netDb lookup in 1.3 seconds, that round trip latency is
recorded in the profiles for all of the routers involved in the two
tunnels (inbound and outbound) through which the request and response
passed, as well as the queried peer\'s profile. Direct measurement, such
as transport layer latency or congestion, is not used as part of the
profile, as it can be manipulated and associated with the measuring
router, exposing them to trivial attacks. While gathering these
profiles, a series of calculations are run on each to summarize its
performance - its latency, capacity to handle lots of activity, whether
they are currently overloaded, and how well integrated into the network
they seem to be. These calculations are then compared for active peers
to organize the routers into four tiers - fast and high capacity, high
capacity, not failing, and failing. The thresholds for those tiers are
determined dynamically, and while they currently use fairly simple
algorithms, alternatives exist.

Using this profile data, the simplest reasonable peer selection strategy
is to pick peers randomly from the top tier (fast and high capacity),
and this is currently deployed for client tunnels. Exploratory tunnels
(used for netDb and tunnel management) pick peers randomly from the
\"not failing\" tier (which includes routers in \'better\' tiers as
well), allowing the peer to sample routers more widely, in effect
optimizing the peer selection through randomized [hill
climbing](https://en.wikipedia.org/wiki/Hill_climbing). These strategies
alone do however leak information regarding the peers in the router\'s
top tier through predecessor and netDb harvesting attacks. In turn,
several alternatives exist which, while not balancing the load as
evenly, will address the attacks mounted by particular classes of
adversaries.

By picking a random key and ordering the peers according to their XOR
distance from it, the information leaked is reduced in predecessor and
harvesting attacks according to the peers\' failure rate and the tier\'s
churn. Another simple strategy for dealing with netDb harvesting attacks
is to simply fix the inbound tunnel gateway(s) yet randomize the peers
further on in the tunnels. To deal with predecessor attacks for
adversaries which the client contacts, the outbound tunnel endpoints
would also remain fixed. The selection of which peer to fix on the most
exposed point would of course need to have a limit to the duration, as
all peers fail eventually, so it could either be reactively adjusted or
proactively avoided to mimic a measured mean time between failures of
other routers. These two strategies can in turn be combined, using a
fixed exposed peer and an XOR based ordering within the tunnels
themselves. A more rigid strategy would fix the exact peers and ordering
of a potential tunnel, only using individual peers if all of them agree
to participate in the same way each time. This varies from the XOR based
ordering in that the predecessor and successor of each peer is always
the same, while the XOR only makes sure their order doesn\'t change.

As mentioned before, I2P currently (release 0.8) includes the tiered
random strategy above, with XOR-based ordering. A more detailed
discussion of the mechanics involved in tunnel operation, management,
and peer selection can be found in the [tunnel
spec]().

## ネットワークデータベース検索ツール {#op.netdb}

As mentioned earlier, I2P\'s netDb works to share the network\'s
metadata. This is detailed in [the network
database]() page, but a basic explanation is
available below.

All I2P routers contain a local netDb, but not all routers participate
in the DHT or respond to leaseset lookups. Those routers that do
participate in the DHT and respond to leaseset lookups are called
\'floodfills\'. Routers may be manually configured as floodfills, or
automatically become floodfill if they have enough capacity and meet
other criteria for reliable operation.

Other I2P routers will store their data and lookup data by sending
simple \'store\' and \'lookup\' queries to the floodfills. If a
floodfill router receives a \'store\' query, it will spread the
information to other floodfill routers using the [Kademlia
algorithm](http://en.wikipedia.org/wiki/Kademlia). The \'lookup\'
queries currently function differently, to avoid an important [security
issue](#lookup). When a lookup is done, the
floodfill router will not forward the lookup to other peers, but will
always answer by itself (if it has the requested data).

Two types of information are stored in the network database.

- A **RouterInfo** stores information on a specific I2P router and how
 to contact it
- A **LeaseSet** stores information on a specific destination (e.g.
 I2P website, e-mail server\...)

All of this information is signed by the publishing party and verified
by any I2P router using or storing the information. In addition, the
data contains timing information, to avoid storage of old entries and
possible attacks. This is also why I2P bundles the necessary code for
maintaining the correct time, occasionally querying some SNTP servers
(the [pool.ntp.org](http://www.pool.ntp.org/) round robin by default)
and detecting skew between routers at the transport layer.

Some additional remarks are also important.

- **Unpublished and encrypted leasesets:**

 One could only want specific people to be able to reach a
 destination. This is possible by not publishing the destination in
 the netDb. You will however have to transmit the destination by
 other means. This is supported by \'encrypted leaseSets\'. These
 leaseSets can only be decoded by people with access to the
 decryption key.

- **Bootstrapping:**

 Bootstrapping the netDb is quite simple. Once a router manages to
 receive a single routerInfo of a reachable peer, it can query that
 router for references to other routers in the network. Currently, a
 number of users post their routerInfo files to a website to make
 this information available. I2P automatically connects to one of
 these websites to gather routerInfo files and bootstrap. I2P calls
 this bootstrap process \"reseeding\".

- **Lookup scalability:**

 Lookups in the I2P network are iterative, not recursive. If a lookup
 from a floodfill fails, the lookup will be repeated to the
 next-closest floodfill. The floodfill does not recursively ask
 another floodfill for the data. Iterative lookups are scalable to
 large DHT networks.

## Transport protocols {#op.transport}

Communication between routers needs to provide confidentiality and
integrity against external adversaries while authenticating that the
router contacted is the one who should receive a given message. The
particulars of how routers communicate with other routers aren\'t
critical - three separate protocols have been used at different points
to provide those bare necessities.

I2P currently supports two transport protocols,
[NTCP2]() over TCP, and
[SSU2]() over UDP. These have replaced the
previous versions of the protocols, [NTCP]() and
[SSU](), which are now deprecated. Both protocols
support both IPv4 and IPv6. By supporting both TCP and UDP transports,
I2P can effectively traverse most firewalls, including those intended to
block traffic in restrictive censorship regimes. NTCP2 and SSU2 were
designed to use modern encryption standards, improve traffic
identification resistance, increase efficiency and security, and make
NAT traversal more robust. Routers publish each supported transport and
IP address in the network database. Routers with access to public IPv4
and IPv6 networks will usually publish four addresses, one for each
combination of NTCP2/SSU2 with IPv4/IPv6.

[SSU2]() supports and extends the goals of SSU.
SSU2 has many similarities to other modern UDP-based protocols such as
Wireguard and QUIC. In addition to the reliable transport of network
messages over UDP, SSU2 provides specialized facilities for
peer-to-peer, cooperative IP address detection, firewall detection, and
NAT traversal. As described in the [SSU spec]():

> The goal of this protocol is to provide secure, authenticated,
> semireliable and unordered message delivery, exposing only a minimal
> amount of data easily discernible to third parties. It should support
> high degree communication as well as TCP-friendly congestion control
> and may include PMTU detection. It should be capable of efficiently
> moving bulk data at rates sufficient for home users. In addition, it
> should support techniques for addressing network obstacles, like most
> NATs or firewalls.

NTCP2 supports and extends the goals of NTCP. It provides an efficient
and fully encrypted transport of network messages over TCP, and
resistance to traffic identification, using modern encryption standards.

I2P supports multiple transports simultaneously. A particular transport
for an outbound connection is selected with \"bids\". Each transport
bids for the connection and the relative value of these bids assigns the
priority. Transports may reply with different bids, depending on whether
there is already an established connection to the peer.

The bid (priority) values are implementation-dependent and may vary
based on traffic conditions, connection counts, and other factors.
Routers also publish their transport preferences for inbound connections
in the network database as transport \"costs\" for each transport and
address.

## 暗号法 {#op.crypto}

I2P uses cryptography at several protocol layers for encryption,
authentication, and verification. The major protocol layers are:
transports, tunnel build messages, tunnel layer encryption, network
database messages, and end-to-end (garlic) messages. I2P\'s original
design used a small set of cryptographic primitives that at the time
were considered secure. These included ElGamal asymmetric encryption,
DSA-SHA1 signatures, AES256/CBC symmetric encryption, and SHA-256
hashes. As available computing power increased and cryptographic
research evolved substantially over the years, I2P needed to upgrade its
primitives and protocols. Therefore, we added a concept of \"encryption
types\" and \"signature types\", and extended our protocols to include
these identifiers and indicate support. This allows us to periodically
update and extend the network support for modern cryptography and
future-proof the network for new primitives, without breaking backward
compatibility or requiring a \"flag day\" for network updates. Some
signature and encryption types are also reserved for experimental use.

The current primitives used in most protocol layers are X25519 key
exchange, EdDSA signatures, ChaCha20/Poly1305 authenticated symmetric
encryption, and SHA-256 hashes. AES256 is still used for tunnel layer
encryption. These modern protocols are used for the vast majority of
network communication Older primitives including ElGamal, ECDSA, and
DSA-SHA1 continue to be supported by most implementations for backward
compatibility when communicating with older routers. Some old protocols
have been deprecated and/or removed completely. In the near future we
will begin research on a migration to post-quantum (PQ) or hybrid-PQ
encryption and signatures to maintain our robust security standards.

These cryptographic primitives are combined together to provide I2P\'s
layered defenses against a variety of adversaries. At the lowest level,
inter-router communication is protected by the transport layer security.
[Tunnel](#op.tunnels) messages passed over the transports have their own
layered encryption. Various other messages are passed along inside
\"garlic messages\", which are also encrypted.

### Garlic messages {#op.garlic}

Garlic messages are an extension of \"onion\" layered encryption,
allowing the contents of a single message to contain multiple
\"cloves\" - fully formed messages alongside their own instructions for
delivery. Messages are wrapped into a garlic message whenever the
message would otherwise be passing in cleartext through a peer who
should not have access to the information - for instance, when a router
wants to ask another router to participate in a tunnel, they wrap the
request inside a garlic, encrypt that garlic to the receiving router\'s
public key, and forward it through a tunnel. Another example is when a
client wants to send a message to a destination - the sender\'s router
will wrap up that data message (alongside some other messages) into a
garlic, encrypt that garlic to the public key published in the
recipient\'s leaseSet, and forward it through the appropriate tunnels.

The \"instructions\" attached to each clove inside the encryption layer
includes the ability to request that the clove be forwarded locally, to
a remote router, or to a remote tunnel on a remote router. There are
fields in those instructions allowing a peer to request that the
delivery be delayed until a certain time or condition has been met,
though they won\'t be honored until the [nontrivial
delays](#future.variablelatency) are deployed. It is possible to
explicitly route garlic messages any number of hops without building
tunnels, or even to reroute tunnel messages by wrapping them in garlic
messages and forwarding them a number of hops prior to delivering them
to the next hop in the tunnel, but those techniques are not currently
used in the existing implementation.

### Session tags {#op.sessiontags}

As an unreliable, unordered, message based system, I2P uses a simple
combination of asymmetric and symmetric encryption algorithms to provide
data confidentiality and integrity to garlic messages. The original
combination was referred to as ElGamal/AES+SessionTags, but that is an
excessively verbose way to describe the simple use of 2048bit ElGamal,
AES256, SHA256 and 32 byte nonces. While this protocol is still
supported, most of the network has migrated to a new protocol,
ECIES-X25519-AEAD-Ratchet. This protocol combines X25519,
ChaCha20/Poly1305, and a synchronized PRNG to generate the 32 byte
nonces. Both protocols will be briefly described below.

#### ElGamal/AES+SessionTags {#op.elg}

The first time a router wants to encrypt a garlic message to another
router, they encrypt the keying material for an AES256 session key with
ElGamal and append the AES256/CBC encrypted payload after that encrypted
ElGamal block. In addition to the encrypted payload, the AES encrypted
section contains the payload length, the SHA256 hash of the unencrypted
payload, as well as a number of \"session tags\" - random 32 byte
nonces. The next time the sender wants to encrypt a garlic message to
another router, rather than ElGamal encrypt a new session key they
simply pick one of the previously delivered session tags and AES encrypt
the payload like before, using the session key used with that session
tag, prepended with the session tag itself. When a router receives a
garlic encrypted message, they check the first 32 bytes to see if it
matches an available session tag - if it does, they simply AES decrypt
the message, but if it does not, they ElGamal decrypt the first block.

Each session tag can be used only once so as to prevent internal
adversaries from unnecessarily correlating different messages as being
between the same routers. The sender of an ElGamal/AES+SessionTag
encrypted message chooses when and how many tags to deliver, prestocking
the recipient with enough tags to cover a volley of messages. Garlic
messages may detect the successful tag delivery by bundling a small
additional message as a clove (a \"delivery status message\") - when the
garlic message arrives at the intended recipient and is decrypted
successfully, this small delivery status message is one of the cloves
exposed and has instructions for the recipient to send the clove back to
the original sender (through an inbound tunnel, of course). When the
original sender receives this delivery status message, they know that
the session tags bundled in the garlic message were successfully
delivered.

Session tags themselves have a very short lifetime, after which they are
discarded if not used. In addition, the quantity stored for each key is
limited, as are the number of keys themselves - if too many arrive,
either new or old messages may be dropped. The sender keeps track
whether messages using session tags are getting through, and if there
isn\'t sufficient communication it may drop the ones previously assumed
to be properly delivered, reverting back to the full expensive ElGamal
encryption.

#### ECIES-X25519-AEAD-Ratchet {#op.ratchet}

ElGamal/AES+SessionTags required substantial overhead in a number of
ways. CPU usage was high because ElGamal is quite slow. Bandwidth was
excessive because large numbers of session tags had to be delivered in
advance, and because ElGamal public keys are very large. Memory usage
was high due to the requirement to store large amounts of session tags.
Reliability was hampered by lost session tag delivery.

ECIES-X25519-AEAD-Ratchet was designed to address these issues. X25519
is used for key exchange. ChaCha20/Poly1305 is used for authenticated
symmetric encryption. Encryption keys are \"double ratcheted\" or
rotated periodically. Session tags are reduced from 32 bytes to 8 bytes
and are generated with a PRNG. The protocol has many similarities to the
signal protocol used in Signal and WhatsApp. This protocol provides
substantially lower overhead in CPU, RAM, and bandwidth.

The session tags are generated from a deterministic synchronized PRNG
running at both ends of the session to generate session tags and session
keys. The PRNG is a HKDF using a SHA-256 HMAC, and is seeded from the
X25519 DH result. Session tags are never transmitted in advance; they
are only included with the message. The receiver stores a limited number
of session keys, indexed by session tag. The sender does not need to
store any session tags or keys because they are not sent in advance;
they may be generated on-demand. By keeping this PRNG roughly
synchronized between the sender and recipient (the recipient precomputes
a window of the next e.g. 50 tags), the overhead of periodically
bundling a large number of tags is removed.

# Future

I2P\'s protocols are efficient on most platforms, including cell phones,
and secure for most threat models. However, there are several areas
which require further improvement to meet the needs of those facing
powerful state-sponsored adversaries, and to meet the threats of
continued cryptographic advances and ever-increasing computing power.
Two possible features, restricted routes and variable latency, were
propsed by jrandom in 2003. While we no longer plan to implement these
features, they are described below.

## Restricted route operation {#future.restricted}

I2P is an overlay network designed to be run on top of a functional
packet switched network, exploiting the end to end principle to offer
anonymity and security. While the Internet no longer fully embraces the
end to end principle (due to the usage of NAT), I2P does require a
substantial portion of the network to be reachable - there may be a
number of peers along the edges running using restricted routes, but I2P
does not include an appropriate routing algorithm for the degenerate
case where most peers are unreachable. It would, however work on top of
a network employing such an algorithm.

Restricted route operation, where there are limits to what peers are
reachable directly, has several different functional and anonymity
implications, dependent upon how the restricted routes are handled. At
the most basic level, restricted routes exist when a peer is behind a
NAT or firewall which does not allow inbound connections. This was
largely addressed by integrating distributed hole punching into the
transport layer, allowing people behind most NATs and firewalls to
receive unsolicited connections without any configuration. However, this
does not limit the exposure of the peer\'s IP address to routers inside
the network, as they can simply get introduced to the peer through the
published introducer.

Beyond the functional handling of restricted routes, there are two
levels of restricted operation that can be used to limit the exposure of
one\'s IP address - using router-specific tunnels for communication, and
offering \'client routers\'. For the former, routers can either build a
new pool of tunnels or reuse their exploratory pool, publishing the
inbound gateways to some of them as part of their routerInfo in place of
their transport addresses. When a peer wants to get in touch with them,
they see those tunnel gateways in the netDb and simply send the relevant
message to them through one of the published tunnels. If the peer behind
the restricted route wants to reply, it may do so either directly (if
they are willing to expose their IP to the peer) or indirectly through
their outbound tunnels. When the routers that the peer has direct
connections to want to reach it (to forward tunnel messages, for
instance), they simply prioritize their direct connection over the
published tunnel gateway. The concept of \'client routers\' simply
extends the restricted route by not publishing any router addresses.
Such a router would not even need to publish their routerInfo in the
netDb, merely providing their self signed routerInfo to the peers that
it contacts (necessary to pass the router\'s public keys).

There are tradeoffs for those behind restricted routes, as they would
likely participate in other people\'s tunnels less frequently, and the
routers which they are connected to would be able to infer traffic
patterns that would not otherwise be exposed. On the other hand, if the
cost of that exposure is less than the cost of an IP being made
available, it may be worthwhile. This, of course, assumes that the peers
that the router behind a restricted route contacts are not hostile -
either the network is large enough that the probability of using a
hostile peer to get connected is small enough, or trusted (and perhaps
temporary) peers are used instead.

Restricted routes are complex, and the overall goal has been largely
abandoned. Several related improvements have greatly reduced the need
for them. We now support UPnP to automatically open firewall ports. We
support both IPv4 and IPv6. SSU2 improved address detection, firewall
state determination, and cooperative NAT hole punching. SSU2, NTCP2, and
address compatibility checks ensure that tunnel hops can connect before
the tunnel is built. GeoIP and country identification allow us to avoid
peers in countries with restrictive firewalls. Support for \"hidden\"
routers behind those firewalls has improved. Some implementations also
support connections to peers on overlay networks such as Yggdrasil.

## Variable latency {#future.variablelatency}

Even though the bulk of I2P\'s initial efforts have been on low latency
communication, it was designed with variable latency services in mind
from the beginning. At the most basic level, applications running on top
of I2P can offer the anonymity of medium and high latency communication
while still blending their traffic patterns in with low latency traffic.
Internally though, I2P can offer its own medium and high latency
communication through the garlic encryption - specifying that the
message should be sent after a certain delay, at a certain time, after a
certain number of messages have passed, or another mix strategy. With
the layered encryption, only the router that the clove exposed the delay
request would know that the message requires high latency, allowing the
traffic to blend in further with the low latency traffic. Once the
transmission precondition is met, the router holding on to the clove
(which itself would likely be a garlic message) simply forwards it as
requested - to a router, to a tunnel, or, most likely, to a remote
client destination.

The goal of variable latency services requires substantial resources for
store-and-forward mechanisms to support it. These mechanisms can and are
supported in various messaging applications, such as i2p-bote. At the
network level, alternative networks such as Freenet provide these
services. We have decided not to pursue this goal at the I2P router
level.

# Similar systems {#similar}

I2P\'s architecture builds on the concepts of message oriented
middleware, the topology of DHTs, the anonymity and cryptography of free
route mixnets, and the adaptability of packet switched networking. The
value comes not from novel concepts of algorithms though, but from
careful engineering combining the research results of existing systems
and papers. While there are a few similar efforts worth reviewing, both
for technical and functional comparisons, two in particular are pulled
out here - Tor and Freenet.

See also the [Network Comparisons Page]().
Note that these descriptions were written by jrandom in 2003 and may not
currently be accurate.

## Tor {#similar.tor}

*[website](https://www.torproject.org/)*

At first glance, Tor and I2P have many functional and anonymity related
similarities. While I2P\'s development began before we were aware of the
early stage efforts on Tor, many of the lessons of the original onion
routing and ZKS efforts were integrated into I2P\'s design. Rather than
building an essentially trusted, centralized system with directory
servers, I2P has a self organizing network database with each peer
taking on the responsibility of profiling other routers to determine how
best to exploit available resources. Another key difference is that
while both I2P and Tor use layered and ordered paths (tunnels and
circuits/streams), I2P is fundamentally a packet switched network, while
Tor is fundamentally a circuit switched one, allowing I2P to
transparently route around congestion or other network failures, operate
redundant pathways, and load balance the data across available
resources. While Tor offers the useful outproxy functionality by
offering integrated outproxy discovery and selection, I2P leaves such
application layer decisions up to applications running on top of I2P -
in fact, I2P has even externalized the TCP-like streaming library itself
to the application layer, allowing developers to experiment with
different strategies, exploiting their domain specific knowledge to
offer better performance.

From an anonymity perspective, there is much similarity when the core
networks are compared. However, there are a few key differences. When
dealing with an internal adversary or most external adversaries, I2P\'s
simplex tunnels expose half as much traffic data than would be exposed
with Tor\'s duplex circuits by simply looking at the flows themselves -
an HTTP request and response would follow the same path in Tor, while in
I2P the packets making up the request would go out through one or more
outbound tunnels and the packets making up the response would come back
through one or more different inbound tunnels. While I2P\'s peer
selection and ordering strategies should sufficiently address
predecessor attacks, should a switch to bidirectional tunnels be
necessary, we could simply build an inbound and outbound tunnel along
the same routers.

Another anonymity issue comes up in Tor\'s use of telescopic tunnel
creation, as simple packet counting and timing measurements as the cells
in a circuit pass through an adversary\'s node exposes statistical
information regarding where the adversary is within the circuit. I2P\'s
unidirectional tunnel creation with a single message so that this data
is not exposed. Protecting the position in a tunnel is important, as an
adversary would otherwise be able to mount a series of powerful
predecessor, intersection, and traffic confirmation attacks.

On the whole, Tor and I2P complement each other in their focus - Tor
works towards offering high speed anonymous Internet outproxying, while
I2P works towards offering a decentralized resilient network in itself.
In theory, both can be used to achieve both purposes, but given limited
development resources, they both have their strengths and weaknesses.
The I2P developers have considered the steps necessary to modify Tor to
take advantage of I2P\'s design, but concerns of Tor\'s viability under
resource scarcity suggest that I2P\'s packet switching architecture will
be able to exploit scarce resources more effectively.

## Freenet {#similar.freenet}

*[website](http://www.freenetproject.org/)*

Freenet played a large part in the initial stages of I2P\'s design -
giving proof to the viability of a vibrant pseudonymous community
completely contained within the network, demonstrating that the dangers
inherent in outproxies could be avoided. The first seed of I2P began as
a replacement communication layer for Freenet, attempting to factor out
the complexities of a scalable, anonymous and secure point to point
communication from the complexities of a censorship resistant
distributed data store. Over time however, some of the anonymity and
scalability issues inherent in Freenet\'s algorithms made it clear that
I2P\'s focus should stay strictly on providing a generic anonymous
communication layer, rather than as a component of Freenet. Over the
years, the Freenet developers have come to see the weaknesses in the
older design, prompting them to suggest that they will require a
\"premix\" layer to offer substantial anonymity. In other words, Freenet
needs to run on top of a mixnet such as I2P or Tor, with \"client
nodes\" requesting and publishing data through the mixnet to the
\"server nodes\" which then fetch and store the data according to
Freenet\'s heuristic distributed data storage algorithms.

Freenet\'s functionality is very complementary to I2P\'s, as Freenet
natively provides many of the tools for operating medium and high
latency systems, while I2P natively provides the low latency mix network
suitable for offering adequate anonymity. The logic of separating the
mixnet from the censorship- resistant distributed data store still seems
self-evident from an engineering, anonymity, security, and resource
allocation perspective, so hopefully the Freenet team will pursue
efforts in that direction, if not simply reusing (or helping to improve,
as necessary) existing mixnets like I2P or Tor.

# Appendix A: Application layer {#app}

I2P itself doesn\'t really do much - it simply sends messages to remote
destinations and receives messages targeting local destinations - most
of the interesting work goes on at the layers above it. By itself, I2P
could be seen as an anonymous and secure IP layer, and the bundled
[streaming library](#app.streaming) as an implementation of an anonymous
and secure TCP layer on top of it. Beyond that,
[I2PTunnel](#app.i2ptunnel) exposes a generic TCP proxying system for
either getting into or out of the I2P network, plus a variety of network
applications provide further functionality for end users.

## ストリーミングライブラリ {#app.streaming}

The I2P streaming library can be viewed as a generic streaming interface
(mirroring TCP sockets), and the implementation supports a [sliding
window protocol](http://en.wikipedia.org/wiki/Sliding_Window_Protocol)
with several optimizations, to take into account the high delay over
I2P. Individual streams may adjust the maximum packet size and other
options, though the default of 4KB compressed seems a reasonable
tradeoff between the bandwidth costs of retransmitting lost messages and
the latency of multiple messages.

In addition, in consideration of the relatively high cost of subsequent
messages, the streaming library\'s protocol for scheduling and
delivering messages has been optimized to allow individual messages
passed to contain as much information as is available. For instance, a
small HTTP transaction proxied through the streaming library can be
completed in a single round trip - the first message bundles a SYN, FIN
and the small payload (an HTTP request typically fits) and the reply
bundles the SYN, FIN, ACK and the small payload (many HTTP responses
fit). While an additional ACK must be transmitted to tell the HTTP
server that the SYN/FIN/ACK has been received, the local HTTP proxy can
deliver the full response to the browser immediately.

On the whole, however, the streaming library bears much resemblance to
an abstraction of TCP, with its sliding windows, congestion control
algorithms (both slow start and congestion avoidance), and general
packet behavior (ACK, SYN, FIN, RST, etc).

## Naming library and address book {#app.naming}

*For more information see the [Naming and Address
Book]() page.*

*Developed by: *

Naming within I2P has been an oft-debated topic since the very beginning
with advocates across the spectrum of possibilities. However, given
I2P\'s inherent demand for secure communication and decentralized
operation, the traditional DNS-style naming system is clearly out, as
are \"majority rules\" voting systems. Instead, I2P ships with a generic
naming library and a base implementation designed to work off a local
name to destination mapping, as well as an optional add-on application
called the \"Address Book\". The address book is a web-of-trust-driven
secure, distributed, and human readable naming system, sacrificing only
the call for all human readable names to be globally unique by mandating
only local uniqueness. While all messages in I2P are cryptographically
addressed by their destination, different people can have local address
book entries for \"Alice\" which refer to different destinations. People
can still discover new names by importing published address books of
peers specified in their web of trust, by adding in the entries provided
through a third party, or (if some people organize a series of published
address books using a first come first serve registration system) people
can choose to treat these address books as name servers, emulating
traditional DNS.

I2P does not promote the use of DNS-like services though, as the damage
done by hijacking a site can be tremendous - and insecure destinations
have no value. DNSsec itself still falls back on registrars and
certificate authorities, while with I2P, requests sent to a destination
cannot be intercepted or the reply spoofed, as they are encrypted to the
destination\'s public keys, and a destination itself is just a pair of
public keys and a certificate. DNS-style systems on the other hand allow
any of the name servers on the lookup path to mount simple denial of
service and spoofing attacks. Adding on a certificate authenticating the
responses as signed by some centralized certificate authority would
address many of the hostile nameserver issues but would leave open
replay attacks as well as hostile certificate authority attacks.

Voting style naming is dangerous as well, especially given the
effectiveness of Sybil attacks in anonymous systems - the attacker can
simply create an arbitrarily high number of peers and \"vote\" with each
to take over a given name. Proof-of-work methods can be used to make
identity non-free, but as the network grows the load required to contact
everyone to conduct online voting is implausible, or if the full network
is not queried, different sets of answers may be reachable.

As with the Internet however, I2P is keeping the design and operation of
a naming system out of the (IP-like) communication layer. The bundled
naming library includes a simple service provider interface which
alternate naming systems can plug into, allowing end users to drive what
sort of naming tradeoffs they prefer.

## I2PTunnel {#app.i2ptunnel}

*Developed by: *

I2PTunnel is probably I2P\'s most popular and versatile client
application, allowing generic proxying both into and out of the I2P
network. I2PTunnel can be viewed as four separate proxying
applications - a \"client\" which receives inbound TCP connections and
forwards them to a given I2P destination, an \"httpclient\" (aka
\"eepproxy\") which acts like an HTTP proxy and forwards the requests to
the appropriate I2P destination (after querying the naming service if
necessary), a \"server\" which receives inbound I2P streaming
connections on a destination and forwards them to a given TCP host+port,
and an \"httpserver\" which extends the \"server\" by parsing the HTTP
request and responses to allow safer operation. There is an additional
\"socksclient\" application, but its use is not encouraged for reasons
previously mentioned.

I2P itself is not an outproxy network - the anonymity and security
concerns inherent in a mix net which forwards data into and out of the
mix have kept I2P\'s design focused on providing an anonymous network
which capable of meeting the user\'s needs without requiring external
resources. However, the I2PTunnel \"httpclient\" application offers a
hook for outproxying - if the hostname requested doesn\'t end in
\".i2p\", it picks a random destination from a user-provided set of
outproxies and forwards the request to them. These destinations are
simply I2PTunnel \"server\" instances run by volunteers who have
explicitly chosen to run outproxies - no one is an outproxy by default,
and running an outproxy doesn\'t automatically tell other people to
proxy through you. While outproxies do have inherent weaknesses, they
offer a simple proof of concept for using I2P and provide some
functionality under a threat model which may be sufficient for some
users.

I2PTunnel enables most of the applications in use. An \"httpserver\"
pointing at a webserver lets anyone run their own anonymous website (or
\"I2P Site\") - a webserver is bundled with I2P for this purpose, but
any webserver can be used. Anyone may run a \"client\" pointing at one
of the anonymously hosted IRC servers, each of which are running a
\"server\" pointing at their local IRCd and communicating between IRCds
over their own \"client\" tunnels. End users also have \"client\"
tunnels pointing at [I2Pmail\'s](#app.i2pmail) POP3 and SMTP
destinations (which in turn are simply \"server\" instances pointing at
POP3 and SMTP servers), as well as \"client\" tunnels pointing at I2P\'s
CVS server, allowing anonymous development. At times people have even
run \"client\" proxies to access the \"server\" instances pointing at an
NNTP server.

## I2PSnark {#app.i2psnark}

*I2PSnark developed: jrandom, et al, ported from
[mjw](http://www.klomp.org/mark/)\'s
[Snark](http://www.klomp.org/snark/) client*

Bundled with the I2P install, I2PSnark offers a simple anonymous
BitTorrent client with multitorrent capabilities, exposing all of the
functionality through a plain HTML web interface.

## I2Pmail/susimail {#app.i2pmail}

*Developed by: *

I2Pmail is more a service than an application - postman offers both
internal and external email with POP3 and SMTP service through I2PTunnel
instances accessing a series of components developed with mastiejaner,
allowing people to use their preferred mail clients to send and receive
mail pseudonymously. However, as most mail clients expose substantial
identifying information, I2P bundles susi23\'s web based susimail client
which has been built specifically with I2P\'s anonymity needs in mind.
The I2Pmail/mail.i2p service offers transparent virus filtering as well
as denial of service prevention with hashcash augmented quotas. In
addition, each user has control of their batching strategy prior to
delivery through the mail.i2p outproxies, which are separate from the
mail.i2p SMTP and POP3 servers - both the outproxies and inproxies
communicate with the mail.i2p SMTP and POP3 servers through I2P itself,
so compromising those non-anonymous locations does not give access to
the mail accounts or activity patterns of the user.


