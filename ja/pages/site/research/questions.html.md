 Open research
questions May 2018 

## Network database

### Floodfills

- Are there any other ways to mitigate network brute-forcing via
 significant floodfill control?
- Is there any way to detect, flag and potentially remove \'bad
 floodfills\' similar to the Tor relay authorities, without actually
 needing to rely on a form of central authority?

## Transports

- How could packet retransmission strategies and timeouts be improved?
- Is there a way for I2P to obfuscate packets and reduce traffic
 analysis more efficiently than other proposed ideas? (Padding
 transport layer, developing mimic protocols, etc.)

## Tunnels and Destinations

### Peer selection

- Is there a way that I2P could perform peer selection more
 efficiently or securely?
- Would it negatively impact anonymity to use geoip in order to
 prioritise physically nearby peers for tunnel building? The primary
 goal would be to increase tunnel success and reduce breakage.

### Unidirectional tunnels

- What are the benefits of unidirectional tunnels over bidirectional
 tunnels? What are the tradeoffs?
- More details are available
 [here]().

### Multihoming

- How effective is multihoming at load-balancing?
- How does it scale? What happens as more routers host the same
 Destination?
- The benefit for anonymity is less correlation of router uptime to
 Destination uptime. Are there tradeoffs?

### Message routing

- How much is the effectiveness of timing attacks reduced by
 fragmentation and mixing of messages?
- What mixing strategies could I2P benefit from?
- How can high-latency techniques (e.g. message-dependent routing
 delays) be effectively employed within or alongside our low-latency
 network?

## Anonymity

- How significantly does browser fingerprinting impact the anonymity
 of I2P users? Would developing a browser package be beneficial for
 the average user?

## Network Related

- What is the overall impact on the network created by \'greedy
 users\' (users who take bandwidth from the network without
 contributing any back themselves)? Would additional steps for
 encouraging bandwidth participation be valuable?


