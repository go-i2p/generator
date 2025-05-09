::: {#i2p-status-notes-for-2005-08-16 .document}
# I2P STATUS NOTES FOR 2005-08-16 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, brief notes today

    * Index:
    1) PeerTest status
    2) Irc2P
    3) Feedspace
    4) meta
    5) ???

    * 1) PeerTest status

    As mentioned before, the upcoming 0.6.1 release will include a series
    of tests to more carefully configure the router and to verify
    reachability (or point out what needs to be done), and while we've
    had some code in CVS for two builds now, there are still some
    refinements left before it'll work as smoothly as necessary.  At the
    moment, I'm making some slight modifications to the test flow
    documented [1] by adding in an additional packet to verify Charlie's
    reachability and delaying Bob's reply to Alice until Charlie has
    responded.  This should reduce the number of unnecessary "ERR-Reject"
    status values people see as Bob won't reply to Alice until he has a
    Charlie who is up for testing (and when Bob doesn't reply, Alice sees
    "Unknown" as the status).

    [1]http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html#peerTesting

    Anyway, yeah, thats that - there should be a 0.6.0.2-3 out tomorrow,
    pushed as a release when its thoroughly tested.

    * 2) Irc2P

    As mentioned on the forum [2], I2P users who use IRC need to update
    their configuration to switch over to the new IRC network.  Duck will
    be going offline temporarily to [redacted], and rather than hope the
    server doesn't have any trouble during that time, postman and smeghead
    have stepped up and built a new IRC network for your use.  Postman
    has also mirrored duck's tracker and i2p-bt site at [3], and I think
    I saw something on the new IRC network about susi firing up a new
    IdleRPG instance (check the channel list for more info).

    My thanks go out to those responsible for the old i2pirc network
    (duck, baffled, the metropipe crew, postman) and to those responsible
    for the new irc2p network (postman, arcturus)!  Interesting services
    and content make I2P worthwhile, and its up to y'all to create 'em!

    [2]http://forum.i2p.net/viewtopic.php?t=898
    [3]http://hq.postman.i2p/

    * 3) Feedspace

    Speaking of which, I was reading through frosk's blog the other day
    and it seems there's some more progress on Feedspace - in particular,
    on a nice lil' GUI.  I know it might not be ready to test yet, but
    I'm sure frosk'll bounce some code our way when its time.  As an
    aside, I've also heard a rumor about another anonymity-aware web
    based blogging tool in the pipeline which'll be able to tie into
    Feedspace when its ready, but again, I'm sure we'll hear more info on
    that when its ready.

    * 4) meta

    Being the greedy bastard that I am, I'd like to move the meetings up
    a bit - instead of 9PM GMT, lets try 8PM GMT.  Why?  Because it fits
    my schedule better ;) (the closest net cafes aren't open too late).

    * 5) ???

    Thats about it for the moment - I'm going to try to be near a net cafe
    for tonight's meeting, so feel free to swing on by #i2p at *8*P GMT on
    the /new/ irc servers {irc.postman.i2p, irc.arcturus.i2p}.  We may
    have a changate bot up to irc.freenode.net - anyone want to run one?

    ciao,
    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFDAkp7WYfZ3rPnHH0RAmuLAJ0WbbJcJ1X4KATSnPaFc112SLoJ0wCfc2Mj
    ZA7O66ghsqwxy4dcVh9e4Hg=
    =5cav
    -----END PGP SIGNATURE-----
:::
