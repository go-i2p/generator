 Streaming iletişim
kuralı 2024-09 0.9.64 

## Özet

The streaming library is technically part of the \"application\" layer,
as it is not a core router function. In practice, however, it provides a
vital function for almost all existing I2P applications, by providing a
TCP-like streams over I2P, and allowing existing apps to be easily
ported to I2P. The other end-to-end transport library for client
communication is the [datagram library]().

The streaming library is a layer on top of the core [I2CP
API]() that allows reliable, in-order, and
authenticated streams of messages to operate across an unreliable,
unordered, and unauthenticated message layer. Just like the TCP to IP
relationship, this streaming functionality has a whole series of
tradeoffs and optimizations available, but rather than embed that
functionality into the base I2P code, it has been factored off into its
own library both to keep the TCP-esque complexities separate and to
allow alternative optimized implementations.

İletilerin nispeten yüksek maliyeti göz önüne alındığında, Streaming
kitaplığının bu iletileri programlamak ve iletmek için kullandığı
iletişim kuralı, iletilen bireysel iletilerin olabildiğince çok bilgi
içermesini sağlayacak şekilde iyileştirilmiştir. Örneğin, Streaming
kitaplığı aracılığıyla vekil sunucu üzerinden geçirilen küçük bir HTTP
işlemi tek bir gidiş-dönüşte tamamlanabilir. İlk iletiler bir SYN, FIN
komutları ve küçük bir HTTP isteği yükünü birleştirir ve yanıt SYN, FIN,
ACK komutları ile HTTP yanıt yükü olur. HTTP sunucusuna SYN/FIN/ACK
komutlarının alındığını söylemek için ek bir ACK komutu iletilmesi
gerekirken, yerel HTTP vekil sunucusu genellikle tarayıcıya tam yanıtı
hemen teslim edebilir.

Streaming kitaplığı, kayan pencereleri, tıkanıklık kontrol algoritmaları
(hem yavaş başlatma hem de tıkanıklıktan kaçınma) ve genel paket
davranışı (ACK, SYN, FIN, RST, rto hesaplama, vb.) ile bir TCP
soyutlamasına çok benzer.

Streaming kitaplığı, I2P üzerinde çalışması için iyileştirilmiş sağlam
bir kitaplıktır. Kurulumu tek aşamalıdır ve tam bir pencereleme
uygulaması içerir.

## API

The streaming library API provides a standard socket paradigm to Java
applications. The lower-level [I2CP]() API is
completely hidden, except that applications may pass [I2CP
parameters](#options) through the streaming
library, to be interpreted by I2CP.

The standard interface to the streaming lib is for the application to
use the [I2PSocketManagerFactory]() to create
an [I2PSocketManager](). The application then
asks the socket manager for an [I2PSession](),
which will cause a connection to the router via
[I2CP](). The application can then setup
connections with an [I2PSocket]() or receive
connections with an [I2PServerSocket]().

Here are the [full streaming library Javadocs]().

İyi bir kullanım örneği için i2psnark koduna bakabilirsiniz.

### Ayarlar ve Varsayılanlar {#options}

The options and current default values are listed below. Options are
case-sensitive and may be set for the whole router, for a particular
client, or for an individual socket on a per-connection basis. Many
values are tuned for HTTP performance over typical I2P conditions. Other
applications such as peer-to-peer services are strongly encouraged to
modify as necessary, by setting the options and passing them via the
call to
[I2PSocketManagerFactory]().createManager(\_i2cpHost,
\_i2cpPort, opts). Time values are in ms.

Note that higher-layer APIs, such as [SAM](),
[BOB](), and
[I2PTunnel](), may override these defaults
with their own defaults. Also note that many options only apply to
servers listening for incoming connections.

0.9.1 sürümünden başlayarak, seçeneklerin tümü olmasa da çoğu etkin bir
soket yöneticisi veya oturumda değiştirilebilir. Ayrıntılı bilgi almak
için javadocs belgelerine bakabilirsiniz.

 Option Default Notes
 --------------------------------------------------- ------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 i2cp.accessList null Erişim listesi veya kara liste için kullanılan Base64 eş karmalarının virgül ya da boşluk ile ayrılmış listesi. As of release .
 i2cp.destination.sigType DSA_SHA1 Geliş bağlantıları için erişim listesi beyaz liste olarak kullanılsın. Geçici bir hedef için imza türünün adı veya numarası. As of release .
 i2cp.enableAccessList false Geliş bağlantıları için erişim listesi beyaz liste olarak kullanılsın. As of release .
 i2cp.enableBlackList false Geliş bağlantıları için erişim listesi kara liste olarak kullanılsın. As of release .
 i2p.streaming.answerPings true Gelen ping paketlerine yanıt verilip verilmeyeceği
 i2p.streaming.blacklist null Bağlamdaki TÜM hedeflerin geliş bağlantıları için kara listeye alınacak Base64 eş karmalarının virgül ya da boşluk ile ayrılmış listesi. Bu seçenek, createManager() options argümanında DEĞİL, bağlam özelliklerinden ayarlanmalıdır. Bunu yöneltici bağlamında ayarlamanın, ayrı bir JVM içindeki ve bağlamdaki yöneltici dışındaki istemcileri etkilemeyeceğini unutmayın. As of release .
 i2p.streaming.bufferSize 64K Henüz yazılmamış ne kadar iletim verisinin (bayt cinsinden) kabul edileceği.
 i2p.streaming.congestionAvoidanceGrowthRateFactor 1 Tıkanıklıktan kaçınma durumundayken pencere boyutunu `1/(windowSize*factor)` oranında büyütürüz. Standart TCP için pencere boyutları bayt cinsindendir, I2P üzerinde ise pencere boyutları iletilerdedir. Daha yüksek bir sayı, daha yavaş büyüme anlamına gelir.
 i2p.streaming.connectDelay -1 Yeni bir bağlantı başlattıktan sonra gerçekten bağlantı kurmaya çalışmadan önce ne kadar bekleneceği. Bu değer \<= 0 ise, başlangıç verisi olmadan hemen bağlantı kurulur. Değer 0 üzerindeyse, çıktı akışı temizlenene, ara bellek dolana veya bu kadar milisaniye geçene kadar bekleyin ve SYN komutuna herhangi bir başlangıç verisi ekleyin.
 i2p.streaming.connectTimeout 5\*60\*1000 Milisaniye cinsinden, bağlantının kurulurken ne kadar süreyle bloke edileceği. Negatif süresiz anlamına gelir. Varsayılan değer 5 dakikadır.
 i2p.streaming.disableRejectLogging false Bağlantı sınırları nedeniyle bir geliş bağlantısı reddedildiğinde günlüklerdeki uyarıların devre dışı bırakılıp bırakılmayacağı. As of release .
 i2p.streaming.dsalist null Alternatif bir DSA hedefi kullanılarak iletişim kurulacak Base64 eş karmalarının ya da ana bilgisayar adlarının virgül ya da boşluk ile ayrılmış listesi. Yalnızca çoklu oturum etkinleştirildiyse ve birincil oturum DSA değilse geçerlidir (genellikle yalnızca paylaşılan istemciler için). Bu seçenek, createManager() options argümanında DEĞİL, bağlam özelliklerinde ayarlanmalıdır. Bunu yöneltici bağlamında ayarlamanın, ayrı bir JVM içindeki ve bağlamdaki yöneltici dışındaki istemcileri etkilemeyeceğini unutmayın. As of release .
 i2p.streaming.enforceProtocol true Yalnızca Streaming iletişim kuralının dinlenip dinlenmeyeceği. True olarak ayarlamak, Hedeflerle 0.7.1 sürümünden (Mart 2009 tarihinde yayınlandı) önceki iletişimleri yasaklar. Bu hedefte birden çok iletişim kuralı çalıştırıyorsanız true olarak ayarlayın. As of release . Default true as of release 0.9.36.
 i2p.streaming.inactivityAction 2 (send) (0=bir şey yapma, 1=bağlantıyı kes) Hareketsizlik zaman aşımında yapılması gerekenler - bir şey yapmayın, bağlantıyı kesin ya da yinelenen bir onay gönderin.
 i2p.streaming.inactivityTimeout 90\*1000 Canlı tut komutu gönderilmeden önce beklenecek süre
 i2p.streaming.initialAckDelay 750 ACK komutu gönderilmeden önceki gecikme
 i2p.streaming.initialResendDelay 1000 Paket üst bilgisindeki yeniden gönderme gecikmesi alanının ilk değeri, çarpı 1000. Tam olarak kullanılmıyor. Aşağıya bakın.
 i2p.streaming.initialRTO 9000 Başlangıç zaman aşımı (kullanılabilecek [paylaşılan veri](#sharing) yoksa). As of release .
 i2p.streaming.initialRTT 8000 İlk gidiş dönüş süresi öngörüsü kullanılabilecek [paylaşılan veri](#sharing) yoksa). 0.9.8 sürümünden beri devre dışı bırakıldı; gerçek RTT kullanır.
 i2p.streaming.initialWindowSize 6 (kullanılabilecek [paylaşılan veri](#sharing) yoksa) Standart TCP için pencere boyutları bayt cinsindendir, I2P üzerinde ise pencere boyutları iletilerdedir.
 i2p.streaming.limitAction reset What action to take when an incoming connection exceeds limits. Valid values are: reset (reset the connection); drop (drop the connection); or http (send a hardcoded HTTP 429 response). Any other value is a custom response to be sent. backslash-r and backslash-n will be replaced with CR and LF. As of release .
 i2p.streaming.maxConcurrentStreams -1 (0 veya negatif değer sınırsız anlamına gelir) Geliş ve gidiş için birleşik toplam sınırdır.
 i2p.streaming.maxConnsPerMinute 0 Geliş bağlantısı sınırı (per peer; 0, devre dışı anlamına gelir) As of release .
 i2p.streaming.maxConnsPerHour 0 (per peer; 0 devre dışı anlamına gelir) As of release .
 i2p.streaming.maxConnsPerDay 0 (per peer; 0 devre dışı anlamına gelir) As of release .
 i2p.streaming.maxMessageSize 1730 Yükün en fazla boyutu, yani bayt cinsinden MTU.
 i2p.streaming.maxResends 8 Başarısız sayılmadan önce en fazla yeniden aktarım sayısı.
 i2p.streaming.maxTotalConnsPerMinute 0 Geliş bağlantısı sınırı (all peers; 0, devre dışı anlamına gelir) As of release .
 i2p.streaming.maxTotalConnsPerHour 0 (all peers; 0 devre dışı anlamına gelir) Bunu aşmak bir sunucuyu uzun süre devre dışı bırakacağından dikkatli kullanın. As of release .
 i2p.streaming.maxTotalConnsPerDay 0 (all peers; 0 devre dışı anlamına gelir) Bunu aşmak bir sunucuyu uzun süre devre dışı bırakacağından dikkatli kullanın. As of release .
 i2p.streaming.maxWindowSize 128 
 i2p.streaming.profile 1 (bulk) 1=bulk; 2=interactive; see important notes [below](#profile).
 i2p.streaming.readTimeout -1 Milisaniye cinsinden, okunurken ne kadar süreyle bloke edileceği. Negatif süresiz anlamına gelir.
 i2p.streaming.slowStartGrowthRateFactor 1 Yavaş başlatma durumundayken pencere boyutunu `1/(factor)` oranında büyütürüz. Standart TCP için pencere boyutları bayt cinsindendir, I2P üzerinde ise pencere boyutları iletilerdedir. Daha yüksek bir sayı, daha yavaş büyüme anlamına gelir.
 i2p.streaming.tcbcache.rttDampening 0.75 Ref: RFC 2140. Kayan nokta değeri. Bağlantı seçenekleriyle değil, yalnızca bağlam özellikleriyle ayarlanabilir. As of release .
 i2p.streaming.tcbcache.rttdevDampening 0.75 Ref: RFC 2140. Kayan nokta değeri. Bağlantı seçenekleriyle değil, yalnızca bağlam özellikleriyle ayarlanabilir. As of release .
 i2p.streaming.tcbcache.wdwDampening 0.75 Ref: RFC 2140. Kayan nokta değeri. Bağlantı seçenekleriyle değil, yalnızca bağlam özellikleriyle ayarlanabilir. As of release .
 i2p.streaming.writeTimeout -1 Milisaniye cinsinden, yazılırken/boşaltılırken ne kadar süreyle bloke edileceği. Negatif süresiz anlamına gelir.

## İletişim Kuralı Teknik Özellikleri

[Streaming kitaplığı teknik özellikleri sayfasına
bakın.]()

## Uygulama Ayrıntıları

### Kurulum

Başlatıcı, SYNCHRONIZE işaret kümesi ile bir paket gönderir. Bu pakette
ilk veriler de bulunabilir.\
Karşıdaki eş, SYNCHRONIZE işaret kümesi ile bir paketle yanıt verir. Bu
pakette ilk yanıt verileri de bulunabilir.

Başlatıcı, SYNCHRONIZE yanıtını almadan önce ilk pencere boyutuna kadar
ek veri paketleri gönderebilir. Bu paketler ayrıca gönderme akış kimliği
alanını 0 olarak ayarlar. Alıcılar, bilinmeyen akışlarda alınan
paketleri, SYNCHRONIZE paketinden önce düzensiz sırada alabileceğinden
kısa bir süre için ara belleğe almalıdır.

### MTU Seçimi ve Uzlaşma

En büyük ileti boyutu (MTU / MRU olarak da adlandırılır), iki eş
arasında desteklenen daha düşük değere göre belirlenir. Tünel iletileri
1 KB olarcak şekilde doldurulduğundan, zayıf bir MTU seçimi büyük
miktarda ek yüke yol açar. MTU, i2p.streaming.maxMessageSize seçeneğiyle
belirtilir. Var olan varsayılan 1730 MTU değeri, tipik durum için ek yük
ile birlikte iki 1K I2NP tünel iletisine tam olarak uyacak şekilde
seçilmiştir. Note: This is the maximum size of the payload only, not
including the header.

Note: For ECIES connections, which have reduced overhead, the
recommended MTU is 1812. The default MTU remains 1730 for all
connections, no matter what key type is used. Clients must use the
minimum of the sent and received MTU, as usual. See proposal 155.

Bir bağlantıdaki ilk iletide, akış katmanı tarafından eklenen 387
baytlık (tipik) bir hedef ve genellikle yöneltici tarafından Garlic
iletisinde paketlenmiş 898 baytlık (tipik) bir \"Kiralama kümesi\"
(LeaseSet) ile oturum anahtarları bulunur. (Daha önce bir ElGamal
oturumu kurulmuşsa, \"Kiralama kümesi\" (LeaseSet) ve oturum anahtarları
paketlenmez). Bu nedenle, her zaman tam bir HTTP isteğini tek bir 1KB
I2NP iletisine uydurma hedefine ulaşılamaz. Bununla birlikte, tünel ağ
geçidi işlemcisinde parçalanma ve gruplama stratejilerinin dikkatli bir
şekilde uygulanmasıyla birlikte MTU değerinin seçimi, özellikle uzun
ömürlü bağlantılar için ağ bant genişliği, gecikme süresi, güvenilirlik
ve verimlilik açısından önemli faktörlerdir.

### Veri Bütünlüğü

Data integrity is assured by the gzip CRC-32 checksum implemented in
[the I2CP layer](#format). There is no checksum
field in the streaming protocol.

### Paket Kapsülleme

Each packet is sent through I2P as a single message (or as an individual
clove in a [Garlic Message]()). Message
encapsulation is implemented in the underlying
[I2CP](), [I2NP](), and
[tunnel message]() layers. There is no
packet delimiter mechanism or payload length field in the streaming
protocol.

### İsteğe Bağlı Gecikme

Veri paketlerinde, alıcının paketi onaylamasından önce, istenilen
gecikmeyi ms cinsinden belirten bir isteğe bağlı gecikme alanı
bulunabilir. Geçerli değerler 0 ile 60000 arasındadır. 0 değeri anında
onay ister. Bu yalnızca bir öneridir ve alıcılar, ek paketlerin tek
seferde onaylanabilmesi için biraz gecikmelidir. Bazı uygulamalarda bu
alanda (ölçülen RTT/2) bir öneri değeri bulunabilir. Sıfır olmayan
isteğe bağlı gecikme değerleri için, alıcılar bir onay göndermeden önce
en fazla gecikmeyi en çok birkaç saniye ile sınırlamalıdır. 60000
üzerinde isteğe bağlı gecikme değerleri boğulmayı gösterir. Ayrıntılı
bilgi almak için aşağıya bakın.

### Alma Penceresi ve Kısma

TCP üst bilgilerinde, bayt cinsinden alma penceresi bulunur. Streaming
iletişim kuralında bir alma penceresi bulunmaz. Yalnızca basit bir
kısma/açma göstergesi kullanılır. Her uç nokta, bayt veya paket olarak
uzak uçtaki alma penceresine ilişkin kendi öngörüsünü korumalıdır. Alıcı
uygulamaları için önerilen en az ara bellek 128 paket veya 217 KB
boyutundadır (yaklaşık 128x1730). I2P ağ gecikmesi, paket kayıpları ve
bunun sonucunda oluşan tıkanıklık denetimi nedeniyle, bu boyuttaki bir
ara bellek nadiren doldurulur. Ancak, yüksek bant genişliğine sahip
\"yerel geri döngü\" (aynı yöneltici) bağlantılarında taşma oluşabilir.

Taşma koşullarını hızlı bir şekilde belirtmek ve sorunsuz bir şekilde
kurtarmak için Streaming iletişim kuralında basit bir geri bildirim için
yöntemi vardır. 60001 ya da daha yüksek değerde isteğe bağlı gecikme
alanına sahip bir paket alınırsa, bu \"kısma\" veya alma penceresinin
sıfır olduğunu gösterir. 60000 veya daha düşük değerde isteğe bağlı
gecikme alanına sahip bir paket \"açmayı\" gösterir. İsteğe bağlı
gecikme alanı olmayan paketler, kısma/açma durumunu etkilemez.

Tıkandıktan sonra, olası kayıp açılmamış paketleri telafi etmek için ara
sıra \"yoklama\" veri paketleri dışında, vericinin tıkanması açılana
kadar veri içeren başka paket gönderilmemelidir. Tıkanmış uç nokta, TCP
üzerinde olduğu gibi araştırmayı kontrol etmek için bir \"kalıcı
zamanlayıcı\" başlatmalıdır. Açılan uç nokta, bu alan kümesi ile birkaç
paket göndermeli veya veri paketleri yeniden alınana kadar bunları
belirli aralıklarla göndermeyi sürdürmelidir. Tıkanıklığın çözülmesi
için beklenecek en fazla süre uygulamaya bağlıdır. Açıldıktan sonra
verici penceresi boyutu ve tıkanıklık denetimi stratejisi uygulamaya
bağlıdır.

### Tıkanıklık Denetimi

Streaming kitaplığı, üstel geri çekilme ile standart yavaş başlangıç
(üstel pencere büyümesi) ve tıkanıklıktan kaçınma (doğrusal pencere
büyümesi) aşamalarını kullanır. Pencereleme ve bildirimler, bayt
sayısını değil paket sayısını kullanır.

### Kapatma

SYNCHRONIZE işaret kümesi ile birlikte herhangi bir pakette CLOSE
işareti de gönderilebilir. Eş CLOSE işaretiyle yanıt verene kadar
bağlantı kapatılmaz. CLOSE paketleri de veri içerebilir.

### Ping / Pong

I2CP katmanında (ICMP echo eşdeğeri) veya veri şemalarında ping işlevi
yoktur. Bu işlev akışta sağlanır. Ping ve pong standart bir akış
paketiyle birleştirilemez; ECHO seçeneği ayarlanmışsa, diğer birçok
işaret, seçenek, ackThrough, sequenceNum, NACK gibi şeyler yok sayılır.

Bir ping paketinin ECHO, SIGNATURE_INCLUDED ve FROM_INCLUDED işaretleri
ayarlanmış olmalıdır. sendStreamId sıfırdan büyük olmalıdır ve
alıcıStreamId yok sayılır. sendStreamId, var olan bir bağlantıya
karşılık gelebilir veya gelmeyebilir.

Bir pong paketinin ECHO işlaretinin ayarlanmış olması gerekir.
sendStreamId sıfır olmalıdır ve alıcıStreamId, ping ile gelen
sendStreamId olur. 0.9.18 sürümünden önce, pong paketinde, ping içinde
bulunan herhangi bir yük bulunmaz.

0.9.18 sürümünden başlayarak, ping ve pong içinde bir yük içerebilir.
Ping içindeki en fazla 32 bayta kadar olan yük, pong içinde döndürülür.

Streaming üzerinde, i2p.streaming.answerPings=false yapılandırmasıyla
pong gönderme devre dışı bırakılabilir.

### i2p.streaming.profile Notes {#profile}

This option supports two values; 1=bulk and 2=interactive. The option
provides a hint to the streaming library and/or router as to the traffic
pattern that is expected.

\"Bulk\" means to optimize for high bandwidth, possibly at the expense
of latency. This is the default. \"Interactive\" means to optimize for
low latency, possibly at the expense of bandwidth or efficiency.
Optimization strategies, if any, are implementation-dependent, and may
include changes outside of the streaming protocol.

Through API version 0.9.63, Java I2P would return an error for any value
other than 1 (bulk) and the tunnel would fail to start. As of API
0.9.64, Java I2P ignores the value. Through API version 0.9.63, i2pd
ignored this option; it is implemented in i2pd as of API 0.9.64.

While the streaming protocol includes a flag field to pass the profile
setting to the other end, this is not implemented in any known router.

### Denetim Bloğunu Paylaşma {#sharing}

Streaming kitaplığı, \"TCP\" Kontrol Bloğu paylaşımını destekler. Bu
paylaşımda, aynı uzak eşe bağlantılar arasında üç önemli Streaming
kitaplığı parametresi (pencere boyutu, gidiş dönüş süresi, gidiş dönüş
süresi farkı) bulunur. Bu paylaşım, bağlantı sırasında \"toplu\"
paylaşım için değil, bağlantı açma/kapama zamanında \"geçici\" paylaşım
için kullanılır (Bkz. 1RFC 21401). Aynı yöneltici üzerindeki diğer
hedeflere bilgi sızıntısı olmaması için ConnectionManager başına (yani
yerel hedef başına) ayrı bir paylaşım bulunur. Belirli bir eş için
paylaşım verilerinin süresi birkaç dakika sonra sona erer. Her yöneltici
için aşağıdaki kontrol bloğu paylaşımı parametreleri ayarlanabilir:

- RTT_DAMPENING = 0.75
- RTTDEV_DAMPENING = 0.75
- WINDOW_DAMPENING = 0.75

### Diğer Parametreler {#other}

Aşağıdaki parametreler sabit kodlanmıştır, ancak inceleme için ilgi
çekici olabilir:

- MIN_RESEND_DELAY = 100 ms (minimum RTO)
- MAX_RESEND_DELAY = 45 sec (maximum RTO)
- MIN_WINDOW_SIZE = 1
- TREND_COUNT = 3
- MIN_MESSAGE_SIZE = 512 (minimum MTU)
- INBOUND_BUFFER_SIZE = maxMessageSize \* (maxWindowSize + 2)
- INITIAL_TIMEOUT (valid only before RTT is sampled) = 9 sec
- \"alpha\" ( RTT dampening factor as per RFC 6298 ) = 0.125
- \"beta\" ( RTTDEV dampening factor as per RFC 6298 ) = 0.25
- \"K\" ( RTDEV multiplier as per RFC 6298 ) = 4
- PASSIVE_FLUSH_DELAY = 175 ms
- Maximum RTT estimate: 60 sec

### Geçmiş

Streaming kitaplığı I2P için organik olarak büyüdü - ilk önce mihi,
I2PTunnel üzerinde bir parça olarak \"mini streaming kitaplığını\"
uyguladı. Bu pencere boyutu 1 ileti ile sınırlıydı (bir sonraki iletiyi
göndermeden önce bir ACK gerekiyordu). Ardından yeniden düzenlendi genel
bir akış arayüzüne (TCP soketlerini yansıtma) ve tam akış uygulaması,
yüksek bant genişliği x gecikme ürününü hesaba katacak şekilde kayan bir
pencere iletişim kuralı ve iyileştirmeler yapıldı. Bireysel akışlar, en
fazla paket boyutunu ve diğer seçenekleri ayarlayabilir. Varsayılan
ileti boyutu, tam olarak iki 1K I2NP tünel iletisine uyacak şekilde
seçilir ve kayıp iletilerin yeniden iletilmesinin bant genişliği
maliyetleri ile birden fazla iletinin gecikmesi ve ek yükü arasında
makul bir denge sağlar.

## Gelecekte Yapılacak Çalışmalar {#future}

Streaming kitaplığının davranışının, uygulama düzeyinde başarım üzerinde
etkisi büyüktür ve bu nedenle, daha fazla inceleme için önemli bir
alandır.

- Streaming kitaplığı parametrelerinin ayrıca ayarlanması gerekebilir.
- Another area for research is the interaction of the streaming lib
 with the NTCP and SSU transport layers. See [the NTCP discussion
 page]() for details.
- Yöneltme algoritmalarının Streaming kitaplığı ile etkileşiminin,
 başarım üzerinde önemli bir etkisi vardır. Özellikle, iletilerin bir
 havuzdaki birden çok tünele rastgele dağıtılması, aksi durumda
 olacağından daha küçük pencere boyutlarıyla sonuçlanan yüksek
 derecede sıra dışı teslimata yol açar. Yöneltici şu anda tek bir
 nereden/nereye hedef çifti için iletileri, tünelin süresi dolana
 veya teslimat hatası oluşana kadar tutarlı bir tünel kümesi
 üzerinden yöneltir. Olası iyileştirmeler için yönelticisi sorunları
 ve tünel seçim algoritmaları gözden geçirilmelidir.
- İlk SYN paketindeki veriler, alıcının MTU değerini aşabilir.
- DELAY_REQUESTED alanı daha fazla kullanılabilir.
- Kısa ömürlü akışlarda yinelenen ilk SYNCHRONIZE paketleri
 tanınmadığından kaldırılabilir.
- Yeniden aktarımda MTU verisini göndermeyin.
- Gidiş penceresi dolu olmadığı sürece veriler birlikte gönderilir.
 (yani, no-Nagle ya da TCP_NODELAY) Büyük olasılıkla bunun için bir
 yapılandırma seçeneği bulunmalıdır.
- zzz, paketleri wireshark uyumlu (pcap) biçimde günlüğe kaydetmek
 için Streaming kitaplığına hata ayıklama kodu ekledi. Başarımı daha
 fazla incelemek için bunu kullanın. Daha fazla Streaming kitaplığı
 parametresini TCP alanlarıyla eşleştirmek için biçimi geliştirmek
 gerekebilir.
- Streaming kitaplığını standart TCP (veya belki de ham yuvalarla
 birlikte boş bir katman) ile değiştirmek için öneriler var. Bunu
 yapmak, ne yazık ki Streaming kitaplığı ile uyumsuz olur. Ancak
 ikisinin başarımını karşılaştırmak iyi olur.


