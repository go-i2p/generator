::: {#i2p-status-notes-for-2005-10-18 .document}
# I2P STATUS NOTES FOR 2005-10-18 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, its Tuesday again

    * Index
    1) 0.6.1.3
    2) Freenet, I2P, and darknets (oh my)
    3) Tunnel bootstrap attacks
    4) I2Phex
    5) Syndie/Sucker
    6) ??? [500+ symmetric nat bounty]

    * 1) 0.6.1.3

    Last Friday we pushed out a new 0.6.1.3 release, and with 70% of the
    network upgraded, reports have been very positive.  The new SSU
    improvements seems to have cut down on unnecessary retransmissions,
    allowing more efficient throughput at higher rates, and there
    haven't been any major problems with the IRC proxy or Syndie
    improvements to my knowledge.

    One thing worth noting is that Eol has posted up a bounty for 
    symmetric NAT support on rentacoder[1], so hopefully we'll get some
    progress on that front!

    [1] http://rentacoder.com/RentACoder/misc/BidRequests
                              ShowBidRequest.asp?lngBidRequestId=349320

    * 2) Freenet, I2P, and darknets (oh my)

    We've finally wrapped up that 100+ message thread with a clearer
    view of the two networks, where they fit, and what room we have for
    further collaboration.  I won't go into what topologies or threat
    models they're best suited for here, but you can dig into the lists
    if you want to know more.  On the collaboration front, I bounced
    toad some sample code for reusing our SSU transport which may be
    helpful for the Freenet folks in the short term, and down the line
    we may be working together to offer premix routing for Freenet users
    in environments where I2P is viable.  As Freenet progresses, we may
    be able to get Freenet working on top of I2P as a client application
    as well, allowing automated content distribution among users running
    it (e.g. pushing around Syndie archives and posts), but we'll see
    how Freenet's planned load and content distribution systems work
    first.

    * 3) Tunnel bootstrap attacks

    Michael Rogers got in touch regarding some interesting new attacks
    on I2P's tunnel creation [2][3][4].  The primary attack
    (successfully mounting a predecessor attack during the entire
    bootstrap process) is interesting, but not really practical - the
    probability of success is (c/n)^t, with c attackers, n peers in
    the network, and t tunnels built by the target (lifetime) - less
    than the probability of an adversary taking over all h hops in a
    tunnel (P(success) = (c/n)^h) after the router has built h tunnels.

    Michael has posted another attack on the list which we're working
    through at the moment, so you'll be able to follow that one up there
    as well.

    [2] http://dev.i2p.net/pipermail/i2p/2005-October/001005.html
    [3] http://dev.i2p.net/pipermail/i2p/2005-October/001008.html
    [4] http://dev.i2p.net/pipermail/i2p/2005-October/001006.html

    * 4) I2Phex

    Striker is making more progress on the upload bug, and reports are
    that he has it pinned down.  It will hopefully get into CVS tonight,
    and will be released as 0.1.1.33 soon afterwards.  Keep an eye on
    the forum [5] for more info.

    [5] http://forum.i2p.net/viewforum.i2p?f=25

    The word on the street is that redzara is making pretty good
    progress merging back in with the Phex mainline too, so hopefully
    with Gregor's help we'll get things up to date soon!

    * 5) Syndie/Sucker

    dust has been crunching away with Sucker as well, with code getting
    more RSS/Atom data into Syndie.  Perhaps we can get Sucker and the
    post CLI further integrated into Syndie, maybe even a web based
    control to schedule imports of different RSS/Atom feeds into various
    blogs.  We shall see...

    * 6) ???

    There's lots going on beyond the above, but thats the main gist of
    what I'm aware of.  If anyone has any questions/concerns, or wants
    to bring some other things up, swing on by the meeting tonight at
    8PM UTC in #i2p!

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD4DBQFDVU4UWYfZ3rPnHH0RApF2AJ9Eqg55ydhqEjqSpkN5BSGb8MerYgCY16bD
    rYTKbx3oDZr3XWp3E9s0ag==
    =ga+r
    -----END PGP SIGNATURE-----
:::
