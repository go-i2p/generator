::: {#i2p-status-notes-for-2005-02-15 .document}
# I2P STATUS NOTES FOR 2005-02-15 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Bonjour, sa cette fois de la semaine encore,

    * Index
    1) Net status
    2) 0.5 status
    3) i2p-bt 0.1.7
    4) ???

    * 1) Net status

    While no new bugs have shown up in the network, last week we gained
    some exposure on a popular French p2p website, which has led to an
    increase both in users and in bittorrent activity.  At the peak, we
    reached 211 routers on the net, though its hovering between 150 and
    180 lately.  Reported bandwidth usage has been up as well, though
    unfortunately the irc reliability has been degraded, with one of the
    servers lowering their bandwidth limits due to the load.  There have
    been a bunch of improvements to the streaming lib to help with this,
    but they've been on the 0.5-pre branch, so not yet available to the
    live net.

    Another transient problem has been the outage of one of the HTTP
    outproxies (www1.squid.i2p), causing 50% of outproxy requests to
    fail.  You can temporarily remove that outproxy by opening up your
    I2PTunnel config [1], editing the eepProxy, and changing the
    "Outproxies:" line to contain only "squid.i2p".  Hopefully we'll
    get that other one back online soon to increase redundancy.

    [1] http://localhost:7657/i2ptunnel/index.jsp

    * 2) 0.5 status

    There has been lots of progress this past week on 0.5 (I bet you're
    tired of hearing that, 'eh?).  Thanks to the help of postman,
    cervantes, duck, spaetz, and some unnamed person, we've been running
    a test network with the new code for nearly a week and have worked
    through a good number of bugs that I hadn't seen in my local test
    network.

    For the past day or so now, the changes have been minor, and I don't
    forsee any substantial code left before the 0.5 release goes out.
    There is some additional cleaning, documentation, and assembly left,
    and it doesn't hurt to let the 0.5 test network churn through in
    case additional bugs are exposed over time.  Since this is going to
    be a BACKWARDS INCOMPATIBLE RELEASE, to give you time to plan for
    updating, I'll fix a simple deadline of THIS FRIDAY as when 0.5
    will be released.

    As bla mentioned on irc, eepsite(I2P Site) hosts may want to take their site
    down on Thursday or Friday and keep them down until Saturday when
    many users will have upgraded.  This will help reduce the effect of
    an intersection attack (e.g. if 90% of the network has migrated to
    0.5 and you're still on 0.4, if someone reaches your eepsite(I2P Site), they
    know you're one of the 10% of routers left on the network).

    I could start to get into whats been updated in 0.5, but I'd end up
    going on for pages and pages, so perhaps I should just hold off and
    put that into the documentation which I should write up :)

    * 3) i2p-bt 0.1.7

    duck has put together a bugfix release to last week's 0.1.6 update,
    and word on the street says its kickass (perhaps /too/ kickass,
    given the increased network usage ;)  More info up @ the i2p-bt
    forum [2]

    [2] http://forum.i2p.net/viewtopic.php?t=300

    * 4) ???

    Lots of other things going on in the IRC discussions and on the
    forum [3], too much to briefly summarize.  Perhaps the interested
    parties can swing by the meeting and give us updates and thoughts?
    Anyway, see y'all shortly

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.2.4 (GNU/Linux)

    iD8DBQFCEl/OGnFL2th344YRAkZQAKC5A+M6tX01BKKplopedAqvpV0QZQCgy+C7
    Cbz/JT+3L2OfdhKAy8p/isQ=
    =VUm2
    -----END PGP SIGNATURE-----
:::
