 BOB - Basic Open
Bridge 2022-06 

## Warning - Deprecated

Not for use by new applications. BOB supports the DSA-SHA1 signature
type only. BOB will not be extended to support new signature types or
other advanced features. New applications should use [SAM
V3]().

BOB is not supported in Java I2P new installs as of release 1.7.0
(2022-02). It will still work in Java I2P originally installed as
version 1.6.1 or earlier, even after updates, but it is unsupported and
may break at any time. BOB is still supported by i2pd as of 2022-06, but
applications should still migrate to SAMv3 for the reasons above.

At this point, most of the good ideas from BOB have been incorporated
into SAMv3, which has more features and more real-world use. BOB may
still work on some installations (see above), but it is not gaining the
advanced features available to SAMv3 and is essentially unsupported,
except by i2pd.

## Language libraries for the BOB API

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python -
 [i2py-bob](http:///w/i2py-bob.git)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## Özet

`ANAHTARLAR` = Anahtar çifti herkese açık+özel, BASE64 biçiminde

`KEY` = Herkese açık anahtar, BASE64 biçiminde

`ERROR`çıktısı, `"HATA"+AÇIKLAMA+"\n"` iletisini döndürür, burada
`AÇIKLAMA` sorunun çıktığı yerdir.

`OK`, `"OK"` iletisini döndürür ve veri varsa o da aynı satırdadır. `OK`
komut yürütülmesinin tamamlandığı anlamına gelir.

`DATA` satırlarında, istediğiniz bilgiler bulunur. Bir istek için birkaç
`DATA` satırı olabilir.

**NOT:** Help komutu, kural ayrıcalığı olan TEK komuttur\... Aslında
hiçbir şey döndürmez! Bu kasıtlıdır, çünkü yardım bir UYGULAMA komutu
değil bir İNSAN komutudur.

## Bağlantı ve Sürüm

Tüm BOB durum çıktıları satır şeklindedir. Satırlar, kullanılan sisteme
bağlı olarak \\n veya \\r\\n sona erebilir. Bağlantı kurulduğunda, BOB
iki satır döndürür:

 BOB version OK 

Kullanılan sürüm: 00.00.10

Önceki sürümlerin büyük onaltılık rakamlar kullandığını ve I2P sürüm
oluşturma standartlarına uygun olmadığını unutmayın. Sonraki sürümlerin
yalnızca 0-9 rakamlarını kullanması önerilir. 00.00.10

Sürüm geçmişi

 Sürüm I2P Yöneltici Sürümü Değişiklikler
 --------------------- ---------------------- ----------------------
 00.00.10 0.9.8 geçerli sürüm
 00.00.00 - 00.00.0F   geliştirme sürümleri

## Komutlar

**LÜTFEN DİKKAT:** Komutlarla ilgili GÜNCEL bilgiler için LÜTFEN
yerleşik yardım komutunu kullanın. Bunun için localhost 2827 adresine
telnet açın ve help yazın. Böylece her komutla ilgili tam bilgileri
görebilirsiniz.

Komutlar asla eskimez veya değiştirilmez. Ancak zamanla yeni komutlar
eklenir.

 COMMAND OPERAND RETURNS help (optional
command to get help on) NOTHING or OK and description of the command
clear ERROR or OK getdest ERROR or OK and KEY getkeys ERROR or OK and
KEYS getnick tunnelname ERROR or OK inhost hostname or IP address ERROR
or OK inport port number ERROR or OK list ERROR or DATA lines and final
OK lookup hostname ERROR or OK and KEY newkeys ERROR or OK and KEY
option key1=value1 key2=value2\... ERROR or OK outhost hostname or IP
address ERROR or OK outport port number ERROR or OK quiet ERROR or OK
quit OK and terminates the command connection setkeys KEYS ERROR or OK
and KEY setnick tunnel nickname ERROR or OK show ERROR or OK and
information showprops ERROR or OK and information start ERROR or OK
status tunnel nickname ERROR or OK and information stop ERROR or OK
verify KEY ERROR or OK visit OK, and dumps BOB\'s threads to the
wrapper.log zap nothing, quits BOB 

Kurulduktan sonra, tüm TCP soketleri gerektiğiNDE engellenebilir ve
engellenecektir. Komut kanalına/kanalından herhangi bir ek iletiye gerek
yoktur. Bu durum, yönelticinin, birçok akışı tek bir sokete sokmaya veya
dışarı atmaya çalışırken boğulmasında SAM ile olduğu gibi OOM ile
patlamadan akışı hızlandırmasını sağlar. Çok fazla bağlantınız olduğunda
ölçeklenemez!

Bu özel arayüzün güzel yanı, herhangi bir şey yazmanın SAM yöntemine
göre çok daha kolay olmasıdır. Kurulumdan sonra yapılacak başka bir
işlem yoktur. Yapılandırma o kadar basittir ki, nc (netcat) gibi çok
basit araçlar bazı uygulamaları gösterecek şekilde kullanılabilir. Bunun
önemi, kişinin bir uygulamanın çalışacağı ve duracağı zamanları
planlayabilmesi ve bunun için uygulamayı değiştirmesinin, hatta
durdurmasının gerekmemesidir. Bunun yerine, kelimenin tam anlamıyla
hedefin \"fişini çıkarabilir\" ve yeniden \"takabilirsiniz\". Köprüyü
kurarken aynı IP/bağlantı noktası adresleri ve hedef anahtarlar
kullanıldığı sürece, normal TCP uygulaması için bir şey fark
etmeyecektir. Basitçe kandırılmış olur. Hedeflere erişilemez ve herhangi
bir bilgi gelmez.

## Örnekler

Aşağıdaki örnek için, iki hedefli çok basit bir yerel geri döngü
bağlantısı kuracağız. Hedef \"ağız\", INET süper sunucu arka plan
programının CHARGEN hizmeti olacaktır. Hedef \"kulak\", telnet
yapabileceğiniz ve güzel ASCII testinin çıktısını izleyebileceğiniz
yerel bir bağlantı noktası olacaktır.

 ÖRNEK OTURUM İLETİŞİMİ \-- basit telnet
127.0.0.1 2827 çalışır A = Application C = BOB komut yanıtı. FROM TO
DIALOGUE C A BOB 00.00.10 C A OK A C setnick mouth C A OK Nickname set
to mouth A C newkeys C A OK
ZMPz1zinTdy3\~zGD\~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr\~0g2-l0vM7Y8nSqtFrSdMw\~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU\~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq\~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw\~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA


**YUKARIDAKİ HEDEF ANAHTARINA DİKKAT EDİN, SİZİNKİ FARKLI OLACAKTIR!**

 FROM TO DIALOGUE A C outhost 127.0.0.1 C A
OK outhost set A C outport 19 C A OK outbound port set A C start C A OK
tunnel starting 

Bu noktada herhangi bir hata olmadı, \"ağız\" takma adıyla bir hedef
kuruldu. Belirtilen hedefle iletişim kurduğunuzda, aslında `19/TCP`
üzerindeki `CHARGEN` hizmetine bağlanırsınız.

Şimdi kalan yarısı, böylece bu hedefle gerçekten iletişime geçebiliriz.

 FROM TO DIALOGUE C A BOB 00.00.10 C A OK A
C setnick ear C A OK Nickname set to ear A C newkeys C A OK
8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg\~3eXtL-7S-qU-wdP-6VF\~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J\~flAvF4wrbF-LfVpMdg\~tjtns6fA\~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f\~dzoRCapAGDDTTnvjXuLrZ-vN-orT\~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A C inhost 127.0.0.1 C A OK inhost set A C inport 37337 C A OK inbound
port set A C start C A OK tunnel starting A C quit C A OK Bye! 

Şimdi tek yapmamız gereken 127.0.0.1 adresinden 37337 numaralı bağlantı
noktasına telnet açtıktan sonra, iletişim kurmak istediğimiz adres
defterinden hedef anahtarı veya sunucu adresini göndermektir. Bu durumda
\"ağız\" ile iletişime geçmek istiyoruz, tek yapmamız gereken anahtarı
yapıştırmak ve göndermek.

**NOT:** Komut kanalındaki \"quit\" komutu, SAM gibi tünellerin
bağlantısını KESMEZ.

 \$ telnet 127.0.0.1 37337 Trying
127.0.0.1\... Connected to 127.0.0.1. Escape character is \'\^\]\'.
ZMPz1zinTdy3\~zGD\~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr\~0g2-l0vM7Y8nSqtFrSdMw\~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU\~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq\~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw\~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefg
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefgh
\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghi
#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghij
\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghijk
\... 

Bu püskürmenin birkaç sanal mili geçtikten sonra, `Control-]` üzerine
basın

 \... cdefghijklmnopqrstuvwxyz{\|}\~
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{\|}\~
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{\|}\~ !\"#\$%&\'()\*+,-./0123456789:;\<= telnet\>
c Connection closed. 

İşte olanlar\...

 telnet -\> ear -\> i2p -\> mouth -\>
chargen -. telnet \<- ear \<- i2p \<- mouth \<\-\-\-\-\-\-\-\-\-\--\' 

I2P sitelerine de bağlanabilirsiniz!

 \$ telnet 127.0.0.1 37337 Trying
127.0.0.1\... Connected to 127.0.0.1. Escape character is \'\^\]\'.
i2host.i2p GET / HTTP/1.1 HTTP/1.1 200 OK Date: Fri, 05 Dec 2008
14:20:28 GMT Connection: close Content-Type: text/html Content-Length:
3946 Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT Accept-Ranges: bytes
\<html\> \<head\> \<title\>I2HOST\</title\> \<link rel=\"shortcut icon\"
href=\"favicon.ico\"\> \</head\> \... \<a
href=\"http://sponge.i2p/\"\>\--Sponge.\</a\>\</pre\> \<img
src=\"/counter.gif\" alt=\"!@\^7A76Z!#(\*&amp;%\"\> visitors. \</body\>
\</html\> Connection closed by foreign host. \$ 

Çok güzel değil mi? Farklı durumlarda ne tür bir çıktının beklendiğini
anlamak için, isterseniz, iyi bilinen diğer bazı I2P sitelerini, var
olmayanları vb. deneyin. Çoğunlukla, hata iletilerinden tümünü görmezden
gelmeniz önerilir. Uygulama için anlamları yoktur ve yalnızca insan hata
ayıklaması için sunulurlar.

Artık onlarla işimiz bittiğine göre hedeflerimizi yazalım.

İlk olarak, hangi hedef takma adlarına sahip olduğumuzu görelim.

 FROM TO DIALOGUE A C list C A DATA
NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true
QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST:
127.0.0.1 C A DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING:
false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT:
not_set OUTHOST: localhost C A OK Listing done 

Tamam, işte buradalar. Önce \"ağız\" hedefini kaldıralım.

 FROM TO DIALOGUE A C getnick mouth C A OK
Nickname set to mouth A C stop C A OK tunnel stopping A C clear C A OK
cleared 

Şimdi \"kulağı\" kaldırmak için, çok hızlı yazdığınızda olanın bu
olduğunu ve size tipik HATA iletilerinin nasıl göründüğünü gösterdiğini
unutmayın.

 FROM TO DIALOGUE A C getnick ear C A OK
Nickname set to ear A C stop C A OK tunnel stopping A C clear C A ERROR
tunnel is active A C clear C A OK cleared A C quit C A OK Bye! 

Çok basit olduğu için bir köprünün alıcı ucunun bir örneğini göstermeye
zahmet etmeyeceğim. Bunun için iki olası ayar vardır ve \"quiet\"
komutuyla değiştirilir.

Varsayılan quiet DEĞİLDİR ve dinleme soketinize gelen ilk veri, bağlantı
kuran hedeftir. BASE64 adresinin ardından yeni bir satırdan oluşan tek
bir satırdır. Bundan sonraki her şey, uygulamanın gerçekten tüketmesi
içindir.

Quiet kipinde, normal bir İnternet bağlantısı gibi düşünün. Hiçbir ek
veri gelmiyor. Normal İnternete doğrudan bağlıymışsınız gibi. Bu kip,
yöneltici panosu tünel ayarları sayfalarında bulunana çok benzer bir
saydamlık biçimine izin verir. Böylece örneğin bir site sunucusunda bir
hedefi göstermek için BOB kullanabilirsiniz ve site sunucusunda
değişiklik yapmanız gerekmez.

Bunun için BOB kullanmanın avantajı daha önce tartışıldığı gibidir.
Uygulama için rastgele çalışma süreleri planlayabilir, farklı bir
bilgisayara yeniden yönlendirebilir vb. Hizmetlerde rastgele açılış ve
kapanış zamanları oluşturmak için tamamen farklı bir süreçle hedefi
durdurabilir ve başlatabilirsiniz. Bu şekilde, yalnızca böyle bir
hizmetle iletişim kurma yeteneğini durdurmuş olursunuz ve onu kapatıp
yeniden başlatmakla uğraşmanıza gerek kalmaz. Güncellemeler yaparken
yerel ağıjnızdaki farklı bir bilgisayarı yönlendirebilir ve gösterebilir
veya neyin çalıştığına vb. bağlı olarak bir dizi yedekleme biligsayarına
işaret edebilirsiniz. BOB ile yapabilecekleriniz hayallerinizle
sınırlıdır.


