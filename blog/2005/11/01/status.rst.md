::: {#i2p-status-notes-for-2005-11-01 .document}
# I2P STATUS NOTES FOR 2005-11-01 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, its that time of the week again

    * Index
    1) 0.6.1.4 and net status
    2) boostraps, predecessors, global passive adversaries, and CBR
    3) i2phex 0.1.1.34
    4) voi2p app
    5) syndie and sucker
    6) ???

    * 1) 0.6.1.4 and net status

    Last saturday's 0.6.1.4 release seems to have gone fairly smoothly -
    75% of the network has upgraded already (thanks!), and most of the
    remaining are on 0.6.1.3 anyway.  Things seems to be working
    reasonably well, and while I haven't heard much feedback about it -
    either positive or negative, I'm assuming y'all would complain
    loudly if it were bad :)

    In particular, I'd be interested in hearing any feedback from people
    on dialup modem connections, as the testing I've done is only a
    basic simulation of that sort of connection.

    * 2) bootstraps, predecessors, global passive adversaries, and CBR

    There's been lots more discussion on the list regarding a few ideas,
    with a summary of the bootstrap attacks up online [1].  I've made
    some progress specing out the crypto for option 3, and while nothing
    has been posted yet, its fairly straightforward.

    [1] http://dev.i2p.net/pipermail/i2p/2005-October/001146.html

    There have been further discussions about how to improve resistance
    to powerful adversaries with constant bitrate (CBR) tunnels, and
    while we have the option to explore that avenue, its currently
    slated for I2P 3.0, as its proper use requires substantial
    resources, and would likely have a measureable impact on who would
    be willing to use I2P with such overhead as well as what groups
    would or would not even be able to.

    * 3) I2Phex 0.1.1.34

    Last saturday we also had a new I2Phex release [2], fixing a file
    descriptor leak which would eventually cause I2Phex to fail (thanks
    Complication!) and removing some code which would allow people to
    remotely tell your I2Phex instance to download some particular
    files (thanks GregorK!).  Upgrading is highly recommended.

    There's also been an update to the CVS version (not yet released)
    which clears up some synchronization issues - Phex assumes some
    network operations are processed immediately, while I2P can sometime
    take a while to do things :)  This manifests itself with the GUI
    hanging for a while, downloads or uploads stalling, or connections
    being refused (and perhaps a few other ways).  It hasn't had much
    testing yet, but will probably be pushed out into 0.1.1.35 this
    week.  I'm sure more news will be posted on the forum when there's
    more news.

    [2] http://forum.i2p.net/viewtopic.php?t=1143

    * 4) voi2p app

    Aum is churning away on his new voice (and text) over I2P app, and
    while I haven't seen it yet, it sounds neat.  Perhaps Aum can give
    us an update in the meeting, or we can just wait patiently for the
    first alpha release :)

    * 5) syndie and sucker

    dust has been working away on syndie and sucker, and the latest CVS
    build of I2P now lets you automatically pull in content from RSS and
    atom feeds and post them to your syndie blog.  At the moment, you've
    got to explicitly add lib/rome-0.7.jar and lib/jdom.jar to your
    wrapper.config (wrapper.java.classpath.20 and 21), but we'll bundle
    it up so that isn't necessary later.  Its still a work in progress,
    and rome 0.8 (not yet released) seems to offer some really cool
    stuff, such as the ability to snag the enclosures off a feed, which
    sucker will then be able to import as an attachment to a syndie
    post (right now it already handles images and links too though!)

    Like all rss feeds, there seem to be some discrepencies with how the
    content is included, so some feeds go in smoother than others.  I
    think if people were to help test it out with different feeds and
    let dust know of any issues that it b0rks on, that might be useful.
    In any case, this stuff looks pretty exciting, nice work dust!

    * 6) ???

    Thats about it for the moment, but if anyone has any questions or
    wants to discuss some things further, swing on by the meeting at 8P
    GMT (remember, daylight savings!)

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFDZ8KCWYfZ3rPnHH0RArTUAJ9040Fq8xFw6w0TSWCD3q1+fEyR6QCfWtdT
    QeaqMIqTB1tvEZI3YEIQX/Y=
    =UAkh
    -----END PGP SIGNATURE-----
:::
