::: {#i2p-status-notes-for-2005-09-13 .document}
# I2P STATUS NOTES FOR 2005-09-13 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, time for the weekly status notes

    * Index
    1) Net status
    2) SSU introductions / NAT hole punching
    3) Bounties
    4) Client app directions
    5) ???

    * 1) Net status

    We're still churning along with the 0.6.0.5 release on the net, and
    nearly everyone has upgraded, with many running one of the builds
    since then (CVS HEAD is 0.6.0.5-9 right now).  Things are still
    working well on the whole, though there has been a substantial
    increase in network traffic from what I've observed, likely due to
    more i2p-bt or i2phex usage.  Once of the irc servers had a bit of
    a bump last night, but the other held on fine and things seem to
    have recovered well.  There have been substantial improvements in
    error handling and other features in the CVS builds however, so I
    expect we'll have a new release later this week.

    * 2) SSU introductions / NAT hole punching

    The latest builds in CVS include support for the long discussed SSU
    introductions [1], allowing us to perform decentralized NAT hole
    punching for users behind a NAT or firewall that they do not control.
    While it doesn't handle symmetric NAT, it does cover a majority of
    cases out there.  Reports from the field are good, though only
    users with the latest builds can contact the NATted users - older
    builds need to wait for the user to contact them first.  Because of
    this, we'll be pushing the code out into a release earlier than
    usual to reduce the amount of time that we have these restricted
    routes in place.

    [1]http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#introduction

    * 3) Bounties

    I was checking the i2p-cvs mailing list earlier and noticed a bunch
    of commits from Comwiz regarding what seems to be phase 3 of the
    unit test bounty [2].  Perhaps Comwiz can give us a status update on
    that stuff during the meeting tonight.

    [2]http://www.i2p.net/bounty_unittests

    As an aside, thanks to the suggestion of an anonymous person, I've
    updated the hall of fame [3] a bit, including the contribution dates,
    bundling multiple donations from a single person together, and
    converting to a single currency.  Thanks again to everyone who has
    contributed, and if there is incorrect information posted or if
    something is missing, please get in touch and it will be updated.

    [3]http://www.i2p.net/halloffame

    * 4) Client app directions

    One of the more recent adjustments in the current CVS builds is the
    removal of the old mode=guaranteed form of delivery.  I hadn't
    realized anyone still used it (and its entirely unnecessary, since
    we've had the full streaming lib for a year now), but when I was
    digging into i2phex I noticed that flag set.  With the current build
    (and all subsequent releases), i2phex will just use mode=best_effort,
    which will hopefully improve its performance.

    My point in bringing this up (beyond mentioning it for i2phex users)
    is to ask what y'all need on the client side of I2P, and whether some
    of my time should be allocated to helping meet some of them.  Off the
    top of my head, I can see lots of work available in different aspects:
     = Syndie: simplified posting, automated synchronization, data
       import, app integration (with i2p-bt, susimail, i2phex, etc),
       threading support to allow forum-like behavior, and more.
     = eepproxy: improved throughput, pipelining support
     = i2phex: general maintenance (I haven't used it enough to know its
       pain points)
     = irc: improved resiliance, detect recurring irc server downtime and
       avoid down servers, filter CTCP actions locally instead of on the
       server, DCC proxy
     = Improved x64 support with jbigi, jcpuid, and the service wrapper
     = systray integration, and removing that dos box
     = Improved bandwidth controls for bursting
     = Improved congestion control for network and CPU overload, as well
       as recovery.
     = Expose more functionality and document the available features of
       the router console to third party apps
     = Client developer docs
     = I2P intro docs

    Plus, beyond all of that, there's the rest of the stuff on the
    roadmap [4] and todo list [5].  I know what we need technically, but
    I don't know what *you* need from a user perspective.  Talk to me,
    whatcha want?

    [4]http://www.i2p.net/roadmap
    [5]http://www.i2p.net/todo

    * 5) ???

    There's some other stuff going on in the router core and app dev
    side beyond whats mentioned above, but not everything is ready for
    consumption at the moment.  If anyone has anything they'd to bring
    up, swing on by the meeting tonight at 8p UTC in #i2p!

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFDJ0DaWYfZ3rPnHH0RAppoAJsET7gG7oEtdIrnJLRBfDEYxj3B0gCfZ1+M
    PVtD2O9r3Xk4yT8r3UWD45E=
    =eh+T
    -----END PGP SIGNATURE-----
:::
