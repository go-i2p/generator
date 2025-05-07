 Tünel Uygulaması 2019 Temmuz 0.9.41 Bu sayfada
geçerli tünel uygulaması açıklanmaktadır.

## Tünel özeti {#tunnel.overview}

I2P içinde, iletiler bir sonraki sıçramaya iletilirken var olan her
türlü araç kullanılarak sanal bir eşler tüneli aracılığıyla bir yönde
aktarılır. İletiler tünelin *ağ geçidine* ulaşır, gruplanır ve/veya
sabit boyutlu tünel iletilerine bölünerek tüneldeki bir sonraki
sıçramaya aktarılır. Bu sıçrama iletinin geçerliliğini işleyip doğrular
ve bir sonraki sıçramaya gönderir. Bu şekilde tünel uç noktasına
ulaşılana kadar sürer. Bu *uç nokta* ağ geçidi tarafından bir araya
getirilmiş iletileri alır ve verilen yönergelere uygun olarak, başka bir
yönelticiye, başka bir yönelticideki başka bir tünele ya da yerele
aktarır.

Tünellerin tümü aynı şekilde çalışır. Ancak geliş ve gidiş tünelleri
olmak üzere iki farklı gruba ayrılabilir. Geliş tünelleri, iletileri
tünel uç noktası olarak hizmet eden tünel oluşturucuya doğru aktaran
güvenilmeyen bir ağ geçidine sahiptir. Gidiş tünellerinde, tünel
oluşturucu, iletileri uzak uç noktaya ileterek ağ geçidi görevi görür.

Tünel oluşturucu, tünele tam olarak hangi eşlerin katılacağını seçer ve
her birine gerekli yapılandırma verilerini sağlar. Herhangi bir sayıda
sıçramaya sahip olabilirler. Katılımcıların veya üçüncü tarafların bir
tünelin uzunluğunu belirlemesi veya hatta ortak katılımcıların aynı
tünelin bir parçası olup olmadıklarının belirlemesinin zorlaştırılması
amaçlanmıştır (uzlaşmış eşlerin tünelde birbirine yakın olduğu durumlar
dışında).

Uygulamada, farklı amaçlar için bir dizi tünel havuzu kullanılır. Her
yerel istemci hedefinin, kendi anonimlik ve başarım gereksinimlerini
karşılamak üzere yapılandırılmış kendi geliş ve gidiş tünelleri vardır.
Ek olarak, yönelticinin kendisi, ağ veri tabanına (netDB) katılmak ve
tünelleri yönetmek için bir dizi havuz bulundurur.

I2P doğası gereği paket anahtarlamalı bir ağdır. Böylece tünellerde bile
paralel olarak çalışan çoklu tünellerden faydalanarak esnekliği arttırır
ve yükü dengeler. Çekirdek I2P katmanının dışında, istemci uygulamaları
için isteğe bağlı bir uçtan uca streaming kitaplığı vardır ve iletileri
yeniden sıralama, yeniden iletme, tıkanıklık denetimi gibi TCP benzeri
özellikler sunar.

An overview of I2P tunnel terminology is [on the tunnel overview
page]().

## Tünelin Çalışması (İletilerin İşlenmesi) {#tunnel.operation}

### Özet

After a tunnel is built, [I2NP messages]() are
processed and passed through it. Tunnel operation has four distinct
processes, taken on by various peers in the tunnel.

1. İlk olarak, tünel ağ geçidi bir dizi I2NP iletisi biriktirir ve
 bunları aktarmak için tünel iletilerini ön işler.
2. Sonra, bu ağ geçidi ön işlenmiş verileri şifreler ve ilk sıçramaya
 iletir.
3. Bu eş ve sonraki tünel katılımcıları, şifreleme katmanını açar,
 bunun bir kopya olmadığını doğrular ve ardından bir sonraki eşe
 iletir.
4. Sonunda tünel iletileri ağ geçidi tarafından özgün şekilde
 paketlenen I2NP iletilerinin yeniden bir araya getirildiği ve
 istendiği gibi aktarıldığı uç noktaya ulaşır.

Ara tünel katılımcıları, bir geliş veya gidiş tünelinde olup
olmadıklarını bilmez. Her zaman bir sonraki sıçrama için \"şifreleme\"
yaparlar. Böylece, gidiş tüneli ağ geçidinde \"şifrenin çözülmesi\" için
simetrik AES şifrelemesinden yararlanarak uç noktada düz metnin ortaya
çıkması sağlanır.

![Inbound and outbound tunnel
schematic](images/tunnels.png "Inbound and outbound tunnel schematic")

+-----------------+-----------------+-----------------+-----------------+
| Rol | Ön işleme | Şifreleme | Art işleme |
| | | işlemi | |
+=================+=================+=================+=================+
| Gidiş ağ geçidi | Parçalama, | Döngüsel | Sonraki |
| (oluşturucu) | toplu işlem ve | şifreleme | sıçramaya |
| | dolgu | (şifre çözme | aktarma |
| | | işlemleri | |
| | | kullanılarak) | |
+-----------------+-----------------+-----------------+-----------------+
| Katılımcı |   | Şifre çözme | Sonraki |
| | | (şifreleme | sıçramaya |
| | | işlemi | aktarma |
| | | kullanılarak) | |
+-----------------+-----------------+-----------------+-----------------+
| Gidiş Uç |   | Düz metin tünel | Parçaları |
| Noktası | | iletisini | birleştirme, |
| | | bulmak için | geliş ağ geçidi |
| | | şifre çözme | ya da |
| | | (bir şifreleme | yönelticisi |
| | | işlemi | tarafından |
| | | kullanılarak) | belirtildiği |
| | | | gibi iletim |
+-----------------+-----------------+-----------------+-----------------+
| ------------- | | | |
+-----------------+-----------------+-----------------+-----------------+
| Geliş Ağ Geçidi | Parçalama, | Şifreleme | Sonraki |
| | toplu işlem ve | | sıçramaya |
| | dolgu | | aktarma |
+-----------------+-----------------+-----------------+-----------------+
| Katılımcı |   | Şifreleme | Sonraki |
| | | | sıçramaya |
| | | | aktarma |
+-----------------+-----------------+-----------------+-----------------+
| Geliş uç |   | Düz metin tünel | Parçaları |
| noktası | | iletisini | birleştirme, |
| (oluşturucu) | | bulmak için | verileri alma |
| | | döngüsel şifre | |
| | | çözme | |
+-----------------+-----------------+-----------------+-----------------+

### Ağ geçidi işlemesi {#tunnel.gateway}

#### İleti Ön İşlemesi {#tunnel.preprocessing}

A tunnel gateway\'s function is to fragment and pack [I2NP
messages]() into fixed-size [tunnel
messages]() and encrypt the tunnel
messages. Tunnel messages contain the following:

- 4 bayt uzunluğunda bir tünel kimliği
- 16 bayt uzunluğunda "Başlatma vektörü" (IV)
- Bir sağlama
- Gerekiyorsa dolgu ekleme
- Bir ya da birkaç { aktarım yönergeleri, I2NP ileti parçaları } eşi

Tünel kimlikleri, her sıçramada kullanılan 4 baytlık sayılardır.
Katılımcılar, iletileri hangi tünel kimliğiyle dinleyeceğini ve bir
sonraki sıçramayı hangi tünel kimliğine aktarmaları gerektiğini bilir ve
her sıçrama, üzerinden ileti alacağı tünel kimliğini seçer. Tünellerin
kendileri kısa ömürlüdür (10 dakika). Sonraki tüneller aynı eşler dizisi
kullanılarak oluşturulsa bile, her sıçramanın tünel kimliği değişir.

Saldırganların ileti boyutunu ayarlayarak, iletileri yol boyunca
etiketlemesini önlemek için, tüm tünel iletilerinin boyutu sabit 1024
bayttır. Daha büyük I2NP iletilerini barındırmak ve daha küçük olanları
daha verimli bir şekilde desteklemek için ağ geçidi, daha büyük I2NP
iletilerini her tünel iletisinde bulunan parçalara böler. Uç nokta, kısa
bir süre için parçalardan I2NP iletisini yeniden oluşturmaya çalışır,
ancak gerektiğinde bunları atar.

Details are in the [tunnel message
specification]().

### Ağ Geçidi Şifrelemesi

İletilerin dolgulu bir yük şeklinde ön işlenmesinden sonra, ağ geçidi
rastgele 16 baytlık bir IV değeri oluşturur. Bunu ve tünel iletisini
gerektiği gibi döngüsel olarak şifreler ve {tunnelID, IV, şifrelenmiş
tünel iletisi grubunu bir sonraki sıçramaya iletir.

Ağ geçidinde şifrelemenin nasıl yapılacağı, tünelin geliş veya gidiş
tüneli olmasına bağlıdır. Geliş tünelleri, yalnızca rastgele bir IV
seçer, ağ geçidinin IV değerini oluşturmak için onu son işleyip
günceller ve ön işlenmiş verileri şifrelemek için bu IV değerini kendi
katman anahtarının yanında kullanır. Gidiş tünelleri, tüneldeki tüm
atlamalar için IV ve katman anahtarları ile (şifrelenmemiş) IV ve
önceden işlenmiş verilerin şifresini döngüsel olarak çözmelidir. Gidiş
tüneli şifrelemesinin sonucunda, her bir eş bunu şifrelediğinde, uç
noktada ön işlenmiş ilk veriler elde edilir.

### Katılımcı İşlemesi {#tunnel.participant}

Bir eş bir tünel iletisi aldığında, iletinin önceki sıçramadan geldiğini
denetler (ilk ileti tünelden geldiğinde hazırlanır). Önceki eş farklı
bir yönelticiyse veya ileti zaten görülmüşse, ileti atılır. Katılımcı
daha sonra geçerli IV değerini belirlemek için IV anahtarını kullanarak
alınan IV verilerini AES256/ECB ile şifreler. Bu IV değerini
katılımcının katman anahtarıyla verileri şifrelemek için kullanır.
Geçerli IV değerini IV anahtarını kullanarak AES256/ECB ile şifreler,
ardından {nextTunnelId, nextIV,cryptData} demetini bir sonraki sıçramaya
aktarır. IV üzerinde yapılan bu çift şifreleme (hem kullanımdan önce hem
de kullanımdan sonra), belirli bir onay saldırısı sınıfına karşı savunma
oluşturmakta yardımcı olur. See [this
email](http://zzz.i2p/archive/2005-07/msg00031.html) and the surrounding
thread for more information.

Yinelenen ileti algılaması, ileti IV değerlerinde eskitme yapan bir
Bloom süzgeci tarafından işlenir. Her yöneltici, katıldığı tüm tüneller
için, alınan iletinin ilk bloğu ile IV değerinin XOR sonucunu üretir,
10-20 dakika sonra (tünellerin süresi dolduğunda) görülmüş kayıtları
atacak şekilde değiştirir. Bloom süzgecinin boyutu ve kullanılan
parametreler, yönelticinin ağ bağlantısını ihmal edilebilir bir hatalı
doğru olasılığıyla doyurmaktan daha fazlası için yeterlidir. Bloom
süzgecine gönderilen benzersiz değer, ilk blok ile IV değerinin XOR
sonucudur ve tüneldeki sıralı olmayan çakışan eşlerin bir iletisinin IV
ve ilk blok değiştirilmiş olarak yeniden gönderilerek etiketlenmesini
önler.

### Uç Nokta İşlemesi {#tunnel.endpoint}

Tüneldeki son sıçramada bir tünel iletisini aldıktan ve doğruladıktan
sonra, uç noktanın ağ geçidi tarafından kodlanan verileri nasıl elde
edeceği tünelin geliş ya da gidiş tüneli olmasına bağlıdır. Gidiş
tüneller için uç nokta, iletiyi diğer katılımcılar gibi katman
anahtarıyla şifreleyerek ön işlenmiş verileri açığa çıkarır. Geliş
tünellerinde, uç nokta aynı zamanda tünel oluşturucudur. Bu nedenle IV
ve iletinin şifresini her adımın katman ve IV anahtarlarını ters sırada
kullanarak yalnızca döngüsel olarak çözebilirler.

Bu noktada, tünel uç noktası, ağ geçidi tarafından gönderilen ve daha
sonra katılan I2NP iletilerine ayrıştırabilecek ve bunları aktarım
yönergelerinde istendiği gibi aktarabilecek ön işlenmiş verilere
sahiptir.

## Tünel Oluşturma {#tunnel.building}

Bir tünel oluştururken, oluşturucu, sıçramaların her birine gerekli
yapılandırma verilerini içeren bir istek göndermeli ve tüneli
etkinleştirmeden önce tümünün kabul etmesini beklemelidir. İstekler,
yalnızca bir bilgiyi (tünel katmanı veya IV anahtarı gibi) bilmesi
gereken eşlerin bu verilere sahip olması için şifrelenir. Ayrıca,
yalnızca tünel oluşturucu eşin yanıtına erişebilir. Tünelleri
oluştururken akılda tutulması gereken üç önemli boyut vardır: Hangi
eşlerin kullanıldığı (ve nerede), isteklerin nasıl gönderildiği (ve
yanıtların alındığı) ve bunların nasıl sürdürüldüğü.

### Eş Seçimi {#tunnel.peerselection}

İki tür tünelin (geliş ve gidiş) ötesinde, farklı tüneller için
kullanılan iki eş seçim türü daha vardır: Keşif ve istemci. Keşif
tünelleri hem ağ veri tabanı (netDB) bakımı hem de tünel bakımı için
kullanılırken, istemci tünelleri uçtan uca istemci iletileri için
kullanılır.

#### Keşif tüneli eş seçimi {#tunnel.selection.exploratory}

Keşif tünelleri, ağın bir alt kümesinden rastgele seçilen eşlerden
oluşur. Belirli alt küme, yerel yönelticiye ve tünel yöneltme
gereksinimlerinin ne olduğuna göre değişir. Genel olarak, keşif
tünelleri, eşin \"başarısız değil ama etkin\" profil kategorisinde
bulunan rastgele seçilmiş eşlerinden oluşturulur. Tünellerin ikincil
amacı, yalnızca tünel yöneltmenin ,ötesinde, istemci tünellerinde
kullanılmak üzere yükseltmek için yeterince kullanılmayan yüksek
kapasiteli eşler bulmaktır.

Exploratory peer selection is discussed further on the [Peer Profiling
and Selection page]().

#### İstemci tüneli eş seçimi {#tunnel.selection.client}

İstemci tünelleri daha katı gereksinim kümesiyle oluşturulur. Yerel
yöneltici, başarım ve güvenilirliğin istemci uygulamasının
gereksinimlerini karşılaması için \"hızlı ve yüksek kapasiteli\" profil
kategorisinden eşler seçer. Ancak, istemcinin anonimlik gereksinimlerine
bağlı olarak, bu temel seçimin ötesinde uyulması gereken birkaç önemli
ayrıntı vardır.

Client peer selection is discussed further on the [Peer Profiling and
Selection page]().

#### Tünellerde Eş Sıralaması {#ordering}

Peers are ordered within tunnels to deal with the [predecessor
attack]() [(2008
update)]().

Öncül saldırıyı boşa çıkarmak için, tünel seçimi eşleri katı bir
sıralamayla seçilmiş olarak tutar. Eğer A, B ve C belirli bir tünel
havuzu için bir tüneldeyse, A\'dan sonraki sıçrama her zaman B\'dir ve
B\'den sonraki sıçrama her zaman C olur.

Sıralama, başlangıçta her tünel havuzu için rastgele bir 32 baytlık
anahtar üretilerek uygulanır. Eşler sıralamayı öngörememelidir, yoksa
bir saldırgan bir tünelin her iki ucunda olma şansını en üst düzeye
çıkarmak için birbirinden çok uzak olan iki yönelticinin karmasını
kullanabilir. Eşler, rastgele anahtardan SHA256 karmasının (eşin
rastgele anahtarla birleştirilmiş karması) ile rastgele anahtarın XOR
uzaklığına göre sıralanır

 p = peer hash
 k = random key
 d = XOR(H(p+k), k)

Her tünel havuzu farklı bir rastgele anahtar kullandığından, sıralama
tek bir havuz içinde tutarlıdır. Ancak farklı havuzlar arasında tutarlı
değildir. Her yöneltici yeniden başlatıldığında yeni anahtarlar
oluşturulur.

### İstek aktarımı {#tunnel.request}

A multi-hop tunnel is built using a single build message which is
repeatedly decrypted and forwarded. In the terminology of [Hashing it
out in Public](), this is \"non-interactive\"
telescopic tunnel building.

This tunnel request preparation, delivery, and response method is
[designed]() to reduce the number of
predecessors exposed, cuts the number of messages transmitted, verifies
proper connectivity, and avoids the message counting attack of
traditional telescopic tunnel creation. (This method, which sends
messages to extend a tunnel through the already-established part of the
tunnel, is termed \"interactive\" telescopic tunnel building in the
\"Hashing it out\" paper.)

The details of tunnel request and response messages, and their
encryption, [are specified here]().

Eşler, çeşitli nedenlerle tünel oluşturma isteklerini reddedebilir.
Ancak giderek daha ciddi hale gelen bir dizi dört reddetme
bilinmektedir: Olasılıklı reddetme (yönelticinin kapasitesine yaklaşması
nedeniyle veya bir istek akışına yanıt olarak), geçici aşırı yük, bant
genişliği aşırı yüklemesi ve kritik başarısızlık. Alındığında, bu dördü,
söz konusu yönelticinin profilini ayarlamaya yardımcı olmak için tünel
oluşturucu tarafından yorumlanır.

For more information on peer profiling, see the [Peer Profiling and
Selection page]().

### Tünel Havuzları {#tunnel.pooling}

To allow efficient operation, the router maintains a series of tunnel
pools, each managing a group of tunnels used for a specific purpose with
their own configuration. When a tunnel is needed for that purpose, the
router selects one out of the appropriate pool at random. Overall, there
are two exploratory tunnel pools - one inbound and one outbound - each
using the router\'s default configuration. In addition, there is a pair
of pools for each local destination - one inbound and one outbound
tunnel pool. Those pools use the configuration specified when the local
destination connects to the router via [I2CP](),
or the router\'s defaults if not specified.

Each pool has within its configuration a few key settings, defining how
many tunnels to keep active, how many backup tunnels to maintain in case
of failure, how long the tunnels should be, whether those lengths should
be randomized, as well as any of the other settings allowed when
configuring individual tunnels. Configuration options are specified on
the [I2CP page]().

### Tünel Uzunlukları ve Varsayılanlar {#length}

[Tünel özeti
sayfasında](#length).

### Öngörülü Oluşturma Stratejisi ve Önceliği {#strategy}

Tünel oluşturma işlemi pahalıdır ve tüneller oluşturulduktan belirli bir
süre sonra sona erer. Bununla birlikte, bir havuzda tünel kalmadığında,
aslında hedef ölüdür. Ayrıca, tünel oluşturma başarı oranı hem yerel hem
de küresel ağ koşullarına göre büyük ölçüde değişebilir. Bu nedenle,
yeni tünellerin gerek duyulmadan önce, fazla tünel oluşturmadan, onları
çok erken oluşturmadan veya çok fazla işlemci veya bant genişliği
tüketmeden, şifrelenmiş tüneller oluşturup göndermeden başarıyla
oluşturulmasını ve oluşturma iletlerinin gönderilmesini sağlamak için
ileriye dönük, uyarlanabilir bir oluşturma stratejisini sürdürmek
önemlidir.

Yöneltici, her bir grup {keşif/istemci, giriş/çıkış, uzunluk, uzunluk
farkı} için başarılı bir tünel oluşturmak amacıyla gereken süre hakkında
istatistik tutar. Bu istatistikleri kullanarak, bir tünelin süresinin
dolmasına ne kadar süre kaldığında yeni bir tünel oluşturmaya çalışması
gerektiğini hesaplar. Başarılı bir değiştirme olmadan sona erme süresi
yaklaştıkça, paralel olarak birden çok derleme denemesi başlatır ve
ardından gerekirse paralel denemelerin sayısını artırır.

Bant genişliğini ve işlemci kullanımını sınırlamak için yöneltici, tüm
havuzlarda bekleyen en fazla derleme denemesi sayısını da sınırlar.
Kritik yapılara (keşif tünelleri ve tünelleri kalmamış havuzlar için
olanlar) öncelik verilir.

## Tünel İletisi Kısıtlaması {#tunnel.throttling}

I2P içindeki tüneller devre anahtarlamalı bir ağa benzese de, I2P
içindeki her şey kesinlikle ileti tabanlıdır. Tüneller yalnızca
iletilerin dağıtımını organize etmeye yardımcı olan hesaplama
hileleridir. İletilerin güvenilirliği veya sıralanması ile ilgili
herhangi bir varsayım yapılmaz ve yeniden aktarım işlemleri daha yüksek
düzeylere bırakılır (I2P istemci katmanı \"Streaming kitaplığı\" gibi).
Bu yapı, I2P ağının hem paket anahtarlamalı hem de devre anahtarlamalı
ağlar için var olan kısma tekniklerinden faydalanmasını sağlar. Örneğin,
her yöneltici, her tünelin ne kadar veri kullandığının hareketli
ortalamasını izleyebilir. Bunu yönelticinin katıldığı diğer tüneller
tarafından kullanılan tüm ortalamalarla birleştirebilir ve kapasitesi
ile kullanımına bağlı olarak ek tünel katılım isteklerini kabul veya red
edebilir. Diğer yandan, her yöneltici, normal İnternet üzerinde
kullanılan araştırmadan yararlanarak, kapasitesini aşan iletileri
kolayca atabilir.

Var olan uygulamada, yönelticiler ağırlıklı rastgele erken atma (WRED)
stratejisi uygular. Katılan tüm yönelticiler için (iç katılımcı, geliş
ağ geçidi ve gidiş uç noktası), yöneltici, bant genişliği sınırlarına
yaklaşıldığında iletilerin bir kısmını rasgele atmaya başlar. Trafik
sınırlara yaklaştıkça veya sınırları aştıkça daha fazla ileti atılır.
Bir iç katılımcı için tüm iletiler parçalanır ve dolgu eklenir. Bu
nedenle tüm iletiler aynı boyuttadır. Ancak geliş ağ geçidinde ve gidiş
uç noktasında, atma kararı tam (birleştirilmiş) ileti üzerinde verilir
ve ileti boyutu dikkate alınır. Daha büyük iletilerin atılma olasılığı
daha yüksektir. Ayrıca, bu iletiler yolculuklarında \"uzak\"
olmadığından ve dolayısıyla bu iletileri bırakmanın ağ maliyeti daha
düşük olduğundan, iletilerin geliş ağ geçidine göre gidiş uç noktasında
atılması daha olasıdır.

## Gelecekte Yapılacak Çalışmalar {#future}

### Karıştırma/toplu işlem {#tunnel.mixing}

İletileri geciktirmek, yeniden sıralamak, yeniden yöneltmek veya dolgu
eklemek için ağ geçidinde ve her sıçramada hangi stratejiler
kullanılabilir? Bu ne ölçüde otomatik olarak yapılmalı, ne kadarı tünel
başına veya sıçrama başına ayar olarak yapılandırılmalı ve tünel
oluşturucu (dolayısıyla kullanıcı) bu işlemi nasıl denetlemelidir? Tüm
bunlar, uzak bir gelecekteki sürümde üzerinde çalışılacak bilinmeyenler
olarak bırakıldı.

### Dolgu Ekleme

Dolgu ekleme stratejileri, ileti boyutu bilgilerinin farklı saldırganlar
tarafından görülmesini ele alarak çeşitli düzeylerde kullanılabilir.
Geçerli sabit tünel iletisinin boyutu 1024 bayttır. Bununla birlikte,
bunun içinde, parçalanmış iletilerin kendilerine tünel tarafından
herhangi bir dolgu eklenmez. Ancak uçtan uca iletiler için Garlic
sarmalamasının bir parçası olarak dolgu eklenebilir.

### WRED

WRED stratejilerinin, uçtan uca başarım ve ağ tıkanıklığı çöküşünün
önlenmesi üzerinde önemli bir etkisi vardır. Geçerli WRED stratejisi
dikkatle değerlendirilmeli ve geliştirilmelidir.


