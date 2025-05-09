::: {#i2p-status-notes-for-2005-07-12 .document}
# I2P STATUS NOTES FOR 2005-07-12 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, its that time of the week again

    * Index
    1) squid/www/cvs/dev.i2p restored
    2) SSU testing
    3) I2CP crypto
    4) ???

    * 1) squid/www/cvs/dev.i2p restored

    After bashing my head on several colo boxes, some of the old services
    have been restored - squid.i2p (one of the two default outproxies),
    www.i2p (a secure pointer to www.i2p.net), dev.i2p (a secure
    pointer to dev.i2p.net, where the mailing list archives, cvsweb, and
    default netDb seeds are found), and cvs.i2p (a secure pointer to our
    CVS server - cvs.i2p.net:2401).  My blog is still awol, but its
    content was lost anyway so there'll need to be a fresh start sooner
    or later.  Now that these services are back online reliably, its
    time to move on to the...

    * 2) SSU testing

    As mentioned in that little yellow box on everyone's router console,
    we've begun the next round of live network testing for SSU.  The
    tests are not for everyone, but if you're adventurous and are
    comfortable doing some manual configuration, check out the details
    referenced on your router console (http://localhost:7657/index.jsp).
    There may be several rounds of testing, but I don't forsee any major
    changes to SSU prior to the 0.6 release (0.6.1 will add support for
    those who cannot forward their ports or otherwise receive inbound
    UDP connections).

    * 3) I2CP crypto

    While working over the new introductory docs again, I'm having a bit
    of trouble justifying the additional layer of encryption done within
    the I2CP SDK.  The original intent of the I2CP crypto layer was to
    provide a baseline end to end protection of the messages transmitted,
    as well as to allow I2CP clients (aka I2PTunnel, the SAM bridge,
    I2Phex, azneti2p, etc) to communicate through untrusted routers.  As
    the implementation progressed however, the I2CP layer's end to end
    protection has become redundant, as all client messages are end to
    end encrypted inside garlic messages by the router, bundling the
    sender's leaseSet and sometimes a delivery status message.  This
    garlic layer already provides end to end encryption from the sender's
    router to the receiver's router - the only difference is that it
    doesn't protect against that router itself being hostile.

    Looking at the forseable use cases however, I can't seem to come up
    with a valid scenario where the local router wouldn't be trusted.
    At the very least, the I2CP crypto only hides the content of the
    message transmitted from the router - the router still needs to know
    to what destination it should be sent.  If necessary, we can add an
    SSH/SSL I2CP listener to allow the I2CP client and the router to
    operate on separate machines, or people who need such situations can
    use existing tunnelling tools.

    Just to reiterate the crypto layering used right now, we have:
     * I2CP's end to end ElGamal/AES+SessionTag layer, encrypting from
       the sender's destination to the recipient's destination.
     * The router's end to end garlic encryption layer
       (ElGamal/AES+SessionTag), encrypting from the sender's router to
       the recipient's router.
     * The tunnel encryption layer for both the inbound and outbound
       tunnels at the hops along each (but not between the outbound
       endpoint and the inbound gateway).
     * The transport encryption layer between each router.

    I want to be fairly cautious about dropping one of those layers, but
    I don't want to waste our resources doing unnecessary work.  What
    I'm proposing is dropping that first I2CP encryption layer (but
    still of course keeping the authentication used during I2CP session
    establishment, leaseSet authorization, and sender authentication).
    Can anyone come up with a reason why we should keep it?

    * 4) ???

    Thats about it for the moment, but lots going on as always.  Still
    no meeting this week, but if someone has something to bring up,
    please don't hesitate to post it on the list or on the forum.  Also,
    while I do read the scrollback in #i2p, general questions or
    concerns should be sent to the list instead so that more people can
    participate in the discussion.

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFC0//0WYfZ3rPnHH0RAs5TAJ9I+yigdzSY8SnLOZS+fNSJ1s/WpwCffzxH
    gB0FYFO3bKRemtBoB1JNyLM=
    =Qbug
    -----END PGP SIGNATURE-----
:::
