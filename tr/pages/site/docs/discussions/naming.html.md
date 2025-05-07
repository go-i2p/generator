 Adlandırma
tartışması 

NOTE: The following is a discussion of the reasons behind the I2P naming
system, common arguments and possible alternatives. See [the naming
page]() for current documentation.

## Vazgeçilen alternatifler

I2P üzerinde adlandırma, en başından beri, çeşitli olasılıkların
savunucuları ile sıkça tartışılan bir konu olmuştur. Bununla birlikte,
I2P uygulamasının güvenli iletişim ve merkezi olmayan işleme şekli için
doğal isteği göz önüne alındığında, geleneksel DNS adlandırma sistemi ve
\"çoğunluk kuralları\" oylama sistemleri açıkça geçersizdir.

I2P, DNS benzeri hizmetlerin kullanımını desteklemez, çünkü bir siteyi
ele geçirmenin verdiği zarar çok büyük olabilir - ve güvenli olmayan
hedeflerin hiçbir değeri yoktur. DNSsec hala kayıt şirketlerine ve
sertifika yetkililerine giderken, I2P ile, bir hedefe gönderilen
istekler ya da yanıt, hedefin herkese açık anahtarlarıyla
şifrelendiğinden ve bir hedefin kendisi yalnızca bir çift herkese açık
anahtar ve sertifika olduğundan engellenemez. Öte yandan DNS sistemleri,
arama yolundaki herhangi bir ad sunucusunun basit hizmet reddi ve
sahtekarlık saldırıları başlatmasına izin verir. Bazı merkezi sertifika
yetkilileri tarafından imzalanmış olarak yanıtları doğrulayan bir
sertifika eklemek, düşmanca ad sunucusu sorunlarının çoğunu giderir,
ancak düşman sertifika yetkilisi saldırılarının yanında yeniden yürütme
saldırılarına da açık olur.

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
tutar. Paketlenmiş adlandırma kitaplığında, [alternatif adlandırma
sistemlerinin](#alternatives) takılabileceği basit bir hizmet sağlayıcı
arabirimi bulunur ve son kullanıcıların yeğlediği adlandırma değiş
tokuşunu yapmalarını sağlar.

## Discussion

Ayrıntılı bilgi almak için. [Adlar: Merkezi olmayan, Güvenli, İnsan
tarafından anlaşılabilir: İki seçin](https://zooko.com/distnames.html).

### Comments by jrandom

(26 Kasım 2005 tarihli eski Syndie üzerindeki bir yazıdan alınmıştır)

Soru: Bazı sunucular bir adres üzerinde anlaşamıyorsa ve bazı adresler
çalışırken diğerleri çalışmıyorsa ne yapmalı? Bir adın doğru kaynağı
kimdir?

Yanıt: Yapamazsınız. Bu aslında I2P üzerindeki adlar ile DNS yapısının
çalışma şekli arasındaki kritik bir farktır - I2P üzerindeki adlar
insanlar tarafından okunabilir, güvenlidir, ancak **küresel olarak eşsiz
değildir**. Bu durum tasarımın gereğidir ve güvenlik gereksinimimizin
doğal bir parçasıdır.

Bir şekilde sizi bir adla ilişkili hedefi değiştirmeye ikna
edebilseydim, siteyi \"devralırdım\" ve bu durum hiçbir koşulda kabul
edilemez. Bunun yerine, biz adları **yerel olarak eşsiz** kılarız:
Bunlar, bir siteyi bulmak için *sizin* kullandığınız şeydir. Tıpkı
şeyleri tarayıcınızın yer imlerine veya IM istemcinizin arkadaş
listesine eklediğinizde nasıl her istediğinizi arayabiliyorsanız ona
benzer. \"Patron\" dediğiniz kişi, başka birinin \"Ali\" dediği kişi
olabilir.

Adlar asla güvenli bir şekilde okunabilir ve küresel olarak eşsiz
olmayacak.

### Comments by zzz

Aşağıda I2P adlandırma sistemiyle ilgili yaygın şikayetlerin zzz
tarafından derlenmiş sonuçlarını görebilirsiniz.

- **Verimsizlik:** Hosts.txt dosyasının tümü indirilir (eepget etag ve
 son değiştirilen üst bilgileri kullandığından, dosya değiştiyse). Şu
 anda neredeyse 800 sunucu için yaklaşık 400K boyutunda.

 Doğru, ancak bu, kendisi çılgınca verimsiz olan i2p bağlamında çok
 büyük bir trafik oluşturmaz (otomatik doldurma veri tabanları, büyük
 şifreleme ek yükü ve dolgu ekleme, garlic yöneltme, vb.). Her 12
 saatte bir, hosts.txt dosyasını birinden indirsenize, ortalama 10
 bayt/sn trafik oluşur.

 Genellikle i2p üzerinde olduğu gibi, burada anonimlik ve verimlilik
 arasında temel bir uzlaşma vardır. Bazı kişiler, verileri en son ne
 zaman istediğinizi ortaya çıkardığı için etag ve son değiştirilen
 üst bilgileri kullanmanın tehlikeli olduğunu söyleyebilir. Başka
 kişiler, büyük olasılıkla daha fazla anonimlik maliyetine yol açacak
 şekilde, yalnızca belirli anahtarların istenmesini önerdi (atlama
 hizmetlerinin yaptığına benzer, ancak daha otomatik bir şekilde).

 Possible improvements would be a replacement or supplement to
 address book (see [p](http:///)), or something simple like
 subscribing to http://example.i2p/cgi-bin/recenthosts.cgi rather
 than http://example.i2p/hosts.txt. If a hypothetical recenthosts.cgi
 distributed all hosts from the last 24 hours, for example, that
 could be both more efficient and more anonymous than the current
 hosts.txt with last-modified and etag.

 A sample implementation is on stats.i2p at [](). This script returns an Etag with a
 timestamp. When a request comes in with the If-None-Match etag, the
 script ONLY returns new hosts since that timestamp, or 304 Not
 Modified if there are none. In this way, the script efficiently
 returns only the hosts the subscriber does not know about, in an
 address book-compatible manner.

 Dolayısıyla verimsizlik büyük bir sorun değil ve radikal
 değişiklikler yapmadan durumu iyileştirmenin birkaç yolu var.

- **Ölçeklenebilir değil:** 400K boyutundaki hosts.txt (doğrusal arama
 ile) dosyası şu anda o kadar da büyük değil ve büyük olasılıkla bir
 soruna yol açmadan 10 ya da 100 katına çıkarabiliriz.

 Ağ trafiği açısından, yukarıya bakabilirsiniz. Ancak, bir anahtar
 için ağ üzerinden yavaş bir gerçek zamanlı sorgu yapmayacaksanız,
 tüm anahtar kümesini, anahtar başına yaklaşık 500 bayt maliyetle
 yerel olarak depolamanız gerekir.

- **Yapılandırma ve \"güvenmeyi\" gerektirir:** Kullanıma hazır adres
 defteri yalnızca http://www.i2p2.i2p/hosts.txt adresine abonedir ve
 nadiren güncellenir. Bu durum yeni kullanıcı deneyiminin
 kötüleşmesine neden olur.

 Bu durum çok kasıtlı olarak düşünülmüştür. jrandom, bir kullanıcının
 bir hosts.txt hizmeti sağlayıcısına \"güvenmesini\" ister ve
 kendisinin de söylemeyi sevdiği gibi, \"güvenmek bir evet/hayır
 konusu değildir\". Yapılandırma adımı, kullanıcıların anonim bir
 ağdaki güven sorunları hakkında düşünmesini sağlar.

 Başka bir örnek olarak, HTTP vekil sunucusundaki \"I2P Sitesi
 Bilinmiyor\" hata sayfası bazı atlama hizmetlerini listeler. Ancak
 özellikle herhangi birini \"önermez\" ve birini seçmek (ya da
 seçmemek) kullanıcıya bağlıdır. jrandom, listelenen hizmet
 sağlayıcılara onları listeleyecek kadar güvendiğimizi ancak anahtarı
 onlardan otomatik olarak alacak kadar güvenmediğimizi söylerdi.

 Bu uygulama ne kadar başarılı, emin değilim. Ancak adlandırma
 sistemi için bir tür güven hiyerarşisi olmalıdır. Herkese eşit
 davranmak, hırsızlık riskini artırabilir.

- **Bu bir DNS değildir**

 Ne yazık ki, i2p üzerinden gerçek zamanlı arama yapmak, internet
 üzerinde gezinmeyi önemli ölçüde yavaşlatır.

 Ayrıca DNS, aramalarda sınırlı ön belleğe alma ve ayrılma süresi
 temelinde işlerken i2p anahtarları kalıcıdır.

 Tabi ki bunu işletecek bir yol bulabiliriz, ama neden? Bu kötü bir
 uyum olur.

- **Güvenilir değil:** Adres defteri abonelikleri için belirli
 sunuculara bağlı olur.

 Evet, yapılandırdığınız birkaç sunucuya bağlı olur. i2p üzerinde ise
 sunucular ve hizmetler bugün var yarın yok olabilir. Diğer herhangi
 bir merkezi sistem (örneğin, DNS kök sunucuları) aynı sorunu
 yaşayacaktır. Tamamen merkezi olmayan bir sistem (herkesin yetkili
 olduğu) ile \"herkes bir kök DNS sunucusudur\" çözümünü uygulayarak
 ya da hosts.txt dosyanızdaki herkesi adres defterinize ekleyen bir
 betik gibi daha da basit bir şeyle oluşturulabilir.

 Bununla birlikte, merkezi ve tam yetkili çözümleri savunan kişiler,
 genellikle çatışmalar ve uçak kaçırma gibi konuları düşünmediler.

- **Garip ama gerçek zamanlı değil:** Bu yapı, hosts.txt
 sağlayıcıları, anahtar ekleme internet formu hizmeti sağlayıcıları,
 atlama hizmeti sağlayıcıları, I2P sitesi durumu bildirme
 hizmetlerinden oluşan bir yamalı bohçadır. Atlama sunucuları ve
 abonelikler bir sorundur, yalnızca DNS gibi çalışmalıdır.

 Güvenilirlik ve güven bölümlerine bakın.

Özetle, var olan sistem korkunç bir şekilde bozuk, verimsiz veya
ölçeklenemez değil ve \"yalnızca DNS kullanma\" önerileri üzerinde de
iyice düşünülmüş değil.

## Alternatifler {#alternatives}

I2P kaynağında, birkaç değiştirilebilir adlandırma sistemi bulunur ve
adlandırma sistemleriyle denemeyi etkinleştiren yapılandırma
seçeneklerini destekler.

- **Meta** - Sırayla iki veya daha fazla başka adlandırma sistemini
 çağırır. Varsayılan olarak, PetName ve ardından HostsTxt çağrılır.

- **PetName** - Bir petnames.txt dosyasında arar. Bu dosyanın biçimi
 hosts.txt ile aynı DEĞİLDİR.

- **HostsTxt** - Sırasıyla aşağıdaki dosyalara bakar:

- 1. privatehosts.txt
 2. userhosts.txt
 3. hosts.txt

- **AddressDB** - Her sunucu, bir addressDb/ klasöründe ayrı bir
 dosyada listelenir.

- **Eepget** - Bir dış sunucudan bir HTTP arama isteği yapar - Meta
 ile HostsTxt aramasından sonra gelmelidir. Bu, atlama sistemini
 artırabilir veya değiştirebilir. Bellek içi ön belleğe alma özelliği
 vardır.

- **Exec** - arama için bir dış program çağırır, Java dışında bağımsız
 arama şemalarında ek deneylere izin verir. HostsTxt aramasından
 sonra veya tek adlandırma sistemi olarak kullanılabilir. Bellek içi
 ön belleğe alma özelliği vardır.

- **Dummy** - Base64 adları için yedek olarak kullanılır. Yoksa
 başarısız olur.

Geçerli adlandırma sistemi, gelişmiş yapılandırma seçeneği
\'i2p.naming.impl\' ile değiştirilebilir (yeniden başlatma gerekir).
Ayrıntılar için core/java/src/net/i2p/client/names bölümüne
bakabilirsiniz.

Adres defteri yalnızca hosts.txt dosyalarını ve biçimini bildiğinden,
herhangi bir yeni sistem HostsTxt ardından gelmelidir veya yerel
depolama ve/veya adres defteri abonelik işlevlerini uygulamalıdır.

## Sertifikalar {#certificates}

I2P hedeflerinde bir sertifika bulunur. Ancak şu anda sertifika her
zaman Null değerindedir. Bir null sertifika ile, base64 hedefleri her
zaman \"AAAA\" ile biten 516 bayttır Sertifika, bu adres defteri
birleştirme yöntemi ile ve başka yerlerde de kontrol ediliyor olabilir.
Ayrıca, bir sertifika oluşturmak veya bir hedefe eklemek için
kullanılabilecek bir yöntem yoktur. Bu nedenle, sertifikaları uygulamak
için bunların güncellenmesi gerekecek.

One possible use of certificates is for [proof of
work](#hashcash).

Bir diğeri \"alt etki alanları\" içindir (tırnak içinde çünkü gerçekte
böyle bir şey yoktur, i2p düz bir adlandırma sistemi kullanır) 2. düzey
etki alanının anahtarları tarafından imzalanacak.

Herhangi bir sertifika uygulamasında, sertifikaları doğrulama yöntemi
gelmelidir. Büyük olasılıkla bu, adres defteri birleştirme kodunda
bulunur. Birden çok sertifika türü veya birden çok sertifika için bir
yöntem var mı?

Bazı merkezi sertifika yetkilisi tarafından imzalanmış yanıtları
doğrulayan bir sertifika eklemek, kötü niyetli ad sunucusu sorunlarının
çoğunu giderecek. Ancak kötü niyetli sertifika yetkilisi saldırılarının
yanında açık yeniden yürütme saldırılarını da bırakacaktır.


