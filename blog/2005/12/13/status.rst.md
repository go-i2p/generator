::: {#i2p-status-notes-for-2005-12-13 .document}
# I2P STATUS NOTES FOR 2005-12-13 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, 'tis that time again

    * Index
    1) Net status and load testing
    2) I2PSnark
    3) Syndie
    4) ???

    * 1) Net status and load testing

    Not much has changed in the last week, though we have had a little
    trouble on the irc servers.  Most of my time has been spent on
    various network load tests, trying to track down the source of our
    current throughput bottleneck.  Tunnels themselves can transfer at
    a high rate.  SSU can transfer at an even higher rate.  And the
    streaming lib can push even more data than that.  There are two
    general possibilities for the bottleneck - some software bug, or
    suboptimal (aka bad) peer selection.  What I'm doing now is trying
    to determine which it is.  Preliminary indications are that some
    peers (perhaps 25%) have no trouble pushing 20-100KBps through a
    tunnel, while the rest stay in the 1-4KBps range under load.
    However, thats only very preliminary results, and more realistic
    load tests are ongoing.

    We've also got zzz's latest changes improving the tunnel creation in
    CVS, and reports from the field have been good - nice work zzz!  I'm
    not sure when 0.6.1.8 will come out, but if not by the weekend, then
    early next week.  We'll see.

    * 2) I2PSnark

    The other day while gathering data from some load tests I patched up
    I2PSnark so that it can deal with torrents created by Azureus and
    I2PRufus again.  The problem was that it didn't know how to deal
    with some of the newer torrent attributes ("name.utf-8" and
    "path.utf-8"), which was causing it to mess up the infohash (and
    hence be unable to talk to the tracker or any peers).  Thats fixed
    in CVS, so it should be a workable anonymous bt client again - if
    anyone has problems getting it to deal with a torrent that I2P-BT
    can deal with, please let me know.

    * 3) Syndie

    Polecat has been hacking away, with the latest addition offering
    thumbnail support for attachments in SML (see the smlref.jsp on the
    current CVS build for more details).  I also put together a first 
    pass at the blog interface, but its not really that great, so
    another pass is definitely in the offing.  Keep an eye on your
    Syndie instance for the latest Syndie news, of course.

    * 4) ???

    There's lots going on, as always, though my focus still continues to
    be on improving performance to the point where its adequate for
    reasonable uses.  As mentioned on the forum, that I2Phex sourceforge
    fiasco is finally taken care of, and discussion continues regarding
    jbigi and jcpuid builds and dependencies (more news on that front
    when there's more to say).  Anyway, as always swing on by the
    meeting tonight at 20:00 UTC and say hey!

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFDnyJJWYfZ3rPnHH0RAn2eAJ0YmiNTCGm46zkyH44YB/gJ1tysOgCfX5UU
    RgvenKVDEEUbUMi8ePPOkuk=
    =GZ6w
    -----END PGP SIGNATURE-----
:::
