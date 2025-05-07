 Yönetilen
istemciler 2014 Şubat
0.9.11 

## Özet

Clients may be started directly by the router when they are listed in
the [clients.config]() file. These clients
may be \"managed\" or \"unmanaged\". This is handled by the
ClientAppManager. Additionally, managed or unmanaged clients may
register with the ClientAppManager so that other clients may retrieve a
reference to them. There is also a simple Port Mapper facility for
clients to register an internal port that other clients may look up.

## Yönetilen istemciler

0.9.4 sürümünden başlayarak yöneltici, yönetilen istemcileri destekler.
Yönetilen istemciler, ClientAppManager tarafından hazırlanır ve
başlatılır. ClientAppManager, istemciye bir referans tutar ve istemcinin
durumuyla ilgili güncellemeleri alır. Durum izlemeyi uygulamak ve bir
istemciyi başlatmak ve durdurmak çok daha kolay olduğundan yönetilen
istemciler yeğlenir. İstemci kodunda, bir istemci durdurulduktan sonra
aşırı bellek kullanımına yol açabilecek durağan başvurulardan kaçınmak
da çok daha kolaydır. Yönetilen istemciler, kullanıcı tarafından
yöneltici panosundan başlatılıp durdurulabilir ve yöneltici
kapatıldığında durdurulur.

Yönetilen istemciler, net.i2p.app.ClientApp ya da
net.i2p.router.app.RouterApp arabirimini uygular. ClientApp arabirimini
uygulayan istemciler, aşağıdaki oluşturucuyu sağlamalıdır:

 public MyClientApp(I2PAppContext context, ClientAppManager listener, String[] args)

RouterApp arabirimini uygulayan istemciler aşağıdaki oluşturucuyu
sağlamalıdır:

 public MyClientApp(RouterContext context, ClientAppManager listener, String[] args)

Sunulan bağımsız değişkenler, client.config dosyasında belirtilir.

## Yönetilmeyen İstemciler

Client.config dosyasında belirtilen ana sınıf, yönetilen bir arabirim
uygulamıyorsa, belirtilen argümanlarla main() ile başlatılur ve
belirtilen argümanlarla main() ile durdurulur. Tüm etkileşimler statik
main() yöntemiyle yapıldığından, yöneltici bir referans tutmaz. Pano,
kullanıcıya doğru durum bilgisi sağlayamaz.

## Kayıtlı İstemciler

Yönetilen veya yönetilmeyen istemciler, diğer istemcilerin kendilerine
bir referans alabilmesi için ClientAppManager üzerine kayıt olabilir.
Kayıt ada göredir. Bilinen kayıtlı istemciler şunlardır:

 console, i2ptunnel, Jetty, outproxy, update

## Bağlantı Noktası Eşleştirme

Yöneltici ayrıca istemcilerin bir iç soket hizmeti bulması için basit
bir mekanizma sağlar. HTTP vekil sunucusu gibi. Bu, bağlantı noktası
eşleştiricisi tarafından sağlanır. Kayıt ada göredir. Kayıt olan
istemciler genellikle bu bağlantı noktasından bir iç öykünme soketi
sağlar.


