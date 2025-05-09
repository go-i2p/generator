::: {#i2p-status-notes-for-2005-12-20 .document}
# I2P STATUS NOTES FOR 2005-12-20 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, time for our weekly pre-meeting status update

    * Index
    1) Net status
    2) I2PSnark updates
    3) Syndie blog UI
    4) ???

    * 1) Net status

    There haven't been many changes in the past week regarding network
    status, since no major updates have been rolled out.  Some people
    are still experiencing an increase in irc disconnects (with sessions
    lasting only a few hours) while others are having multiday sessions.
    It has almost been three weeks since the last release though, and
    zzz's tunnel creation updates seem to be helping out, so we'll
    probably have a new release out in the next few days.  That release
    will probably not yet include changes based on the lessons being
    learnt from the ongoing load testing, however (since I don't want to
    hold up the release too long).

    2) I2PSnark updates

    In the past week, I've added in multitorrent support to snark and
    strapped a simple web interface on top of it.  Reports from beta
    testers are fairly positive, but there is still some debugging left
    to be done, since snark wasn't originally designed to continue
    running after a particular torrent was stopped (and, in turn, relied
    upon the JVM to shut down, releasing held resources).  Its also
    fairly memory intensive when actively participating in swarms
    (holding pieces in memory rather than keeping data entirely on disk,
    etc).  This means heavy I2PSnark users will likely want to increase
    their JVM's maximum heap size, or alternately, use a standalone JVM
    for their I2PSnark usage.

    There's a standalone I2PSnark build in CVS right now - pull the
    latest and run:
      ant i2psnark
      cp i2psnark-standalone.zip /some/directory
      cd /some/directory ; unzip i2psnark-standalone.zip ; cd i2psnark
      java -jar launch-i2psnark.jar & 
      lynx http://localhost:8002/

    I'll bundle the necessary scripts in with the new release to
    automate that as well, so users with normal I2P installs can just
    run I2PSnark standalone with as little hassle as possible.

    3) Syndie blog UI

    As mentioned last week, there have been some improvements to the 
    Syndie blog UI in the latest CVS.  There's a new page that offers
    two different summaries of users - a list of your favorite blogs,
    and a separate list of other blogs, both ordered by last update
    date.  The favorites list is essentially a way to view blogs
    through a whitelist (only listing authors marked with the smiley
    face), while the "other blogs" list is a way to view them through a
    blacklist (avoiding authors marked with that frown face).  Both
    lists simply go to a slightly modified threaded view, except it
    displays multiple posts at once, and only includes threads started
    by the selected author (not threads they merely participated in).

    4) ???

    There is lots going on at the app level as well as in the router
    core, and there has been some interesting discussions on the forum
    in the past week.  In any case, if anyone wants to bring anything up
    during our meeting, swing on by in a few minutes and say hi!

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.4.1 (GNU/Linux)

    iD8DBQFDqGKDWYfZ3rPnHH0RAiHcAJ9FuF0+Pnq1DKE+phJ7tWHNHHYJAgCcDZks
    6BpcLIJvkfMv+VMT26BEhFY=
    =+a9R
    -----END PGP SIGNATURE-----
:::
