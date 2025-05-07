 Adlandırma ve
Adres Defteri 2025-01
0.9.65 

## Özet {#overview}

I2P, genel bir adlandırma kitaplığı ve yerel bir adla hedef eşleme
arasında çalışmak üzere tasarlanmış bir temel uygulamanın yanında [adres
defteri](#addressbook) adlı bir eklenti uygulamasıyla birlikte gelir.
I2P ayrıca Tor .onion adreslerine benzer [Base32 sunucu
adlarını](#base32) destekler.

Adres defteri, yerel benzersizliği zorunlu kılarak insan tarafından
okunabilir tüm adların küresel olarak benzersiz olmasını şart koşamayan,
güvenli, dağıtılmış ve insan tarafından okunabilir bir adlandırma
sistemidir. I2P üzerindeki tüm iletiler, hedefleri tarafından
şifrelenerek adreslendiğinden, farklı kişilerde, farklı hedeflere atıfta
bulunan \"Alice\" yerel adres defteri kayıtları olabilir. İnsanlar,
güven ağlarında belirtilen eşlerin yayınlanmış adres defterlerini içe
aktararak veya üçüncü bir taraf aracılığıyla sağlanan kayıtları
ekleyerek (bazı kişiler ilk gelen ilk alır kayıt sistemini kullanarak
bazı adres defterleri düzenlemişse) yeni adlar keşfedebilir. Bu adres
defterleri geleneksel DNS sunucusuna benzeyen ad sunucuları olarak
düşünülebilir.

NOTE: For the reasoning behind the I2P naming system, common arguments
against it and possible alternatives see the [naming
discussion]() page.

## Adlandırma Sistemi Bileşenleri {#components}

I2P ağında merkezi bir adlandırma otoritesi yoktur. Tüm sunucu adları
yereldir.

Adlandırma sistemi oldukça basittir ve çoğu yöneltici dışındaki
uygulamalarda bulunur, ancak I2P dağıtımıyla birlikte gelir. Bileşenleri
şunlardır:

1. Aramaları yapan ve [Base32 sunucu adlarını](#base32) işleyen yerel
 [adlandırma hizmeti](#lookup).
2. Yönelticiden aramalar isteyen ve başarısız aramalara yardımcı olması
 için kullanıcıyı uzaktan atlama hizmetlerine yönlendiren [HTTP vekil
 sunucusu](#httpproxy).
3. Kullanıcıların yerel hosts.txt dosyalarına sunucu eklemesini
 sağlayan HTTP [host-add formları](#add-services)
4. Kendi aramalarını ve yönlendirmelerini sağlayan HTTP [sıçrama
 hizmetleri](#jump-services).
5. HTTP aracılığıyla alınan dış sunucu listelerini yerel listeyle
 birleştiren [adres defteri](#addressbook) uygulaması.
6. Adres defteri yapılandırması ve yerel sunucu listelerinin
 görüntülenmesi için basit bir site ön yüzü olan [SusiDNS](#susidns)
 uygulaması.

## Naming Services {#lookup}

All destinations in I2P are 516-byte (or longer) keys. (To be more
precise, it is a 256-byte public key plus a 128-byte signing key plus a
3-or-more byte certificate, which in Base64 representation is 516 or
more bytes. Non-null
[Certificates](#certificates) are in
use now for signature type indication. Therefore, certificates in
recently-generated destinations are more than 3 bytes.

Bir uygulama (i2ptunnel ya da HTTP vekil sunucusu) bir hedefe adına göre
erişmek isterse, yöneltici bu adı çözmek için çok basit bir yerel arama
yapar.

### Hosts.txt Naming Service

Hosts.txt adlandırma hizmeti, metin dosyalarında basit bir doğrusal
arama yapar. Bu adlandırma hizmeti, 0.8.8 sürümünde Blockfile adlandırma
hizmeti ile değiştirilene kadar 0.8.8 varsayılan hizmetti. Dosya
binlerce kayda ulaştığından hosts.txt biçimi çok yavaşlamıştı.

It does a linear search through three local files, in order, to look up
host names and convert them to a 516-byte destination key. Each file is
in a simple [configuration file
format](), with hostname=base64, one per
line. The files are:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile Naming Service

Blockfile adlandırma hizmeti, birden çok \"adres defterini\"
hostsdb.blockfile adlı tek bir veri tabanı dosyasında saklar. 0.8.8
sürümünden başlayarak bu adlandırma hizmeti varsayılan olarak
kullanılıyor.

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

Adlandırma hizmeti, oluşturulması sırasında hosts.txt adlandırma hizmeti
tarafından kullanılan üç dosyadaki kayıtları içe aktarır. Blockfile,
privatehosts.txt, userhosts.txt ve hosts.txt adıyla sırayla aranan üç
haritalamayı koruyarak önceki uygulamanın davranışını taklit eder.
Ayrıca, geriye doğru hızlı arama yapabilmek için geriye doğru arama
haritası tutar.

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

HTTP vekil sunucusu, \'.i2p\' ile biten tüm sunucu adları için yöneltici
aracılığıyla bir arama yapar. Diğer durumlarda, isteği yapılandırılmış
bir HTTP çıkış vekil sunucusuna iletir. Bu nedenle, pratikte, tüm HTTP
(I2P sitesi) sunucu adları, sözde üst düzey etki alanı \'.i2p\' ile
bitmelidir.

Yöneltici sunucu adını çözümleyemezse, HTTP vekil sunucusu kullanıcıya
birkaç \"atlama\" hizmetine bağlantılar içeren bir hata sayfası
görüntüler. Ayrıntılar için aşağıya bakın.

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

## Adres Defteri {#addressbook}

### Geliş Abonelikleri ve Birleştirme

Adres defteri uygulaması, düzenli aralıklarla diğer kullanıcıların
hosts.txt dosyalarını alır ve birkaç kontrolden sonra bunları yerel
hosts.txt dosyası ile birleştirir. Adlandırma çakışmaları, ilk gelen ilk
alır ilkesiyle çözülür.

Başka bir kullanıcının hosts.txt dosyasına abone olmak, onlara belirli
bir miktarda güven vermeyi gerektirir. Örneğin, yeni sunucu/anahtar
girişini size iletmeden önce yeni bir site için kendi anahtarlarını
hızla yazarak yeni bir siteyi \'ele geçirmelerini\' istemezsiniz.

Bu nedenle, varsayılan olarak yapılandırılan tek abonelik, sunucuların
bir kopyasını içeren ve I2P paketine katılmış
`http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`
dosyasıdır. Kullanıcılar, yerel adres defteri uygulamalarında ek
abonelikler yapılandırmalıdır (subscriptions.txt veya
[SusiDNS](#susidns) ile).

Bazı diğer genel adres defteri abonelik bağlantıları:

- [http:///cgi-bin/i2hostetag](http:///cgi-bin/i2hostetag)
- [http:///cgi-bin/newhosts.txt](http:///cgi-bin/newhosts.txt)

Bu hizmetlerin işletmecilerinin, çeşitli sunucuları listeleme ilkeleri
olabilir. Bu listede bulunması, onaylandığı anlamına gelmez.

### Adlandırma Kuralları

I2P üzerinde sunucu adlarında herhangi bir teknik sınırlama olmamasını
ummakla birlikte, adres defteri aboneliklerden içe aktarılan sunucu
adları üzerinde çeşitli kısıtlamalar uygular. Bunu temel tipografi
koruması ve tarayıcılarla uyumluluk ve güvenlik sağlamak için yapar.
Kurallar temelde RFC2396 3.2.2 bölümündekilerle aynıdır. Bu kuralları
ihlal eden sunucu adları diğer yönelticilere dağıtılmayabilir.

Adlandırma Kuralları:

- İçe aktarma sırasında adlar küçük harfe dönüştürülür
- Adlar, küçük harfe dönüştürüldükten sonra var olan userhosts.txt ve
 hosts.txt dosyalarındaki (privatehosts.txt değil) var olan adlarla
 çakışmaları denetlenir.
- Yalnızca \[a-z\] \[0-9\] \'.\' ve \'-\' karakterleri küçük harfe
 dönüştürüldükten sonra kullanılmalıdır.
- \'.\' ya da \'-\' ile başlamamalıdır.
- \'.i2p\' ile bitmelidir.
- \'.i2p ile birlikte en fazla 67 karakterden oluşmalıdır.
- \'..\' içermemelidir.
- \'.-\' ya da \'-.\' bulunmamalıdır (0.6.1.33 gibi).
- IDN için \'xn\--\' dışında \'\--\' bulunmamalıdır.
- Base32 sunucu adları (\*.b32.i2p), Base32 kullanımı için ayrılmıştır
 ve bu nedenle içe aktarılmasına izin verilmez.
- Certain hostnames reserved for project use are not allowed
 (proxy.i2p, router.i2p, console.i2p, mail.i2p, \*.proxy.i2p,
 \*.router.i2p, \*.console.i2p, \*.mail.i2p, and others)
- Hostnames starting with \'www.\' are discouraged and are rejected by
 some registration services. Some addressbook implementations
 automatically strip \'www.\' prefixes from lookups. So registring
 \'www.example.i2p\' is unnecessary, and registering a different
 destination for \'www.example.i2p\' and \'example.i2p\' will make
 \'www.example.i2p\' unreachable for some users.
- Anahtarların Base64 geçerliliği denetlenir.
- Anahtarların hosts.txt dosyasında var olan anahtarlarla çakışıp
 çakışmadığı denetlenir (privatehosts.txt denetlenmez).
- En az anahtar uzunluğu 516 bayt.
- En fazla anahtar uzunluğu 616 bayt (100 bayta kadar olan
 sertifikaları katmak için).

Tüm denetimleri geçen abonelik yoluyla alınan herhangi bir ad, yerel
adlandırma hizmeti ile eklenir.

Bir sunucu adındaki \'.\' karakterlerinin herhangi bir önemi yoktur ve
herhangi bir gerçek adlandırma veya güven hiyerarşisini göstermez.
\'Host.i2p\' adı zaten varsa, herhangi birinin hosts.txt dosyasına
\'a.host.i2p\' adını eklemesini engelleyen bir şey yoktur ve bu ad
başkalarının adres defteri tarafından alınabilir. Etki alanı olmayan
\'sahiplere\' (sertifikalar?) alt etki alanlarını reddetme yöntemleri ve
bu yöntemlerin istenilebilirliği ve uygulanabilirliği, gelecekteki
tartışma konularıdır.

Uluslararası etki alanı adları (IDN) i2p üzerinde de çalışır (punnycode
\'xn\--\' biçimiyle). Firefox konum çubuğunda IDN .i2p alan adlarının
doğru şekilde oluşturulduğunu görmek için about:config adresinden
\'network.IDN.whitelist.i2p (boolean) = true\' yapılandırmasını
ayarlayın.

Adres defteri uygulaması privatehosts.txt dosyasını hiç
kullanmadığından, pratikte bu dosya, hosts.txt içinde zaten bulunan
siteler için özel takma adlar veya \"evcil adlar\" eklemenin uygun
olduğu tek yerdir.

### Gelişmiş Abonelik Akış Biçimi

As of release 0.9.26, subscription sites and clients may support an
advanced hosts.txt feed protocol that includes metadata including
signatures. This format is backwards-compatible with the standard
hosts.txt hostname=base64destination format. See [the
specification](/spec/subscription) for details.

### Gidiş Abonelikleri

Adres Defteri, birleştirilmiş hosts.txt dosyasını başkaları tarafından
abone olunabilmesi için erişilebilecek bir konuma (geleneksel olarak
yerel I2P sitesinin kök klasöründeki hosts.txt) yayınlar. Bu adım isteğe
bağlıdır ve varsayılan olarak devre dışıdır.

### Hosting and HTTP Transport Issues

Adres defteri uygulaması, eepget ile birlikte, aboneliğin site sunucusu
tarafından geri döndürülen Etag ve/veya son değişiklik bilgilerini
kaydeder. Bu özellik, gereken bant genişliğini büyük ölçüde azaltır,
çünkü hiçbir şey değişmediyse site sunucusu bir sonraki almada \'304
değiştirilmedi\' iletisi geri döndürür.

Ancak, değişiklik yapılmışsa tüm hosts.txt dosyası indirilir. Bu konuyla
ilgili tartışma için aşağıya bakabilirsiniz.

Durağan bir hosts.txt veya eşdeğer bir CGI uygulaması sunan sunucuların,
bir Content-Length üst bilgisi ve bir Etag veya Last-Modified üst
bilgisi göndermesi önemle önerilir. Ayrıca sunucunun uygun durumda \'304
değiştirilmedi\' iletisi sunduğundan emin olun. Bu özellik, ağ bant
genişliğini önemli ölçüde azaltır ve bozulma olasılığını düşürür.

## Sunucu Ekleme Hizmetleri {#add-services}

Sunucu ekleme hizmeti, parametre olarak bir sunucu adı ve bir Base64
anahtarı alan ve bunu yerel hosts.txt dosyasına ekleyen basit bir CGI
uygulamasıdır. Diğer yönelticiler bu hosts.txt dosyasına abone olursa,
yeni sunucu adı ve anahtarları ağ üzerinde yayılır.

Sunucu ekleme hizmetlerinin en azından yukarıda listelenen adres defteri
uygulamasının getirdiği kısıtlamaları getirmesi önerilir. Sunucu ekleme
hizmetleri, sunucu adlarına ve anahtarlarına ek kısıtlamalar
getirebilir, örneğin:

- \'Alt etki alanı\' sayısı için bir sınır.
- Çeşitli yöntemlerle \'alt etki alanları\' için yetkilendirme.
- Hashcash veya imzalanmış sertifikalar.
- Sunucu adlarının ve/veya içeriğin editörlerce incelenmesi.
- Sunucuların içeriğe göre sınıflandırılması.
- Belirli sunucu adının rezervasyonu veya reddi.
- Belirli bir zaman diliminde kaydedilen ad sayısıyla ilgili
 kısıtlamalar.
- Kayıt ve yayın arasındaki gecikmeler.
- Sunucunun doğrulama için hazır olması şartı.
- Sona erme ve/veya iptal etme.
- IDN sahtecilik reddi.

## Atlama Hizmetleri {#jump-services}

Bir atlama hizmeti, parametre olarak bir sunucu adını alan ve
`?i2paddresshelper=key` dizgesi eklenmiş olarak uygun adrese bir 301
yönlendirmesi döndüren basit bir CGI uygulamasıdır. HTTP vekil sunucusu,
eklenen dizgeyi yorumlar ve bu anahtarı gerçek hedef olarak kullanır. Ek
olarak, vekil sunucu bu anahtarı ön belleğe alır, böylece yeniden
başlatılıncaya kadar adres yardımcısı gerekli olmaz.

Aboneliklerde olduğu gibi, atlama hizmeti kullanmanın belirli bir güven
düzeyi anlamına geldiğini unutmayın. Çünkü atlama hizmeti bir
kullanıcıyı kötü niyetli bir şekilde yanlış bir hedefe yönlendirebilir.

En iyi hizmeti sağlamak amacıyla, yerel sunucu listesinin güncel olması
için bir atlama hizmetinin birkaç hosts.txt sağlayıcısına abone olması
gerekir.

## SusiDNS

SusiDNS, adres defteri aboneliklerini yapılandırmak ve dört adres
defteri dosyasına erişmeyi sağlayan basit bir internet arayüzüdür. Tüm
gerçek işler \'adres defteri\' uygulaması tarafından yapılır.

Şu anda, SusiDNS içinde adres defteri adlandırma kurallarını çok azı
uygulanır. Bu nedenle bir kullanıcı, adres defteri abonelik kuralları
tarafından reddedilen sunucu adlarını yerel olarak ekleyebilir.

## Base32 Adları {#base32}

I2P, Tor ağındaki .onion adreslerine benzer Base32 sunucu adlarını
destekler. Base32 adresleri, tam 516 karakterli Base64 hedefleri veya
adres yardımcılarından çok daha kısadır ve kullanımı daha kolaydır.
Örnek: 1ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p1

Tor ağında adres 16 karakterdir (80 bit) veya SHA-1 karma değerinin
yarısıdır. I2P, tam SHA-256 karmasını temsil etmek için 52 karakter (256
bit) kullanır. Biçimi {52 chars}.b32.i2p şeklindedir. Tor gizli
hizmetlerini aynı {52 chars}.onion biçimine dönüştürmek için bir
[öneri](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013)
vardır. Base32, tam hedefi almak amacıyla \"Kiralama kümesini\"
(LeaseSet) aramak için yönelticiyi I2CP üzerinden sorgulayan adlandırma
hizmetinde uygulanır. Base32 aramaları, yalnızca hedef açık olduğunda ve
bir \"Kiralama kümesi\" (LeaseSet) yayınlandığında başarılı olur. Çözüm,
bir ağ veri tabanı araması gerektirebileceğinden, yerel adres defteri
aramasından çok daha uzun sürebilir.

Base32 adresleri, sunucu adlarının veya tam hedeflerin kullanıldığı çoğu
yerde kullanılabilir. Ancak ad hemen çözümlenmezse bunların başarısız
olabileceği bazı istisnalar vardır. Örneğin, ad bir hedefe
çözümlenemezse I2PTunnel başarısız olur.

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


