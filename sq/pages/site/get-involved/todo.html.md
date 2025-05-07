 I2P Project
Targets 

- [Core functionality](#core)
 - [NetworkDB and profile tuning and ejection policy for large
 nets](#netdb)
- [Security / anonymity](#security)
 - [Full blown n-hop restricted routes with optional trusted
 links](#fullRestrictedRoutes)
 - [Hashcash for routerIdentity, destination, and tunnel
 request](#hashcash)
 - [Advanced tunnel operation
 (batching/mixing/throttling/padding)](#batching)
 - [Stop & go mix w/ garlics & tunnels](#stop)
- [Performance]()

 

Note: This page is not up-to-date. See [the
roadmap]() for current plans.

Below is a more detailed (yet still incomplete) discussion of the major
areas of future development on the core I2P network, spanning the
plausibly planned releases. This does not include stego transports,
porting to wireless devices, or tools to secure the local machine, nor
does it include client applications that will be essential in I2P\'s
success. There are probably other things that will come up, especially
as I2P gets more peer review, but these are the main \'big things\'. See
also [the roadmap](). Want to help? [Get
involved]()!

## Core functionality {#core}

- ### NetworkDB and profile tuning and ejection policy for large nets {#netdb}

 Within the current network database and profile management
 implementation, we have taken the liberty of some practical
 shortcuts. For instance, we don\'t have the code to drop peer
 references from the K-buckets, as we don\'t have enough peers to
 even plausibly fill any of them, so instead, we just keep the peers
 in whatever bucket is appropriate. Another example deals with the
 peer profiles - the memory required to maintain each peer\'s profile
 is small enough that we can keep thousands of full blown profiles in
 memory without problems. While we have the capacity to use trimmed
 down profiles (which we can maintain 100s of thousands in memory),
 we don\'t have any code to deal with moving a profile from a
 \"minimal profile\" to a \"full profile\", a \"full profile\" to a
 \"minimal profile\", or to simply eject a profile altogether. It
 just wouldn\'t be practical to write that code yet, since we aren\'t
 going to need it for a while.

 That said, as the network grows we are going to want to keep these
 considerations in mind. We will have some work to do, but we can put
 it off for later.

## Security / anonymity {#security}

- ### Full blown n-hop restricted routes with optional trusted links {#fullRestrictedRoutes}

 The restricted route functionality described before was simply a
 functional issue - how to let peers who would not otherwise be able
 to communicate do so. However, the concept of allowing restricted
 routes includes additional capabilities. For instance, if a router
 absolutely cannot risk communicating directly with any untrusted
 peers, they can set up trusted links through those peers, using them
 to both send and receive all of its messages. Those hidden peers who
 want to be completely isolated would also refuse to connect to peers
 who attempt to get them to (as demonstrated by the garlic routing
 technique outlined before) - they can simply take the garlic clove
 that has a request for delivery to a particular peer and tunnel
 route that message out one of the hidden peer\'s trusted links with
 instructions to forward it as requested.

- ### Hashcash for routerIdentity, destination, and tunnel request {#hashcash}

 Within the network, we will want some way to deter people from
 consuming too many resources or from creating so many peers to mount
 a [Sybil]() attack. Traditional techniques
 such as having a peer see who is requesting a resource or running a
 peer aren\'t appropriate for use within I2P, as doing so would
 compromise the anonymity of the system. Instead, we want to make
 certain requests \"expensive\".

 [Hashcash](http://www.hashcash.org/) is one technique that we can
 use to anonymously increase the \"cost\" of doing certain
 activities, such as creating a new router identity (done only once
 on installation), creating a new destination (done only once when
 creating a service), or requesting that a peer participate in a
 tunnel (done often, perhaps 2-300 times per hour). We don\'t know
 the \"correct\" cost of each type of certificate yet, but with some
 research and experimentation, we could set a base level that is
 sufficiently expensive while not an excessive burden for people with
 few resources.

 There are a few other algorithms that we can explore for making
 those requests for resources \"nonfree\", and further research on
 that front is appropriate.

- ### Advanced tunnel operation (batching/mixing/throttling/padding) {#batching}

 To powerful passive external observers as well as large colluding
 internal observers, standard tunnel routing is vulnerable to traffic
 analysis attacks - simply watching the size and frequency of
 messages being passed between routers. To defend against these, we
 will want to essentially turn some of the tunnels into its own mix
 cascade - delaying messages received at the gateway and passing them
 in batches, reordering them as necessary, and injecting dummy
 messages (indistinguishable from other \"real\" tunnel messages by
 peers in the path). There has been a significant amount of
 [research]() on these algorithms that we can
 lean on prior to implementing the various tunnel mixing strategies.

 In addition to the anonymity aspects of more varied tunnel
 operation, there is a functional dimension as well. Each peer only
 has a certain amount of data they can route for the network, and to
 keep any particular tunnel from consuming an unreasonable portion of
 that bandwidth, they will want to include some throttles on the
 tunnel. For instance, a tunnel may be configured to throttle itself
 after passing 600 messages (1 per second), 2.4MB (4KBps), or
 exceeding some moving average (8KBps for the last minute). Excess
 messages may be delayed or summarily dropped. With this sort of
 throttling, peers can provide ATM-like QoS support for their
 tunnels, refusing to agree to allocate more bandwidth than the peer
 has available.

 In addition, we may want to implement code to dynamically reroute
 tunnels to avoid failed peers or to inject additional hops into the
 path. This can be done by garlic routing a message to any particular
 peer in a tunnel with instructions to redefine the next-hop in the
 tunnel.

- ### Stop & go mix w/ garlics & tunnels {#stop}

 Beyond the per-tunnel batching and mixing strategy, there are
 further capabilities for protecting against powerful attackers, such
 as allowing each step in a garlic routed path to define a delay or
 window in which it should be forwarded on. This would enable
 protections against the long term intersection attack, as a peer
 could send a message that looks perfectly standard to most peers
 that pass it along, except at any peers where the clove exposed
 includes delay instructions.

## Performance

Performance related improvements are listed on the
[Performance]() page.


