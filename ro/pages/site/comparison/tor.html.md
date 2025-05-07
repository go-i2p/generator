 I2P Compared to
Tor Noiembrie 2016 

## Tor / Onion Routing

*[\[Tor\]](https://www.torproject.org/) [\[Onion
Routing\]](http://www.onion-router.net)*

Tor and Onion Routing are both anonymizing proxy networks, allowing
people to tunnel out through their low latency mix network. The two
primary differences between Tor / Onion-Routing and I2P are again
related to differences in the threat model and the out-proxy design
(though Tor supports hidden services as well). In addition, Tor takes
the directory-based approach - providing a centralized point to manage
the overall \'view\' of the network, as well as gather and report
statistics, as opposed to I2P\'s distributed [network
database]() and [peer
selection]().

The I2P/Tor outproxy functionality does have a few substantial
weaknesses against certain attackers - once the communication leaves the
mixnet, global passive adversaries can more easily mount traffic
analysis. In addition, the outproxies have access to the cleartext of
the data transferred in both directions, and outproxies are prone to
abuse, along with all of the other security issues we\'ve come to know
and love with normal Internet traffic.

However, many people don\'t need to worry about those situations, as
they are outside their threat model. It is, also, outside I2P\'s
(formal) functional scope (if people want to build outproxy
functionality on top of an anonymous communication layer, they can). In
fact, some I2P users currently take advantage of Tor to outproxy.

### Comparison of Tor and I2P Terminology

While Tor and I2P are similar in many ways, much of the terminology is
different.

Tor

I2P

Cell

Message

Client

Router or Client

Circuit

Tunnel

Directory

NetDb

Directory Server

Floodfill Router

Entry Guards

Fast Peers

Entry Node

Inproxy

Exit Node

Outproxy

Hidden Service

Hidden Service, I2P Site or Destination

Hidden Service Descriptor

LeaseSet

Introduction point

Inbound Gateway

Node

Router

Onion Proxy

I2PTunnel Client (more or less)

Onion Service

Hidden Service, I2P Site or Destination

Relay

Router

Rendezvous Point

somewhat like Inbound Gateway + Outbound Endpoint

Router Descriptor

RouterInfo

Server

Router

### Benefits of Tor over I2P

- Much bigger user base; much more visibility in the academic and
 hacker communities; benefits from formal studies of anonymity,
 resistance, and performance; has a non-anonymous, visible,
 university-based leader
- Has already solved some scaling issues I2P has yet to address
- Has significant funding
- Has more developers, including several that are funded
- More resistant to state-level blocking due to TLS transport layer
 and bridges (I2P has proposals for \"full restricted routes\" but
 these are not yet implemented)
- Big enough that it has had to adapt to blocking and DOS attempts
- Designed and optimized for exit traffic, with a large number of exit
 nodes
- Better documentation, has formal papers and specifications, better
 website, many more translations
- More efficient with memory usage
- Tor client nodes have very low bandwidth overhead
- Centralized control reduces the complexity at each node and can
 efficiently address Sybil attacks
- A core of high capacity nodes provides higher throughput and lower
 latency
- C, not Java (ewww)

### Benefits of I2P over Tor

- Designed and optimized for hidden services, which are much faster
 than in Tor
- Fully distributed and self organizing
- Peers are selected by continuously profiling and ranking
 performance, rather than trusting claimed capacity
- Floodfill peers (\"directory servers\") are varying and untrusted,
 rather than hardcoded
- Small enough that it hasn\'t been blocked or DOSed much, or at all
- Peer-to-peer friendly
- Packet switched instead of circuit switched
 - implicit transparent load balancing of messages across multiple
 peers, rather than a single path
 - resilience vs. failures by running multiple tunnels in parallel,
 plus rotating tunnels
 - scale each client\'s connections at O(1) instead of O(N) (Alice
 has e.g. 2 inbound tunnels that are used by all of the peers
 Alice is talking with, rather than a circuit for each)
- Unidirectional tunnels instead of bidirectional circuits, doubling
 the number of nodes a peer has to compromise to get the same
 information. Counter-arguments and further discussion
 [here]().
- Protection against detecting client activity, even when an attacker
 is participating in the tunnel, as tunnels are used for more than
 simply passing end to end messages (e.g. netDb, tunnel management,
 tunnel testing)
- Tunnels in I2P are short lived, decreasing the number of samples
 that an attacker can use to mount an active attack with, unlike
 circuits in Tor, which are typically long lived.
- I2P APIs are designed specifically for anonymity and security, while
 SOCKS is designed for functionality.
- Essentially all peers participate in routing for others
- The bandwidth overhead of being a full peer is low, while in Tor,
 while client nodes don\'t require much bandwidth, they don\'t fully
 participate in the mixnet.
- Integrated automatic update mechanism
- Both TCP and UDP transports
- Java, not C (ewww)

### Other potential benefits of I2P but not yet implemented

\...and may never be implemented, so don\'t count on them!

- Defense vs. message count analysis by garlic wrapping multiple
 messages
- Defense vs. long term intersection by adding delays at various hops
 (where the delays are not discernible by other hops)
- Various mixing strategies at the tunnel level (e.g. create a tunnel
 that will handle 500 messages / minute, where the endpoint will
 inject dummy messages if there are insufficient messages, etc)


