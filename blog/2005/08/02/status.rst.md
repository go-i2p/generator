::: {#i2p-status-notes-for-2005-08-02 .document}
# I2P STATUS NOTES FOR 2005-08-02 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, belated notes today,

    * Index:
    1) 0.6 status
    2) PeerTest
    3) SSU introductions
    4) I2PTunnel web interface
    5) mnet over i2p
    6) ???

    * 1) 0.6 status

    As you've all seen, we pushed out the 0.6 release a few days ago, and
    on the whole, things have been going fairly well.  Some of the
    transport improvements since 0.5.* have exposed issues with the netDb
    implementation, but fixes for much of that is in testing now (as the
    0.6-1 build) and will be deployed as 0.6.0.1 fairly shortly.  We've
    also run into some problems with different NAT and firewall setups,
    as well as MTU issues with some users - issues that weren't present
    in the smaller test network due to fewer testers.  Workarounds have
    been added in for the worst offenders, but we've got a long term
    solution coming up soon - peer tests.

    * 2) PeerTest

    With 0.6.1, we're going to deploy a new system to collaboratively
    test and configure the public IPs and ports.  This is integrated
    within the core SSU protocol and will be backwards compatible.
    Essentially what it does is lets Alice ask Bob what her public IP
    and port number is, and then in turn have Bob get Charlie to confirm
    her proper configuration, or to find out what the limitation
    preventing properation is.  The technique is nothing new on the net,
    but is a new addition to the i2p codebase and should remove most
    common configuration error.

    * 3) SSU introductions

    As described in the SSU protocol spec, there is going to be
    functionality to let people behind firewalls and NATs participate
    fully in the network, even if they couldn't otherwise receive
    unsolicited UDP messages.  It won't work for all potential situations,
    but will address most.  There are similarities between the messages
    described in the SSU spec and the messages necessary for the PeerTest,
    so perhaps when the spec is be updated with those messages, we'll be
    able to piggyback the introductions with the PeerTest messages.  In
    any case, we'll deploy these introductions in 0.6.2, and that too will
    be backwards compatible.

    * 4) I2PTunnel web interface

    Some people have noticed and filed reports regarding various quirks
    on the I2PTunnel web interface, and smeghead has started putting
    together the fixes necessary - perhaps he can explain those updates
    in more detail, as well as an ETA on those?

    * 5) mnet over i2p

    While I haven't been around on the channel when the discussions were
    going on, from reading the logs it seems icepick has been doing some
    hacking to get mnet running on top of i2p - allowing the mnet
    distributed data store to offer resilient content publishing with
    anonymous operation.  I don't know too much about the progress on this
    front, but it sounds like icepick is making good progress tying in
    with I2P through SAM and twisted, but perhaps icepick can fill us in
    further?

    * 6) ???

    Ok, lots more going on than the above, but I'm already running late
    so I suppose I should stop typing and push this message out there.
    I'll be able to get online for a bit this evening, so if anyone is
    around we could have a meeting around 9:30p or so (whenever you get
    this ;) in #i2p on the usual irc servers {irc.duck.i2p, irc.postman.i2p,
    irc.freenode.net, irc.metropipe.net}.

    Thanks for your patience and help moving things forward!

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFC7+LCWYfZ3rPnHH0RAimUAJ9gMqGtl6huPkIkd8P1prbkSqrdpQCdF8L+
    jRueb/0QtxGouKlYVM6C1Ms=
    =LRI4
    -----END PGP SIGNATURE-----
:::
