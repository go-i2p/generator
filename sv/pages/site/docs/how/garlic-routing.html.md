 Garlic Routing March 2014 0.9.12 

## Garlic Routing and \"Garlic\" Terminology

The terms \"garlic routing\" and \"garlic encryption\" are often used
rather loosely when referring to I2P\'s technology. Here, we explain the
history of the terms, the various meanings, and the usage of \"garlic\"
methods in I2P.

\"Garlic routing\" was first coined by [Michael J.
Freedman](http://www.cs.princeton.edu/~mfreed/) in Roger Dingledine\'s
Free Haven [Master\'s thesis](http://www.freehaven.net/papers.html)
Section 8.1.1 (June 2000), as derived from [Onion
Routing](http://www.onion-router.net/).

\"Garlic\" may have been used originally by I2P developers because I2P
implements a form of bundling as Freedman describes, or simply to
emphasize general differences from Tor. The specific reasoning may be
lost to history. Generally, when referring to I2P, the term \"garlic\"
may mean one of three things:

1. Layered Encryption
2. Bundling multiple messages together
3. ElGamal/AES Encryption

Unfortunately, I2P\'s usage of \"garlic\" terminology over the past
seven years has not always been precise; therefore the reader is
cautioned when encountering the term. Hopefully, the explanation below
will make things clear.

### Layered Encryption

Onion routing is a technique for building paths, or tunnels, through a
series of peers, and then using that tunnel. Messages are repeatedly
encrypted by the originator, and then decrypted by each hop. During the
building phase, only the routing instructions for the next hop are
exposed to each peer. During the operating phase, messages are passed
through the tunnel, and the message and its routing instructions are
only exposed to the endpoint of the tunnel.

This is similar to the way Mixmaster (see [network
comparisons]()) sends messages - taking a
message, encrypting it to the recipient\'s public key, taking that
encrypted message and encrypting it (along with instructions specifying
the next hop), and then taking that resulting encrypted message and so
on, until it has one layer of encryption per hop along the path.

In this sense, \"garlic routing\" as a general concept is identical to
\"onion routing\". As implemented in I2P, of course, there are several
differences from the implementation in Tor; see below. Even so, there
are substantial similarities such that I2P benefits from a [large amount
of academic research on onion
routing](http://www.onion-router.net/Publications.html), [Tor, and
similar mixnets](http://freehaven.net/anonbib/topic.html).

### Bundling Multiple Messages

Michael Freedman defined \"garlic routing\" as an extension to onion
routing, in which multiple messages are bundled together. He called each
message a \"bulb\". All the messages, each with its own delivery
instructions, are exposed at the endpoint. This allows the efficient
bundling of an onion routing \"reply block\" with the original message.

This concept is implemented in I2P, as described below. Our term for
garlic \"bulbs\" is \"cloves\". Any number of messages can be contained,
instead of just a single message. This is a significant distinction from
the onion routing implemented in Tor. However, it is only one of many
major architectural differences between I2P and Tor; perhaps it is not,
by itself, enough to justify a change in terminology.

Another difference from the method described by Freedman is that the
path is unidirectional - there is no \"turning point\" as seen in onion
routing or mixmaster reply blocks, which greatly simplifies the
algorithm and allows for more flexible and reliable delivery.

### ElGamal/AES Encryption

In some cases, \"garlic encryption\" may simply mean
[ElGamal/AES+SessionTag]() encryption
(without multiple layers).

## \"Garlic\" Methods in I2P

Now that we\'ve defined various \"garlic\" terms, we can say that I2P
uses garlic routing, bundling and encryption in three places:

1. For building and routing through tunnels (layered encryption)
2. For determining the success or failure of end to end message
 delivery (bundling)
3. For publishing some network database entries (dampening the
 probability of a successful traffic analysis attack) (ElGamal/AES)

There are also significant ways that this technique can be used to
improve the performance of the network, exploiting transport
latency/throughput tradeoffs, and branching data through redundant paths
to increase reliability.

### Tunnel Building and Routing

In I2P, tunnels are unidirectional. Each party builds two tunnels, one
for outbound and one for inbound traffic. Therefore, four tunnels are
required for a single round-trip message and reply.

Tunnels are built, and then used, with layered encryption. This is
described on the [tunnel implementation
page](). Tunnel building details are defined
on [this page](). We use
[ElGamal/AES+SessionTag]() for the
encryption.

Tunnels are a general-purpose mechanism to transport all [I2NP
messages](), and [Garlic
Messages](#msg_Garlic) are not used to build
tunnels. We do not bundle multiple [I2NP
messages]() into a single [Garlic
Message](#msg_Garlic) for unwrapping at the
outbound tunnel endpoint; the tunnel encryption is sufficient.

### End-to-End Message Bundling

At the layer above tunnels, I2P delivers end-to-end messages between
[Destinations](#struct_Destination).
Just as within a single tunnel, we use
[ElGamal/AES+SessionTag]() for the
encryption. Each client message as delivered to the router through the
[I2CP interface]() becomes a single [Garlic
Clove](#struct_GarlicClove) with its own
[Delivery
Instructions](#struct_GarlicCloveDeliveryInstructions),
inside a [Garlic Message](#msg_Garlic).
Delivery Instructions may specify a Destination, Router, or Tunnel.

Generally, a Garlic Message will contain only one clove. However, the
router will periodically bundle two additional cloves in the Garlic
Message:

![Garlic Message
Cloves](/_static/images/garliccloves.png "Garlic Message Cloves"){style="text-align:center;"}

1. A [Delivery Status
 Message](#msg_DeliveryStatus), with
 [Delivery
 Instructions](#struct_GarlicCloveDeliveryInstructions)
 specifying that it be sent back to the originating router as an
 acknowledgment. This is similar to the \"reply block\" or \"reply
 onion\" described in the references. It is used for determining the
 success or failure of end to end message delivery. The originating
 router may, upon failure to receive the Delivery Status Message
 within the expected time period, modify the routing to the far-end
 Destination, or take other actions.
2. A [Database Store
 Message](#msg_DatabaseStore), containing a
 [LeaseSet](#struct_LeaseSet) for
 the originating Destination, with [Delivery
 Instructions](#struct_GarlicCloveDeliveryInstructions)
 specifying the far-end destination\'s router. By periodically
 bundling a LeaseSet, the router ensures that the far-end will be
 able to maintain communications. Otherwise the far-end would have to
 query a floodfill router for the network database entry, and all
 LeaseSets would have to be published to the network database, as
 explained on the [network database page]().

By default, the Delivery Status and Database Store Messages are bundled
when the local LeaseSet changes, when additional [Session
Tags](#type_SessionTag) are delivered,
or if the messages have not been bundled in the previous minute. As of
release 0.9.2, the client may configure the default number of Session
Tags to send and the low tag threshold for the current session. See the
[I2CP options specification](#options) for
details. The session settings may also be overridden on a per-message
basis. See the [I2CP Send Message Expires
specification](#msg_SendMessageExpires) for
details.

Obviously, the additional messages are currently bundled for specific
purposes, and not part of a general-purpose routing scheme.

As of release 0.9.12, the Delivery Status Message is wrapped in another
Garlic Message by the originator so that the contents are encrypted and
not visible to routers on the return path.

### Storage to the Floodfill Network Database

As explained on the [network database
page](#delivery), local
[LeaseSets](#struct_LeaseSet) are sent
to floodfill routers in a [Database Store
Message](#msg_DatabaseStore) wrapped in a
[Garlic Message](#msg_Garlic) so it is not
visible to the tunnel\'s outbound gateway.

## Future Work

The Garlic Message mechanism is very flexible and provides a structure
for implementing many types of mixnet delivery methods. Together with
the unused delay option in the [tunnel message Delivery
Instructions](#struct_TunnelMessageDeliveryInstructions),
a wide spectrum of batching, delay, mixing, and routing strategies are
possible.

In particular, there is potential for much more flexibility at the
outbound tunnel endpoint. Messages could possibly be routed from there
to one of several tunnels (thus minimizing point-to-point connections),
or multicast to several tunnels for redundancy, or streaming audio and
video.

Such experiments may conflict with the need to ensure security and
anonymity, such as limiting certain routing paths, restricting the types
of I2NP messages that may be forwarded along various paths, and
enforcing certain message expiration times.

As a part of [ElGamal/AES encryption](), a
garlic message contains a sender specified amount of padding data,
allowing the sender to take active countermeasures against traffic
analysis. This is not currently used, beyond the requirement to pad to a
multiple of 16 bytes.

Encryption of additional messages to and from the [floodfill
routers](#delivery).

## Referenser

- The term garlic routing was first coined in Roger Dingledine\'s Free
 Haven [Master\'s thesis](http://www.freehaven.net/papers.html) (June
 2000), see Section 8.1.1 authored by [Michael J.
 Freedman](http://www.cs.princeton.edu/~mfreed/).
- [Onion router
 publications](http://www.onion-router.net/Publications.html)
- [Onion Routing on
 Wikipedia](http://en.wikipedia.org/wiki/Onion_routing)
- [Garlic Routing on
 Wikipedia](http://en.wikipedia.org/wiki/Garlic_routing)
- [I2P Meeting 58]() (2003) discussing the
 implementation of garlic routing
- [Tor](https://www.torproject.org/)
- [Free Haven publications](http://freehaven.net/anonbib/topic.html)
- Onion routing was first described in [Hiding Routing
 Information](http://www.onion-router.net/Publications/IH-1996.pdf)
 by David M. Goldschlag, Michael G. Reed, and Paul F. Syverson in
 1996.


