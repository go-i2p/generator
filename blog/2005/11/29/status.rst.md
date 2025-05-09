::: {#i2p-status-notes-for-2005-11-29 .document}
# I2P STATUS NOTES FOR 2005-11-29 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi gang, its tuesday again

    * Index
    1) Net status and 0.6.1.6
    2) Syndie
    3) I2P Rufus 0.0.4
    4) ???

    * 1) Net status and 0.6.1.6

    Another week, another release.  The network seems reasonably well
    behaved, and with 60+% of the routers up to date, there does appear
    to be a noticeable improvement in performance, at least from the
    perspective of bandwidth efficiency and end to end throughput.  Its
    still not where I'd like it to be, but we're getting there.

    There have been some issues with the latest release though,
    including some bugs I unintentionally injected into Raccoon23's
    dynamic keys patch.  Those have been corrected in CVS though, and we
    should have a 0.6.1.7 release out in the next day or two (which will
    include some other neat stuff as well).  If you haven't run into
    trouble, then don't worry, and if you don't know if you've run into
    trouble, you haven't :)

    One thing I'm considering for 0.6.1.7 is perhaps dropping support
    for the TCP transport (at least for normal communication).  The
    general idea is that we can use the TCP transport for people's
    restricted routes / trusted links, but not to require it for general
    network operation, as we do for SSU.  This'll only happen if I can
    get some issues resolved cleanly, so it might not make it into
    0.6.1.7, but its on the short list of things to do.  You've been
    warned :)

    * 2) Syndie

    There is lots of progress on the Syndie front as well, though some
    important bits are going on within Syndie itself.  If you haven't
    checked it out yet, swing by the roadmap thread [1], or some of the
    other threads posted recently.  I've also posted up some basic info
    on how syndie works behind the scenes, and will be expanding upon
    that in the coming days [2].

    [1] http://localhost:7657/syndie/threads.jsp?tags=roadmap
        or http://syndiemedia.i2p.net/threads.jsp?tags=roadmap
    [2] http://localhost:7657/syndie/threads.jsp?tags=syndie.doc
        or http://syndiemedia.i2p.net/threads.jsp?tags=syndie.doc

    * 3) I2P Rufus 0.0.4

    Rawn and defnax have done it again with a new I2P Rufus release [3].
    Looks like some good progress over there, nice work y'all!

    [3] http://forum.i2p.net/viewtopic.php?t=1244

    * 4) ???

    There's some interesting stuff coming down the pipe, and we're
    making some good progress clearing issues to get us towards 0.6.2
    and beyond.  As always, swing on by the meeting tonight to discuss
    things further - #i2p at 8p UTC!

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFDjKoiWYfZ3rPnHH0RAoP+AKCBqpM6IT5leoNz+u5X6ZeXeK2+WQCeKkI0
    TGFrhg6eQyzhNa6jNV3s3bA=
    =vhfE
    -----END PGP SIGNATURE-----
:::
