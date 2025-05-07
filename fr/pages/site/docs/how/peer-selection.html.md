 Peer Profiling and
Selection 2024-02 0.9.62 

## NOTE

This page describes the Java I2P implementation of peer profiling and
selection as of 2010. While still broadly accurate, some details may no
longer be correct. We continue to evolve banning, blocking, and
selection strategies to address newer threats, attacks, and network
conditions. The current network has multiple router implementations with
various versions. Other I2P implementations may have completely
different profiling and selection strategies, or may not use profiling
at all.

## Vue d'ensemble

### Peer Profiling

**Peer profiling** is the process of collecting data based on the
**observed** performance of other routers or peers, and classifying
those peers into groups. Profiling does **not** use any claimed
performance data published by the peer itself in the [network
database]().

Profiles are used for two purposes:

1. Sélectionner des pairs pour retransmettre notre trafic à travers, ce
 qui est discuté ci-dessous
2. Choosing peers from the set of floodfill routers to use for network
 database storage and queries, which is discussed on the [network
 database]() page

### Peer Selection

**Peer selection** is the process of choosing which routers on the
network we want to relay our messages to go through (which peers will we
ask to join our tunnels). To accomplish this, we keep track of how each
peer performs (the peer\'s \"profile\") and use that data to estimate
how fast they are, how often they will be able to accept our requests,
and whether they seem to be overloaded or otherwise unable to perform
what they agree to reliably.

Unlike some other anonymous networks, in I2P, claimed bandwidth is
untrusted and is **only** used to avoid those peers advertising very low
bandwidth insufficient for routing tunnels. All peer selection is done
through profiling. This prevents simple attacks based on peers claiming
high bandwidth in order to capture large numbers of tunnels. It also
makes [timing attacks](#timing) more
difficult.

Peer selection is done quite frequently, as a router may maintain a
large number of client and exploratory tunnels, and a tunnel lifetime is
only 10 minutes.

### Further Information

For more information see the paper [Peer Profiling and Selection in the
I2P Anonymous Network]() presented at [PET-CON
2009.1](). See [below](#notes) for notes on minor
changes since the paper was published.

## Profils

Each peer has a set of data points collected about them, including
statistics about how long it takes for them to reply to a network
database query, how often their tunnels fail, and how many new peers
they are able to introduce us to, as well as simple data points such as
when we last heard from them or when the last communication error
occurred. The specific data points gathered can be found in the
[code]().

Profiles are fairly small, a few KB. To control memory usage, the
profile expiration time lessens as the number of profiles grows.
Profiles are kept in memory until router shutdown, when they are written
to disk. At startup, the profiles are read so the router need not
reinitialize all profiles, thus allowing a router to quickly
re-integrate into the network after startup.

## Peer Summaries

While the profiles themselves can be considered a summary of a peer\'s
performance, to allow for effective peer selection we break each summary
down into four simple values, representing the peer\'s speed, its
capacity, how well integrated into the network it is, and whether it is
failing.

### Vitesse

The speed calculation simply goes through the profile and estimates how
much data we can send or receive on a single tunnel through the peer in
a minute. For this estimate it just looks at performance in the previous
minute.

### Capacité {#capacity}

The capacity calculation simply goes through the profile and estimates
how many tunnels the peer would agree to participate in over a given
time period. For this estimate it looks at how many tunnel build
requests the peer has accepted, rejected, and dropped, and how many of
the agreed-to tunnels later failed. While the calculation is
time-weighted so that recent activity counts more than later activity,
statistics up to 48 hours old may be included.

Recognizing and avoiding unreliable and unreachable peers is critically
important. Unfortunately, as the tunnel building and testing require the
participation of several peers, it is difficult to positively identify
the cause of a dropped build request or test failure. The router assigns
a probability of failure to each of the peers, and uses that probability
in the capacity calculation. Drops and test failures are weighted much
higher than rejections.

## Peer organization

As mentioned above, we drill through each peer\'s profile to come up
with a few key calculations, and based upon those, we organize each peer
into three groups - fast, high capacity, and standard.

The groupings are not mutually exclusive, nor are they unrelated:

- A peer is considered \"high capacity\" if its capacity calculation
 meets or exceeds the median of all peers.
- A peer is considered \"fast\" if they are already \"high capacity\"
 and their speed calculation meets or exceeds the median of all
 peers.
- A peer is considered \"standard\" if it is not \"high capacity\"

These groupings are implemented in the router\'s
[ProfileOrganizer]().

### Group size limits

The size of the groups may be limited.

- The fast group is limited to 30 peers. If there would be more, only
 the ones with the highest speed rating are placed in the group.
- The high capacity group is limited to 75 peers (including the fast
 group) If there would be more, only the ones with the highest
 capacity rating are placed in the group.
- The standard group has no fixed limit, but is somewhat smaller than
 the number of RouterInfos stored in the local network database. On
 an active router in today\'s network, there may be about 1000
 RouterInfos and 500 peer profiles (including those in the fast and
 high capacity groups)

## Recalculation and Stability

Summaries are recalculated, and peers are resorted into groups, every 45
seconds.

The groups tend to be fairly stable, that is, there is not much
\"churn\" in the rankings at each recalculation. Peers in the fast and
high capacity groups get more tunnels build through them, which
increases their speed and capacity ratings, which reinforces their
presence in the group.

## Peer Selection

The router selects peers from the above groups to build tunnels through.

### Peer Selection for Client Tunnels

Client tunnels are used for application traffic, such as for HTTP
proxies and web servers.

Pour réduire la sensibilité à [certaines
attaques](http://blog.torproject.org/blog/one-cell-enough), et augmenter
la performance les pairs pour construire des tunnels de client sont
choisis aléatoirement à partir du groupe le plus petit, qui est le
groupe \"rapide\". Il n'y a aucun biais à sélectionner des pairs qui
étaient précédemment des participants à un tunnel pour le même client.

### Peer Selection for Exploratory Tunnels

Exploratory tunnels are used for router administrative purposes, such as
network database traffic and testing client tunnels. Exploratory tunnels
are also used to contact previously unconnected routers, which is why
they are called \"exploratory\". These tunnels are usually
low-bandwidth.

Les pairs pour construire des tunnels exploratoires sont généralement
choisis aléatoirement à partir du groupe standard. Si le taux de
réussite de ces tentatives de construction est bas comparé au taux de
réussite de construction de tunnel de client, au lieu de cela le routeur
choisira une moyenne pondérée de pairs aléatoires à partir du groupe de
haute capacité. Cela aide à maintenir un taux de réussite de
construction satisfaisant même quand la performance du réseau est
pauvre. Il n'y a aucun biais à sélectionner des pairs qui étaient
précédemment des participants à un tunnel exploratoire.

As the standard group includes a very large subset of all peers the
router knows about, exploratory tunnels are essentially built through a
random selection of all peers, until the build success rate becomes too
low.

### Restrictions

To prevent some simple attacks, and for performance, there are the
following restrictions:

- Two peers from the same /16 IP space may not be in the same tunnel.
- A peer may participate in a maximum of 33% of all tunnels created by
 the router.
- Peers with extremely low bandwidth are not used.
- Peers for which a recent connection attempt failed are not used.

### Peer Ordering in Tunnels

Peers are ordered within tunnels to to deal with the [predecessor
attack]() [(2008
update)](). More information is on the [tunnel
page](#ordering).

## Future Work

- Continue to analyze an tune speed and capacity calculations as
 necessary
- Implement a more aggressive ejection strategy if necessary to
 control memory usage as the network grows
- Evaluate group size limits
- Use GeoIP data to include or exclude certain peers, if configured

## Notes

For those reading the paper [Peer Profiling and Selection in the I2P
Anonymous Network](), please keep in mind the
following minor changes in I2P since the paper\'s publication:

- The Integration calculation is still not used
- In the paper, \"groups\" are called \"tiers\"
- The \"Failing\" tier is no longer used
- The \"Not Failing\" tier is now named \"Standard\"

## Références

- [Profilage de pair et sélection dans le réseau anonyme
 I2P](pdf/I2P-PET-CON-2009.1.pdf)
- [One Cell Enough](http://blog.torproject.org/blog/one-cell-enough)
- [Tor Entry
 Guards](https://wiki.torproject.org/noreply/TheOnionRouter/TorFAQ#EntryGuards)
- [Murdoch 2007 Paper](http://freehaven.net/anonbib/#murdoch-pet2007)
- [Tune-up for
 Tor](http://www.crhc.uiuc.edu/~nikita/papers/tuneup-cr.pdf)
- [Low-resource Routing Attacks Against
 Tor](http://cs.gmu.edu/~mccoy/papers/wpes25-bauer.pdf)


