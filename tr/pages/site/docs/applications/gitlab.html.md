 I2P ile GitLab
Kurmak 2020-09 0.9.47 

# I2P Üzerinden GitLab Kurulumu {#gitlab-over-i2p-setup}

::: {.meta author="idk" date="2020-03-16" excerpt="Başkaları için I2P Git depolarını yansıtın ve herkese açık İnternet depolarını köprüleyin."}
:::

Bu bölümde hizmetin kendisini yönetmek için Docker ile GitLab ve I2P
yapılandırmaları için kullandığım kurulum sürecini anlatacağım. Bu
şekilde I2P üzerinde GitLab barındırmak çok kolaydır ve tek kişi
tarafından çok zorlanmadan yönetilebilir. Yapılandırmamda, bir Debian
sunucu sisteminde docker kapsayıcılarını ve bir I2P yönelticisini
barındırmak için bir Debian sanal makinesi kullanıyorum. Ancak bu
kurulum bazı insanlar için gereğinden fazla olabilir. Bu yönergeler, bir
sanal makinede olsun veya olmasın, herhangi bir Debian tabanlı sistemde
çalışmalı ve Docker ile bir I2P yönelticisinin bulunduğu herhangi bir
sisteme kolayca dönüştürülebilmelidir. Bu rehber Docker ile başlar ve
altında herhangi bir sanal makine olmadığını varsayar.

## Bağımlılıklar ve Docker {#dependencies-and-docker}

GitLab bir kapsayıcı içinde çalıştığı için ana sistemimize yalnızca
kapsayıcı için gerekli olan bağımlılıkları kurmanız gerekir. Uygun bir
şekilde, gerek duyduğunuz her şeyi aşağıdaki komutlarla kurabilirsiniz:

 sudo apt install docker.io

başka şekilde değiştirilmemiş bir Debian sistemi veya Docker
uygulamasının kendi \"Topluluk\" Debian deposunu eklediyseniz, şunları
kullanabilirsiniz:

 sudo apt install docker-ce

onun yerine.

### Docker Kapsayıcılarını Alın {#fetch-the-docker-containers}

Docker kurduktan sonra GitLab için gerekli Docker kapsayıcılarını
getirebilirsiniz. *Henüz çalıştırmayın.*

 docker pull gitlab/gitlab-ce

İlgilenenler için gitlab-ce Docker kalıbı, sıfırdan ve üst öge olarak
Ubuntu Docker kalıpları kullanılarak oluşturulmuştur. Burada üçüncü
taraf kalıpları bulunmadığından, güncellemeler sunucu kalıplarına
eklenir eklenmez gelmelidir. Dockerfile kalıbını kendiniz incelemek
isterseniz [GitLab kaynak
kodu](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile)
bölümüne bakabilirsiniz.

## GitLab kullanımı için bir I2P HTTP vekil sunucusu kurun (önemli bilgiler, isteğe bağlı adımlar) {#set-up-an-i2p-http-proxy-for-gitlab-to-useimportant-information-optional-steps}

I2P içindeki GitLab sunucuları, I2P dışındaki İnternet üzerindeki
sunucularla etkileşime girme yeteneği olarak ya da olmayarak
işletilebilir. GitLab sunucusunun I2P dışındaki sunucularla etkileşimine
*izin verilmediği* bir durumda, I2P dışındaki İnternet üzerindeki bir
Git sunucusundan bir Git deposunu kopyalayarak anonim hale getiremezler.
Bununla birlikte, I2P içindeki diğer Git hizmetlerinden depoları dışa
aktarabilir ve yansıtabilirler.

GitLab sunucusunun I2P dışındaki sunucularla etkileşimine *izin
verildiği* durumlarda, I2P dışındaki içeriği I2P ile erişilebilir bir
kaynağa yansıtmak için kullanıcılar tarafından kullanılabilen bir
\"Köprü\" görevi görebilir. Ancak *bu kullanım anonim değildir*. Anonim
olmayan İnternet üzerindeki Git hizmetleri ile doğrudan bağlantı
kurulacaktır.

**İnternet depolarına** erişmek için **köprülenmiş, anonim olmayan bir
GitLab kopyası işletmek istiyorsanız** daha fazla değişiklik yapmanız
gerekmez.

**Depolara** erişmek için **yalnızca internet erişimi olmayan bir I2P
GitLab kopyası işletmek istiyorsanız**, GitLab yapılandırmasını bir I2P
HTTP vekil sunucusu kullanacak şekilde ayarlamanız gerekir. Varsayılan
I2P HTTP vekil sunucusu yalnızca `127.0.0.1` adresinden dinlediğinden,
Docker ağının sunucu/ağ geçidi adresini dinleyen Docker için genellikle
`172.17.0.1` olan yeni bir arayüz ayarlamanız gerekecektir. Benimkini
`4446` bağlantı noktası için yapılandırıyorum.

## Kapsayıcıyı Yerel Olarak Başlatın {#start-the-container-locally}

Bu kurulumu yaptıktan sonra kapsayıcıyı başlatabilir ve GitLab kopyanızı
yerel olarak yayınlayabilirsiniz.

 docker run --detach \
 --env HTTP_PROXY=http://172.17.0.1:4446 \
 --publish 127.0.0.1:8443:443 --publish 127.0.0.1:8080:80 --publish 127.0.0.1:8022:22 \
 --name gitlab \
 --restart always \
 --volume /srv/gitlab/config:/etc/gitlab:Z \
 --volume /srv/gitlab/logs:/var/log/gitlab:Z \
 --volume /srv/gitlab/data:/var/opt/gitlab:Z \
 gitlab/gitlab-ce:latest

Yerel GitLab kopyanızı ziyaret edin ve yönetici hesabınızı ayarlayın.
Güçlü bir parola seçin ve kaynaklarınıza uygun kullanıcı hesabı
sınırlamalarını yapılandırın.

## gitlab.rb dosyasını değiştirin (isteğe bağlı, ama \"köprülenmiş anonim olmayan\" sunucular için iyi bir fikir) {#modify-gitlab.rboptional-but-a-good-idea-for-bridged-non-anonymous-hosts}

HTTP vekil sunucu ayarlarınızı daha ayrıntılı bir şekilde de
uygulayabilirsiniz. Böylece kullanıcıların yalnızca seçtiğiniz etki
alanlarındaki depoları yansıtmasını sağlayabilirsiniz. Etki alanı
muhtemelen bir kuruluş tarafından işletildiğinden, yansıtılabilir
depoların makul bir ilke kümesine uymasını sağlamak için bunu
kullanabilirsiniz. Ne de olsa, anonim olmayan İnternet üzerinde I2P
üzerindekinden çok daha fazla taciz edici içerik var. Bu kadar kötü bir
yerden taciz edici içeriğin sunulmasını çok kolaylaştırmak istemeyiz.

/src/gitlab/config kapsayıcısının içindeki gitlab.rb dosyanıza aşağıdaki
satırları ekleyin. Bu ayarlar, biraz sonra yeniden başlattığınızda
geçerlilik kazanacak.

 gitlab_rails['env'] = {
 "http_proxy" => "http://172.17.0.1:4446",
 "https_proxy" => "http://172.17.0.1:4446",
 "no_proxy" => ".github.com,.gitlab.com"
 }
 gitaly['env'] = {
 "http_proxy" => "http://172.17.0.1:4446",
 "https_proxy" => "http://172.17.0.1:4446",
 "no_proxy" => "unix,.github.com,.gitlab.com"
 }
 gitlab_workhorse['env'] = {
 "http_proxy" => "http
 "https_proxy" => "http://172.17.0.1:4446",
 "no_proxy" => "unix,.github.com,.gitlab.com"
 }

### Hizmet tünellerinizi kurun ve bir sunucu adı kaydı yapın {#set-up-your-service-tunnels-and-sign-up-for-a-hostname}

GitLab yerel olarak kurulduktan sonra, I2P yöneltici panosuna gidin.
Biri 8080 TCP bağlantı noktası üzerindeki GitLab internet (HTTP)
arabirimine ve diğeri 802 TCP bağlantı noktası üzerindeki GitLab SSH
arabirimine gidişte iki sunucu tüneli kurmanız gerekecek.

#### GitLab internet (HTTP) arabirimi {#gitlab-webhttp-interface}

İnternet arayüzü için bir "HTTP" sunucu tüneli kullanın.
<http://127.0.0.1:7657/i2ptunnelmgr> adresinden "Yeni tünel
yardımcısını" başlatın ve her adımda aşağıdaki şekilde ilerleyin:

1. "Sunucu tüneli\" seçin
2. "HTTP sunucu" seçin
3. "GitLab internet hizmetini" doldurun veya tüneli başka bir şekilde
 tanımlayın
4. Sunucu olarak `127.0.0.1` ve bağlantı noktası olarak `8080` yazın.
5. "Yöneltici başlatıldığında tünel de otomatik olarak başlatılsın"
 olarak seçin
6. Seçimlerinizi doğrulayın

##### Bir sunucu adı kaydedin (isteğe bağlı) {#register-a-hostnameoptional}

I2P üzerindeki internet hizmetleri,[stats.i2p](http://stats.i2p) gibi
bir atlama hizmeti sağlayıcısına bir kimlik doğrulama dizgesi göndererek
kendilerinin sunucu adlarını kaydedebilir. Bunun için
<http://127.0.0.1:7657/i2ptunnelmgr> dosyasını yeniden açın ve az önce
kurduğunuz "GitLab internet hizmeti" ögesine tıklayın. \"Sunucu
ayarlarını düzenle\" bölümünün en altına gidin ve kayıt kimlik
doğrulaması üzerine tıklayın. Sunucu adı eklemek için kimlik doğrulaması
yazan alanı kopyalayın ve sunucu adınızı eklemek için
[stats.i2p](http://stats.i2p/i2p/addkey.html) adresine gidin. Bir alt
etki alanı kullanmak istiyorsanız (git.idk.i2p gibi) alt etki alanınız
için doğru kimlik doğrulama dizgesini kullanmanız gerektiğini unutmayın.
Bu işlem biraz daha karmaşıktır ve ayrı yönergeler yazılması gerekir.

#### GitLab SSH Arayüzü {#gitlab-ssh-interface}

SSH arayüzü için bir "Standart" sunucu tüneli kullanın.
<http://127.0.0.1:7657/i2ptunnelmgr> adresinden "Yeni tünel
yardımcısını" başlatın ve her adımda aşağıdaki şekilde ilerleyin:

1. "Sunucu tüneli\" seçin
2. "Standart sunucu" seçin
3. "GitLab SSH hizmeti" yazın veya tünele başka bir ad yazın
4. Sunucu olarak `127.0.0.1` ve bağlantı noktası olarak `8022` yazın.
5. "Yöneltici başlatıldığında tünel de otomatik olarak başlatılsın"
 olarak seçin
6. Seçimlerinizi doğrulayın

## GitLab hizmetini yeni sunucu adı ile yeniden başlatın {#re-start-the-gitlab-service-with-the-new-hostname}

Son olarak, `gitlab.rb` dosyasını değiştirdiyseniz veya bir sunucu adı
kaydettiyseniz, ayarların geçerli olması için GitLab hizmetini yeniden
başlatmanız gerekir.

 docker stop gitlab
 docker rm gitlab
 docker run --detach \
 --hostname your.hostname.i2p \
 --hostname thisisreallylongbase32hostnamewithfiftytwocharacters.b32.i2p \
 --env HTTP_PROXY=http://172.17.0.1:4446 \
 --publish 127.0.0.1:8443:443 --publish 127.0.0.1:8080:80 --publish 127.0.0.1:8022:22 \
 --name gitlab \
 --restart always \
 --volume /srv/gitlab/config:/etc/gitlab:Z \
 --volume /srv/gitlab/logs:/var/log/gitlab:Z \
 --volume /srv/gitlab/data:/var/opt/gitlab:Z \
 gitlab/gitlab-ce:latest


