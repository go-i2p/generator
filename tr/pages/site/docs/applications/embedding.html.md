 Uygulamanıza I2P
Gömmek 2023-01 2.1.0 

## Özet

Bu sayfa, tüm I2P yöneltici binary dosyasını uygulamanızla birlikte
paketlemekle ilgilidir. Bu konu, I2P ile çalışmak için bir uygulama
yazmakla ilgili değildir (paketlenmiş ya da dış). However, many of the
guidelines may be useful even if not bundling a router.

Pek çok proje paketleniyor ya da I2P paketlemesi hakkında konuşuluyor.
Doğru yapılırsa harika. Yanlış yapılırsa, ağımıza gerçekten zarar
verebilir. I2P yönelticisi karmaşıktır ve tüm bu karmaşıklığı
kullanıcılarınızdan uzak tutmak zor olabiliyor. Bu sayfada bazı genel
yönergeler anlatılmaktadır.

Most of these guidelines apply equally to Java I2P or i2pd. However,
some guidelines are specific to Java I2P and are noted below.

### Bizimle görüşün

Bir görüşme başlatın. Yardım etmek için buradayız. I2P kullanan
uygulamalar, ağı büyütmek ve herkes için anonimliği sağlamak bizim için
umut ve heyecan verici fırsatlardır.

### Yönelticinizi akıllıca seçin

Uygulamanız Java veya Scala üzerindeyse, bu seçim kolaydır - Java
yönelticisini kullanın. C/C++ kullanıyorsanız, i2pd kullanmanızı
öneririz. i2pcpp geliştirme çalışmaları durdu. Diğer dillerdeki
uygulamalar için en iyisi SAM ya da BOB ya da SOCKS kullanmak ve Java
yönelticisini ayrı bir işlem olarak paketlemektir. Aşağıdakilerden
bazıları yalnızca Java yönelticisi için geçerlidir.

### Lisanslama

Paketlediğiniz yazılımın lisans gereksinimlerini karşıladığınızdan emin
olun.

## Configuration

### Varsayılan yapılandırmayı doğrulayın

Doğru bir varsayılan yapılandırma çok önemlidir. Çoğu kullanıcı
varsayılanları değiştirmez. Uygulamanızın varsayılanlarının,
paketlediğiniz yönelticinin varsayılanlarından farklı olması
gerekebilir. Gerekirse yöneltici varsayılanlarını değiştirin.

İncelenecek bazı önemli varsayılanlar: En fazla bant genişliği, tünel
miktarı ve uzunluğu, en fazla katkıda bulunulan tünel. Bunların çoğu,
uygulamanızın beklenen bant genişliğine ve kullanım kalıplarına
bağlıdır.

Kullanıcılarınızın ağa katkıda bulunmasını sağlamak için yeterli bant
genişliği ve tünel yapılandırın. Büyük olasılıkla gerek
duymayacağınızdan ve çalışan diğer tüm I2P kopyaları ile çakışacağından,
dış I2CP kullanımını devre dışı bırakmayı değerlendirin. Ayrıca örneğin
çıkarken JVM sonlandırılmasını engellemek için de yapılandırmalara
bakın.

### Trafiğe Katkıda Bulunma Değerlendirmeleri

Katkıda bulunulan trafiği devre dışı bırakmak sizin için cazip
gelebilir. Bunu yapmanın birkaç yolu vardır (gizli kip, en fazla tünel
sayısını 0 yapmak, paylaşılan bant genişliğini 12 KBytes/sn değerinin
altına ayarlamak). Katkıda bulunulan trafik olmadan, normal kapatma
konusunda endişelenmeniz gerekmez, kullanıcılarınız kendileri tarafından
üretilmeyen bant genişliği kullanımını görmez, vb. Ancak, katkı
tünellerine izin vermeniz için birçok neden var.

Her şeyden önce, ağ ile \"bütünleşme\" şansı yoksa yöneltici o kadar iyi
çalışmaz, Buna, sizin aracılığınızla tüneller oluşturan başkaları
tarafından muazzam bir şekilde yardımcı olur.

İkincisi, geçerli ağdaki yönelticiler yüzde 90% oranında katkıda
bulunulan trafiğe izin verir. Java yönelticisinde varsayılandır.
Başvurunuz başkaları için yönlendirilme yapmıyorsa ve gerçekten sık
kullanılmaya başlıyorsa, o zaman ağda bir sülüğe dönüşür ve şu anda
sahip olduğumuz dengeyi bozar. Gerçekten büyürse, Tor haline geliriz ve
zamanımızı insanlara aktarmayı etkinleştirmeleri için yalvararak
geçiririz.

Üçüncüsü, katkıda bulunulan trafik, kullanıcılarınızın anonimliğine
yardımcı olan örtü trafiğidir.

Katkıda bulunulan trafiği varsayılan olarak devre dışı bırakmanızı
kesinlikle önermiyoruz. Bunu yaparsanız ve uygulamanız çok kullanılmaya
başlanırsa, ağı bozabilir.

### Kalıcılık

You must save the router\'s data (netdb, configuration, etc.) between
runs of the router. I2P does not work well if you must reseed each
startup, and that\'s a huge load on our reseed servers, and not very
good for anonymity either. Even if you bundle router infos, I2P needs
saved profile data for best performance. Without persistence, your users
will have a poor startup experience.

There are two possibilities if you cannot provide persistence. Either of
these eliminates your project\'s load on our reseed servers and will
significantly improve startup time.

1\) Set up your own project reseed server(s) that serve much more than
the usual number of router infos in the reseed, say, several hundred.
Configure the router to use only your servers.

2\) Bundle one to two thousand router infos in your installer.

Also, delay or stagger your tunnel startup, to give the router a chance
to integrate before building a lot of tunnels.

### Yapılandırılabilirlik

Kullanıcılarınıza önemli ayarların yapılandırmasını değiştirmeleri
olanağı sağlayın. I2P karmaşıklığının çoğunu gizlemek isteyebileceğinizi
anlıyoruz, ancak bazı temel ayarları görüntülemek önemlidir. Yukarıdaki
varsayılanlara ek olarak, UPnP, IP/port gibi bazı ağ ayarları yardımcı
olabilir.

### Otomatik Doldurma Değerlendirmeleri

Belirli bir bant genişliği ayarının üzerinde ve diğer sağlık ölçütlerini
karşılayan yönelticiniz, bağlantılarda ve bellek kullanımında (en
azından Java yöneltici ile) büyük bir artışa neden olabilecek otomatik
doldurma yapar. Bunun uygun olup olmadığını değerlendirin. Otomatik
doldurmayı devre dışı bırakabilirsiniz, ancak bu durumda en hızlı
kullanıcılarınız yapabilecekleri katkıda bulunmazlar. Ayrıca,
uygulamanızın tipik çalışma süresi de etkilidir.

### Yeniden Tohumlama

Yöneltici bilgilerini paketlemeyi ya da yeniden tohumlanmış
sunucularımızı kullanmayı seçin. Java yeniden tohumlama sunucu listesi
kaynak kodundadır. Yani kaynağınızı güncel tutarsanız sunucu listesi de
güncel olur. Karşıt hükümetlerin yapabileceği engellemeleri de hesaba
katın.

### Use Shared Clients

Java I2P i2ptunnel supports shared clients, where clients may be
configured to use a single pool. If you require multiple clients, and if
consistent with your security goals, configure the clients to be shared.

### Limit Tunnel Quantity

Specify tunnel quantity explicitly with the options `inbound.quantity`
and `outbound.quantity`. The default in Java I2P is 2; the default in
i2pd is higher. Specify in the SESSION CREATE line using SAM to get
consistent settings with both routers. Two each in/out is sufficient for
most low-to-medium bandwidth and low-to-medium fanout applications.
Servers and high-fanout P2P applications may need more. See [this forum
post](http://zzz.i2p/topics/1584) for guidance on calculating
requirements for high-traffic servers and applications.

### Specify SAM SIGNATURE_TYPE

SAM defaults to DSA_SHA1 for destinations, which is not what you want.
Ed25519 (type 7) is the correct selection. Add SIGNATURE_TYPE=7 to the
DEST GENERATE command, or to the SESSION CREATE command for
DESTINATION=TRANSIENT.

### Limit SAM Sessions

Most applications will only need one SAM session. SAM provides the
ability to quickly overwhelm the local router, or even the broader
network, if a large number of sessions are created. If multiple
sub-services can use a single session, set them up with a PRIMARY
session and SUBSESSIONS (not currently supported on i2pd). A reasonable
limit to sessions is 3 or 4 total, or maybe up to 10 for rare
situations. If you do have multiple sessions, be sure to specify a low
tunnel quantity for each, see above.

In almost no situation should you require a unique session
per-connection. Without careful design, this could quickly DDoS the
network. Carefully consider if your security goals require unique
sessions. Please consult with the Java I2P or i2pd developers before
implementing per-connection sessions.

### Ağ Kaynağı Kullanımını Azaltmak

Note that these options are not currently supported on i2pd. These
options are supported via I2CP and SAM (except delay-open, which is via
i2ptunnel only). See the I2CP documentation (and, for delay-open, the
i2ptunnel configuration documentation) for details.

Uygulama tünellerinizi gecikmeli açmayı, boştayken azaltmayı ve/veya
kapatmayı değerlendirin. i2ptunnel kullanıyorsanız bunu kolayca
yapabilirsiniz. Ancak doğrudan I2CP kullanıyorsanız, bir kısmını siz
eklemelisiniz. Bazı arka plan \"Dağıtılmış karma tablosu\" (DHT)
etkinliklerinin varlığında bile tünel sayısını azaltan ve ardından
tüneli kapatan kod örneği için i2psnark uygulamasına bakabilirsiniz.

## Life Cycle

### Güncellenebilirlik

Yapabiliyorsanız otomatik güncelleme özelliği ekleyin ya da en azından
yeni sürümleri otomatik olarak bildirin. En büyük korkumuz, çok sayıda
yönelticinin güncellenmeden kalmasıdır. Java yöneltici yılda yaklaşık
6-8 sürüm yayınlar ve bu güncellemeler kullanıcıların izlediği ağın
sağlığı için çok önemlidir. Genellikle bir sürümün yayınlandıktan 6
hafta sonra ağda 80% oranında kullanıldığını görüyoruz ve bu şekilde
kalmasını istiyoruz. Yöneltici içindeki otomatik güncelleme işlevini
devre dışı bırakma konusunda endişelenmenize gerek yok. Bu kod yöneltici
panosunda bulunuyor ve muhtemelen paketinize katmıyorsunuz.

### Dağıtım

Kademeli bir kullanıma sunma planınız olsun. Ağı bir anda boğmayın. Şu
anda günde yaklaşık 25 bin tekil kullanıcımız ve ayda 40 bin tekil
kullanıcımız oluyor. Büyük olasılıkla yılda 2-3 kat büyümeyi çok fazla
sorun yaşamadan halledebiliriz. Bundan daha hızlı bir artış
öngörüyorsanız YA DA kullanıcı tabanınızın bant genişliği dağılımı (ya
da çalışma süresi dağılımı ya da herhangi bir önemli özelliği) var olan
kullanıcı tabanımızdan önemli ölçüde farklıysa, gerçekten bunu
görüşmemiz gerekir. Büyüme planlarınız ne kadar büyükse, bu kontrol
listesindeki her şey o kadar önem kazanır.

### Uzun Süreki Çalışma İçin Tasarlayın ve Destekleyin

Kullanıcılarınıza, I2P uygulamasının çalıştıkça iyileştiğini söyleyin.
İyi çalışması için başlatmadan sonra birkaç dakika beklemek gerekir. Bu
süre ilk kurulumdan sonra daha da fazla olabilir. Ortalama çalışma
süreniz bir saatten azsa, I2P çözümü büyük olasılıkla size uygun
değildir.

## User Interface

### Durumu Görüntüleyin

Kullanıcılara uygulama tünellerinin hazır olduğu hakkında bazı
göstergeler sağlayın. Sabırlı olmalarını hatırlatın.

### Uygun Şekilde Kapatın

Yapabiliyorsanız, katılımcı tünellerinizin süresi dolana kadar kapatmayı
erteleyin. Kullanıcılarınızın tünelleri kolayca kapatmasına izin
vermeyin ya da en azından onaylamalarını isteyin.

### Eğitim ve Bağış

Kullanıcılarınıza I2P hakkında daha fazla bilgi edinmek ve bağış yapmak
için bağlantılar sunarsanız iyi olur.

### Dış Yöneltici Seçeneği

Kullanıcı tabanınıza ve uygulamanıza bağlı olarak, bir dış yöneltici
kullanma seçeneği ya da ayrı bir paket seçeneği sunmak yararlı olabilir.

## Other Topics

### Diğer Ortak Hizmetlerin Kullanımı

Diğer yaygın I2P hizmetlerini (haber akışları, hosts.txt abonelikleri,
izleyiciler, dış vekil sunucular gibi) kullanmayı ya da bunlara bağlantı
vermeyi planlıyorsanız, bu hizmetleri aşırı yüklemediğinizden emin olun.
Sorun çıkmayacağından emin olmak için bu hizmetleri işleten kişilerle
görüşün.

### Zaman / NTP Sorunları

Note: This section refers to Java I2P. i2pd does not include an SNTP
client.

I2P içinde bir SNTP istemcisi bulunur. I2P uygulamasının çalışması için
doğru zaman gerekir. Hatalı bir sistem saatini dengeler ancak bu,
başlatmayı geciktirebilir. I2P uygulamasının SNTP sorgularını devre dışı
bırakabilirsiniz. Ancak uygulamanız sistem saatinin doğru olduğundan
emin olmadıkça bu önerilmez.

### Neyi Nasıl Paketleyeceğinizi Seçin

Note: This section refers to Java I2P only.

En azından i2p.jar, router.jar, stream.jar ve mstreaming.jar dosyalarına
gerek duyacaksınız. Yalnızca veri şeması uygulaması için iki akış jar
dosyasını atlayabilirsiniz. Bazı uygulamalar daha fazlasına gerek
duyabilir, i2ptunnel.jar veya addressbook.jar gibi. Şifrelemeyi çok daha
hızlandırmak için jbigi.jar veya desteklediğiniz platformlar için bir
alt kümesini unutmayın. Oluşturmak için Java 7 veya üstü gereklidir.
Debian / Ubuntu paketleri oluşturuyorsanız, I2P paketini derlemek yerine
PPA üzerinden isteyin. Örneğin susimail, susidns, yöneltici panosu ve
i2psnark uygulamalarına neredeyse hiç gerek duymazsınız.

Aşağıdaki dosyalar \"i2p.dir.base\" özelliği ile belirtilen I2P kurulum
klasörüne eklenmelidir. Yeniden tohumlama için gerekli olan
sertifikaları / klasörü ve IP doğrulaması için blocklist.txt dosyasını
unutmayın. Geoip klasörü isteğe bağlıdır, ancak yönelticinin konuma göre
kararlar alabilmesi için önerilir. Geoip bulunuyorsa,
GeoLite2-Country.mmdb dosyasını bu klasöre eklediğinizden emin olun
(installer/resources/GeoLite2-Country.mmdb.gz dosyasından ayıklayın).
hosts.txt dosyası gerekli olabilir. Uygulamanızın kullandığı tüm
sunucuları içerecek şekilde değiştirebilirsiniz. Başlangıç
varsayılanlarını değiştirmek için temel klasöre bir router.config
dosyası ekleyebilirsiniz. Client.config ve i2ptunnel.config dosyalarını
gözden geçirin ve düzenleyin ya da kaldırın.

Lisans gereksinimleri, LICENSES.txt dosyasını ve licenses klasörünü
eklemenizi gerektirebilir.

- Ayrıca bir hosts.txt dosyasını eklemek isteyebilirsiniz.
- Be sure to specify a bootclasspath if you are compiling Java I2P for
 your release, rather than taking our binaries.

### Android değerlendirmeleri

Note: This section refers to Java I2P only.

Android yöneltici uygulamamız birden fazla istemci tarafından
paylaşılabilir. Kurulu değilse, kullanıcı bir istemci uygulamasını
başlattığında kullanıcıya sorulur.

Bazı geliştiriciler, bunun kötü bir kullanıcı deneyimi olduğu
konusundaki endişelerini dile getirdiler ve yönelticiyi uygulamalarına
yerleştirmek istiyorlar. Yol haritamızda, yerleştirmeyi
kolaylaştırabilecek bir Android yöneltici hizmet kitaplığımız var. Daha
fazla bilgi gerekli.

Yardıma gerek duyarsanız lütfen bizimle görüşün.

### Maven jar dosyaları

Note: This section refers to Java I2P only.

[Maven
Central](http://search.maven.org/#search%7Cga%7C1%7Cg%3A%22net.i2p%22)
üzerinde sınırlı sayıda jar dosyamız var. Maven Central üzerinde
yayınlanan jar dosyalarını iyileştirmek ve genişletmek için ele almamız
gereken çok sayıda sorun bildirimi kaydı var.

Yardıma gerek duyarsanız lütfen bizimle görüşün.

### Veri şeması (\"Dağıtılmış karma tablosu\", DHT) değerlendirmeleri

Uygulamanız bir \"Dağıtılmış karma tablosu\" (DHT) için olduğu gibi I2P
veri şemaları kullanıyorsa, ek yükü azaltmak ve güvenilirliği artırmak
için birçok gelişmiş seçenek vardır. Bunun, iyi çalışmaya başlaması için
biraz zaman ve deneme gerekebilir. Boyut / güvenilirlik denkliklerinin
farkında olun. Yardım almak için bizimle görüşün. Aynı hedefte veri
şemaları ve akış kullanılabilir ve yapılması önerilir. Bunun için ayrı
hedefler oluşturmayın. İlgisiz verilerinizi var olan ağ \"Dağıtılmış
karma tablosu\" (DHT) ögelerinde (iMule, bote, bittorrent ve yöneltici)
depolamayın. Kendi ögenizi oluşturun. Çekirdek düğümleri sabit
kodluyorsanız, birkaç tane olmasını öneririz.

### Outproxies

I2P outproxies to the clearnet are a limited resource. Use outproxies
only for normal user-initiated web browsing or other limited traffic.
For any other usage, consult with and get approval from the outproxy
operator.

### Pazarlama desteği

Birlikte çalışalım. Projenizi tamamlayana kadar beklemeyin. Bize Twitter
kullanıcı adınızı verin ve projenizle ilgili tweet atmaya başlayın,
iyiliğin karşılığını vereceğiz.

### Zararlı yazılım

Lütfen I2P ağını kötü niyetler için kullanmayın. Hem ağımıza hem de
itibarımıza büyük zarar verebilir.

### Bize Katılın

Bu açık olabilir, ancak topluluğa katılın. I2P uygulamasını 7/24
çalıştırın. Projeniz için bir I2P aitesi açın. IRC #i2p-dev kanalında
takılın. Forumlara yazın. Duyulmasına yardımcı olun. Kullanıcılar, test
edenler, çevirmenler ve hatta kodlayıcılar edinmenize yardımcı
olabiliriz.

## Examples

### Uygulama Örnekleri

Yönelticiyi paketleyen bir uygulama örneği için I2P Android uygulamasını
kurup kurcalamak ve koduna bakmak isteyebilirsiniz. Kullanıcıya neyi
gösterdiğimizi ve neyi gizlediğimizi görün. Yönelticiyi başlatmak ve
durdurmak için kullandığımız durum makinesine bakın. Bazı örnekler:
Vuze, Nightweb Android uygulaması, iMule, TAILS, iCloak ve Monero.

### Kod Örneği

Note: This section refers to Java I2P only.

Yukarıdakilerin hiçbiri size Java yönelticiyi paketlemek için kodunuzu
nasıl yazacağınızı söylemez. Bu nedenle aşağıda kısa bir örnek
verilmiştir.

 import java.util.Properties;
 import net.i2p.router.Router;

 Properties p = new Properties();
 // add your configuration settings, directories, etc.
 // where to find the I2P installation files
 p.addProperty("i2p.dir.base", baseDir);
 // where to find the I2P data files
 p.addProperty("i2p.dir.config", configDir);
 // bandwidth limits in K bytes per second
 p.addProperty("i2np.inboundKBytesPerSecond", "50");
 p.addProperty("i2np.outboundKBytesPerSecond", "50");
 p.addProperty("router.sharePercentage", "80");
 p.addProperty("foo", "bar");
 Router r = new Router(p);
 // don't call exit() when the router stops
 r.setKillVMOnEnd(false);
 r.runRouter();

 ...

 r.shutdownGracefully();
 // will shutdown in 11 minutes or less

Bu kod, Android uygulamamızda olduğu gibi uygulamanızın yönelticiyi
başlattığı durum içindir. Yönelticinin, Java paketlerimizde olduğu gibi,
Jetty internet uygulamaları ile birlikte client.config ve
i2ptunnel.config dosyaları aracılığıyla uygulamayı başlatmasını da
sağlayabilirsiniz. Her zaman olduğu gibi, durum yönetimi zor olan
kısımdır.

See also: [the Router
javadocs](http:///net/i2p/router/Router.html).


