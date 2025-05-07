 Naming
discussion 

NOTE: The following is a discussion of the reasons behind the I2P naming
system, common arguments and possible alternatives. See [the naming
page]() for current documentation.

## Discarded alternatives

Naming within I2P has been an oft-debated topic since the very beginning
with advocates across the spectrum of possibilities. However, given
I2P\'s inherent demand for secure communication and decentralized
operation, the traditional DNS-style naming system is clearly out, as
are \"majority rules\" voting systems.

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
[alternate naming systems](#alternatives) can plug into, allowing end
users to drive what sort of naming tradeoffs they prefer.

## Discussion

See also [Names: Decentralized, Secure, Human-Meaningful: Choose
Two](https://zooko.com/distnames.html).

### Comments by jrandom

(adapted from a post in the old Syndie, November 26, 2005)

Q: What to do if some hosts do not agree on one address and if some
addresses are working, others are not? Who is the right source of a
name?

A: You don\'t. This is actually a critical difference between names on
I2P and how DNS works - names in I2P are human readable, secure, but
**not globally unique**. This is by design, and an inherent part of our
need for security.

If I could somehow convince you to change the destination associated
with some name, I\'d successfully \"take over\" the site, and under no
circumstances is that acceptable. Instead, what we do is make names
**locally unique**: they are what *you* use to call a site, just as how
you can call things whatever you want when you add them to your
browser\'s bookmarks, or your IM client\'s buddy list. Who you call
\"Boss\" may be who someone else calls \"Sally\".

Names will not, ever, be securely human readable and globally unique.

### Comments by zzz

The following from zzz is a review of several common complaints about
I2P\'s naming system.

- **Inefficiency:** The whole hosts.txt is downloaded (if it has
 changed, since eepget uses the etag and last-modified headers).
 It\'s about 400K right now for almost 800 hosts.

 True, but this isn\'t a lot of traffic in the context of i2p, which
 is itself wildly inefficient (floodfill databases, huge encryption
 overhead and padding, garlic routing, etc.). If you downloaded a
 hosts.txt file from someone every 12 hours it averages out to about
 10 bytes/sec.

 As is usually the case in i2p, there is a fundamental tradeoff here
 between anonymity and efficiency. Some would say that using the etag
 and last-modified headers is hazardous because it exposes when you
 last requested the data. Others have suggested asking for specific
 keys only (similar to what jump services do, but in a more automated
 fashion), possibly at a further cost in anonymity.

 Possible improvements would be a replacement or supplement to
 address book (see [p](http:///)), or something simple like
 subscribing to http://example.i2p/cgi-bin/recenthosts.cgi rather
 than http://example.i2p/hosts.txt. If a hypothetical recenthosts.cgi
 distributed all hosts from the last 24 hours, for example, that
 could be both more efficient and more anonymous than the current
 hosts.txt with last-modified and etag.

 A sample implementation is on stats.i2p at [](). This script returns an Etag with a
 timestamp. When a request comes in with the If-None-Match etag, the
 script ONLY returns new hosts since that timestamp, or 304 Not
 Modified if there are none. In this way, the script efficiently
 returns only the hosts the subscriber does not know about, in an
 address book-compatible manner.

 Die Ineffizienz ist kein großes Problem und es gibt mehrere Wege die
 Dinge zu verbessern ohne radikale Änderungen.

- **Not Scalable:** The 400K hosts.txt (with linear search) isn\'t
 that big at the moment and we can probably grow by 10x or 100x
 before it\'s a problem.

 As far as network traffic see above. But unless you\'re going to do
 a slow real-time query over the network for a key, you need to have
 the whole set of keys stored locally, at a cost of about 500 bytes
 per key.

- **Requires configuration and \"trust\":** Out-of-the-box address
 book is only subscribed to http://www.i2p2.i2p/hosts.txt, which is
 rarely updated, leading to poor new-user experience.

 This is very much intentional. jrandom wants a user to \"trust\" a
 hosts.txt provider, and as he likes to say, \"trust is not a
 boolean\". The configuration step attempts to force users to think
 about issues of trust in an anonymous network.

 As another example, the \"I2P Site Unknown\" error page in the HTTP
 Proxy lists some jump services, but doesn\'t \"recommend\" any one
 in particular, and it\'s up to the user to pick one (or not).
 jrandom would say we trust the listed providers enough to list them
 but not enough to automatically go fetch the key from them.

 How successful this is, I\'m not sure. But there must be some sort
 of hierarchy of trust for the naming system. To treat everyone
 equally may increase the risk of hijacking.

- **It isn\'t DNS**

 Unfortunately real-time lookups over i2p would significantly slow
 down web browsing.

 Also, DNS is based on lookups with limited caching and time-to-live,
 while i2p keys are permanent.

 Sure, we could make it work, but why? It\'s a bad fit.

- **Not reliable:** It depends on specific servers for address book
 subscriptions.

 Yes it depends on a few servers that you have configured. Within
 i2p, servers and services come and go. Any other centralized system
 (for example DNS root servers) would have the same problem. A
 completely decentralized system (everybody is authoritative) is
 possible by implementing an \"everybody is a root DNS server\"
 solution, or by something even simpler, like a script that adds
 everybody in your hosts.txt to your address book.

 People advocating all-authoritative solutions generally haven\'t
 thought through the issues of conflicts and hijacking, however.

- **Awkward, not real-time:** It\'s a patchwork of hosts.txt
 providers, key-add web form providers, jump service providers, I2P
 Site status reporters. Jump servers and subscriptions are a pain, it
 should just work like DNS.

 See the reliability and trust sections.

So, in summary, the current system is not horribly broken, inefficient,
or un-scalable, and proposals to \"just use DNS\" aren\'t well
thought-through.

## Alternativen {#alternatives}

The I2P source contains several pluggable naming systems and supports
configuration options to enable experimentation with naming systems.

- **Meta** - calls two or more other naming systems in order. By
 default, calls PetName then HostsTxt.

- **PetName** - Looks up in a petnames.txt file. The format for this
 file is NOT the same as hosts.txt.

- **HostsTxt** - Looks up in the following files, in order:

- 1. privatehosts.txt
 2. userhosts.txt
 3. hosts.txt

- **AddressDB** - Each host is listed in a separate file in a
 addressDb/ directory.

- **Eepget** - does an HTTP lookup request from an external server -
 must be stacked after the HostsTxt lookup with Meta. This could
 augment or replace the jump system. Includes in-memory caching.

- **Exec** - calls an external program for lookup, allows additional
 experimentation in lookup schemes, independent of java. Can be used
 after HostsTxt or as the sole naming system. Includes in-memory
 caching.

- **Dummy** - used as a fallback for Base64 names, otherwise fails.

The current naming system can be changed with the advanced config option
\'i2p.naming.impl\' (restart required). See
core/java/src/net/i2p/client/naming for details.

Any new system should be stacked with HostsTxt, or should implement
local storage and/or the address book subscription functions, since
address book only knows about the hosts.txt files and format.

## Zertifikate {#certificates}

I2P destinations contain a certificate, however at the moment that
certificate is always null. With a null certificate, base64 destinations
are always 516 bytes ending in \"AAAA\", and this is checked in the
address book merge mechanism, and possibly other places. Also, there is
no method available to generate a certificate or add it to a
destination. So these will have to be updated to implement certificates.

One possible use of certificates is for [proof of
work](#hashcash).

Another is for \"subdomains\" (in quotes because there is really no such
thing, i2p uses a flat naming system) to be signed by the 2nd level
domain\'s keys.

With any certificate implementation must come the method for verifying
the certificates. Presumably this would happen in the address book merge
code. Is there a method for multiple types of certificates, or multiple
certificates?

Adding on a certificate authenticating the responses as signed by some
centralized certificate authority would address many of the hostile
nameserver issues but would leave open replay attacks as well as hostile
certificate authority attacks.


