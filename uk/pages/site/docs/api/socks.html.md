 SOCKS 

## SOCKS і SOCKS проксі

The SOCKS proxy is working as of release 0.7.1. SOCKS 4/4a/5 are
supported. Enable SOCKS by creating a SOCKS client tunnel in i2ptunnel.
Both shared-clients and non-shared are supported. There is no SOCKS
outproxy so it is of limited use. 

Many applications leak sensitive information that could identify you on
the Internet. I2P only filters connection data, but if the program you
intend to run sends this information as content, I2P has no way to
protect your anonymity. For example, some mail applications will send
the IP address of the machine they are running on to a mail server.
There is no way for I2P to filter this, thus using I2P to \'socksify\'
existing applications is possible, but extremely dangerous.

And quoting from a 2005 email:

 ... there is a reason why human and
 others have both built and abandoned the SOCKS proxies. Forwarding
 arbitrary traffic is just plain unsafe, and it behooves us as
 developers of anonymity and security software to have the safety of
 our end users foremost in our minds.

Hoping that we can simply strap an arbitrary client on top of I2P
without auditing both its behavior and its exposed protocols for
security and anonymity is naive. Pretty much \*every\* application and
protocol violates anonymity, unless it was designed for it specifically,
and even then, most of those do too. That\'s the reality. End users are
better served with systems designed for anonymity and security.
Modifying existing systems to work in anonymous environments is no small
feat, orders of magnitude more work that simply using the existing I2P
APIs.

The SOCKS proxy supports standard address book names, but not Base64
destinations. Base32 hashes should work as of release 0.7. It supports
outgoing connections only, i.e. an I2PTunnel Client. UDP support is
stubbed out but not working yet. Outproxy selection by port number is
stubbed out.

The notes for [Meeting 81]() and [Meeting
82]() in March 2004.

[Onioncat](http://www.abenteuerland.at/onioncat/)

[](http:///)

### If You Do Get Something Working

Please let us know. And please provide substantial warnings about the
risks of socks proxies. 
