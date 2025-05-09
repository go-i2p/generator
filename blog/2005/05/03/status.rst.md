::: {#i2p-status-notes-for-2005-05-03 .document}
# I2P STATUS NOTES FOR 2005-05-03 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, lots of stuff on the table this week

    * Index
    1) Net status
    2) SSU status
    3) i2phex
    4) awol
    5) ???

    * 1) Net status

    No big changes on the overall network health - things seem fairly
    stable, and though we've got the occational bump services seem to be
    doing well.  There have been lots of updates to CVS since the last
    release but no show stopper bug fixes.  We may have one more release
    before my move, just to get the latest CVS out further, but I'm not
    sure yet.

    * 2) SSU status

    Are you tired of hearing me say that there's been lots of progress
    on the UDP transport?  Well, too bad - there's been lots of progress
    on the UDP transport.  Over the weekend we moved off the private
    network testing and onto the live net and a dozen or so routers
    upgraded and exposed their SSU address - allowing them to be
    reachable by the TCP transport by most users but letting SSU enabled
    routers to talk via UDP.

    The testing still very early, but it went much better than I
    expected.  Congestion control was very well behaved and both
    throughput and latency were quite sufficient - it was able to
    properly identify real bandwidth limits and effectively share that
    link with competing TCP streams.

    With the stats gathered from the helpful volunteers, it became clear
    how important the selective acknowledgement code is to proper
    operation in highly congested networks.  I've spent the last few
    days implementing and testing that code, and have updated the SSU
    spec [1] to include a new efficient SACK technique.  It won't be
    backwards compatible with the earlier SSU code, so people who have
    been helping test should disable the SSU transport until a new build
    is ready for testing (hopefully in the next day or two).

    [1]http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

    * 3) i2phex

    sirup has been churning away on a port of phex to i2p, and while
    there's a lot of work to do before its ready for joe sixpack,
    earlier this evening I was able to fire it up, browse sirup's shared
    files, grab some data, and use its *cough* "instant" chat interface.

    There's lots more info up on sirup's eepsite(I2P Site) [2], and help testing
    by people already in the i2p community would be great (though
    please, until sirup blesses it as a public release, and i2p is at
    least 0.6 if not 1.0, lets keep it within the i2p community).  I
    believe sirup will be around for this week's meeting, so perhaps we
    can get some more info then!

    [2]http://sirup.i2p/

    * 4) awol

    Speaking of being around, I probably won't be here for next week's
    meeting and will be offline for the following 3-4 weeks.  While that
    probably means there won't be any new releases, there are still a
    bunch of really interesting things for people to hack on:
     = applications like feedspace, i2p-bt/ducktorrent, i2phex, fire2pe,
        the addressbook, susimail, q, or something completely new.
     = the eepproxy - it'd be great to get filtering, support for
        persistent HTTP connections, 'listen on' ACLs, and perhaps an
        exponential backoff to deal with outproxy timeouts (rather than
        plain round robin)
     = the PRNG (as discussed on the list)
     = a PMTU library (either in Java or in C with JNI)
     = the unit test bounty and the GCJ bounty
     = router memory profiling and tuning
     = and a whole lot more.

    So, if you're feeling bored and want to help out, but are in need of
    inspiration, perhaps one of the above might get you going.  I'll
    probably stop by a net cafe every once in a while, so I'll be
    reachable through email, but the response time will be O(days).

    * 5) ???

    Ok, thats about all I've got to bring up for the moment.  For those
    who want to help out with the SSU testing over the next week, keep
    an eye out for info on my blog [3].  For the rest of y'all, I'll see
    you at the meeting!

    =jr
    [3]http://jrandom.dev.i2p/
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.2.4 (GNU/Linux)

    iD8DBQFCd81nWYfZ3rPnHH0RAuoTAJ0VhtNJjYB7sv0XecoCCBvz63z/GACfasKz
    vJ2B+nJiHEMLwobhZIRS2hQ=
    =E3vU
    -----END PGP SIGNATURE-----
:::
