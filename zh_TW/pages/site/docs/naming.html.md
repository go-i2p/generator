 地址簿 2025-01 0.9.65 

## 總覽 {#overview}

I2P 提供了一个通用的命名库和一个基础实现
设计用于从本地名称到目的地的映射，以及一个称为 的附加应用程序，称为
[地址簿](#addressbook). I2P也支持 [Base32 主机地址](#base32)
就像Tor的.onion地质。

地址簿是一个信任网络驱动的安全、分布式和人类可读的命名系统，
只是牺牲了人类可读名称的全球唯一性的要求，只规定了 本地唯一性。
虽然I2P的所有信息都是按目的地加密编址的
目的地，但不同的人可以在本地地址簿中输入 \"Alice
\"的本地地址簿条目，指的是不同的目的地。
人们仍然可以通过导入已发布的地址簿，导入新的同伴的公开地址簿来发现新的名字。
通过添加通过第三方提供的条目，或者（如果一些人组织
如果一些人使用先到先得的注册方式组织了一系列公布的地址簿
系统），人们可以选择把这些地址簿当作名称服务器，模仿传统的DNS。

NOTE: For the reasoning behind the I2P naming system, common arguments
against it and possible alternatives see the [naming
discussion]() page.

## 命名系统组件 {#components}

I2P中没有中央命名机构。 所有的主机名都是本地的。

命名系统相当简单，大部分是在路由器外部的应用程序中实现的。 但与 I2P
发行版捆绑在一起。 这些组件是：

1. 本地的[命名服务](#lookup) 可以进行查找，并处理[Base32地址](#base32).
2. [HTTP代理](#httpproxy)要求路由器进行查找，并将用户指向远程跳转服务
 以协助解决查询失败的问题。
3. HTTP [host-add 表单](#add-services) 允许用户添加 hosts 到他们本地的
 hosts.txt
4. HTTP [跳转(jump)服务](#jump-services)
 提供它们自身的网络查询和重定向。
5. [地址簿](#addressbook) 应用程序将通过HTTP检索外部
 列表与本地列表合并。
6. [SusiDNS](#susidns) 应用程序是一个简单的网络前端
 用于配置地址簿和查看本地主机列表。

## Naming Services {#lookup}

All destinations in I2P are 516-byte (or longer) keys. (To be more
precise, it is a 256-byte public key plus a 128-byte signing key plus a
3-or-more byte certificate, which in Base64 representation is 516 or
more bytes. Non-null
[Certificates](#certificates) are in
use now for signature type indication. Therefore, certificates in
recently-generated destinations are more than 3 bytes.

如果一个应用程序（i2ptunnel或HTTP代理）希望访问
目的地的名字，路由器会做一个非常简单的本地查询 来解决。

### Hosts.txt Naming Service

hosts.txt 命名服务在文本文件中进行简单的线性搜索。
文本文件进行简单的线性搜索。这个命名服务是默认的，直到
0.8.8版之前，这个命名服务一直是默认的，直到它被Blockfile命名服务所取代。
hosts.txt格式在文件增加到数千个条目后变得太慢。

It does a linear search through three local files, in order, to look up
host names and convert them to a 516-byte destination key. Each file is
in a simple [configuration file
format](), with hostname=base64, one per
line. The files are:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile Naming Service

Blockfile命名服务将多个 \"地址簿 \"存储在
一个名为hostsdb.blockfile的数据库文件中。
这个命名服务从0.8.8版本开始成为默认。

A blockfile is simply on-disk storage of multiple sorted maps (key-value
pairs), implemented as skiplists. The blockfile format is specified on
the [Blockfile page](). It provides fast
Destination lookup in a compact format. While the blockfile overhead is
substantial, the destinations are stored in binary rather than in Base
64 as in the hosts.txt format. In addition, the blockfile provides the
capability of arbitrary metadata storage (such as added date, source,
and comments) for each entry to implement advanced address book
features. The blockfile storage requirement is a modest increase over
the hosts.txt format, and the blockfile provides approximately 10x
reduction in lookup times.

创建时，命名服务从hosts.txt命名服务使用的三个文件中导入。
区块文件模仿以前的实现，维护三个地图，按顺序搜索，分别为privatehosts.txt、userhosts.txt和hosts.txt。
它还维护了一个反向查找地图，以实现快速反向查找。

### Other Naming Service Facilities

The lookup is case-insensitive. The first match is used, and conflicts
are not detected. There is no enforcement of naming rules in lookups.
Lookups are cached for a few minutes. Base 32 resolution is [described
below](#base32). For a full description of the Naming Service API see
the [Naming Service Javadocs](). This API
was significantly expanded in release 0.8.7 to provide adds and removes,
storage of arbitrary properties with the hostname, and other features.

### Alternatives and Experimental Naming Services

The naming service is specified with the configuration property
`i2p.naming.impl=class`. Other implementations are possible. For
example, there is an experimental facility for real-time lookups (a la
DNS) over the network within the router. For more information see the
[alternatives on the discussion
page](#alternatives).

HTTP代理通过路由器对所有以\'.i2p\'结尾的主机名进行查询。
否则，它会将请求转发到配置好的HTTP外代理。
因此，所有的HTTP（I2P网站）主机名必须以伪顶级域\'.i2p\'结尾。

如果路由解析主机名失败，HTTP代理返回用户一个包含若干"跳转"服务链接的错误页面。详见下文。

## .i2p.alt Domain {#alt}

We previously [applied to reserve the .i2p
TLD](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/)
following the procedures specified in [RFC
6761](https://www.rfc-editor.org/rfc/rfc6761.html). However, this
application and all others were rejected, and RFC 6761 was declared a
\"mistake\".

After many years of work by the GNUnet team and others, the .alt domain
was reserved as a special-use TLD in [RFC
9476](https://www.rfc-editor.org/rfc/rfc9476.html) as of late 2023.
While there are no official registrars sanctioned by IANA, we have
registered the .i2p.alt domain with the primary unofficial registrar
[GANA](https://gana.gnunet.org/dot-alt/dot_alt.html). This does not
prevent others from using the domain, but it should help discourage it.

One benefit to the .alt domain is that, in theory, DNS resolvers will
not forward .alt requests once they update to comply with RFC 9476, and
that will prevent DNS leaks. For compatibility with .i2p.alt hostnames,
I2P software and services should be updated to handle these hostnames by
stripping off the .alt TLD. These updates are scheduled for the first
half of 2024.

At this time, there are no plans to make .i2p.alt the preferred form for
display and interchange of I2P hostnames. This is a topic for further
research and discussion.

## 地址簿 {#addressbook}

### 传入订阅和合并

地址簿应用程序会定期
检索其他用户的hosts.txt文件并将其与本地hosts.txt合并，并经过多次检查。
命名冲突以先到先得的方式解决。

订阅另一个用户的hosts.txt文件意味着给予他们一定程度的信任。
你肯定不希望他们，例如，\"劫持 \"一个新网站
在把真正的的host/key输入给你之前，替换成他们自己的key，从而 \"劫持
\"一个新的网站。

由于这个原因，默认情况下唯一的订阅
只有`http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`。
其中包含一份包含在I2P发行版中的hosts.txt副本。
用户必须在他们的地址簿应用程序中配置其他的订阅（通过 subscriptions.txt
或

SusiDNS）。

其他一些公共地址簿订阅链接有：

- [http:///cgi-bin/i2hostetag](http:///cgi-bin/i2hostetag)
- [http:///cgi-bin/newhosts.txt](http:///cgi-bin/newhosts.txt)

这些服务的运营商可能有不同的政策来注册主机。
出现在这个名单上并不意味着得到认可。

### 命名规则

While there are hopefully not any technical limitations within I2P on
host names, the address book enforces several restrictions on host names
imported from subscriptions. It does this for basic typographical sanity
and compatibility with browsers, and for security. The rules are
essentially the same as those in RFC2396 Section 3.2.2. Any hostnames
violating these rules may not be propagated to other routers.

命名规则:

- 名字将在导入时被转换为小写形式
- Names are checked for conflict with existing names in the existing
 userhosts.txt and hosts.txt (but not privatehosts.txt) after
 conversion to lower case.
- Must contain only \[a-z\] \[0-9\] \'.\' and \'-\' after conversion
 to lower case.
- 开头必须不能是 \'.\' 或者 \'-\'。
- 结尾必须是 \'.i2p\'。
- 最多67个字符，包括 \'.i2p\'。
- 不能包含 \'..\'。
- Must not contain \'.-\' or \'-.\' (as of 0.6.1.33).
- Must not contain \'\--\' except in \'xn\--\' for IDN.
- Base32 hostnames (\*.b32.i2p) are reserved for base 32 use and so
 are not allowed to be imported.
- Certain hostnames reserved for project use are not allowed
 (proxy.i2p, router.i2p, console.i2p, mail.i2p, \*.proxy.i2p,
 \*.router.i2p, \*.console.i2p, \*.mail.i2p, and others)
- Hostnames starting with \'www.\' are discouraged and are rejected by
 some registration services. Some addressbook implementations
 automatically strip \'www.\' prefixes from lookups. So registring
 \'www.example.i2p\' is unnecessary, and registering a different
 destination for \'www.example.i2p\' and \'example.i2p\' will make
 \'www.example.i2p\' unreachable for some users.
- Keys are checked for base64 validity.
- Keys are checked for conflict with existing keys in hosts.txt (but
 not privatehosts.txt).
- Minimum key length 516 bytes.
- Maximum key length 616 bytes (to account for certs up to 100 bytes).

Any name received via subscription that passes all the checks is added
via the local naming service.

Note that the \'.\' symbols in a host name are of no significance, and
do not denote any actual naming or trust hierarchy. If the name
\'host.i2p\' already exists, there is nothing to prevent anybody from
adding a name \'a.host.i2p\' to their hosts.txt, and this name can be
imported by others\' address book. Methods to deny subdomains to
non-domain \'owners\' (certificates?), and the desirability and
feasibility of these methods, are topics for future discussion.

International Domain Names (IDN) also work in i2p (using punycode
\'xn\--\' form). To see IDN .i2p domain names rendered correctly in
Firefox\'s location bar, add \'network.IDN.whitelist.i2p (boolean) =
true\' in about:config.

As the address book application does not use privatehosts.txt at all, in
practice this file is the only place where it is appropriate to place
private aliases or \"pet names\" for sites already in hosts.txt.

### Advanced Subscription Feed Format

As of release 0.9.26, subscription sites and clients may support an
advanced hosts.txt feed protocol that includes metadata including
signatures. This format is backwards-compatible with the standard
hosts.txt hostname=base64destination format. See [the
specification](/spec/subscription) for details.

### Outgoing Subscriptions

Address Book will publish the merged hosts.txt to a location
(traditionally hosts.txt in the local I2P Site\'s home directory) to be
accessed by others for their subscriptions. This step is optional and is
disabled by default.

### Hosting and HTTP Transport Issues

The address book application, together with eepget, saves the Etag
and/or Last-Modified information returned by the web server of the
subscription. This greatly reduces the bandwidth required, as the web
server will return a \'304 Not Modified\' on the next fetch if nothing
has changed.

However the entire hosts.txt is downloaded if it has changed. See below
for discussion on this issue.

Hosts serving a static hosts.txt or an equivalent CGI application are
strongly encouraged to deliver a Content-Length header, and either an
Etag or Last-Modified header. Also ensure that the server delivers a
\'304 Not Modified\' when appropriate. This will dramatically reduce the
network bandwidth, and reduce chances of corruption.

## Host Add Services {#add-services}

A host add service is a simple CGI application that takes a hostname and
a Base64 key as parameters and adds that to its local hosts.txt. If
other routers subscribe to that hosts.txt, the new hostname/key will be
propagated through the network.

It is recommended that host add services impose, at a minimum, the
restrictions imposed by the address book application listed above. Host
add services may impose additional restrictions on hostnames and keys,
for example:

- A limit on number of \'subdomains\'.
- Authorization for \'subdomains\' through various methods.
- Hashcash or signed certificates.
- Editorial review of host names and/or content.
- Categorization of hosts by content.
- Reservation or rejection of certain host names.
- Restrictions on the number of names registered in a given time
 period.
- Delays between registration and publication.
- Requirement that the host be up for verification.
- Expiration and/or revocation.
- IDN spoof rejection.

## Jump Services

A jump service is a simple CGI application that takes a hostname as a
parameter and returns a 301 redirect to the proper URL with a
`?i2paddresshelper=key` string appended. The HTTP proxy will interpret
the appended string and use that key as the actual destination. In
addition, the proxy will cache that key so the address helper is not
necessary until restart.

Note that, like with subscriptions, using a jump service implies a
certain amount of trust, as a jump service could maliciously redirect a
user to an incorrect destination.

To provide the best service, a jump service should be subscribed to
several hosts.txt providers so that its local host list is current.

## SusiDNS

SusiDNS is simply a web interface front-end to configuring address book
subscriptions and accessing the four address book files. All the real
work is done by the \'address book\' application.

Currently, there is little enforcement of address book naming rules
within SusiDNS, so a user may enter hostnames locally that would be
rejected by the address book subscription rules.

## Base32 Names {#base32}

I2P supports Base32 hostnames similar to Tor\'s .onion addresses. Base32
addresses are much shorter and easier to handle than the full
516-character Base64 Destinations or addresshelpers. Example:
`ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

In Tor, the address is 16 characters (80 bits), or half of the SHA-1
hash. I2P uses 52 characters (256 bits) to represent the full SHA-256
hash. The form is {52 chars}.b32.i2p. Tor has a
[proposal](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013)
to convert to an identical format of {52 chars}.onion for their hidden
services. Base32 is implemented in the naming service, which queries the
router over I2CP to lookup the LeaseSet to get the full Destination.
Base32 lookups will only be successful when the Destination is up and
publishing a LeaseSet. Because resolution may require a network database
lookup, it may take significantly longer than a local address book
lookup.

Base32 addresses can be used in most places where hostnames or full
destinations are used, however there are some exceptions where they may
fail if the name does not immediately resolve. I2PTunnel will fail, for
example, if the name does not resolve to a destination.

## Extended Base32 Names {#newbase32}

Extended base 32 names were introduced in release 0.9.40 to support
encrypted lease sets. Addresses for encrypted leasesets are identified
by 56 or more encoded characters, not including the \".b32.i2p\" (35 or
more decoded bytes), compared to 52 characters (32 bytes) for
traditional base 32 addresses. See proposals 123 and 149 for additional
information.

Standard Base 32 (\"b32\") addresses contain the hash of the
destination. This will not work for encrypted ls2 (proposal 123).

You can\'t use a traditional base 32 address for an encrypted LS2
(proposal 123), as it contains only the hash of the destination. It does
not provide the non-blinded public key. Clients must know the
destination\'s public key, sig type, the blinded sig type, and an
optional secret or private key to fetch and decrypt the leaseset.
Therefore, a base 32 address alone is insufficient. The client needs
either the full destination (which contains the public key), or the
public key by itself. If the client has the full destination in an
address book, and the address book supports reverse lookup by hash, then
the public key may be retrieved.

So we need a new format that puts the public key instead of the hash
into a base32 address. This format must also contain the signature type
of the public key, and the signature type of the blinding scheme.

This section documents a new b32 format for these addresses. While we
have referred to this new format during discussions as a \"b33\"
address, the actual new format retains the usual \".b32.i2p\" suffix.

### Creation and encoding

Construct a hostname of {56+ chars}.b32.i2p (35+ chars in binary) as
follows. First, construct the binary data to be base 32 encoded:

 flag (1 byte)
 bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
 bit 1: 0 for no secret, 1 if secret is required
 bit 2: 0 for no per-client auth,
 1 if client private key is required
 bits 7-3: Unused, set to 0

 public key sigtype (1 or 2 bytes as indicated in flags)
 If 1 byte, the upper byte is assumed zero

 blinded key sigtype (1 or 2 bytes as indicated in flags)
 If 1 byte, the upper byte is assumed zero

 public key
 Number of bytes as implied by sigtype

Post-processing and checksum:

 Construct the binary data as above.
 Treat checksum as little-endian.
 Calculate checksum = CRC-32(data[3:end])
 data[0] ^= (byte) checksum
 data[1] ^= (byte) (checksum >> 8)
 data[2] ^= (byte) (checksum >> 16)

 hostname = Base32.encode(data) || ".b32.i2p"

Any unused bits at the end of the b32 must be 0. There are no unused
bits for a standard 56 character (35 byte) address.

### Decoding and Verification

 Strip the ".b32.i2p" from the hostname
 data = Base32.decode(hostname)
 Calculate checksum = CRC-32(data[3:end])
 Treat checksum as little-endian.
 flags = data[0] ^ (byte) checksum
 if 1 byte sigtypes:
 pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
 blinded sigtype = data[2] ^ (byte) (checksum >> 16)
 else (2 byte sigtypes) :
 pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
 blinded sigtype = data[3] || data[4]
 parse the remainder based on the flags to get the public key

### Secret and Private Key Bits

The secret and private key bits are used to indicate to clients,
proxies, or other client-side code that the secret and/or private key
will be required to decrypt the leaseset. Particular implementations may
prompt the user to supply the required data, or reject connection
attempts if the required data is missing.

### Notes

- XORing first 3 bytes with the hash provides a limited checksum
 capability, and ensures that all base32 chars at the beginning are
 randomized. Only a few flag and sigtype combinations are valid, so
 any typo is likely to create an invalid combination and will be
 rejected.
- In the usual case (1 byte sigtypes, no secret, no per-client auth),
 the hostname will be {56 chars}.b32.i2p, decoding to 35 bytes, same
 as Tor.
- Tor 2-byte checksum has a 1/64K false negative rate. With 3 bytes,
 minus a few ignored bytes, ours is approaching 1 in a million, since
 most flag/sigtype combinations are invalid.
- Adler-32 is a poor choice for small inputs, and for detecting small
 changes. We use CRC-32 instead. CRC-32 is fast and is widely
 available.
- While outside the scope of this specification, routers and/or
 clients must remember and cache (probably persistently) the mapping
 of public key to destination, and vice versa.
- Distinguish old from new flavors by length. Old b32 addresses are
 always {52 chars}.b32.i2p. New ones are {56+ chars}.b32.i2p
- Tor discussion thread [is
 here](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- Don\'t expect 2-byte sigtypes to ever happen, we\'re only up to 13.
 No need to implement now.
- New format can be used in jump links (and served by jump servers) if
 desired, just like b32.
- Any secret, private key, or public key longer than 32 bytes would
 exceed the DNS max label length of 63 chars. Browsers probably do
 not care.
- No backward compatibility issues. Longer b32 addresses will fail to
 be converted to 32-byte hashes in old software.


