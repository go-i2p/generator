 I2P Tehdit
Modeli 2010 Kasım 0.8.1 low medium high
ERR_INVALID 
 
 

- **Damage Potential**: **
- **Reliability**: **
- **Exploitability**: **
- **Affected Users**: **
- **Discoverability**: **
- **Severity**: */5*
- **Priority**: */9*

 

### Saldırı Dizini

- [Kaba kuvvet saldırıları](#bruteforce)
- [Zamanlama saldırıları](#timing)
- [Ara kesit saldırıları](#intersection)
- [Hizmet reddi saldırıları](#dos)
- [Etiketleme saldırıları](#tagging)
- [Bölümleme saldırıları](#partitioning)
- [Önceleme saldırıları](#predecessor)
- [Hasat saldırıları](#harvesting)
- [Trafik İncelemesi ile Kimlik Belirleme](#traffic)
- [Sybil saldırıları](#sybil)
- [Arkadaş tüketme saldırıları](#buddy)
- [Şifreleme saldırıları](#crypto)
- [Otomatik doldurma saldırıları](#floodfill)
- [Diğer ağ veri tabanı saldırıları](#netdb)
- [Merkezileştirilmiş kaynak saldırıları](#central)
- [Geliştirme saldırıları](#dev)
- [Uygulama saldırıları](#impl)
- [Diğer Savunmalar](#blocklist)

 

## \"Anonim\" ile ne demek istiyoruz?

Anonimlik düzeyiniz, \"birinin bilmesini istemediğiniz bilgileri
öğrenmesi ne kadar zor\" olduğu şeklinde tanımlanabilir. Kim olduğunuz,
nerede bulunduğunuz, kiminle iletişim kurduğunuz ve ne zaman iletişim
kurduğunuz gibi. \"Mükemmel\" anonimlik burada kullanışlı bir kavram
değildir. Yazılımlar sizi bilgisayar kullanmayan veya İnternet üzerinde
olmayan insanlara dönüştürmez. Bunun yerine, yalnızca sitelere göz
atanlardan, veri alışverişinde bulunanlara, güçlü kuruluşlar veya
devletler tarafından keşfedilmekten korkanlara kadar, olabilecek
herkesin gerçek gereksinimlerini karşılamak için yeterli anonimlik
sağlamaya çalışıyoruz.

I2P tarafından özel gereksinimleriniz için yeterli anonimliğin sağlanıp
sağlanamadığı sorusu zor bir sorudur. Ancak bu sayfa, gereksinimlerinizi
karşılayıp karşılamadığına karar verebilmeniz için I2P uygulamasının
çeşitli saldırılar altında nasıl çalıştığını keşfederek bu soruyu
yanıtlanmanıza yardımcı olacaktır.

I2P ağının aşağıda açıklanan tehditlere karşı direnci hakkında daha
fazla araştırma ve inceleme yapılmasını memnuniyetle karşılarız. Var
olan literatürün daha fazla gözden geçirilmesine (çoğu Tor ağına
odaklanmıştır) ve I2P ağına odaklanan özgün çalışmalara gerek var.

## Ağ Topolojisi Özeti

I2P builds off the ideas of many [other]()
[systems](), but a few key points should be kept
in mind when reviewing related literature:

- **I2P özgür bir yöneltme karma ağıdır.** İletiyi oluşturan kişi,
 iletilerin gönderileceği yolu (gidiş tüneli) açık olarak tanımlar ve
 ileti alıcısı, iletilerin alınacağı yolu (geliş tüneli) açık olarak
 tanımlar.
- **I2P ağında resmi giriş ve çıkış noktaları yoktur.** Tüm eşler
 karışıma tam olarak katılır ve ağ katmanında giriş ya da çıkış vekil
 sunucuları yoktur (ancak uygulama katmanında birkaç vekil sunucu
 bulunur)
- **I2P tamamen dağıtılmıştır.** Merkezi denetim veya bir otorite
 yoktur. Bazı yönelticiler, ağın geri kalanıyla uyumluluğu bozmadan,
 karma basamakları (tünelleri oluşturmak ve tünel uç noktasında
 iletmeyi denetlemek için gerekli anahtarları vermek) veya dizin
 tabanlı profil oluşturmak ve seçmek için değiştirilebilir. Ancak
 elbette bunu yapmak şart değildir (ve hatta kişinin anonimliğine
 zarar verebilir).

We have documented plans to implement [nontrivial
delays](#stop) and [batching
strategies](#batching) whose existence is only
known to the particular hop or tunnel gateway that receives the message,
allowing a mostly low latency mixnet to provide cover traffic for higher
latency communication (e.g. email). However we are aware that
significant delays are required to provide meaningful protection, and
that implementation of such delays will be a significant challenge. It
is not clear at this time whether we will actually implement these delay
features.

Teoride, ileti yolu boyunca yönelticiler, iletiyi bir sonraki eşe
iletmeden önce, var olan uygulama bunu yapmasa da, rastgele sayıda
sıçrama eklenebilir.

## Tehdit Modeli

I2P tasarımı, 2003 yılında, şunların ortaya çıkmasından kısa bir süre
sonra başladı. [\[Onion Routing\]](http://www.onion-router.net),
[\[Freenet\]](http://freenetproject.org/) ve
[\[Tor\]](https://www.torproject.org/). Tasarımımız, o dönemde
yayınlanan araştırmalardan önemli ölçüde yararlanıyor. I2P, birkaç onion
yöneltme tekniği kullanır. Bu nedenle Tor ağına yönelmiş olan önemli
akademik ilgiden yararlanmayı sürdürüyoruz.

[Anonimlik literatüründe](http://freehaven.net/anonbib/topic.html)
(büyük ölçüde [Trafik Analizi: İletişim kuralları, saldırılar, tasarım
sorunları ve açık sorunlar](http://citeseer.ist.psu.edu/454354.html))
ortaya konulan saldırılardan ve analizlerden yola çıkarak, tanımlanmış
çeşitli saldırılar ve I2P savunmaları aşağıda kısaca açıklanmıştır. Yeni
saldırılar tanımlandıkça bu listeyi güncelliyoruz.

I2P ağına özgü olabilecek bazı saldırılar da vardır. Bu saldırıların
tümüne bir yanıtımız yok. Ancak araştırmayı ve savunmamızı geliştirmeyi
sürdürüyoruz.

Ayrıca, var olan ağın mütevazı boyutu nedeniyle bu saldırıların çoğu
olması gerekenden çok daha kolay yapılabiliyor. Ele alınması gereken
bazı sınırlamaların farkında olsak da, I2P yüz binlerce veya milyonlarca
katılımcıyı desteklemek için tasarlanmıştır. İnsanları bilgilendirmeyi
ve ağı büyütmeyi sürdürdükçe, bu saldırıları yapmak çok daha zor hale
gelecek.

The [network comparisons]() and [\"garlic\"
terminology]() pages may also be helpful
to review.

{# Hide DREAD ratings until we know how we want to use them

Attacks are judged using the [modified **DREAD**
model]():

- **Damage Potential**: If a threat exploit occurs, how much damage
 will be caused?
- **Reliability**: How reliable is the attack?
- **Exploitability**: What is needed to exploit this threat?
- **Affected Users**: How many users will be affected?
- **Discoverability**: How easy is it to discover this threat?

Each category is given a rating of low, medium or high. The severity and
priority scores are calculated using the equations outlined
[here]().

#}

### Kaba kuvvet saldırıları {#bruteforce}

{# DREAD_score(2, 1, 1, 1, 3) #}

Tüm düğümler arasında aktarılan tüm iletileri izleyerek ve hangi
iletinin hangi yolu izlediğini ilişkilendirmeye çalışarak, küresel bir
pasif veya aktif saldırgan tarafından bir kaba kuvvet saldırısı
yapılabilir. Ağdaki tüm eşler sık sık ileti gönderdiğinden (hem uçtan
uca hem de ağ bakım iletileri), ayrıca bir uçtan uca iletinin yolu
boyunca boyutu ve verileri değiştiğinden, bu saldırıyı I2P ağına
yüklemek önemsiz olmalıdır. Ek olarak, yönelticiler arası iletişim hem
şifrelemiş hem de akışkan olduğundan (iki tane 1024 baytlık ileti bir
tane 2048 baytlık iletiden ayırt edilemez kılındığından), dış
saldırganın iletilere de erişimi yoktur.

Bununla birlikte, güçlü bir saldırgan eğilimleri belirlemek için kaba
kuvvet kullanabilir. Bir I2P hedefine 5 GB veri gönderebilir ve herkesin
ağ bağlantısını izleyebilirse, 5 GB veri almayan tüm eşleri ortadan
kaldırabilir. Bu saldırıyı yenmek için teknikler vardır ancak maliyeti
aşırı derecede yüksek olabilir
([Tarzan](http://citeseer.ist.psu.edu/freedman02tarzan.html) taklitleri
veya sabit oranlı trafik gibi). Çoğu kullanıcı bu saldırıyla ilgilenmez,
çünkü onu yapmanın maliyeti aşırı yüksektir (ve genellikle yasa dışı bir
faaliyet gerektirir). Ancak, örneğin büyük bir internet hizmeti
sağlayıcısındaki veya bir internet alıp verme noktasındaki bir gözlemci
hala bu saldırıyı yapabilir. Buna karşı savunma yapmak isteyenler, düşük
bant genişliği sınırları belirlemek ve I2P siteleri için yayınlanmamış
veya \"Şifrelenmiş kiralama kümeleri\" (EncryptedLeaseSets) kullanmak
gibi uygun karşı önlemleri almak isteyeceklerdir. Önemsiz gecikmeler ve
kısıtlanmış rotalar gibi diğer karşı önlemler şu anda uygulanmamaktadır.

As a partial defense against a single router or group of routers trying
to route all the network\'s traffic, routers contain limits as to how
many tunnels can be routed through a single peer. As the network grows,
these limits are subject to further adjustment. Other mechanisms for
peer rating, selection and avoidance are discussed on the [peer
selection page]().

### Zamanlama saldırıları {#timing}

{# DREAD_score(2, 2, 2, 3, 2) #}

I2P iletileri tek yönlüdür ve mutlaka bir yanıt gönderileceği anlamına
gelmez. Bununla birlikte, I2P ağı üzerindeki uygulamaların büyük
olasılıkla iletilerinin sıklığına bakılarak tanınabilir kalıpları
olacaktır. Örneğin, bir HTTP isteği, HTTP yanıtını içeren büyük bir
yanıt iletisi dizisine sahip küçük bir ileti olacaktır. Bir saldırgan,
bu verileri ve ağ topolojisinin geniş bir görünümünü kullanarak, iletiyi
aktarmak için çok yavaş olan bazı bağlantıları diskalifiye edebilir.

Bu tür bir saldırı güçlüdür. Ancak I2P üzerinde uygulanabilirliği net
değildir. Sıraya alma, ileti işleme ve kısıtlama nedeniyle ileti
gecikmelerindeki çeşitlilik genellikle bir iletinin tek bir bağlantı
üzerinden geçirilme süresini karşılar veya aşar Hatta saldırgan, ileti
alınır alınmaz bir yanıt gönderileceğini bilir. Yine de otomatik
yanıtları ortaya çıkaracak bazı senaryolar vardır. Streaming kitaplığı
(SYN+ACK ile), garantili teslimat ileti kipini (\"Veri iletisi\" +
\"Aktarım durumu iletisi\" DataMessage+DeliveryStatusMessage ile)
sağlar.

Without protocol scrubbing or higher latency, global active adversaries
can gain substantial information. As such, people concerned with these
attacks could increase the latency (using [nontrivial
delays](#stop) or [batching
strategies](#batching)), include protocol
scrubbing, or other advanced tunnel routing
[techniques](#batching), but these are
unimplemented in I2P.

References: [Low-Resource Routing Attacks Against Anonymous
Systems]()

### Ara kesit saldırıları {#intersection}

{# DREAD_score(3, 2, 2, 3, 3) #}

Düşük gecikmeli sistemlere yönelik kesişme saldırıları son derece
güçlüdür. Hedefle periyodik olarak iletişim kurulur ve ağda hangi
eşlerin olduğu izlenir. Zamanla, düğüm kayması gerçekleştikçe,
saldırgan, bir ileti başarıyla geçtiğinde çevrim içi olan eş kümelerini
basitçe keserek hedef hakkında önemli bilgiler elde eder. Ağ büyüdükçe
bu saldırının maliyeti önemli olmaya başlar. Ancak bazı senaryolarda
gene de yapılabilir.

In summary, if an attacker is at both ends of your tunnel at the same
time, he may be successful. I2P does not have a full defense to this for
low latency communication. This is an inherent weakness of low-latency
onion routing. Tor provides a [similar
disclaimer]().

I2P üzerinde uygulanan kısmi savunmalar:

- [strict ordering](#ordering) of peers
- [peer profiling and selection]() from
 a small group that changes slowly
- Tek bir eş üzerinden yöneltilen tünel sayısının sınırlandırılması
- Aynı /16 IP aralığındaki eşlerin tek bir tünelin üyesi olmasının
 önlenmesi
- I2P siteleri veya diğer barındırılan hizmetler için, birden çok
 yönelticide eşzamanlı barındırmayı veya [birden çok
 barındırmayı](#intersection) destekliyoruz.

Toplamda bile, bu savunmalar tam bir çözüm değildir. Ayrıca, güvenlik
açığımızı önemli ölçüde artırabilecek bazı tasarım seçimleri yaptık:

- Düşük bant genişliği olan \"koruyucu düğümler\" kullanmıyoruz
- Birkaç tünelden oluşan tünel havuzları kullanıyoruz ve trafik
 tünelden tünele kayabiliyor.
- Tüneller uzun ömürlü değildir; Her 10 dakikada bir yeni tüneller
 inşa edilir.
- Tünel uzunlukları yapılandırılabilir. Tam koruma için 3 sıçramalı
 tüneller önerilirken, birçok uygulama ve hizmet varsayılan olarak 2
 sıçramalı tünelleri kullanır.

In the future, it could for peers who can afford significant delays (per
[nontrivial delays](#stop) and [batching
strategies](#batching)). In addition, this is only
relevant for destinations that other people know about - a private group
whose destination is only known to trusted peers does not have to worry,
as an adversary can\'t \"ping\" them to mount the attack.

Reference: [One Cell Enough]()

### Hizmet reddi saldırıları {#dos}

I2P ağına karşı her birinin farklı maliyet ve sonuçları olan bir dizi
hizmet reddi saldırısı yapılabilir:

{# DREAD_score(1, 1, 2, 1, 3) #}

**Açgözlü kullanıcı saldırısı:** Basit olarak, katkıda bulunmak
istediklerinden çok daha fazla kaynak tüketmeye çalışan kişiler yapar.
Buna karşı şu savunma yapılır:

- Set defaults so that most users provide resources to the network. In
 I2P, users route traffic by default. In sharp distinction to [other
 networks](), over 95% of I2P users
 relay traffic for others.
- Kullanıcıların ağa katkılarını (paylaşım yüzdesini) artırabilmeleri
 için kolay yapılandırma seçenekleri sağlayın. Kullanıcıların neye
 katkıda bulunduklarını görebilmeleri için \"paylaşma oranı\" gibi
 anlaşılması kolay ölçümleri görüntüleyin.
- Bloglar, forumlar, IRC ve diğer iletişim araçlarıyla güçlü bir
 topluluk oluşturun.

::: {style="clear:both"}
:::

{# DREAD_score(2, 1, 1, 2, 3) #}

**Starvation attack:** A hostile user may attempt to harm the network by
creating a significant number of peers in the network who are not
identified as being under control of the same entity (as with Sybil).
These nodes then decide not to provide any resources to the network,
causing existing peers to search through a larger network database or
request more tunnels than should be necessary. Alternatively, the nodes
may provide intermittent service by periodically dropping selected
traffic, or refusing connections to certain peers. This behavior may be
indistinguishable from that of a heavily-loaded or failing node. I2P
addresses these issues by maintaining
[profiles]() on the peers, attempting to
identify underperforming ones and simply ignoring them, or using them
rarely. We have significantly enhanced the ability to recognize and
avoid troublesome peers; however there are still significant efforts
required in this area.

::: {style="clear:both"}
:::

{# DREAD_score(1, 2, 2, 2, 3) #}

**Flooding attack:** A hostile user may attempt to flood the network, a
peer, a destination, or a tunnel. Network and peer flooding is possible,
and I2P does nothing to prevent standard IP layer flooding. The flooding
of a destination with messages by sending a large number to the
target\'s various inbound tunnel gateways is possible, but the
destination will know this both by the contents of the message and
because the tunnel\'s tests will fail. The same goes for flooding just a
single tunnel. I2P has no defenses for a network flooding attack. For a
destination and tunnel flooding attack, the target identifies which
tunnels are unresponsive and builds new ones. New code could also be
written to add even more tunnels if the client wishes to handle the
larger load. If, on the other hand, the load is more than the client can
deal with, they can instruct the tunnels to throttle the number of
messages or bytes they should pass on (once the [advanced tunnel
operation](#batching) is implemented).

::: {style="clear:both"}
:::

{# DREAD_score(1, 1, 1, 1, 1) #}

**İşlemci yükü saldırısı:** Şu anda, insanların bir eşten uzaktan
kriptografik olarak pahalı bir işlem gerçekleştirmesini isteyebileceği
bazı yöntemler vardır ve bir saldırgan, işlemciyi aşırı yükleyerek bu
eşe çok sayıda saldırı girişiminde bulunmak için bunları kullanabilir.
Hem iyi mühendislik uygulamaları kullanmak hem de potansiyel olarak bu
pahalı isteklere eklenecek önemsiz olmayan sertifikaları (HashCash gibi)
zorunlu kılmak sorunu hafifletmelidir. Ancak hala bir saldırganın
uygulamadaki çeşitli açıklardan yaralanabileceği yerler olabilir.

::: {style="clear:both"}
:::

{# DREAD_score(2, 2, 3, 2, 3) #}

**Floodfill DOS attack:** A hostile user may attempt to harm the network
by becoming a floodfill router. The current defenses against unreliable,
intermittent, or malicious floodfill routers are poor. A floodfill
router may provide bad or no response to lookups, and it may also
interfere with inter-floodfill communication. Some defenses and [peer
profiling]() are implemented, however
there is much more to do. For more information see the [network database
page](#threat).

::: {style="clear:both"}
:::

### Etiketleme saldırıları {#tagging}

{# DREAD_score(1, 3, 1, 1, 1) #}

Tagging attacks - modifying a message so that it can later be identified
further along the path - are by themselves impossible in I2P, as
messages passed through tunnels are signed. However, if an attacker is
the inbound tunnel gateway as well as a participant further along in
that tunnel, with collusion they can identify the fact that they are in
the same tunnel (and prior to adding [unique hop
ids](#tunnelId) and other updates, colluding peers
within the same tunnel can recognize that fact without any effort). An
attacker in an outbound tunnel and any part of an inbound tunnel cannot
collude however, as the tunnel encryption pads and modifies the data
separately for the inbound and outbound tunnels. External attackers
cannot do anything, as the links are encrypted and messages signed.

### Bölümleme saldırıları {#partitioning}

{# DREAD_score(3, 1, 1, 1, 2) #}

Bölümleme saldırıları - Bir ağdaki eşleri (teknik veya analitik olarak)
bölmenin yollarını ararlar. Güçlü bir düşmanla uğraşırken ağın boyutunun
anonimliğinizi belirlemede önemli bir rol oynadığını akılda tutmanız
önemlidir. Bölümlenmiş ağlar oluşturmak için eşler arasında bağlantıları
keserek teknik bölümleme, yerleşik I2P ağ veri tabanı tarafından
işlenir. Burada ağı iyileştirmek için diğer bölümlere yönelik var olan
bağlantılardan yararlanılmasını sağlamak amacıyla çeşitli eşler hakkında
istatistikler tutulur. Ancak, saldırgan kontrolsüz eşlere olan tüm
bağlantıları keserse, hedefi yalıtmış olur ve hiçbir ağ veri tabanı
iyileştirmesi bunu düzeltemez. Bu noktada, yönelticinin yapmayı
umabileceği tek şey, daha önce güvenilir olan önemli sayıda eşin
kullanılamaz olduğunu fark etmek ve istemciyi bağlantısının geçici
olarak kesildiği konusunda uyarmak olur (bu algılama kodu şu anda
kullanılmıyor).

Partitioning the network analytically by looking for differences in how
routers and destinations behave and grouping them accordingly is also a
very powerful attack. For instance, an attacker
[harvesting](#harvesting) the network database will know when a
particular destination has 5 inbound tunnels in their LeaseSet while
others have only 2 or 3, allowing the adversary to potentially partition
clients by the number of tunnels selected. Another partition is possible
when dealing with the [nontrivial delays](#stop)
and [batching strategies](#batching), as the
tunnel gateways and the particular hops with non-zero delays will likely
stand out. However, this data is only exposed to those specific hops, so
to partition effectively on that matter, the attacker would need to
control a significant portion of the network (and still that would only
be a probabilistic partition, as they wouldn\'t know which other tunnels
or messages have those delays).

Also discussed on the [network database
page](#threat) (bootstrap attack).

### Önceleme saldırıları {#predecessor}

{# DREAD_score(1, 1, 1, 1, 3) #}

Önceki saldırı, tünellerine katılarak ve (sırasıyla giden veya gelen
tüneller için) önceki veya sonraki sıçramayı izleyerek hedefe \'yakın\'
olan eşleri görmek amacıyla pasif olarak istatistik topluyor. Zamanla,
tamamen rastgele bir eşler örneği ve rastgele sıralama kullanarak, bir
saldırgan hangi eşin istatistiksel olarak diğerlerinden daha \"yakın\"
olduğunu görebilecek ve bu eş de hedefin bulunduğu yerde olacaktır.

I2P avoids this in four ways: first, the peers selected to participate
in tunnels are not randomly sampled throughout the network - they are
derived from the [peer selection]()
algorithm which breaks them into tiers. Second, with [strict
ordering](#ordering) of peers in a tunnel,
the fact that a peer shows up more frequently does not mean they\'re the
source. Third, with [permuted tunnel
length](#length) (not enabled by default)
even 0 hop tunnels can provide plausible deniability as the occasional
variation of the gateway will look like normal tunnels. Fourth, with
[restricted routes](#fullRestrictedRoutes)
(unimplemented), only the peer with a restricted connection to the
target will ever contact the target, while attackers will merely run
into that gateway.

The current [tunnel build method]() was
specifically designed to combat the predecessor attack. See also [the
intersection attack](#intersection).

References: []() which is an
update to the 2004 predecessor attack paper []().

### Hasat saldırıları {#harvesting}

{# DREAD_score(1, 1, 2, 2, 3) #}

\"Hasat etmek\", I2P çalıştıran kullanıcıların listesini derlemek
anlamına gelir. Yasal saldırılar için ve yalnızca bir eş çalıştırarak,
kiminle bağlantı kurduğunu görerek ve bulabildiği diğer eşlere olan
referansları toplayarak diğer saldırılara yardımcı olacak veriler elde
edilebilir.

I2P aslında, yalnızca bu bilgileri içeren dağıtılmış bir ağ veri tabanı
olduğundan, bu saldırıya karşı etkili savunmalarla tasarlanmamıştır.
Aşağıdaki faktörler, saldırıyı pratikte biraz daha zorlaştırır:

- Ağın büyümesi, ağı belirli bir oranda elde etmeyi zorlaştıracaktır.
- Otomatik doldurma yönelticileri, DOS koruması olarak sorgu
 sınırlarını uygular
- Bir yönelticinin bilgilerinin \"Ağ veri tabanında\" (NetDB)
 yayınlamasını engelleyen (aynı zamanda veri aktarımını da
 engelleyen) \"Gizli kip\" şu anda yaygın olarak kullanılmıyor ancak
 kullanılabilir.

In future implementations, [basic](#nat) and
[comprehensive](#fullRestrictedRoutes) restricted
routes, this attack loses much of its power, as the \"hidden\" peers do
not publish their contact addresses in the network database - only the
tunnels through which they can be reached (as well as their public keys,
etc).

Gelecekte, yönelticiler, bir I2P düğümü olarak tanımlamanın riskli
olacağı belirli bir ülkede olup olmadıklarını belirlemek için GeoIP
verisini kullanabilir. Bu durumda, yöneltici otomatik olarak gizli kipi
etkinleştirebilir veya diğer kısıtlı rota yöntemlerini yürürlüğe
koyabilir.

### Trafik İncelemesi ile Kimlik Belirleme {#traffic}

{# DREAD_score(1, 1, 2, 3, 3) #}

By inspecting the traffic into and out of a router, a malicious ISP or
state-level firewall could identify that a computer is running I2P. As
discussed [above](#harvesting), I2P is not specifically designed to hide
that a computer is running I2P. However, several design decisions made
in the design of the [transport layer and
protocols]() make it somewhat difficult to
identify I2P traffic:

- Rastgele bağlantı noktası seçimi
- Tüm trafiği uçtan uca şifrelemek
- İletişim kuralı baytı veya diğer şifrelenmemiş sabit alanlar olmadan
 Diffie-Hellman anahtar alış verişi
- Simultaneous use of both [TCP]() and
 [UDP]() transports. UDP may be much harder for
 some Deep Packet Inspection (DPI) equipment to track.

Yakın gelecekte, muhtemelen aşağıdakilerle birlikte I2P taşıyıcı
iletişim kurallarını daha da karmaşık hale getirerek trafik analizi
sorunlarını doğrudan ele almayı planlıyoruz:

- Özellikle bağlantı kuruluşunda el sıkışma sırasında, taşıyıcı
 katmanında rastgele uzunluklarda dolgu ekleme
- Paket boyutu dağıtım imzalarının incelenmesi ve gerektiğinde ek
 dolgu ekleme
- SSL veya diğer yaygın iletişim kurallarını taklit eden ek taşıyıcı
 yöntemlerinin geliştirilmesi
- Taşıyıcı katmanındaki paket boyutlarını nasıl etkilediklerini görmek
 için daha yüksek katmanlardaki dolgu ekleme stratejilerinin gözden
 geçirilmesi
- Tor ağına erişimi engellemek için çeşitli devlet düzeyinde güvenlik
 duvarları tarafından uygulanan yöntemlerin gözden geçirilmesi
- Doğrudan \"Derin paket denetimi\" (DPI) ve şaşırtma uzmanlarıyla
 çalışmalar

Reference: [Breaking and Improving Protocol
Obfuscation]()

### Sybil saldırıları {#sybil}

{# DREAD_score(3, 2, 1, 3, 3) #}

Sybil, saldırganın keyfi olarak çok sayıda gizli düğüm oluşturduğu ve
artan sayıları diğer saldırıların yapılmasına yardımcı olmak için
kullandığı bir saldırı kategorisini tanımlar. Örneğin, bir saldırgan,
eşlerin rastgele seçildiği bir ağdaysa ve bu eşlerden biri olma 80&37;
şansı istiyorsa, ağdaki düğüm sayısının beş katını oluşturur ve zarları
atar. Kimlik özgür olduğunda, Sybil güçlü bir düşman için çok etkili bir
teknik olabilir. Bunu ele almanın birincil tekniği basitçe kimliği
\'özgür olmayan\' hale getirmektir -
[Tarzan](http://www.pdos.lcs.mit.edu/tarzan/) (diğerlerinin yanı sıra)
IP adreslerinin sınırlı olduğu gerçeğini kullanırken, IIP yeni bir
kimlik oluşturmak için \'ücret\' almak amacıyla
[HashCash](http://www.hashcash.org/) kullanır. Şu anda Sybil konusunu
ele almak için herhangi bir özel teknik uygulamadık. Ancak yönelticinin
ve hedefin veri yapılarına, gerektiğinde uygun değerde bir HashCash
sertifikası (veya kıtlığı kanıtlayan başka bir sertifika) içerebilen yer
belirtici sertifikaları katıyoruz.

HashCash sertifikalarının çeşitli yerlerde istenmesinin iki büyük sorunu
vardır:

- Geriye dönük uyumluluğu korumak
- Klasik HashCash sorunu. Mobil aygıtlar gibi düşük kaliteli
 makinelerde hala uygulanabilirken, yüksek kaliteli makinelerde
 çalışmanın anlamlı kanıtları olan HashCash değerlerinin seçilmesi.

Belirli bir IP aralığındaki yöneltici sayısındaki çeşitli sınırlamalar,
güvenlik açığını, makineleri birkaç IP bloğuna yerleştirme yeteneğine
sahip olmayan saldırganlara karşı kısıtlar. Ancak bu, güçlü bir rakibe
karşı anlamlı bir savunma sağlamaz.

See the [network database page](#threat) for more
Sybil discussion.

### Arkadaş tüketme saldırıları {#buddy}

{# DREAD_score(3, 2, 2, 1, 3) #}

(Reference: [In Search of an Anonymous and Secure
Lookup]() Section 5.2)

By refusing to accept or forward tunnel build requests, except to a
colluding peer, a router could ensure that a tunnel is formed wholly
from its set of colluding routers. The chances of success are enhanced
if there is a large number of colluding routers, i.e. a [Sybil
attack](#sybil). This is somewhat mitigated by our [peer
profiling]() methods used to monitor the
performance of peers. However, this is a powerful attack as the number
of routers approaches *f* = 0.2, or 20% malicious nodes, as specifed in
the paper. The malicous routers could also maintain connections to the
target router and provide excellent forwarding bandwidth for traffic
over those connections, in an attempt to manipulate the profiles managed
by the target and appear attractive. Further research and defenses may
be necessary.

### Şifreleme saldırıları {#crypto}

{# DREAD_score(3, 2, 1, 3, 1) #}

We use strong cryptography with long keys, and we assume the security of
the industry-standard cryptographic primitives used in I2P, as
documented [on the low-level cryptography
page](). Security features include the
immediate detection of altered messages along the path, the inability to
decrypt messages not addressed to you, and defense against
man-in-the-middle attacks. The key sizes chosen in 2003 were quite
conservative at the time, and are still longer than those used in [other
anonymity networks](https://torproject.org/). We don\'t think the
current key lengths are our biggest weakness, especially for
traditional, non-state-level adversaries; bugs and the small size of the
network are much more worrisome. Of course, all cryptographic algorithms
eventually become obsolete due to the advent of faster processors,
cryptographic research, and advancements in methods such as rainbow
tables, clusters of video game hardware, etc. Unfortunately, I2P was not
designed with easy mechanisms to lengthen keys or change shared secret
values while maintaining backward compatibility.

Upgrading the various data structures and protocols to support longer
keys will have to be tackled eventually, and this will be a [major
undertaking](), just as it will be for
[others](https://torproject.org/). Hopefully, through careful planning,
we can minimize the disruption, and implement mechanisms to make it
easier for future transitions.

Gelecekte, birkaç I2P iletişim kuralı ve veri yapısı, iletilerin
rastgele boyutlara güvenli bir şekilde dolgu eklenmesini destekler. Bu
nedenle iletiler sabit boyutta yapılabilir veya Garlic iletileri
rastgele değiştirilebilir. Böylece bazı dişler gerçekte olduğundan daha
fazla alt diş içeriyor gibi görünebilir. Ancak şu anda Garlic, tünel ve
uçtan uca iletiler basit rastgele dolgu eklemeyi içeriyor.

### Otomatik doldurma anonimlik saldırıları {#floodfill}

{# DREAD_score(3, 2, 1, 2, 2) #}

In addition to the floodfill DOS attacks described [above](#ffdos),
floodfill routers are uniquely positioned to learn about network
participants, due to their role in the netDb, and the high frequency of
communication with those participants. This is somewhat mitigated
because floodfill routers only manage a portion of the total keyspace,
and the keyspace rotates daily, as explained on the [network database
page](#threat). The specific mechanisms by which
routers communicate with floodfills have been [carefully
designed](#delivery). However, these threats
should be studied further. The specific potential threats and
corresponding defenses are a topic for future research.

### Diğer ağ veri tabanı saldırıları {#netdb}

A hostile user may attempt to harm the network by creating one or more
floodfill routers and crafting them to offer bad, slow, or no responses.
Several scenarios are discussed on the [network database
page](#threat).

### Merkezi Kaynak Saldırıları {#central}

{# DREAD_score(1, 1, 1, 3, 3) #}

Saldırıya uğrayabilecek veya saldırılar için bir vektör olarak
kullanılabilecek birkaç merkezi veya sınırlı kaynak (bazıları I2P içinde
olan, bazıları olmayan) vardır. Kasım 2007 tarihinden itibaren jrandom
ortadan kaybolduğundan ve ardından Ocak 2008 tarihinde i2p.net
barındırma hizmeti kaybedildiğinden, I2P ağının geliştirilmesi ve
işletilmesinde çoğu şimdi dağıtılmış olan çok sayıda merkezi kaynak
vurgulanmış oldu. Dışarıdan erişilebilen kaynaklara yapılan saldırılar,
ağın işleyişini değil, esas olarak yeni kullanıcıların bizi bulma
yeteneğini etkiler.

- The [website]() is mirrored and uses DNS
 round-robin for external public access.
- Routers now support [multiple external reseed
 locations](#reseed), however more reseed hosts
 may be needed, and the handling of unreliable or malicious reseed
 hosts may need improvement.
- Yönelticiler artık birden çok güncelleme dosyası konumunu
 destekliyor. Kötü niyetli bir güncelleme sunucusu büyük bir dosya
 gönderebilir, boyutun sınırlaması gerekir.
- Yönelticiler artık birden çok varsayılan güvenilir güncelleme
 imzalayıcısını destekliyor.
- Yönelticiler artık [birden çok güvenilir olmayan otomatik doldurma
 eşini](#ffdos) daha iyi idare ediyor. Kötü amaçlı otomatik doldurma
 üzerine [daha fazla](#floodfill) çalışma yapılması
 [gerekiyor](#ffdos).
- The code is now stored in a [distributed source control
 system]().
- Yönelticiler tek bir haber sunucusuna güveniyor. Ancak farklı bir
 sunucuyu gösteren sabit kodlanmış bir yedek adres vardır. Kötü
 niyetli bir haber sunucusu büyük bir dosya gönderebilir. Boyutun
 sınırlanması gerekir.
- [Naming system services](), including
 address book subscription providers, add-host services, and jump
 services, could be malicious. Substantial protections for
 subscriptions were implemented in release 0.6.1.31, with additional
 enhancements in subsequent releases. However, all naming services
 require some measure of trust, see [the naming
 page]() for details.
- i2p2.de için DNS hizmetine bağlı kalmayı sürdürüyoruz. Bunu
 kaybetmek yeni kullanıcıları çekme yeteneğimizde önemli kesintilere
 neden olur ve kaybı i2p.net örneğinde olduğu gibi ağı (kısa ya da
 orta vadede) küçültür.

### Geliştirme saldırıları {#dev}

{# DREAD_score(2, 1, 1, 3, 1) #}

Bu saldırılar doğrudan ağ üzerinde değil, bunun yerine ya yazılımın
geliştirilmesine katkıda bulunan herkese yasal engeller getirerek ya da
geliştiricilerin yazılımı değiştirmesini sağlamak için var olan her yolu
kullanarak geliştirme ekibinin peşine düşer. Geleneksel teknik önlemler
bu saldırıları yenemez ve birisi bir geliştiricinin hayatını veya
geçimini tehdit ederse (hatta yalnızca bir mahkeme emriyle birlikte
hapis tehdidi altında bir tutuklama emri çıkarsa), büyük bir sorunumuz
olur.

Bununla birlikte, iki teknik bu saldırılara karşı savunmaya yardımcı
olur:

- All components of the network must be open source to enable
 inspection, verification, modification, and improvement. If a
 developer is compromised, once it is noticed the community should
 demand explanation and cease to accept that developer\'s work. All
 checkins to our [distributed source control
 system]() are cryptographically signed,
 and the release packagers use a trust-list system to restrict
 modifications to those previously approved.
- Development over the network itself, allowing developers to stay
 anonymous but still secure the development process. All I2P
 development can occur through I2P - using a [distributed source
 control system](), a distributed source
 control system, IRC chat, public web servers, discussion forums
 (forum.i2p), and the software distribution sites, all available
 within I2P.

Ayrıca, herhangi bir savunmanın gerekmesi durumunda yasal önerilerde
bulunan çeşitli kuruluşlarla ilişkilerimizi sürdürüyoruz.

### Uygulama saldırıları (hatalar) {#impl}

{# DREAD_score(2, 2, 1, 3, 1) #}

Olabildiğince deniyoruz. Çoğu önemsiz uygulamada tasarım veya uygulama
sırasında hatalar bulunur ve I2P bir istisna değildir. I2P üzerinden
çalışan iletişimin anonimliğine veya güvenliğine beklenmedik şekillerde
saldırmak için kullanılabilecek hatalar olabilir. Tasarıma veya
kullanımdaki iletişim kurallarına yönelik saldırılara karşı koymaya
yardımcı olmak için, birçok gözün sistemi iyileştireceği umuduyla tüm
tasarımları ve belgeleri yayınlıyoruz ve incelenmesi ile eleştirilmesini
istiyoruz. [belirsiz bir ortam oluşturarak güvenlik
sağlanacağına](http://www.haystacknetwork.com/) inanmıyoruz.

Ek olarak, koda aynı şekilde davranılıyor ve yazılım sisteminin
gereksinimlerini karşılamayan bir şeyi (değişiklik kolaylığı ile
birlikte) yeniden işlemeye veya atmaya karşı isteksizlik çok az. Ağın ve
yazılım bileşenlerinin tasarımı ve uygulanmasına ilişkin belgeler,
güvenliğin önemli bir parçasıdır. Bunlar olmadan geliştiriciler,
eksiklikleri ve hataları bulmak için yazılımı öğrenmeye yeterince zaman
harcamak istemeyecektir.

Yazılımımızda, özellikle yetersiz bellek hataları (OOM), yöneltici
konsolundaki siteler arası betik çalıştırma (XSS) sorunları ve çeşitli
iletişim kuralları üzerinden yapılan standart olmayan girişlerden
kaynaklanabilecek diğer güvenlik açıkları nedeniyle hizmet reddi ile
ilgili hatalar bulunabilir.

I2P is still a small network with a small development community and
almost no interest from academic or research groups. Therefore we lack
the analysis that [other anonymity networks](https://torproject.org/)
may have received. We continue to recruit people to [get
involved]() and help.

## Diğer Savunmalar

### Engelleme Listeleri {#blocklist}

I2P, bir dereceye kadar bir engelleme listesinde bulunan IP adreslerinde
çalışan eşlerden kaçınacak şekilde geliştirilebilir. P2P karşıtı
kuruluşların, devlet düzeyindeki potansiyel karşıtların ve benzerlerinin
bulunduğu birkaç engelleme listesi, standart biçimlerde yaygın olarak
bulunur.

Etkin eşler güncel engelleme listesinde gerçekten göründükleri ölçüde,
yalnızca bir eş alt kümesi tarafından engelleme, ağı bölümlere ayırma,
erişilebilirlik sorunlarını artırma ve genel güvenilirliği düşürme
eğiliminde olacaktır. Bu nedenle, belirli bir engelleme listesi üzerinde
anlaşmak ve varsayılan olarak etkinleştirmek isteriz.

Engelleme listeleri, kötü niyetliliğe karşı bir dizi savunmanın yalnızca
bir parçasıdır (belki de küçük bir parçasıdır). Profil oluşturma
sistemi, \"Ağ veri tabanı\" (NetDB) herhangi bir şeye güvenmemize gerek
kalmaması için yöneltici davranışını ölçmek amacıyla büyük ölçüde iyi
bir iş çıkarır. Ancak yapılabilecek daha çok şey var. Yukarıdaki
listedeki konuların her biri için, kötü niyetleri algılamakta
yapabileceğimiz iyileştirmeler var.

Bir engelleme listesi otomatik güncellemelerle merkezi bir yerde
barındırılıyorsa, ağ bir [merkezi kaynak saldırısına](#central) karşı
savunmasızdır. Bir listeye otomatik abone olunması, liste hizmeti
sağlayıcısına i2p ağını kapatma gücü verir. Tamamen.

Şu anda, yazılımımızla birlikte yalnızca geçmiş DOS kaynaklarının IP
adreslerini listeleyen varsayılan bir engelleme listesi dağıtılıyor.
Otomatik güncelleme mekanizması yok. Belirli bir IP aralığı I2P ağına
ciddi saldırılar uygularsa, insanlardan forumlar, bloglar gibi bant dışı
mekanizmalar aracılığıyla engelleme listelerini el ile güncellemelerini
istememiz gerekir.


