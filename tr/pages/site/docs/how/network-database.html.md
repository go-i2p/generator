 Ağ veri tabanı 2025-03 0.9.65 

## Özet

I2P \"Ağ veri tabanı\" (NetDB), özel bir dağıtılmış veri tabanıdır ve
yalnızca iki tür veri içerir: Yöneltici iletişim bilgileri
(**\"Yöneltici bilgileri\" (RouterInfo)**) ile hedef iletişim bilgileri
(**\"Kiralama kümeleri\" (LeaseSets)**). Her veri parçası uygun tarafça
imzalanır ve onu kullanan veya saklayan herkes tarafından doğrulanır. Ek
olarak, verilerin içinde canlılık bilgileri bulunur. Böylece ilgisiz
kayıtlar silinerek ve daha yeni kayıtlar eskilerin yerine geçirilerek
belirli saldırı sınıflarına karşı koruma sağlanır.

\"Ağ veri tabanı\" (NetDB), \"Otomatik doldurma\" adı verilen basit bir
yöntemle dağıtılır. Dağıtılmış veri tabanını \"Otomatik doldurma
yönelticileri\" olarak adlandırılan tüm yönelticilerin bir alt kümesi
korur.

## RouterInfo {#routerInfo}

\"Bir I2P yönelticisi ile başka bir yöneltici iletişim kurmak
istediğinde, karşılıklı olarak bazı önemli veri parçalarını bilmeleri
gerekir. Bunların tümü yöneltici tarafından anahtar olarak yöneltici
kimliğinin SHA-256 değeri ile dağıtılan \"Yöneltici bilgileri\"
(RouterInfo) adlı bir yapı içine paketlenir ve imzalanır. Yapıda şunlar
bulunur:

- Yönelticinin kimliği (bir şifreleme anahtarı, bir imzalama anahtarı
 ve bir sertifika)
- Ulaşılabilecek iletişim adresleri
- Bunun ne zaman yayınlandığı
- İsteğe bağlı metin seçenekleri
- Kimliğin imzalama anahtarı tarafından yukarıdakiler ile oluşturulmuş
 imza

### Beklenen Ayarlar

Şart olmamasına rağmen aşağıdaki metin seçeneklerinin var olması
beklenir:

**caps** (Yetenek işaretleri - Otomatik doldurma katılımını, yaklaşık
bant genişliğini ve algılanan erişilebilirliği belirtmek için
kullanılır)

**D**: Medium congestion (as of release 0.9.58)

**E**: High congestion (as of release 0.9.58)

**f**: Otomatik doldurma

**G**: Rejecting all tunnels (as of release 0.9.58)

**H**: Gizli

**K**: Bu değerler, diğer yönelticiler tarafından temel kararlar için
kullanılır. Bu yönelticiye bağlanmalı mıyız? Bu yöneltici üzerinden bir
tünel yöneltmeye çalışmalı mıyız? Özellikle bant genişliği yeteneği
bayrağı, yalnızca yönelticinin tünelleri yöneltmek için en az eşiği
karşılayıp karşılamadığını belirlemek için kullanılır. En az eşiğin
üzerinde, duyurulan bant genişliği değeri, kullanıcı arayüzünde
görüntüleme ve hata ayıklama ile ağ analizi dışında yönelticinin hiçbir
yerinde kullanılmaz veya güvenilmez.

Valid NetID numbers:

Usage

NetID Number

Reserved

0

Reserved

1

Current Network (default)

2

Reserved Future Networks

3 - 15

Forks and Test Networks

16 - 254

Reserved

255

### Diğer Seçenekler

Additional text options include a small number of statistics about the
router\'s health, which are aggregated by sites such as [](http:///) for network performance analysis
and debugging. These statistics were chosen to provide data crucial to
the developers, such as tunnel build success rates, while balancing the
need for such data with the side-effects that could result from
revealing this data. Current statistics are limited to:

- Keşif tüneli oluşturma başarısı, reddetme ve zaman aşımı oranları
- Katkıda bulunulan tünel sayısının 1 saatlik ortalaması

These are optional, but if included, help analysis of network-wide
performance. As of API 0.9.58, these statistics are simplified and
standardized, as follows:

- Option keys are stat\_(statname).(statperiod)
- Option values are \';\' -separated
- Stats for event counts or normalized percentages use the 4th value;
 the first three values are unused but must be present
- Stats for average values use the 1st value, and no \';\' separator
 is required
- For equal weighting of all routers in stats analysis, and for
 additional anonymity, routers should include these stats only after
 an uptime of one hour or more, and only one time every 16 times that
 the RI is published.

Example:

 stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
 stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
 stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
 stat_tunnel.participatingTunnels.60m = 289.20

Floodfill routers may publish additional data on the number of entries
in their network database. These are optional, but if included, help
analysis of network-wide performance.

The following two options should be included by floodfill routers in
every published RI:

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

Example:

 netdb.knownLeaseSets = 158
 netdb.knownRouters = 11374

The data published can be seen in the router\'s user interface, but is
not used or trusted by any other router.

### Aile Ayarları

0.9.24 sürümüyle birlikte yönelticiler aynı varlık tarafından işletilen
bir \"ailenin\" parçası olduklarını duyurabilir. Aynı ailedeki birden
çok yöneltici tek bir tünelde kullanılmaz.

Aile ayarları şunlardır:

- **family** (Aile adı)
- **family.key** The signature type code of the family\'s [Signing
 Public
 Key](#type_SigningPublicKey)
 (in ASCII digits) concatenated with \':\' concatenated with the
 Signing Public Key in base 64
- **family.sig** The signature of ((family name in UTF-8) concatenated
 with (32 byte router hash)) in base 64

### \"Yöneltici bilgileri\" (RouterInfo) sona erme süresi

\"Yöneltici bilgileri\" (RouterInfo) kayıtlarının belirlenmiş bir
geçerlilik süresi yoktur. Her yöneltici \"Yöneltici bilgileri\"
aramalarının sıklığını bellek veya disk kullanımına göre belirlemek için
kendi yerel ilkesini kullanmakta özgürdür. Geçerli uygulamada aşağıdaki
genel ilkeler bulunur.

- Kalıcı olarak saklanan veriler eski olabileceğinden, ilk çalışma
 saatinde geçerlilik süresi kuıllanılmaz.
- 25 veya daha az \"Yöneltici bilgileri\" (RouterInfo) kaydı varsa
 geçerlilik süresi yoktur.
- Yerel \"Yöneltici bilgileri\" (RouterInfo) kaydı sayısı arttıkça,
 makul bir \"Yöneltici bilgileri\" sayısını korumak amacıyla
 geçerlilik süresi kısalır. 120 altında yöneltici için geçerlilik
 süresi 72 saat, 300 yöneltici için geçerlilik süresi yaklaşık 30
 saattir.
- RouterInfos containing [SSU]() introducers
 expire in about an hour, as the introducer list expires in about
 that time.
- Geçerli \"Yöneltici bilgileri\" (RouterInfo) kayıtları onlar için
 sık sık yeniden yayınlanacağından, otomatik doldurma sunucularında
 tüm yerel \"Yöneltici bilgileri\" kayıtları için kısa bir geçerlilik
 süresi (1 saat) kullanılır.

### Kalıcı \"Yöneltici bilgileri\" (RouterInfo) depolama

Yeniden başlatmadan sonra kullanılabilmesi için \"Yöneltici bilgileri
(RouterInfo)\" düzenli aralıklarla diske yazılır.

\"Üst Kiralama kümelerinin\" (MetaLeaseSets) verilerinin uzun süreli
olarak kalıcı olarak saklanması istenebilir. Bu durum, uygulamaya
bağlıdır.

### Şunlara da bakabilirsiniz

[\"Yöneltici bilgileri\" (RouterInfo) teknik
özellikleri](#struct_RouterInfo)

[\"Yöneltici bilgileri\" (RouterInfo) Java
belgeleri](http:///net/i2p/data/router/RouterInfo.html)

## LeaseSet {#leaseSet}

\"Ağ veri tabanında\" (NetDB) dağıtılan ikinci veri parçası, belirli bir
müşteri hedefi için bir grup **tünel giriş noktasını (kiralamaları)**
belgeleyen bir \"Kiralama kümesi\" (LeaseSet) olur. Bu kiralamaların her
birinde şu bilgiler bulunur:

- Tünel ağ geçidi yönelticisi (kimliğini belirterek)
- İleti göndermek için bu yönelticideki tünel kimliği (4 baytlık bir
 sayı)
- Bu tünelin geçerlilik süresi.

\"Kiralama kümesi\" (LeaseSet), hedefin SHA-256 değerinden türetilen
anahtar altında \"Ağ veri tabanı\" (NetDB) üzerinde tutulur. Bir
istisna, 0.9.38 sürümünden başlayarak \"Şifrelenmiş kiralama kümeleri\"
(EncryptedLeaseSets, LS2) içindir. Bayt (3) türünün SHA-256 değeri ve
ardından körleştirilmiş herkese açık anahtar, \"Dağıtılmış karma
tablosu\" (DHT) anahtarı için kullanılır ve sonra her zamanki gibi
döndürülür. Aşağıdaki Kademlia yakınlık ölçümü bölümüne bakın.

Bu kiralamalara ek olarak, \"Kiralama kümesi\" (LeaseSet) şunları
içerir:

- Hedefin kendisi (bir şifreleme anahtarı, bir imzalama anahtarı ve
 bir sertifika)
- Ek herkese açık şifreleme anahtarı: Garlic iletilerinin uçtan uca
 şifrelenmesi için kullanılır
- Ek herkese açık imzalama anahtarı: \"Kiralama kümesi\" (LeaseSet)
 iptali için tasarlandı, ancak şu anda kullanılmıyor.
- Hedefin bir \"Kiralama kümesi\" (LeaseSet) yayınladığından emin
 olmak için tüm \"Kiralama kümesi\" (LeaseSet) verilerinin imzası.

[Kiralama teknik
özellikleri](#struct_Lease)\
[\"Kiralama kümesi\" (LeaseSet) teknik
özellikleri](#struct_LeaseSet)

[Kiralama Java
belgeleri](http:///net/i2p/data/Lease.html)\
[\"Kiralama kümesi\" (LeaseSet) Java
belgeleri](http:///net/i2p/data/LeaseSet.html)

0.9.38 sürümüyle, üç yeni \"Kiralama kümesi\" (LeaseSet) türü
tanımlanmıştır; LeaseSet2, MetaLeaseSet ve EncryptedLeaseSet. Ayrıntılar
için aşağıya bakın.

### Yayınlanmamış \"Kiralama kümeleri\" (LeaseSets) {#unpublished}

Yalnızca gidiş bağlantıları için kullanılan bir hedef için \"Kiralama
kümesi\" (LeaseSet) *yayından kaldırıldı*. Hiçbir zaman yayınlanmak için
bir otomatik doldurma yönelticisine gönderilmez. İnternet üzerinde
gezinme ve IRC istemcileri için olanlar gibi \"istemci\" tünelleri
yayınlanmaz. Sunucular, [I2NP depolama iletileri](#lsp) nedeniyle, bu
yayınlanmamış hedeflere ileti göndermeyi sürdürebilir.

### Geçersiz kılınmış \"Kiralama kümeleri\" (LeaseSets) {#revoked}

Bir \"Kiralama kümesi\" (LeaseSet), sıfır kiralama yapan yeni bir
\"Kiralama kümesi\" (LeaseSet) yayınlayarak *geçersiz kılınabilir*.
Geçersiz kılmalar, \"Kiralama kümesi\" tarafından kullanılan ek imzalama
anahtarı ile imzalanmalıdır. Geçersiz kılma tam olarak kullanıma
alınmadı ve herhangi bir pratik kullanımı olup olmadığı belirsiz. Söz
konusu imzalama anahtarı yalnızca bunun için planlandığından şu anda
kullanılmıyor.

### LeaseSet2 (LS2) {#ls2}

0.9.38 sürümünden başlayarak otomatik dolgular yeni \"Kiralama kümesi\"
(LeaseSet) LS2 yapısını destekliyor. Bu yapı eski \"Kiralama kümesi\"
(LeaseSet) yapısına çok benzer ve aynı amaca hizmet eder. Yeni yapı,
yeni şifreleme türlerini, çoklu şifreleme türlerini, seçenekleri, çevrim
dışı imzalama anahtarlarını ve diğer özellikleri destekleyecek esnekliği
sağlar. Ayrıntılı bilgi almak için 123 numaralı öneriye bakabilirsiniz.

### Meta LeaseSet (LS2) {#meta}

0.9.38 sürümünden başlayarak, otomatik doldurmalar yeni bir \"Üst
kiralama kümesi\" (MetaLeaseSet) yapısını destekler. Bu yapı, diğer
\"Kiralama kümelerine\" (LeaseSets) atıfta bulunmak için \"Dağıtılmış
karma tablosu\" (DHT) üzerinde ağaç benzeri bir yapı sağlar. Bir site,
\"Üst kiralama kümesini\" (MetaLeaseSet) kullanarak, ortak bir hizmet
sağlamak için birkaç farklı hedefin kullanıldığı büyük, çoklu barındırma
hizmetlerini uygulayabilir. Bir \"Üst kiralama kümesindeki\"
(MetaLeaseSet) kayıtlar, hedefler veya diğer \"Üst kiralama
kümeleridir\" ve 18,2 saate kadar uzun geçerlilik süreleri olabilir. Bu
yapıyı kullanılarak, ortak bir hizmeti barındıran yüzlerce veya binlerce
hedef çalıştırılabilmelidir. Ayrıntılı bilgi almak için 123 numaralı
öneriye bakabilirsiniz.

### \"Şifrelenmiş kiralama kümeleri\" (EncryptedLeaseSets) (LS1) {#encrypted}

Bu bölümde, sabit bir simetrik anahtar kullanarak eski, güvenli olmayan
\"Kiralama kümesi\" (LeaseSet) şifreleme yöntemi açıklanır.
\"Şifrelenmiş kiralama kümelerinin\" (EncryptedLeaseSets) LS2 sürümü
için aşağıya bakın.

Bir \"*Şifrelenmiş* kiralama kümesi\" (EncryptedLeaseSet) içinde, tüm
kiralamalar ayrı bir anahtarla şifrelenir. Kiralamaların kodu yalnızca
çözülebilir ve bu nedenle hedefle yalnızca anahtara sahip olanlar
bağlantı kurabilir. \"Kiralama kümesinin\" (LeaseSet) şifrelenmiş
olduğuna hakkında bir işaret veya başka bir doğrudan gösterge yoktur.
\"Şifrelenmiş kiralama kümeleri\" (EncryptedLeaseSets) yaygın olarak
kullanılmıyor. Kullanıcı arayüzünün ve \"Şifrelenmiş kiralama
kümelerinin\" (EncryptedLeaseSets) uygulanmasının geliştirilmesi
geleceğe dönük bir araştırma konusudur.

### \"Şifrelenmiş kiralama kümeleri\" (EncryptedLeaseSets) (LS2) {#encrypted2}

0.9.38 sürümünden başlayarak, otomatik doldurma yeni bir \"Şifrelenmiş
kiralama kümesi\" (EncryptedLeaseSet) yapısını destekler. Hedef gizlidir
ve otomatik doldurmada yalnızca körleştirilmiş bir herkese açık anahtar
ve bir geçerlilik süresi görünür. Yalnızca tam hedefe sahip olanlar
yapının şifresini çözebilir. Yapı, hedefin karma değerine değil,
körleştirilmiş herkese açık anahtarın karma değerine dayalı olarak bir
\"Dağıtılmış karma tablosu\" (DHT) konumunda depolanır. Ayrıntılar için
123 numaralı öneriye bakabilirsiniz.

### \"Kiralama kümesi\" (LeaseSet) geçerlilik süresi

Normal \"Kiralama kümeleri\" (LeaseSets) için geçerlilik süresi,
kiralamalarının sona erme zamanıdır. Yeni LS2 \"Kiralama kümesi\"
(LeaseSet) veri yapıları için geçerlilik süresi üst bilgilerde
belirtilir. LS2 için geçerlilik süresi, kiralamaların sona erme
zamanlarıyla eşleşmelidir. \"Şifrelenmiş kiralama kümesi\"
(EncryptedLeaseSet) ve \"Üst kiralama kümesi\" (MetaLeaseSet) için
geçerlilik süresi değişebilir ve belirlenmek üzere en uzun geçerlilik
süresi dayatılabilir.

### \"Kiralama kümesi\" (LeaseSet) kalıcı depolaması

\"Kiralama kümesi\" (LeaseSet) verilerinin kalıcı olarak depolanması
gerekmez, çünkü bu veriler çok hızlı bir şekilde geçersiz olur. Ancak,
\"Şifrelenmiş kiralama kümesi\" (EncryptedLeaseSet) ve \"Üst kiralama
kümesi\" (MetaLeaseSet) verilerinin uzun geçerlilik süresiyle kalıcı
olarak saklanması önerilebilir.

### Şifreleme Anahtarı Seçimi (LS2) {#ls2keys}

2\. \"Kiralama kümesi\" (LeaseSet2) birden çok şifreleme anahtarı
içerebilir. Anahtarlar, en çok yeğlenen sunucu sırasına göredir.
Varsayılan istemci davranışı, desteklenen bir şifreleme türüne sahip ilk
anahtarın seçilmesidir. İstemciler, şifreleme desteğine, göreli başarıma
ve diğer faktörlere dayalı diğer seçim algoritmalarını kullanabilir.

## Ön yükleme {#bootstrap}

\"Ağ veri tabanı\" (NetDB) merkezi değildir, ancak bütünleştirme
sürecinin sizi bağlaması için en az bir eş referansına gerek duyarsınız.
Bunun için, yönelticinizi etkin bir eşin \"Yöneltici bilgileri\"
(RouterInfo) ile \"yeniden tohumlar\", özellikle de
`routerInfo-$hash.dat` dosyalarını alıp `netDB/` klasörünüze
kaydedersiniz. Bu dosyaları size herhangi biri sağlayabilir. Hatta kendi
netDb klasörünüzü görünür kılarak bunları başkalarına da sunabilirsiniz.
Süreci basitleştirmek için, gönüllüler netDb klasörlerini (veya bir alt
kümesini) normal (i2p olmayan) ağda yayınlar ve bu klasör adresleri I2P
içinde sabit kodlanmıştır. Yöneltici ilk kez başlatıldığında, otomatik
olarak bu adreslerden biri rastgele seçilerek alınır.

## Otomatik doldurma {#floodfill}

Otomatik doldurma \"Ağ veri tabanı\" (NetDB), basit bir dağıtılmış
depolama mekanizmasıdır. Depolama algoritması basittir: Verileri,
kendisini bir otomatik doldurma yönelticisi olarak tanıtan en yakın eşe
gönderir. Otomatik doldurma \"Ağ veri tabanı\" (NetDB) üzerinde bulunan
bir eş, otomatik doldurma \"Ağ veri tabanı\" (NetDB) üzerinde bulunmayan
bir eşten bir \"Ağ veri tabanı\" (NetDB) deposu aldığında, onu otomatik
doldurma \"Ağ veri tabanı\" (NetDB) eşlerinin bir alt kümesine gönderir.
Seçilen eşler, belirli bir anahtara ([XOR ölçüsü ile](#kad)) en yakın
olanlardır.

Otomatik doldurma \"Ağ veri tabanı\" (NetDB) için kimin parçası olduğunu
belirlemek önemsizdir. Her yönelticinin yayınlanan \"Yöneltici
bilgileri\" (RouterInfo) içinde bir yetenek olarak ortaya çıkar.

Otomatik doldurmaların merkezi bir yöneticisi yoktur ve bir \"uzlaşma\"
oluşturmazlar. Yalnızca basit bir \"Dağıtılmış karma tablosu\" (DHT)
kapsaması sağlarlar.

### Otomatik doldurma yöneltici aboneliği {#opt-in}

Dizin sunucularının sabit kodlandığı ve güvenilir olduğu ve bilinen
varlıklar tarafından işletildiği Tor ağının aksine, I2P otomatik
doldurma eş kümesinin üyelerinin güvenilir olması gerekmez ve zaman
içinde değişebilir.

\"Ağ veri tabanı\" (NetDB) güvenilirliğini artırmak ve ağ veri tabanı
trafiğinin yöneltici üzerindeki etkisini en aza indirmek için, otomatik
doldurma yalnızca yüksek bant genişliği sınırlarıyla yapılandırılmış
yönelticilerde otomatik olarak etkinleştirilir. Yüksek bant genişliği
sınırlarına sahip yönelticilerin (varsayılan çok daha düşük olduğu için
el ile yapılandırılması gerekir) daha düşük gecikmeli bağlantılarda
olduğu varsayılır ve 7/24 kullanılabilir olma olasılıkları daha
yüksektir. Otomatik doldurma yönelticisi için geçerli en az paylaşım
bant genişliği: 128 KBytes/sn.

Ek olarak, bir yöneltici, otomatik doldurma işlemi otomatik olarak
etkinleştirilmeden önce sistem durumu (gidiş ileti kuyruğu süresi, görev
gecikmesi vb.) için birkaç ek sınamadan geçmelidir.

Otomatik katılım için geçerli kurallarla, ağdaki yönelticilerin yaklaşık
6&37; kadarı otomatik doldurma yönelticileridir.

Bazı eşler, otomatik doldurma için el ile yapılandırılırken, diğerleri,
otomatik doldurma eşlerinin sayısı bir eşik değerinin altına düştüğünde
otomatik olarak gönüllü olan yüksek bant genişliğine sahip
yönelticilerdir. Böylece herhangi bir saldırı olduğunda, otomatik
doldurma yönelticilerinin kaybedilmesi ve uzun vadeli bir ağ hasarı
önlenir. Ters durumda, bekleyen çok fazla otomatik doldurma yönelticisi
olduğunda, bu eşler kendilerini otomatik doldurma rolünden çıkarır.

### Otomatik Doldurma Yöneltici Rolleri

Otomatik doldurma yönelticilerinin, otomatik doldurma olmayan
yönelticilerin hizmetlerine ek olan tek hizmetleri, \"Ağ veri tabanı\"
(NetDB) depolarını kabul etmek ve ağ veri tabanı sorgularına yanıt
vermektir. Genellikle yüksek bant genişlikleri olduğunda, çok sayıda
tünele katkıda bulunma olasılıkları daha yüksektir (diğer bir deyişle,
diğerleri için bir \"aktarıcı\" olur). Ancak bu onların dağıtılmış veri
tabanı hizmetleriyle doğrudan ilgili değildir.

## Kademlia Yakınlık Ölçümü {#kad}

\"Ağ veri tabanı\" (NetDB), yakınlığı belirlemek için Kademlia tarzı
basit bir XOR ölçümü kullanır. Bir Kademlia anahtarı oluşturmak için
"Yöneltici kimliği" (RouterIdentity) veya hedefin SHA-256 karması
hesaplanır. Bir istisna, 0.9.38 sürümünden başlayarak \"Şifrelenmiş
kiralama kümeleri\" (EncryptedLeaseSets, LS2) içindir. Bayt (3) türünün
SHA-256 değeri ve ardından körleştirilmiş herkese açık anahtar,
\"Dağıtılmış karma tablosu\" (DHT) anahtarı için kullanılır ve sonra her
zamanki gibi döndürülür.

[Sybil saldırılarının](#sybil-partial) maliyetlerini artırmak için bu
algoritmada bir değişiklik yapıldı. Aranan anahtarın kaydedilmiş SHA-256
karması yerine, SHA-256 karması, 8 baytlık bir ASCII dizgesi yyyyMMdd,
yani SHA256(anahtar + yyyyMMdd) olarak gösterilen UTC tarihi ile eklenen
32 baytlık ikili arama anahtarından alınır. Buna \"yöneltme anahtarı\"
denir ve her gün UTC gece yarısında değişir. Otomatik doldurma yöneltici
karmaları değil, yalnızca arama anahtarı bu şekilde değiştirilir. Günlük
\"Dağıtılmış karma tablosu\" (DHT) döndürmesi, tam anlamıyla bir
döndürme olmasa da bazen \"anahtar alanı döndürme\" olarak adlandırılır.

Yöneltme anahtarları hiçbir zaman herhangi bir I2NP iletisinde kablo
üzerinden gönderilmez. Yalnızca uzaklığın belirlenmesi için yerel olarak
kullanılırlar.

## Network Database Segmentation - Sub-Databases {#segmentation}

Traditionally Kademlia-style DHT\'s are not concerned with preserving
the unlinkability of information stored on any particular node in the
DHT. For example, a piece of information may be stored to one node in
the DHT, then requested back from that node unconditionally. Within I2P
and using the netDb, this is not the case, information stored in the DHT
may only be shared under certain known circumstances where it is
\"safe\" to do so. This is to prevent a class of attacks where a
malicious actor can try to associate a client tunnel with a router by
sending a store to a client tunnel, then requesting it back directly
from the suspected \"Host\" of the client tunnel.

### Segmentation Structure

I2P routers can implement effective defenses against the attack class
provided a few conditions are met. A network database implementation
should be able to keep track of whether a database entry was recieved
down a client tunnel or directly. If it was recieved down a client
tunnel, then it should also keep track of which client tunnel it was
recieved through, using the client\'s local destination. If the entry
was recieved down multiple client tunnels, then the netDb should keep
track of all destinations where the entry was observed. It should also
keep track of whether an entry was recieved as a reply to a lookup, or
as a store.

In both the Java and C++ implementations, this achieved by using a
single \"Main\" netDb for direct lookups and floodfill operations first.
This main netDb exists in the router context. Then, each client is given
it\'s own version of the netDb, which is used to capture database
entries sent to client tunnels and respond to lookups sent down client
tunnels. We call these \"Client Network Databases\" or \"Sub-Databases\"
and they exist in the client context. The netDb operated by the client
exists for the lifetime of the client only and contains only entries
that are communicated with the client\'s tunnels. This makes it
impossible for entries sent down client tunnels to overlap with entries
sent directly to the router.

Additionally, each netDb needs to be able to remember if a database
entry was recieved because it was sent to one of our destinations, or
because it was requested by us as part of a lookup. If a database entry
it was recieved as a store, as in some other router sent it to us, then
a netDb should respond to requests for the entry when another router
looks up the key. However, if it was recieved as a reply to a query,
then the netDb should only reply to a query for the entry if the entry
had already been stored to the same destination. A client should never
answer queries with an entry from the main netDb, only it\'s own client
network database.

These strategies should be taken and used combined so that both are
applied. In combination, they \"Segment\" the netDb and secure it
against attacks.

## Depolama, doğrulama ve arama mekanizması {#delivery}

### Eşlerde \"Yöneltici bilgileri (RouterInfo)\" depolama

[I2NP]() DatabaseStoreMessages containing the
local RouterInfo are exchanged with peers as a part of the
initialization of a [NTCP]() or
[SSU]() transport connection.

### Eşlere \"Kiralama kümesi\" (LeaseSet) depolama {#lsp}

[I2NP]() DatabaseStoreMessages containing the
local LeaseSet are periodically exchanged with peers by bundling them in
a garlic message along with normal traffic from the related Destination.
This allows an initial response, and later responses, to be sent to an
appropriate Lease, without requiring any LeaseSet lookups, or requiring
the communicating Destinations to have published LeaseSets at all.

### Floodfill Selection

\"Veri tabanı kaydetme iletisi\" (DatabaseStoreMessage), tutulmakta olan
\"Yöneltici bilgileri\" (RouterInfo) veya \"Kiralama kümesi\" (LeaseSet)
için geçerli yöneltme anahtarına en yakın olan otomatik doldurucuya
gönderilmelidir. Şu anda, en yakın otomatik doldurucu yerel veri
tabanında yapılan bir aramayla bulunur. Bu otomatik doldurucu gerçekte
en yakındaki olmasa bile, birden fazla otomatik doldurucuya gönderilerek
\"daha yakın\" doldurma sağlar. Böylece, yüksek düzeyde hata toleransı
sağlanır.

Geleneksel Kademlia üzerinde, bir eş, \"Dağıtılmış karma tablosu\" (DHT)
verilerine en yakın hedefe bir öge eklemeden önce \"en yakını bul\"
araması yapar. Doğrulama işlemi, varsa daha yakın otomatik doldurucuları
keşfetme eğiliminde olacağından, bir yöneltici, düzenli olarak
yayınladığı \"Yöneltici bilgileri\" (RouterInfo) ve \"Kiralama
kümeleri\" (LeaseSets) için \"Dağıtılmış karma tablosu\" (DHT)
\"mahallesi\" hakkındaki bilgisini hızla artıracaktır. I2NP bir \"en
yakını bul\" iletisi tanımlamasa da, gerekirse, bir yöneltici, \"Veri
tabanı arama yanıtı iletisi\" (DatabaseSearchReplyMessage) içinde daha
yakın bir eş alınmayana kadar en az anlamlı bit çevrilmiş bir anahtar
(yani anahtar \^ 0x01) için yinelemeli bir arama yapabilir. . Böylece,
daha uzaktaki bir eş \"Ağ veri tabanı\" (NetDB) ögesine sahip olsa bile
gerçek en yakın eşin bulunmasını sağlar.

### Otomatik doldurma yönelticilerinde \"Yöneltici bilgileri\" (RouterInfo) depolama

A router publishes its own RouterInfo by directly connecting to a
floodfill router and sending it a [I2NP]()
DatabaseStoreMessage with a nonzero Reply Token. The message is not
end-to-end garlic encrypted, as this is a direct connection, so there
are no intervening routers (and no need to hide this data anyway). The
floodfill router replies with a [I2NP]()
DeliveryStatusMessage, with the Message ID set to the value of the Reply
Token.

In some circumstances, a router may also send the RouterInfo
DatabaseStoreMessage out an exploratory tunnel; for example, due to
connection limits, connection incompatibility, or a desire to hide the
actual IP from the floodfill. The floodfill may not accept such a store
in times of overload or based on other criteria; whether to explicitly
declare non-direct store of a RouterInfo illegal is a topic for further
study.

### Otomatik doldurma yönelticilerine \"Kiralama kümesi\" (LeaseSet) depolama

Bir yönelticinin \"Kiralama kümelerinin\" (LeaseSets) yönelticiyle
ilişkilendirilememesine dikkat etmesi gerektiğinden, \"Kiralama
kümelerinin\" depolanması \"Yöneltici bilgileri\" (RouterInfo)
verilerine göre çok daha hassastır.

A router publishes a local LeaseSet by sending a
[I2NP]() DatabaseStoreMessage with a nonzero Reply
Token over an outbound client tunnel for that Destination. The message
is end-to-end garlic encrypted using the Destination\'s Session Key
Manager, to hide the message from the tunnel\'s outbound endpoint. The
floodfill router replies with a [I2NP]()
DeliveryStatusMessage, with the Message ID set to the value of the Reply
Token. This message is sent back to one of the client\'s inbound
tunnels.

### Otomatik Doldurma {#otomatik-doldurma}

Like any router, a floodfill uses various criteria to validate the
LeaseSet or RouterInfo before storing it locally. These criteria may be
adaptive and dependent on current conditions including current load,
netdb size, and other factors. All validation must be done before
flooding.

After a floodfill router receives a DatabaseStoreMessage containing a
valid RouterInfo or LeaseSet which is newer than that previously stored
in its local NetDb, it \"floods\" it. To flood a NetDb entry, it looks
up several (currently ) floodfill routers closest to the
routing key of the NetDb entry. (The routing key is the SHA256 Hash of
the RouterIdentity or Destination with the date (yyyyMMdd) appended.) By
flooding to those closest to the key, not closest to itself, the
floodfill ensures that the storage gets to the right place, even if the
storing router did not have good knowledge of the DHT \"neighborhood\"
for the routing key.

The floodfill then directly connects to each of those peers and sends it
a [I2NP]() DatabaseStoreMessage with a zero Reply
Token. The message is not end-to-end garlic encrypted, as this is a
direct connection, so there are no intervening routers (and no need to
hide this data anyway). The other routers do not reply or re-flood, as
the Reply Token is zero.

Floodfills must not flood via tunnels; the DatabaseStoreMessage must be
sent over a direct connection.

Floodfills must never flood an expired LeaseSet or a RouterInfo
published more than one hour ago.

### \"Yöneltici bilgileri\" (RouterInfo) ve \"Kiralama kümesi\" (LeaseSet) arama {#lookup}

The [I2NP]() DatabaseLookupMessage is used to
request a netdb entry from a floodfill router. Lookups are sent out one
of the router\'s outbound exploratory tunnels. The replies are specified
to return via one of the router\'s inbound exploratory tunnels.

Aramalar genellikle istenilen anahtara en yakın iki \"iyi\" (başarısız
olmayan bağlantı) otomatik doldurma aktarıcı yönelticisine paralel
olarak gönderilir.

If the key is found locally by the floodfill router, it responds with a
[I2NP]() DatabaseStoreMessage. If the key is not
found locally by the floodfill router, it responds with a
[I2NP]() DatabaseSearchReplyMessage containing a
list of other floodfill routers close to the key.

\"Kiralama kümesi\" (LeaseSet) aramaları, 0.9.5 sürümünden başlayarak
uçtan uca Garlic şifrelenmiştir. \"Yöneltici bilgileri\" (RouterInfo)
aramaları şifrelenmez ve bu nedenle istemci tünelinin gidiş uç noktası
(OBEP) tarafından izlenmeye karşı savunmasızdır. Bunun nedeni ElGamal
şifrelemesinin maliyetidir. \"Yöneltici bilgileri\" (RouterInfo) arama
şifrelemesi, gelecekteki bir sürümde etkinleştirilebilir.

0.9.7 sürümünden başlayarak, bir \"Kiralama kümesi\" (LeaseSet)
aramasına (bir \"Veri tabanı kaydetme iletisi\" (DatabaseStoreMessage)
veya bir \"Veri tabanı arama yanıtı iletisi\"
(DatabaseSearchReplyMessages)) verilen yanıtlar, aramaya oturum anahtarı
ve etiketi katılarak şifrelenir. Böylece, yanıt tünelinin geliş ağ
geçidinden (IBGW) gelen yanıt gizlenir. Arama şifrelemesini
etkinleştirirsek, \"Yöneltici bilgileri\" (RouterInfo) aramalarına
verilen yanıtlar şifrelenir.

(Reference: [Hashing it out in Public]() Sections
2.2-2.3 for terms below in italics)

Ağın nispeten küçük boyutu ve otomatik doldurma yedekliliği nedeniyle,
aramalar genellikle O(log n) yerine O(1) şeklindedir. Bir yönelticinin,
ilk denemede yanıtı almak için anahtara yeterince yakın bir otomatik
doldurma yönelticisini bilme olasılığı yüksektir. 0.8.9 öncesindeki
sürümlerde, yönelticiler iki arama yedekliliği kullandı (yani, farklı
eşlere paralel olarak iki arama yapıldı) ve aramalar için ne *iç içe* ne
de *yinelemeli* yöneltme uygulandı. *Sorgu başarısızlığı olasılığını
azaltmak* için sorgular aynı anda *birden fazla yöneltme ile*
gönderildi.

0.8.9 sürümünden itibaren, *yinelemeli aramalar* arama artıklığı olmadan
uygulanıyor. Bu yöntem, tüm otomatik doldurma eşleri bilinmediğinde çok
daha iyi çalışacak daha verimli ve güvenilir bir arama sağlıyor ve ağ
büyümesine yönelik ciddi bir sınırlamayı ortadan kaldırıyor. Ağ
büyüdükçe ve her yöneltici otomatik doldurma eşlerinin yalnızca küçük
bir alt kümesini bildikçe, aramalar O(log n) şeklinde olur. Eş, anahtara
daha yakın referanslar döndürmese bile, arama işlemi ek güvenlik
sağlamak ve kötü niyetli bir otomatik doldurma yönelticisinin anahtar
uzayının bir bölümünden kara delik oluşturmasını önlemek için bir
sonraki en yakın eşle ilerler. Aramalar, toplam arama zaman aşımına
ulaşılana veya en fazla eş sayısı sorgulanana kadar sürdürülür.

*Düğüm kimlikleri*, *doğrulanabilir*. Çünkü yöneltici karmasını doğrudan
hem düğüm kimliği hem de Kademlia anahtarı olarak kullanırız. Arama
anahtarına daha yakın olmayan yanlış yanıtlar genellikle yok sayılır.
Ağın güncel boyutu göz önüne alındığında, bir yöneltici *hedef kimliği
uzayının komşuluğu hakkında ayrıntılı bilgiye* sahiptir.

### \"Yöneltici bilgileri\" (RouterInfo) depolama doğrulaması

Note: RouterInfo verification is disabled as of release 0.9.7.1 to
prevent the attack described in the paper [Practical Attacks Against the
I2P Network](). It is not clear if
verification can be redesigned to be done safely.

Bir depolamanın başarılı olduğunu doğrulamak için, bir yöneltici
yalnızca 10 saniye kadar bekler. Ardından anahtara yakın başka bir
otomatik doldurma yönelticisine bir arama gönderir (ancak depolamanın
gönderildiğine değil). Aramalar, yönelticinin gidiş keşif tünellerinden
birini gönderdi. Aramalar, gidiş uç noktası (OBEP) tarafından
gözetlenmeyi önlemek için uçtan uca Garlic şifrelenir.

### \"Kiralama kümesi\" (LeaseSet) depolama doğrulaması

Bir depolamanın başarılı olduğunu doğrulamak için, bir yöneltici
yalnızca 10 saniye kadar bekler. Ardından anahtara yakın başka bir
otomatik doldurma yönelticisine bir arama gönderir (ancak depolamanın
gönderildiğine değil). Aramalar, doğrulanmakta olan \"Kiralama
kümesinin\" (LeaseSet) hedefi için istemci gidiş tünellerinden birini
gönderdi. Gidiş tünelinin OBEP tarafından gözetlenmesini önlemek için,
aramalar uçtan uca Garlic olarak şifrelenir. Yanıtlar, istemcinin geliş
tünellerinden biri aracılığıyla döndürülecek şekilde belirtilir.

0.9.7 sürümünden başlayarak, yanıt tünelinin geliş ağ geçidinden (IBGW)
gelen yanıtı gizlemek için hem \"Yöneltici bilgileri\" (RouterInfo) hem
de \"Kiralama kümesi\" (LeaseSet) aramaları (bir \"Veri tabanı kaydetme
iletisi\" (DatabaseStoreMessage) veya bir \"Veri tabanı arama yanıtı
iletisi\" (DatabaseSearchReplyMessages)) için yanıtlar şifrelenir.

### Keşif

*Exploration* is a special form of netdb lookup, where a router attempts
to learn about new routers. It does this by sending a floodfill router a
[I2NP]() DatabaseLookup Message, looking for a
random key. As this lookup will fail, the floodfill would normally
respond with a [I2NP]() DatabaseSearchReplyMessage
containing hashes of floodfill routers close to the key. This would not
be helpful, as the requesting router probably already knows those
floodfills, and it would be impractical to add all floodfill routers to
the \"don\'t include\" field of the DatabaseLookup Message. For an
exploration query, the requesting router sets a special flag in the
DatabaseLookup Message. The floodfill will then respond only with
non-floodfill routers close to the requested key.

### Arama Yanıtları Hakkında Notlar

Bir arama isteğine verilen yanıt, bir veri tabanı depolama iletisi
(başarı durumunda) veya bir veri tabanı arama yanıt iletisi
(başarısızlık durumunda). DSRM, yanıtın kaynağını belirtmek için bir
yöneltici karma alanı içerir. Veri tabanı depolama iletisinde bu
bulunmaz. Veri tabanı arama yanıt iletisinin \'kimden\' alanı kimliği
doğrulanmamış ve sahte veya geçersiz olabilir. Başka bir yanıt etiketi
bulunmaz. Bu nedenle, paralel olarak birden çok istekte bulunurken,
çeşitli otomatik doldurma yönelticilerinin başarımını izlemek zordur.

## Birden Çok Barındırma {#multihome}

Hedefler, aynı kişisel ve herkese açık anahtarlar (geleneksel olarak
eepPriv.dat dosyalarında depolanır) kullanılarak aynı anda birden çok
yönelticide barındırılabilir. Her iki örnek de imzalı \"Kiralama
kümelerini\" (LeaseSets) otomatik doldurma eşlerine düzenli olarak
yayınlayacağından, en son yayınlanan \"Kiralama kümesi\" (LeaseSet) bir
veri tabanı araması isteği yapan bir eşe döndürülür. \"Kiralama
kümelerinin\" (LeaseSets) en fazla 10 dakikalık bir kullanım ömrü
olduğundan, belirli bir bulut sunucusunun çökmesi durumunda kesinti en
fazla 10 dakika olur ve genellikle bundan çok daha azdır. Çoklu
barındırma arama işlevi doğrulandı ve ağdaki çeşitli hizmetler
tarafından kullanılıyor.

0.9.38 sürümünden başlayarak, otomatik doldurmalar yeni bir \"Üst
kiralama kümesi\" (MetaLeaseSet) yapısını destekler. Bu yapı, diğer
\"Kiralama kümelerine\" (LeaseSets) atıfta bulunmak için \"Dağıtılmış
karma tablosu\" (DHT) üzerinde ağaç benzeri bir yapı sağlar. Bir site,
\"Üst kiralama kümesini\" (MetaLeaseSet) kullanarak, ortak bir hizmet
sağlamak için birkaç farklı hedefin kullanıldığı büyük, çoklu barındırma
hizmetlerini uygulayabilir. Bir \"Üst kiralama kümesindeki\"
(MetaLeaseSet) kayıtlar, hedefler veya diğer \"Üst kiralama
kümeleridir\" ve 18,2 saate kadar uzun geçerlilik süreleri olabilir. Bu
yapıyı kullanılarak, ortak bir hizmeti barındıran yüzlerce veya binlerce
hedef çalıştırılabilmelidir. Ayrıntılı bilgi almak için 123 numaralı
öneriye bakabilirsiniz.

## Tehdit İncelemesi {#threat}

Also discussed on [the threat model
page](#floodfill).

Kötü niyetli bir kullanıcı, bir veya daha fazla otomatik doldurma
yönelticisi oluşturarak ve bunları kötü, yavaş veya hiç yanıt vermeyecek
şekilde hazırlayarak ağa zarar vermeye çalışabilir. Bazı senaryolar
aşağıda tartışılmıştır.

### Büyümeyle Genel Azaltma

There are currently around floodfill routers in the
network. Most of the following attacks will become more difficult, or
have less impact, as the network size and number of floodfill routers
increase.

### Süreklilikle Genel Azaltma

Via flooding, all netdb entries are stored on the 
floodfill routers closest to the key.

### Sahtecilikler

Tüm \"Ağ veri tabanı\" (NetDB) kayıtları oluşturucuları tarafından
imzalanmıştır. Bu nedenle hiçbir yöneltici bir \"Yöneltici bilgileri\"
(RouterInfo) veya \"Kiralama kümesi\" (LeaseSet) verisini taklit edemez.

### Yavaş ya da Yanıtsız

Each router maintains an expanded set of statistics in the [peer
profile]() for each floodfill router,
covering various quality metrics for that peer. The set includes:

- Ortalama yanıt süresi
- İstenilen verilerle yanıtlanan sorguların yüzdesi
- Başarıyla doğrulanan depolamaların yüzdesi
- Son başarılı depolama
- Son başarılı arama
- Son yanıt

Bir yönelticinin hangi otomatik doldurma yönelticisinin bir anahtara en
yakın olduğunu belirlemesi gerektiğinde, hangi otomatik doldurma
yönelticilerinin \"iyi\" olduğunu belirlemesi için bu ölçümler
kullanılır. \"İyiliği\" belirlemek için kullanılan yöntemler ve eşikler
nispeten yenidir ve daha fazla analiz ve iyileştirmeye açıktır. Tamamen
yanıt vermeyen bir yöneltici hızlı bir şekilde belirlenip bunlardan
kaçınılırken, yalnızca bazen kötü niyetli olan yönelticilerle uğraşmak
çok daha zor olabilir.

### Sybil Saldırısı (Tam Anahtar Uzayı) {#sybil}

An attacker may mount a [Sybil attack]() by
creating a large number of floodfill routers spread throughout the
keyspace.

(In a related example, a researcher recently created a [large number of
Tor relays]().) If successful, this could be an
effective DOS attack on the entire network.

Otomatik doldurma yönelticileri, yukarıda açıklanan eş profil ölçümleri
kullanılarak \"kötü\" olarak işaretlenecek kadar hatalı çalışmıyorsa, bu
senaryonun, ele alınması zordur. Tor yanıtı, aktarıcı durumunda çok daha
çevik olabilir, çünkü şüpheli aktarıcılar uzlaşmadan el ile
kaldırılabilir. I2P ağı için bazı olası yanıtlar aşağıda listelenmiştir.
Ancak bunların hiçbiri tam olarak tatmin edici değildir:

- Kötü yöneltici karmalarının veya IP adreslerinin bir listesini
 derleyin ve listeyi çeşitli yollarla duyurun (konsol haberleri,
 site, forum vb.); kullanıcıların listeyi el ile indirmeleri ve yerel
 \"kara listelerine\" eklemeleri gerekir.
- Ağdaki herkesten otomatik doldurmayı el ile etkinleştirmesini
 isteyin (Sybil ile daha fazla Sybil kullanarak savaşın)
- Sabit kodlanmış \"hatalı\" listeyi içeren yeni bir yazılım sürümü
 yayınlayın
- \"Kötü\" eşleri otomatik olarak belirleme girişiminde bulunarak, eş
 profili ölçümlerini ve eşiklerini iyileştiren yeni bir yazılım
 sürümü yayınlayın.
- Tek bir IP bloğundaki otomatik doldurma yönelticileri çok fazla
 sayıdaysa azaltan yazılım ekleyin
- Tek bir kişi veya grup tarafından kontrol edilen, aboneliğe dayalı
 otomatik bir kara liste uygulayın. Bu, aslında Tor \"uzlaşma\"
 modelinin bir bölümünü uygular. Ne yazık ki, tek bir bireye veya
 gruba belirli bir yönelticinin veya IP adresinin ağdaki katılımını
 engelleme veya hatta tüm ağı tamamen kapatma veya yok etme gücü de
 verir.

Ağ boyutu büyüdükçe bu saldırı daha zor hale gelir.

### Sybil Saldırısı (Parçalı Anahtar Uzayı) {#sybil-partial}

An attacker may mount a [Sybil attack]() by
creating a small number (8-15) of floodfill routers clustered closely in
the keyspace, and distribute the RouterInfos for these routers widely.
Then, all lookups and stores for a key in that keyspace would be
directed to one of the attacker\'s routers. If successful, this could be
an effective DOS attack on a particular I2P Site, for example.

Anahtar uzayı, anahtarın şifreleme (SHA-256) karması tarafından dizine
eklendiğinden, bir saldırgan, anahtara yeterince yakın olana kadar üst
üste yöneltici karmaları oluşturmak için bir kaba kuvvet yöntemi
kullanmalıdır. Ağ boyutuna bağlı olduğundan bunun için gereken hesaplama
gücü miktarı bilinmemektedir.

Bu saldırıya karşı kısmi bir savunma olarak, Kademlia tarafından
\"yakınlığı\" belirlemek için kullanılan algoritma zamanla değiştirilir.
Yakınlığı belirlemek için anahtarın karmasını (H(k)) kullanmak yerine,
geçerli tarih dizgesine eklenen anahtarın karmasını kullanırız, (H(k +
YYYYMMDD)). Özgün anahtarı bir \"yöneltme anahtarına\" dönüştüren
\"yöneltme anahtarı oluşturucu\" adlı bir işlev bunu yapar. Başka bir
deyişle, \"Ağ veri tabanı\" (NetDB) anahtar uzayının tamamı her gün UTC
gece yarısında \"döndürülür\". Herhangi bir kısmi anahtar alanı
saldırısının her gün yeniden oluşturulması gerekir. Çünkü döndürme
işleminden sonra saldıran yönelticiler artık hedef anahtara veya
birbirlerine yakın olmayacaktır.

Ağ boyutu büyüdükçe bu saldırı daha zor hale gelir. Bununla birlikte,
son araştırmalar, anahtar uzayını döndürmenin özellikle etkili
olmadığını göstermektedir. Bir saldırgan, çok sayıda yöneltici karma
değerini önceden hesaplayabilir ve yalnızca birkaç yöneltici,
döndürmeden sonraki yarım saat içinde anahtar uzayının bir bölümünü
\"tutturmak\" için yeterlidir.

Günlük anahtar uzayı döndürmenin bir sonucu, dağıtılmış \"Ağ veri
tabanının\" (NetDB) döndürme işleminden birkaç dakika sonra güvenilmez
olmasıdır. Yeni \"en yakın\" yöneltici henüz bir depolama almadığı için
aramalar başarısız olur. Sorunun kapsamı ve hafifletme yöntemleri
(örneğin gece yarısı \"Ağ veri tabanı\" (NetDB) \"terkleri\") üzerinde
daha fazla çalışılması gereken bir konudur.

### Ön Yükleme Saldırıları

Bir saldırgan, yeniden oluşturulmuş bir siteyi ele geçirerek veya 
geliştiricileri, yeniden oluşturulmuş siteyi yönelticideki sabit 
kodlanmış listeye eklemeleri için kandırarak, yalıtılmış veya
çoğunluğun  denetimindeki bir ağda yeni yönelticiler başlatmayı
deneyebilir.

Birkaç savunma önlemi alınabilir ve bunların çoğu planlanmıştır:

- Yeniden tohumlama için HTTPS yerine HTTP iletişim kuralına
 dönülmesine izin vermeyin. Bir MITM saldırganı kolayca HTTPS
 erişimini engelleyip ardından HTTP iletişim kuralına yanıt
 verebilir.
- Kurucuda yeniden çekirdek verilerinin paketlenmesi

Uygulanan savunmalar:

- Yeniden tohumlama görevi, yalnızca tek bir site kullanmak yerine,
 birkaç yeniden oluşturulmuş sitenin her birinden bir \"Yöneltici
 bilgileri\" (RouterInfo) alt kümesi alacak şekilde değiştirildi.
- Yeniden tohumlanmış siteleri düzenli olarak yoklayan ve verilerin
 eskimiş veya ağın diğer görünümleriyle tutarsız olmadığını
 doğrulayan ağ dışı bir yeniden izleme hizmeti oluşturuldu.
- 0.9.14 sürümünden başlayarak, yeniden tohumlama verileri imzalanmış
 bir zip dosyasında paketleniyor ve indirildiğinde imza doğrulanıyor.
 See [the su3
 specification](#su3)
 for details.

### Sorgu Yakalama

See also [lookup](#lookup) (Reference: [Hashing it out in
Public]() Sections 2.2-2.3 for terms below in
italics)

Ön yükleme saldırısına benzer şekilde, otomatik doldurma yönelticisi
kullanan bir saldırgan, referanslarını döndürerek, eşleri kendisi
tarafından kontrol edilen bir yöneltici alt kümesine \"yöneltmeye\"
çalışabilir.

Bunun keşif yoluyla çalışması pek olası değildir. Çünkü keşif düşük
sıklıkla yapılan bir görevdir. Yönelticiler, eş referanslarının çoğunu
normal tünel oluşturma faaliyeti yoluyla elde eder. Keşif sonuçları
genellikle birkaç yöneltici karmasıyla sınırlıdır ve her keşif sorgusu
rastgele bir otomatik doldurma yönelticisine yönlendirilir.

As of release 0.8.9, *iterative lookups* are implemented. For floodfill
router references returned in a [I2NP]()
DatabaseSearchReplyMessage response to a lookup, these references are
followed if they are closer (or the next closest) to the lookup key. The
requesting router does not trust that the references are closer to the
key (i.e. they are *verifiably correct*. The lookup also does not stop
when no closer key is found, but continues by querying the next-closet
node, until the timeout or maximum number of queries is reached. This
prevents a malicious floodfill from black-holing a part of the key
space. Also, the daily keyspace rotation requires an attacker to
regenerate a router info within the desired key space region. This
design ensures that the query capture attack described in [Hashing it
out in Public]() is much more difficult.

### \"Dağıtılmış karma tablosu\" (DHT) temelli aktarıcı seçimi

(Reference: [Hashing it out in Public]() Section 3)

This doesn\'t have much to do with floodfill, but see the [peer
selection page]() for a discussion of the
vulnerabilities of peer selection for tunnels.

### Bilgi Kaçakları

(Reference: [In Search of an Anonymous and Secure
Lookup]() Section 3)

This paper addresses weaknesses in the \"Finger Table\" DHT lookups used
by Torsk and NISAN. At first glance, these do not appear to apply to
I2P. First, the use of DHT by Torsk and NISAN is significantly different
from that in I2P. Second, I2P\'s network database lookups are only
loosely correlated to the [peer
selection]() and [tunnel
building]() processes; only
previously-known peers are used for tunnels. Also, peer selection is
unrelated to any notion of DHT key-closeness.

Bunlardan bazıları, I2P ağı daha fazla genişlediğinde daha ilginç
olabilir. Şu anda, her yöneltici ağın büyük bir bölümünü biliyor. Bu
nedenle ağ veri tabanında belirli Yöneltici Bilgilerini aramak,
gelecekte bu yönelticiyi bir tünelde kullanma niyetinin güçlü bir
göstergesi değildir. Belki ağ 100 kat daha büyük olduğunda, arama daha
ilişkilendirilebilir olabilir. Tabii ki, daha büyük bir ağ, bir Sybil
saldırısını çok daha zor hale getirir.

However, the general issue of DHT information leakage in I2P needs
further investigation. The floodfill routers are in a position to
observe queries and gather information. Certainly, at a level of *f* =
0.2 (20% malicious nodes, as specifed in the paper) we expect that many
of the Sybil threats we describe
([here](#sybil), [here](#sybil) and
[here](#sybil-partial)) become problematic for several reasons.

## Geçmiş {#history}

[\"Ağ veri tabanı\" (NetDB) tartışma sayfasına
taşındı]().

## Gelecekte Yapılacak Çalışmalar {#future}

Ek \"Ağ veri tabanı\" (NetDB) aramalarının ve yanıtlarının uçtan uca
şifrelenmesi.

Arama yanıtlarını izlemek için daha iyi yöntemler.


