 I2P ile GitLab
Kurmak 2020-09 0.9.47 

# Git over I2P for Users

I2P tüneli üzerinden Git erişimini ayarlama eğitimi. Bu tünel, I2P
üzerindeki tek bir Git hizmetine erişim noktanız olarak davranır.

**Hizmeti i2pgit.org/git.idk.i2p adresinden kullanmayı düşünüyorsanız,
büyük olasılıkla önceden yapılandırılmış bir tüneliniz vardır ve bu
öğreticinin çoğu sizin için geçerli olmayacaktır.**

## Bir: Git hizmetinde bir hesap açın {#first-set-up-an-account-at-a-git-service}

Uzak bir Git hizmetinde depolarınızı oluşturmak için o hizmette bir
kullanıcı hesabı açın. Elbette, yerel depolar oluşturarak bunları uzak
bir Git hizmetine gönderme seçeneğiniz de vardır. Ancak çoğu durumda bir
hesap açılması ve sunucuda kendiniz için bir depo alanı oluşturmanız
gerekir. GitLab hesap açma formu çok basittir:

Bunlar, HTTP ve SSH ağ geçitlerini kullanan herhangi bir i2p Git kopyası
için genel bilgilerdir. I2P projesine katkıda bulunmayı düşünüyorsanız,
topluluğa açık olan I2P GitLab üzerinde bir hesap açmalısınız.
Yöneticinin çok sayıda spam kaydını ayırması gerektiğinden, hesap
kaydının tamamlanması birkaç gün sürebilir. Ana sayfadaki açıklamaları
kullanarak insan olduğunuzu onaylamak için yönetici ile iletişime
geçebilir ve süreci hızlandırabilirsiniz.

- **[I2P içinden - (http://git.idk.i2p)](http://git.idk.i2p)**
- **[I2P dışından - (https://i2pgit.org)](https://i2pgit.org)**

![Registration is easy!](/_static/images/git/register.png)

## Second: Create a project to test with

Kurulum işleminin çalıştığından emin olmak için sunucudan bir deneme
havuzu oluşturmanızı sağlar. Bu eğitimin amacına yönelik olarak I2P
yöneltici dalını kullanacağız. İlk olarak, i2p-hackers/i2p.i2p deposuna
gidin:

![Browse to i2p.i2p](/_static/images/git/explore.png)

![I2P Hackers i2p.i2p](/_static/images/git/i2p.png)

Ardından, hesabınızda bir dalını oluşturun.

![Roger is forking](/_static/images/git/fork.png)

![Roger is finished](/_static/images/git/forked.png)

## Third: Set up your git client tunnel

Sunucuma okuma-yazma erişimine sahip olmak için SSH istemciniz için bir
tünel kurmanız gerekecek. Örnek olarak, bunun yerine HTTP tünelini
kullanacağız. Ancak yalnızca salt okunur erişime, HTTP/S kopyalamaya
gerek duyuyorsanız, tüm bunları atlayabilir ve Git yapılandırması için
önceden hazırlanmış I2P HTTP vekil sunucusunu kullanmak amacıyla
http_proxy ortam değişkenini kullanabilirsiniz. Örneğin:

 http_proxy=http://localhost:4444 git clone http://gittest.i2p/i2p-developer/i2p.i2p

![Client tunnel](/_static/images/git/wizard1.png)

![Git over I2P](/_static/images/git/wizard2.png)

Ardından, itme ve çekme istekleri için kullanacağınız adresi ekleyin. Bu
örnek adresin I2P üzerinden salt okunur HTTP kopyaları için olduğunu
unutmayın. Yöneticiniz Git HTTP (Akıllı HTTP) iletişim kuralına izin
vermiyorsa, SSH kopyasının base32 adresini almanız gerekecektir. Bir SSH
klonu base32 adresiniz varsa, bu adımda başarısız olan base32 adresi
yerine onu kullanın.

![gittest.i2p](/_static/images/git/wizard3.png)

I2P hizmetinin yerel olarak iletileceği bir bağlantı noktası seçin.

![localhost:localport](/_static/images/git/wizard4.png)

Çok kullandığım için istemci tünelimi otomatik olarak başlatıyorum ama
bu size kalmış.

![Auto Start](/_static/images/git/wizard5.png)

Her şey bittiğinde, buna çok benzemeli.

![Review settings](/_static/images/git/wizard6.png)

## Dört: Bir kopya oluşturmayı deneyin {#trans--fourth-attempt-a-clone--endtrans}

Artık tüneliniz hazır, SSH üzerinden kopyalamayı deneyebilirsiniz.

Git kişisel gizliliği: Git gönderileri, Git gönderi iletilerine yerel
saat diliminizi yansıtacak şekilde yapılandırılabilen bir zaman damgası
ekler. Tüm gönderilerde UTC saat diliminin kullanılmasını zorlamak için
bir Git takma adı kullanmanız önerilir. Örnek:

 git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'

değiştirmenizi sağlayacak

 git commit

şunun için

 git utccommit

yerel saat diliminizi gizlemek için.

 GIT_SSH_COMMAND="ssh -p 7442" \
 git clone git@127.0.0.1:i2p-developer/i2p.i2p

Uzak ucun beklenmedik bir şekilde kapandığı ile ilgili bir hata
görebilirsiniz. Ne yazık ki Git hala sürdürülebilir kopyalamayı
desteklemiyor. Bunu yapana kadar, bu sorunu aşmanın oldukça kolay birkaç
yolu var. İlk ve en kolayı, sığ bir derinliğe kopyalamaya çalışmaktır:

 GIT_SSH_COMMAND="ssh -p 7442" \
 git clone --depth 1 git@127.0.0.1:i2p-developer/i2p.i2p

Sığ bir kopyalama gerçekleştirdikten sonra, depo klasörüne geçerek ve
aşağıdakileri çalıştırarak geri kalanını sürdürerek alabilirsiniz:

 git fetch --unshallow

Bu noktada, henüz tüm dallarınıza sahip değilsiniz. Aşağıdaki komutları
çalıştırarak onları alabilirsiniz:

 git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
 git fetch origin

Bu komutlar, Git yazılımına kaynaktan alma sırasında tüm dallar alınacak
şekilde depo yapılandırmasını değiştirmesini söyler.

Bu işe yaramazsa, tünel yapılandırma menüsünü açarak bazı yedek tüneller
eklemeyi deneyebilirsiniz.

![Backup Tunnels](/_static/images/git/tweak2.png)

Bu da işe yaramazsa, denenmesi gereken bir sonraki kolay şey tünel
uzunluğunu azaltmaktır. Ancak koda katkıda bulunma çalışmalarınızın,
birçok kötü amaçlı düğüm işleterek tüm yolunuzu denetlemeye çalışan ve
bol kaynağı olan bir saldırgan tarafından izlendiğini ve anonimliğinizin
bozulması riskiyle karşı karşıya olduğunu düşünüyorsanız, bunu yapmayın.
Bu durum size pek olası gelmiyorsa güvenle yapabilirsiniz.

![One-Hop Tunnels](/_static/images/git/tweak1.png)

## *Geliştiriciler için Önerilen İş Akışı!* {#trans--suggested-workflow-for-developers--endtrans}

Sürüm denetimi hayatınızı kolaylaştırabilir, ancak en iyi sonucu
alabilmek için onu iyi kullanmanız gerekir! Bunun ışığında, birçoğunun
GitHub üzerinden aşina olduğu, önce dallandır, özelliği dalda geliştir
şeklinde bir iş akışı öneriyoruz. Böyle bir iş akışında, ana dal,
güncellemeler için bir tür \"Gövde\" olarak kullanılır ve programcı
tarafından asla dokunulmaz. Bunun yerine ana dalda yapılan tüm
değişiklikler diğer dallardan birleştirilir. Çalışma alanınızı buna göre
kurmak için aşağıdaki adımları izleyin:

- **Asla ana dalda değişiklik yapmayın**. Resmi kaynak kodundaki
 güncellemeleri düzenli olarak almak için ana dalı kullanacaksınız.
 Tüm değişiklikler özellik dallarında yapılmalıdır.

1. Yukarı akış kaynak kodunu kullanarak yerel deponuzda ikinci bir uzak
 depo kurun.

 git remote add upstream git@127.0.0.1:i2p-hackers/i2p.i2p

2. Var olan ana daldaki tüm yukarı akış değişikliklerini çekin:

 git pull upstream master

3. Kaynak kodunda herhangi bir değişiklik yapmadan önce, üzerinde
 geliştirme çalışmalarının yapılacağı yeni özellik dalını denetleyin:

 git checkout -b feature-branch-name

4. Değişikliklerinizi tamamladığınızda bunları gönderin ve dalınıza
 itme isteğinde bulunun

 git commit -am "I added an awesome feature!"
 git push origin feature-branch-name

5. Bir birleştirme isteğinde bulunun. Birleştirme isteği onaylandığında
 ve yukarı akış ana dalına getirildiğinde, ana dalı yerel olarak
 denetleyin ve değişiklikleri alın:

 git checkout master
 git pull upstream master

6. Yukarı akış ana dalında (i2p-hackers/i2p.i2p) bir değişiklik
 yapıldığında da, bu akışı kullanarak ana kodunuzu
 güncelleyebilirsiniz.

 git checkout master
 git pull upstream master

Git zaman damgası sorununa yönelik Git utccommit takma adı çözümüne,
burada ilk kez yayınlanan bilgilerden ulaşıldı:
[saebamini.com](https://saebamini.com/Git-commit-with-UTC-timestamp-ignore-local-timezone/).


