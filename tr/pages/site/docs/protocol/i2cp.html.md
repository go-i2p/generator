 I2CP
2025-04 0.9.66 

I2P istemci iletişim kuralı (I2CP), yöneltici ile ağ üzerinden iletişim
kurmak isteyen herhangi bir istemci arasındaki endişelerin güçlü bir
şekilde ayrılmasını sağlar. Tek bir TCP soketi üzerinden ileti gönderip
alarak güvenli ve asenkron iletişim sağlar. I2CP ile bir istemci
uygulaması, yönelticiye kim olduklarını (\"hedefleri\"), hangi
anonimlik, güvenilirlik ve gecikme sürelerinin değişeceğini ve
iletilerin nereye gönderileceğini söyler. Yöneltici, istemciye herhangi
bir iletinin ne zaman geldiğini bildirmek ve kullanılacak bazı tüneller
için yetki istemek için I2CP iletişim kuralını kullanır.

The protocol itself is implemented in Java, to provide the [Client
SDK](). This SDK is exposed in the i2p.jar package,
which implements the client-side of I2CP. Clients should never need to
access the router.jar package, which contains the router itself and the
router-side of I2CP. There is also a [C library
implementation](). A non-Java client would also
have to implement the [streaming library]()
for TCP-style connections.

Applications can take advantage of the base I2CP plus the
[streaming]() and
[datagram]() libraries by using the [Simple
Anonymous Messaging]() or
[BOB]() protocols, which do not require clients to
deal with any sort of cryptography. Also, clients may access the network
by one of several proxies - HTTP, CONNECT, and SOCKS 4/4a/5.
Alternatively, Java clients may access those libraries in
ministreaming.jar and streaming.jar. So there are several options for
both Java and non-Java applications.

Client-side end-to-end encryption (encrypting the data over the I2CP
connection) was disabled in I2P release 0.6, leaving in place the
[ElGamal/AES end-to-end encryption]() which
is implemented in the router. The only cryptography that client
libraries must still implement is [DSA public/private key
signing](#DSA) for
[LeaseSets](#msg_CreateLeaseSet) and [Session
Configurations](#struct_SessionConfig), and
management of those keys.

Standart bir I2P kurulumunda, 7654 numaralı bağlantı noktası, dış java
istemcileri tarafından yerel yöneltici ile I2CP üzerinden iletişim
kurmak için kullanılır. Varsayılan olarak, yöneltici 127.0.0.1 adresine
bağlanır. 0.0.0.0 adresine bağlanmak için
`i2cp.tcp.bindAllInterfaces=true` gelişmiş yöneltici yapılandırma
seçeneğini ayarlayın ve yönelticiyi yeniden başlatın. Yöneltici ile aynı
JVM üzerindeki istemciler, iletileri bir iç JVM arabirimi üzerinden
doğrudan yönelticiye aktarır.

Some router and client implementations may also support external
connections over SSL, as configured by the i2cp.SSL=true option. While
SSL is not the default, it is strongly recommended for any traffic that
may be exposed to the open Internet. The authorization user/password (if
any), the [Private
Key](#type_PrivateKey) and [Signing
Private Key](#type_SigningPrivateKey)
for the
[Destination](#struct_Destination) are
all transmitted in-the-clear unless SSL is enabled. Some router and
client implementations may also support external connections over domain
sockets.

## I2CP İletişim Kuralı Teknik Özellikleri

Now on the [I2CP Specification page]().

## I2CP Hazırlanması

When a client connects to the router, it first sends a single protocol
version byte (0x2A). Then it sends a [GetDate
Message](#msg_GetDate) and waits for the [SetDate
Message](#msg_SetDate) response. Next, it sends a
[CreateSession Message](#msg_CreateSession)
containing the session configuration. It next awaits a [RequestLeaseSet
Message](#msg_RequestLeaseSet) from the router,
indicating that inbound tunnels have been built, and responds with a
CreateLeaseSetMessage containing the signed LeaseSet. The client may now
initiate or receive connections from other I2P destinations.

## I2CP Ayarları {#options}

### Yöneltici Tarafı Ayarları

The following options are traditionally passed to the router via a
[SessionConfig](#struct_SessionConfig) contained
in a [CreateSession Message](#msg_CreateSession)
or a [ReconfigureSession
Message](#msg_ReconfigureSession).

Yöneltici Tarafı Ayarları

Seçenek

Yayınlanma Tarihi

Önerilen Argümanlar

İzin Verilen Aralık

Varsayılan

Açıklama

clientMessageTimeout

 

 

8\*1000 - 120\*1000

60\*1000

Gönderilen tüm iletiler için zaman aşımı (ms). Kullanılmıyor. Tek tek
ileti ayarları için iletişim kuralının teknik özelliklerine
bakabilirsiniz.

crypto.lowTagThreshold

0.9.2

 

1-128

30

Daha fazlası gönderilmeden önce iletilecek en az sayıda ElGamal/AES
oturum etiketi. Önerilen: Yaklaşık olarak tagdsToSend \* 2/3

crypto.ratchet.inboundTags

0.9.47

 

1-?

160

Inbound tag window for ECIES-X25519-AEAD-Ratchet. Local inbound tagset
size. See proposal 144.

crypto.ratchet.outboundTags

0.9.47

 

1-?

160

Outbound tag window for ECIES-X25519-AEAD-Ratchet. Advisory to send to
the far-end in the options block. See proposal 144.

crypto.tagsToSend

0.9.2

 

1-128

40

Bir seferde gönderilecek ElGamal/AES oturum etiketlerinin sayısı.
İstemci çiftinin bant genişliği nispeten düşük olan istemciler için
(IRC, bazı UDP uygulamaları), bu değer daha düşük ayarlanabilir.

explicitPeers

 

 

 

null

Tüneller oluşturulacak eşlerin Base 64 karmalarının virgül ile ayrılmış
listesi. Yalnızca hata ayıklama için

i2cp.dontPublishLeaseSet

 

true, false

 

false

Genellikle istemciler için true, sunucular için false olarak
ayarlanmalıdır

i2cp.fastReceive

0.9.4

 

true, false

false

True olarak ayarlandığında, yöneltici bir MessageStatus göndermek ve bir
ReceiveMessageBegin beklemek yerine MessagePayload gönderir.

i2cp.leaseSetAuthType

0.9.41

0

0-2

0

The type of authentication for encrypted LS2. 0 for no per-client
authentication (the default); 1 for DH per-client authentication; 2 for
PSK per-client authentication. See proposal 123.

i2cp.leaseSetEncType

0.9.38

4,0

0-65535,\...

0

The encryption type to be used, as of 0.9.38. Interpreted client-side,
but also passed to the router in the SessionConfig, to declare intent
and check support. As of 0.9.39, may be comma-separated values for
multiple types. See PublicKey in common strutures spec for values. See
proposals 123, 144, and 145.

i2cp.leaseSetOfflineExpiration

0.9.38

 

 

 

The expiration of the offline signature, 4 bytes, seconds since the
epoch. See proposal 123.

i2cp.leaseSetOfflineSignature

0.9.38

 

 

 

The base 64 of the offline signature. See proposal 123.

i2cp.leaseSetPrivKey

0.9.41

 

 

 

A base 64 X25519 private key for the router to use to decrypt the
encrypted LS2 locally, only if per-client authentication is enabled.
Optionally preceded by the key type and \':\'. Only \"ECIES_X25519:\" is
supported, which is the default. See proposal 123. Do not confuse with
i2cp.leaseSetPrivateKey which is for the leaseset encryption keys.

i2cp.leaseSetSecret

0.9.39

 

 

\"\"

Base 64 encoded UTF-8 secret used to blind the leaseset address. See
proposal 123.

i2cp.leaseSetTransientPublicKey

0.9.38

 

 

 

\[type:\]b64 The base 64 of the transient private key, prefixed by an
optional sig type number or name, default DSA_SHA1. See proposal 123.

i2cp.leaseSetType

0.9.38

1,3,5,7

1-255

1

The type of leaseset to be sent in the CreateLeaseSet2 Message.
Interpreted client-side, but also passed to the router in the
SessionConfig, to declare intent and check support. See proposal 123.

i2cp.messageReliability

 

 

BestEffort, None

BestEffort

Garantili olarak devre dışı bırakılmıştır. 0.8.1 sürümünde None olarak
ayarlanmıştır. Streaming kitaplığı varsayılanı 0.8.1 sürümünden
başlayarak, istemci tarafı varsayılanı 0.9.4 sürümünden başlayarak None
olarak ayarlanmıştır.

i2cp.password

0.8.2

string

 

 

Kimlik doğrulaması için, yöneltici tarafından isteniyorsa. İstemci bir
yönelticiyle aynı JVM üzerinde çalışıyorsa bu seçenek gerekli değildir.
Uyarı - SSL (i2cp.SSL=true) kullanılmadığı sürece kullanıcı adı ve
parola yönelticiye düz metin olarak gönderilir. Kimlik doğrulaması
yalnızca SSL kullanılırken önerilir.

i2cp.username

0.8.2

string

 

 

inbound.allowZeroHop

 

true, false

 

true

Sıfır sıçramalı geliş tüneline izin veriliyorsa

outbound.allowZeroHop

 

true, false

 

true

Sıfır sıçramalı gidiş tüneline izin veriliyorsa

inbound.backupQuantity

 

İki yönelticinin aynı tünelde olmaması gerekip gerekmediğini belirlemek
için eşleştirilecek IP bayt sayısı. Devre dışı bırakmak için 0 yazın.

outbound.IPRestriction

 

İki yönelticinin aynı tünelde olmaması gerekip gerekmediğini belirlemek
için eşleştirilecek IP bayt sayısı. Devre dışı bırakmak için 0 yazın.

inbound.length

 

Geliş tünellerinin uzunluğuna eklenecek veya çıkarılacak rastgele
miktar. Pozitif bir sayı x, 0 ile x arasında rastgele bir miktar eklemek
anlamına gelir. Negatif bir sayı -x, -x ile x arasında rastgele bir
miktar eklemek anlamına gelir. Yöneltici, tünelin toplam uzunluğunu 0
ile 7 (dahil) arasında sınırlar. 0.7.6 sürümünden önce varsayılan
varsyans 1 idi.

outbound.lengthVariance

 

Gidiş tünellerinin uzunluğuna eklenecek veya çıkarılacak rastgele
miktar. Pozitif bir sayı x, 0 ile x arasında rastgele bir miktar eklemek
anlamına gelir. Negatif bir sayı -x, -x ile x arasında rastgele bir
miktar eklemek anlamına gelir. Yöneltici, tünelin toplam uzunluğunu 0
ile 7 (dahil) arasında sınırlar. 0.7.6 sürümünden önce varsayılan
varsyans 1 idi.

inbound.nickname

 

string

 

 

Tünelin adı. Genellikle varsayılan olarak hedefin Base64 karma değerinin
ilk birkaç karakterini kullanacak olan routerconsole değerinde
kullanılır.

outbound.nickname

 

string

 

 

Tünelin adı. inbound.nickname ayarlanmadıkça genellikle yok sayılır.

outbound.priority

0.9.4

Giden iletiler için öncelik ayarlaması. Daha yüksek değer, daha yüksek
önceliklidir.

inbound.quantity

 

Geliş tüneli sayısı. 0.9 sürümünde sınır 6 yerine 16 yapıldı. Ancak 6
üzerindeki sayılar eski sürümlerle uyumlu değildir.

outbound.quantity

 

Yeniden başlatmalar arasında tutarlı eş sıralaması için kullanılır.

outbound.randomKey

0.9.17

Base 64 encoding of 32 random bytes

 

 

inbound.\*

 

 

 

 

Ön eki \"inbound\" olan diğer seçenekler. geliş tüneli havuzu
ayarlarının \"bilinmeyen seçenekler\" özelliklerinde saklanır.

outbound.\*

 

 

 

 

Ön eki \"outbound\" olan diğer seçenekler. gidiş tüneli havuzu
ayarlarının \"bilinmeyen seçenekler\" özelliklerinde saklanır.

shouldBundleReplyInfo

0.9.2

true, false

 

true

Bir yanıt \"Kiralama kümesinin\" (LeaseSet) paketlenmesini devre dışı
bırakmak için false olarak ayarlayın. \"Kiralama kümelerini\"
(LeaseSets) yayınlamayan istemcilerin, herhangi bir yanıt verebilmesi
için bu seçeneğin \"True\" olması gerekir. Ayrıca uzun bağlantı süreleri
olan birden çok barındırma sağlayan sunucular için de \"True\" ayarının
kullanılması önerilir.

\"False\" olarak ayarlamak, özellikle istemci çok sayıda geliş tüneli
(kiralama) olacak şekilde yapılandırılmışsa, gidiş bant genişliğinden
önemli ölçüde kazanım sağlayabilir. Yanıtlar hala gerekliyse, bu, bant
genişliği yükünü uzak uçtaki istemciye ve otomatik doldurma işlemine
kaydırabilir. \"False\" ayarının uygun olabileceği birkaç durum vardır:

- Yanıt gerekmeyen tek yönlü iletişim olması durumunda
- \"Kiralama kümesi\" (LeaseSet) yayınlandığında ve daha yüksek yanıt
 gecikmesi kabul edilebildiğinde
- \"Kiralama kümesi\" (LeaseSet) yayınlandığında, istemci bir
 \"sunucu\" iken, tüm bağlantılar geliştir yani açıkça bağlantı
 kurulan uzak uç hedefinde \"Kiralama kümesi\" (LeaseSet) zaten
 vardır. Bağlantılar ya kısadır ya da uzun ömürlü bir bağlantıdaki
 gecikmenin geçici olarak artması, diğer ucun süre bitiminden sonra
 \"Kiralama kümesini\" yeniden alması kabul edilebilir. HTTP
 sunucuları bu gereksinimlere uyabilir.

Not: Büyük miktar, uzunluk veya varyans ayarları önemli başarım veya
güvenilirlik sorunlarına neden olabilir.

Note: As of release 0.7.7, option names and values must use UTF-8
encoding. This is primarily useful for nicknames. Prior to that release,
options with multi-byte characters were corrupted. Since options are
encoded in a [Mapping](#type_Mapping),
all option names and values are limited to 255 bytes (not characters)
maximum.

### İstemci Tarafı Ayarları

Aşağıdaki seçenekler istemci tarafında yorumlanır ve
I2PClient.createSession() çağrısı ile I2PSession üzerine aktarılırsa
yorumlanır. Streaming kitaplığı da bu seçenekleri I2CP üzerine
iletmelidir. Diğer uygulamaların varsayılanları farklı olabilir.

İstemci Tarafı Ayarları

Seçenek

Yayınlanma Tarihi

Önerilen Argümanlar

İzin Verilen Aralık

Varsayılan

Açıklama

i2cp.closeIdleTime

0.7.1

1800000

True olarak ayarlandığında, yöneltici bir MessageStatus göndermek ve bir
ReceiveMessageBegin beklemek yerine MessagePayload gönderir.

i2cp.gzip

0.6.5

true, false

 

true

Gidiş verilerini gzip ile sıkıştır

i2cp.leaseSetAuthType

0.9.41

0

0-2

0

The type of authentication for encrypted LS2. 0 for no per-client
authentication (the default); 1 for DH per-client authentication; 2 for
PSK per-client authentication. See proposal 123.

i2cp.leaseSetBlindedType

0.9.39

 

0-65535

See prop. 123

The sig type of the blinded key for encrypted LS2. Default depends on
the destination sig type. See proposal 123.

i2cp.leaseSetClient.dh.nnn

0.9.41

b64name:b64pubkey

 

 

The base 64 of the client name (ignored, UI use only), followed by a
\':\', followed by the base 64 of the public key to use for DH
per-client auth. nnn starts with 0 See proposal 123.

i2cp.leaseSetClient.psk.nnn

0.9.41

b64name:b64privkey

 

 

The base 64 of the client name (ignored, UI use only), followed by a
\':\', followed by the base 64 of the private key to use for PSK
per-client auth. nnn starts with 0. See proposal 123.

i2cp.leaseSetEncType

0.9.38

0

0-65535,\...

0

The encryption type to be used, as of 0.9.38. Interpreted client-side,
but also passed to the router in the SessionConfig, to declare intent
and check support. As of 0.9.39, may be comma-separated values for
multiple types. See also i2cp.leaseSetPrivateKey. See PublicKey in
common strutures spec for values. See proposals 123, 144, and 145.

i2cp.leaseSetKey

0.7.1

 

 

 

\"Şifrelenmiş kiralama kümeleri\" (EncryptedLeaseSets) için. Base 64
"Oturum anahtarı" (sessionKey) (44 karakter)

i2cp.leaseSetOption.nnn

0.9.66

srvKey=srvValue

 

 

A service record to be placed in the LeaseSet2 options. Example:
\"\_smtp.\_tcp=1 86400 0 0 25 \...b32.i2p\" nnn starts with 0. See
proposal 167.

i2cp.leaseSetPrivateKey

0.9.18

 

 

 

Şifreleme için Base 64 kişisel anahtarı. İsteğe bağlı olarak, şifreleme
türü adı veya numarası ve \':\' ile başlar. LS1 için yalnızca bir
anahtar desteklenir ve yalnızca varsayılan olan \"0:\" veya
\"ELGAMAL_2048:\" desteklenir. 0.9.39 sürümünden başlayarak, LS2 için
birden çok anahtar virgül ile ayrılmış olabilir ve her bir anahtarın
farklı bir şifreleme türü olması gerekir. I2CP, kişisel anahtardan
herkese açık anahtarı üretecektir. Yeniden başlatmalar arasında kalıcı
\"Kiralama kümesi\" (LeaseSet) anahtarları için kullanın. 123, 144 ve
145 numaralı önerilere bakın. Ayrıca i2cp.leaseSetEncType bilgilerine
bakabilirsiniz. Do not confuse with i2cp.leaseSetPrivKey which is for
encrypted LS2.

i2cp.leaseSetSecret

0.9.39

 

 

\"\"

Base 64 encoded UTF-8 secret used to blind the leaseset address. See
proposal 123.

i2cp.leaseSetSigningPrivateKey

0.9.18

 

 

 

İmzalar için Base 64 kişisel anahtarı. İsteğe bağlı olarak önce anahtar
türü ve \':\' gelir. DSA_SHA1 varsayılandır. Anahtar türü, hedefteki
imza türüyle eşleşmelidir. I2CP, kişisel anahtardan herkese açık
anahtarı üretecektir. Yeniden başlatmalar arasında kalıcı \"Kiralama
kümesi\" (LeaseSet) anahtarları için kullanın.

i2cp.leaseSetType

0.9.38

1,3,5,7

1-255

1

The type of leaseset to be sent in the CreateLeaseSet2 Message.
Interpreted client-side, but also passed to the router in the
SessionConfig, to declare intent and check support. See proposal 123.

i2cp.messageReliability

 

 

BestEffort, None

None

Guaranteed devre dışıdır; 0.8.1 sürümünde None eklenmiştir. 0.9.4
sürümünde None varsayılan değer olmuştur.

i2cp.reduceIdleTime

0.7.1

1200000

Yönelticiye SSL kullanarak bağlanın. İstemci bir yöneltici ile aynı JVM
üzerinde çalışıyorsa bu seçenek yok sayılır ve istemci bu yönelticiye
içeriden bağlanır.

i2cp.tcp.host

 

 

 

127.0.0.1

Yöneltici sunucu adı. İstemci bir yöneltici ile aynı JVM üzerinde
çalışıyorsa bu seçenek yok sayılır ve istemci bu yönelticiye içeriden
bağlanır.

i2cp.tcp.port

 

 

1-65535

7654

Yöneltici I2CP bağlantı noktası. İstemci bir yöneltici ile aynı JVM
üzerinde çalışıyorsa bu seçenek yok sayılır ve istemci bu yönelticiye
içeriden bağlanır.

Not: Sayılarla birlikte tüm bağımsız değişkenler dizgedir. True/false
değerleri, büyük/küçük harfe duyarlı olmayan dizgelerdir. Büyük/küçük
harfe duyarlı olmayan \"true\" dışındaki her şey false olarak
yorumlanır. Tüm seçenek adları büyük/küçük harfe duyarlıdır.

## I2CP Yük Verileri Biçimi ve Çoklama {#format}

The end-to-end messages handled by I2CP (i.e. the data sent by the
client in a [SendMessageMessage](#msg_SendMessage)
and received by the client in a
[MessagePayloadMessage](#msg_MessagePayload)) are
gzipped with a standard 10-byte gzip header beginning with 0x1F 0x8B
0x08 as specified by [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt). As
of release 0.7.1, I2P uses ignored portions of the gzip header to
include protocol, from-port, and to-port information, thus supporting
streaming and datagrams on the same destination, and allowing
query/response using datagrams to work reliably in the presence of
multiple channels.

gzip işlevi tamamen kapatılamaz. Ancak i2cp.gzip=false ayarı, gzip efor
ayarını 0 değerine döndürür, bu da biraz işlemci kazanımı sağlayabilir.
Implementations may select different gzip efforts on a per-socket or
per-message basis, depending on an assessment of the compressibility of
the contents. Due to the compressibility of destination padding
implemented in API 0.9.57 (proposal 161), compression of the streaming
SYN packets in each direction, and of repliable datagrams, is
recommended even if the payload is not compressible. Implementations may
wish to write a trivial gzip/gunzip function for a gzip effort of 0,
which will provide large efficiency gains over a gzip library for this
case.

Bayt

İçerik

0-2

Gzip üst bilgisi 0x1F 0x8B 0x08

3

Gzip işaretleri

4-5

I2P kaynak bağlantı noktası (gzip mtime)

6-7

I2P hedefi bağlantı noktası (gzip mtime)

8

Gzip xflags (set to 2 to be indistinguishable from the Java
implementation)

9

I2P İletişim Kuralı (6 = Streaming, 17 = Veri şeması, 18 = Ham veri
şemaları) (Gzip OS)

Note: I2P protocol numbers 224-254 are reserved for experimental
protocols. I2P protocol number 255 is reserved for future expansion.

Veri bütünlüğü, standart gzip CRC-32 kullanılarak [RFC
1952](http://www.ietf.org/rfc/rfc1952.txt) ile belirtildiği şekilde
şöyle doğrulanır:

## Important Differences from Standard IP

I2CP ports are for I2P sockets and datagrams. They are unrelated to your
local sockets or ports. Because I2P did not support ports and protocol
numbers prior to release 0.7.1, ports and protocol numbers are somewhat
different from that in standard IP, for backward compatibility:

- Port 0 is valid and has special meaning.
- Ports 1-1023 are not special or privileged.
- Servers listen on port 0 by default, which means \"all ports\".
- Clients send to port 0 by default, which means \"any port\".
- Clients send from port 0 by default, which means \"unspecified\".
- Servers may have a service listening on port 0 and other services
 listening on higher ports. If so, the port 0 service is the default,
 and will be connected to if the incoming socket or datagram port
 does not match another service.
- Most I2P destinations only have one service running on them, so you
 may use the defaults, and ignore I2CP port configuration.
- Protocol 0 is valid and means \"any protocol\". However, this is not
 recommended, and probably will not work. Streaming requires that the
 protocol number is set to 6.
- Streaming sockets are tracked by an internal connection ID.
 Therefore, there is no requirement that the 5-tuple of
 dest:port:dest:port:protocol be unique. For example, there may be
 multiple sockets with the same ports between two destinations.
 Clients do not need to pick a \"free port\" for an outbound
 connection.

## Gelecekte Yapılacak Çalışmalar {#future}

- Geçerli kimlik doğrulama yöntemi, karma şifreleri kullanacak şekilde
 değiştirilebilir.
- Kişisel anahtarların imzalanması, kiralama kümesi oluşturma
 iletisinde yapılır. Zorunlu değildir. Geri çekme özelliği
 eklenmemiştir. Rastgele verilerle değiştirilmeli veya
 kaldırılmalıdır.
- Some improvements may be able to use messages previously defined but
 not implemented. For reference, here is the [I2CP Protocol
 Specification Version 0.9]() (PDF) dated
 August 28, 2003. That document also references the [Common Data
 Structures Specification Version 0.9]().

## See Also {#links}

[C library implementation](http://git.repo.i2p/w/libi2cp.git) 
