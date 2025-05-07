 I2CP
2025-04 0.9.66 

The I2P Client Protocol (I2CP) exposes a strong separation of concerns
between the router and any client that wishes to communicate over the
network. It enables secure and asynchronous messaging by sending and
receiving messages over a single TCP socket. With I2CP, a client
application tells the router who they are (their \"destination\"), what
anonymity, reliability, and latency tradeoffs to make, and where to send
messages. In turn the router uses I2CP to tell the client when any
messages have arrived, and to request authorization for some tunnels to
be used.

The protocol itself is implemented in Java, to provide the [Client
SDK](). This SDK is exposed in the i2p.jar package,
which implements the client-side of I2CP. Clients should never need to
access the router.jar package, which contains the router itself and the
router-side of I2CP. There is also a [C library
implementation](). A non-Java client would also
have to implement the [streaming library]()
for TCP-style connections.

Applications can take advantage of the base I2CP plus the
[streaming]() and
[datagram]() libraries by using the [Simple
Anonymous Messaging]() or
[BOB]() protocols, which do not require clients to
deal with any sort of cryptography. Also, clients may access the network
by one of several proxies - HTTP, CONNECT, and SOCKS 4/4a/5.
Alternatively, Java clients may access those libraries in
ministreaming.jar and streaming.jar. So there are several options for
both Java and non-Java applications.

Client-side end-to-end encryption (encrypting the data over the I2CP
connection) was disabled in I2P release 0.6, leaving in place the
[ElGamal/AES end-to-end encryption]() which
is implemented in the router. The only cryptography that client
libraries must still implement is [DSA public/private key
signing](#DSA) for
[LeaseSets](#msg_CreateLeaseSet) and [Session
Configurations](#struct_SessionConfig), and
management of those keys.

In a standard I2P installation, port 7654 is used by external java
clients to communicate with the local router via I2CP. By default, the
router binds to address 127.0.0.1. To bind to 0.0.0.0, set the router
advanced configuration option `i2cp.tcp.bindAllInterfaces=true` and
restart. Clients in the same JVM as the router pass messages directly to
the router through an internal JVM interface.

Some router and client implementations may also support external
connections over SSL, as configured by the i2cp.SSL=true option. While
SSL is not the default, it is strongly recommended for any traffic that
may be exposed to the open Internet. The authorization user/password (if
any), the [Private
Key](#type_PrivateKey) and [Signing
Private Key](#type_SigningPrivateKey)
for the
[Destination](#struct_Destination) are
all transmitted in-the-clear unless SSL is enabled. Some router and
client implementations may also support external connections over domain
sockets.

## I2CP Protocol Specification

Now on the [I2CP Specification page]().

## I2CP Initialization

When a client connects to the router, it first sends a single protocol
version byte (0x2A). Then it sends a [GetDate
Message](#msg_GetDate) and waits for the [SetDate
Message](#msg_SetDate) response. Next, it sends a
[CreateSession Message](#msg_CreateSession)
containing the session configuration. It next awaits a [RequestLeaseSet
Message](#msg_RequestLeaseSet) from the router,
indicating that inbound tunnels have been built, and responds with a
CreateLeaseSetMessage containing the signed LeaseSet. The client may now
initiate or receive connections from other I2P destinations.

## I2CP Options {#options}

### Router-side Options

The following options are traditionally passed to the router via a
[SessionConfig](#struct_SessionConfig) contained
in a [CreateSession Message](#msg_CreateSession)
or a [ReconfigureSession
Message](#msg_ReconfigureSession).

Router-side Options

Option

As Of Release

Recommended Arguments

Allowable Range

Parazgjedhje

Përshkrim

clientMessageTimeout

 

 

8\*1000 - 120\*1000

60\*1000

The timeout (ms) for all sent messages. Unused. See the protocol
specification for per-message settings.

crypto.lowTagThreshold

0.9.2

 

1-128

30

Minimum number of ElGamal/AES Session Tags before we send more.
Recommended: approximately tagsToSend \* 2/3

crypto.ratchet.inboundTags

0.9.47

 

1-?

160

Inbound tag window for ECIES-X25519-AEAD-Ratchet. Local inbound tagset
size. See proposal 144.

crypto.ratchet.outboundTags

0.9.47

 

1-?

160

Outbound tag window for ECIES-X25519-AEAD-Ratchet. Advisory to send to
the far-end in the options block. See proposal 144.

crypto.tagsToSend

0.9.2

 

1-128

40

Number of ElGamal/AES Session Tags to send at a time. For clients with
relatively low bandwidth per-client-pair (IRC, some UDP apps), this may
be set lower.

explicitPeers

 

 

 

null

Comma-separated list of Base 64 Hashes of peers to build tunnels
through; for debugging only

i2cp.dontPublishLeaseSet

 

true, false

 

false

Should generally be set to true for clients and false for servers

i2cp.fastReceive

0.9.4

 

true, false

false

If true, the router just sends the MessagePayload instead of sending a
MessageStatus and awaiting a ReceiveMessageBegin.

i2cp.leaseSetAuthType

0.9.41

0

0-2

0

The type of authentication for encrypted LS2. 0 for no per-client
authentication (the default); 1 for DH per-client authentication; 2 for
PSK per-client authentication. See proposal 123.

i2cp.leaseSetEncType

0.9.38

4,0

0-65535,\...

0

The encryption type to be used, as of 0.9.38. Interpreted client-side,
but also passed to the router in the SessionConfig, to declare intent
and check support. As of 0.9.39, may be comma-separated values for
multiple types. See PublicKey in common strutures spec for values. See
proposals 123, 144, and 145.

i2cp.leaseSetOfflineExpiration

0.9.38

 

 

 

The expiration of the offline signature, 4 bytes, seconds since the
epoch. See proposal 123.

i2cp.leaseSetOfflineSignature

0.9.38

 

 

 

The base 64 of the offline signature. See proposal 123.

i2cp.leaseSetPrivKey

0.9.41

 

 

 

A base 64 X25519 private key for the router to use to decrypt the
encrypted LS2 locally, only if per-client authentication is enabled.
Optionally preceded by the key type and \':\'. Only \"ECIES_X25519:\" is
supported, which is the default. See proposal 123. Do not confuse with
i2cp.leaseSetPrivateKey which is for the leaseset encryption keys.

i2cp.leaseSetSecret

0.9.39

 

 

\"\"

Base 64 encoded UTF-8 secret used to blind the leaseset address. See
proposal 123.

i2cp.leaseSetTransientPublicKey

0.9.38

 

 

 

\[type:\]b64 The base 64 of the transient private key, prefixed by an
optional sig type number or name, default DSA_SHA1. See proposal 123.

i2cp.leaseSetType

0.9.38

1,3,5,7

1-255

1

The type of leaseset to be sent in the CreateLeaseSet2 Message.
Interpreted client-side, but also passed to the router in the
SessionConfig, to declare intent and check support. See proposal 123.

i2cp.messageReliability

 

 

BestEffort, None

BestEffort

Guaranteed is disabled; None implemented in 0.8.1; the streaming lib
default is None as of 0.8.1, the client side default is None as of 0.9.4

i2cp.password

0.8.2

string

 

 

For authorization, if required by the router. If the client is running
in the same JVM as a router, this option is not required. Warning -
username and password are sent in the clear to the router, unless using
SSL (i2cp.SSL=true). Authorization is only recommended when using SSL.

i2cp.username

0.8.2

string

 

 

inbound.allowZeroHop

 

true, false

 

true

If incoming zero hop tunnel is allowed

outbound.allowZeroHop

 

true, false

 

true

If outgoing zero hop tunnel is allowed

inbound.backupQuantity

 

Number of IP bytes to match to determine if two routers should not be in
the same tunnel. 0 to disable.

outbound.IPRestriction

 

Number of IP bytes to match to determine if two routers should not be in
the same tunnel. 0 to disable.

inbound.length

 

Random amount to add or subtract to the length of tunnels in. A positive
number x means add a random amount from 0 to x inclusive. A negative
number -x means add a random amount from -x to x inclusive. The router
will limit the total length of the tunnel to 0 to 7 inclusive. The
default variance was 1 prior to release 0.7.6.

outbound.lengthVariance

 

Random amount to add or subtract to the length of tunnels out. A
positive number x means add a random amount from 0 to x inclusive. A
negative number -x means add a random amount from -x to x inclusive. The
router will limit the total length of the tunnel to 0 to 7 inclusive.
The default variance was 1 prior to release 0.7.6.

inbound.nickname

 

string

 

 

Name of tunnel - generally used in routerconsole, which will use the
first few characters of the Base64 hash of the destination by default.

outbound.nickname

 

string

 

 

Name of tunnel - generally ignored unless inbound.nickname is unset.

outbound.priority

0.9.4

Priority adjustment for outbound messages. Higher is higher priority.

inbound.quantity

 

Number of tunnels in. Limit was increased from 6 to 16 in release 0.9;
however, numbers higher than 6 are incompatible with older releases.

outbound.quantity

 

Used for consistent peer ordering across restarts.

outbound.randomKey

0.9.17

Base 64 encoding of 32 random bytes

 

 

inbound.\*

 

 

 

 

Any other options prefixed with \"inbound.\" are stored in the \"unknown
options\" properties of the inbound tunnel pool\'s settings.

outbound.\*

 

 

 

 

Any other options prefixed with \"outbound.\" are stored in the
\"unknown options\" properties of the outbound tunnel pool\'s settings.

shouldBundleReplyInfo

0.9.2

true, false

 

true

Set to false to disable ever bundling a reply LeaseSet. For clients that
do not publish their LeaseSet, this option must be true for any reply to
be possible. \"true\" is also recommended for multihomed servers with
long connection times.

Setting to \"false\" may save significant outbound bandwidth, especially
if the client is configured with a large number of inbound tunnels
(Leases). If replies are still required, this may shift the bandwidth
burden to the far-end client and the floodfill. There are several cases
where \"false\" may be appropriate:

- Unidirectional communication, no reply required
- LeaseSet is published and higher reply latency is acceptable
- LeaseSet is published, client is a \"server\", all connections are
 inbound so the connecting far-end destination obviously has the
 leaseset already. Connections are either short, or it is acceptable
 for latency on a long-lived connection to temporarily increase while
 the other end re-fetches the LeaseSet after expiration. HTTP servers
 may fit these requirements.

Note: Large quantity, length, or variance settings may cause significant
performance or reliability problems.

Note: As of release 0.7.7, option names and values must use UTF-8
encoding. This is primarily useful for nicknames. Prior to that release,
options with multi-byte characters were corrupted. Since options are
encoded in a [Mapping](#type_Mapping),
all option names and values are limited to 255 bytes (not characters)
maximum.

### Client-side Options

The following options are interpreted on the client side, and will be
interpreted if passed to the I2PSession via the
I2PClient.createSession() call. The streaming lib should also pass these
options through to I2CP. Other implementations may have different
defaults.

Client-side Options

Option

As Of Release

Recommended Arguments

Allowable Range

Parazgjedhje

Përshkrim

i2cp.closeIdleTime

0.7.1

1800000

If true, the router just sends the MessagePayload instead of sending a
MessageStatus and awaiting a ReceiveMessageBegin.

i2cp.gzip

0.6.5

true, false

 

true

Gzip outbound data

i2cp.leaseSetAuthType

0.9.41

0

0-2

0

The type of authentication for encrypted LS2. 0 for no per-client
authentication (the default); 1 for DH per-client authentication; 2 for
PSK per-client authentication. See proposal 123.

i2cp.leaseSetBlindedType

0.9.39

 

0-65535

See prop. 123

The sig type of the blinded key for encrypted LS2. Default depends on
the destination sig type. See proposal 123.

i2cp.leaseSetClient.dh.nnn

0.9.41

b64name:b64pubkey

 

 

The base 64 of the client name (ignored, UI use only), followed by a
\':\', followed by the base 64 of the public key to use for DH
per-client auth. nnn starts with 0 See proposal 123.

i2cp.leaseSetClient.psk.nnn

0.9.41

b64name:b64privkey

 

 

The base 64 of the client name (ignored, UI use only), followed by a
\':\', followed by the base 64 of the private key to use for PSK
per-client auth. nnn starts with 0. See proposal 123.

i2cp.leaseSetEncType

0.9.38

0

0-65535,\...

0

The encryption type to be used, as of 0.9.38. Interpreted client-side,
but also passed to the router in the SessionConfig, to declare intent
and check support. As of 0.9.39, may be comma-separated values for
multiple types. See also i2cp.leaseSetPrivateKey. See PublicKey in
common strutures spec for values. See proposals 123, 144, and 145.

i2cp.leaseSetKey

0.7.1

 

 

 

For encrypted leasesets. Base 64 SessionKey (44 characters)

i2cp.leaseSetOption.nnn

0.9.66

srvKey=srvValue

 

 

A service record to be placed in the LeaseSet2 options. Example:
\"\_smtp.\_tcp=1 86400 0 0 25 \...b32.i2p\" nnn starts with 0. See
proposal 167.

i2cp.leaseSetPrivateKey

0.9.18

 

 

 

Base 64 private keys for encryption. Optionally preceded by the
encryption type name or number and \':\'. For LS1, only one key is
supported, and only \"0:\" or \"ELGAMAL_2048:\" is supported, which is
the default. As of 0.9.39, for LS2, multiple keys may be
comma-separated, and each key must be a different encryption type. I2CP
will generate the public key from the private key. Use for persistent
leaseset keys across restarts. See proposals 123, 144, and 145. See also
i2cp.leaseSetEncType. Do not confuse with i2cp.leaseSetPrivKey which is
for encrypted LS2.

i2cp.leaseSetSecret

0.9.39

 

 

\"\"

Base 64 encoded UTF-8 secret used to blind the leaseset address. See
proposal 123.

i2cp.leaseSetSigningPrivateKey

0.9.18

 

 

 

Base 64 private key for signatures. Optionally preceded by the key type
and \':\'. DSA_SHA1 is the default. Key type must match the signature
type in the destination. I2CP will generate the public key from the
private key. Use for persistent leaseset keys across restarts.

i2cp.leaseSetType

0.9.38

1,3,5,7

1-255

1

The type of leaseset to be sent in the CreateLeaseSet2 Message.
Interpreted client-side, but also passed to the router in the
SessionConfig, to declare intent and check support. See proposal 123.

i2cp.messageReliability

 

 

BestEffort, None

None

Guaranteed is disabled; None implemented in 0.8.1; None is the default
as of 0.9.4

i2cp.reduceIdleTime

0.7.1

1200000

Connect to the router using SSL. If the client is running in the same
JVM as a router, this option is ignored, and the client connects to that
router internally.

i2cp.tcp.host

 

 

 

127.0.0.1

Router hostname. If the client is running in the same JVM as a router,
this option is ignored, and the client connects to that router
internally.

i2cp.tcp.port

 

 

1-65535

7654

Router I2CP port. If the client is running in the same JVM as a router,
this option is ignored, and the client connects to that router
internally.

Note: All arguments, including numbers, are strings. True/false values
are case-insensitive strings. Anything other than case-insensitive
\"true\" is interpreted as false. All option names are case-sensitive.

## I2CP Payload Data Format and Multiplexing {#format}

The end-to-end messages handled by I2CP (i.e. the data sent by the
client in a [SendMessageMessage](#msg_SendMessage)
and received by the client in a
[MessagePayloadMessage](#msg_MessagePayload)) are
gzipped with a standard 10-byte gzip header beginning with 0x1F 0x8B
0x08 as specified by [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt). As
of release 0.7.1, I2P uses ignored portions of the gzip header to
include protocol, from-port, and to-port information, thus supporting
streaming and datagrams on the same destination, and allowing
query/response using datagrams to work reliably in the presence of
multiple channels.

The gzip function cannot be completely turned off, however setting
i2cp.gzip=false turns the gzip effort setting to 0, which may save a
little CPU. Implementations may select different gzip efforts on a
per-socket or per-message basis, depending on an assessment of the
compressibility of the contents. Due to the compressibility of
destination padding implemented in API 0.9.57 (proposal 161),
compression of the streaming SYN packets in each direction, and of
repliable datagrams, is recommended even if the payload is not
compressible. Implementations may wish to write a trivial gzip/gunzip
function for a gzip effort of 0, which will provide large efficiency
gains over a gzip library for this case.

Bytes

Përmbajtje

0-2

Gzip header 0x1F 0x8B 0x08

3

Gzip flags

4-5

I2P Source port (Gzip mtime)

6-7

I2P Destination port (Gzip mtime)

8

Gzip xflags (set to 2 to be indistinguishable from the Java
implementation)

9

I2P Protocol (6 = Streaming, 17 = Datagram, 18 = Raw Datagrams) (Gzip
OS)

Note: I2P protocol numbers 224-254 are reserved for experimental
protocols. I2P protocol number 255 is reserved for future expansion.

Data integrity is verified with the standard gzip CRC-32 as specified by
[RFC 1952](http://www.ietf.org/rfc/rfc1952.txt).

## Important Differences from Standard IP

I2CP ports are for I2P sockets and datagrams. They are unrelated to your
local sockets or ports. Because I2P did not support ports and protocol
numbers prior to release 0.7.1, ports and protocol numbers are somewhat
different from that in standard IP, for backward compatibility:

- Port 0 is valid and has special meaning.
- Ports 1-1023 are not special or privileged.
- Servers listen on port 0 by default, which means \"all ports\".
- Clients send to port 0 by default, which means \"any port\".
- Clients send from port 0 by default, which means \"unspecified\".
- Servers may have a service listening on port 0 and other services
 listening on higher ports. If so, the port 0 service is the default,
 and will be connected to if the incoming socket or datagram port
 does not match another service.
- Most I2P destinations only have one service running on them, so you
 may use the defaults, and ignore I2CP port configuration.
- Protocol 0 is valid and means \"any protocol\". However, this is not
 recommended, and probably will not work. Streaming requires that the
 protocol number is set to 6.
- Streaming sockets are tracked by an internal connection ID.
 Therefore, there is no requirement that the 5-tuple of
 dest:port:dest:port:protocol be unique. For example, there may be
 multiple sockets with the same ports between two destinations.
 Clients do not need to pick a \"free port\" for an outbound
 connection.

## Future Work {#future}

- The current authorization mechanism could be modified to use hashed
 passwords.
- The Signing Private Keys is included in the Create Lease Set
 message, it is not required. Revocation is unimplemented. It should
 be replaced with random data or removed.
- Some improvements may be able to use messages previously defined but
 not implemented. For reference, here is the [I2CP Protocol
 Specification Version 0.9]() (PDF) dated
 August 28, 2003. That document also references the [Common Data
 Structures Specification Version 0.9]().

## See Also {#links}

[C library implementation](http://git.repo.i2p/w/libi2cp.git) 
