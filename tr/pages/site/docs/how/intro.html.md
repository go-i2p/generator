 I2P Nasıl Çalışır
Hafif Bir Giriş 

I2P, güvenli ve anonim iletişimi destekleyen bir ağ oluşturmayı,
dağıtmayı ve sürdürmeyi amaçlayan bir projedir. I2P kullanan kişiler,
anonimlik, güvenilirlik, bant genişliği kullanımı ve gecikme arasındaki
dengeleri kontrol eder. Ağda, sistemin bütünlüğünü, güvenliğini veya
anonimliğini tehlikeye atabilecek şekilde baskı uygulanabilecek hiçbir
merkezi nokta bulunmaz. Ağ, çeşitli saldırılara yanıt olarak devingen
yeniden yapılandırmayı destekler ve kullanılabilir olduğunda ek
kaynaklardan yararlanmak üzere tasarlanmıştır. Tabii ki, ağın tüm
yönleri açık ve ücretsiz olarak kullanılabilir.

Diğer birçok anonimleştirici ağdan farklı olarak, I2P, alıcıyı değil,
bazı iletişimlerin kaynağını gizleyerek veya tam tersi şekilde anonimlik
sağlamaya çalışmaz. I2P, I2P kullanan eşlerin birbirleriyle anonim
olarak iletişim kurmasını sağlayacak şekilde tasarlanmıştır. Hem
gönderici hem de alıcı birbirleri ve üçüncü şahıslar tarafından
tanımlanamaz. Örneğin, bugün hem I2P içi siteler (anonim yayınlamaya /
barındırmaya izin veren) hem de normal internet için HTTP vekil
sunucuları (anonim internet gezinmesine izin veren) vardır. Sunucuları
I2P içinde çalıştırma yeteneği çok önemlidir, çünkü normal İnternet
üzerine bağlanan tüm çıkış vekil sunucularının izlenmesi, devre dışı
bırakılması ve hatta daha fazla kötü niyetli saldırı girişiminde
bulunmak için devralınması olasılığı yüksektir.

The network itself is message oriented - it is essentially a secure and
anonymous IP layer, where messages are addressed to cryptographic keys
(Destinations) and can be significantly larger than IP packets. Some
example uses of the network include \"I2P Sites\" (webservers hosting
normal web applications within I2P), a BitTorrent client (\"I2PSnark\"),
or a distributed data store. With the help of the
[I2PTunnel]() application, we are able to
stream traditional TCP/IP applications over I2P, such as SSH, IRC, a
squid proxy, and even streaming audio. Most people will not use I2P
directly, or even need to know they\'re using it. Instead their view
will be of one of the I2P enabled applications, or perhaps as a little
controller app to turn on and off various proxies to enable the
anonymizing functionality.

An essential part of designing, developing, and testing an anonymizing
network is to define the [threat model](),
since there is no such thing as \"true\" anonymity, just increasingly
expensive costs to identify someone. Briefly, I2P\'s intent is to allow
people to communicate in arbitrarily hostile environments by providing
good anonymity, mixed in with sufficient cover traffic provided by the
activity of people who require less anonymity. This way, some users can
avoid detection by a very powerful adversary, while others will try to
evade a weaker entity, *all on the same network*, where each one\'s
messages are essentially indistinguishable from the others.

## Neden?

There are a multitude of reasons why we need a system to support
anonymous communication, and everyone has their own personal rationale.
There are many [other efforts]() working on
finding ways to provide varying degrees of anonymity to people through
the Internet, but we could not find any that met our needs or threat
model.

## Nasıl?

The network at a glance is made up of a set of nodes (\"routers\") with
a number of unidirectional inbound and outbound virtual paths
(\"tunnels\", as outlined on the [tunnel
routing]() page). Each router is
identified by a cryptographic RouterIdentity which is typically long
lived. These routers communicate with each other through existing
transport mechanisms (TCP, UDP, etc), passing various messages. Client
applications have their own cryptographic identifier (\"Destination\")
which enables it to send and receive messages. These clients can connect
to any router and authorize the temporary allocation (\"lease\") of some
tunnels that will be used for sending and receiving messages through the
network. I2P has its own internal [network
database]() (using a modification of the Kademlia
algorithm) for distributing routing and contact information securely.

::: {.box style="text-align:center;"}
![Ağ topolojisi
örneği](images/net.png "Ağ topolojisi örneği")
:::

Yukarıda, Alice, Bob, Charlie ve Dave, yerel yönelticilerinde tek bir
hedefe sahip yönelticiler işletiyor. Her birinin hedef başına bir çift 2
sıçramalı geliş tüneli vardır (1, 2, 3, 4, 5 ve 6 olarak etiketlenir) ve
bu yönelticinin gidiş tünel havuzunun küçük bir alt kümesi 2 sıçramalı
gidiş tünelleri ile gösterilir. Basit olması için, Charlie\'nin geliş
tünelleri ve Dave\'in gidiş tünelleri ve her yönelticinin gidiş tüneli
havuzunun geri kalanı gösterilmemiştir (tipik olarak bir seferde birkaç
tünelle stoklanmıştır). Alice ve Bob birbirleriyle konuştuğunda, Alice
(pembe) gidiş tünellerinden birinden Bob\'un (yeşil) geliş tünellerinden
(tünel 3 veya 4) birini hedefleyen bir ileti gönderir. Alice, yeni
kiralamalar yapılıp eski kiralamalar sona erdikçe sürekli güncellenen ağ
veri tabanını sorgulayarak iletileri yöneltici üzerinde bu tünellere
doğru göndermeyi bilir.

If Bob wants to reply to Alice, he simply goes through the same
process - send a message out one of his outbound tunnels targeting one
of Alice\'s inbound tunnels (tunnel 1 or 2). To make things easier, most
messages sent between Alice and Bob are
[garlic]() wrapped, bundling the
sender\'s own current lease information so that the recipient can reply
immediately without having to look in the network database for the
current data.

To deal with a wide range of attacks, I2P is fully distributed with no
centralized resources - and hence there are no directory servers keeping
statistics regarding the performance and reliability of routers within
the network. As such, each router must keep and maintain profiles of
various routers and is responsible for selecting appropriate peers to
meet the anonymity, performance, and reliability needs of the users, as
described in the [peer selection]() page.

The network itself makes use of a significant number of [cryptographic
techniques and algorithms]() - a full
laundry list includes 2048bit ElGamal encryption, 256bit AES in CBC mode
with PKCS#5 padding, 1024bit DSA signatures, SHA256 hashes, 2048bit
Diffie-Hellman negotiated connections with station to station
authentication, and [ElGamal /
AES+SessionTag]().

I2P üzerinden gönderilen içerik üç katmanda şifrelenir. Garlic
şifrelemesi (iletinin alıcıya teslim edildiğini doğrulamak için), tünel
şifrelemesi (bir tünelden geçen tüm iletilerin tünel ağ geçidi
tarafından tünel uç noktasına şifrelenmesi için) ve yönelticiler arası
taşıyıcı katmanı şifrelemesi (kısa ömürlü anahtarlarla AES256 kullanan
TCP taşıyıcısı için) kullanılır.

I2P 0.6 sürümünde uçtan uca (I2CP) şifreleme (istemci uygulamasından
sunucu uygulamasına) devre dışı bırakıldı; Alice\'in yönelticisi \"a\"
ile Bob\'un yönelticisi \"h\" arasında uçtan uca (Garlic) şifreleme (I2P
istemci yönelticisinden I2P sunucu yönelticisine) kalır. Terimlerin
farklı kullanımına dikkat edin! A ile h arasındaki tüm veriler uçtan uca
şifrelenir, ancak I2P yöneltici ile uygulamalar arasındaki I2CP
bağlantısı uçtan uca şifrelenmiş değildir! A ve h, Alice ve Bob\'un
yönelticileridir. Aşağıdaki tabloda Alice ve Bob, I2P üzerinde çalışan
uygulamalardır.

::: {.box style="text-align:center;"}
![Uçtan uca katmanlı
şifreleme](images/endToEndEncryption.png "Uçtan uca katmanlı şifreleme")
:::

The specific use of these algorithms are outlined
[elsewhere]().

Güçlü anonimliğe gerek duyan kişilerin ağı kullanmasına izin veren iki
ana mekanizma, açıkça geciktirilmiş Garlic yöneltmeli iletiler ve
iletilerin birleştirilmesi ve karıştırılması için destek içeren daha
kapsamlı tünellerdir. Bunlar şu anda 3.0 sürümü için planlanıyor. Ancak
hiçbir gecikme olmaksızın Garlic yöneltmeli iletiler ve FIFO tünelleri
şu anda yerinde. Ek olarak, 2.0 sürümü, insanların kısıtlanmış rotaların
arkasında (belki de güvenilir eşlerle) kurulmasına ve çalışmasına ve
ayrıca daha esnek ve anonim taşıyıcıların konuşlandırılmasına olanak
sağlayacaktır.

Some questions have been raised with regards to the scalability of I2P,
and reasonably so. There will certainly be more analysis over time, but
peer lookup and integration should be bounded by `O(log(N))` due to the
[network database]()\'s algorithm, while end to
end messages should be `O(1)` (scale free), since messages go out K hops
through the outbound tunnel and another K hops through the inbound
tunnel, with K no longer than 3. The size of the network (N) bears no
impact.

## Ne zaman?

I2P initially began in Feb 2003 as a proposed modification to
[Freenet](http://freenetproject.org) to allow it to use alternate
transports, such as [JMS](), then grew into its own
as an \'anonCommFramework\' in April 2003, turning into I2P in July,
with code being written in earnest starting in August \'03. I2P is
currently under development, following the
[roadmap]().

## Kim tarafından?

We have a small [team]() spread around several
continents, working to advance different aspects of the project. We are
very open to other developers who want to get involved and anyone else
who would like to contribute in other ways, such as critiques, peer
review, testing, writing I2P enabled applications, or documentation. The
entire system is open source - the router and most of the SDK are
outright public domain with some BSD and Cryptix licensed code, while
some applications like I2PTunnel and I2PSnark are GPL. Almost everything
is written in Java (1.5+), though some third party applications are
being written in Python and other languages. The code works on [Sun Java
SE](http://java.com/en/) and other Java Virtual Machines.

## Nerede?

Anyone interested should join us on the IRC channel #i2p-dev (hosted
concurrently on irc.freenode.net, irc.postman.i2p, irc.echelon.i2p,
irc.dg.i2p and irc.oftc.net). There are currently no scheduled
development meetings, however [archives are
available]().

The current source is available in [git]().

## Ek Bilgiler

See [the Index to Technical Documentation]().


