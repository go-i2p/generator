::: {#i2p-status-notes-for-2005-11-15 .document}
# I2P STATUS NOTES FOR 2005-11-15 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, time for our weekly status notes

    * Index
    1) Net status / 0.6.1.5
    2) Syndie updates
    3) I2Phex
    4) I2P-Rufus
    5) Issue tracker
    6) ???

    * 1) Net status / 0.6.1.5

    The past week on the network has been pretty solid, and the other
    day stats.i2p logged more than 2000 unique routers on I2P over the
    past two weeks.  The stable network size has only gradually grown,
    but its nice to see I2P handling high churn rates without much
    trouble.

    There will be a new 0.6.1.5 release tonight with a whole bunch of
    changes, including a fairly heavily revamped Syndie, so keep an
    eye on the list, the forum, or the website for an announcement.

    * 2) Syndie updates

    As mentioned, we'll be bundling an updated Syndie tonight with 
    changes to the user interface, integration of dust's Sucker (for
    importing RSS/Atom into Syndie), and Ragnarok's updater (for
    scheduled synchronization).  Based on CofE's suggestion, Syndie will
    also default to "single user mode" and log in automatically to a
    default account.  People with existing Syndie logins can configure
    which account to log into automatically (see admin.jsp), though
    Syndie instances in multiuser mode (namely syndiemedia.i2p,
    glog.i2p, and gloinsblog.i2p) behave much like before.

    Another feature of the update is we will pull posts off those three
    multiuser Syndie instances automatically by default, using the
    HTTP proxy configured on config.jsp, which defaults to the eepproxy.
    Of course, this can be changed by simply going to the addressbook
    and unchecking the "Syndicate?" checkbox.

    There's a lot more to Syndie in this release as well, so I encourage
    people to give it a spin once you upgrade to 0.6.1.5.  You can also
    get a glimpse of how it works on syndiemedia [1] (with an updated
    intro doc @ [2]), though functionality is limited when you're not
    logged in as an administrator.

    [1] http://syndiemedia.i2p.net/
    [2] http://syndiemedia.i2p.net/about.html

    * 3) I2Phex

    Just a short note saying that 0.1.1.36 will be coming out later this
    evening as well, including the latest bugfix for that "Please insert
    a disk" popup.  Check the forum for news.

    * 4) I2P-Rufus

    defnax and Rawn have put together another I2P-Rufus release [2],
    available at defnax's site [3] or awup's mirror [4]

    [2] http://forum.i2p.net/viewtopic.php?t=1199
    [3] http://55cancri.i2p/archive/I2PRufus_0.0.3.zip
    [4] http://awup.i2p/downloads/I2PRufus_0.0.3.zip

    * 5) Issue tracker

    As mentioned on my blog [5], I'm looking for a good issue tracking
    package for I2P/et al, without the hassles of bugzilla.  Cervantes
    came up with an interesting solution [6] which has some really cool
    benefits, but I'd be interested to hear what other people think too.
    (perhaps post up your thoughts to syndie :)

    [5] http://syndiemedia.i2p.net/threads.jsp?
        post=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1132012800003&
    [5] http://syndiemedia.i2p.net/threads.jsp?
        post=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1132012800004&

    * 6) ???

    Lots and lots going on, as always.  Swing on by #i2p in a few
    minutes for our weekly dev meeting, and check the website and forum
    later tonight for the 0.6.1.5 announcement!

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFDejmgWYfZ3rPnHH0RAvbNAJ4ljQPgBSU+th4yNfkQItRDjAgbyQCffcuE
    wzUvzQmeOtZhXfemCLSsuZE=
    =w5pB
    -----END PGP SIGNATURE-----
:::
