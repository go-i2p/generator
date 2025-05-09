::: {#i2p-status-notes-for-2005-03-15 .document}
# I2P STATUS NOTES FOR 2005-03-15 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, weekly update time

    * Index
    1) Net status
    2) Feedspace
    3) ???

    * 1) Net status

    Over the last week, much of my time has been spent analyzing the
    network's behavior, tracking stats and trying to reproduce various
    events in the simulator.  While some of the funky network behavior
    can be attributed to the two dozen or so routers still on older
    versions, the key factor is that our speed calculations aren't
    giving us good data - we aren't able to properly identify peers who
    can pump data quickly.  In the past, this wasn't much of a problem,
    since there was a bug causing us to use the 8 highest capacity peers
    as the 'fast' pool, rather than building legitimate capacity derived
    tiers.  Our current speed calculation is derived from a periodic
    latency test (the RTT of a tunnel test, in particular), but that
    provides insufficient data to have any confidence in the value.
    What we need is a better way to gather more data points while still
    allowing 'high capacity' peers to be promoted to the 'fast' tier, as
    necessary.

    To verify that this is the key problem we're facing, I cheated a bit
    and added functionality to manually select what peers should be used
    in a particular tunnel pool's selection.  With those explicitly
    chosen peers, I've had over two days on irc without disconnect and
    fairly reasonable performance w/ another service I control.  For the
    last two days or so, I've been trying out a new speed calculator
    using some new stats, and while it has improved selection, it still
    has some problems.  I've worked through a few alternatives this
    afternoon, but there's still work to be done to try 'em out on the
    net.

    * 2) Feedspace

    Frosk has put up another rev of the i2pcontent/fusenet docs, except
    now at a new home with a new name: http://feedspace.i2p/ - see
    either orion [1] or my blog [2] for the destination.  This stuff
    looks really promising, both from the perspective of "hey, kickass
    functionality" and "hey, that'll help I2P's anonymity".  Frosk and
    gang are working away, but they're most certainly looking for input
    (and help).  Perhaps we can get Frosk to give us an update in the
    meeting?

    [1] http://orion.i2p/#feedspace.i2p
    [2] http://jrandom.dev.i2p/

    * 3) ???

    Ok, it may not look like much, but there's lots going on, really :)
    I'm sure I've missed some things too, so swing on by the meeting
    and see whats up.

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.2.4 (GNU/Linux)

    iD8DBQFCN0wvGnFL2th344YRAvQbAKDT3rvYHcqAwuFyNEjW4WhRWgjucwCg4Z4S
    mvxKNX+jQ7jnfBFyJponyCc=
    =NMuv
    -----END PGP SIGNATURE-----
:::
