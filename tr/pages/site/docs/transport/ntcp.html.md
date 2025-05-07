 NTCP (NIO temelli
TCP) 2021-10 0.9.52 

DEPRECATED, NO LONGER SUPPORTED. Disabled by default as of 0.9.40
2019-05. Support removed as of 0.9.50 2021-05. Replaced by
[NTCP2](). NTCP is a Java NIO-based transport
introduced in I2P release 0.6.1.22. Java NIO (new I/O) does not suffer
from the 1 thread per connection issues of the old TCP transport.
NTCP-over-IPv6 is supported as of version 0.9.8.

Varsayılan olarak, NTCP, SSU tarafından otomatik olarak algılanan IP
adresi ve bağlantı noktasını kullanır. config.jsp üzerinde
etkinleştirildiğinde, SSU, dış adres değiştiğinde veya güvenlik duvarı
durumu değiştiğinde NTCP katmanını bilgilendirir ya da yeniden başlatır.
Artık durağan bir IP adresi ya da dyndns hizmeti olmadan gelen TCP
bağlantısını etkinleştirebilirsiniz.

I2P içindeki NTCP kodu, güvenilir aktarım için temeldeki Java TCP
taşıyıcısını kullandığından görece hafiftir (SSU kodunun 1/4
boyutundadır).

## [Yöneltici Adresi Teknik Özellikleri]{#ra}

Ağ veri tabanında aşağıdaki özellikler depolanır.

- **Transport name:** NTCP
- **host:** IP (IPv4 or IPv6). Shortened IPv6 address (with \"::\") is
 allowed. Host names were previously allowed, but are deprecated as
 of release 0.9.32. See proposal 141.
- **port:** 1024 - 65535

## NTCP İletişim Kuralı Teknik Özellikleri

### Standart İleti Biçimi

Bağlantının kuruluşundan sonra, NTCP taşıyıcısı basit bir sağlama
toplamı ile bireysel I2NP iletileri gönderir. Şifrelenmemiş ileti
aşağıdaki gibi kodlanmıştır:


+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+
\| sizeof(data) \| \| +\-\-\-\-\-\--+\-\-\-\-\-\--+ + \| data \| \~ \~
\| \| + +\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+ \| \| padding
+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+
\| Adler checksum of sz+data+pad \|
+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+


Veriler daha sonra AES/256/CBC ile şifrelenir. Şifreleme için oturum
anahtarı, bağlantı kuruluşu sırasında görüşülür (Diffie-Hellman 2048 bit
kullanılarak). İki yöneltici arasındaki bağlantının kuruluşu,
EstablishState sınıfında uygulanır ve ayrıntıları aşağıda verilmiştir.
AES/256/CBC şifrelemesi için IV, önceki şifrelenmiş iletinin son 16
baytıdır.

Toplam ileti uzunluğunu (altı boyut ve sağlama toplamı baytı dahil)
16\'nın katına getirmek için 0-15 bayt dolgu eklenmesi gerekir. En büyük
ileti boyutu şu anda 16 KB olabilir. Bu nedenle en büyük veri boyutu şu
anda 16 KB - 6 veya 16378 bayttır. En küçük veri boyutu 1 olabilir.

### Zaman Eşitleme İleti Biçimi

Özel bir durum, sizeof(data) değerinin 0 olduğu bir üst veri iletisidir.
Bu durumda, şifrelenmemiş ileti şu şekilde kodlanır:


+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+
\| 0 \| timestamp in seconds \| uninterpreted
+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+
uninterpreted \| Adler checksum of bytes 0-11 \|
+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+\-\-\-\-\-\--+


Toplam uzunluk: 16 bayt. Zaman eşitleme iletisi yaklaşık 15 dakikalık
aralıklarla gönderilir. İleti standart iletiler gibi şifrelenir.

### Sağlamalar

The standard and time sync messages use the Adler-32 checksum as defined
in the [ZLIB Specification]().

### Boşta Bekleme Zaman Aşımı

Boşta bekleme zaman aşımı ve bağlantı kapatmayı, her uç nokta kendi
belirler ve değişiklik gösterebilir. Geçerli uygulamada, bağlantı sayısı
yapılandırılan en fazla değere yaklaştıkça zaman aşımı azaltılır ve
bağlantı sayısı düşük olduğunda zaman aşımı artırılır. Önerilen en az
zaman aşımı iki dakika ve üzerindedir. Önerilen en fazla zaman aşımı on
dakika ve üzerindedir.

### \"Yöneltici bilgileri\" (RouterInfo) alış verişi

Bağlantının kuruluşundan sonra ve daha sonra her 30-60 dakikada bir, iki
yöneltici genellikle bir \"Veri tabanı kaydetme iletisi\"
(DatabaseStoreMessage) kullanarak \"Yöneltici bilgileri\" (RouterInfo)
alış verişi yapmalıdır. Ancak, yinelenen bir ileti göndermemek için
Alice ilk kuyruğa alınan iletinin bir \"Veri tabanı kaydetme iletisi\"
(DatabaseStoreMessage) olup olmadığını denetlemelidir. Bu durum
genellikle bir otomatik doldurma yönelticisi ile bağlantı kurulurken
geçerlidir.

### Bağlantı Kuruluşu Sıralaması

Kurulum durumunda, Diffie-Hellman anahtar ve imza alış verişi için 4
aşamalı bir ileti dizisi kullanılır. İlk iki iletide 2048 bit Diffie
Hellman alış verişi bulunur. Ardından, bağlantıyı doğrulamak için kritik
verilerin imzaları alınıp verilir.

 Alice contacts Bob
========================================================= X+(H(X) xor
Bob.identHash)\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--Y+E(H(X+Y)+tsB+padding,
sk, Y\[239:255\])
E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk,
hX_xor_Bob.identHash\[16:31\])\-\--\>
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--E(S(X+Y+Alice.identHash+tsA+tsB)+padding,
sk, prev) 


 İşaret:
 X, Y: 256 bayt Diffie-Hellman herkese açık anahtarları
 H(): 32 byte SHA256 Hash
 E(data, session key, IV): AES256 Encrypt
 S(): Signature
 tsA, tsB: zaman damgaları (4 bayt, epoch sonrası saniye)
 sk: 32 bayt oturum anahtarı
 sz: Alice'in 2 bayt boyutunda kimliği izler

#### Diffie-Hellman anahtar alış verişi {#DH}

The initial 2048-bit DH key exchange uses the same shared prime (p) and
generator (g) as that used for I2P\'s [ElGamal
encryption](#elgamal).

Diffie-Hellman anahtar alış verişi, aşağıda açıklanan birkaç adımdan
oluşur. Bu adımlar ve I2P yönelticileri arasında gönderilen iletiler
arasındaki eşleme kalın olarak işaretlenmiştir.

1. Alice gizli bir x tamsayısı üretir. Ardından şunu hesaplamayı yapar:
 `X = g^x mod p`.
2. Alice, Bob tarafına X değerini gönderir **(1. ileti)**.
3. Bob gizli bir y tamsayısı üretir. Ardından şu hesaplamayı yapar:
 `Y = g^y mod p`.
4. Bob, Alice tarafına Y değerini gönderir **(2. ileti)**.
5. Alice oturum anahtarını hesaplar `sessionKey = Y^x mod p`.
6. Bob oturum anahtarını hesaplar `sessionKey = X^y mod p`.
7. Artık Alice ve Bob paylaşılan bir oturum anahtarına sahiptir
 `sessionKey = g^(x*y) mod p`.

The sessionKey is then used to exchange identities in **Message 3** and
**Message 4**. The exponent (x and y) length for the DH exchange is
documented on the [cryptography
page](#exponent).

#### Session Key Details

The 32-byte session key is created as follows:

1. Take the exchanged DH key, represented as a positive minimal-length
 BigInteger byte array (two\'s complement big-endian)
2. If the most significant bit is 1 (i.e. array\[0\] & 0x80 != 0),
 prepend a 0x00 byte, as in Java\'s BigInteger.toByteArray()
 representation
3. If that byte array is greater than or equal to 32 bytes, use the
 first (most significant) 32 bytes
4. If that byte array is less than 32 bytes, append 0x00 bytes to
 extend to 32 bytes. *(vanishingly unlikely)*

#### 1. ileti (oturum isteği)

This is the DH request. Alice already has Bob\'s [Router
Identity](#struct_RouterIdentity), IP
address, and port, as contained in his [Router
Info](#struct_RouterInfo), which was
published to the [network database](). Alice
sends Bob:

 X+(H(X) xor
Bob.identHash)\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\>
Boyut: 288 bytes 

İçerik:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| X,
as calculated from DH \| + + \| \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| HXxorHI \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ X ::
Diffie-Hellman tarafından sağlanan 256 bayt X HXxorHI :: SHA256
Karması(X) xor SHA256 Karması(Bob\'un \`Yöneltici Kimliği\`
(RouterIdentity)) (32 bytes) 

**Notlar:**

- Bob kendi yöneltici karmasını kullanarak HXxorHI verisini doğrular.
 Doğrulama yapılamazsa, Alice yanlış yönelticiye bağlanmıştır ve Bob
 bağlantıyı keser.

#### 2. ileti (oturum oluşturuldu)

Bu Diffie-Hellman yanıtıdır. Bob, Alice\'e şunu gönderir:


\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--Y+E(H(X+Y)+tsB+padding,
sk, Y\[239:255\]) Boyut: 304 bytes 

Şifrelenmemiş İçerik


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| Y
as calculated from DH \| + + \| \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| HXY \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| tsB
\| padding \| +\-\-\--+\-\-\--+\-\-\--+\-\-\--+ + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ Y ::
Diffie-Hellman tarafından sağlanan 256 bayt Y HXY :: SHA256 Karması(X, Y
ile birleştirilir) (32 bytes) tsB :: 4 bayt zaman damgası (epoch sonrası
geçen saniye) padding :: 12 baytlık rastgele veriler 

Şifrelenmiş İçerik:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| Y
as calculated from DH \| + + \| \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| encrypted data \| + + \| \| + + \| \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 


 Y: Diffie-Hellman tarafından sağlanan 256 bayt Y

 encrypted data: 48 bytes AES encrypted using the DH session key and
 the last 16 bytes of Y as the IV

**Notlar:**

- Alice may drop the connection if the clock skew with
 Bob is too high as calculated using tsB.

#### 3. ileti (A oturum onayı)

Bu iletide, Alice\'in yöneltici kimliği ve kritik verilerin imzası
bulunur. Alice Bob\'a şunu gönderir:


E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk,
hX_xor_Bob.identHash\[16:31\])\-\--\> Boyut: 448 bytes (typ. for 387
byte identity and DSA signature), see notes below 

Şifrelenmemiş İçerik


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| sz
\| Alice\'s Router Identity \| +\-\-\--+\-\-\--+ + \| \| \~ . . . \~ \|
\| + +\-\-\--+\-\-\--+\-\-\--+ \| \| tsA
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
padding \| +\-\-\--+ + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| signature \| + + \| \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ sz ::
Alice\'in izlenecek yöneltici kimliği 2 bayt boyutunda (387+) ident ::
Alice\'in 387+ bayt \`Yöneltici kimliği\` (RouterIdentity) tsA :: 4 bayt
zaman damgası (epoch sonrası geçen saniye) padding :: 0-15 baytlık
rastgele veriler signature :: Aşağıdaki birleştirilmiş verilerin
\`İmzası\`: X, Y, Bob\'un \`Yöneltici kimliği\` (RouterIdentity), tsA,
tsB. Alice, iletiyi \`Yöneltici kimliği\` (RouterIdentity) içindeki
\`SigningPublicKey\` ile ilişkili \`SigningPrivateKey\` ile imzalar. 

Şifrelenmiş İçerik:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| encrypted data \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 


 encrypted data: 448 bytes AES encrypted using the DH session key and
 the last 16 bytes of HXxorHI (i.e., the last 16 bytes of message #1) as the IV
 448 is the typical length, but it could be longer, see below.

**Notlar:**

- Bob imzayı doğrular ve başarısızlık durumunda bağlantıyı keser.
- Alice ile tsA kullanılarak hesaplanan saat farkı çok yüksekse Bob
 bağlantıyı kesebilir.
- Alice, bu iletinin şifrelenmiş içeriğinin son 16 baytını bir sonraki
 ileti için IV olarak kullanır.
- Through release 0.9.15, the router identity was always 387 bytes,
 the signature was always a 40 byte DSA signature, and the padding
 was always 15 bytes. As of release 0.9.16, the router identity may
 be longer than 387 bytes, and the signature type and length are
 implied by the type of the [Signing Public
 Key](#type_SigningPublicKey)
 in Alice\'s [Router
 Identity](#struct_RouterIdentity).
 The padding is as necessary to a multiple of 16 bytes for the entire
 unencrypted contents.
- The total length of the message cannot be determined without
 partially decrypting it to read the Router Identity. As the minimum
 length of the Router Identity is 387 bytes, and the minimum
 Signature length is 40 (for DSA), the minimum total message size is
 2 + 387 + 4 + (signature length) + (padding to 16 bytes), or 2 +
 387 + 4 + 40 + 15 = 448 for DSA. The receiver could read that
 minimum amount before decrypting to determine the actual Router
 Identity length. For small Certificates in the Router Identity, that
 will probably be the entire message, and there will not be any more
 bytes in the message to require an additional decryption operation.

#### 4. ileti (B oturum onayı)

Bu ileti, kritik verilerin imzasıdır. Bob, Alice\'e şunu gönderir:

 \*
\<\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--E(S(X+Y+Alice.identHash+tsA+tsB)+padding,
sk, prev) Boyut: 48 bytes (typ. for DSA signature), see notes below 

Şifrelenmemiş İçerik


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| signature \| + + \| \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
padding \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+
signature :: Aşağıdaki birleştirilmiş verilerin \`İmzası\`: X, Y,
Alice\'in \`Yöneltici Kimliği\`, tsA, tsB. Bob, iletiyi \`Yöneltici
Kimliğindeki\` \`SigningPublicKey\` ile ilişkili \`SigningPrivateKey\`
ile imzalar. padding :: 0-15 baytlık rastgele veriler 

Şifrelenmiş İçerik:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| encrypted data \| \~ . . . \~ \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 


 encrypted data: Data AES encrypted using the DH session key and
 the last 16 bytes of the encrypted contents of message #2 as the IV
 48 bytes for a DSA signature, may vary for other signature types

**Notes:**

- Alice imzayı doğrular ve başarısızlık durumunda bağlantıyı keser.
- Bob, bu iletinin şifrelenmiş içeriğinin son 16 baytını bir sonraki
 ileti için IV olarak kullanır.
- Through release 0.9.15, the signature was always a 40 byte DSA
 signature and the padding was always 8 bytes. As of release 0.9.16,
 the signature type and length are implied by the type of the
 [Signing Public
 Key](#type_SigningPublicKey)
 in Bob\'s [Router
 Identity](#struct_RouterIdentity).
 The padding is as necessary to a multiple of 16 bytes for the entire
 unencrypted contents.

#### Bağlantı Kuruluşundan Sonra

Bağlantı kurulur ve standart veya zaman eşitleme iletileri alınıp
verilebilir. Sonraki tüm iletiler anlaşmalı Diffie-Hellman oturum
anahtarı kullanılarak AES ile şifrelenir. Alice, bir sonraki IV olarak
3. iletinin şifrelenmiş içeriğinin son 16 baytını kullanır. Bob, 4.
iletinin şifrelenmiş içeriğinin son 16 baytını sonraki \"Başlatma
vektörü\" (IV) olarak kullanır.

### Bağlantıyı Denetle İletisi

Alternatif olarak, Bob bir bağlantı aldığında, bu bir bağlantı denetimi
olabilir (belki de Bob, birinden dinleyicisini doğrulamasını
istemiştir). Bağlantı denetimi şu anda kullanılmıyor. Ancak, kayıt için
bağlantıların aşağıdaki gibi biçimlendirildiğinden emin olun. Bir bilgi
denetimi bağlantısı, aşağıdakileri içeren 256 bayt alır:

- 32 bayt yorumlanmamış, yok sayılan veri
- 1 bayt boyut
- yerel yönelticinin IP adresini oluşturan bu kadar bayt (uzak tarafın
 ulaştığı şekilde)
- yerel yönelticiye ulaşılan 2 bayt bağlantı noktası numarası
- Uzak tarafın bildiği şekliyle 4 bayt i2p ağ süresi (epoch sonrası
 saniye)
- yorumlanmamış dolgu ekleme verileri, 223. bayta kadar
- yerel yönelticinin kimlik karması ile SHA256 32. bayt ile 223. bayt
 arasının xor sonucu

Bağlantı denetimi 0.9.12 sürümünden sonra tamamen devre dışı
bırakılmıştır.

## Tartışma

Now on the [NTCP Discussion Page]().

## [Gelecekte Yapılacak Çalışmalar]{#future}

- En büyük ileti boyutu yaklaşık 32 KB olarak yükseltilmelidir.
- Verilerin parçalanmasını dış saldırganlardan daha fazla gizlemek
 için bir dizi sabit paket boyutu uygun olabilir. Ancak tünel, Garlic
 ve uçtan uca dolgu ekleme o zamana kadar çoğu gereksinim için
 yeterli olmalıdır. Ancak, sınırlı sayıda ileti boyutu oluşturmak
 amacıyla bir sonraki 16 baytlık sınırın ötesinde dolgu ekleme için
 şu anda herhangi bir koşul bulunmuyor.
- NTCP için bellek kullanımı (çekirdek ile birlikte) SSU ile
 karşılaştırılmalıdır.
- İlk paket boyutlarına bakılarak I2P trafiğinin tanınmasını
 engellemek için kuruluş iletileri bir şekilde rastgele
 doldurulabilir mi?


