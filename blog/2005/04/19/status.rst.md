::: {#i2p-status-notes-for-2005-04-19 .document}
# I2P STATUS NOTES FOR 2005-04-19 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, its that time of the week again,

    * Index
    1) Net status
    2) SSU status
    3) Roadmap update
    4) Q status
    5) ???

    * 1) Net status

    Over the nearly two weeks since 0.5.0.6 came out, things have been
    mostly positive, though service providers (eepsites(I2P Sites), ircd, etc) have
    been running into some bugs as of late.  While clients are in good
    shape, over time a server may run into situation where failing
    tunnels can trigger some excessive throttling code, preventing
    proper rebuilding and publication of the leaseSet.

    There have been some fixes in CVS, among other things, and I expect
    that we'll have a new 0.5.0.7 out in the next day or so.

    * 2) SSU status

    For those not following my (oh so exciting) blog, there's been a lot
    of progress with the UDP transport, and right now its fairly safe to
    say that the UDP transport will not be our throughput bottleneck :)
    While debugging that code, I've taken the opportunity to work
    through the queueing at higher levels as well, finding points where
    we can remove unnecessary choke points.  As I said last week,
    though, there's still a lot of work to do.  More info will be
    available when there's more info available.

    * 3) Roadmap update

    Its april now, so the roadmap [1] has been updated accordingly -
    dropping 0.5.1 and shifting some dates.  The big change there is
    moving 0.6 from April to June, though that really isn't as big of a
    change as it looks like.  As I mentioned last week, my own schedule
    has moved around a bit, and rather than moving to $somewhere in
    June, I'm moving to $somewhere in May.  While we could have whats
    necessary for 0.6 ready this month, there is no way I'm going to
    shove out a major update like that and then dissapear for a month,
    since the reality of software is that there'll be bugs not caught
    in testing.

    [1] http://www.i2p.net/roadmap

    * 4) Q status

    Aum has been going wild on Q, putting in more goodies for us, with
    the latest screenshots up on his site [2].  He has also committed
    the code to CVS too (yay), so we'll hopefully be able to begin alpha
    testing soon.  I'm sure we'll hear more from aum with details on how
    to help, or you can dig into the goods in CVS at i2p/apps/q/

    [2] http://aum.i2p/q/

    * 5) ???

    There has been lots more going on as well, with some lively
    discussions on the mailing list, the forum, and irc.  I'm not
    going to try to summarize those here, since there are only a few
    minutes until the meeting, but swing on by if there's something not
    discussed that you want to bring up!

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.2.4 (GNU/Linux)

    iD8DBQFCZWKUWYfZ3rPnHH0RArKcAJ0dGCGnQhNu7dvncvPRdOqYe3Q5MQCfcz9X
    T3H2xh74GXTtBdOloaAHS9o=
    =iRwf
    -----END PGP SIGNATURE-----
:::
