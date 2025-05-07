 MYI2P 

There has been discussion about a distributed blogging application for a
few months now called \"MyI2P\". While the original discussions were
lost, we were able to retrieve a Google
[cache](http://dev.i2p.net/~jrandom/i2p.net/myi2p.html) of it. It isn\'t
pretty, but it includes the basic overview and some discussion that
ensued.

The application itself is not yet implemented, and the ideas behind it
have been made less ambitious over time, but they are still valid and
the current [plan]() is to have the core MyI2P
functionality available along side the I2P 1.0 release. That will
include a distributed address book to enable secure, distributed, and
human readable naming by sacrificing the need for global uniqueness -
basically everyone has their own local address book and can
\'subscribe\' to other people\'s address books, letting MyI2P
periodically retrieve new name to destination mappings (leaving
conflicts up to the user to resolve). In addition to the address book,
there will be a distributed blogging system using a reduced and secured
subset of [bbcode](http://www.phpbb.com/phpBB/faq.php?mode=bbcode) to
essentially provide an anonymous
[LiveJournal](http://www.livejournal.com/) with a \'friends list\' and
transparent access control (authenticated by the I2P
[datagrams]() with rules defined based on the
address book).

Additional functionality, such as integration with a DHT backing store
or swarming file transfers for \'attachments\' can be added later. Email
may or may not get in the first pass either, though its implementation
is essentially just a blog entry with private access, so perhaps some UI
designer can come up with something. Exporting the data to RSS or access
through ATOM will be an option down the road as well.


