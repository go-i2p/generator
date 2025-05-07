 ElGamal/AES +
Oturum etiketi şifrelemesi April
2020 0.9.46 

## Özet

Uçtan uca şifreleme için ElGamal/AES+Oturum etiketi kullanılır.

Güvenilmez, sıralı olmayan ileti tabanlı bir sistem olan I2P, garlic
iletilerinin veri gizliliği ve bütünlüğü sağlamak için asimetrik ve
simetrik şifreleme algoritmalarının basit bir kombinasyonunu kullanır.
Bir bütün olarak, kombinasyon ElGamal/AES+Oturum etiketi olarak anılır.
Ancak bu, 2048 bit ElGamal, AES-256, SHA-256 ve 32 bayt nonce
kullanımını açıklamak için aşırı derecede ayrıntılı bir yoldur.

Bir yöneltici ilk kez başka bir yönelticiye göndereceği bir garlic
iletisini şifrelemek istediğinde, bir AES-256 oturum anahtarı için
anahtarlama materyalini ElGamal ile şifreler ve bu şifrelenmiş ElGamal
bloğunun ardından AES-256/CBC ile şifrelenmiş yükü ekler. Şifrelenmiş
yüke ek olarak, AES ile şifrelenmiş bölümü yük uzunluğu, şifrelenmemiş
yükün SHA-256 karması ve ayrıca bir dizi \"oturum etiketi\" - rastgele
32 baytlık olmayanlar - bulunur. Gönderici bir dahaki sefere bir garlic
iletisini başka bir yönlendiriciye şifrelemek istediğinde, ElGamal yeni
bir oturum anahtarını şifrelemek yerine, daha önce teslim edilmiş oturum
etiketlerinden birini seçer ve AES, daha önce olduğu gibi, o oturum
etiketiyle kullanılan oturum anahtarını kullanarak yükü şifreler. Bu
bilgi oturum etiketinin başına eklenir. Bir yöneltici bir garlic
şifrelenmiş iletisi aldığında, uygun bir oturum etiketiyle eşleşip
eşleşmediğini görmek için ilk 32 baytı kontrol eder. Eşleşme bulunursa
yalnızca AES iletisinin şifresini çözer. Bulunmazsa ElGamal ilk bloğun
şifresini çözer.

Her oturum etiketi, iç izleyicilerin aynı yönelticiler arasında olduğu
gibi farklı iletileri gereksiz yere ilişkilendirmesini önlemek için
yalnızca bir kez kullanılabilir. ElGamal/AES+Oturum etiketi şifrelemiş
iletisinin göndericisi, ne zaman ve kaç etiketin teslim edileceğini
seçer ve alıcıya bir sürü iletiyi kapsayacak kadar yeterli etiket
hazırlar. Garlic iletileri küçük bir ek iletiyi bir diş (\"teslim durumu
iletisi\") olarak paketleyerek etiket tesliminin başarılı olduğunu
algılayabilir - garlic iletisi hedeflenen alıcıya ulaştığında ve şifresi
başarıyla çözüldüğünde, bu küçük teslim durumu dişlerden biridir. Açığa
çıkar ve alıcının dişi özgün göndericiye geri göndermesi için yönergeler
içerir (elbette bir geliş tüneli üzeirnden). Özgün gönderici bu teslim
durumu iletisini aldığında, garlic iletisinde gruplanan oturum
etiketlerinin başarıyla iletildiğini bilir.

Oturum etiketlerinin ömürleri kısadır. bu sürenin sonunda
kullanılmazlarsa atılır. Ek olarak, her bir anahtar için depolanan
miktar ve anahtarların sayısı sınırlıdır. Çok fazla gelirse, yeni veya
eski iletiler kaybolabilir Gönderici, oturum etiketlerini kullanan
iletilerin geçip geçmediğini izler ve yeterli iletişim yoksa, daha önce
düzgün bir şekilde iletildiği varsayılanları bırakarak en pahalı ElGamal
şifrelemesine geri dönebilir. Bir oturum, tüm etiketleri tükenene veya
süresi dolana kadar var olmayı sürdürür

Oturumlar tek yönlüdür. Etiketler Alice tarafından Bob tarafına iletilir
ve Alice daha sonra Bob tarafına gönderilen sonraki iletilerdeki
etiketleri birer birer kullanır.

Oturumlar, hedefler arasında, yönelticiler arasında veya yöneltici ile
hedef arasında kurulabilir. Her yöneltici ve hedef,in oturum
anahtarlarını ve oturum etiketlerini izlemek için kendi oturum anahtarı
yöneticisi vardır. Ayrı oturum anahtarı yöneticileri olması, düşmanlar
tarafından birden çok hedefin birbiriyle veya bir yönelticiyle
ilişkilendirilmesini önler.

## İleti Almak

Alınan her ileti iki olası koşuldan birine sahiptir:

1. Var olan bir oturumun parçasıdır ve bir oturum etiketi ve bir AES
 ile şifrelenmiş blok içerir
2. Yeni bir oturum içindir ve hem ElGamal hem de AES ile şifrelenmiş
 blokları içerir.

Bir yöneltici bir ileti aldığında, önce bunun var olan bir oturumdan
geldiğini varsayar. Oturum etiketini aramaya ve AES kullanarak aşağıdaki
verilerin şifresini çözmeye çalışır. Bunda başarısız olursa, oturumun
yeni olduğunu varsayar ve şifresini ElGamal kullanarak çözmeye çalışır.

## Yeni Oturum İleti Teknik Özellikleri {#new}

Yeni oturum ElGamal iletisi şifrelenmiş bir ElGamal bloğu ve şifrelenmiş
bir AES bloğu şeklinde iki bölümden oluşur.

Şifrelenmiş iletide şunlar bulunur:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| ElGamal Encrypted Block \| \~ \~ \| \| +
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| \| \|
+\-\-\--+\-\-\--+ + \| \| + + \| AES Encrypted Block \| \~ \~ \| \| +
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| + +\-\-\--+\-\-\--+


### ElGamal Bloğu

Şifrelenmiş ElGamal bloğu her zaman 514 bayt uzunluğundadır.

Şifrelenmemiş ElGamal verileri 222 bayt uzunluğundadır ve şunları
içerir:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| Session Key \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| Pre-IV \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ + + \|
\| + + \| 158 bytes random padding \| \~ \~ \| \| + +\-\-\--+\-\-\--+ \|
\| +\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 

The 32-byte [Session
Key](#type_SessionKey) is the
identifier for the session. The 32-byte Pre-IV will be used to generate
the IV for the AES block that follows; the IV is the first 16 bytes of
the SHA-256 Hash of the Pre-IV.

The 222 byte payload is encrypted [using
ElGamal](#elgamal) and the encrypted block
is 514 bytes long.

### AES Bloğu {#aes}

AES bloğundaki şifrelenmemiş verilerde şunlar buunur:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|tag
count\| \| +\-\-\--+\-\-\--+ + \| \| + + \| Session Tags \| \~ \~ \|
\| + + \| \| + +\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \| \|
payload size \| \| +\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ +
\| \| + + \| Payload Hash \| + + \| \| + +\-\-\--+\-\-\--+ \| \|flag\|
\| +\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ + \| \| + +
\| New Session Key (opt.) \| + + \| \| + +\-\-\--+ \| \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ + \| \| + + \|
Payload \| \~ \~ \| \| + +\-\-\--//\-\--+\-\-\--+ \| \| \|
+\-\-\--+\-\-\--+\-\-\--//\-\--+\-\-\--+ + \| Padding to 16 bytes \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 

#### Definition

 tag count: 2-byte \`Integer\`, 0-200
Session Tags: That many 32-byte \`SessionTag\`s payload size: 4-byte
\`Integer\` Payload Hash: The 32-byte SHA256 \`Hash\` of the payload
flag: A one-byte value. Normally == 0. If == 0x01, a Session Key follows
New Session Key: A 32-byte \`SessionKey\`, to replace the old key, and
is only present if preceding flag is 0x01 Payload: the data Padding:
Random data to a multiple of 16 bytes for the total length. May contain
more than the minimum required padding. En az
uzunluk: 48 bayt

The data is then [AES Encrypted](), using
the session key and IV (calculated from the pre-IV) from the ElGamal
section. The encrypted AES Block length is variable but is always a
multiple of 16 bytes.

#### Notlar

- Actual max payload length, and max block length, is less than 64 KB;
 see the [I2NP Overview]().
- Yeni oturum anahtarı şu anda kullanılmamış ve asla var olmamış.

## Var Olan Oturum İletisinin Teknik Özellikleri {#existing}

Sorunsuz iletilen oturum etiketleri, kullanılıncaya ya da atılıncaya
kadar kısa bir süre (şu anda 15 dakika) boyunca hatırlanır. Bir etiket,
yalnızca AES ile şifrelenmiş bir blok içeren ve önünde bir ElGamal bloğu
bulunmayan var olan oturum şletisinde paketlenerek kullanılır.

Var olan oturum iletisi şu şekildedir:


+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| Session Tag \| + + \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ \|
\| + + \| AES Encrypted Block \| \~ \~ \| \| + + \| \|
+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+\-\-\--+ 

#### Definition

 Session Tag: A 32-byte \`SessionTag\`
previously delivered in an AES block AES Encrypyted Block: As specified
above. 

Oturum etiketi ayrıca IV öncesi olarak da hizmet eder. IV, oturum
etiketinin SHA-256 karmasının ilk 16 baytıdır.

Var olan bir oturumdan gelen bir iletinin kodunu çözmek için yöneltici,
ilişkili bir oturum anahtarı bulmak amacıyla oturum etiketini arar.
Oturum etiketi bulunursa, ilgili oturum anahtarı kullanılarak AES
bloğunun şifresi çözülür. Etiket bulunamazsa, iletinin bir [yeni oturum
iletisi](#new) olduğu varsayılır.

## Oturum Etiketi Yapılandırma Seçenekleri {#config}

As of release 0.9.2, the client may configure the default number of
Session Tags to send and the low tag threshold for the current session.
For brief streaming connections or datagrams, these options may be used
to significantly reduce bandwidth. See the [I2CP options
specification](#options) for details. The session
settings may also be overridden on a per-message basis. See the [I2CP
Send Message Expires
specification](#msg_SendMessageExpires) for
details.

## Gelecekte Yapılacak Çalışmalar {#future}

**Note:** ElGamal/AES+SessionTags is being replaced with
ECIES-X25519-AEAD-Ratchet (Proposal 144). The issues and ideas
referenced below have been incorporated into the design of the new
protocol. The following items will not be addressed in
ElGamal/AES+SessionTags.

Oturum anahtarı yönetimi algoritmalarının ayarlanabileceği birçok olası
alan vardır. Bazıları akış kitaplığı davranışıyla etkileşime girebilir
ya da genel başarım üzerinde önemli bir etkiye sahip olabilir.

- Teslim edilen etiketlerin sayısı, tünel ileti katmanında son dolgu
 eklemenin 1 KB olacağı akılda tutularak, ileti boyutuna bağlı
 olabilir.
- İstemciler, gerekli etiket sayısı konusunda bir öneri olarak
 yönelticiye bir oturum ömrü öngörüsü gönderebilir.
- Teslim edilen etiket sayısının çok az olması, yönelticinin pahalı
 ElGamal şifrelemesine geri dönmesine neden olur.
- Yöneltici, oturum etiketlerinin teslim edildiğini varsayabilir ya da
 bunları kullanmadan önce onay bekleyebilir. Her strateji için
 uzlaşmalar vardır.
- Çok kısa iletiler için, ElGamal bloğundaki pre-IV ve dolgu ekleme
 (padding( alanlarının neredeyse tam 222 baytı, bir oturum kurmak
 yerine iletinin tamamı için kullanılabilir.
- Dolgu ekleme stratejisini değerlendirin. Şu anda en az 128 bayt
 olacak şekilde dolgu ekliyoruz. Küçük iletilere dolgu yerine birkaç
 etiket eklemek daha iyi olur.
- Oturum etiketi sistemi çift yönlü olsaydı belki işler daha verimli
 olabilirdi, bu nedenle \'ileri\' yolda teslim edilen etiketler
 \'geri\' yolda kullanılabilir. Böylece ilk yanıtta ElGamal
 şifrelemesinden kaçınılabilir. Şu anda yöneltici kendisine tünel
 test iletileri gönderirken bunun gibi incelikler yapıyor.
- Change from Session Tags to [a synchronized
 PRNG](#prng).
- Several of these ideas may require a new I2NP message type, or set a
 flag in the [Delivery
 Instructions](#struct_TunnelMessageDeliveryInstructions),
 or set a magic number in the first few bytes of the Session Key
 field and accept a small risk of the random Session Key matching the
 magic number.


