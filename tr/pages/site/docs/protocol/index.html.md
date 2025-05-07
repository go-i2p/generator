 İletişim Kuralı
Yığını 2024-01 0.9.61 

Here is the protocol stack for I2P. See also the [Index to Technical
Documentation]().

Yığındaki katmanların her biri ek yetenekler sağlar. Yetenekleri,
iletişim kuralı yığınının altından başlayarak aşağıda görebilirsiniz.

- **İnternet Katmanı:**\
 IP: İnternet iletişim kuralı (Internet Protocol). Normal internet
 üzerindeki sunucuların adreslenmesini ve en iyi çabayı kullanarak
 internet üzerinden paketlerin yöneltilmesini sağlar.
- **Taşıyıcı Katmanı:**\
 TCP: \"Aktarım denetimi iletişim kuralı\" (Transmission Control
 Protocol), paketlerin internet üzerinden güvenilir şekilde
 gönderilmesini ve sırayla teslim edilmesini sağlar.\
 UDP: Kullanıcı veri şeması iletişim kuralı (User Datagram Protocol),
 paketlerin internet üzerinden güvenilmez şekilde, sıralamaya uymadan
 teslim edilmesini sağlar.
- **I2P taşıyıcı katmanı:**, 2 I2P yönelticisi arasında şifrelenmiş
 bağlantılar sağlar. Bunlar henüz anonim değildir ve bu kesinlikle
 bir sıçramadan sıçramaya bağlantısıdır. Bu yetenekleri sağlamak için
 iki iletişim kuralı uygulanır. NTCP2, TCP üzerinden kullanılırken,
 SSU UDP üzerinden kullanılır.\
 [NTCP2](): NIO temelli TCP\
 [SSU](): Güvenli
 yarı güvenilir UDP
- **I2P tünel katmanı:** Tam olarak şifrelenmiş tünel bağlantıları
 sağlar.\
 [Tunnel messages](): tunnel messages
 are large messages containing encrypted I2NP (see below) messages
 and encrypted instructions for their delivery. The encryption is
 layered. The first hop will decrypt the tunnel message and read a
 part. Another part can still be encrypted (with another key), so it
 will be forwarded.\
 [I2NP messages](): I2P Network Protocol
 messages are used to pass messages through multiple routers. These
 I2NP messages are combined in tunnel messages.
- **I2P Garlic katmanı:** I2P iletilerinin şifrelenmiş ve anonim
 olarak uçtan uca aktarılmasını sağlar.\
 [I2NP messages](): I2P Network Protocol
 messages are wrapped in each other and used to ensure encryption
 between two tunnels and are passed along from source to destination,
 keeping both anonymous.

Aşağıdaki katmanlar kesinlikle artık I2P iletişim kuralı yığınının bir
parçası değildir. Bunlar çekirdek \'I2P yöneltici\' işlevlerinin bir
parçası değildir. Bununla birlikte, bu katmanların her biri,
uygulamaların basit ve kullanışlı şekilde I2P kullanmasını sağlamak için
ek işlevler sunar.

**I2P istemci katmanı:** Herhangi bir istemcinin yöneltici API
uygulamasını doğrudan kullanmasına gerek kalmadan I2P işlevlerini
kullanmasını sağlar.\
[I2CP](): I2P Client Protocol, allows secure and
asynchronous messaging over I2P by communicating messages over the I2CP
TCP socket.

**I2P uçtan uca taşıma katmanı:** I2P üzerinde TCP veya UDP benzeri
işlevsellik sağlar.\
[Streaming Library](): an implementation of
TCP-like streams over I2P. This allows easier porting of existing
applications to I2P.\
[Datagram Library](): an implementation of
UDP-like messages over I2P. This allows easier porting of existing
applications to I2P.

**I2P uygulama arayüzü katmanı:** I2P üzerine uygulamaları kolaylaştıran
ek (isteğe bağlı) kitaplıklar.\
[I2PTunnel]()\
[SAMv3]()

**I2P uygulama vekil sunucu katmanı:** Vekil sunucu sistemleri.\
Son olarak, **\'I2P uygulama katmanı\'** olarak kabul edilebilecek olan,
I2P üzerinde çalışan çok sayıda uygulamadır. Bunları kullandıkları I2P
yığın katmanına göre sıralayabiliriz.

- **Streaming/veri şeması uygulamaları**: i2psnark, Syndie, i2phex\...
- **SAM uygulamaları**: IMule, i2p-bt\...
- **Other I2P
 applications**: Syndie, EepGet,
 [plugins]()\...
- **Normal uygulamalar**: Jetty, Apache, Git, tarayıcılar, e-posta\...

::: {.box style="text-align:center;"}
![I2P Network
stack](images/protocol_stack.png "I2P Network stack")\
\
Şekil 1: I2P ağ yığınının katmanları.
:::

\

\* Not: SAM hem streaming kitaplığını hem de veri şemalarını
kullanabilir.


