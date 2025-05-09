::: {#i2p-status-notes-for-2005-06-21 .document}
# I2P STATUS NOTES FOR 2005-06-21 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, time to start back up our weekly status notes

    * Index
    1) Dev[eloper] status
    2) Dev[elopment] status
    3) Unit test bounty
    4) Service outage
    5) ???

    * 1) Dev[eloper] status

    After 4 cities in 4 countries, I'm finally getting settled and
    churning through code again.  Last week I got the last of the
    pieces to a laptop together, I'm no longer couch hopping, and
    while I don't have net access at home, there are plenty of net
    cafes around, so access is reliable (just infrequent and
    expensive).

    That last point means that I won't be hanging out on irc as much
    as before, at least until the fall (I've got a sublet through
    August or so and will be looking for a place where I can get 24/7 net
    access).  That doesn't, however, mean that I won't be doing as
    much - I'll just be working largely on my own test network, pushing
    out builds for live net testing (and, er, oh yeah, releases).  It
    does mean though that we may want to move some discussions that used
    to go on free form in #i2p onto the list [1] and/or the forum [2] (I
    do still read the #i2p backlog though).  I haven't found a
    reasonable place where I can go to for our development meetings yet,
    so I won't be there this week, but perhaps by next week I'll have
    found one.

    Anyway, enough about me.

    [1] http://dev.i2p.net/pipermail/i2p/
    [2] http://forum.i2p.net/

    * 2) Dev[elopment] status

    While I've been moving, there have been two main fronts that I've
    been working on - documentation and the SSU transport (the later
    only since I got the laptop).  The docs are still in progress, with
    a big ol' scary overview one as well as a series of smaller
    implementation docs (covering things like source layout, component
    interaction, etc).

    SSU progress is going well - the new ACK bitfields are in place, the
    communication is dealing with (simulated) loss effectively, rates
    are appropriate for the various conditions, and I've cleared some of
    the uglier bugs I had run into previously.  I am continuing to test
    these changes though, and once its appropriate we'll plot out a
    series of live net tests for which we'll need some volunteers to
    help out with.  More news on that front when its available.

    * 3) Unit test bounty

    I'm glad to announce that Comwiz has come forward with a series of
    patches to claim the first phase of the unit test bounty [3]!  We are
    still working through some minor details of the patches, but I've
    received the updates and generated both the junit and clover reports
    as necessary.  I expect we'll have the patches in CVS shortly, at
    which point we'll put out Comwiz's testing docs.

    As clover is a commercial product (free for OSS developers [4]),
    only those who have installed clover and received their clover
    license will be able to generate the clover reports.  In any case,
    we'll be publishing the clover reports on the web periodically, so
    those who don't have clover installed can still see how well our
    test suite is doing.

    [3] http://www.i2p.net/bounties_unittest
    [4] http://www.cenqua.com/clover/

    * 4) Service outage

    As many have probably noticed, (at least) one of the outproxies is
    offline (squid.i2p), as is www.i2p, dev.i2p, cvs.i2p, and my blog.
    These are not unrelated events - the machine hosting them is hosed.
    I'm working on getting it back up though, at which point those five
    services will be back in operation.  Just an FYI.

    * 5) ???

    As there isn't a dev meeting on irc this week, if anyone else has
    anything to bring up, please feel free to post up to the list or the
    forum.  I've been following the discussions on the list, the forum,
    and in #i2p while I've been away, and have been glad to be able to
    sit back and let other people answer most of the questions.

    I do appreciate the patience people have had with the slow down in
    releases as well, and realize that in some projects that would be
    cause for alarm.  I2P is not, however, one of those projects - I've
    been working on it fulltime for more than two years now and will not
    stop until the needs that have been driving it are met.  I am not
    wed to particular technologies for technologies sake, but merely
    follow what seems to be the best path from here to where we need to
    be, and as far as I can tell, we are still following the best path
    available.  This summer, fall, and winter look to be a very exciting
    time in the anonymity field.

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFCuEcEWYfZ3rPnHH0RAvltAJ0fuhd/QRRqICtnqITeljKRw8cbbACeInKx
    gaRYTsDAU3zHBCxr4TiSl18=
    =uXj9
    -----END PGP SIGNATURE-----
:::
