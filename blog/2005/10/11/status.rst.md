::: {#i2p-status-notes-for-2005-10-11 .document}
# I2P STATUS NOTES FOR 2005-10-11 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, its tuesday again

    * Index
    1) 0.6.1.2
    2) I2PTunnelIRCClient
    3) Syndie
    4) I2Phex
    5) Stego and darknets (re: flamewar)
    5) ???

    * 1) 0.6.1.2

    Last week's 0.6.1.2 release has gone pretty well so far - 75% of the
    network has upgraded, HTTP POST is working fine, and the streaming
    lib is pushing data reasonably efficiently (the full response to an
    HTTP request is often received in a single end to end round trip).
    The network has also grown a bit - steady numbers look like 400-ish
    peers, though it bursted up a bit further to 6-700 with churn during
    the peak of the digg/gotroot [1] reference over the weekend.

    [1] http://gotroot.com/tiki-read_article.php?articleId=195
        (yeah, really old article, I know, but someone found it again)

    Since 0.6.1.2 came out, there has been even more good stuff added
    in - the cause of the recent irc2p netsplits has been found (and
    fixed), as have some pretty hefty improvements upon SSU's packet
    transmission (saving upwards of 5% of the packets).  I'm not sure
    exactly when 0.6.1.3 will come out, but maybe later this week.
    We'll see.

    * 2) I2PTunnelIRCClient

    The other day, after some discussion, dust whipped up a new extension
    to I2PTunnel - the "ircclient" proxy.  It works by filtering the
    content sent and received between the client and server over I2P, 
    stripping unsafe IRC messages and rewriting ones that should be
    adjusted.  After some testing, its looking quite good, and dust has
    contributed it to I2PTunnel and its now offered to people through the
    web interface.  Its been great that the irc2p folks have patched up
    their IRC servers to drop unsafe messages, but now we don't have to
    trust them to do so anymore - the local user has control over their
    own filtering.

    Using it is quite easy - instead of building a "Client proxy" for IRC
    as before, just build an "IRC proxy".  If you want to convert your 
    existing "Client proxy" to an "IRC proxy", you can (cringe) edit the
    i2ptunnel.config file, changing the "tunnel.1.type=client" to
    "tunnel.1.ircclient" (or whatever number is appropriate for your
    proxy).

    If things go well, this will be made the default I2PTunnel proxy type
    for IRC connections in the next release.

    Nice work dust, thanks!

    * 3) Syndie

    Ragnarok's scheduled syndication feature seems to be going well, and
    since 0.6.1.2 came out, there have been two new features coming
    forward - I've added in a new simplified CLI to post into Syndie [2],
    and dust (yay dust!) has whipped up some code to pull content out of
    an RSS/Atom feed, pull in any enclosures or images referenced in it,
    and convert the RSS content to SML (!!!) [3][4].

    The implications of these two together should be clear.  More news
    when there's more news.

    [2] http://syndiemedia.i2p/index.jsp?
               blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&
               entry=1128816000000&expand=true
    [3] http://syndiemedia.i2p/index.jsp?
               blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&
               entry=1128816000001&expand=true
    [4] http://dust.i2p/Sucker.java
        (we'll get it integrated into CVS soon enough)

    * 4) I2Phex

    Word on the street is that I2Phex is working pretty well, but that
    issues over time still persist.  There has been some discussion on
    the forum [5] regarding how to proceed, and GregorK, the lead 
    Phex dev, has even chimed in to voice support of integrating the
    I2Phex functionality back into Phex (or at least let the mainline
    Phex offer a simple plugin interface for the transport layer).

    This would be really quite kickass, as it'd mean much less code to
    maintain, plus we'd get the benefit of the Phex team's work on 
    improving the codebase.  However, for this to work, we need some 
    hackers to come forward and take charge of the migration.  The
    I2Phex code makes pretty clear where sirup changed things, so it
    shouldn't be too hard, but its probably not quite trivial either ;)

    I don't really have time to jump on this right now, but swing by
    the forum if you want to help.

    [5] http://forum.i2p.net/viewforum.php?f=25

    * 5) Stego and darknets (re: flamewar)

    The mailing list [6] has been pretty active as of late with the
    discussion regarding steganography and darknets.  The topic has
    moved largely over to the Freenet tech list [7] under the subject
    "I2P conspiracy theories flamewar", but its still ongoing.

    I'm not sure I have much to add that isn't part of the posts
    themselves, but some people have mentioned that the discussion has
    helped with their understanding of I2P and Freenet, so it might be
    worth browsing.  Or maybe not ;)

    [6] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html
    [7] nttp://news.gmane.org/gmane.network.freenet.technical

    * 6) ???

    As you can see, lots of exciting stuff going on, and I'm sure I've
    missed some things.  Swing on by #i2p in a few minutes for our 
    weekly meeting and say hey!

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFDTBeBWYfZ3rPnHH0RAncNAJ0YwUj/S1JvjWopGWZBR2+eT9hwHwCfRi2t
    pGTlS9rp+6WTthBLEZ07b2s=
    =rJ43
    -----END PGP SIGNATURE-----
:::
