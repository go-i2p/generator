 I2P Network
Protocol (I2NP) Oktober 2018 0.9.37 

The I2P Network Protocol (I2NP), which is sandwiched between I2CP and
the various I2P transport protocols, manages the routing and mixing of
messages between routers, as well as the selection of what transports to
use when communicating with a peer for which there are multiple common
transports supported.

### I2NP Definition

I2NP (I2P Network Protocol) messages can be used for one-hop,
router-to-router, point-to-point messages. By encrypting and wrapping
messages in other messages, they can be sent in a secure way through
multiple hops to the ultimate destination. Priority is only used locally
at the origin, i.e. when queuing for outbound delivery.

The priorities listed below may not be current and are subject to
change. See the [OutNetMessage
Javadocs]() for the current priority
settings. Priority queueing implementation may vary.

### Message Format

The following table specifies the traditional 16-byte header used in
NTCP. The SSU and NTCP2 transports use modified headers.

 Field Byte
 ---------------- ------------
 Type 1
 Unik ID 4
 Utløp 8
 Payload Length 2
 Sjekksum 1
 Payload 0 - 61.2KB

While the maximum payload size is nominally 64KB, the size is further
constrained by the method of fragmenting I2NP messages into multiple 1KB
tunnel messages as described on [the tunnel implementation
page](). The maximum number of fragments is
64, and the message may not be perfectly aligned, So the message must
nominally fit in 63 fragments.

The maximum size of an initial fragment is 956 bytes (assuming TUNNEL
delivery mode); the maximum size of a follow-on fragment is 996 bytes.
Therefore the maximum size is approximately 956 + (62 \* 996) = 62708
bytes, or 61.2 KB.

In addition, the transports may have additional restrictions. The NTCP
limit is 16KB - 6 = 16378 bytes. The SSU limit is approximately 32 KB.
The NTCP2 limit is approximately 64KB - 20 = 65516 bytes, which is
higher than what a tunnel can support.

Note that these are not the limits for datagrams that the client sees,
as the router may bundle a reply leaseset and/or session tags together
with the client message in a garlic message. The leaseset and tags
together may add about 5.5KB. Therefore the current datagram limit is
about 10KB. This limit will be increased in a future release.

### Message Types

Higher-numbered priority is higher priority. The majority of traffic is
TunnelDataMessages (priority 400), so anything above 400 is essentially
high priority, and anything below is low priority. Note also that many
of the messages are generally routed through exploratory tunnels, not
client tunnels, and therefore may not be in the same queue unless the
first hops happen to be on the same peer.

Also, not all message types are sent unencrypted. For example, when
testing a tunnel, the router wraps a DeliveryStatusMessage, which is
wrapped in a GarlicMessage, which is wrapped in a DataMessage.

Melding

Type

Payload Length

Prioritet

Kommentarer

DatabaseLookupMessage

2

 

500

Kan variere

DatabaseSearchReplyMessage

3

Typ. 161

300

Size is 65 + 32\*(number of hashes) where typically, the hashes for
three floodfill routers are returned.

DatabaseStoreMessage

1

Varierer

460

Priority may vary. Size is 898 bytes for a typical 2-lease leaseSet.
RouterInfo structures are compressed, and size varies; however there is
a continuing effort to reduce the amount of data published in a
RouterInfo as we approach release 1.0.

DataMessage

20

4 - 62080

425

Priority may vary on a per-destination basis

DeliveryStatusMessage

10

12

 

Used for message replies, and for testing tunnels - generally wrapped in
a GarlicMessage

[GarlicMessage](#op.garlic)

11

 

 

Generally wrapped in a DataMessage - but when unwrapped, given a
priority of 100 by the forwarding router

[TunnelBuildMessage](#tunnelCreate.requestRecord)

21

4224

500

[TunnelBuildReplyMessage](#tunnelCreate.replyRecord)

22

4224

300

TunnelDataMessage

18

1028

400

The most common message. Priority for tunnel participants, outbound
endpoints, and inbound gateways was reduced to 200 as of release
0.6.1.33. Outbound gateway messages (i.e. those originated locally)
remains at 400.

TunnelGatewayMessage

19

 

300/400

VariableTunnelBuildMessage

23

1057 - 4225

500

Shorter TunnelBuildMessage as of 0.7.12

VariableTunnelBuildReplyMessage

24

1057 - 4225

300

Shorter TunnelBuildReplyMessage as of 0.7.12

Others listed in [2003 Spec]()

0,4-9,12

 

 

Obsolete, Unused

### Full Protocol Specification

[On the I2NP Specification page](). See also
the [Common Data Structure Specification
page]().

### Future Work

It isn\'t clear whether the current priority scheme is generally
effective, and whether the priorities for various messages should be
adjusted further. This is a topic for further research, analysis and
testing.


