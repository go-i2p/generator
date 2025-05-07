 IRC Uygulamasını
Yapılandırmak 2020-11
0.9.47 

# IRC Uygulaması

- [Clients](#clients)
- [Servers](#servers)

[]{#clients}

## İstemciler

There are many IRC clients that can be used with I2P. In fact, all IRC
clients can be connected to the Irc2P Service by connecting them to the
IRC Tunnel.

- [Pidgin(Windows, Linux) Adium(OSX)](#pidgin)
- [XChat(Windows, Linux) XChat Aqua(OSX)](#xchat)
- [Thunderbird(Windows, Linux, OSX)](#thunderbird)
- [Revolution IRC(Android)](#revolution)
- [Dispatch(Windows, Linux, OSX)(WebClient)](#dispatch)

### Check the IRC tunnel

Herhangi bir IRC istemcisini Irc2P üzerinde sohbet edecek şekilde
yapılandırmak için önce IRC tünelinizin kullanılabilir olduğundan emin
olun. [Gizli hizmet yönetimi](http://127.0.0.1:7657/i2ptunnel/) bölümüne
gidin ve \"İstemci tünelleri\" bölümünde Irc2P seçeneğini arayın. Sağ
taraftaki \"Durum\" göstergesi sarı ya da yeşil ise Irc2P tüneliniz
hazırdır ve bir sonraki adıma geçebilirsiniz.

![IRC Tunnel
Check](images/irc/tuncheck-irc-all.png "IRC Tunnel Check")

Bu IRC tüneline herhangi bir IRC istemcisi bağlanabilir. Sık kullanılan
birkaç istemci için ayrıntılı yönergeleri aşağıda bulabilirsiniz.

[]{#pidgin}

### Pidgin

Pidgin is a very popular Instant Messaging client with built-in IRC
support. It is also possible to use it with many other kinds of chat
service, and it supports using multiple accounts at once and has a
variety of plugin-ins. There is a similar application for OSX called
\"Adium.\" The instructions for Pidgin are similar in Adium.

![Open the
menu](images/irc/pidgin-irc-0.png "Pidgin Step One")

Pidgin uygulamasını başlattıktan sonra bir \"Arkadaş listesi\" penceresi
görmelisiniz. Bu penceredeki araç çubuğundan \"Hesaplar\" menüsünü açın.
I2P hesabınızı yapılandırmaya başlamak için \"Hesap yönetimi\" üzerine
tıklayın.

![Add the
account](images/irc/pidgin-irc-1.png "Pidgin Step Two")

\"Ekle\" düğmesine tıklayın. Açılan pencerede, \"İletişim kuralı\"
altından \"IRC\" seçin ve \"Sunucu\" olarak 127.0.0.1 yazın. Ardından
bir kullanıcı adı ve parola seçin. IRC, üzerine katılmanız için bir
takma ad kaydetmeniz zorunlu değildir. Ancak dilerseniz Irc2P bağlantısı
kurduktan sonra bunu yapabilirsiniz.

![Configure username, hostname,
password](images/irc/pidgin-irc-2.png "Pidgin Step Three")

\"Gelişmiş\" sekmesine gidin ve \"Bağlantı noktası\" alanına 6668 yazın.
Tüneliniz I2P tarafından sağlanan şifrelemeyi kullandığından SSL
seçeneğinin *devre dışı* bırakılmış olduğundan emin olun.

![Configure
port](images/irc/pidgin-irc-3.png "Pidgin Step Four")
[]{#xchat}

### XChat

XChat sunucu listesi menüsünü açın ve \"Ekle\" düğmesine tıklayın.

![Add a
server](images/irc/xchat-irc-0.png "XChat Step One")

Create a new network named \"Irc2P\" to configure for I2P IRC. Click the
\"Edit\" button on the right-hand side. Make sure you disable TLS and
SSL inside I2P.

![Add a
server](images/irc/xchat-irc-1.png "XChat Step Two")

Change the value in \"Servers\" from the default to \`localhost/6668\`,
and configure the default channels you want to join. I suggest #i2p and
#i2p-dev

![Add a
server](images/irc/xchat-irc-2.png "XChat Step Three")

Sunucu listesine dönmek için \"Edit server\" penceresini kapatın ve
I2PRC bağlantısı kurmak için \"Bağlan\"\' üzerine tıklayın.

![Add a
server](images/irc/xchat-irc-3.png "XChat Step Four")
[]{#thunderbird}

### Thunderbird

Thunderbird penceresinin üst kısmındaki araç çubuğundan \"Sohbet\"
düğmesine tıklayın.

![Add a
chat](images/irc/thunderbird-irc-0.png "Thunderbird Step One")

Irc2P kurmak için Başla düğmesine tıklayın.

![Get
Started](images/irc/thunderbird-irc-1.png "Thunderbird Step Two")

Birinci adımda ağ türü olarak \"IRC\" seçin.

![Pick
IRC](images/irc/thunderbird-irc-2.png "Thunderbird Step Three")

Bir takma ad seçin ve IRC sunucunuzu 127.0.0.1 olarak ayarlayın, ancak
bir bağlantı noktası belirtmeyin.

![Set username and
server](images/irc/thunderbird-irc-3.png "Thunderbird Step Four")

İstiyorsanız bir parola ayarlayın.

![Add a
server](images/irc/thunderbird-irc-4.png "Thunderbird Step Five")

IRC sunucusunu \"Irc2P\" gibi bir takma adla yapılandırın ve bağlantı
noktasını 6668 olarak ayarlayın.

![Add a
server](images/irc/thunderbird-irc-5.png "Thunderbird Step Six")

Özetiniz böyle görünüyorsa Irc2P bağlantısı kurmaya hazırsınız
demektir..

![Add a
server](images/irc/thunderbird-irc-6.png "Thunderbird Step Seven")
[]{#revolution}

### Revolution IRC

Revolution IRC, Android için kullanımı kolay bir IRC istemcisidir.
Birden çok hizmette birden çok hesabı yönetebilir. Böylece Irc2P ve I2P
olmayan IRC ağlarınız için de kullanabilirsiniz.

I2P ile Revolution IRC yapılandırmasına başlamak için köşedeki \"Sunucu
ekle\" düğmesine (\`+\` şeklinde) tıklayın.

![Add a
server](images/irc/revolution-irc-0.png "Revolution Step One")

Sunucu adını yazın, adresi \"127.0.0.1\" ve bağlantı noktasını 6668
olarak değiştirin.

![Configure it like
this](images/irc/revolution-irc-1.png "Revolution Step Two")

Kendinize bir takma ad verin ve bazı kanallara otomatik olarak
katılınacak şekilde yapılandırın.

![Open the
menu](images/irc/revolution-irc-2.png "Revolution Step Three")
[]{#dispatch}

### Dispatch

Dispatch, internet arayüzüne sahip, kararlı, kendinizin
barındırabileceği bir IRC istemcisidir. Üzerinden iletişim kurarak
kullanılabilen yerel I2P yapılandırmasına sahiptir. [SAM v3
API]().

Dispatch genel ayarları \`config.toml\` dosyası içinden yapılır.

 # Defaults for the client connect form
 [defaults]
 name = "myinvisibleirc.i2p"
 host = "anircservergoeshere.b32.i2p"
 port = 6667
 channels = [
 "#i2p",
 "#i2p-dev"
 ]
 server_password = ""
 ssl = false

[]{#servers}

## Sunucular

- [Eris(Windows, OSX, Linux)](#eris)

[]{#eris}

### Eris

Eris, I2P için kendi kendini yapılandırabilen, ve kolay yapılandırılan
bir IRC sunucusudur. Özel bir IRC sunucusu işletmek istiyorsanız, en
kolay yollardan biridir.

This is a valid configuration of the Eris IRC server, but it uses a
default password for the admin account(admin). You should change the
operator.admin.password and account.admin.password before deploying to a
real service.

 mutex: {}
 network:
 name: Local
 server:
 password: ""
 listen: []
 tlslisten: {}
 i2plisten:
 invisibleirc:
 i2pkeys: iirc
 samaddr: 127.0.0.1:7656
 log: ""
 motd: ircd.motd
 name: myinvisibleirc.i2p
 description: Hidden IRC Services
 operator:
 admin:
 password: JDJhJDA0JE1vZmwxZC9YTXBhZ3RWT2xBbkNwZnV3R2N6VFUwQUI0RUJRVXRBRHliZVVoa0VYMnlIaGsu
 account:
 admin:
 password: JDJhJDA0JGtUU1JVc1JOUy9DbEh1WEdvYVlMdGVnclp6YnA3NDBOZGY1WUZhdTZtRzVmb1VKdXQ5ckZD
 www: 
 listen: []
 tlslisten: {}
 i2plisten:
 i2pinfoirc:
 i2pkeys: iircwww
 samaddr: "127.0.0.1:7656"
 templatedir: lang


