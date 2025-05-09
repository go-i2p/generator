::: {#i2p-status-notes-for-2005-07-05 .document}
# I2P STATUS NOTES FOR 2005-07-05 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi gang, its that time of the week,

    * Index
    1) Dev status
    2) Tunnel IVs
    3) SSU MACs
    3) ???

    * 1) Dev status

    Another week, another message saying "There's been a lot of progress
    on the SSU transport" ;)  My local mods are stable and have been
    pushed to CVS (HEAD sits at 0.5.0.7-9), but no release yet.  More
    news on that front soon.  Details on the non-SSU related changes up
    in the history [1], though I'm keeping SSU related changes out of
    that list so far, since SSU isn't used by any non-devs yet (and devs
    read i2p-cvs@ :)

    [1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

    * 2) Tunnel IVs

    For the last few days, dvorak has been posting occational thoughts
    on different ways to attack the tunnel crypto, and while most of
    them were already addressed, we were able to come up with one
    scenario that would allow participants to tag a pair of messages to
    determine that they're in the same tunnel.  The way it worked was
    the earlier peer would let a message go past it and then later on
    swap the IV and first data block from that first tunnel message and
    place it in a new one.  This new one would of course be corrupt, but
    it wouldn't look like a replay, since the IVs were different.  Down
    the line, the second peer could then just discard that message so
    that the tunnel endpoint couldn't detect the attack.

    One of the core issues behind it is that there are no ways to verify
    a tunnel message as goes down the tunnel without opening up a whole
    slew of attacks (see an earlier tunnel crypto proposal [2] for one
    method that gets close, but has pretty sketchy probabilities and
    imposes some artificial limits on the tunnels).

    [2]http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel.html?rev=HEAD

    There is, however, a trivial way around the particular attack
    outlined - simply treat xor(IV, first data block) as the unique
    identifier fed through the bloom filter instead of the IV alone.
    This way, intermediate peers will see the dup and drop it before it
    reaches the second colluding peer.  CVS has been updated to include
    this defense, though I very, very much doubt its a practical threat
    given the current network size, so I'm not pushing it out as a
    release by itself.

    This doesn't affect the viability of other timing or shaping attacks
    however, but its best to clear up the easy to handle attacks when we
    see 'em.

    * 3) SSU MACs

    As described in the spec [3], the SSU transport uses a MAC for each
    datagram transmitted.  This is in addition to the verification hash
    sent with each I2NP message (as well as the end to end verification
    hashes on client messages).  Right now, the spec and the code uses a
    truncated HMAC-SHA256 - transmitting and verifying only the first
    16 bytes of the MAC.  This is *cough* a bit wasteful, as the HMAC
    uses the SHA256 hash twice in its operation, each time running with
    a 32 byte hash, and recent profiling of the SSU transport suggests
    this is near the critical path for CPU load.  As such, I've done a
    little exploring with replacing HMAC-SHA256-128 with a plain
    HMAC-MD5(-128) - while MD5 is clearly not as strong as SHA256, we're
    truncating the SHA256 down to the same size as MD5 anyway so the
    amount of brute force required for collision is the same (2^64
    attempts).  I'm playing around with it at the moment and the speedup
    is substantial (getting more than 3x the HMAC throughput on 2KB
    packets than with SHA256), so perhaps we may go live with that
    instead.  Or if someone can come up with a great reason not to (or
    a better alternative), its simple enough to switch out (just one
    line of code).

    [3]http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

    * 4) ???

    Thats about it for the moment, and as always, feel free to post up
    your thoughts and concerns whenever.  CVS HEAD is now buildable
    again for those without junit installed (for the moment I've pulled
    the tests out of i2p.jar, but still runnable with the test ant
    target), and I expect there'll be more news about 0.6 testing fairly
    soon (I'm still battling with the oddities of the colo box at the
    moment - telnetting to my own interfaces fail locally (with no
    useful errno), work remotely, all without any iptables or other
    filters.  joy).  I still don't have net access @ home, so won't be
    around for a meeting tonight, but perhaps next week.

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFCyr3uWYfZ3rPnHH0RAjwFAJ4pZ+icnR8MioHxrCjVPfFG2a/9KgCdEQBc
    p1RmRcbFNI8vA+qVwFGVFT4=
    =HJHn
    -----END PGP SIGNATURE-----
:::
