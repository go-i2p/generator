::: {#i2p-status-notes-for-2005-03-01 .document}
# I2P STATUS NOTES FOR 2005-03-01 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, time for our status update

    * Index
    1) 0.5.0.1
    2) roadmap
    3) addressbook editor and config
    4) i2p-bt
    5) ???

    * 1) 0.5.0.1

    As discussed last week, a few hours after the meeting we pushed out
    a new 0.5.0.1 release fixing the bugs in 0.5 that had caused the
    massive number of tunnels being built (among other things).
    Generally, this rev has improved things, but under wider testing,
    we've come across some additional bugs that have been hitting a few
    people.  In particular, the 0.5.0.1 rev can gobble tons of CPU if
    you have a slow machine or your router's tunnels fail in bulk, and
    some long lived I2PTunnel servers can gobble up RAM until it OOMs.
    There has also been a long standing bug in the streaming lib, where
    we can fail to establish a connection if just the right failures
    happen.

    Most of these (among others) have been fixed in cvs, but some remain
    outstanding.  Once they're all fixed, we'll package 'er up and ship
    it as a 0.5.0.2 release.  I'm not exactly sure when that'll be,
    hopefully this week, but we'll see.

    * 2) roadmap

    After major releases, the roadmap [1] seems to get... adjusted.  The
    0.5 release was no different.  That page reflects what I think is
    reasonable and appropriate for the way forward, but of course, if
    more people jump on to help out with things, it can certainly be
    adjusted.  You'll notice the substantial break between 0.6 and
    0.6.1, and while this does reflect lots of work, it also reflects
    the fact that I'll be moving (its that time of the year again).

    [1] http://www.i2p.net/roadmap

    * 3) addressbook editor and config

    Detonate has started some work on a web based interface to manage
    the addressbook entries (hosts.txt), and its looking pretty
    promising.  Perhaps we can get an update from detonate during the
    meeting?

    In addition, smeghead has been doing some work on a web based
    interface to manage the addressbook configuration (the
    subscriptions.txt, config.txt).  Perhaps we can get an update from
    smeghead during the meeting?

    * 4) i2p-bt

    There's been some progress on the i2p-bt front, with a new 0.1.8
    release addressing the azneti2p compatability issues as discussed
    in last week's meeting.  Perhaps we can get an update from duck or
    smeghead during the meeting?

    Legion has also created a fork off the i2p-bt rev, merged in some
    other code, patched up some things, and has a windows binary
    available on his eepsite(I2P Site).  The announcement [2] seems to suggest
    that source may be made available, though its not up on the eepsite(I2P Site)
    at the moment.  The i2p devs haven't audited (or even seen) the code
    to that client, so those who need anonymity may want to get and
    review a copy of the code first.

    [2] http://forum.i2p.net/viewtopic.php?t=382

    There's also work on a version 2 of Legion's BT client, though I
    don't know the status of that.  Perhaps we can get an update from
    Legion during the meeting?

    * 5) ???

    Thats about all I have to say atm, lots and lots going on.  Anyone
    else working on things that perhaps we can get an update for during
    the meeting?

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.2.4 (GNU/Linux)

    iD8DBQFCJNebGnFL2th344YRAobNAJ4lfCULXX7WAGZxOlh/NzTuV1eNwgCg1eV/
    /h5I4b/h0SPpmq/GVKZsLns=
    =EEkH
    -----END PGP SIGNATURE-----
:::
