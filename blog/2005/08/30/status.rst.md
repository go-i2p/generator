::: {#i2p-status-notes-for-2005-08-30 .document}
# I2P STATUS NOTES FOR 2005-08-30 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, its that time of the week again

    * Index
    1) Net status
    2) floodfill netDb
    3) Syndie
    4) ???

    * 1) Net status

    With 0.6.0.3 out for a week, the reports are pretty good, though the
    logging and display has been pretty confusing for some.  As of a few
    minutes ago, I2P is reporting that a substantial number of people
    have misconfigured their NATs or firewalls though - out of 241 peers,
    41 have seen the status go to ERR-Reject, while 200 have been
    straight OK (when they can get an explicit status).  This is not
    good, but it has helped focus what needs to be done a bit further.

    Since the release, there have been a few bugfixes for long standing
    error conditions, bringing the current CVS HEAD up to 0.6.0.3-4,
    which will likely be pushed out as 0.6.0.4 later this week.

    * 2) floodfill netDb

    As discussed [1] in my blog [2], we're trying out a new backwards
    compatible netDb which will address both the restricted route
    situation we're seeing (20% of the routers) and simplify things a
    bit.  The floodfill netDb is deployed as part of 0.6.0.3-4 without
    any further configuration, and basically works by querying within
    the floodfill db before falling back onto the existing kademlia
    db.  If a few people want to help try it out, swing on up to
    0.6.0.3-4 and give 'er a whirl!

    [1]http://syndiemedia.i2p.net/index.jsp?selector=entry://ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1125100800001
    [2]http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

    * 3) Syndie

    Syndie development is progressing quite well, with the full remote
    syndication in operation and optimized for I2P's needs (minimizing
    the number of HTTP requests, instead bundling results and uploads in
    multipart HTTP posts).  The new remote syndication means you can run
    your own local Syndie instance, reading and posting offline, and
    then later on, sync your Syndie with someone else's - pulling down
    any new posts and pushing up any locally created posts (either in
    bulk, by blog, or by post).

    One public Syndie site is syndiemedia.i2p (also reachable on the web
    at http://syndiemedia.i2p.net/) with its public archives reachable
    at http://syndiemedia.i2p/archive/archive.txt (point your Syndie node
    at that to sync it).  The 'front page' on that syndiemedia has been
    filtered to include only my blog, by default, but you can still
    access the other blogs through the drop down and adjust your default
    accordingly.  (over time, syndiemedia.i2p's default will change to
    a set of introductory posts and blogs, giving a good entry point
    into syndie).

    One effort still underway is the internationalization of the Syndie
    codebase.  I've got my local copy modified to work properly with any
    content (any character set / locale / etc) on any machine (with
    potentially differing character sets / locale / etc), serving up the
    data clean so that the user's browser can interpret it properly.  I
    have run into problems with one Jetty component that Syndie uses
    though, as their class for dealing with internationalized multipart
    requests isn't character set conscious.  Yet ;)

    Anyway, that means that once the internationalization part is
    sorted, content and blogs will be renderable and editable across all
    languages (but not translated, of course, yet).  Until then though,
    content created may get b0rked once the internationalization is
    finished (since there are UTF-8 strings inside the signed content
    areas).  But stil, feel free to hack around, and hopefully I'll get
    things finished tonight or tomorrow sometime.

    Also, some ideas still on the horizon for SML [3] include a
    [torrent attachment="1"]my file[/torrent] tag which would offer a
    one click way to let people fire off the attached torrent in their
    favorite BT client (susibt, i2p-bt, azneti2p, or even a non-i2p bt
    client).  Is there demand for other sorts of hooks (e.g. an [ed2k]
    tag?), or do people have entirely different crazy ideas for pushing
    content in Syndie?

    [3]http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1124496000000

    * 4) ???

    Anyway, lots and lots going on, so swing by the meeting in 10 minutes
    on irc://irc.{postman,arcturus,freshcoffee}.i2p/#i2p or freenode.net!

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFDFNUWWYfZ3rPnHH0RAoiaAJkB3QXi6PQ7ATzQc3bq6gQHYO8IqACdGVet
    omzf6cHV9GW3oBCkAHg7gns=
    =6X2N
    -----END PGP SIGNATURE-----
:::
