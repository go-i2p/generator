::: {#i2p-status-notes-for-2005-01-11 .document}
# I2P STATUS NOTES FOR 2005-01-11 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, time for the weekly update

    * Index
    1) Net status
    2) 0.5 progress
    3) 0.6 status
    4) azneti2p
    5) fbsd
    6) hosts.txt as WoT
    7) ???

    * 1) Net status

    Overall the net is handling itself well, though we had some problems
    with one of the irc servers being offline and my outproxy acting up.
    However, the other irc server was (and still is) around (though at
    the moment doesn't have CTCP disabled - see [1]), so we were able to
    satiate our need for irc :)

    [1] http://ugha.i2p/HowTo/IrcAnonymityGuide

    * 2) 0.5 progress

    There's progress, ever onwards!  Ok, I suppose I should get into a
    little more detail than that.  I've finally got the new tunnel
    routing crypto implemented and tested (yay!), but during some
    discussions we found a place where there could be one level of
    anonymity leak, so its being revised (the first hop would have
    known they were the first hop, which is Bad.  but really really
    easy to fix).  Anyway, I hope to get the docs and code on that
    updated and posted soon, and docs on the rest of the 0.5 tunnel
    operation / pooling / etc posted later.  More news when there's
    more news.

    * 3) 0.6 status

    (what!?)

    Mule has begun investigations into the UDP transport, and we've
    been mining zab for his experiences with limewire's UDP code.
    Its all very promising, but much work to be done (and still
    several months out on the roadmap [2]).  Got some inspiration or
    suggestions?  Get involved and help focus it towards what needs to
    be done!

    [2] http://www.i2p.net/roadmap#0.6

    * 4) azneti2p

    I almost wet my pants when I got the info, but it looks like the
    folks at azureus have written up an I2P plugin, allowing both
    anonymous tracker usage and anonymous data comm!  Multiple
    torrents work within a single I2P destination too, and it uses
    the I2PSocket directly, allowing tight integration with the
    streaming lib.  The azneti2p plugin is still in the early stages
    with this 0.1 release, and there are lots of optimizations and ease
    of use improvements coming down the pipe, but if you're up for
    getting your hands dirty, swing by i2p-bt on the i2p irc networks
    and get in on the fun :)

    For the adventurus types, get the latest azureus [3], check their
    i2p howto [4], and snag the plugin [5].

    [3] http://azureus.sourceforge.net/index_CVS.php
    [4] http://azureus.sourceforge.net/doc/AnonBT/i2p/I2P_howto.htm
    [5] http://azureus.sourceforge.net/plugin_details.php?plugin=azneti2p

    duck has been taking heroic measures to keep compatability with
    i2p-bt, and there is frantic hacking in #i2p-bt as I type this, so
    keep an eye out for a new i2p-bt release Real Soon Now.

    * 5) fbsd

    Thanks to the work of lioux, there's now a freebsd ports entry for
    i2p [6].  While we aren't really looking to have lots of
    distro-specific installs out there, he promises to keep it updated
    when we give sufficient notice for new release.  This should be
    helpful for fbsd-current folks - thanks lioux!

    [6] http://www.freshports.org/net/i2p/

    * 6) hosts.txt as WoT

    Now that the 0.4.2.6 release has bundled in Ragnarok's addressbook,
    the process of keeping your hosts.txt populated with new entries is
    in every user's control.  Not only that, but you can view the
    addressbook subscriptions as a poor-man's web of trust - you import
    new entries from a site you trust to introduce you to new
    destinations (defaults being dev.i2p and duck.i2p).

    With this capacity comes a whole new dimension - the ability for
    people to choose what sites to essentially link to in their
    hosts.txt and which ones not to.  While there is a place for the
    public free-for-all that has occurred in the past, now that the
    naming system is not just in theory but in practice fully
    distributed, people will need to figure out their own policies on
    publishing other people's destinations.

    The important part behind the scenes here is that this is a learning
    opportunity for the I2P community.  Before, both gott and I were
    trying to help push the naming issue by publishing gott's site as
    jrandom.i2p (he asked for that site first - I did not, and have no
    control whatsoever as to the contents of that URL).  Now we may
    begin to explore how we are going to deal with sites not listed in
    the http://dev.i2p.net/i2p/hosts.txt or on forum.i2p.  Not being
    posted on those locations doesn't prevent in any way a site from
    operating - your hosts.txt is just your local address book.

    Anyway, enough babbling, I just wanted to put people on notice so
    we can all see what is to be done.

    * 7) ???

    Yowza, thats a lot of stuff.  Busy week, and I don't forsee things
    slowing down anytime soon.  So, swing on by the meeting in a few
    minutes and we can talk about stuff.

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.2.4 (GNU/Linux)

    iD8DBQFB5D2EGnFL2th344YRAoMnAJsHxgRyB3eydlqKiCy54CYzRCEbsQCfRWV0
    ItUMfG4sTnmRKk5m2u9Yxjg=
    =cJJx
    -----END PGP SIGNATURE-----
:::
