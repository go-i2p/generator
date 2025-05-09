::: {#i2p-status-notes-for-2005-01-04 .document}
# I2P STATUS NOTES FOR 2005-01-04 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, time for our first weekly status notes of 2005

    * Index
    1) Net status
    2) 0.4.2.6
    3) 0.5
    4) jabber @ chat.i2p
    5) ???

    * 1) Net status

    Over the last week, things have been pretty interesting on the net -
    on nye, there were some comments posted to a popular website talking
    about i2p-bt and we've had a small burst of new users.  At the
    moment there are between 120-150 routers on the net, though that
    peaked at 160 a few days ago.  The network held its own though, with
    high capacity peers picking up the excess load without much
    disruption to other peers.  Some users running without bandwidth
    limits on really fast links have reported throughput of 2-300KBps,
    while those with less capacity use the usual low 1-5KBps.

    I think I remember Connelly mentioning that he was seeing 300+
    different routers over the course of a few days after new years, so
    there has been significant churn.  On the other hand, we now have a
    steady 120-150 users online, unlike the previous 80-90, which is a
    reasonable increase.  We still do *not* want it to grow too much
    yet though, as there are known implementation issues that still need
    to be done.  Specifically, until the 0.6 release [1], we're going to
    want to stay below 2-300 peers to keep the number of threads at a
    reasonable level.  However, if someone wants to help out
    implementing the UDP transport, we can get there much faster.

    In the last week, I've watched the stats put out by the i2p-bt
    trackers and there have been gigs of large files transferred, with
    some reports of 80-120KBps.  IRC has had more bumps than usual
    since those comments were posted on that website, but its still on
    the order of hours between disconnect.  (from what I can tell, the
    router that irc.duck.i2p is on has been running pretty close to its
    bandwidth limit, which would explain things)

    [1] http://www.i2p.net/roadmap#0.6

    * 2) 0.4.2.6

    There have been some fixes and new features added to CVS since the
    0.4.2.5 release that we're going to want to roll out soon,
    including reliability fixes for the streaming lib, improved
    resiliance to IP address change, and the bundling of ragnarok's
    addressbook implementation.

    If you haven't heard of the addressbook or haven't used it, the
    short story is that it will magically update your hosts.txt file
    by periodically fetching and merging changes from some anonymously
    hosted locations (default being http://dev.i2p/i2p/hosts.txt and
    http://duck.i2p/hosts.txt).  You won't need to change any files,
    touch any configuration, or run any extra applications - it'll be
    deployed inside the I2P router as a standard .war file.

    Of course, if you *do* want to get down and dirty with the
    addressbook, you are more than welcome to - see Ragnarok's site [2]
    for the details.  People who already have the addressbook deployed
    in their router will need to do a little tap dancing during the
    0.4.2.6 upgrade, but it'll work with all your old config settings.

    [2] http://ragnarok.i2p/

    * 3) 0.5

    Numbers, numbers, numbers!  Well, as I've said before, the 0.5
    release will be revamping how the tunnel routing works, and progress
    is being made on that front.  For the last few days I've been
    implementing the new encryption code (and unit tests), and once
    they're working I'll post up a doc describing my current thoughts on
    how, what, and why the new tunnel routing will operate.  I'm getting
    the encryption implemented for it now instead of later so that
    people can review what it means in a concrete sense, as well as find
    problems areas and suggestions for improvement.  I'm hoping to have
    the code working by the end of the week, so maybe there'll be more
    docs posted this weekend.  No promises though.

    * 4) jabber @ chat.i2p

    jdot has started up a new jabber server, and it seems to work pretty
    well for both one on one conversations and group chat.  check out
    the info on the forum [3].  the i2p dev discussion channel will
    still be the irc #i2p, but its always nice to have alternatives.

    [3] http://forum.i2p.net/viewtopic.php?t=229

    * 5) ???

    Ok, thats about all I have to mention at the moment - I'm sure
    there's lots more going on that other people want to bring up
    though, so swing on by the meeting in 15m @ the usual place [4] and
    tell us whats up!

    =jr

    [4] irc://irc.{duck,baffled}.i2p/#i2p
        irc://iip/#i2p
        irc://irc.freenode.net/#i2p
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.2.4 (GNU/Linux)

    iD8DBQFB2wGXGnFL2th344YRAuAkAJwPh8frN6Caof0unduGzijXFyFDnwCfXD/8
    ZQXQmqk6EIx184r2Zi7poZg=
    =+oCL
    -----END PGP SIGNATURE-----
:::
