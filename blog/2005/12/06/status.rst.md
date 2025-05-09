::: {#i2p-status-notes-for-2005-12-06 .document}
# I2P STATUS NOTES FOR 2005-12-06 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, 'tis tuesday again

    * Index
    1) 0.6.1.7 and net status
    2) Experimental tunnel failures
    3) SSU and NATs
    4) Syndie
    5) ???

    * 1) 0.6.1.7 and net status

    Last thursday brought out a new bugfix release of I2P, and with 70%
    of the network upgraded, it seems to have done the trick.  Some
    people are still getting high tunnel participation counts, but not
    as many as before.  Over the last few days we've also had a bit of a
    surge in new users, according to stats.i2p, though churn is still
    fairly high.  There have been some high load situations recently
    though, but that seems to be due to...

    * 2) Experimental tunnel failures

    zzz has been digging through the published stats and monitoring the
    local router, and we've got a pretty substantial tunnel creation
    failure rate, especially with longer tunnels.  According to zzz.i2p,
    that particular router is getting abysmal creation success - 3 hop
    exploratory tunnels are successfully built only 0.47% of the time,
    with 1 hop exploratory tunnels built successfully 7.5% of the time.
    There's some progress on a patch to the router up on that site too,
    and we'll hopefully be getting that into 0.6.1.8.

    The failure rate will hopefully be going away with 0.6.2, since
    we'll have that modified tunnel creation / crypto.  However, 0.6.2
    is currently on the back burner while performance is still being
    optimized.  However, the failure rate does have performance
    implications itself, so we may need to move forward in any case.
    I'm currently running some modified network load tests to determine
    the throttle point.  We'll see how things progress.

    * 3) SSU and NATs

    The other day bar posted [1] a discussion regarding what NAT
    topologies our SSU transport will deal with, and what we can do to
    get better results.  As bar states in the summary, the view that
    I2P outright doesn't support symmetric NATs isn't quite true, but,
    with care, we can support them in some careful situations.
    Hopefully we can continue to review how the SSU protocol and
    implementation can be enhanced to enable transparent operation for
    more users.

    [1] http://dev.i2p.net/pipermail/i2p/2005-December/001236.html

    * 4) Syndie

    There has been a lot of progress on Syndie lately, with much
    of the discussion going on within Syndie itself [2].  While progress
    continues regarding Syndie's threaded display, there's also some
    thoughts about the blog-like display, as well as a main entrypoint
    for an archive, such as with niceman's proposal [3].  I expect we'll
    see some progress on that front soon.

    Polecat has also been working on improving SML itself, and CofE has
    suggested some enhancements to allow multipage posts, so hopefully
    we'll get some of those in place too.  There has also been work on
    exporting the data in XML and XML/RDF, and a first pass of that is
    already implemented in CVS (see the history.txt for details [4]).
    It'd be great to use those to feed rich client apps for slick
    navigation and wysiwyg editing.

    I've also been putting together some tech details about how Syndie
    works, with two posts in Syndie so far [5].  There'll be more info
    posted later, of course.

    [2] http://syndiemedia.i2p.net/threads.jsp
    [3] http://syndiemedia.i2p.net/threads.jsp?
        post=OH18-lmBh6niM4~pXMLNcXsNXRG-uEVUujM5eRQDjyE=/1133568000001
    [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD
    [5] http://syndiemedia.i2p.net/threads?tags=syndie.doc

    * 5) ???

    There is lots going on, both within the core and the app level, and
    I'm leaving out some things that may not be ready for public
    consumption yet too.  But if people have things they'd like to
    discuss, swing on by the meeting in -10 minutes and get your rant
    on :)

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFDlfBhWYfZ3rPnHH0RAmauAJ9986/F1tWK4FSc60rnsU3Le3fV4gCdE6NC
    I52RW2XsrcEziJHHrihfBms=
    =3PMr
    -----END PGP SIGNATURE-----
:::
