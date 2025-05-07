 SOCKS 

## SOCKS ve SOCKS vekil sunucuları

The SOCKS proxy is working as of release 0.7.1. SOCKS 4/4a/5 are
supported. Enable SOCKS by creating a SOCKS client tunnel in i2ptunnel.
Both shared-clients and non-shared are supported. There is no SOCKS
outproxy so it is of limited use. 

Birçok uygulama, İnternet üzerinde kim olduğunuzun belirlenebilmesini
sağlayacak hassas bilgileri sızdırır. I2P yalnızca bağlantı verilerini
süzer, ancak çalıştırmayı düşündüğünüz uygulama bu bilgileri içerik
olarak gönderirse, I2P anonimliğinizi korumak için bir şey yapamaz.
Örneğin, bazı e-posta uygulamaları, üzerinde çalıştıkları bilgisayarın
IP adresini bir e-posta sunucusuna gönderir. I2P bu bilgiyi süzemez. Bu
nedenle var olan uygulamalar \'socks\' ile I2P üzerinde kullanılabilir,
ancak son derece tehlikelidir.

2005 tarihli bir e-postadan alıntı:

 ... insanların ve diğerlerinin SOCKS vekil sunucularını önce kurup sonra 
 terk etmesinin bir nedeni var. Rastgele trafiği yöneltmek kesinlikle güvenli 
 değildir ve son kullanıcılarımızın güvenliğini akılımızdaki her şeyden önde 
 tutmak, anonimlik ve güvenlik yazılımı geliştiricileri olarak bize düşüyor.

Hem davranışını hem de güvenlik ve anonimlik için açık iletişim
kurallarını denetlemeden keyfi bir istemciyi I2P ağına
bağlayabileceğimizi ummak saflık olur. Hemen hemen \*her\* uygulama ve
iletişim kuralı, özellikle bunun için tasarlanmadıkça anonimliği bozar.
Ona göre tasarlanmış olanlar bile bunu yapar. Gerçek bu. Hizmetler, son
kullanıcılara, anonimlik ve güvenlik için tasarlanmış sistemlerle daha
iyi verilir. Var olan sistemleri anonim ortamlarda çalışacak şekilde
değiştirmek az buz bir iş değil. Var olan I2P API yazılımlarını
kullanmaktan çok daha büyük bir iş.

SOCKS vekil sunucusu standart adres defteri adlarını destekler, ancak
Base64 hedeflerini desteklemez. Base32 karmaları, 0.7 sürümünden
başlayarak çalışır. Yalnızca gidiş bağlantılarını, yani bir I2PTunnel
İstemcisini destekler. UDP desteği eklendi ancak henüz çalışmıyor.
Bağlantı noktasına göre çıkış vekil sunucusu seçimi eklendi.

The notes for [Meeting 81]() and [Meeting
82]() in March 2004.

[Onioncat](http://www.abenteuerland.at/onioncat/)

[](http:///)

### İşe yarayan bir şey bulursanız

Lütfen bize bildirin. Ve lütfen socks vekil sunucularının riskleri
hakkında gerekli uyarıları yapın. 
