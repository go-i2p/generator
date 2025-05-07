 I2P üzerinden
Bittorent 2024-11 0.9.64 

I2P üzerinde birkaç bittorrent istemcisi ve izleyicisi var. I2P
adresleme, IP ve bağlantı noktası yerine bir hedef kullandığından, I2P
üzerinde çalışmak için izleyici ve istemci yazılımında küçük
değişiklikler gerekir. Bu değişiklikler aşağıda belirtilmiştir. Eski I2P
istemcileri ve izleyicileri ile uyumluluk sağlamak için yönergeleri
dikkatlice inceleyin.

Bu sayfada, tüm istemciler ve izleyiciler için ortak olan iletişim
kuralı ayrıntıları bulunur. Belirli istemci ve izleyiciler, diğer
benzersiz özellikleri veya iletişim kurallarını uygulayabilir.

I2P için ek istemci ve izleme yazılımı aktarımlarını memnuniyetle
karşılıyoruz.

## General Guidance for Developers

Most non-Java bittorrent clients will connect to I2P via
[SAMv3](). SAM sessions (or
inside I2P, tunnel pools or sets of tunnels) are designed to be
long-lived. Most bittorrent clients will only need one session, created
at startup and closed on exit. I2P is different from Tor, where circuits
may be rapidly created and discarded. Think carefully and consult with
I2P developers before designing your application to use more than one or
two simultaneous sessions, or to rapidly create and discard them.
Bittorrent clients must not create a unique session for every
connection. Design your client to use the same session for announces and
client connections.

Also, please ensure your client settings (and guidance to users about
router settings, or router defaults if you bundle a router) will result
in your users contributing more resources to the network than they
consume. I2P is a peer-to-peer network, and the network cannot survive
if a popular application drives the network into permanent congestion.

Do not provide support for bittorrent through an I2P outproxy to the
clearnet as it will probably be blocked. Consult with outproxy operators
for guidance.

The Java I2P and i2pd router implementations are independent and have
minor differences in behavior, feature support, and defaults. Please
test your application with the latest version of both routers.

i2pd SAM is enabled by default; Java I2P SAM is not. Provide
instructions to your users on how to enable SAM in Java I2P (via
/configclients in the router console), and/or provide a good error
message to the user if the initial connect fails, e.g. \"ensure that I2P
is running and the SAM interface is enabled\".

The Java I2P and i2pd routers have different defaults for tunnel
quantities. The Java default is 2 and the i2pd default is 5. For most
low- to medium-bandwidth and low- to medium-connection counts, 3 is
sufficient. Please specify the tunnel quantity in the SESSION CREATE
message to get consistent performance with the Java I2P and i2pd
routers.

I2P supports multiple signature and encryption types. For compatibility,
I2P defaults to old and inefficient types, so all clients should specify
newer types.

If using SAM, the signature type is specified in the DEST GENERATE and
SESSION CREATE (for transient) commands. All clients should set
SIGNATURE_TYPE=7 (Ed25519).

The encryption type is specified in the SAM SESSION CREATE command or in
i2cp options. Multiple encryption types are allowed. Some trackers
support ECIES-X25519, some support ElGamal, and some support both.
Clients should set i2cp.leaseSetEncType=4,0 (for ECIES-X25519 and
ElGamal) so that they may connect to both.

DHT support requires SAM v3.3 PRIMARY and SUBSESSIONS for TCP and UDP
over the same session. This will require substantial development effort
on the client side, unless the client is written in Java. i2pd does not
currently support SAM v3.3. libtorrent does not currently support SAM
v3.3.

Without DHT support, you may wish to automatically announce to a
configurable list of known open trackers so that magnet links will work.
Consult with I2P users for information on currently-up open trackers and
keep your defaults up-to-date. Supporting the i2p_pex extension will
also help alleviate the lack of DHT support.

For more guidance to developers on ensuring your application uses only
the resources it needs, please see the [SAMv3
specification]() and [our
guide to bundling I2P with your
application]().
Contact I2P or i2pd developers for further assistance.

## Duyurular

İstemciler, eski izleyicilerle uyumluluk için duyuruya genellikle sahte
bir port=6881 parametresi ekler. İzleyiciler port parametresini yok
sayabilir ve buna gerek duymamalıdır.

The ip parameter is the base 64 of the client\'s
[Destination](#struct_Destination),
using the I2P Base 64 alphabet \[A-Z\]\[a-z\]\[0-9\]-\~.
[Destinations](#struct_Destination)
are 387+ bytes, so the Base 64 is 516+ bytes. Clients generally append
\".i2p\" to the Base 64 Destination for compatibility with older
trackers. Trackers should not require an appended \".i2p\".

Diğer parametreler standart bittorrent ile aynıdır.

İstemciler için geçerli hedefler 387 ve üzeri bayttan oluşur (Base 64
kodlamasında 516 ve üzeri). Şu an normal kabul edilebilecek en fazla
değer 475 bayttır. İzleyicinin, kısa yanıtlar vermesi için Base64 kodunu
çözmesi gerektiğinden (aşağıya bakın), bir izleyicinin duyurulan hatalı
Base64 kodunu çözmesi ve reddetmesi gerekebilir.

Varsayılan yanıt türü, kısa değildir. İstemciler, compact=1 parametresi
ile kısa bir yanıt isteyebilir. İzleyici, istendiğinde kısa bir yanıt
verebilir, ancak zorunlu değildir. Note: All popular trackers now
support compact responses and at least one requires compact=1 in the
announce. All clients should request and support compact responses.

Yeni I2P istemcilerinin geliştiricilerinin, duyurular için 4444 bağlantı
noktasını HTTP istemci vekil sunucusu yerine kendi tünellerini
kullanması şiddetle önerilir. Bunu yapmak hem daha verimlidir hem de
izleyici tarafından hedefin dayatılmasını sağlar (aşağıya bakın).

Şu anda UDP duyurusunu/yanıtlarını destekleyen herhangi bir I2P
istemcisi ya da izleyicisi bilinmiyor.

## Kısa Olmayan İzleyici Yanıtları

Kısa olmayan yanıt, bir I2P \"ip\" parametresi ile standart bittorrent
üzerindeki gibidir. This is a long base64-encoded \"DNS string\",
probably with a \".i2p\" suffix.

İzleyiciler, eski istemcilerle uyumluluk için duyuruya genellikle sahte
bir port anahtarı ekler ya da duyurudaki port parametresini kullanır.
İstemciler port parametresini yok sayabilir ve buna gerek duymamalıdır.

The value of the ip key is the base 64 of the client\'s
[Destination](#struct_Destination), as
described above. Trackers generally append \".i2p\" to the Base 64
Destination if it wasn\'t in the announce ip, for compatibility with
older clients. Clients should not require an appended \".i2p\" in the
responses.

Diğer yanıt anahtarları ve değerleri standart bittorrent ile aynıdır.

## Kısa İzleyici Yanıtları

In the compact response, the value of the \"peers\" dictionary key is a
single byte string, whose length is a multiple of 32 bytes. This string
contains the concatenated [32-byte SHA-256
Hashes](#type_Hash) of the binary
[Destinations](#struct_Destination) of
the peers. This hash must be computed by the tracker, unless destination
enforcement (see below) is used, in which case the hash delivered in the
X-I2P-DestHash or X-I2P-DestB32 HTTP headers may be converted to binary
and stored. The peers key may be absent, or the peers value may be
zero-length.

Kısa yanıt desteğinin kullanımı istemciler ve izleyiciler için isteğe
bağlı olsa da, normal yanıt boyutunu 90% kadar azalttığı için
kullanılması önemle önerilir.

## Hedef Dayatma

Some, but not all, I2P bittorrent clients announce over their own
tunnels. Trackers may choose to prevent spoofing by requiring this, and
verifying the client\'s
[Destination](#struct_Destination)
using HTTP headers added by the I2PTunnel HTTP Server tunnel. The
headers are X-I2P-DestHash, X-I2P-DestB64, and X-I2P-DestB32, which are
different formats for the same information. These headers cannot be
spoofed by the client. A tracker enforcing destinations need not require
the ip announce parameter at all.

Birkaç istemci, duyurular için kendi tünelleri yerine HTTP vekil
sunucusunu kullandığından, hedefleri zorunlu kılmak, kendi tünelleri
üzerinden duyuru yapmaya dönüştürülmemiş istemciler tarafından
kullanılmasını önler.

Ne yazık ki, ağ büyüdükçe kötü niyetli davranış miktarı da artacak. Bu
nedenle sonunda tüm izleyicilerin hedefleri zorunlu kılmasını
bekliyoruz. Hem izleyici hem de istemci geliştiricileri bunu
öngörmelidir.

## Sunucu Adlarını Duyurma

Announce URL host names in torrent files generally follow the [I2P
naming standards](). In addition to host names
from address books and \".b32.i2p\" Base 32 hostnames, the full Base 64
Destination (with \[or without?\] \".i2p\" appended) should be
supported. Non-open trackers should recognize their own host name in any
of these formats.

Anonimliği korumak için, istemciler genellikle torrent dosyalarındaki
I2P olmayan duyuru adreslerini yok saymalıdır.

## İstemci Bağlantıları

İstemciden istemciye bağlantılar, standart TCP üzerinden iletişim
kuralını kullanır. Şu anda bilinen bir uTP iletişimi destekleyen I2P
istemcisi yok.

I2P uses 387+ byte
[Destinations](#struct_Destination)
for addresses, as explained above.

İstemci yalnızca hedefin karma değerine sahipse (bir kısa yanıt ya da
PEX gibi), bunu Base 32 ile kodlayıp, \".b32.i2p\" ekleyerek, varsa tam
hedefi döndürecek olan adlandırma hizmetini sorgulayan bir arama
yapmalıdır.

İstemci, kısa olmayan bir yanıtta aldığı bir eşin tam Hedefine sahipse,
bunu doğrudan bağlantı kurulumunda kullanmalıdır. Arama için bir Hedefi
tekrar Base 32 karma değerine dönüştürmeyin, bu oldukça verimsiz olur.

## Ağ Geçişini Engelleme

Anonimliği korumak için, I2P bittorrent istemcileri genellikle I2P
dışındaki duyuruları ya da eş bağlantıları desteklemez. I2P HTTP vekil
sunucuları genellikle duyuruları engeller. Bilinen bir Bittorrent
trafiği destekleyen SOCKS vekil sunucusu yok.

I2P olmayan istemcilerin bir HTTP vekil sunucusu aracılığıyla
kullanılmasını önlemek için, I2P izleyicileri genellikle bir
X-Forwarded-For HTTP üst bilgisi içeren erişimleri veya duyuruları
engeller. İzleyiciler, IPv4 veya IPv6 IP adresleri olan standart ağ
duyurularını reddetmeli ve bunları yanıt olarak aktarmamalıdır.

## PEX

I2P PEX is based on ut_pex. As there does not appear to be a formal
specification of ut_pex available, it may be necessary to review the
libtorrent source for assistance. It is an extension message, identified
as \"i2p_pex\" in [the extension
handshake](http://www.bittorrent.org/beps/bep_0010.html). It contains a
bencoded dictionary with up to 3 keys, \"added\", \"added.f\", and
\"dropped\". The added and dropped values are each a single byte string,
whose length is a multiple of 32 bytes. These byte strings are the
concatenated SHA-256 Hashes of the binary
[Destinations](#struct_Destination) of
the peers. This is the same format as the peers dictionary value in the
i2p compact response format specified above. The added.f value, if
present, is the same as in ut_pex.

## DHT

\"Dağıtılmış karma tablosu\" (DHT) desteği, 0.9.2 sürümünden başlayarak
i2psnark istemcisine eklenmiştir. [BEP
5](http://www.bittorrent.org/beps/bep_0005.html) ile öngörülen
farklılıklar aşağıda açıklanmıştır ve değişebilir. \"Dağıtılmış karma
tablosu\" (DHT) destekleyen bir istemci geliştirmek istiyorsanız I2P
geliştiricileri ile görüşün.

Standart \"Dağıtılmış karma tablosu\" (DHT) ile farklı olarak, I2P
\"Dağıtılmış karma tablosu\" (DHT), el sıkışma seçeneklerinde veya PORT
iletisinde bir bit kullanmaz. [Eklenti el
sıkışmasında](http://www.bittorrent.org/beps/bep_0010.html) \"i2p_dht\"
olarak tanımlanan bir eklenti iletisiyle tanıtılır. Her ikisi de tamsayı
olan \"port\" ve \"rport\" olmak üzere iki anahtarlı kodlanmış bir
sözlük içerir.



The UDP (datagram) port listed in the compact node info is used to
receive repliable (signed) datagrams. This is used for queries, except
for announces. We call this the \"query port\". This is the \"port\"
value from the extension message. Queries use
[I2CP]() protocol number 17.

In addition to that UDP port, we use a second datagram port equal to the
query port + 1. This is used to receive unsigned (raw) datagrams for
replies, errors, and announces. This port provides increased efficiency
since replies contain tokens sent in the query, and need not be signed.
We call this the \"response port\". This is the \"rport\" value from the
extension message. It must be 1 + the query port. Responses and
announces use [I2CP]() protocol number 18.

Kısa eş bilgisi 4 bayt IP + 2 bayt bağlantı noktası yerine 32 bayttır
(32 bayt SHA-256 karma). Eş bağlantı noktası yoktur. Bir yanıtta,
\"değerler\" anahtarı, her biri tek bir kısa eş bilgisi içeren
dizgelerin bir listesidir.

Kısa düğüm bilgisi, 20 bayt düğüm kodu + 4 bayt IP + 2 bayt bağlantı
noktası yerine 54 bayttır (20 bayt düğüm kodu + 32 bayt SHA-256
karması + 2 bayt bağlantı noktası). Bir yanıtta, \"düğümler\" anahtarı,
birleştirilmiş kısa düğüm bilgisini içeren tek baytlık bir dizgedir.

Güvenli düğüm kimliği gereksinimi: Çeşitli \"Dağıtılmış karma tablosu\"
(DHT) saldırılarını daha zor hale getirmek için, düğüm kimliğinin ilk 4
baytı, hedef karmasının ilk 4 baytı ile eşleşmelidir ve düğüm kimliğinin
sonraki iki baytı, hedef karmasının bağlantı noktası ile exclusive-ORed
değerinin sonraki iki baytı ile eşleşmelidir.

Bir torrent dosyasında, izleyicisiz torrent sözlüğü \"düğümler\"
anahtarı TBD\'dir. Bir sunucu dizgesi ve bir bağlantı noktası
tamsayısını içeren bir liste listesi yerine 32 baytlık ikili dizgelerin
(SHA-256 karmaları) bir listesi olabilir. Alternatifler: Birleştirilmiş
karmalara sahip tek bir bayt dizgesi ya da yalnızca dizgelerin bir
listesi.

## Veri Şeması (UDP) İzleyicileri

İstemcilerde ve izleyicilerde henüz UDP izleyici desteği bulunmuyor.
[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ile öngörülen
farklılıklar aşağıda açıklanmıştır ve değişebilir. Veri şeması
duyurularını destekleyen bir istemci veya izleyici geliştirmek
istiyorsanız, I2P geliştiricileri ile görüşün.

See [Proposal 160]().

## Ek Bilgiler

- I2P bittorrent standards are generally discussed on [](http:///).
- A chart of current tracker software capabilities is [also available
 there](http:///files/trackers.html).
- The [I2P bittorrent
 FAQ](http:///viewtopic.php?t=2068)
- [DHT on I2P discussion](http:///topics/812)


