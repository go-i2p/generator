 I2P Ağ İletişim
Kuralı (I2NP) 2018 Ekim 0.9.37 

I2CP ve çeşitli I2P taşıyıcı iletişim kuralları arasında sıkıştırılmış
olan I2P ağ iletişim kuralı (I2NP), yönelticiler arasında iletilerin
yöneltilmesi ve karıştırılması işlemlerinin yanında, birden fazla
bağlantı noktası bulunan bir eş ile iletişim kurarken hangi
taşıyıcıların kullanılacağının seçilmesini sağlar. Yaygın taşıyıcılar
desteklenir.

### I2NP Tanımı

I2NP (I2P ağ iletişim kuralı) iletileri tek sıçramalı, yönelticiden
yönelticiye, noktadan noktaya iletiler için kullanılabilir. İletiler,
şifrelenerek ve diğer iletilere sarmalanarak, çoklu sıçrama yoluyla son
hedefe güvenli bir şekilde gönderilebilirler. Öncelik yalnızca kaynakta
yerel olarak, yani ileti gidiş aktarım için kuyruğa alınırken
kullanılır.

The priorities listed below may not be current and are subject to
change. See the [OutNetMessage
Javadocs]() for the current priority
settings. Priority queueing implementation may vary.

### İleti Biçimi

Aşağıdaki tabloda, NTCP içinde kullanılan geleneksel 16 baytlık üst
bilgiyi görebilirsiniz. SSU ve NTCP2 taşıyıcılarında değiştirilmiş üst
bilgiler kullanılır.

 Alan Bayt
 --------------- ------------
 Tür 1
 Benzersiz kod 4
 Sona erme 8
 Yük uzunluğu 2
 Sağlama 1
 Yük 0 - 61.2KB

While the maximum payload size is nominally 64KB, the size is further
constrained by the method of fragmenting I2NP messages into multiple 1KB
tunnel messages as described on [the tunnel implementation
page](). The maximum number of fragments is
64, and the message may not be perfectly aligned, So the message must
nominally fit in 63 fragments.

Bir ilk parçanın en fazla boyutu 956 bayttır (TÜNEL aktarım kipi
varsayılarak); bir izleme parçasının en fazla boyutu 996 bayttır. Bu
nedenle en fazala boyut yaklaşık 956 + (62 \* 996) = 62708 bayt veya
61.2 KB olur.

Ek olarak, taşıyıcıların ek kısıtlamaları olabilir. NTCP sınırı 16KB - 6
= 16378 bayttır. SSU sınırı yaklaşık 32 KB değerindedir. NTCP2 sınırı
yaklaşık olarak 64KB - 20 = 65516 bayttır ve bu, bir tünelin
destekleyebileceğinden daha fazladır.

Yöneltici bir yanıt \"Kiralama kümesini\" (LeaseSet) ve/veya oturum
etiketlerini istemci iletisiyle birlikte bir Garlic iletisinde
paketleyebileceğinden, bunların istemcinin gördüğü veri şemalarının
sınırları olmadığını unutmayın. \"Kiralama kümesi\" (LeaseSet) ve
etiketler birlikte yaklaşık 5.5 KB ekleyebilir. Bu nedenle var olan veri
şeması sınırı yaklaşık 10KB olur. Bu sınır gelecekteki bir sürümde
artırılacaktır.

### İleti Türleri

Daha yüksek numaralı öncelik değeri, daha yüksek öncelik anlamına gelir.
Trafiğin çoğunluğu tünel veri iletileridir (TunnelDataMessages) (öncelik
400). Bu nedenle 400 üzerindeki her şey aslında yüksek önceliklidir ve
altındaki her şey düşük önceliklidir. Ayrıca iletilerin çoğunun
genellikle istemci tünelleri yerine keşif tünelleri üzerinden
yöneltildiğini ve bu nedenle ilk sıçramalar aynı eşte olmadıkça aynı
kuyrukta olmayabileceğini unutmayın.

Ayrıca, tüm ileti türleri şifrelenmemiş olarak gönderilmez. Örneğin, bir
tüneli sınarken, yöneltici bir \"Veri iletisi\" (DataMessage) içine
sarmalanmış bir \"Garlic iletisi\" (GarlicMessage) içine sarmalanmış bir
\"Aktarım durumu iletisi\" (DeliveryStatusMessage) sarmalar.

İleti

Tür

Yük uzunluğu

Öncelik

Açıklamalar

DatabaseLookupMessage

2

 

500

Değişebilir

DatabaseSearchReplyMessage

3

Typ. 161

300

Boyut 65 + 32\*(karma sayısı) olup, burada tipik olarak üç otomatik
doldurma yönelticisi için karmalar döndürülür.

DatabaseStoreMessage

1

Değişir

460

Öncelik değişebilir. Tipik bir 2 kiralamalı \"Kiralama kümesi\"
(LeaseSet) için boyut 898 bayttır. \"Yöneltici bilgileri\" (RouterInfo)
yapıları sıkıştırılır ve boyut değişir. Bununla birlikte, 1.0 sürümüne
yaklaşırken \"Yöneltici bilgileri\" (RouterInfo) ile yayınlanan veri
miktarını azaltmak için süregelen bir çaba var.

DataMessage

20

4 - 62080

425

Öncelik, her hedef bazında değişebilir

DeliveryStatusMessage

10

12

 

İleti yanıtları ve tünelleri sınamak için kullanılır. Genellikle bir
Garlic iletisi (GarlicMessage) içine sarmalanır

[GarlicMessage](#op.garlic)

11

 

 

Genellikle bir veri iletisi (DataMessage) içine sarmalanır. Ancak paket
açıldığında, aktaran yöneltici tarafından 100 önceliği verilir

[TunnelBuildMessage](#tunnelCreate.requestRecord)

21

4224

500

[TunnelBuildReplyMessage](#tunnelCreate.replyRecord)

22

4224

300

TunnelDataMessage

18

1028

400

En yaygın ileti. Tünel katılımcıları, gidiş uç noktaları ve geliş ağ
geçitleri için öncelik, 0.6.1.33 sürümünden başlayarak 200 olacak
şekilde düşürüldü. Gidiş ağ geçidi iletileri (yani yerel olarak
oluşturulanlar) 400 olarak kaldı.

TunnelGatewayMessage

19

 

300/400

VariableTunnelBuildMessage

23

1057 - 4225

500

0.7.12 sürümünde tünel oluşturma iletisi (TunnelBuildMessage) kısaltıldı

VariableTunnelBuildReplyMessage

24

1057 - 4225

300

0.7.12 sürümünde tünel oluşturma iletisi (TunnelBuildMessage) kısaltıldı

Others listed in [2003 Spec]()

0,4-9,12

 

 

Kullanımdan kaldırıldı, kullanılmıyor

### Tam İletişim Kuralı Teknik Özellikleri

[On the I2NP Specification page](). See also
the [Common Data Structure Specification
page]().

### Gelecekte Yapılacak Çalışmalar

Geçerli öncelik şemasının genel olarak etkili olup olmadığı ve çeşitli
iletiler için önceliklerin daha fazla ayarlanması gerekip gerekmediği
açık değildir. Bu konuda, daha fazla araştırma, analiz ve test
gerekiyor.


