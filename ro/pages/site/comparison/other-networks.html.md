 I2P Compared to
Other Anonymous Networks 

The following networks are discussed on this page.

- RetroShare
- Morphmix / Tarzan
- Mixminion / Mixmaster
- JAP
- MUTE / AntsP2P
- Haystack

Most of the following sections are fairly old, and may not be accurate.
For an overview of available comparisons, see the [main network
comparisons page](). You may contribute an
analysis by entering a [new issue on Github]().

## RetroShare

*[\[RetroShare\]](http://retroshare.net)*

RetroShare is a set of peer-to-peer applications running in a
[Friend-to-friend (F2F)]() network. Each peer
of such F2F network makes direct IP connections only to authenticated
peers (\"friends\") after explicit certificates exchange. It can
discover unauthenticated peers (e.g. friends of friends), but
connections to them are relayed over \"friend\" peers for providing
privacy and anonymity.

RetroShare is designed to build a private network of trusted peers,
while I2P is designed to be a large-scaled public anonymous network.
Recent versions of RetroShare have options to run as a public
\"darknet\" by using I2P or Tor as a transport. That way all connections
are anonymized and no trust is required for adding new \"friends\".

## Morphmix / Tarzan

*[\[Morphmix paper at
Freehaven\]](https://www.freehaven.net/anonbib/cache/morphmix:wpes2002.pdf)
[\[Tarzan paper at
Freehaven\]](https://www.freehaven.net/anonbib/cache/tarzan:ccs02.pdf)*

Morphmix and Tarzan are both fully distributed, peer to peer networks of
anonymizing proxies, allowing people to tunnel out through the low
latency mix network. Morphmix includes some very interesting collusion
detection algorithms and Sybil defenses, while Tarzan makes use of the
scarcity of IP addresses to accomplish the same. The two primary
differences between these systems and I2P are related to I2P\'s [threat
model]() and their out-proxy design (as
opposed to providing both sender and receiver anonymity). There is
source code available to both systems, but we are not aware of their use
outside of academic environments.

## Mixminion / Mixmaster

*[\[Mixminion\]](http://mixminion.net/)
[\[Mixmaster\]](http://mixmaster.sourceforge.net/)*

As with Tor and Onion Routing, both Mixminion and Mixmaster take the
directory based approach as well.

## JAP

*[\[JAP\]](http://anon.inf.tu-dresden.de/index_en.html)*

JAP (Java Anonymous Proxy) is a network of mix cascades for anonymizing
web requests, and as such it has a few centralized nodes (participants
in the cascade) that blend and mix requests from clients through the
sequence of nodes (the cascade) before proxying out onto the web. The
scope, threat model, and security is substantially different from I2P,
but for those who don\'t require significant anonymity but still are not
satisfied with an Anonymizer-like service, JAP is worth reviewing. One
caution to note is that anyone under the jurisdiction of the German
courts may want to take care, as the German Federal Bureau of Criminal
Investigation (FBCI) has successfully mounted an
[attack]() on the network. Even though the method
of this attack was later found to be illegal in the German courts, the
fact that the data was successfully collected is the concern. Courts
change their minds based upon circumstance, and this is evidence that if
a government body or intelligence agency wanted to, they could gather
the data, even if it may be found inadmissible in some courts later)

## MUTE / AntsP2P

*[\[MUTE\]](http://mute-net.sourceforge.net/)
[\[AntsP2P\]](http://antsp2p.sourceforge.net/)*

Both of these systems work through the same basic
[antnet]() routing, providing some degree of
anonymity based on the threat model of providing plausible deniability
against a simple non-colluding adversary. With the antnet routing, they
first either do a random walk or a broadcast search to find some peer
with the data or identity desired, and then use a feedback algorithm to
optimize that found path. This works well for applications that merely
want to know what other people around them have to offer - \"How are
y\'all doing\" vs. \"Hey Alice, how are you\" - you basically get a
local cluster of nodes that can share files with and maintain some
degree of anonymity (though you don\'t have much control over who is in
that group of peers).

However, the algorithm does not scale well at all - if the application
wants to speak with a particular peer it ends up doing a broadcast
search or random walk (though if they are lucky enough for that to
succeed, the antnet routing should optimize that found connection). This
means that while these networks can work great at small scales, they are
not suitable for large networks where someone wants to get in touch with
another specific peer. That does not mean that there is no value in
these systems, just that their applicability is limited to situations
where their particular issues can be addressed.

## Haystack

This was a closed-source network targeted at Iranian users. Tor did a
[good writeup on what to look for in a circumvention
tool](). Suffice it to say that being closed
source and publicly targeting a specific country are not good ideas. I2P
is, of course, open source. However, that source, and our [technical
documentation](), need much more review.

## Paid VPN Services

You may contribute an analysis by entering a [new issue on
Github]().

## Others

You may contribute an analysis by entering a [new issue on
Github]().


