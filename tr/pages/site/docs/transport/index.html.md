 Taşıyıcı Özeti 2018 Haziran 0.9.36 

## I2P Taşıyıcıları

I2P üzerindeki bir \"taşıyıcı\", iki yöneltici arasında doğrudan,
noktadan noktaya iletişim sağlamak için kullanılan bir yöntemdir.
Taşıyıcılar, iletişim kurulan yönelticinin belirli bir iletiyi alması
gereken kişi olduğunu doğrularken, dış saldırganlara karşı gizlilik ve
bütünlük sağlamalıdır.

I2P aynı anda birçok taşıyıcıyı destekler. Şu anda kullanılan üç
taşıyıcı var:

Her biri, kimlik doğrulama, akış denetimi, bildirimler ve yeniden iletim
ile bir \"bağlantı\" paradigması sağlar.

## Taşıyıcı Hizmetleri

I2P üzerindeki taşıyıcı alt sistemi şu hizmetleri sağlar:

- Reliable delivery of [I2NP]() messages.
 Transports support I2NP message delivery ONLY. They are not
 general-purpose data pipes.
- İletilerin sırayla aktarılması tüm taşıyıcılar tarafından garanti
 EDİLMEZ.
- Yönelticinin küresel iletişim bilgileri olarak yayınladığı
 \"Yöneltici bilgileri\" (RouterInfo), her taşıyıcı için bir ya da
 birkaç tane olabilen bir dizi yöneltici adresini tutar. Her
 taşıyıcı, IPv4 veya (0.9.8 sürümünden başlayarak) IPv6 üzerinden bu
 adreslerden birini kullanarak bağlanabilir.
- Her giden ileti için en iyi taşıyıcıyı seçer
- Giden iletileri önceliklerine göre kuyruğa ekler
- Yöneltici yapılandırmasına göre hem gidiş hem de geliş bant
 genişliği sınırlar
- Taşıyıcı bağlantılarını kurar ve kaldırır
- Noktadan noktaya iletişimi şifreler
- Her taşıyıcı için bağlantı sınırlarını gözetir. Bu sınırlar için
 çeşitli eşikleri uygular ve eşik durumunu yönelticiye bildirir.
 Böylece duruma göre operasyonel değişiklikler yapabilir
- UPnP (Evrensel tak ve çalıştır) kullanarak güvenlik duvarında
 bağlantı noktası açar
- İş birlikli NAT/Güvenlik duvarı geçişi sağlar
- UPnP, geliş bağlantılarını inceler ve ağ aygıtlarının belirlenmesi
 ile birlikte çeşitli yöntemlerle yerel IP adreslerini algılar
- Güvenlik duvarı durumu ve yerel IP adreslerinin koordinasyonu ile
 taşıyıcılar arasında değişiklikler yapar
- Güvenlik duvarı durumu ve yerel IP adresi iletişimi ile yöneltici ve
 kullanıcı arabiriminde değişiklikler yapar
- NTP için yedek olarak yönelticinin saatini düzenli olarak
 güncellemek için kullanılan bir uzlaşma saati belirler
- Her eşin, bağlı olup olmadığı, yakın zamanda bağlanıp bağlanmadığı
 ve son denemede erişilebilir olup olmadığı gibi durum bilgilerini
 tutar
- Yerel bir kural kümesine göre geçerli IP adreslerini sınıflandırır
- Yöneltici tarafından otomatik ve el ile tutulan yasaklanmış eş
 listelerini değerlendirir ve bu eşlerin giden ve gelen
 bağlantılarını reddeder

## Taşıyıcı Adresleri

Taşıyıcı alt sistemi, her biri bir taşıyıcı yöntemi, IP adresi ve
bağlantı noktası içeren bir dizi yöneltici adresi tutar. Bu adresler,
duyurulan iletişim noktalarını oluşturur ve yöneltici tarafından ağ veri
tabanında yayınlanır. Adreslerde ayrıca isteğe bağlı bir dizi ek seçenek
bulunabilir.

Her bir taşıyıcı yöntemi birkaç yöneltici adresi yayınlayabilir.

Tipik senaryolar şunlardır:

- Bir yönelticinin yayınlanmış bir adresi yoktur. Bu nedenle \"gizli\"
 olarak kabul edilir ve gelen bağlantıları alamaz
- A router is firewalled, and therefore publishes an SSU address which
 contains a list of cooperating peers or \"introducers\" who will
 assist in NAT traversal (see [the SSU spec]()
 for details)
- Yöneltici güvenlik duvarı arkasında değildir veya NAT bağlantı
 noktaları açıktır. Doğrudan erişilebilir IP adresi ve bağlantı
 noktaları içeren NTCP ve SSU adresleri yayınlar.

## Taşıyıcı Seçimi

The transport system delivers [I2NP messages]()
only. The transport selected for any message is independent of the
upper-layer protocols and contents (router or client messages, whether
an external application was using TCP or UDP to connect to I2P, whether
the upper layer was using [the streaming
library]() streaming or
[datagrams](), datagrams etc.).

Her giden ileti için, taşıyıcı sistemi her taşıyıcıdan \"teklif\" ister.
En düşük (en iyi) değeri veren taşıyıcı kazanır ve aktarım için iletiyi
alır. Bir taşıyıcı teklif vermeyi reddedebilir.

Bir taşıyıcının teklif verip vermeyeceği ve hangi değerde olacağı birçok
faktöre bağlıdır:

- Taşıyıcı ayarlarının yapılandırılması
- Taşıyıcının eşe zaten bağlı olup olmadığı
- Çeşitli bağlantı sınırı eşiklerine göre var olan bağlantı sayısı
- Eşe yapılan son bağlantı denemelerinin başarısız olup olmadığı
- Farklı taşıyıcılar farklı boyut sınırlarına sahip olduğundan
 iletinin boyutu
- Eşin, \"Yöneltici bilgileri\" (RouterInfo) verilerinde duyurulduğu
 gibi, bu taşıyıcının gelen bağlantıları kabul edip edemeyeceği
- Bağlantının dolaylı mı (tanıtıcılar gerektiren) yoksa doğrudan mı
 olacağı
- \"Yöneltici bilgileri\" (RouterInfo) verilerinde duyurulan eşin
 taşıyıcı tercihi

Genel olarak, teklif değerleri, iki yöneltici herhangi bir zamanda
yalnızca tek bir taşıyıcı ile bağlanacak şekilde seçilir. Ancak bu bir
gereklilik değildir.

## Yeni Taşıyıcılar ve Gelecekteki Çalışmalar

Şunlar gibi ek taşıyıcılar geliştirilebilir:

- TLS/SSH gibi görünen bir taşıyıcı
- Diğer tüm yönelticiler tarafından erişilemeyen yönelticiler için
 \"dolaylı\" bir taşıyıcı (\"kısıtlanmış rotaların bir biçimi\")
- Tor uyumlu değiştirilebilir taşıyıcılar

Her taşıyıcı için varsayılan bağlantı sınırlarını ayarlama çalışmaları
sürüyor. I2P, herhangi bir yönelticinin başka bir yönelticiye
bağlanabileceği varsayıldığı bir \"ağ örgüsü\" olarak tasarlanmıştır. Bu
varsayım, bağlantı sınırlarını aşan yönelticiler ve kısıtlayıcı durum
güvenlik duvarlarının (kısıtlanmış rotalar) arkasındaki yönelticiler
tarafından bozulabilir.

Bir NTCP bağlantısı için bellek gereksinimlerinin SSU için olandan daha
yüksek olduğu varsayımına göre, geçerli bağlantı sınırları SSU için NTCP
kullanılmasına göre daha yüksektir. Ancak, NTCP ara bellekleri kısmen
çekirdekte ve SSU ara bellekleri Java yığınında bulunduğundan, bu
varsayımı doğrulamak zordur.

Analyze [Breaking and Improving Protocol
Obfuscation]() and see how transport-layer padding
may improve things.


