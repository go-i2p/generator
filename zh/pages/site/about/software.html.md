 Intro 

# The I2P Software (I2P)

**[I2PSnark]()**: Snark is an I2P network
only BitTorrent client. It never makes a connection to a peer over any
other network.

**[The Address Book]()**: This is a
locally-defined list of human-readable addresses ( ie: i2p-projekt.i2p)
and corresponding I2P
addresses.(udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p)
It integrates with other applications to allow you to use those
human-readable addresses in place of those I2P addresses. It is more
similar to a hosts file or a contact list than a network database or a
DNS service. There is no recognized global namespace, you decide what
any given .i2p domain maps to in the end.

**The QR Code Generator**: Besides the Address Book, I2P addresses can
be shared by converting them into QR codes and scanning them with a
camera. This is especially useful for Android devices.

**[I2P Hidden Services Manager]()** This is a
general-purpose adapter for forwarding services ( ie SSH ) into I2P and
proxying client requests to and from I2P. It provides a variety of
"Tunnel Types" which are able to do advance filtering of traffic before
it reaches I2P.

### I2P Network Compatible Applications

**[Mozilla
Firefox]()**: A web browser with advanced
privacy and security features, this is the best browser to configure to
browse I2P sites.

**[Chromium]()**: A web browser developed by
Google that is the Open-Source base of Google Chrome, this is sometimes
used as an alternative to Firefox.

**[BiglyBT](https://biglybt.com)**: A Feature-Rich bittorrent
client including I2P support and the unique ability to "Bridge" regular
torrents in-to I2P so people can download them anonymously.

**[OpenSSH](https://openssh.com)**: OpenSSH is a popular program used
by systems administrators to [remotely administer a
server](), or to provide "Shell" accounts for users
on the server.

**[Git]()/[Gitlab]()**: Git
is a source-code control tool which is distributed, and often recommends
a fork-first workflow. Hosting source code on I2P is an important
activity, so Gitlab-specific instructions are available for all to
use.

**[Debian](https://debian.org) and
[Ubuntu](https://ubuntu.com) GNU/Linux**: It is possible to obtain
packages for Debian and Ubuntu GNU/Linux over I2P using
[apt-transport-i2p](https://i2pgit.org/idk/apt-transport-i2p) and
[apt-transport-i2phttp](https://i2pgit.org/idk/apt-transport-i2phttp).
In the future, a bittorrent-based transport may also be developed. 

### Applications for Developers to create new things

**[The SAM API
Bridge]()**: The SAM API is a language-independent
API for writing applications that are I2P-native by communicating with
the local I2P router. It can provide Streaming-like capabilities,
Anonymous Datagrams, or Repliable Datagrams.

**[The BOB API
Bridge]()**: This is a deprecated technology, BOB
users should migrate to SAM if it is possible for them to do so.

**[The I2CP
API]()**: Not strictly an application, this is how
Java applications communicate with the I2P router to set up tunnels,
generate and manage keys, and communicate with other peers on the
network.


