::: {#i2p-status-notes-for-2005-03-08 .document}
# I2P STATUS NOTES FOR 2005-03-08 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, weekly update time

    * Index
    1) 0.5.0.2
    2) mail.i2p updates
    3) i2p-bt updates
    4) ???

    * 1) 0.5.0.2

    The other day we pushed out the 0.5.0.2 release and a good portion
    of the network has upgraded (yay!)  Reports are coming in that the
    worst offenders from 0.5.0.1 have been killed, and overall things
    seem to be working fine.  There are still some reliability issues,
    though the streaming lib has been handling it (irc connections
    lasting for 12-24+ hours seems the norm).  I've been trying to
    track down some of the issues remaining, but it would be really,
    really good if everyone got up to date ASAP.

    As things stand for moving forward, reliability is king.  Only after
    an overwhelming majority of messages that should succeed do succeed
    will there be work on improving throughput.  Beyond the batching
    tunnel preprocessor, another dimension we may want to explore is
    feeding more latency data into the profiles.  We currently only use
    test and tunnel management messages to determine each peer's "speed"
    ranking, but we should probably snag any measurable RTTs for other
    actions, such as netDb and even end to end client messages.  On the
    other hand, we'll have to weight them accordingly, since for an
    end to end message, we cannot separate the four portions of the
    measurable RTT (our outbound, their inbound, their outbound, our
    inbound).  Perhaps we can do some garlic trickery to bundle a
    message targetting one of our inbound tunnels along side some
    outbound messages, cutting the other side's tunnels out of the
    measurement loop.

    * 2) mail.i2p updates

    Ok, I don't know what updates postman has in store for us, but
    there'll be an update during the meeting.  See the logs to find
    out!

    * 3) i2p-bt update

    I don't know what updates duck & gang have for us, but I've heard
    some ruminations of progress on the channel.  Perhaps we can get
    an update out of 'im.

    * 4) ???

    Lots and lots going on, but if there's anything in particular y'all
    want to bring up and discuss, swing on by the meeting in a few
    minutes.  Oh, and just a reminder, if you haven't upgraded yet,
    please do so ASAP (upgrading is insanely simple - download a file,
    click a button)

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.2.4 (GNU/Linux)

    iD8DBQFCLgzVGnFL2th344YRAuY0AKCg03zFJBDbWYjV4jqd96gKtBhpFwCgwLLP
    EHsY9W9LztKK3FZBHPN2FyE=
    =QUzy
    -----END PGP SIGNATURE-----
:::
