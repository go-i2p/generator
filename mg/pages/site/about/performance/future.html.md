 Future Performance
Improvements August 2010 0.8 

There are a few major techniques that can be done to improve the
perceived performance of I2P - some of the following are CPU related,
others bandwidth related, and others still are protocol related.
However, all of those dimensions affect the latency, throughput, and
perceived performance of the network, as they reduce contention for
scarce resources. This list is of course not comprehensive, but it does
cover the major ones that are seen.

For past performance improvements see the [Performance
History]().

## Better peer profiling and selection

Probably one of the most important parts of getting faster performance
will be improving how routers choose the peers that they build their
tunnels through - making sure they don\'t use peers with slow links or
ones with fast links that are overloaded, etc. In addition, we\'ve got
to make sure we don\'t expose ourselves to a
[Sybil]() attack from a powerful adversary
with lots of fast machines.

## Network database tuning

We\'re going to want to be more efficient with the network database\'s
healing and maintenance algorithms - rather than constantly explore the
keyspace for new peers - causing a significant number of network
messages and router load - we can slow down or even stop exploring until
we detect that there\'s something new worth finding (e.g. decay the
exploration rate based upon the last time someone gave us a reference to
someone we had never heard of). We can also do some tuning on what we
actually send - how many peers we bounce back (or even if we bounce back
a reply), as well as how many concurrent searches we perform.

## Session Tag Tuning and Improvements

The way the [ElGamal/AES+SessionTag]()
algorithm works is by managing a set of random one-time-use 32 byte
arrays, and expiring them if they aren\'t used quickly enough. If we
expire them too soon, we\'re forced to fall back on a full (expensive)
ElGamal encryption, but if we don\'t expire them quickly enough, we\'ve
got to reduce their quantity so that we don\'t run out of memory (and if
the recipient somehow gets corrupted and loses some tags, even more
encryption failures may occur prior to detection). With some more active
detection and feedback driven algorithms, we can safely and more
efficiently tune the lifetime of the tags, replacing the ElGamal
encryption with a trivial AES operation.

Additional ideas for improving Session Tag delivery are described on the
[ElGamal/AES+SessionTag page](#future).

## Migrate sessionTag to synchronized PRNG {#prng}

Right now, our [ElGamal/AES+SessionTag]()
algorithm works by tagging each encrypted message with a unique random
32 byte nonce (a \"session tag\"), identifying that message as being
encrypted with the associated AES session\'s key. This prevents peers
from distinguishing messages that are part of the same session, since
each message has a completely new random tag. To accomplish this, every
few messages bundle a whole new set of session tags within the encrypted
message itself, transparently delivering a way to identify future
messages. We then have to keep track of what messages are successfully
delivered so that we know what tags we may use.

This works fine and is fairly robust, however it is inefficient in terms
of bandwidth usage, as it requires the delivery of these tags ahead of
time (and not all tags may be necessary, or some may be wasted, due to
their expiration). On average though, predelivering the session tag
costs 32 bytes per message (the size of a tag). As Taral suggested
though, that size can be avoided by replacing the delivery of the tags
with a synchronized PRNG - when a new session is established (through an
ElGamal encrypted block), both sides seed a PRNG for use and generate
the session tags on demand (with the recipient precalculating the next
few possible values to handle out of order delivery).

## Longer lasting tunnels

The current default tunnel duration of 10 minutes is fairly arbitrary,
though it \"feels okay\". Once we\'ve got tunnel healing code and more
effective failure detection, we\'ll be able to more safely vary those
durations, reducing the network and CPU load (due to expensive tunnel
creation messages).

This appears to be an easy fix for high load on the big-bandwidth
routers, but we should not resort to it until we\'ve tuned the tunnel
building algorithms further. However, the 10 minute tunnel lifetime is
hardcoded in quite a few places, so substantial effort would be required
to change the duration. Also, it would be difficult to maintain backward
compatibility with such a change.

Currently, since the network average tunnel build success rate is fairly
high, there are no current plans to extend tunnel lifetime.

## Adjust the timeouts

Yet another of the fairly arbitrary but \"okay feeling\" things we\'ve
got are the current timeouts for various activities. Why do we have a 60
second \"peer unreachable\" timeout? Why do we try sending through a
different tunnel that a LeaseSet advertises after 10 seconds? Why are
the network database queries bounded by 60 or 20 second limits? Why are
destinations configured to ask for a new set of tunnels every 10
minutes? Why do we allow 60 seconds for a peer to reply to our request
that they join a tunnel? Why do we consider a tunnel that doesn\'t pass
our test within 60 seconds \"dead\"?

Each of those imponderables can be addressed with more adaptive code, as
well as tunable parameters to allow for more appropriate tradeoffs
between bandwidth, latency, and CPU usage.

## Full streaming protocol improvements

- Perhaps re-enable the interactive stream profile (the current
 implementation only uses the bulk stream profile).
- Client level bandwidth limiting (in either or both directions on a
 stream, or possibly shared across multiple streams). This would be
 in addition to the router\'s overall bandwidth limiting, of course.
- Access control lists (only allowing streams to or from certain other
 known destinations).
- Web controls and monitoring the health of the various streams, as
 well as the ability to explicitly close or throttle them.

Additional ideas for improving the streaming library are described on
the [streaming library page](#future).


