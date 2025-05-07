 Datagrammen 2025-04 0.9.66 

## Datagram Overview

Datagrams build upon the base [I2CP]() to provide
authenticated and repliable messages in a standard format. This lets
applications reliably read the \"from\" address out of a datagram and
know that the address really sent the message. This is necessary for
some applications since the base I2P message is completely raw - it has
no \"from\" address (unlike IP packets). In addition, the message and
sender are authenticated by signing the payload.

Datagrams, like [streaming library
packets](), are an application-level
construct. These protocols are independent of the low-level
[transports](); the protocols are converted
to I2NP messages by the router, and either protocol may be carried by
either transport.

## Application Guide

Applications written in Java may use the [datagram
API](), while applications in other languages can
use [SAM]()\'s datagram support. There is also
limited support in i2ptunnel in the [SOCKS
proxy](), the \'streamr\' tunnel types, and
udpTunnel classes.

### Datagram Length

The application designer should carefully consider the tradeoff of
repliable vs. non-repliable datagrams. Also, the datagram size will
affect reliability, due to tunnel fragmentation into 1KB tunnel
messages. The more message fragments, the more likely that one of them
will be dropped by an intermediate hop. Messages larger than a few KB
are not recommended. Over about 10 KB, the delivery probablility drops
dramatically.

[See the Datagrams Specification
page.]()

Also note that the various overheads added by lower layers, in
particular garlic messages, place a large burden on intermittent
messages such as used by a Kademlia-over-UDP application. The
implementations are currently tuned for frequent traffic using the
streaming library.

### I2CP Protocol Number and Ports

The standard I2CP protocol number for signed (repliable) datagrams is
PROTO_DATAGRAM (17). Applications may or may not choose to set the
protocol in the I2CP header. The default is implementation-dependent. It
must be set to demultiplex datagram and streaming traffic received on
the same Destination.

As datagrams are not connection-oriented, the application may require
port numbers to correlate datagrams with particular peers or
communications sessions, as is traditional with UDP over IP.
Applications may add \'from\' and \'to\' ports to the I2CP (gzip) header
as described in the [I2CP page](#format).

There is no method within the datagram API to specify whether it is
non-repliable (raw) or repliable. The application should be designed to
expect the appropriate type. The I2CP protocol number or port should be
used by the application to indicate datagram type. The I2CP protocol
numbers PROTO_DATAGRAM (signed, also known as Datagram1),
PROTO_DATAGRAM_RAW, PROTO_DATAGRAM2, and PROTO_DATAGRAM3 are defined in
the [I2PSession API]() for this purpose. A
common design pattern in client/server datagram applications is to use
signed datagrams for a request which includes a nonce, and use a raw
datagram for the reply, returning the nonce from the request.

Defaults:

- PROTO_DATAGRAM = 17
- PROTO_DATAGRAM_RAW = 18
- PROTO_DATAGRAM2 = 19
- PROTO_DATAGRAM3 = 20

The protocols and ports may be set in I2CP\'s [I2PSession
API](), as implemented in
[I2PSessionMuxedImpl]().

### Data Integrity

Data integrity is assured by the gzip CRC-32 checksum implemented in
[the I2CP layer](#format). Authenticated datagrams
(Datagram1 and Datagram2) also ensure integrity. There is no checksum
field in the datagram protocol.

### Packet Encapsulation

Each datagram is sent through I2P as a single message (or as an
individual clove in a [Garlic
Message]()). Message encapsulation is
implemented in the underlying [I2CP](),
[I2NP](), and [tunnel
message]() layers. There is no packet
delimiter mechanism or length field in the datagram protocol.

## Specification {#spec}

[See the Datagrams Specification
page.]()


