 Garlic Yöneltme 2014 Mart 0.9.12 

## Garlic Yöneltme ve \"Garlic\" Terminolojisi

\"Garlic yöneltme\" ve \"garlic şifreleme\" terimleri, I2P
teknolojisinden bahsederken genellikle oldukça gevşek bir şekilde
kullanılır. Burada terimlerin tarihçesini, çeşitli anlamlarını ve
\"garlic\" yöntemlerinin I2P içindeki kullanımını açıklıyoruz.

\"Garlic yöneltme\" ilk olarak [Michael J.
Freedman](http://www.cs.princeton.edu/~mfreed/) tarafından Roger
Dingledine\'nin Free Haven [Yüksek Lisans
tezinin](http://www.freehaven.net/papers.html) 8.1.1 bölümündeki
(Haziran 2000), [Onion yöneltmeden](http://www.onion-router.net/)
türetilmiştir.

\"Garlic\" Freedman\'ın tanımladığı gibi bir paketleme biçimi uyguladığı
ya da yalnızca Tor ile genel farklılıkları vurgulamak için özgün olarak
I2P geliştiricileri tarafından kullanılmış olabilir. Gerçek nedenleri
tarihte kaybolmuş olabilir. Genel olarak, I2P ağında \"garlic\" terimi
üç şeyden biri anlamına gelebilir:

1. Katmanlı Şifreleme
2. Bir kaç iletinin bir arada paketlenmesi
3. ElGamal/AES Şifrelemesi

Ne yazık ki, I2P geçen yedi yılda \"garlic\" terminolojisini her zaman
aynı kesinlikte kullanmadı. Bu nedenle okuyucu, bu terimle
karşılaştığında dikkatli olmalıdır. Umarım, aşağıdaki açıklama her şeyi
açıklığa kavuşturur.

### Katmanlı Şifreleme

Onion yöneltme, bir dizi eş aracılığıyla yollar veya tüneller oluşturmak
ve ardından bu tüneli kullanmak için kullanılan bir yöntemdir. İletiler,
oluşturucu tarafından üst üste şifrelenir ve ardından her sıçramada
şifresi çözülür. Tünel oluşturulurken, her bir eşte yalnızca bir sonraki
sıçramanın yöneltme yönergeleri açığa çıkar. İşlem sırasında, iletiler
tünelden geçirilir ve ileti ile yöneltme yönergeleri yalnızca tünelin uç
noktasında açığa çıkar.

This is similar to the way Mixmaster (see [network
comparisons]()) sends messages - taking a
message, encrypting it to the recipient\'s public key, taking that
encrypted message and encrypting it (along with instructions specifying
the next hop), and then taking that resulting encrypted message and so
on, until it has one layer of encryption per hop along the path.

Bu anlamda, genel bir kavram olarak \"garlic yöneltme\", \"onion
yöneltme\" ile aynıdır. I2P üzerinde uygulandığı gibi, elbette Tor
uygulamasına göre aşağıdaki gibi birkaç fark vardır. Öyle olsa bile, I2P
[onion yöneltme ve](http://www.onion-router.net/Publications.html), [Tor
ve benzeri karma ağlar üzerine yapılan çok sayıda akademik
araştırmadan](http://freehaven.net/anonbib/topic.html) yarar sağlar.

### Birkaç İletiyi Paketlemek

Michael Freedman, \"garlic yöneltmesini\", birden fazla iletinin bir
araya getirildiği onion yöneltmesinin geliştirilmiş bir şekli olarak
tanımladı. Her iletiye \"ampul\" dedi. Her biri kendi teslim
yönergelerini taşıyan tüm iletiler, uç noktada açığa çıkar. Böylece
özgün iletiyle onion yöneltmesi \"yanıt bloğu\" verimli bir şekilde
paketlenir.

Bu kavram I2P üzerinde aşağıda açıklandığı gibi uygulanır. Garlic
\"ampulleri\" için \"dişler\" terimini kullanıyoruz. Tek bir ileti
yerine herhangi bir sayıda ileti yer alabilir. Bu, Tor üzerinde
uygulanan onion yöneltmesine göre önemli bir farktır. Ancak, I2P ve Tor
arasındaki birçok önemli mimari farklılıktan yalnızca biridir. Belki de
tek başına terminoloji değişikliğini haklı çıkarmaya yeterli değildir.

Freedman tarafından açıklanan yönteme göre bir başka fark, yolun tek
yönlü olmasıdır. Onion yöneltme veya mixmaster yanıt bloklarında
görüldüğü gibi, algoritmayı büyük ölçüde basitleştirerek daha esnek ve
güvenilir aktarım sağlayan bir \"dönüm noktası\" yoktur.

### ElGamal/AES Şifrelemesi

In some cases, \"garlic encryption\" may simply mean
[ElGamal/AES+SessionTag]() encryption
(without multiple layers).

## I2P içindeki \"Garlic\" Yöntemleri

Artık çeşitli \"garlic\" terimlerini tanımladığımıza göre, I2P garlic
yöneltmesinin paketleme ve şifreleme için üç yerde kullandığını
söyleyebiliriz:

1. Tüneller oluşturmak ve yöneltmek için (katmanlı şifreleme)
2. Uçtan uca ileti tesliminin (paketleme) başarısını veya
 başarısızlığını belirlemek için
3. Bazı ağ veri tabanı kayıtlarını yayınlamak için (başarılı bir trafik
 analizi saldırısı olasılığını azaltmak) (ElGamal/AES)

Bu yöntemin, ağın başarımını iyileştirmek, taşıma gecikmesinden/çıkış
takaslarından yararlanmak ve güvenilirliği artırmak için yedekli yollar
aracılığıyla verileri dallandırmak için kullanılabileceği önemli yolları
da vardır.

### Tünel Oluşturma ve Yöneltme

I2P üzerinde tüneller tek yönlüdür. Her bir taraf, biri gidiş ve biri
geliş trafiği için olmak üzere iki tünel oluşturur. Bu nedenle, tek bir
gidiş-dönüş iletisi ve yanıtı için dört tünel gerekir.

Tunnels are built, and then used, with layered encryption. This is
described on the [tunnel implementation
page](). Tunnel building details are defined
on [this page](). We use
[ElGamal/AES+SessionTag]() for the
encryption.

Tunnels are a general-purpose mechanism to transport all [I2NP
messages](), and [Garlic
Messages](#msg_Garlic) are not used to build
tunnels. We do not bundle multiple [I2NP
messages]() into a single [Garlic
Message](#msg_Garlic) for unwrapping at the
outbound tunnel endpoint; the tunnel encryption is sufficient.

### Uçtan Uca İleti Paketleme

At the layer above tunnels, I2P delivers end-to-end messages between
[Destinations](#struct_Destination).
Just as within a single tunnel, we use
[ElGamal/AES+SessionTag]() for the
encryption. Each client message as delivered to the router through the
[I2CP interface]() becomes a single [Garlic
Clove](#struct_GarlicClove) with its own
[Delivery
Instructions](#struct_GarlicCloveDeliveryInstructions),
inside a [Garlic Message](#msg_Garlic).
Delivery Instructions may specify a Destination, Router, or Tunnel.

Genellikle, bir Garlic iletisinde yalnızca bir diş bulunur. Bununla
birlikte yöneltici Garlic iletisinde düzenli olarak pakete iki diş daha
ekler:

![Garlic Message
Cloves](/_static/images/garliccloves.png "Garlic Message Cloves"){style="text-align:center;"}

1. A [Delivery Status
 Message](#msg_DeliveryStatus), with
 [Delivery
 Instructions](#struct_GarlicCloveDeliveryInstructions)
 specifying that it be sent back to the originating router as an
 acknowledgment. This is similar to the \"reply block\" or \"reply
 onion\" described in the references. It is used for determining the
 success or failure of end to end message delivery. The originating
 router may, upon failure to receive the Delivery Status Message
 within the expected time period, modify the routing to the far-end
 Destination, or take other actions.
2. A [Database Store
 Message](#msg_DatabaseStore), containing a
 [LeaseSet](#struct_LeaseSet) for
 the originating Destination, with [Delivery
 Instructions](#struct_GarlicCloveDeliveryInstructions)
 specifying the far-end destination\'s router. By periodically
 bundling a LeaseSet, the router ensures that the far-end will be
 able to maintain communications. Otherwise the far-end would have to
 query a floodfill router for the network database entry, and all
 LeaseSets would have to be published to the network database, as
 explained on the [network database page]().

By default, the Delivery Status and Database Store Messages are bundled
when the local LeaseSet changes, when additional [Session
Tags](#type_SessionTag) are delivered,
or if the messages have not been bundled in the previous minute. As of
release 0.9.2, the client may configure the default number of Session
Tags to send and the low tag threshold for the current session. See the
[I2CP options specification](#options) for
details. The session settings may also be overridden on a per-message
basis. See the [I2CP Send Message Expires
specification](#msg_SendMessageExpires) for
details.

Açıkçası, ek iletiler şu anda genel amaçlı bir yöneltme şemasının
parçası olarak değil, belirli amaçlar için paketlenmiştir.

0.9.12 sürümünden başlayarak, teslimat durumu iletisi, içeriğin
şifrelenmesi ve dönüş yolundaki yönelticiler tarafından görülmemesi için
gönderici tarafından başka bir garlic iletisine sarılır.

### Otomatik doldurma Ağ veri tabanına depolama

As explained on the [network database
page](#delivery), local
[LeaseSets](#struct_LeaseSet) are sent
to floodfill routers in a [Database Store
Message](#msg_DatabaseStore) wrapped in a
[Garlic Message](#msg_Garlic) so it is not
visible to the tunnel\'s outbound gateway.

## Gelecekte Yapılacak Çalışmalar

The Garlic Message mechanism is very flexible and provides a structure
for implementing many types of mixnet delivery methods. Together with
the unused delay option in the [tunnel message Delivery
Instructions](#struct_TunnelMessageDeliveryInstructions),
a wide spectrum of batching, delay, mixing, and routing strategies are
possible.

Özellikle, gidiş tüneli uç noktasında çok daha fazla esneklik
potansiyeli vardır. İletiler büyük olasılıkla oradan birkaç tünelden
birine yöneltilebilir (böylece noktadan noktaya bağlantılar en aza
indirilir) ya da yedeklilik veya ses ve görüntü akışı için birkaç tünel
ile çok noktaya yayın yapılabilir.

Bu tür deneyler, belirli yöneltme yollarının sınırlandırılması, çeşitli
yollar boyunca iletilebilecek I2NP iletilerinin türlerinin kısıtlanması
ve belirli ileti geçerlilik sürelerinin uygulanması gibi güvenlik ve
anonimlik sağlama gereksinimiyle çelişebilir.

As a part of [ElGamal/AES encryption](), a
garlic message contains a sender specified amount of padding data,
allowing the sender to take active countermeasures against traffic
analysis. This is not currently used, beyond the requirement to pad to a
multiple of 16 bytes.

Encryption of additional messages to and from the [floodfill
routers](#delivery).

## Referanslar

- Garlic yöneltme terimi ilk olarak Roger Dingledine\'in Free Haven
 [Michael J. Freedman](http://www.cs.princeton.edu/~mfreed/)
 tarafından yazılmış olan [Yüksek lisans
 tezinde](http://www.freehaven.net/papers.html) (Haziran 2000) 8.1.1
 bölümünde kullanılmıştır.
- [Onion yöneltme
 yayınları](http://www.onion-router.net/Publications.html)
- [Wikipedia Üzerinde Onion
 Yöneltme](http://en.wikipedia.org/wiki/Onion_routing)
- [Wikipedia Üzerinde Garlic
 Yöneltme](http://en.wikipedia.org/wiki/Garlic_routing)
- [I2P Meeting 58]() (2003) discussing the
 implementation of garlic routing
- [Tor](https://www.torproject.org/)
- [Free Haven yayınları](http://freehaven.net/anonbib/topic.html)
- Onion yöneltme ilk olarak 1996 yılında David M. Goldschlag,
 Michael G. Reed ve Paul F. Syverson tarafından [Hiding Routing
 Information](http://www.onion-router.net/Publications/IH-1996.pdf)
 içinde tanımlanmıştır.


