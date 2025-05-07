 I2P: Anonim
iletişim için ölçeklenebilir bir çatı 2025-01 0.9.65 

- [Giriş](#intro)
- [I2P İşlemesi](#op)
 - [Özet](#op.overview)
 - [Tüneller](#op.tunnels)
 - [Ağ veri tabanı](#op.netdb)
 - [Taşıyıcı iletişim kuralları](#op.transport)
 - [Şifreleme](#op.crypto)
- [Gelecek](#future)
 - [Restricted Routes](#future.restricted)
 - [Variable Latency](#future.variablelatency)
- [Similar Networks](#similar)
 - [Tor](#similar.tor)
 - [Freenet](#similar.freenet)
- [Application Layer](#app)
 - [Streaming](#app.streaming)
 - [Naming and Addressbook](#app.naming)
 - [I2PSnark](#app.i2psnark)
 - [I2PTunnel](#app.i2ptunnel)
 - [I2P Email](#app.i2pmail)

 

NOTE: This document was originally written by jrandom in 2003. While we
strive to keep it current, some information may be obsolete or
incomplete. The transport and cryptography sections are current as of
2025-01.

# Giriş {#intro}

I2P, üzerinde herhangi bir sayıda farklı anonimlik veya güvenlik
bilincine sahip uygulamanın çalışabileceği, ölçeklenebilir, kendi
kendini düzenleyen, esnek bir paket anahtarlamalı anonim ağ katmanıdır.
Bu uygulamaların her biri, özgür bir rota karma ağının uygun şekilde
uygulanması konusunda endişelenmeden kendi anonimliklerini, gecikme
sürelerini ve verim uzlaşmalarını yapabilir ve etkinliklerini
halihazırda I2P üzerinde çalışan daha büyük anonimlik grubuyla
harmanlayabilir.

Applications available already provide the full range of typical
Internet activities - **anonymous** web browsing, web hosting, chat,
file sharing, e-mail, blogging and content syndication, as well as
several other applications under development.

- İnternet üzerinde gezinme: Vekil sunucu desteği olan herhangi bir
 tarayıcı kullanılabilir.
- Chat: IRC and other protocols
- File sharing: [I2PSnark](#app.i2psnark) and other applications
- E-mail: [susimail](#app.i2pmail) and other applications
- Blog: using any local web server, or available plugins

[Freenet](#similar.freenet) ya da [GNUnet](https://www.gnunet.org/en/)
gibi içerik dağıtım ağlarında barındırılan sitelerin aksine, I2P
üzerinde barındırılan hizmetler tamamen etkileşimlidir. Geleneksel
internet tarzı arama motorları, forumlar, yorum yapabileceğiniz bloglar,
veri tabanı destekli siteler ve yerel olarak kurmaya gerek kalmadan
Freenet gibi sabit sistemleri sorgulamak için köprüler vardır.

Anonimliğin etkin olduğu tüm bu uygulamalarla, I2P ileti odaklı ara
yazılım rolünü üstlenir. Uygulamalar bir şifreli belirtece (\"hedef\")
bazı veriler göndermek istediklerini söyler ve I2P verilerin oraya
anonim bir şeklikde güvenli olarak ulaşmasını sağlar. Ayrıca, I2P en iyi
çabayla anonim iletilerin güvenilir, sıralı akışlar olarak aktarılmasını
sağlamak için basit bir [akış](#app.streaming) kitaplığı sağlar ve ağın
yüksek bant genişliği gecikme ürünü için ayarlanmış TCP tabanlı bir
tıkanıklık kontrol algoritmasını şeffaf bir şekilde sunar. Var olan
uygulamaları ağa bağlamak için birkaç basit SOCKS vekil sunucusu bulunsa
da, hemen hemen her uygulama, anonim bir bağlamda hassas bilgileri rutin
olarak açığa çıkardığından, bunların değeri pek bilinmemiştir.
İlerlemenin tek güvenli yolu, düzgün çalışmayı sağlamak için bir
uygulamayı tamamen denetlemek ve ağdan en iyi şekilde yararlanmak için
kullanılabilecek çeşitli dillerde bir dizi API sağlamamıza yardımcı
olmaktır.

I2P is not a research project - academic, commercial, or governmental,
but is instead an engineering effort aimed at doing whatever is
necessary to provide a sufficient level of anonymity to those who need
it. It has been in active development since early 2003 with one full
time developer and a dedicated group of part time contributors from all
over the world. All of the work done on I2P is open source and freely
available on the [website](), with the majority of
the code released outright into the public domain, though making use of
a few cryptographic routines under BSD-style licenses. The people
working on I2P do not control what people release client applications
under, and there are several GPL\'ed applications available
([I2PTunnel](#app.i2ptunnel), [susimail](#app.i2pmail),
[I2PSnark](#app.i2psnark), [I2P-Bote](#app.i2pbote),
[I2Phex](#app.i2phex) and others.).
[Funding]() for I2P comes entirely from
donations, and does not receive any tax breaks in any jurisdiction at
this time, as many of the developers are themselves anonymous.

# İşletme {#op}

## Özet {#op.overview}

I2P işleyişini anlamak için birkaç temel kavramın anlaşılması önemlidir.
İlk olarak, I2P, ağa katılan yazılım (bir \"yöneltici\") ile bireysel
uygulamalarla ilişkili anonim uç noktalar (\"hedefler\") arasında kesin
bir ayrım yapar. Birinin I2P çalıştırdığı gerçeği genellikle bir sır
değildir. Gizli olan, kullanıcının ne yaptığı, herhangi bir şey
yapıyorsa belirli bir hedefin hangi yönelticiye bağlı olduğu hakkında
bilgidir. Son kullanıcıların yönelticilerinde tipik olarak birkaç yerel
hedefi olacaktır. Örneğin, biri IRC sunucuları için vekil sunucuyu, bir
başkası, kullanıcının anonim site sunucusunu (\"I2P Sitesi\"), diğeri
bir I2Phex kopyasını, diğeri torrent kullanımı gibi işlemleri destekler.

Anlaşılması gereken bir diğer kritik kavram da \"tünel\"dir. Tünel,
açıkça seçilmiş bir yöneltrici listesi üzerinden yöneltilen bir yoldur.
Katmanlı şifreleme kullanılır, bu nedenle yönelticilerin her biri
yalnızca tek bir katmanın şifresini çözebilir. Şifresi çözülen
bilgilerde, iletilecek şifreli bilgilerle birlikte bir sonraki
yönelticinin IP adresi bulunur. Her tünelin bir başlangıç noktası (\"ağ
geçidi\" olarak da bilinen ilk yöneltrici) ve bir bitiş noktası vardır.
İletiler yalnızca bir şekilde gönderilebilir. İletileri geri göndermek
için başka bir tünel gereklidir.

::: {.box style="text-align:center;"}
\
\
![Inbound and outbound tunnel
schematic](images/tunnels.png "Inbound and outbound tunnel schematic")\
\
Şekil 1: İki tünel türü: Geliş ve gidiş.
:::

İki tür tünel vardır: **\"gidiş\" tüneli** tünel oluşturucudan dışarı
iletiler gönderirken, **\"geliş\" tüneli** iletileri tünel oluşturucuya
getirir. Bu iki tünel bir arada kullanılarak kullanıcıların birbirlerine
ileti gönderilmesi sağlanır. Gönderici (yukarıdaki görselde \"Alice\")
bir gidiş tüneli oluştururken alıcı (yukarıdaki görselde \"Bob\") bir
geliş tüneli oluşturur. Geliş tünelinin ağ geçidi, herhangi bir başka
kullanıcıdan ileti alabilir ve bunları uç noktaya (\"Bob\") kadar
gönderir. Gidiş tünelinin uç noktasının, geliş tünelinin ağ geçidine
ileti göndermesi gerekir. Bunu yapmak için gönderici (\"Alice\") şifreli
iletisine yönergeler ekler. Gidiş tünelinin uç noktası iletinin
şifresini çözdüğünde, iletiyi doğru geliş ağ geçidine (\"Bob\" ağ
geçidi) iletmek için yönergeleri almış olur.

Anlaşılması gereken üçüncü kritik kavram, ağ üst verilerini paylaşmak
için kullanılan bir çift algoritma olan I2P **\"Ağ veri tabanı\"
(NetDB)** olacak. Taşınan iki üst veri türü **\"Yöneltici bilgileri\"
(RouterInfo)** ve

\"Kiralama kümeleri\" (LeaseSets) - \"Yöneltici bilgileri\"
(RouterInfo), yönelticilere belirli bir yöneltici ile iletişim kurmak
için gerekli verileri (herkese açık anahtarlar, taşıyıcı adresleri, vb.)
verirken, \"Kiralama kümesi\" (LeaseSet) yönelticilere belirli bir
hedefle iletişim kurmak için gereken bilgileri verir. Bir \"Kiralama
kümesi\" (LeaseSet) içinde bir dizi \"kiralama\" bulunur. Bu
kiralamaların her biri, belirli bir hedefe ulaşmayı sağlayan bir tünel
ağ geçidi belirtir. Bir kiralamadaki tüm bilgiler şunlardır:

- Belirli bir hedefe ulaşmayı sağlayan bir tünelin geliş ağ geçidi.
- Bir tünelin geçerlilik süresi.
- İletileri şifreleyebilmek için (tünelden göndermek ve hedefe ulaşmak
 için) herkese açık anahtar çifti.

Yönelticiler, \"Yöneltici bilgilerini\" (RouterInfo) doğrudan \"Ağ veri
tabanına\" (NetDB) gönderirken, \"Kiralama kümeleri\" (LeaseSets) gidiş
tünelleri üzerinden gönderilir (bir yönelticinin kendi \"Kiralama
kümesi\" ile ilişkilendirilmesini önlemek için \"Kiralama kümelerinin\"
anonim olarak gönderilmesi gerekir).

Ağda başarılı bağlantılar kurmak için yukarıdaki kavramları
birleştirebiliriz.

Alice, kendi geliş ve gidiş tünellerini oluşturmak için \"Yöneltici
bilgilerini\" (RouterInfo) toplamak amacıyla \"Ağ veri tabanı\" (NetDB)
üzerinde bir arama yapar. Böylece, tünellerinde sıçrama olarak
kullanabileceği eşlerin listelerini toplar. Daha sonra ilk sıçramaya bir
oluşturma iletisi gönderebilir, bir tünel oluşturulmasını isteyebilir ve
yönelticiden tünel oluşturulana kadar oluşturma iletisini göndermesini
isteyebilir.

::: {.box style="text-align:center;"}
\
\
![Request information on other
routers](images/netdb_get_routerinfo_1.png "Request information on other routers")
                   \
\
![Build tunnel using router
information](images/netdb_get_routerinfo_2.png "Build tunnel using router information")\
\
Şekil 2: Tünelleri oluşturmak için kullanılan yöneltici bilgileri.
:::

\

Alice, Bob\'a bir ileti göndermek istediğinde, önce Bob\'un \"Kiralama
kümesini\" (LeaseSet) bulmak için \"Ağ veri tabanında\" (NetDB) bir
arama yapar ve ona var olan geliş tüneli ağ geçitlerini öğrenir.
Ardından, gidiş tünellerinden birini seçer ve iletiyi Bob\'un geliş
tüneli ağ geçitlerinden birine iletmek için gidiş tünelinin uç noktası
için yönergelerle birlikte aşağıya gönderir. Gidiş tüneli uç noktası bu
yönergeleri aldığında, iletiyi istendiği gibi iletir ve Bob\'un geliş
tüneli ağ geçidi bunu aldığında, tünelden Bob\'un yönelticisine
iletilir. Alice, Bob\'un iletiyi yanıtlayabilmesini istiyorsa, kendi
hedefini iletinin bir parçası olarak açıkça iletmelidir. Bu,
[Streaming](#app.streaming) kitaplığında yapılan daha yüksek düzeyle bir
katman sunularak yapılabilir. Alice ayrıca, Bob\'un yanıt vermek
istemesi durumunda \"Ağ veri tabanı\" (NetDB) araması yapmasına gerek
kalmaması için en son \"Kiralama kümesini\" (LeaseSet) iletiye katarak
yanıt süresini kısaltabilir. Ancak bu seçenek isteğe bağlıdır.

::: {.box style="text-align:center;"}
\
\
![Connect tunnels using
LeaseSets](images/netdb_get_leaseset.png "Connect tunnels using leaseSets")\
\
Şekil 3: \"Kiralama kümelerini\" (LeaseSets) kullanarak gidiş ve geliş
tünellerini bağlamak.
:::

\

Tünellerin kendileri, ağ içindeki eşlere karşı izinsiz açığa çıkmalarını
önlemek için katmanlı şifreleme kullansa da (ağ dışındaki eşlere izin
açığa çıkmayı önlemek için taşıma katmanının yaptığı gibi), gidiş tüneli
uç noktasından ve geliş tüneli ağ geçidinden gelen iletiyi gizlemek için
ek bir uçtan uca şifreleme katmanı eklemek gerekir. Bu \"[Garlic
şifrelemesi](#op.garlic)\", Alice\'in yönelticisinin birden çok iletiyi
tek bir \"Garlic iletisine\" sarmalamasını ve belirli bir ortak
anahtarla şifrelemesini sağlar. Böylece aracı eşler Garlic içinde kaç
ileti olduğunu, bu iletilerin ne söylediğini veya bu iletilerin nerede
olduğunu ya da bu dişin hangi hedefe gönderildiğini belirleyemez. Alice
ve Bob arasında tipik uçtan uca iletişim için, garlic Bob\'un \"Kiralama
kümesinde\" (LeaseSet) yayınlanan ortak anahtarla şifrelenir. Böylece
herkese açık anahtar Bob\'un kendi yönelticisine verilmeden iletinin
şifrelenmesi sağlanır.

Akılda tutulması gereken bir diğer önemli durum, I2P uygulamasının
tamamen ileti temelli olduğu ve yol boyunca bazı iletilerin
kaybolabileceğidir. I2P kullanan uygulamalar, ileti odaklı arayüzleri
kullanabilir ve kendi tıkanıklık denetimi ile güvenilirlik
gereksinimlerini karşılayabilir. Ancak çoğunun en iyi şekilde hizmet
sağlaması için, I2P uygulamasını akış temelli bir ağ olarak görüntülemek
için sağlanan [akış](#app.streaming) kitaplığını yeniden kullanması
gerekir.

## Tüneller {#op.tunnels}

Geliş ve gidiş tünelleri benzer ilkelerle çalışır. Tünel ağ geçidi, bir
dizi tünel iletisi biriktirir ve sonunda bunları tünel aktarımı için bir
şey olarak ön işler. Ardından, ağ geçidi ön işlenmiş verileri şifreler
ve ilk sıçramaya iletir. Bu eş ve sonraki tünel katılımcıları, bir
sonraki eşe iletmeden önce kopya olmadığını doğruladıktan sonra bir
şifreleme katmanı ekler. Sonunda ileti, iletilerin yeniden bölündüğü ve
istendiği gibi iletildiği uç noktaya ulaşır. Fark, tüneli oluşturanın
yaptığı işte ortaya çıkar. Geliş tünellerinde, oluşturucu uç noktadır ve
eklenen tüm katmanların şifresini çözer. Gidiş tünellerinde oluşturucu
ağ geçididir ve tüm katmanların şifresini önceden çözer. Her sıçrama
için şifrelemenin tüm katmanları eklendikten sonra, ileti tünel uç
noktasına net bir şekilde ulaşır.

İletileri iletmek için belirli eşlerin seçilmesi ve bunların özel
sıralaması, hem I2P anonimliğini hem de başarım özelliklerini anlamak
için önemlidir. Ağ veri tabanının (aşağıda) hangi eşlerin sorgulanıp
kayıtları depolayacağını seçmek için kendi ölçütleri olsa da, tünel
oluşturucular ağdaki herhangi bir eşi herhangi bir sırayla (ve hatta
herhangi bir sayıda) tek bir tünelde kullanabilir. Mükemmel gecikme ve
kapasite verileri küresel olarak biliniyor olsaydı, seçim ve sıralama,
istemci tehdit modelleri ve belirli gereksinimleri tarafından
yönlendirilirdi. Ne yazık ki, gecikme ve kapasite verilerinin anonim
olarak toplanması önemsiz değildir ve bu bilgileri sağlamak için
güvenilmeyen eşlere bağlı olmanın anonimlik üzerinde ciddi etkileri
vardır.

Anonimlik açısından en basit yöntem, tüm ağdan rastgele eşler seçmek,
bunları rastgele sıralamak ve bu eşleri sonsuza kadar bu sırayla
kullanmak olur. Başarım açısından bakıldığında, en basit yöntem, gerekli
yedek kapasiteye sahip en hızlı eşleri seçmek, yükü şeffaf olarak
devretmek için yükü farklı eşler arasında dağıtmak ve kapasite bilgileri
değiştiğinde tüneli yeniden oluşturmak olur. İlki hem kırılgan hem de
verimsiz iken, ikincisi için erişilemez bilgiler gerekir ve yetersiz
anonimlik sunar. Bunun yerine I2P, eşleri profillerine göre düzenlemek
için anonimlik farkında ölçüm koduyla birleştirilmiş bir dizi eş seçim
stratejisi sunmaya çalışır.

Temel olarak, I2P etkileşimde bulunduğu eşlerin dolaylı davranışlarını
sürekli olarak ölçerek profillerini oluşturur. Örneğin, bir eş 1,3
saniyede bir \"Ağ veri tabanı\" (NetDB) aramasına yanıt verdiğinde, bu
gidiş dönüş gecikmesi tüm yönelticilerin profillerine kaydedilerek,
İstek ve yanıtın geçtiği iki tünelde (geliş ve gidiş) ve sorgulanan eşin
profilinde yer alır. Taşıma katmanı gecikmesi veya tıkanıklık gibi
doğrudan ölçümler, manipüle edilebildiği ve ölçüm yönelticisi ile
ilişkilendirilebileceğinden ve onları önemsiz saldırılara açık
bırakabileceğinden profilin bir parçası olarak kullanılmaz. Bu profiller
toplanırken, başarımını, gecikmesini, çok sayıda etkinliği işleme
kapasitesini, şu anda aşırı yüklü olup olmadığını ve ağ ile ne kadar
bütünleşmiş olduğunu özetlemek için her biri üzerinde bir dizi hesaplama
yapılır. Daha sonra bu hesaplamalar, yönelticileri hızlı ve yüksek
kapasiteli, yüksek kapasiteli, sorunsuz ve sorunlu olmak üzere dört
düzeyde gruplamak için etkin eşleri karşılaştırmakta kullanılır. Bu
düzeylerin eşikleri devingen olarak belirlenir ve şu anda oldukça basit
algoritmalar kullanır. Ancak alternatifleri de vardır.

Bu profil verileri kullanılarak, en basit uygun eş seçimi stratejisi,
eşleri üst düzeyden (hızlı ve yüksek kapasiteli) rastgele seçmektir. Şu
anda istemci tünelleri bu şekilde dağıtılmaktadır. Keşif tünelleri (\"Ağ
veri tabanı\" (NetDB) ve tünel yönetimi için kullanılır) \"sorunsuz\"
düzeyinden (\'daha iyi\" katmanlardaki yönelticileri de içerir) rastgele
eşler seçer. Eşler arası yönelticileri daha geniş bir şekilde örnekleme
olanağı sağlar ve aslında rastgele [tepe
tırmanışı](https://en.wikipedia.org/wiki/Hill_climbing) ile eş seçimini
iyileştirir. Ancak bu stratejiler, öncül ve \"Ağ veri tabanı\" (NetDB)
hasat saldırıları ile yönelticinin en üst düzeyindeki eşler hakkında
bilgi sızdırır. Buna karşılık, yükü eşit olarak dengelememekle birlikte,
belirli düşman sınıfları tarafından düzenlenen saldırılara karşı koyacak
çeşitli alternatifler vardır.

Rastgele bir anahtar seçerek ve eşleri ondan XOR uzaklıklarına göre
sıralayarak, eşlerin başarısızlık oranına ve düzeyin karıştırılmasına
göre öncül ve hasat saldırılarında sızdırılan bilgiler azaltılır. \"Ağ
veri tabanı\" (NetDB) hasat saldırılarıyla başa çıkmak için başka bir
basit strateji, geliş tüneli ağ geçitlerini düzeltmek ve aynı zamanda
tünellerdeki eşleri daha da rastgele hale getirmektir. İstemcinin
bağlantı kurduğu düşmanlara yönelik önceki saldırılarla başa çıkmak için
gidiş tüneli uç noktaları da sabit kalır. En çok maruz kalan noktada
hangi eşin düzeltileceğinin seçiminin elbette bir süre sınırı olmalıdır.
Çünkü sonunda tüm eşler başarısız olur. Böylece diğer yönelticilerin
sorunları arasında ölçülen ortalama süreyi taklit etmek için tepkisel
olarak ayarlanabilir ya da etkisel olarak önlenebilir. Bu iki strateji,
sırayla, sabit bir açık eş ve tüneller arasında bir XOR tabanlı sıralama
kullanılarak birleştirilebilir. Daha katı bir strateji, tam eşleri ve
olası bir tünelin sıralamasını düzeltir. Yalnızca her biri aynı şekilde
katılmayı kabul ederse tek tek eşler kullanılır. Bu yöntem, XOR tabanlı
sıralamadan farklıdır, çünkü her bir eşin öncülü ve ardılı her zaman
aynıdır. XOR ise yalnızca sıralarının değişmediğinden emin olur.

As mentioned before, I2P currently (release 0.8) includes the tiered
random strategy above, with XOR-based ordering. A more detailed
discussion of the mechanics involved in tunnel operation, management,
and peer selection can be found in the [tunnel
spec]().

## Ağ veri tabanı {#op.netdb}

As mentioned earlier, I2P\'s netDb works to share the network\'s
metadata. This is detailed in [the network
database]() page, but a basic explanation is
available below.

All I2P routers contain a local netDb, but not all routers participate
in the DHT or respond to leaseset lookups. Those routers that do
participate in the DHT and respond to leaseset lookups are called
\'floodfills\'. Routers may be manually configured as floodfills, or
automatically become floodfill if they have enough capacity and meet
other criteria for reliable operation.

Other I2P routers will store their data and lookup data by sending
simple \'store\' and \'lookup\' queries to the floodfills. If a
floodfill router receives a \'store\' query, it will spread the
information to other floodfill routers using the [Kademlia
algorithm](http://en.wikipedia.org/wiki/Kademlia). The \'lookup\'
queries currently function differently, to avoid an important [security
issue](#lookup). When a lookup is done, the
floodfill router will not forward the lookup to other peers, but will
always answer by itself (if it has the requested data).

Ağ veri tabanında iki türde bilgi depolanır.

- **\"Yöneltici bilgileri\" (RouterInfo)** belirli bir I2P yönelticisi
 ve nasıl bağlantı kurulacağı hakkında bilgileri tutar.
- **\"Kiralama kümesi\" (LeaseSet)** belirli bir hedefin bilgilerini
 tutar (I2P sitesi, e-posta sunucusu gibi)

Tüm bu bilgiler, yayınlayan tarafça imzalanır ve bilgileri kullanan veya
depolayan herhangi bir I2P yönelticisi tarafından doğrulanır. Ek olarak,
eski kayıtların tutulmasını ve olası saldırıları önlemek için verilerde
süre bilgisi bulunur. Bu aynı zamanda I2P tarafından doğru zamanı
korumak, ara sıra bazı SNTP sunucularını sorgulamak (varsayılan olarak
[pool.ntp.org](http://www.pool.ntp.org/) round robin) ve taşıyıcı
katmanındaki yönelticiler arasındaki sapmayı algılamak için gerekli kodu
bir araya getirmekte kullanılır.

Bazı ek açıklamalar da önemlidir.

- **Yayınlanmamış ve \"Şifrelenmiş kiralama kümeleri\"
 (EncryptedLeaseSets):**

 One could only want specific people to be able to reach a
 destination. This is possible by not publishing the destination in
 the netDb. You will however have to transmit the destination by
 other means. This is supported by \'encrypted leaseSets\'. These
 leaseSets can only be decoded by people with access to the
 decryption key.

- **Ön yükleme:**

 Bootstrapping the netDb is quite simple. Once a router manages to
 receive a single routerInfo of a reachable peer, it can query that
 router for references to other routers in the network. Currently, a
 number of users post their routerInfo files to a website to make
 this information available. I2P automatically connects to one of
 these websites to gather routerInfo files and bootstrap. I2P calls
 this bootstrap process \"reseeding\".

- **Arama ölçeklenebilirliği:**

 Lookups in the I2P network are iterative, not recursive. If a lookup
 from a floodfill fails, the lookup will be repeated to the
 next-closest floodfill. The floodfill does not recursively ask
 another floodfill for the data. Iterative lookups are scalable to
 large DHT networks.

## Taşıyıcı iletişim kuralları {#op.transport}

Yönelticiler arasındaki iletişimde, iletişim kurulan yönelticinin
belirli bir iletiyi alması gereken yöneltici olduğunu doğrulanırken, dış
düşmanlara karşı gizlilik ve bütünlük sağlanması gerekir. Yönelticilerin
diğer yönelticilerle nasıl iletişim kurduğunun ayrıntıları kritik
değildir. Temel gereksinimleri karşılamak için farklı noktalarda üç ayrı
iletişim kuralı kullanılmıştır.

I2P currently supports two transport protocols,
[NTCP2]() over TCP, and
[SSU2]() over UDP. These have replaced the
previous versions of the protocols, [NTCP]() and
[SSU](), which are now deprecated. Both protocols
support both IPv4 and IPv6. By supporting both TCP and UDP transports,
I2P can effectively traverse most firewalls, including those intended to
block traffic in restrictive censorship regimes. NTCP2 and SSU2 were
designed to use modern encryption standards, improve traffic
identification resistance, increase efficiency and security, and make
NAT traversal more robust. Routers publish each supported transport and
IP address in the network database. Routers with access to public IPv4
and IPv6 networks will usually publish four addresses, one for each
combination of NTCP2/SSU2 with IPv4/IPv6.

[SSU2]() supports and extends the goals of SSU.
SSU2 has many similarities to other modern UDP-based protocols such as
Wireguard and QUIC. In addition to the reliable transport of network
messages over UDP, SSU2 provides specialized facilities for
peer-to-peer, cooperative IP address detection, firewall detection, and
NAT traversal. As described in the [SSU spec]():

> Bu iletişim kuralının amacı, güvenli, kimliği doğrulanmış, yarı
> güvenilir ve sıralanmamış ileti aktarımını sağlamak ve üçüncü
> tarafların kolayca fark edemeyeceği kadar az miktarda veri ortaya
> çıkarmaktır. TCP dostu tıkanıklık denetiminin yanında yüksek düzeyli
> iletişimi desteklerken PMTU algılamasını da içerebilir. Ev
> kullanıcıları için toplu verileri yeterli hızlarda verimli bir şekilde
> aktarabilmelidir. Ayrıca, NAT veya güvenlik duvarı gibi yaygın
> kullanılan ağ engellerini ele alan teknikleri desteklemelidir.

NTCP2 supports and extends the goals of NTCP. It provides an efficient
and fully encrypted transport of network messages over TCP, and
resistance to traffic identification, using modern encryption standards.

I2P, aynı anda birden fazla taşıyıcı kullanılmasını destekler. Gidiş
bağlantısı için belirli bir taşıyıcı \"teklifler\" yoluyla seçilir.
Bağlantı için her taşıyıcı teklifi ve bu tekliflerin göreli değeri
önceliği belirler. Taşıyıcılar, eş ile daha önce kurulmuş bir bağlantı
olup olmadığına bağlı olarak farklı tekliflerle yanıt verebilir.

The bid (priority) values are implementation-dependent and may vary
based on traffic conditions, connection counts, and other factors.
Routers also publish their transport preferences for inbound connections
in the network database as transport \"costs\" for each transport and
address.

## Şifreleme {#op.crypto}

I2P uses cryptography at several protocol layers for encryption,
authentication, and verification. The major protocol layers are:
transports, tunnel build messages, tunnel layer encryption, network
database messages, and end-to-end (garlic) messages. I2P\'s original
design used a small set of cryptographic primitives that at the time
were considered secure. These included ElGamal asymmetric encryption,
DSA-SHA1 signatures, AES256/CBC symmetric encryption, and SHA-256
hashes. As available computing power increased and cryptographic
research evolved substantially over the years, I2P needed to upgrade its
primitives and protocols. Therefore, we added a concept of \"encryption
types\" and \"signature types\", and extended our protocols to include
these identifiers and indicate support. This allows us to periodically
update and extend the network support for modern cryptography and
future-proof the network for new primitives, without breaking backward
compatibility or requiring a \"flag day\" for network updates. Some
signature and encryption types are also reserved for experimental use.

The current primitives used in most protocol layers are X25519 key
exchange, EdDSA signatures, ChaCha20/Poly1305 authenticated symmetric
encryption, and SHA-256 hashes. AES256 is still used for tunnel layer
encryption. These modern protocols are used for the vast majority of
network communication Older primitives including ElGamal, ECDSA, and
DSA-SHA1 continue to be supported by most implementations for backward
compatibility when communicating with older routers. Some old protocols
have been deprecated and/or removed completely. In the near future we
will begin research on a migration to post-quantum (PQ) or hybrid-PQ
encryption and signatures to maintain our robust security standards.

These cryptographic primitives are combined together to provide I2P\'s
layered defenses against a variety of adversaries. At the lowest level,
inter-router communication is protected by the transport layer security.
[Tunnel](#op.tunnels) messages passed over the transports have their own
layered encryption. Various other messages are passed along inside
\"garlic messages\", which are also encrypted.

### Garlic iletileri {#op.garlic}

Garlic messages are an extension of \"onion\" layered encryption,
allowing the contents of a single message to contain multiple
\"cloves\" - fully formed messages alongside their own instructions for
delivery. Messages are wrapped into a garlic message whenever the
message would otherwise be passing in cleartext through a peer who
should not have access to the information - for instance, when a router
wants to ask another router to participate in a tunnel, they wrap the
request inside a garlic, encrypt that garlic to the receiving router\'s
public key, and forward it through a tunnel. Another example is when a
client wants to send a message to a destination - the sender\'s router
will wrap up that data message (alongside some other messages) into a
garlic, encrypt that garlic to the public key published in the
recipient\'s leaseSet, and forward it through the appropriate tunnels.

Şifreleme katmanının içindeki her bir dişe eklenmiş \"yönergeler\",
dişin yerel olarak, uzak bir yönelticiye ya da uzak bir yönelticideki
uzak bir tünele aktarılmasını isteme yeteneğini bulundurur. Bu
yönergelerde, bir eşin aktarımın belirli bir zaman veya koşul
karşılanana kadar ertelenmesini istemesini sağlayan alanlar vardır.
Ancak bunlar [önemsiz gecikmeler](#future.variablelatency) dağıtılana
kadar kabul edilmez. Garlic iletilerini tünel oluşturmadan herhangi bir
sayıda sıçrama ile açıkta yöneltmek ya da tünel iletilerini garlic
iletilerine sararak ve tüneldeki bir sonraki sıçramaya iletmeden önce
birkaç sıçramadan geçirerek yönlendirilebilir. Ancak bu teknikler şu
andaki uygulama kullanılmıyor

### Oturum etiketleri {#op.sessiontags}

As an unreliable, unordered, message based system, I2P uses a simple
combination of asymmetric and symmetric encryption algorithms to provide
data confidentiality and integrity to garlic messages. The original
combination was referred to as ElGamal/AES+SessionTags, but that is an
excessively verbose way to describe the simple use of 2048bit ElGamal,
AES256, SHA256 and 32 byte nonces. While this protocol is still
supported, most of the network has migrated to a new protocol,
ECIES-X25519-AEAD-Ratchet. This protocol combines X25519,
ChaCha20/Poly1305, and a synchronized PRNG to generate the 32 byte
nonces. Both protocols will be briefly described below.

#### ElGamal/AES+SessionTags {#op.elg}

Bir yöneltici ilk kez başka bir yönelticiye göndereceği bir garlic
iletisini şifrelemek istediğinde, bir AES-256 oturum anahtarı için
anahtarlama materyalini ElGamal ile şifreler ve bu şifrelenmiş ElGamal
bloğunun ardından AES-256/CBC ile şifrelenmiş yükü ekler. Şifrelenmiş
yüke ek olarak, AES ile şifrelenmiş bölümü yük uzunluğu, şifrelenmemiş
yükün SHA-256 karması ve ayrıca bir dizi \"oturum etiketi\" - rastgele
32 baytlık olmayanlar - bulunur. Gönderici bir dahaki sefere bir garlic
iletisini başka bir yönlendiriciye şifrelemek istediğinde, ElGamal yeni
bir oturum anahtarını şifrelemek yerine, daha önce teslim edilmiş oturum
etiketlerinden birini seçer ve AES, daha önce olduğu gibi, o oturum
etiketiyle kullanılan oturum anahtarını kullanarak yükü şifreler. Bu
bilgi oturum etiketinin başına eklenir. Bir yöneltici bir garlic
şifrelenmiş iletisi aldığında, uygun bir oturum etiketiyle eşleşip
eşleşmediğini görmek için ilk 32 baytı kontrol eder. Eşleşme bulunursa
yalnızca AES iletisinin şifresini çözer. Bulunmazsa ElGamal ilk bloğun
şifresini çözer.

Her oturum etiketi, iç izleyicilerin aynı yönelticiler arasında olduğu
gibi farklı iletileri gereksiz yere ilişkilendirmesini önlemek için
yalnızca bir kez kullanılabilir. ElGamal/AES+Oturum etiketi şifrelemiş
iletisinin göndericisi, ne zaman ve kaç etiketin teslim edileceğini
seçer ve alıcıya bir sürü iletiyi kapsayacak kadar yeterli etiket
hazırlar. Garlic iletileri küçük bir ek iletiyi bir diş (\"teslim durumu
iletisi\") olarak paketleyerek etiket tesliminin başarılı olduğunu
algılayabilir - garlic iletisi hedeflenen alıcıya ulaştığında ve şifresi
başarıyla çözüldüğünde, bu küçük teslim durumu dişlerden biridir. Açığa
çıkar ve alıcının dişi özgün göndericiye geri göndermesi için yönergeler
içerir (elbette bir geliş tüneli üzeirnden). Özgün gönderici bu teslim
durumu iletisini aldığında, garlic iletisinde gruplanan oturum
etiketlerinin başarıyla iletildiğini bilir.

Oturum etiketlerinin ömürleri kısadır. bu sürenin sonunda
kullanılmazlarsa atılır. Ek olarak, her bir anahtar için depolanan
miktar ve anahtarların sayısı sınırlıdır. Çok fazla gelirse, yeni veya
eski iletiler kaybolabilir Gönderici, oturum etiketlerini kullanan
iletilerin geçip geçmediğini izler ve yeterli iletişim yoksa, daha önce
düzgün bir şekilde iletildiği varsayılanları bırakarak en pahalı ElGamal
şifrelemesine geri dönebilir.

#### ECIES-X25519-AEAD-Ratchet {#op.ratchet}

ElGamal/AES+SessionTags required substantial overhead in a number of
ways. CPU usage was high because ElGamal is quite slow. Bandwidth was
excessive because large numbers of session tags had to be delivered in
advance, and because ElGamal public keys are very large. Memory usage
was high due to the requirement to store large amounts of session tags.
Reliability was hampered by lost session tag delivery.

ECIES-X25519-AEAD-Ratchet was designed to address these issues. X25519
is used for key exchange. ChaCha20/Poly1305 is used for authenticated
symmetric encryption. Encryption keys are \"double ratcheted\" or
rotated periodically. Session tags are reduced from 32 bytes to 8 bytes
and are generated with a PRNG. The protocol has many similarities to the
signal protocol used in Signal and WhatsApp. This protocol provides
substantially lower overhead in CPU, RAM, and bandwidth.

The session tags are generated from a deterministic synchronized PRNG
running at both ends of the session to generate session tags and session
keys. The PRNG is a HKDF using a SHA-256 HMAC, and is seeded from the
X25519 DH result. Session tags are never transmitted in advance; they
are only included with the message. The receiver stores a limited number
of session keys, indexed by session tag. The sender does not need to
store any session tags or keys because they are not sent in advance;
they may be generated on-demand. By keeping this PRNG roughly
synchronized between the sender and recipient (the recipient precomputes
a window of the next e.g. 50 tags), the overhead of periodically
bundling a large number of tags is removed.

# Gelecek {#future}

I2P\'s protocols are efficient on most platforms, including cell phones,
and secure for most threat models. However, there are several areas
which require further improvement to meet the needs of those facing
powerful state-sponsored adversaries, and to meet the threats of
continued cryptographic advances and ever-increasing computing power.
Two possible features, restricted routes and variable latency, were
propsed by jrandom in 2003. While we no longer plan to implement these
features, they are described below.

## Kısıtlanmış yöneltme işlemi {#future.restricted}

I2P, anonimlik ve güvenlik sunmak için uçtan uca ilkesinden yararlanan,
işlevsel bir paket anahtarlamalı ağın üzerinde çalıştırılmak üzere
tasarlanmış bir kaplama ağıdır. İnternet artık uçtan uca ilkesini (NAT
kullanımı nedeniyle) tam olarak benimsemese de, I2P ağının erişilebilir
olması için ağın önemli bir bölümünün uçtan uca olması gerekir.
Kenarlarda kısıtlanmış rotalar kullanarak çalışan birkaç eş olabilir.
Ancak I2P, çoğu eşin erişilemediği bozulmuş durum için uygun bir
yöneltme algoritması sunmaz Bununla birlikte, böyle bir algoritmayı
kullanan bir ağ üzerinde çalışacaktır.

Restricted route operation, where there are limits to what peers are
reachable directly, has several different functional and anonymity
implications, dependent upon how the restricted routes are handled. At
the most basic level, restricted routes exist when a peer is behind a
NAT or firewall which does not allow inbound connections. This was
largely addressed by integrating distributed hole punching into the
transport layer, allowing people behind most NATs and firewalls to
receive unsolicited connections without any configuration. However, this
does not limit the exposure of the peer\'s IP address to routers inside
the network, as they can simply get introduced to the peer through the
published introducer.

Beyond the functional handling of restricted routes, there are two
levels of restricted operation that can be used to limit the exposure of
one\'s IP address - using router-specific tunnels for communication, and
offering \'client routers\'. For the former, routers can either build a
new pool of tunnels or reuse their exploratory pool, publishing the
inbound gateways to some of them as part of their routerInfo in place of
their transport addresses. When a peer wants to get in touch with them,
they see those tunnel gateways in the netDb and simply send the relevant
message to them through one of the published tunnels. If the peer behind
the restricted route wants to reply, it may do so either directly (if
they are willing to expose their IP to the peer) or indirectly through
their outbound tunnels. When the routers that the peer has direct
connections to want to reach it (to forward tunnel messages, for
instance), they simply prioritize their direct connection over the
published tunnel gateway. The concept of \'client routers\' simply
extends the restricted route by not publishing any router addresses.
Such a router would not even need to publish their routerInfo in the
netDb, merely providing their self signed routerInfo to the peers that
it contacts (necessary to pass the router\'s public keys).

Kısıtlanmış rotaların ardında bulunanlar için, büyük olasılıkla diğer
insanların tünellerine daha az katkıda bulunacakları ve bağlı oldukları
yönelticiler, aksi durumda açığa çıkmayacak trafik kalıplarını
çıkarabilecekleri için uzlaşmalar vardır. Öte yandan, bu uzlaşmanın
maliyeti, bir IP adresinin kullanıma sunulmasının maliyetinden daha
düşükse, buna değebilir. Bu, elbette, yönelticinin kısıtlı bir yöneltme
temasının arkasındaki eşlerin düşman olmadığını varsayar. Ya ağ çok
büyük olduğundan, düşman bir eşe bağlanma olasılığı çok küçüktür ya da
güvenilir (ve belki de geçici) eşler kullanılır.

Restricted routes are complex, and the overall goal has been largely
abandoned. Several related improvements have greatly reduced the need
for them. We now support UPnP to automatically open firewall ports. We
support both IPv4 and IPv6. SSU2 improved address detection, firewall
state determination, and cooperative NAT hole punching. SSU2, NTCP2, and
address compatibility checks ensure that tunnel hops can connect before
the tunnel is built. GeoIP and country identification allow us to avoid
peers in countries with restrictive firewalls. Support for \"hidden\"
routers behind those firewalls has improved. Some implementations also
support connections to peers on overlay networks such as Yggdrasil.

## Değişken gecikme {#future.variablelatency}

Başlangıçtaki I2P çabalarının çoğu düşük gecikmeli iletişim üzerine olsa
da, tasarım başından beri değişken gecikmeli hizmetler düşünülerek
yapıldı. En temel düzeyde, I2P üzerinde çalışan uygulamalar, trafik
kalıplarını düşük gecikmeli trafikle harmanlarken orta ve yüksek
gecikmeli iletişimin anonimliğini sunabilir. I2P içinde garlic
şifrelemesi yoluyla kendi orta ve yüksek gecikmeli iletişimini
sunabilir. İleti belirli bir gecikmeden sonra, belirli bir zamanda,
belirli sayıda iletiden sonra ya da başka bir karma strateji ile
gönderilebilir. Katmanlı şifrelemeyle, yöneltici yalnızca gecikme
isteğini açıklayan dişin yüksek gecikme süresi gerektirdiğini bilir ve
bu da trafiğin düşük gecikmeli trafikle daha fazla karışmasını sağlar.
İletim ön koşulu karşılandıktan sonra, yöneltici dişi (kendisi büyük
olasılıkla bir garlic iletisidir) istendiği gibi bir yönelticiye bir
tünele ya da büyük olasılıkla uzak bir istemci hedefine gönderir.

The goal of variable latency services requires substantial resources for
store-and-forward mechanisms to support it. These mechanisms can and are
supported in various messaging applications, such as i2p-bote. At the
network level, alternative networks such as Freenet provide these
services. We have decided not to pursue this goal at the I2P router
level.

# Benzer sistemler {#similar}

I2P mimarisi, ileti odaklı ara yazılım kavramları, \"Dağıtılmış karma
tablosu\" (DHT) topolojisi, serbest rota karma ağlarının anonimliği ve
şifrelemesi ile paket anahtarlamalı ağların uyarlanabilirliği üzerine
kuruludur. Değeri, yeni algoritma kavramlarından değil, var olan
sistemlerin ve makalelerin araştırma sonuçlarını birleştiren dikkatli
mühendislikten gelir. Hem teknik hem de işlevsel karşılaştırmalar için
incelemeye değer birkaç benzer çaba olsa da, özellikle iki tanesi öne
çıkarıldı - Tor ve Freenet.

See also the [Network Comparisons Page]().
Note that these descriptions were written by jrandom in 2003 and may not
currently be accurate.

## Tor {#similar.tor}

*[site](https://www.torproject.org/)*

İlk bakışta Tor ve I2P, işlevsellik ve anonimlikle ilgili oldukça
benzerdir. I2P gelişimi, Tor üzerindeki erken aşama çabalarını bilmeden
önce başlamış olsa da, özgün onion yöneltme ve ZKS çabalarından alınan
derslerin çoğu I2P tasarımı ile bütünleştirildi. Dizin sunucuları ile
temelde güvenilir, merkezi bir sistem oluşturmak yerine, I2P, var olan
kaynaklardan en iyi şekilde nasıl yararlanılacağını belirlemek için her
bir eşin diğer yönelticilerin profilini çıkarma sorumluluğunu üstlendiği
kendi kendini düzenleyen bir ağ veri tabanı kullanır. Diğer önemli bir
fark, hem I2P hem de Tor katmanlı ve sıralı yollar (tüneller ve
devreler/akışlar) kullanmasına rağmen, I2P temelde paket anahtarlamalı
bir ağ iken, Tor ağının temelde devre anahtarlamalı olması nedeniyle I2P
ağı, sorunlar ve yedekli yolları kullanarak verileri var olan kaynaklar
arasında dengeler ve tıkanıklık veya diğer ağlar etrafından şeffaf bir
şekilde yöneltme sağlar. Tor, bütünleşik çıkış vekil sunucusu keşfi ve
seçimi sunarak faydalı çıkış vekil sunucu işlevselliği sunarken, I2P, bu
tür uygulama katmanı kararlarını I2P üzerinde çalışan uygulamalara
bırakır. Aslında I2P, geliştiricilere daha iyi başarım sunmak için kendi
etki alanına özgü bilgilerinden yararlanarak farklı stratejiler
denemeleri için TCP benzeri akış kitaplığını uygulama katmanı dışına
açtı.

Anonimlik açısından bakıldığında, çekirdek ağlar karşılaştırıldığında
çok fazla benzerlik görülebilir. Ancak, birkaç önemli farklılık da
vardır. Ağ içindeki bir saldırganla ya da çok sayıdaki dış saldırganla
uğraşırken, Tek yönlü I2P tünelleri, yalnızca akışların kendilerine
bakarak, çift yönlü Tor devrelerinin taşıyacağının yarısı kadar trafik
verisi açığa çıkarır. Bir HTTP isteği ve yanıtı Tor ağında aynı yolu
izlerken, I2P ağında isteği oluşturan paketler bir ya da daha fazla
çıkış tünelinden dışarı çıkar ve yanıtı oluşturan paketler bir ya da
daha fazla farklı geliş tünelinden geri gelir. I2P eş seçimi ve sıralama
stratejileri önceki saldırıları yeterince ele alırken, çift yönlü
tünellere geçiş gerekliyse, aynı yönelticiler boyunca basitçe bir geliş
ve gidiş tüneli oluşturabiliriz.

Tor üzerinde teleskopik tünel oluşturma kullanımında başka bir anonimlik
sorunu ortaya çıkıyor. Bir devredeki hücreler bir saldırganın düğümünden
geçerken basit paket sayımı ve zamanlama ölçümleri, düşmanın devre
içinde nerede olduğuna ilişkin istatistiksel bilgileri ortaya çıkarıyor.
Bu verilerin açığa çıkmaması için I2P tek bir ileti ile tek yönlü tünel
oluşturuyor. Bir saldırgan bir dizi güçlü öncül, kavşak ve trafik
doğrulama saldırısı gerçekleştirebileceğinden, bir tünelin konumunun
korunması önemlidir.

Genel olarak, Tor ve I2P odak noktalarında birbirlerini tamamlar. Tor,
yüksek hızlı anonim İnternet çıkış vekil sunucusu sağlamaya çalışırken,
I2P kendi içinde merkezi olmayan esnek bir ağ sağlamaya çalışır.
Teoride, ikisi de her iki amaca da ulaşmak için kullanılabilir. Ancak
sınırlı geliştirme kaynakları göz önüne alındığında, her ikisinin de
güçlü ve zayıf yönleri vardır. I2P geliştiricileri, Tor uygulamasını I2P
ağının tasarımından yaralanacak şekilde değiştirmek için gerekli
adımları düşündüler. Ancak Tor uygulamasının kıt kaynaklar altında
yaşayabilirliği konusundaki endişeler, I2P paket anahtarlama mimarisinin
kıt kaynakları daha etkili bir şekilde kullanabileceğini gösteriyor.

## Freenet {#similar.freenet}

*[site](http://www.freenetproject.org/)*

Freenet, I2P tasarımının ilk aşamalarında büyük bir rol oynadı. Tamamen
ağ içinde yer alan canlı bir takma adlı topluluğun yaşayabilirliğini
kanıtlayarak, çıkış vekil sunucularının doğasında bulunan tehlikelerden
kaçınılabileceğini gösterdi. İlk I2P tohumu, ölçeklenebilir, anonim ve
güvenli bir noktadan noktaya iletişimin karmaşıklıklarını sansüre
dayanıklı dağıtılmış bir veri deposunun karmaşıklıklarından ayırmaya
çalışan Freenet için bir yedek iletişim katmanı olarak başladı. Ancak
zamanla, Freenet algoritmalarının doğasında bulunan bazı anonimlik ve
ölçeklenebilirlik sorunları, I2P odak noktasının, bir Freenet bileşeni
olmak yerine kesinlikle genel bir anonim iletişim katmanı sağlamak
olması gerektiğini açıkça ortaya koydu. Yıllar geçtikçe, Freenet
geliştiricileri eski tasarımdaki zayıflıkları görmeye başladı ve önemli
bir anonimlik sunmak için bir \"ön karışım\" katmanına gerek
duyacaklarını önermeye yöneldi. Başka bir deyişle, Freenet I2P veya Tor
gibi bir karma ağ üzerinde çalışmalıdır. \"İstemci düğümleri\", karma ağ
üzerinde \"sunucu düğümleri\" üzerine veri alma istekleri gönderir ve
verileri yayınlar. Ardından verileri buluşsal dağıtılmış Freenet
depolama algoritmalarına göre alır ve depolar.

Freenet işlevselliği I2P işlevlerini tamamlar. Çünkü Freenet yerel
olarak orta ve yüksek gecikmeli sistemleri çalıştırmak için birçok araç
sunarken, I2P yerel olarak yeterli anonimlik sunmaya uygun düşük
gecikmeli karma ağı sağlar. Karma ağı sansüre dayanıklı dağıtılmış veri
deposundan ayırma mantığı mühendislik, anonimlik, güvenlik ve kaynak
ayırma açısından hala açık görünüyor. Bu yüzden umarım Freenet ekibi,
I2P veya Tor gibi var olan karma ağları yalnızca yeniden kullanmak (veya
gerektiğinde iyileştirilmesine yardımcı olmak) yerine bu yönde çaba
harcar.

# Appendix A: Application layer {#app}

Aslında I2P pek bir şey yapmaz. Yalnızca uzak hedeflere iletiler
gönderir ve yerel hedeflere yönelik iletileri alır. İlginç çalışmaların
çoğu, I2P üzerrindeki katmanlarda olur. I2P kendi başına anonim ve
güvenli bir IP katmanı olarak, [streaming kitaplığı](#app.streaming) ile
bunun üzerinde anonim ve güvenli bir TCP katmanının bir uygulaması
olarak görülebilir. Bunun ötesinde, [I2PTunnel](#app.i2ptunnel), I2P
ağına girmek veya çıkmak için genel bir TCP vekil sunucu sistemi sunar.
Ayrıca çeşitli ağ uygulamaları son kullanıcılar için daha fazla
işlevsellik sağlar.

## Streaming kitaplığı {#app.streaming}

I2P Streaming kitaplığı, genel bir akış arabirimi (TCP soketlerini
yansıtma) olarak görülebilir ve uygulama, I2P üzerindeki yüksek
gecikmeyi hesaba katmak için çeşitli iyileştirmelerle [kayan aralık
iletişim kuralını](http://en.wikipedia.org/wiki/Sliding_Window_Protocol)
destekler. Akışlar bireysel olarak en fazla paket boyutunu ve diğer
seçenekleri ayarlayabilir. Ancak varsayılan olarak sıkıştırılmış 4KB,
kayıp iletilerin yeniden iletilmesinin bant genişliği maliyetleri ile
çoklu iletilerin gecikmesi arasında makul bir denge kuruyor gibi
görünmektedir.

Ek olarak, sonraki iletilerin nispeten yüksek maliyeti göz önüne
alındığında, Streaming kitaplığının iletileri programlama ve teslim etme
iletişim kuralı, iletilen bireysel iletilerin var olduğu kadar çok bilgi
içermesine izin verecek şekilde iyileştirilmiştir. Örneğin, Streaming
kitaplığı aracılığıyla vekil sunucu üzerinden geçilrilen küçük bir HTTP
işlemi tek bir gidiş-dönüşte tamamlanabilir. İlk ileti bir SYN, FIN
iletileri ile küçük yükü (genellikle bir HTTP isteğine uyar) paketler ve
yanıt SYN, FIN, ACK iletileri ile küçük yükü paketler (birçok HTTP
yanıtı uygundur). HTTP sunucusuna SYN/FIN/ACK iletilerinin alındığını
söylemek için ek bir ACK iletilmesi gerekirken, yerel HTTP vekil
sunucusu tarayıcıya tam yanıtı hemen teslim edebilir.

Bununla birlikte, genel olarak, Streaming kitaplığı, kayan aralıklar,
tıkanıklık kontrol algoritmaları (hem yavaş başlatma hem de
tıkanıklıktan kaçınma) ve genel paket davranışı (ACK, SYN, FIN, RST,
vb.) ile bir TCP soyutlamasına benzer.

## Adlandırma kitaplığı ve adres defteri {#app.naming}

*For more information see the [Naming and Address
Book]() page.*

*Developed by: *

I2P üzerinde adlandırma, en başından beri, çeşitli olasılıkların
savunucuları ile sıkça tartışılan bir konu olmuştur. Bununla birlikte,
I2P yapısının güvenli iletişim ve merkezi olmayan çalışma şekli için
doğal istekleri göz önüne alındığında, geleneksel DNS benzeri adlandırma
sistemi ve \"çoğunluk kuralları\" oylama sistemleri açıkça geçersizdir.
Bunun yerine, I2P, genel bir adlandırma kitaplığı ve yerel bir adla
hedef eşleme üzerinde çalışacak şekilde tasarlanmış bir temel
uygulamanın yanı sıra \"Adres defteri\" adı verilen isteğe bağlı bir ek
uygulamayla birlikte gelir. Adres defteri, yalnızca yerel benzersizliği
zorunlu kılarak, yalnızca insan tarafından okunabilen tüm adların
küresel olarak benzersiz olması çağrısını feda eden, ağa güvenmeye
odaklı, güvenli, dağıtılmış ve insan tarafından okunabilir bir
adlandırma sistemidir. I2P ağındaki tüm iletiler, hedefleri tarafından
şifrelenmiş olarak adreslenirken, farklı kişilerin, farklı hedefleri
gösteren aynı \"Alice\" yerel adres defteri kayıtları bulunabilir.
İnsanlar, güvendikleri ağlarda belirtilen eşlerin yayınlanmış adres
defterlerini içe aktararak, üçüncü bir taraf aracılığıyla sağlanan
kayıtları ekleyerek ya da (bazı kişiler bir ilk gelen ilk alır kayıt
sistemi kullanarak bazı yayınlanmış adres defterleri düzenlerse) yine de
yeni adlar keşfedebilir. İnsanlar bu adres defterlerini geleneksel DNS
sistemini taklit eden ad sunucuları olarak değerlendirmeyi seçebilirler.

I2P, DNS benzeri hizmetlerin kullanımını desteklemez, çünkü bir sitenin
ele geçirilmesinin vereceği zarar çok büyük olabilir ve güvenli olmayan
hedeflerin hiçbir değeri yoktur. DNSsec verileri kayıt şirketlerine ve
sertifika yetkililerine geri giderken, I2P ile, bir hedefe gönderilen
veriler, hedefin herkese açık anahtarları ile şifrelendiğinden ve bir
hedefin kendisi yalnızca bir herkese açık anahtar ve sertifika çifti
olduğundan, istekler engellenemez veya yanıta müdahale edilemez. Öte
yandan DNS tarzı sistemler, arama yolundaki ad sunucularından herhangi
birinin basit hizmet reddi ve sahtekarlık saldırıları başlatmasına izin
verir. Yanıtları doğrulamak için merkezi sertifika yetkilileri
tarafından imzalanmış bir sertifika eklemek, kötü niyetli ad sunucusu
sorunlarının çoğunu giderse de, kötü niyetli sertifika yetkilisi
saldırılarının yanında yeniden yürütme saldırılarına da açık kalır.

Oylama biçimindeki adlandırma da tehlikelidir. Özellikle de anonim
sistemlerdeki Sybil saldırılarının etkinliği göz önüne alındığında -
saldırgan yalnızca keyfi olarak yüksek sayıda eş oluşturabilir ve
belirli bir adı devralmak için her biriyle \"oy kullanabilir\".
Proof-of-work yöntemleri, kimliği özgür olmayan hale getirmek için
kullanılabilir. Ancak ağ büyüdükçe, çevrim içi oylama yapmak için
herkesle iletişim kurmayı sağlayacak yük çok fazladır ya da ağın tamamı
sorgulanmazsa, farklı yanıt kümelerine ulaşılabilir. .

Ancak İnternet üzerinde olduğu gibi, I2P bir adlandırma sisteminin
tasarımını ve çalışmasını (IP benzeri) iletişim katmanının dışında
tutar. Paketlenmiş adlandırma kitaplığında, alternatif adlandırma
sistemlerinin takılabileceği basit bir hizmet sağlayıcı arabirimi
bulunur ve son kullanıcıların yeğlediği adlandırma değiş tokuşunu
yapmalarını sağlar.

## I2PTunnel {#app.i2ptunnel}

*Developed by: *

I2PTunnel, büyük olasılıkla en beğenilen ve çok yönlü I2P istemci
uygulamasıdır. I2P ağında hem geliş hem de çıkış vekil sunucularının
kullanılmasını sağlar. I2PTunnel, dört ayrı vekil sunucu uygulaması
olarak görülebilir. Gelen TCP bağlantılarını alan ve bunları belirli bir
I2P hedefine ileten bir \"istemci\", bir HTTP vekil sunucusu gibi
davranan ve istekleri sunucuya ileten bir \"httpclient\" (aka
\"eepproxy\"), istekleri uygun I2P hedefine ileten (gerekirse adlandırma
hizmetini sorguladıktan sonra), bir hedefte gelen I2P akış
bağlantılarını alan ve bunları belirli bir TCP sunucu + bağlantı
noktasına ileten bir \"sunucu\" ve daha güvenli çalışmayı sağlamak için
HTTP isteğini ve yanıtlarını ayrıştıran genişletilmiş bir \"https
sunucusu\". Ek bir \"socksclient\" uygulaması var. Ancak daha önce
bahsedilen nedenlerle kullanılması önerilmiyor.

I2P ağı bir çıkış vekil sunucusu ağı değildir. Veriler karma bir ağdan
içeri ve dışarı aktarılırken anonimlik ve güvenlik endişeleri de
aktarılır. I2P tasarımı, kullanıcının gereksinimlerini karşılamak için
dış kaynaklara gerek duyulmayan bir anonim bir ağ sağlamaya
odaklanmıştır. Bununla birlikte I2PTunnel \"httpclient\" uygulaması,
bağlantı kurulması istenilen sunucu adı \".i2p\" ile bitmiyorsa,
kullanıcı tarafından sağlanan bir çıkış vekil sunucusu kümesinden
rastgele bir hedef seçerek ve isteği onlara ileterek çıkış vekil
sunucusu için bir bağlantı sağlar. Bu hedefler, açıkça çıkış vekil
sunucusu işletmeyi seçmiş gönüllüler tarafından yürütülen I2PTunnel
\"sunucu\" kopyalarıdır. Varsayılan olarak hiç bir kopya çıkış vekil
sunucusu değildir ve bir çıkış vekil sunucusu işletmek, başkalarına
otomatik olarak sizin vekil sunucunuzu kullanmasını söylemez. Çıkış
vekil sunucularının doğal zayıflıkları olsa da, I2P kullanımı için basit
bir kavramsal kanıt sunarlar ve bazı kullanıcılar için yeterli
olabilecek bir tehdit modeline göre bazı işlevler sağlarlar.

I2PTunnel ile genel olarak gerek duyulan çoğu şey kullanılabilir. Bir
site sunucusunu gösteren bir \"https sunucusu\", herkesin kendi anonim
sitesini (veya \"I2P sitesini\") işletebilmesini sağlar. I2P ile
birlikte bu amaçla kullanılabilecek bir site sunucusu gelir. Ancak bunun
dışındaki herhangi bir site sunucusu da kullanılabilir. İsteyen herkes,
her biri kendi yerel IRCd uygulamasını gösteren bir \"sunucu\" işleten
ve kendi \"istemci\" tünelleri üzerinden IRCd uygulamaları arasında
iletişim kuran ve anonim olarak barındırılan IRC sunucularından birini
gösteren bir \"istemci\" işletebilir. Son kullanıcılar ayrıca anonim
geliştirme yapılabilen [I2Pmail](#app.i2pmail) POP3 ve SMTP hedeflerini
gösteren \"istemci\" tünellerini (sırasıyla POP3 ve SMTP sunucularını
gösteren \"sunucu\" kopyaları) ve ayrıca I2P CVS sunucusunu gösteren
\"istemci\" tünellerini kullanabilir. Bazı durumlarda insanlar bir NNTP
sunucusunu gösteren \"sunucu\" kopyalarına erişmek için bile \"istemci\"
vekil sunucuları işletti.

## I2PSnark {#app.i2psnark}

*I2PSnark geliştirildi: jrandom ve et
al[mjw](http://www.klomp.org/mark/) kullanıcısının
[Snark](http://www.klomp.org/snark/) istemcisinden bir dal oluşturdu*

I2P kurulumuyla birlikte gelen I2PSnark, çoklu torrent özellikleri olan
basit bir anonim BitTorrent istemcisidir ve tüm işlevlerin bir düz HTML
internet arayüzü ile kullanılmasını sağlar.

## I2Pmail/susimail {#app.i2pmail}

*Developed by: *

I2Pmail is more a service than an application - postman offers both
internal and external email with POP3 and SMTP service through I2PTunnel
instances accessing a series of components developed with mastiejaner,
allowing people to use their preferred mail clients to send and receive
mail pseudonymously. However, as most mail clients expose substantial
identifying information, I2P bundles susi23\'s web based susimail client
which has been built specifically with I2P\'s anonymity needs in mind.
The I2Pmail/mail.i2p service offers transparent virus filtering as well
as denial of service prevention with hashcash augmented quotas. In
addition, each user has control of their batching strategy prior to
delivery through the mail.i2p outproxies, which are separate from the
mail.i2p SMTP and POP3 servers - both the outproxies and inproxies
communicate with the mail.i2p SMTP and POP3 servers through I2P itself,
so compromising those non-anonymous locations does not give access to
the mail accounts or activity patterns of the user.


