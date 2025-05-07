 Eş Profilinin
Belirlenmesi ve Seçimi 2024-02 0.9.62 

## NOTE

This page describes the Java I2P implementation of peer profiling and
selection as of 2010. While still broadly accurate, some details may no
longer be correct. We continue to evolve banning, blocking, and
selection strategies to address newer threats, attacks, and network
conditions. The current network has multiple router implementations with
various versions. Other I2P implementations may have completely
different profiling and selection strategies, or may not use profiling
at all.

## Özet

### Eş Profilinin Belirlenmesi

**Peer profiling** is the process of collecting data based on the
**observed** performance of other routers or peers, and classifying
those peers into groups. Profiling does **not** use any claimed
performance data published by the peer itself in the [network
database]().

Profiller iki amaçla kuıllanılır:

1. Aşağıda tartışılan, trafiğimizi aktarmak için eşlerin seçilmesi
2. Choosing peers from the set of floodfill routers to use for network
 database storage and queries, which is discussed on the [network
 database]() page

### Eş Seçimi

**Eş seçimi**, iletilerimizi aktarmak için ağda hangi yönelticilerden
geçmesini istediğimizi seçme işlemidir (hangi eşlerin tünellerimize
katılmasını isteyeceğiz). Bunu başarmak için, her bir eşin başarımını
(eşin \"profili\") izleriz ve bu verilerle ne kadar hızlı olduklarını,
isteklerimizi ne sıklıkla kabul edebileceklerini, aşırı yüklenmiş gibi
görünüp görünmediklerini ve işlemleri güvenilir bir şekilde yerine
getirebilecekler mi öngörmek için kullanırız.

Unlike some other anonymous networks, in I2P, claimed bandwidth is
untrusted and is **only** used to avoid those peers advertising very low
bandwidth insufficient for routing tunnels. All peer selection is done
through profiling. This prevents simple attacks based on peers claiming
high bandwidth in order to capture large numbers of tunnels. It also
makes [timing attacks](#timing) more
difficult.

Bir yöneltici çok sayıda istemci ve keşif tüneli tutabileceğinden ve
tünel ömrü yalnızca 10 dakika olduğundan, eş seçimi oldukça sık yapılır.

### Diğer Bilgiler

For more information see the paper [Peer Profiling and Selection in the
I2P Anonymous Network]() presented at [PET-CON
2009.1](). See [below](#notes) for notes on minor
changes since the paper was published.

## Profiller

Each peer has a set of data points collected about them, including
statistics about how long it takes for them to reply to a network
database query, how often their tunnels fail, and how many new peers
they are able to introduce us to, as well as simple data points such as
when we last heard from them or when the last communication error
occurred. The specific data points gathered can be found in the
[code]().

Profiller oldukça küçüktür ve birkaç KB boyutundadır. Bellek kullanımını
kontrol etmek için, profil sayısı arttıkça profil geçerliliği süresi
azalır. Profiller, diske yazıldığında yöneltici kapanana kadar bellekte
tutulur. Başlangıçta profiller okunur, böylece yönelticinin tüm
profilleri yeniden başlatmasına gerek kalmaz. Böylece bir yönelticinin
başlatılmasından sonra hızla ağ ile yeniden bütünleşmesine izin verilir.

## Eş Özetleri

Profiller bir eşin başarımının bir özeti olarak kabul edilebilirken,
etkili eş seçimine izin vermek için her bir özeti, eşin hızını,
kapasitesini, ağ ile ne kadar iyi bütünleştiğini ve ne kadar başarısız
olduğunu gösteren dört basit değere böldük.

### Hız

Hız hesaplaması basitçe profilden geçer ve bir dakika içinde eş
üzerinden tek bir tünelde ne kadar veri gönderip alabileceğimizi
öngörür. Bu öngörü için yalnızca bir önceki dakikadaki başarıma bakar.

### Kapasite {#capacity}

Kapasite hesaplaması basitçe profilden geçer ve eşin belirli bir zaman
diliminde kaç tünele katılmayı kabul edeceğini öngörür. Bu öngörü için,
eşin kaç tünel oluşturma isteğini kabul ettiğine, reddettiğine ve
vazgeçtiğine ve daha sonra üzerinde uzlaşmaya varılan tünellerden
kaçının başarısız olduğuna bakar. Hesaplama zaman ağırlıklı olarak
yapılır. Yakın geçmişteki eylemler daha eski eylemlere göre daha
ağırlıklıdır. 48 saate kadar olan istatistikler katılabilir.

Güvenilmez ve ulaşılamayan eşleri tanımak ve bunlardan kaçınmak kritik
derecede önemlidir. Ne yazık ki, tünel oluşturma ve sınama birkaç eşin
katılımını gerektirdiğinden, vazgeçilen bir oluşturma isteğinin ya da
sınama hatasının nedenini kesin olarak belirlemek zordur. Yöneltici,
eşlerin her birine bir arıza olasılığı atar ve bu olasılığı kapasite
hesaplamasında kullanır. Vazgeçmeler ve sınama başarısızlıkları,
reddetmelere göre ağırlıklıdır.

## Eş organizasyonu

Yukarıda bahsedildiği gibi, birkaç temel hesaplama yapmak için her bir
eşin profilini inceleriz ve bunlara dayanarak, her bir eşi hızlı, yüksek
kapasiteli ve standart olmak üzere üç gruba ayırırız.

Gruplamalar birbirini dışlamaz ya da ilgisiz değildir:

- Bir eşin kapasite hesaplaması tüm eşlerin medyan değerine eşit ya da
 büyükse \"yüksek kapasiteli\" olarak kabul edilir.
- Bir eş, zaten \"yüksek kapasiteli\" ise ve hız hesaplamaları tüm
 eşlerin medyan değerine eşit ya da büyükse \"hızlı\" olarak kabul
 edilir.
- Bir eş, \"yüksek kapasiteli\" değilse \"standart\" olarak kabul
 edilir

These groupings are implemented in the router\'s
[ProfileOrganizer]().

### Grup boyutu sınırları

Grupların büyüklüğü sınırlı olabilir.

- Hızlı grup 30 eş ile sınırlıdır. Daha fazla olacaksa, yalnızca en
 yüksek hız derecesindekiler gruba yerleştirilir.
- Yüksek kapasiteli grup 75 eşle sınırlıdır (hızlı grup dahil) Daha
 fazla olacaksa, yalnızca en yüksek kapasite derecesindekiler gruba
 yerleştirilir.
- Standart grubun sabit bir sınırı yoktur, ancak yerel \"Ağ veri
 tabanı\" (netDB) üzerinde depolanan \"Yöneltici bilgileri\"
 (RouterInfo) sayısından biraz daha küçüktür. Günümüz ağındaki etkin
 bir yönelticide, yaklaşık 1000 \"Yöneltici bilgisi\" (RouterInfo) ve
 500 eş profil (hızlı ve yüksek kapasiteli gruplardakiler dahil)
 bulunabilir.

## Yeniden Hesaplama ve Kararlılık

Özetler yeniden hesaplanır ve eşler her 45 saniyede bir gruplara
ayrılır.

Gruplar oldukça kararlı olma eğilimindedir. Yani her yeniden hesaplamada
sıralamada çok fazla \"çalkalanma\" yoktur. Hızlı ve yüksek kapasiteli
gruplardaki eşler, içlerinde daha fazla tünel oluşturur. Bu da onların
hız ve kapasite oranlarını artırır ve gruptaki varlıklarını güçlendirir.

## Eş Seçimi

Yöneltici, tüneller oluşturmak için yukarıdaki gruplardan eşler seçer.

### İstemci Tünelleri için Eş Seçimi

İstemci tünelleri, HTTP vekil sunucuları ve site sunucuları gibi
uygulama trafiği için kullanılır.

[Bazı saldırılara](http://blog.torproject.org/blog/one-cell-enough)
duyarlılığı azaltmak ve başarımı artırmak için, istemci tünelleri
oluşturmaya yönelik eşler, \"hızlı\" grup olan en küçük gruptan rastgele
seçilir. Daha önce aynı istemci için bir tünele katılan eşleri seçmeye
yönelik bir önyargı yoktur.

### Keşif Tünelleri için Eş Seçimi

Keşif tünelleri, ağ veri tabanı trafiği ve istemci tünellerini sınama
gibi yöneltici yönetim amaçları için kullanılır. Keşif tünelleri, daha
önce bağlantısı olmayan yönelticilerle iletişim kurmak için de
kullanılır, bu nedenle bunlara \"keşif\" adı verilir. Bu tüneller bant
genişliği genellikle düşüktür.

Keşif tünelleri oluşturmak için eşler genellikle standart gruptan
rastgele seçilir. Bu oluşturma girişimlerinin başarı oranı, istemci
tüneli oluşturma başarı oranına kıyasla düşükse, yöneltici, bunun yerine
yüksek kapasite grubundan rastgele bir ağırlıklı ortalamadaki eşleri
seçer. Böylece, ağ başarımı düşük olduğunda bile tatmin edici bir
derleme başarı oranı korunabilir. Daha önce bir keşif tüneline katılan
eşleri seçmeye yönelik bir önyargı yoktur.

Standart grup, yönelticinin bildiği tüm eşlerin çok büyük bir alt
kümesini içerdiğinden, keşif tünelleri, temel olarak, oluşturma başarı
oranı çok düşük olana kadar tüm eşlerin rastgele seçilmesiyle
oluşturulur.

### Kısıtlamalar

Bazı basit saldırıları önlemek ve başarımı artırmak için aşağıdaki
kısıtlamalar vardır:

- Aynı /16 IP adresi aralığından iki eş aynı tünelde olmayabilir.
- Bir eş, yöneltici tarafından oluşturulan tüm tünellerin en fazla 33%
 kadarına katkıda bulunabilir.
- Bant genişliği çok düşük olan eşler kullanılmaz.
- Yakın zamanda bir bağlantı girişiminin başarısız olduğu eşler
 kullanılmaz.

### Tünellerde Eş Sıralaması

Peers are ordered within tunnels to to deal with the [predecessor
attack]() [(2008
update)](). More information is on the [tunnel
page](#ordering).

## Gelecekte Yapılacak Çalışmalar

- Gerekli oldukça hız ve kapasite hesaplamalarını incelemeye ve ince
 ayarları yapmayı sürdürün
- Ağ büyüdükçe bellek kullanımını denetlemek için gerekirse daha
 agresif bir çıkartma stratejisi uygulayın
- Grup boyutu sınırlarını değerlendirin
- Yapılandırılmışsa, belirli eşlerin katılması ya da katılmaması için
 GeoIP verilerini kullanın

## Notlar {#notes}

For those reading the paper [Peer Profiling and Selection in the I2P
Anonymous Network](), please keep in mind the
following minor changes in I2P since the paper\'s publication:

- Bütünleşme hesaplaması hala kullanılmıyor
- Makalede, \"gruplar\" \"düzeyler\" olarak anılmıştır.
- \"Başarısız\" düzeyi artık kullanılmıyor
- \"Başarısız olmayan\" düzeyi artık \"Standart\" olarak
 adlandırılıyor

## Referanslar

- [I2P anonim ağında eş profilinin belirlenmesi ve
 seçimi](pdf/I2P-PET-CON-2009.1.pdf)
- [Bir hücre yeter](http://blog.torproject.org/blog/one-cell-enough)
- [Tor giriş
 koruyucuları](https://wiki.torproject.org/noreply/TheOnionRouter/TorFAQ#EntryGuards)
- [Murdoch 2007
 makalesi](http://freehaven.net/anonbib/#murdoch-pet2007)
- [Tor için ince
 ayarlar](http://www.crhc.uiuc.edu/~nikita/papers/tuneup-cr.pdf)
- [Tor karşıtı düşük kaynaklı yöneltme
 saldırıları](http://cs.gmu.edu/~mccoy/papers/wpes25-bauer.pdf)


