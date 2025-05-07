 Uygulama Ekleri 2012 Haziran 0.9 

## Genel Bilgiler

The I2P network includes a plugin architecture to support both easy
development and installation of new plugins.

Şu anda dağıtılmış e-postaları, blogları, IRC istemcilerini, dağıtılmış
dosya depolamayı, wiki sayfalarını ve başka pek çok özelliği sağlayan
uygulama ekleri var.

### Adding Plugins To Your I2P Router

I2P uygulama ekleri, uygulama eki indirme adresini [Yöneltici panosu
uygulama eki yapılandırma sayfası](http://127.0.0.1:7657/configplugins)
üzerindeki uygun bölüme kopyalayarak kurulabilir.

Yayınlandığı sayfadan uygulama eki adresini kopyalayarak başlayın.

![](/_static/images/plugins/plugin-step-0.png)

Ardından, pano ana sayfasında bağlantısını bulabileceğiniz uygulama eki
yapılandırma sayfasını açın.

![](/_static/images/plugins/plugin-step-1.png)

Adresi adres alanına yapıştırıp \"Uygulama ekini kur\" üzerine tıklayın.

![](/_static/images/plugins/plugin-step-2.png)

### i2p kullanıcılarına ve uygulama geliştiricilerine faydaları:

- Uygulamaların kolay dağıtılması
- `i2pupdate.sud` boyutunu büyütme endişesi olmadan yeniliğe ve ek
 kitaplıkların kullanılmasına izin verir
- Asla I2P kurulum paketine eklenmeyecek büyük veya özel amaçlı
 uygulamaları destekler
- Uygulamaların şifrelenmiş olarak imzalanmasını ve doğrulanmasını
 sağlar
- Yöneltici için olduğu gibi uygulamaların otomatik güncellenmesini
 sağlar
- Daha küçük güncellemeler için istenirse ilk kurulum ve güncelleme
 paketleri ayrılabilir
- Uygulamalar tek tıkla kurulabilir. Artık kullanıcılardan
 `wrapper.config` veya `clients.config` dosyalarını değiştirmeleri
 istenmez
- Uygulamalar temel `$I2P` kurulumundan ayrılabilir
- I2P sürümü, Java sürümü, Jetty sürümü ve önceden kurulmuş uygulama
 sürümleri için otomatik uyumluluk denetimi
- Panoya otomatik bağlantı ekleme
- Yeniden başlatma gerektirmeden sınıf yolunun değiştirilmesi ile
 birlikte uygulamanın otomatik olarak başlatılması
- İnternet uygulamalarının pano Jetty kopyasıyla otomatik
 bütünleştirilmesi ve başlatılması
- Facilitate creation of \'app stores\' like the one at [](http://)
- Tek tıkla kaldırma
- Pano için dil ve tema paketleri
- Ayrıntılı uygulama bilgilerinin yöneltici panosunda görüntülenmesi
- Java olmayan uygulamalar da desteklenir

### Gerekli I2P sürümü

0.7.12 ya da üzeri.

### Bir uygulama ekini güncellemek

Bir uygulama ekini son sürüme güncellemek için
[configclients.jsp](http://127.0.0.1:7657/configclients.jsp#plugin)
bölümündeki güncelle düğmesine tıklamanız yeterlidir. Uygulama ekinin
daha yeni bir sürümü olup olmadığını denetlemek için bir düğme ve tüm
uygulama eklerinin güncellemelerini denetlemek için başka bir düğme
vardır. Uygulama ekleri, yeni bir I2P sürümüne güncellenirken
(geliştirme yapımları katılmaz) güncellemeler otomatik olarak
denetlenir.

![](/_static/images/plugins/plugin-update-0.png)

### Geliştirme

See the latest [plugin specification]()

See also the sources for plugins developed by various people. Some
plugins, such as
[snowman](http:///plugins/snowman), were
developed specifically as examples.

### Başlarken

To create a plugin from an existing binary package you will need to get
makeplugin.sh from [the i2p.scripts repository in
git]().

### Bilinen Sorunlar

Yönelticinin uygulama eki mimarisinin şu anda herhangi bir ek güvenlik
yalıtımı veya uygulama eki sanal alanı **sağlamadığını** unutmayın.

- Sınıf ön belleğini temizlemek için sınıf yükleyici kandırmak
 gerektirdiğinden, uygulama eki zaten çalıştırılmışsa, katılmış jar
 dosyalarını (war dosyaları değil) içeren bir uygulama ekinin
 güncellemeleri tanınmaz. Yönelticinin tam olarak yeniden
 başlatılması gereklidir.
- Durdurulacak bir şey olmasa bile durdurma düğmesi görüntülenebilir.
- Ayrı bir Java sanal makinesinde çalışan uygulama ekleri, `$CWD`
 içinde `logs/` klasörü oluşturur.
- jrandom ve zzz (yöneltici güncellemesiyle aynı anahtarları kullanan)
 dışında başka bir başlangıç anahtarı yoktur. Bu nedenle bir
 imzalayan için görülen ilk anahtar otomatik olarak kabul edilir ve
 başka bir imzalama anahtarının yetkisi yoktur.
- Bir uygulama ekini silerken, özellikle Windows üzerinde klasör her
 zaman silinmez.
- Java 1.5 makinesine Java 1.6 gerektiren bir uygulama eki kurmak,
 uygulama eki dosyasının pack200 sıkıştırması kullanılırsa \"uygulama
 eki bozuk\" iletisi görüntülenir.
- Tema ve çeviri uygulama ekleri denenmemiştir.
- Otomatik başlatmayı devre dışı bırakmak her zaman işe yaramaz.


