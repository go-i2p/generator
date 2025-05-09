::: {#i2p-status-notes-for-2005-02-01 .document}
# I2P STATUS NOTES FOR 2005-02-01 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, weekly status time

    * Index
    1) 0.5 status
    2) nntp
    3) tech proposals
    4) ???

    * 1) 0.5 status

    There has been lots of progress on the 0.5 front, with a big batch
    of commits yesterday.  The bulk of the router now uses the new
    tunnel encryption and tunnel pooling [1], and it has been working
    well on the test network.  There are still some key pieces left to
    integrate, and the code is obviously not backwards compatible, but
    I'm hoping we can do some wider scale deployment sometime next week.

    As mentioned before, the initial 0.5 release will provide the
    foundation on which different tunnel peer selection/ordering
    strategies can operate.  We'll start with a basic set of
    configurable parameters for the exploratory and client pools, but
    later releases will probably include other options for different
    user profiles.

    [1]http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

    * 2) nntp

    As mentioned on LazyGuy's site [2] and my blog [3], we've got a new
    NNTP server up and running on the network, reachable at nntp.fr.i2p.
    While LazyGuy has fired up some suck [4] scripts to read in a few
    lists from gmane, the content is pretty much of, for, and by I2P
    users.  jdot, LazyGuy, and myself did some research into what
    newsreaders could be used safely, and there seem to be some pretty
    easy solutions.  See my blog for instructions on running slrn [5]
    to do anonymous newsreading and posting.

    [2] http://fr.i2p/
    [3] http://jrandom.dev.i2p/
    [4] http://freshmeat.net/projects/suck/
    [5] http://freshmeat.net/projects/slrn/

    * 3) tech proposals

    Orion and others have put up a series of RFCs for various tech
    issues up on ugha's wiki [6] to help flesh out some of the harder
    client and app level problems out there.  Please use that as the
    place to discuss naming issues, updates to SAM, swarming ideas, and
    the like - when you post up there, we can all collaborate at our own
    place to get a better result.

    [6] http://ugha.i2p/I2pRfc

    * 4) ???

    Thats all I have for the moment (good thing too, as the meeting
    starts momentarily).  As always, post up your thoughts whenever and
    wherever :)

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.2.4 (GNU/Linux)

    iD8DBQFB/+1+GnFL2th344YRAuF5AKDF/FzxzlKs25B2FRLsmC61KRQjlgCg/YjD
    kF6G0CoDu08TvpEtuzuzH9o=
    =ewBU
    -----END PGP SIGNATURE-----
:::
