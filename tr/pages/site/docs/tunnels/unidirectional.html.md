 Çift yönlü
tüneller 2016 Kasım
0.9.27 

## Özet

Bu sayfa, çift yönlü I2P tünellerinin kökenlerini ve tasarımını açıklar.
Ayrıntılı bilgi almak için şuraya bakabilirsiniz:

- [Tünel özeti
 sayfası]()
- [Tünel teknik
 özellikleri]()
- [Tünel oluşturma teknik
 özellikleri]()
- [Tünel tasarımı
 tartışması]()
- [Eş seçimi]()
- [Toplantı 125
 (\~13:12-13:30)]()

## Gözden geçirme

Tek yönlü tünellerin avantajları hakkında yayınlanmış herhangi bir
araştırma hakkında bilgi sahibi olmasak da, çift yönlü bir tünel
üzerinden algılanabilecek bir istek/yanıt modelinin algılanmasını
zorlaştırıyor gibi görünüyor. Birçok uygulama ve iletişim kuralı,
özellikle HTTP, verileri bu şekilde aktarır. Trafiğin hedefe doğru ve
hedeften geriye doğru aynı rotayı izlemesi, yalnızca zamanlama ve trafik
hacmi verilerine sahip bir saldırganın bir tünelin izlediği yolu
belirlemesini kolaylaştırabilir. Yanıtın farklı bir yoldan geri gelmesi
tartışmaya açık olsa da bu belirlemeyi zorlaştırır.

Bir iç saldırganla veya çoğu dış saldırganla uğraşırken, I2P ağının yönü
olmayan tünelleri, yalnızca akışların kendilerine bakarak çift yönlü
devrelerde olacağının yarısı kadar trafik verisi oluşturur. Bir HTTP
isteği ve yanıtı Tor üzerinde aynı yolu izler. I2P, isteği oluşturan
paketler bir ya da birkaç gidiş tünelinden dışarı çıkar ve yanıtı
oluşturan paketler bir ya da birkaç farklı geliş tünelinden geri gelir.

Geliş ve gidiş iletişimleri için iki ayrı tünel kullanma stratejisi, var
olan tek teknik değildir ve anonimlik etkileri vardır. Olumlu tarafı,
ayrı tüneller kullanmak, bir tüneldeki katılımcıların analiz
yapabileceği trafik verilerini azaltır. Örneğin, bir tarayıcıdan bir
gidiş tünelindeki eşler yalnızca bir HTTP GET trafiğini görürken, bir
geliş tüneli, tünel boyunca teslim edilen yükü görür. Çift yönlü
tünellerle, tüm katılımcılar, örneğin bir yöne 1KB, diğer yöne 100KB
gönderildiğini görebilir. Olumsuz tarafı, tek yönlü tünellerin
kullanılması, profilinin çıkarılması ve hesaba katılması gereken iki eş
grubunın olması ve önceki saldırıların artan hızına yönelik ek özen
gösterilmesinin gerekmesidir. Tünel havuzlama ve oluşturma süreci (eş
seçimi ve sıralama stratejileri), öncül saldırı endişelerini en aza
indirmelidir.

## Anonimlik

A recent [paper by Hermann and Grothoff]() declared
that I2P\'s unidirectional tunnels \"seems to be a bad design
decision\".

Makalenin ana noktası, tek yönlü tünellerdeki anonimleştirmelerin daha
uzun zaman alması ve bir avantaj sağlaması, ancak tek yönlü tünellerde
bir saldırganın daha emin olabileceğidir. Bu nedenle, makale bunun bir
avantaj olmadığını, en azından uzun ömürlü I2P sitelerinde bir
dezavantaj olduğunu iddia ediyor.

Bu sonuç makale tarafından tam olarak desteklenmiyor. Tek yönlü
tüneller, açıkça diğer saldırıları azaltır ve makaledeki saldırı
riskinin çift yönlü bir tünel mimarisine yapılan saldırılarla bedelinin
nasıl ödeneceği açık değildir.

Bu sonuç, her durumda geçerli olmayabilecek keyfi bir kesinliğe karşı
zaman ağırlığına (bedel ödeme) dayanmaktadır. Örneğin, biri olası IP
adreslerinin bir listesini yapabilir ve ardından her birine bir mahkeme
celbi gönderebilir. Veya saldırgan sırayla DDoS yapabilir ve basit bir
kavşak saldırısı yoluyla I2P sitesinin kapanıp kapanmadığını görebilir.
Bu kadar yakınlık yeterince iyi olabilir veya zaman daha önemli
olabilir.

Sonuç, kesinliğin zamana karşı belirli bir şekilde ağırlığının
belirlenmesine dayanmaktadır ve bu ağırlık değerlendirmesi yanlış
olabilir. Özellikle mahkeme celbi, arama emri ve nihai onay için geçerli
diğer yöntemlerin bulunduğu gerçek dünya örneğinde kesinlikle
tartışmalıdır.

Tek yönlü ve çift yönlü tünellerin bedellerinin ödenmesinin tam bir
analizi, açıkça makalenin kapsamı dışındadır ve başka bir yerde
yapılmamıştır. Örneğin, bu saldırı, Onion yöneltmeli ağlar hakkında
yayınlanan çok sayıda olası zamanlama saldırısıyla nasıl
karşılaştırılır? Yazarların, etkili bir şekilde yapılabilecek olsa bile,
bu analizi yapmadıkları görülebilir.

Tor, çift yönlü tüneller kullanır ve birçok akademik incelemeden
geçmiştir. I2P tek yönlü tüneller kullanır ve yayınlanmış çok az
inceleme vardır. Tek yönlü tünelleri savunan bir araştırma belgesinin
olmaması, bunun kötü bir tasarım seçimi olduğu ya da yalnızca üzerinde
daha fazla çalışmaya gerek olduğu anlamına mı gelir? Hem I2P hem de Tor
üzerinde zamanlama saldırılarına ve dağıtılmış saldırılara karşı savunma
oluşturmak zordur. Tasarım amacı (yukarıdaki referanslara bakın), tek
yönlü tünellerin zamanlama saldırılarına karşı daha dirençli olmasıydı.
Bununla birlikte, makale biraz farklı bir zamanlama saldırısı türü
sunuyor. Bu saldırı, yenilikçi olduğu kadar, I2P ağının tünel mimarisini
(ve dolayısıyla bir bütün olarak I2P ağını) \"kötü tasarım\" olarak
etiketlemek için yeterli mi? Dolaylı olarak Tor ağından açıkça daha
zayıf mı, yoksa yalnızca daha fazla araştırma ve inceleme gerektiren bir
tasarım alternatifi mi? I2P ağının şu anda Tor ve diğer projelerden daha
zayıf olduğunu düşünmek için başka nedenler var (ağ boyutunun küçük
olması, finansman eksikliği, inceleme eksikliği gibi) ama tek yönlü
tüneller gerçekten bir zayıflık nedeni mi?

Özetle, \"kötü tasarım kararı\" görünüşe göre (makale çift yönlü
tünelleri \"kötü\" olarak etiketlemediğinden) \"tek yönlü tüneller
kesinlikle çift yönlü tünellerden daha zayıftır\" ifadesinin kısaltılmış
halidir. Ancak makale bu sonucu desteklememektedir.


