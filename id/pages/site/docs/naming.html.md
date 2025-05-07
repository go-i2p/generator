 Penamaan dan Buku
Alamat 2025-01 0.9.65 

## Ikhtisar {#overview}

I2P berisi library penamaan umum dan implementasi base yang didesain
untuk penamaan lokal kepada pemetaan destinasi, termasuk aplikasi
tambahan yang bernama [addressbook](#addressbook). I2P juga mendukung
[Base32 hostnames](#base32) mirip dengan alamat .onion di Tor.

Addressbook adalah sistem penamaan yang berbasis web, aman,
terdistribusi, dan terbaca manusia, hanya punya kekurangan di nama
alamat yang kurang dapat dibaca manusia supaya unik secara global dengan
mewajibkan hanya alamat lokal. Walaupun semua pesan di I2P dibuat
alamatnya terenkripsi oleh destinasinya, setiap orang dapat memiliki
entri yang sama, misalnya \"Alice\" yang dapat berarti destinasi yang
berbeda. Setiap orang dapat menemukan nama baru dengan cara mengimpor
adressbook yang dipublikasikan oleh peer, yang dispesifikkan di web
trust mereka, dengan menambah entri yang disediakan pihak ketiga, atau
(jika ada pihak yang mengatur beberapa publikasi addressbook dengan cara
registrasi pertama datang pertama ditulis) orang-orang dapat memilih
untuk menganggap addressbook ini sebagai name server, meniru sistem DNS
tradisional.

NOTE: For the reasoning behind the I2P naming system, common arguments
against it and possible alternatives see the [naming
discussion]() page.

## Komponen Sistem Penamaan {#components}

Tidak ada otoritas utama penamaan di I2P. Semua nama host diatur secara
lokal di setiap komputer pengguna.

Sistem penamaan cukup sederhana dan sebagian besar diterapkan di
aplikasi di luar router, tapi disertakan di distribusi I2P.
Komponen-komponennya adalah:

1. [Servis penamaan](#lookup) lokal yang melakukan pencarian juga
 menangani [Base32 hostnames](#base32).
2. [HTTP proxy](#httpproxy) meminta router untuk mencari host dan
 mengarahkan pengguna kepada remote jump service jika pencarian host
 gagal.
3. [formulir host-add](#add-services) HTTP membuat pengguna dapat
 menambah host ke dalam hosts.txt
4. HTTP [jump services](#jump-services) menyediakan pencarian dan
 pengalihan host.
5. Aplikasi [addressbook](#addressbook) menggabungkan daftar host
 eksternal, yang diambil secara HTTP, dengan daftar lokal.
6. Aplikasi [SusiDNS](#susidns) adalah aplikasi front-end sederhana
 untuk pengaturan addressbook dan menampilkan daftar host lokal.

## Naming Services {#lookup}

All destinations in I2P are 516-byte (or longer) keys. (To be more
precise, it is a 256-byte public key plus a 128-byte signing key plus a
3-or-more byte certificate, which in Base64 representation is 516 or
more bytes. Non-null
[Certificates](#certificates) are in
use now for signature type indication. Therefore, certificates in
recently-generated destinations are more than 3 bytes.

Jika sebuah aplikasi (i2ptunnel atau proxy HTTP) ingin mengakses sebuah
destinasi dengan menggunakan nama destinasinya, router melaksanakan
pencarian sangat sederhana secara lokal untuk menemukan nama host
tersebut.

### Hosts.txt Naming Service

Servis Penamaan Host.txt melaksanakan pencarian sederhana dan linier
terhadap file teks. Servis penamaan ini adalah standar sampai rilis
0.8.8 yang mana diganti oleh Blockfile Naming Service. Format hosts.txt
menjadi lambat setelah ukuran file-nya menjadi ribuan entri.

It does a linear search through three local files, in order, to look up
host names and convert them to a 516-byte destination key. Each file is
in a simple [configuration file
format](), with hostname=base64, one per
line. The files are:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile Naming Service

Blockfile Naming Service menyimpan beberapa \"addressbooks\" ke dalam
satu file database file bernama hostsdb.blockfile. Servis penamaan ini
menjadi standar sejak rilis 0.8.8.

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

Pada saat dia dibuat, servis penamaan mengimpor entri dari ketiga file
yang digunakan oleh Servis Penamaan hosts.txt. Blockfile meniru
penerapan sebelumnya dengan mempertahankan ketiga maps yang dicari
secara berurutan, yang bernama privatehosts.txt, userhosts.txt dan
hosts.txt. Dia juga mempertahankan reverse-lookup map untuk menerapkan
reverse lookup yang cepat.

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

The HTTP proxy does a lookup via the router for all hostnames ending in
\'.i2p\'. Otherwise, it forwards the request to a configured HTTP
outproxy. Thus, in practice, all HTTP (I2P Site) hostnames must end in
the pseudo-Top Level Domain \'.i2p\'.

Jika router gagal untuk mencari nama host, proxy HTTP menampilkan
halaman kesalahan pengguna dengan link ke beberapa \"jump\" service.
Lihat di bawah ini untuk detailnya.

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

## Buku Alamat {#addressbook}

### Subskripsi dan Merging yang Akan Datang

Aplikasi buku alamat secara berkala mengambil file hosts.txt milik user
lain dan menggabungkan mereka dengan hosts.txt lokal, setelah beberapa
pemeriksaan. Konflik penamaan diselesaikan dengan dasar yang pertama
datang itu yang pertama dilayani.

Berlangganan ke hosts.txt file milik pengguna lain berarti memberikan
kepercayaan kepada mereka. Anda tidak ingin mereka, misalnya,
\'membajak\' situs baru dengan secara cepat memasukkan kunci mereka
sendiri untuk situs baru sebelum melewati entri host kunci baru kepada
Anda.

Untuk alasan ini, satu-satunya langganan yang dikonfigurasi secara
default adalah
`http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`
, yang berisi salinan hosts.txt yang disertakan dalam rilis I2P.
Pengguna harus mengatur langganan atau subskripsi tambahan di dalam
aplikasi buku alamat lokal (dengan file subscriptions.txt atau
[SusiDNS](#susidns)).

Some other public address book subscription links:

- [http:///cgi-bin/i2hostetag](http:///cgi-bin/i2hostetag)
- [http:///cgi-bin/newhosts.txt](http:///cgi-bin/newhosts.txt)

Operator dari layanan ini mungkin memiliki berbagai kebijakan untuk
daftar host. Kehadiran daftar ini tidak menyiratkan endorsement.

### Aturan Penamaan

Sementara diharapkan tidak ada segala pembatasan teknis dalam I2P pada
nama host, buku alamat memberlakukan pembatasan beberapa nama host yang
diimpor dari langganan. Hal ini untuk dasar kewarasan tipografi dan
kompatibilitas dengan browser, dan keamanan. Aturan-aturan ini pada
dasarnya sama dengan RFC2396 Section 3.2.2. Nama host yang melanggar
aturan-aturan ini mungkin tidak diterapkan ke router lain.

Aturan Penamaan:

- Nama diubah menjadi huruf kecil pada saat diimpor.
- Nama-nama baru diperiksa apakah konflik dengan nama-nama yang sudah
 ada di userhosts.txt di hosts.txt yang sudah ada (tapi bukan di
 privatehosts.txt) setelah konversi ke huruf kecil.
- Hanya boleh berisi \[a-z\] \[0-9\] \'.\' dan \'-\' setelah konversi
 ke huruf kecil.
- Tidak boleh dimulai dengan \'.\' or \'-\'.
- Harus diakhiri \'.i2p\'.
- 67 karakter maksimum, termasuk \'.i2p\'.
- Tidak boleh mengandung \'\... \'.
- Tidak boleh mengandung \'.-\' atau \'-.\' (seperti dari 0.6.1.33).
- Tidak boleh mengandung \'\--\' kecuali di \'xn\--\' untuk IDN.
- Nama host Base32 (\*.b32.i2p) dipesan untuk penggunaan base 32 use
 sehingga tidak boleh diimpor.
- Certain hostnames reserved for project use are not allowed
 (proxy.i2p, router.i2p, console.i2p, mail.i2p, \*.proxy.i2p,
 \*.router.i2p, \*.console.i2p, \*.mail.i2p, and others)
- Hostnames starting with \'www.\' are discouraged and are rejected by
 some registration services. Some addressbook implementations
 automatically strip \'www.\' prefixes from lookups. So registring
 \'www.example.i2p\' is unnecessary, and registering a different
 destination for \'www.example.i2p\' and \'example.i2p\' will make
 \'www.example.i2p\' unreachable for some users.
- Key diperiksa untuk validitas base64.
- Keys diperiksa apakah ada konflik di key yang sudah ada di hosts.txt
 (bukan di privatehosts.txt).
- Panjang minimum key adalah 516 byte.
- Panjang maksimum key adalah 616 bytes (untuk menampung sertifikat
 sebesar maksimum 100 bytes).

Nama-nama host yang diterima lewat langganan yang lolos semua
pemeriksaan akan ditambahkan melalui local naming service.

Perhatikan bahwa simbol \".\" di nama host tidak berarti apapun, dan
tidak menandakan penamaan atau hirarki kepercayaan. Jika nama
\'host.i2p\' sudah ada, tidak ada yang dapat mencegah siapapun untuk
menambahkan nama \'a.host.i2p\' ke dalam hosts.txt milik mereka, dan
nama ini dapat diimpor ke addressbook siapapun. Metode untuk mencegah
penamaan subdomains kepada bukan \"pemilik\" domain (sertifikat?), dan
niat serta kelayakan metode-metode ini, adalah topik untuk diskusi
selanjutnya.

International Domain Names (IDN) juga berfungsi di i2p (menggunakan
format punycode \'xn\--\'). Untuk dapat melihat nama domain IDN .i2p
dapat ditampilkan dengan baik di Firefox, tambahkan
\'network.IDN.whitelist.i2p (boolean) = true\' di about:config.

Karena aplikasi addressbook tidak menggunakan privatehosts.txt sama
sekali, dalam praktiknya file ini adalah satu-satunya tempat yang tepat
untuk menempatkan alias pribadi atau \"pet names\" untuk situs yang
sudah ada di dalam hosts.txt.

### Format Feed Langganan Lanjutan

As of release 0.9.26, subscription sites and clients may support an
advanced hosts.txt feed protocol that includes metadata including
signatures. This format is backwards-compatible with the standard
hosts.txt hostname=base64destination format. See [the
specification](/spec/subscription) for details.

### Langganan Keluar

Address Book will publish the merged hosts.txt to a location
(traditionally hosts.txt in the local I2P Site\'s home directory) to be
accessed by others for their subscriptions. This step is optional and is
disabled by default.

### Hosting and HTTP Transport Issues

Aplikasi addressbook, bersama dengan eepget, menyimpan informasi Etag
dan/atau Last-Modified yang dikirimkan oleh web server untuk langganan.
Ini banyak mengurangi bandwidth yang dibutuhkan karena web server akan
menampilkan \'304 Not Modified\' di pengambilan berikutnya jika tidak
ada yang berubah.

Namun seluruh hosts.txt diunduh jika itu telah berubah. Lihat di bawah
ini untuk diskusi isu ini.

Hosts yang menyediakan file hosts.txt statis atau aplikasi CGI yang
sebanding dengannya sangat disarankan untuk menyediakan Content-Length
header, sekaligus Etag atau Last-Modified header. Juga pastikan server
menampilkan \'304 Not Modified\' ketika diperlukan. Ini akan banyak
mengurangi bandwidth jaringan dan mengurangi kemungkinan data korup.

## Host Add Services {#add-services}

Host add service adalah aplikasi CGI yang menggunakan hostname dan a
Base64 key debagai parameter dan menambahkannya ke dalam hosts.txt
lokal. Jika router lain berlangganan hosts.txt itu, hostname/kunci baru
akan disebarluaskan melalui jaringan.

Disarankan host add service menerapkan, minimum, batasan yang diterapkan
oleh aplikasi addressbook di atas. Host add services dapat menerapkan
tambahan batasan terhadap hostname atau key, misalnya:

- Batasan jumlah \'subdomains\'.
- Otorisasi \'subdomains\' melalui banyak metode.
- Hashcash atau signed certificate.
- Review editor terhadap host names dan/atau isi.
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


