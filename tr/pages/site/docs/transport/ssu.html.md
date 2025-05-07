 Güvenli Yarı
Güvenilir UDP (SSU) 2025-01 0.9.64 

**DEPRECATED** - SSU has been replaced by SSU2. SSU support was removed
from i2pd in release 2.44.0 (API 0.9.56) 2022-11. SSU support was
removed from Java I2P in release 2.4.0 (API 0.9.61) 2023-12.

SSU (also called \"UDP\" in much of the I2P documentation and user
interfaces) was one of two [transports]()
implemented in I2P. The other is [NTCP2]().
Support for [NTCP]() has been removed.

SSU, I2P 0.6 sürümünde tanıtıldı. Standart bir I2P kurulumunda
yöneltici, gidiş bağlantılar için hem NTCP hem de SSU kullanır. IPv6
üzerinden SSU, 0.9.8 sürümünden başlayarak destekleniyor.

SSU \"yarı güvenilir\" olarak anılır, çünkü onaylanmayan iletileri en
fazla sınır sayısına ulaşana kadar yeniden ve yeniden iletir. İleti
ancak bundan sonra atılır.

## SSU Hizmetleri

NTCP taşıyıcısı gibi, SSU taşıyıcısı da güvenilir, şifrelenmiş,
bağlantıya odaklı, noktadan noktaya veri aktarımı sağlar. SSU taşıyıcısı
ek olarak, aşağıdakiler ile birlikte IP adresi algılama ve NAT aktarım
hizmetleri de sağlar:

- [Tanıtıcıları](#introduction) kullanarak işbirlikli NAT/Güvenlik
 duvarı geçişi
- Gelen paketlerin incelenmesi ve [eş sınaması](#peerTesting) ile
 yerel IP adresi algılaması
- Güvenlik duvarı durumu ve yerel IP iletişimi ve her ikisi için de
 NTCP üzerinde değişiklik yapılması
- Güvenlik duvarı durumu ve yerel IP adresi iletişimi ile yöneltici ve
 kullanıcı arabiriminde değişiklikler yapar

## [Yöneltici Adresi Teknik Özellikleri]{#ra}

Ağ veri tabanında aşağıdaki özellikler depolanır.

**Transport name:** SSU

**caps:** \[B,C,4,6\] [See below](#capabilities).

**host:** IP (IPv4 or IPv6). Shortened IPv6 address (with \"::\") is
allowed. May or may not be present if firewalled. Host names were
previously allowed, but are deprecated as of release 0.9.32. See
proposal 141.

**iexp\[0-2\]:** Expiration of this introducer. ASCII digits, in seconds
since the epoch. Only present if firewalled, and introducers are
required. Optional (even if other properties for this introducer are
present). As of release 0.9.30, proposal 133.

**ihost\[0-2\]:** Introducer\'s IP (IPv4 or IPv6). Host names were
previously allowed, but are deprecated as of release 0.9.32. See
proposal 141. Shortened IPv6 address (with \"::\") is allowed. Only
present if firewalled, and introducers are required.

SSU taşıyıcısının yarı güvenilir aktarım gereksinimi, TCP dostu
çalışması ve yüksek çıkış kapasitesi sağlaması, tıkanıklık denetiminde
büyük bir serbestlik sağlar. Aşağıda özetlenen tıkanıklık denetimi
algoritmasının hem bant genişliği açısından verimli olması hem de basit
şekilde uygulanması amaçlanmıştır.

Paketler, yönelticinin gidiş kapasitesini aşmamaya veya uzak eşin
ölçülen kapasitesini aşmamaya özen göstererek yöneltici ilkesine göre
programlanır. Ölçülen kapasite, TCP üzerindeki yavaş başlatma ve
tıkanıklıktan kaçınma sınırlarına göre çalışır. Gönderme kapasitesinde
ek artış ve tıkanıklık durumunda çarpımsal azaltma özellikleri bulunur.
TCP iletişim kuralından farklı olarak, yönelticiler belirli bir süre
veya sayıda yeniden iletimden sonra diğer iletileri aktarmayı
sürdürürken bazı iletileri atabilir.

Tıkanıklık algılama teknikleri de TCP iletişim kuralından farklıdır. Her
iletinin kendine özgü ve sıralı olmayan bir tanımlayıcısı vardır ve her
iletinin boyutu sınırlıdır. En fazla 32KB olabilir. Bu geri bildirimi
göndericiye verimli bir şekilde iletmek için, alıcı düzenli olarak
tamamen onaylı (ACK) ileti tanımlayıcılarının bir listesini bulundurur
ve ayrıca kısmen alınan iletiler için bit alanları içerebilir. Burada
her bit bir parçanın alımını temsil eder. Yinelenen parçalar gelirse,
ileti yeniden onaylanmalı (ACK) ya da ileti hala tam olarak alınmadıysa,
bit alanı yeni güncellemelerle yeniden iletilmelidir.

Var olan uygulama, paketleri belirli bir boyuta doldurmaz. Bunun yerine
yalnızca tek bir ileti parçasını bir pakete yerleştirir ve gönderir (MTU
değerinin aşılmamasına dikkat edin).

### [MTU]{#mtu}

Yöneltici sürümü 0.8.12 ile başlayarak, IPv4 için iki MTU değeri
kullanılır: 620 ve 1484. MTU değeri, yeniden aktarılan paketlerin
yüzdesine göre ayarlanır.

Her iki MTU değeri için de (MTU % 16) == 12 olması istenir. Böylece 28
baytlık IP/UDP üst bilgisinden sonraki yük bölümü şifreleme amacıyla 16
baytın katı olur.

Küçük MTU değeri için, 2646 baytlık bir değişken tünel oluşturma
iletisinin birden çok pakete verimli bir şekilde paketlenmesi istenir.
620 bayt MTU ile 5 pakete güzelce sığar.

Ölçümlere dayanarak, 1492, neredeyse tüm makul küçük I2NP iletilerine
uyar (daha büyük I2NP iletileri, 1900 ile 4500 bayt arasında olabilir.
Bu da zaten canlı bir ağ MTU değerine sığmaz).

MTU değerleri, 0.8.9 - 0.8.11 sürümleri için 608 ve 1492 idi. Geniş MTU,
0.8.9 sürümünün yayınlanmasından önce 1350 idi.

En fazla alınan paket boyutu, 0.8.12 sürümünden başlayarak 1571 bayt
oldu. 0.8.9 - 0.8.11 sürümleri için 1535 bayttı. 0.8.9 sürümünden önce
2048 bayttı.

0.9.2 sürümünden itibaren, bir yönelticinin ağ arabirimi MTU değeri 1484
bayttan azsa, bunu ağ veri tabanında yayınlar ve bir bağlantı
kurulduğunda diğer yönelticiler buna saygı göstermelidir.

IPv6 için en az MTU değeri 1280 bayttır. IPv6 IP/UDP üst bilgisi 48
bayttır. Bu nedenle 1280 için doğru olan (MTN % 16 == 0) bir MTU
kullanırız. En fazla IPv6 MTU değeri 1488 bayttır (0.9.28 sürümünden
önce en fazla 1472 bayttır).

### [İleti Boyutu Sınırları]{#max}

En fazla ileti boyutu nominal olarak 32KB iken, pratik sınır farklıdır.
İletişim kuralı, parça sayısını 7 ya da 128 bit ile sınırlar. Ancak var
olan uygulama, her iletiyi, 608 MTU kullanıldığında 64 \* 534 = 33,3 KB
için yeterli olan en fazla 64 parça ile sınırlar. Birlikte verilen
\"Kiralama kümelerl\" (LeaseSets) ve oturum anahtarları için oluşan ek
yük nedeniyle, uygulama düzeyinde pratik sınır yaklaşık 6 KB daha düşük
veya yaklaşık 26 KB olur. UDP taşıyıcı sınırını 32KB üzerine çıkarmak
için daha fazla çalışma yapılması gerekiyor. Daha büyük MTU kullanan
bağlantılarda daha büyük iletiler kullanılabilir.

## Boşta Bekleme Zaman Aşımı

Boşta bekleme zaman aşımı ve bağlantı kapatmayı, her uç nokta kendi
belirler ve değişiklik gösterebilir. Geçerli uygulamada, bağlantı sayısı
yapılandırılan en fazla değere yaklaştıkça zaman aşımı azaltılır ve
bağlantı sayısı düşük olduğunda zaman aşımı artırılır. Önerilen en az
zaman aşımı iki dakika ve üzerindedir. Önerilen en fazla zaman aşımı on
dakika ve üzerindedir.

## [Anahtarlar]{#keys}

Kullanılan tüm şifreleme, 32 bayt anahtar ve 16 bayt \"Başlatma
vektörü\" (IV) ile AES256/CBC yöntemidir. Alice, Bob ile bir oturum
başlattığında, MAC ve oturum anahtarları üzerinde, Diffie-Hellman alış
verişinin bir parçası olarak uzlaşılır ve ardından bunlar sırasıyla HMAC
ve şifreleme için kullanılır. Diffie-Hellman alış verişi sırasında,
Bob\'un herkes tarafından bilinen introKey bilgisi MAC ve şifreleme için
kullanılır.

Hem ilk ileti hem de sonraki yanıt, yanıtlayanın (Bob) giriş anahtarını
kullanır. Yanıtlayanın, istekte bulunanın (Alice) giriş anahtarını
bilmesi gerekmez. Bob tarafından kullanılan DSA imzalama anahtarı,
Alice\'in DSA anahtarı Bob tarafından bilinmemesine rağmen, onunla
iletişim kurduğunda Alice tarafından zaten bilinmelidir.

Alıcı bir iletiyi aldıktan sonra, \"kimden\" IP adresini ve kurulu tüm
oturumlarla bağlantı noktasını denetler. Eşleşmeler varsa, bu oturumun
MAC anahtarları HMAC ile sınanır. Bunların hiçbiri doğrulamazsa veya
eşleşen IP adresi yoksa, alıcı MAC üzerinde introKey değerlerini dener.
Bu da doğrulamazsa, paket atılır. Doğrulanırsa, ileti türüne göre
yorumlanır, ancak alıcı aşırı yüklenirse yine de atılabilir.

Alice ve Bob\'un yerleşik bir oturumu varsa, ancak Alice herhangi bir
nedenle anahtarları kaybederse ve Bob ile iletişim kurmak isterse,
istediği zaman oturum isteği (SessionRequest) ve ilgili iletileri
kullanarak yeni bir oturum oluşturabilir. Bob anahtarı kaybetmişse ama
Alice bunu bilmiyorsa, ilk önce yanıt istiyor (WantReply) işareti
ayarlanmış bir veri iletisi (DataMessage) göndererek onu yanıt vermeye
zorlar ve Bob yanıt vermemeyi sürdürürse anahtarın kaybolduğunu
varsayarak yeniden yeni bir tane kurar.

For the DH key agreement, [RFC3526]() 2048bit
MODP group (#14) is used:

 p = 2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
 g = 2

These are the same p and g used for I2P\'s [ElGamal
encryption](#elgamal).

## [Yinelenmeyi engelleme]{#replay}

SSU katmanında yinelenme, aşırı eski zaman damgaları taşıyan veya bir IV
değerini yeniden kullanan paketlerin reddedilmesi ile engellenir.
Yinelenen IV değerlerini saptamak için, düzenli olarak \"eskitme\" yapan
bir dizi Bloom süzgeci ile yalnızca yeni eklenen IV değerleri ayıklanır.

Veri iletilerinde (DataMessage) kullanılan ileti kimlikleri, SSU
taşıyıcısının üzerindeki katmanlarda tanımlanır ve şeffaf bir şekilde
geçirilir. Bu kimlikler belirli bir sırada değildir. Aslında tamamen
rastgele olaiblirler. SSU katmanı, messageId için yinelenmeyi engellleme
girişiminde bulunmaz. Bu durumu daha yüksek katmanlar hesaba katmalıdır.

## Adresleme {#addressing}

Bir SSU eşi ile iletişim kurmak için iki bilgi grubundan biri
gereklidir: Eşe herkesin erişebildiği durumlarda doğrudan adres veya Eşi
tanıtmak için üçüncü bir tarafın kullanılacağı dolaylı bir adres. Bir
eşin sahip olabileceği adres sayısında herhangi bir kısıtlama yoktur.

 Direct: host, port, introKey, options Indirect: tag,
relayhost, port, relayIntroKey, targetIntroKey, options 

Adreslerin her biri, bir dizi seçeneği de ortaya çıkarabilir. O belirli
eşin özel yetenekleri olabilir. Kullanılabilen yeteneklerin listesi için
[aşağı](#capabilities) bakabilirsiniz.

The addresses, options, and capabilities are published in the [network
database]().

## [Doğrudan Oturum Kuruluşu]{#direct}

NAT geçişi için üçüncü taraf gerekmediğinde doğrudan oturum oluşturma
kullanılır. İleti sıralaması aşağıdaki gibidir:

### [Bağlantı kuruluşu (doğrudan)]{#establishDirect}

Alice doğrudan Bob ile bağlantı kurar. IPv6, 0.9.8 sürümünden başlayarak
desteklenir.

 Alice Bob SessionRequest
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-- SessionCreated
SessionConfirmed \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-- DeliveryStatusMessage
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-- DatabaseStoreMessage
DatabaseStoreMessage \-\-\-\-\-\-\-\-\-\-\-\-\-\--\> Data
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\> Data 

After the SessionConfirmed message is received, Bob sends a small
[DeliveryStatus message](#msg_DeliveryStatus)
as a confirmation. In this message, the 4-byte message ID is set to a
random number, and the 8-byte \"arrival time\" is set to the current
network-wide ID, which is 2 (i.e. 0x0000000000000002).

After the status message is sent, the peers usually exchange
[DatabaseStore messages](#msg_DatabaseStore)
containing their
[RouterInfos](#struct_RouterInfo),
however, this is not required.

Durum iletisinin türü veya içeriği önemli görünmüyor. En başta veri
tabanı kaydetme (DatabaseStore) iletisi birkaç saniye geciktiği için bu
eklenmişti. Artık kayıt hemen gönderildiğinden, durum iletisi
kaldırılabilir.

## [Giriş]{#introduction}

Giriş anahtarları, geleneksel olarak 0.9.47 sürümünden başlayarak
yöneltici karması ile aynı olan, ancak 0.9.48 sürümünden başlayarak
rastgele olabilecekleri bir dış kanal (ağ veri tabanı (netDB))
aracılığıyla aktarılır. Bunların bir oturum anahtarı oluştururken
kullanılmaları gerekir. Dolaylı adres için, eş ilk önce bir aktarıcı
sunucusuyla iletişim kurmalı ve ondan, verilen etiket altında bu
alktarıcı sunucusunun bildiği eşe bir giriş yapmasını istemelidir.
Olabiliyorsa aktarıcı sunucu adreslenen eşe istekte bulunan eşle
iletişim kurmasını söyleyen bir ileti gönderir ve ayrıca istekte bulunan
eşe, adreslenen eşin bulunduğu IP adresini ve bağlantı noktasını verir.
Ek olarak, bağlantıyı kuran eş, bağlandıkları eşin ortak anahtarlarını
zaten bilmelidir (ancak bu durum herhangi bir aracı aktarıcı eş için
gerekli değildir).

Etkin NAT geçişi için üçüncü taraf tanıtımı yoluyla dolaylı oturum
kurulması gereklidir. NAT veya güvenlik duvarının arkasındaki,
istenmeyen gelen UDP paketlerine izin vermeyen bir yöneltici olan
Charlie, önce birkaç eşle iletişim kurar ve bazılarını tanıtıcı olarak
hizmet etmek üzere seçer. Bu eşlerin (Bob, Bill, Betty, vb.) her biri
Charlie\'ye bir tanıtım etiketi sağlar (4 baytlık rastgele bir sayı) ve
daha sonra onunla iletişim kurma yöntemleri olarak herkese açık olarak
yayınlar. Charlie\'nin yayınlanmış iletişim yöntemlerini bilen bir
yöneltici olan Alice, önce bir ya da birkaç tanıtıcıya bir aktarıcı
isteği (RelayRequest) paketi gönderir ve her birinden onu Charlie ile
tanıştırmasını ister (Charlie\'yi tanımlamak için giriş etiketini
sunar). Bob daha sonra Alice\'in genel IP adresini ve bağlantı noktası
numarasını içeren bir aktarıcı girişi (RelayIntro) paketini Charlie\'ye
iletir, ardından Alice, Charlie\'nin herkese açık IP adresini ve
bağlantı noktası numarasını içeren bir aktarıcı yanıtı (RelayResponse)
paketini geri alır. Charlie aktarıcı yanıtı (RelayIntro) paketini
aldığında, Alice\'in IP adresine ve bağlantı noktasına küçük bir
rastgele paket gönderir (NAT/güvenlik duvarında bir delik açar) ve Alice
Bob\'un aktarıcı yanıtı (RelayResponse) paketini aldığında, belirtilen
IP adresi ve bağlantı noktası numarası ile yeni bir tam yönlü oturum
kurulumuna başlar.

### [Bağlantı kuruluşu (bir tanıtıcı kullanarak dolaylı)]{#establishIndirect}

Alice ilk önce, isteği Charlie\'ye ileten tanıtıcı Bob ile bağlantı
kurar.

 Alice Bob Charlie RelayRequest
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-- RelayResponse RelayIntro
\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
HolePunch (data ignored) SessionRequest
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
SessionCreated SessionConfirmed
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
DeliveryStatusMessage
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--
DatabaseStoreMessage DatabaseStoreMessage
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
Data
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
Data 

Delik açıldıktan sonra, doğrudan bir kuruluşta olduğu gibi Alice ve
Charlie arasında oturum kurulur.

### IPv6 Notes

IPv6 is supported as of version 0.9.8. Published relay addresses may be
IPv4 or IPv6, and Alice-Bob communication may be via IPv4 or IPv6.
Through release 0.9.49, Bob-Charlie and Alice-Charlie communication is
via IPv4 only. Relaying for IPv6 is supported as of release 0.9.50. See
the specification for details.

While the specification was changed as of version 0.9.8, Alice-Bob
communication via IPv6 was not actually supported until version 0.9.50.
Earlier versions of Java routers erroneously published the \'C\'
capability for IPv6 addresses, even though they did not actually act as
an introducer via IPv6. Therefore, routers should only trust the \'C\'
capability on an IPv6 address if the router version is 0.9.50 or higher.

## [Eş sınaması]{#peerTesting}

Eşler için işbirliğine dayalı erişilebilirlik sınamasının otomasyonu,
bir dizi eş sınaması (PeerTest) iletisi ile sağlanır. Düzgün
yürütülmesiyle, bir eş kendi erişilebilirliğini belirleyebilir ve
davranışını buna göre güncelleyebilir. Sınama süreci oldukça basittir:

 Alice Bob Charlie PeerTest
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
PeerTest\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--PeerTest
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--PeerTest
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--PeerTest
PeerTest\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--PeerTest


Eş sınaması (PeerTest) iletilerinin her biri, Alice tarafından
başlatıldığı gibi, sınama serisinin kendisini tanımlayan bir belirteç
(nonce) taşır. Alice, beklediği belirli bir iletiyi alamazsa, uygun
şekilde yeniden iletir ve alınan verilere ya da eksik iletilere göre
ulaşılabilirliğini belirler. Ulaşılabilecek çeşitli son durumlar şu
şekildedir:

- Alice, Bob\'dan yanıt almazsa, belirli bir sayıya ulaşana kadar
 yeniden iletir. Ancak yanıt gelmezse, Alive güvenlik duvarı veya NAT
 yapılandırmasının bir şekilde yanlış olduğunu anlar ve bir gidiş
 paketinin doğrudan yanıtı olsabile tüm gelen UDP paketlerini
 reddeder. Alternatif olarak, Bob çalışmıyor olabilir veya
 Charlie\'den yanıt alınmamasına yol açabilir.
- Alice, üçüncü bir taraftan (Charlie) beklenen belirteç (nonce) ile
 bir eş sınaması (PeerTest) iletisi almazsa, Alice, Bob\'un yanıtını
 zaten almış olsa bile, ilk isteğini Bob\'a belirli bir sayıya
 ulaşana kadar yeniden iletir. Charlie\'nin ilk iletisi hala
 iletilmiyor ancak Bob\'un iletisi geliyorsa, Alice istenmeyen
 bağlantı girişimlerini reddeden bir NAT veya güvenlik duvarı
 arkasında olduğunu ve bağlantı noktası yönlendirmenin düzgün
 çalışmadığını bilir (Bob\'un sunduğu IP ve bağlantı noktası
 iletilmelidir).
- Alice, Bob ve Charli\'den iki eş sınaması (PeerTest) iletisini de
 alırsa, ancak Bob\'un ve Charlie\'nin ikinci iletilerindeki ekteki
 IP adresi ve bağlantı noktası numaraları eşleşmiyorsa, Alice
 simetrik bir NAT arkasında olduğunu ve tüm giden paketlerinin
 iletişim kurduğu her eşe farklı \'kaynak\' bağlantı noktalarından
 gönderilecek şekilde yeniden yazdığını anlar. Bir bağlantı noktasını
 açıkça iletmesi ve daha fazla bağlantı noktası keşfini göz ardı
 ederek bu bağlantı noktasını her zaman uzaktan bağlantı için açıkta
 tutması gerekir.
- Alice, Charlie\'nin ilk iletisini alır ancak ikinci iletisini
 almazsa, eş sınaması (PeerTest) iletisini belirli bir sayıya ulaşana
 kadar Charlie\'ye yeniden iletir. Yanıt alamazsa, Charlie\'nin
 kafasının karıştığını veya artık çevrim içi olmadığını bilir.

Alice, Bob\'u eş sınamalarına katılabilecek gibi görünen tanıdık eşleri
arasından keyfi olarak seçmelidir. Bob sırayla Charlie\'yi eş
sınamalarına katılabilecek gibi görünen ve hem Bob hem de Alice\'den
farklı bir IP adresinde bulunan eşleri arasından keyfi olarak
seçmelidir. İlk hata koşulu oluşursa (Alice, Bob\'dan eş sınaması
(PeerTest) iletilerini almaz), Alice, Bob olarak yeni bir eş atamaya ve
farklı bir belirteç (nonce) ile yeniden denemeye karar verebilir.

Alice\'in tanıtım anahtarı, Charlie\'nin herhangi bir ek bilgi bilmeden
onunla iletişim kurabilmesi için tüm \"Eş sınaması\" (PeerTest)
iletilerinde bulunur.\
0.9.15 sürümünden başlayarak, sızdırma saldırılarını önlemek için
Alice\'in Bob ile kurulmuş bir oturumu olması gerekir.\
Eş sınamasının geçerli olması için Alice\'in Charlie ile kurulmuş bir
oturumu olmamalıdır.\
Alice, Charlie ile bir oturum kurabilir, ancak bu şart değildir.

### IPv6 Notes

Through release 0.9.26, only testing of IPv4 addresses is supported.
Only testing of IPv4 addresses is supported. Therefore, all Alice-Bob
and Alice-Charlie communication must be via IPv4. Bob-Charlie
communication, however, may be via IPv4 or IPv6. Alice\'s address, when
specified in the PeerTest message, must be 4 bytes. As of release
0.9.27, testing of IPv6 addresses is supported, and Alice-Bob and
Alice-Charlie communication may be via IPv6, if Bob and Charlie indicate
support with a \'B\' capability in their published IPv6 address. See
[Proposal 126](/spec/proposals/126-ipv6-peer-testing) for details.

Prior to release 0.9.50, Alice sends the request to Bob using an
existing session over the transport (IPv4 or IPv6) that she wishes to
test. When Bob receives a request from Alice via IPv4, Bob must select a
Charlie that advertises an IPv4 address. When Bob receives a request
from Alice via IPv6, Bob must select a Charlie that advertises an IPv6
address. The actual Bob-Charlie communication may be via IPv4 or IPv6
(i.e., independent of Alice\'s address type).

As of release 0.9.50, If the message is over IPv6 for an IPv4 peer test,
or (as of release 0.9.50) over IPv4 for an IPv6 peer test, Alice must
include her introduction address and port. See [Proposal
158](/spec/proposals/158) for details.

## [İletim penceresi, onaylar (ACK) ve yeniden iletimler]{#acks}

The DATA message may contain ACKs of full messages and partial ACKs of
individual fragments of a message. See the data message section of [the
protocol specification page]() for details.

The details of windowing, ACK, and retransmission strategies are not
specified here. See the Java code for the current implementation. During
the establishment phase, and for peer testing, routers should implement
exponential backoff for retransmission. For an established connection,
routers should implement an adjustable transmission window, RTT estimate
and timeout, similar to TCP or [streaming]().
See the code for initial, min and max parameters.

## [Güvenlik]{#security}

UDP kaynak adresleri tabi ki sahte olabilir. Ayrıca, belirli SSU
iletilerinde (RelayRequest, RelayResponse, RelayIntro, PeerTest) bulunan
IP adresleri ve bağlantı noktaları doğru olmayabilir. Bunun yanında
belirli işlemler ve yanıtlar için hız sınırlandırması uygulanması
gerekebilir.

Doğrulamanın ayrıntıları burada açıklanmamıştır. Uygulayıcılar uygun
yerlere savunmalar eklemelidir.

## [Eş yetenekleri]{#capabilities}

One or more capabilities may be published in the \"caps\" option.
Capabilities may be in any order, but \"BC46\" is the recommended order,
for consistency across implementations.

B
: Eş adresinde \'B\' yeteneği bulunuyorsa, bu, eş sınamalarına \'Bob\'
 veya \'Charlie\' olarak katılmaya istekli oldukları ve
 katılabilecekleri anlamına gelir. Through 0.9.26, peer testing was
 not supported for IPv6 addresses, and the \'B\' capability, if
 present for an IPv6 address, must be ignored. As of 0.9.27, peer
 testing is supported for IPv6 addresses, and the presence or absense
 of the \'B\' capability in an IPv6 address indicates actual support
 (or lack of support).

C
: If the peer address contains the \'C\' capability, that means they
 are willing and able to serve as an introducer via that address -
 serving as an introducer Bob for an otherwise unreachable Charlie.
 Prior to release 0.9.50, Java routers incorrectly published the
 \'C\' capability for IPv6 addresses, even though IPv6 introducers
 was not fully implemented. Therefore, routers should assume that
 versions prior to 0.9.50 cannot act as an introducer over IPv6, even
 if the \'C\' capability is advertised.

4
: As of 0.9.50, indicates outbound IPv4 capability. If an IP is
 published in the host field, this capability is not necessary. If
 this is an address with introducers for IPv4 introductions, \'4\'
 should be included. If the router is hidden, \'4\' and \'6\' may be
 combined in a single address.

6
: As of 0.9.50, indicates outbound IPv6 capability. If an IP is
 published in the host field, this capability is not necessary. If
 this is an address with introducers for IPv6 introductions, \'6\'
 should be included (not currently supported). If the router is
 hidden, \'4\' and \'6\' may be combined in a single address.

# [Gelecekte Yapılacak Çalışmalar]{#future}

Note: These issues will be addressed in the development of SSU2.

- Pencere boyutu ayarının ve diğer parametrelerin değerlendirilmesi ve
 başarımı artırmak için iletişim kuralı uygulamasının ayarlanması ile
 birlikte mevcut SSU başarımının analizi, gelecekte yapılabilecek bir
 çalışma konusudur.
- Geçerli uygulama aynı paketler için yeniden ve yeniden onay
 gönderir. Bu durum yükü gereksiz yere artırır.
- Varsayılan küçük MTU değeri olan 620 analiz edilmeli ve büyük
 olasılıkla artırılmalıdır. Geçerli MTU ayarlama stratejisi
 değerlendirilmelidir. 1730 baytlık bir akış lib paketi 3 küçük SSU
 paketine sığar mı? Büyük olasılıkla hayır.
- İletişim kuralı, kurulum sırasında MTU değerlerini alıp verecek
 şekilde geliştirilmelidir.
- Yeniden anahtarlama şu anda uygulanmıyor ve asla uygulanamayacak.
- Yöneltici girişi (RelayIntro) ve yöneltici yanıtı (RelayResponse)
 iletilerindeki \'soru (challenge)\' alanlarının olası kullanımı ve
 oturum isteği (SessionRequest) ve oturum oluşturuldu
 (SessionCreated) iletilerindeki dolgu ekleme (padding) alanının
 kullanımı belgelenmemiştir.
- Verilerin parçalanmasını dış saldırganlardan daha fazla gizlemek
 için bir dizi sabit paket boyutu uygun olabilir. Ancak tünel, Garlic
 ve uçtan uca dolgu ekleme o zamana kadar çoğu gereksinim için
 yeterli olmalıdır.
- Oturum oluşturuldu (SessionCreated) ve oturum onaylandı
 (SessionConfirmed) iletilerinde oturum açma süreleri kullanılmamış
 veya doğrulanmamış görünüyor.

# Uygulama Şeması

Bu şema, geçerli uygulamayı doğru bir şekilde yansıtıyor olmalı, ancak
küçük farklılıklar olabilir.

![](images/udp.png)

# [Teknik özellikler]{#spec}

[Şimdi SSU teknik özellikleri
sayfasında](). 
