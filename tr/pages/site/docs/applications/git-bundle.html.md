 I2P ile GitLab
Kurmak 2020-09 0.9.47 

# I2P kaynak kodunu almak için Git paketi kullanmak {#using-a-git-bundle-to-fetch-the-i2p-source-code}

Büyük yazılım depolarını I2P üzerinden kopyalamak zor olabilir ve bazen
Git kullanmak bunu zorlaştırabilir. Neyse ki, bazen de
kolaylaştırabilir. Git üzerindeki `git bundle` komutu ile bir Git
deposunu bir dosyaya dönüştürerek yerel diskinize alabilirsiniz.
Ardından yerel diskinizdeki bu dosyadaki bulunan depoyu Git üzerine
kopyalayabilir, alabilir veya içe aktarabilirsiniz. Bu özelliği
Bittorrent indirmeleri ile birleştirerek kalan sorunlarımızı `git clone`
komutu ile çözebiliriz.

## Başlamadan önce {#before-you-start}

Bir Git paketi oluşturmayı düşünüyorsanız, MTN deposunun değil, **Git**
deposunun tam bir kopyasına zaten **sahip olmalısınız**. Bunu GitHub ya
da git.idk.i2p üzerinden alabilirsiniz. Ancak sığ bir kopya (--depth=1
ile oluşturulan bir kopya) *hiç* *çalışmaz*. Sessizce başarısız olur ve
bir dal gibi görünen bir şey oluşturur. Ancak onu kopyalamaya
çalıştığınızda başarısız olur. Bu bölüm yalnızca önceden oluşturulmuş
bir Git paketi alıyorsanız sizin için geçerli değildir.

## I2P Kaynağını Bittorrent ile Almak {#fetching-i2p-source-via-bittorrent}

Birinin, sizin için önceden oluşturduğu var olan bir `Git paketine`
karşı gelen bir torrent dosyası ya da bir magnet bağlantısı sunması
gerekir. 18 Mart 2020 Çarşamba tarihinde, ana hat i2p.i2p kaynak kodunun
yeni, doğru şekilde oluşturulmuş bir paketini, benim pastebin
[paste.idk.i2p/f/4hq37i](http://paste.idk.i2p/f/4h137i) adresimde I2P
içinde bulabilirsiniz.

Bir paketiniz olduğunda, ondan çalışan bir depo oluşturmak için Git
kullanmanız gerekir. GNU/Linux ve i2psnark kullanıyorsanız, git paketi
\$HOME/.i2p/i2psnark içinde veya Debian üzerinde bir hizmet olarak
/var/lib/i2p/i2p-config/i2psnark içinde bulunmalıdır. GNU/Linux üzerinde
BiglyBT kullanıyorsanız, bunun yerine büyük olasılıkla "\$HOME/BiglyBT
Downloads/" konumundadır. Buradaki örnekler, GNU/Linux üzerinde I2PSnark
kullandığınızı varsayıyor. Başka bir şey kullanıyorsanız, paketin yolunu
istemciniz ve platformunuz tarafından yeğlenen indirme klasörü ile
değiştirin.

### `Git kopyası` kullanmak {#using-git-clone}

Git paketinden kopyalamak kolaydır:

 git clone $HOME/.i2p/i2psnark/i2p.i2p.bundle

Aşağıdaki hatayı alırsanız, bunun yerine el ile \`\`git init\`\` ve
\`\`git fetch\`\` komutlarını kullanmayı deneyin.

 fatal: multiple updates for ref 'refs/remotes/origin/master' not allowed

### `git init` ve `git fetch` kullanmak {#using-git-init-and-git-fetch}

Öncelikle Git deposuna dönüştürmek için bir i2p.i2p klasörü oluşturun.

 mkdir i2p.i2p && cd i2p.i2p

Ardından, değişiklikleri geri almak için boş bir Git deposu hazırlayın.

 git init

Son olarak, paketten depoyu alın.

 git fetch $HOME/.i2p/i2psnark/i2p.i2p.bundle

### Paket uzak sürümünü yukarı akış uzak sürümüyle değiştirin {#replace-the-bundle-remote-with-the-upstream-remote}

Artık bir paketiniz olduğuna göre, uzaktaki sürümü yukarı akış deposu
kaynağına ayarlayarak değişikliklere ayak uydurabilirsiniz.

 git remote set-url origin git@127.0.0.1:i2p-hackers/i2p.i2p

## Paket Oluşturmak {#generating-a-bundle}

İlk olarak, i2p.i2p deposunun başarılı bir `--unshallow` klonunu elde
edene kadar [Kullanıcılar için Git rehberini](GIT.md) izleyin. Zaten bir
kopyanız varsa, bir torrent paketi oluşturmadan önce
`git fetch --unshallow` komutunu yürüttüğünüzden emin olun.

Bundan sonra, ilgili ant hedefini çalıştırmanız yeterlidir:

 ant git-bundle

ve ortaya çıkan paketi I2PSnark indirme kalsörünüze kopyalayın. Örneğin:

 cp i2p.i2p.bundle* $HOME/.i2p/i2psnark/

Bir veya iki dakika içinde I2PSnark torrenti alır. Torrenti tohumlamaya
başlamak için "Başlat" düğmesine tıklayın.


