 Tünel Yöneltme 2011 Temmuz 0.8.7 

## Özet

Bu sayfada, daha teknik sayfalara, ayrıntılara ve özelliklere verilen
bağlantılarla birlikte I2P tünel terminolojisine ve çalışma şekline
genel bir bakış bulunur.

As briefly explained in the [introduction](), I2P
builds virtual \"tunnels\" - temporary and unidirectional paths through
a sequence of routers. These tunnels are classified as either inbound
tunnels (where everything given to it goes towards the creator of the
tunnel) or outbound tunnels (where the tunnel creator shoves messages
away from them). When Alice wants to send a message to Bob, she will
(typically) send it out one of her existing outbound tunnels with
instructions for that tunnel\'s endpoint to forward it to the gateway
router for one of Bob\'s current inbound tunnels, which in turn passes
it to Bob.

![Alice connecting through her outbound tunnel to Bob via his inbound
tunnel](images/tunnelSending.png "Alice connecting through her outbound tunnel to Bob via his inbound tunnel")

 A: Çıkış Ağ Geçidi (Alice)
 B: Çıkış Katılımcısı
 C: Gidiş Uç Noktası
 D: Geliş Ağ Geçidi
 E: Geliş Katılımcısı
 F: Geliş Uç Noktası (Bob)

## Tünel sözlüğü

- **Tunnel gateway** - the first router in a tunnel. For inbound
 tunnels, this is the one mentioned in the LeaseSet published in the
 [network database](). For outbound tunnels,
 the gateway is the originating router. (e.g. both A and D above)
- **Tünel uç noktası.** Bir tüneldeki son yöneltici. (yukarıdaki C ve
 F gibi)
- **Tünel katılımcısı.** Ağ geçidi veya uç nokta dışında bir tüneldeki
 tüm yönelticiler (yukarıdaki B ve E gibi)
- **n sıçramalı tünel.**Belirli sayıda yönelticiler arası sıçrama
 içeren bir tünel. Örnek:
 - **0 sıçramalı tünel.** Ağ geçidinin de bir uç nokta olduğu bir
 tünel
 - **1 sıçramalı tünel.** Bir ağ geçidinin doğrudan uç nokta ile
 görüştüğü bir tünel
 - **2 (ya da daha fazla) sıçramalı tünel.** En az bir ara tünel
 katılımcısının bulunduğu bir tünel (yukarıdaki şekilde biri
 Alice\'den giden, biri Bob\'a gelen iki tane 2 sıçramalı tünel
 bulunuyor)
- **Tunnel ID** - A [4 byte
 integer](#type_TunnelId) different
 for each hop in a tunnel, and unique among all tunnels on a router.
 Chosen randomly by the tunnel creator.

## Tünel Oluşturma Bilgileri

Routers performing the three roles (gateway, participant, endpoint) are
given different pieces of data in the initial [Tunnel Build
Message]() to accomplish their tasks:

- **Tünel ağ geçidine şunlar iletilir:**
 - **tunnel encryption key** - an [AES private
 key](#type_SessionKey) for
 encrypting messages and instructions to the next hop
 - **tunnel IV key** - an [AES private
 key](#type_SessionKey) for
 double-encrypting the IV to the next hop
 - **reply key** - an [AES public
 key](#type_SessionKey) for
 encrypting the reply to the tunnel build request
 - **Yanıt IV**. Tünel oluşturma isteğinin yanıtını şifreleyen IV
 - **Tünel kodu**. 4 bayt tamsayı (yalnızca geliş ağ geçitleri
 için)
 - **Sonraki sıçrama**. Yoldaki bir sonraki yönelticinin hangisi
 olduğu (bu bir 0 sıçramalı tünel değilse ve ağ geçidi aynı
 zamanda uç nokta değilse)
 - **Sonraki tünel kodu**. Sonraki sıçramanın tünel kodu
- **Tüm ara tünel katılımcılarına şunlar iletilir:**
 - **tunnel encryption key** - an [AES private
 key](#type_SessionKey) for
 encrypting messages and instructions to the next hop
 - **tunnel IV key** - an [AES private
 key](#type_SessionKey) for
 double-encrypting the IV to the next hop
 - **reply key** - an [AES public
 key](#type_SessionKey) for
 encrypting the reply to the tunnel build request
 - **Yanıt IV**. Tünel oluşturma isteğinin yanıtını şifreleyen IV
 - **Tünel kodu**. 4 bayt tamsayı
 - **Sonraki sıçrama**. Yoldaki bir sonraki yönelticinin hangisi
 olduğu
 - **Sonraki tünel kodu**. Sonraki sıçramanın tünel kodu
- **Tünel uç noktasına şunlar iletilir:**
 - **tunnel encryption key** - an [AES private
 key](#type_SessionKey) for
 encrypting messages and instructions to the the endpoint
 (itself)
 - **tunnel IV key** - an [AES private
 key](#type_SessionKey) for
 double-encrypting the IV to the endpoint (itself)
 - **reply key** - an [AES public
 key](#type_SessionKey) for
 encrypting the reply to the tunnel build request (outbound
 endpoints only)
 - **Yanıt IV**. Tünel oluşturma isteğinin yanıtını şifreleyen IV
 (yalnızca gidiş uç noktaları için)
 - **Tünel kodu**. 4 bayt tamsayı (yalnızca gidiş uç noktaları
 için)
 - **Yanıt yönelticisi**. Yanıtın gönderileceği tünelin geliş ağ
 geçidi (yalnızca gidiş uç noktaları için)
 - **Yanıt tüneli kodu**. Yanıt yönelticisinin tünel kimliği
 (yalnızca gidiş uç noktaları için)

Details are in the [tunnel creation
specification]().

## Tünel havuzu

Several tunnels for a particular purpose may be grouped into a \"tunnel
pool\", as described in the [tunnel
specification](#tunnel.pooling). This
provides redundancy and additional bandwidth. The pools used by the
router itself are called \"exploratory tunnels\". The pools used by
applications are called \"client tunnels\".

## Tünel uzunluğu {#length}

As mentioned above, each client requests that their router provide
tunnels to include at least a certain number of hops. The decision as to
how many routers to have in one\'s outbound and inbound tunnels has an
important effect upon the latency, throughput, reliability, and
anonymity provided by I2P - the more peers that messages have to go
through, the longer it takes to get there and the more likely that one
of those routers will fail prematurely. The less routers in a tunnel,
the easier it is for an adversary to mount traffic analysis attacks and
pierce someone\'s anonymity. Tunnel lengths are specified by clients via
[I2CP options](#options). The maximum number of
hops in a tunnel is 7.

### 0 sıçramalı tüneller

Bir tünelde uzak yönelticiler olmadığında, kullanıcının çok temel bir
makul reddedilebilirliği vardır (çünkü kimse onlara ileti gönderen eşin
yalnızca tünelin bir parçası olarak iletmediğine emin değildir). Ancak,
istatistiksel bir analiz saldırısı başlatmak ve belirli bir hedefe
yönelik iletilerin her zaman tek bir ağ geçidi üzerinden gönderildiğini
fark etmek oldukça kolay olacaktır. 0 sıçramalı gidiş tünellerinde
istatistiksel analiz yapmak daha karmaşıktır. Ancak benzer bilgileri
gösterebilir (ancak bir araya getirmek biraz daha zor olacaktır).

### 1 sıçramalı tüneller

With only one remote router in a tunnel, the user has both plausible
deniability and basic anonymity, as long as they are not up against an
internal adversary (as described on [threat
model]()). However, if the adversary ran a
sufficient number of routers such that the single remote router in the
tunnel is often one of those compromised ones, they would be able to
mount the above statistical traffic analysis attack.

### 2 sıçramalı tüneller

Bir tünelde iki ya da daha fazla uzak yöneltici olduğunda, trafik
analizi saldırısını bir araya getirme maliyetleri artar. Bu saldırıyı
yapabilmek için birçok uzak yönelticisinin güvenliğinin ihlal edilmesi
gerekir.

### 3 (ya da daha fazla) sıçramalı tüneller

To reduce the susceptibility to [some attacks](), 3
or more hops are recommended for the highest level of protection.
[Recent studies]() also conclude that more than 3
hops does not provide additional protection.

### Varsayılan tünel uzunlukları

The router uses 2-hop tunnels by default for its exploratory tunnels.
Client tunnel defaults are set by the application, using [I2CP
options](#options). Most applications use 2 or 3
hops as their default.

## Tünel sınaması {#testing}

All tunnels are periodically tested by their creator by sending a
DeliveryStatusMessage out an outbound tunnel and bound for another
inbound tunnel (testing both tunnels at once). If either fails a number
of consecutive tests, it is marked as no longer functional. If it was
used for a client\'s inbound tunnel, a new leaseSet is created. Tunnel
test failures are also reflected in the [capacity rating in the peer
profile](#capacity).

## Tünel oluşturma

Tunnel creation is handled by [garlic
routing]() a Tunnel Build Message to a
router, requesting that they participate in the tunnel (providing them
with all of the appropriate information, as above, along with a
certificate, which right now is a \'null\' cert, but will support
hashcash or other non-free certificates when necessary). That router
forwards the message to the next hop in the tunnel. Details are in the
[tunnel creation specification]().

## Tunnel encryption

Multi-layer encryption is handled by [garlic
encryption]() of tunnel messages. Details
are in the [tunnel specification](). The IV
of each hop is encrypted with a separate key as explained there.

## Gelecekte Yapılacak Çalışmalar

- Sınamaların sayısını sarımsak dişleri ile sarmalamak, bireysel tünel
 katılımcılarını ayrı ayrı sınamak gibi diğer tünel sınama yöntemleri
 kullanılabilir.,
- Varsayılan olarak 3 sıçramalı keşif tünellerine geçiş.
- Uzak gelecekteki bir sürümde, havuz oluşturma, karıştırma ve artık
 oluşturma ayarlarını belirten seçenekler uygulanabilir.
- Uzak gelecekteki bir sürümde, tünelin ömrü boyunca izin verilen
 iletilerin miktarı ve boyutuna ilişkin sınırlamalar uygulanabilir
 (300 iletiden ya da dakikada 1MB boyutundan fazla olamaz gibi).

## Şunlara da bakabilirsiniz

- [Tünel teknik
 özellikleri]()
- [Tünel oluşturma teknik
 özellikleri]()
- [Çift yönlü
 tüneller]()
- [Tünel iletisi teknik
 özellikleri]()
- [Garlic
 yöneltme]()
- [ElGamal/AES+OturumEtiketi]()
- [I2CP
 ayarları](#options)


