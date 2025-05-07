 I2PControl -
Remote Control Service 2022-01 0.9.52 

I2P enables a [JSONRPC2](http://en.wikipedia.org/wiki/JSON-RPC)
interface via the plugin [I2PControl](). The
aim of the interface is to provide simple way to interface with a
running I2P node. A client, itoopie, has been developed in parallel. The
JSONRPC2 implementation for the client as well as the plugin is provided
by the java libraries [JSON-RPC
2.0](http://software.dzhuvinov.com/json-rpc-2.0.html). A list of
implementations of JSON-RPC for various languages can be found at [the
JSON-RPC wiki](http://json-rpc.org/wiki/implementations).

I2PControl varsayılan olarak https://localhost:7650 bağlantı noktasını
dinler

## API, 1. sürüm.

Parametreler yalnızca adlandırılmış bir şekilde sağlanır (haritalar).

#### JSON-RPC 2 biçimi

Request: { \"id\": \"id\", \"method\":
\"Method-name\", \"params\": { \"Param-key-1\": \"param-value-1\",
\"Param-key-2\": \"param-value-2\", \"Token\": \"\*\*actual token\*\*\"
}, \"jsonrpc\": \"2.0\" } Response: { \"id\": \"id\", \"result\": { \"Result-key-1\":
\"result-value-1\", \"Result-key-2\": \"result-value-2\" }, \"jsonrpc\":
\"2.0\" } 

- - Param-key-1 -- Description
 - Param-key-2 -- Description
 - Token -- Her isteğin kimliğini doğrulamak için kullanılan kod
 (\'Authenticate\' RPC yöntemi dışında)

- - Result-key-1 -- Description
 - Result-key-2 -- Description

#### Uygulanan yöntemler

- - API -- \[long\] İstemci tarafından kullanılan I2PControl API
 sürümü.
 - Password -- \[String\] Uzak sunucu üzerinde kimlik doğrulaması
 için kullanılan parola.

- - API -- \[long\] Sunucu tarafından uygulanan birincil I2PControl
 API sürümü.
 - Token -- \[String\] Sonraki iletişimler için kullanılan kod.

```{=html}
<!-- -->
```
- - Echo -- \[String\] Değer yanıt olarak döndürülür.
 - Token -- \[String\] İstemcinin kimliğini doğrulamak için
 kullanılan kod. Sunucu tarafından \'Authenticate\' RPC yöntemi
 ile sağlanır.

- - Result -- \[String\] İstekteki \'echo\' anahtarının değeri.

```{=html}
<!-- -->
```
- - Stat -- \[String\] Determines which
 rateStat to fetch, see
 [ratestats]().
 - Period -- \[long\] Milisaniye cinsinden, bir stat değerinin
 hangi dönem için alınacağını belirler.
 - Token -- \[String\] İstemcinin kimliğini doğrulamak için
 kullanılan kod. Sunucu tarafından \'Authenticate\' RPC yöntemi
 ile sağlanır.

- - Result -- \[double\] Returns the average value for the requested
 rateStat and period.

```{=html}
<!-- -->
```
- - \*i2pcontrol.address -- \[String\] I2PControl için yeni bir
 dinleme adresi ayarlar (şu anda I2PControl yalnızca 127.0.0.1 ve
 0.0.0.0 kullanıyor).
 - \*i2pcontrol.password -- \[String\] I2PControl parolasını
 değiştirir. Tüm kimlik doğrulama kodları geçersiz kılınır.
 - \*i2pcontrol.port -- \[String\] I2PControl tarafından
 bağlantıların dinleneceği bağlantı noktasını değiştirir.
 - Token -- \[String\] İstemcinin kimliğini doğrulamak için
 kullanılan kod. Sunucu tarafından \'Authenticate\' RPC yöntemi
 ile sağlanır.

- - \*\*i2pcontrol.address -- \[null\] Adres değiştirilmişse geri
 döndürür
 - \*\*i2pcontrol.password -- \[null\] Ayar değiştirilmişse geri
 döndürür
 - \*\*i2pcontrol.port -- \[null\] Ayar değiştirilmişse geri
 döndürür
 - SettingsSaved -- \[Boolean\] Herhangi bir değişiklik yapılmışsa
 true döndürür.
 - RestartNeeded -- \[Boolean\] Etkili olması için yeniden başlatma
 gerektiren herhangi bir değişiklik yapıldıysa true döndürür.

```{=html}
<!-- -->
```
- - \*i2p.router.status -- \[n/a\]
 - \*i2p.router.uptime -- \[n/a\]
 - \*i2p.router.version -- \[n/a\]
 - \*i2p.router.net.bw.inbound.1s -- \[n/a\]
 - \*i2p.router.net.bw.inbound.15s -- \[n/a\]
 - \*i2p.router.net.bw.outbound.1s -- \[n/a\]
 - \*i2p.router.net.bw.outbound.15s -- \[n/a\]
 - \*i2p.router.net.status -- \[n/a\]
 - \*i2p.router.net.tunnels.participating -- \[n/a\]
 - \*i2p.router.netdb.activepeers -- \[n/a\]
 - \*i2p.router.netdb.fastpeers -- \[n/a\]
 - \*i2p.router.netdb.highcapacitypeers -- \[n/a\]
 - \*i2p.router.netdb.isreseeding -- \[n/a\]
 - \*i2p.router.netdb.knownpeers -- \[n/a\]
 - Token -- \[String\] İstemcinin kimliğini doğrulamak için
 kullanılan kod. Sunucu tarafından \'Authenticate\' RPC yöntemi
 ile sağlanır.

- - \*\*i2p.router.status -- \[String\] Yöneltcinin durumu nedir. A
 free-format, translated string intended for display to the user.
 May include information such as whether the router is accepting
 participating tunnels. Content is implementation-dependent.
 - \*\*i2p.router.uptime -- \[long\] Milisaniye cinsinden,
 yönelticinin çalışma süresi nedir. Note: i2pd routers prior to
 version 2.41 returned this value as a string. For compatibility,
 clients should handle both string and long.
 - \*\*i2p.router.version -- \[String\] Yöneltcinin hangi I2P
 sürümünü çalıştırdığı.
 - \*\*i2p.router.net.bw.inbound.1s -- \[double\] B/sn cinsinden 1
 saniyelik ortalama geliş bant genişliği.
 - \*\*i2p.router.net.bw.inbound.15s -- \[double\] B/sn cinsinden
 15 saniyelik ortalama geliş bant genişliği.
 - \*\*i2p.router.net.bw.outbound.1s -- \[double\] B/sn cinsinden 1
 saniyelik ortalama gidiş bant genişliği.
 - \*\*i2p.router.net.bw.outbound.15s -- \[double\] B/sn cinsinden
 15 saniyelik ortalama gidiş bant genişliği.
 - \*\*i2p.router.net.status -- \[long\] Geçerli ağ durumu nedir.
 Aşağıdaki numaralandırmaya göre:
 - 0 -- OK
 - 1 -- TESTING
 - 2 -- FIREWALLED
 - 3 -- HIDDEN
 - 4 -- WARN_FIREWALLED_AND_FAST
 - 5 -- WARN_FIREWALLED_AND_FLOODFILL
 - 6 -- WARN_FIREWALLED_WITH_INBOUND_TCP
 - 7 -- WARN_FIREWALLED_WITH_UDP_DISABLED
 - 8 -- ERROR_I2CP
 - 9 -- ERROR_CLOCK_SKEW
 - 10 -- ERROR_PRIVATE_TCP_ADDRESS
 - 11 -- ERROR_SYMMETRIC_NAT
 - 12 -- ERROR_UDP_PORT_IN_USE
 - 13 -- ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL
 - 14 -- ERROR_UDP_DISABLED_AND_TCP_UNSET
 - \*\*i2p.router.net.tunnels.participating -- \[long\] I2P
 ağındaki kaç tünele katkıda bulunuyoruz.
 - \*\*i2p.router.netdb.activepeers -- \[long\] Son zamanlarda kaç
 eş ile iletişim kurduk.
 - \*\*i2p.router.netdb.fastpeers -- \[long\] Kaç eş \'hızlı\'
 olarak kabul ediliyor.
 - \*\*i2p.router.netdb.highcapacitypeers -- \[long\] Kaç eş
 \'yüksek kapasiteli\' olarak kabul ediliyor.
 - \*\*i2p.router.netdb.isreseeding -- \[boolean\] Yöneltici,
 sunucuları kendi \"Ağ veri tabanına\" (NetDB) yeniden tohumluyor
 mu?
 - \*\*i2p.router.netdb.knownpeers -- \[long\] Kaç tane eş
 biliniyor (\"Ağ veri tabanı\" (NetDB) içinde listelenmiştir).

```{=html}
<!-- -->
```
- - \*FindUpdates -- \[n/a\] **Engelleme**. İmzalı güncellemeler
 için bir arama başlatır.
 - \*Reseed -- \[n/a\] Uzak bir sunucudan \"Ağ veri tabanı\"
 (NetDB) üzerine eşler getirerek bir yöneltici yeniden
 tohumlaması başlatır.
 - \*Restart -- \[n/a\] Yönelticiyi yeniden başlatır.
 - \*RestartGraceful -- \[n/a\] Yönelticiyi sorunsuz bir şekilde
 yeniden başlatır (katkıda bulunulan tünellerin süresinin
 dolmasını bekler).
 - \*Shutdown -- \[n/a\] Yönelticiyi kapatır.
 - \*ShutdownGraceful -- \[n/a\] Yönelticiyi sorunsuz bir şekilde
 kapatır (katkıda bulunulan tünellerin süresinin dolmasını
 bekler).
 - \*Update -- \[n/a\] İmzalı kaynaklardan bir yöneltici
 güncellemesi başlatır.
 - Token -- \[String\] İstemcinin kimliğini doğrulamak için
 kullanılan kod. Sunucu tarafından \'Authenticate\' RPC yöntemi
 ile sağlanır.

- - \*\*FindUpdates -- \[boolean\] **Engelleme**. İmzalı bir
 güncelleme bulunursa true değerini döndürür.
 - \*\*Reseed -- \[null\] İstenmişse, yeniden tohumlama işleminin
 başlatıldığını doğrular.
 - \*\*Restart -- \[null\] İstenmişse, yeniden başlatma işleminin
 başlatıldığını doğrular.
 - \*\*RestartGraceful -- \[null\] İstenmişse, sorunsuz bir yeniden
 başlatma işleminin başlatıldığını doğrular.
 - \*\*Shutdown -- \[null\] İstenmişse, bir kapatma işleminin
 başlatıldığını doğrular
 - \*\*ShutdownGraceful -- \[null\] İstenmişse, sorunsuz bir
 kapatma işleminin başlatıldığını doğrular
 - \*\*Update -- \[String\] **Engelleme**. İstenmişse,
 güncellemenin durumunu döndürür

```{=html}
<!-- -->
```
- - \*i2p.router.net.ntcp.port -- \[String\] TCP taşıyıcısı için
 hangi bağlantı noktasının kullanıldığı. Null gönderilirse,
 geçerli ayarı döndürür.
 - \*i2p.router.net.ntcp.hostname -- \[String\] TCP taşıyıcısı için
 hangi sunucu adının kullanıldığı. Null gönderilirse, geçerli
 ayarı döndürür.
 - \*i2p.router.net.ntcp.autoip -- \[String\] TCP taşıyıcısı için
 otomatik olarak algılanan IP adresinin kullanılması. Null
 gönderilirse, geçerli ayarı döndürür.
 - \*i2p.router.net.ssu.port -- \[String\] UDP taşıyıcısı için
 hangi bağlantı noktasının kullanıldığı. Null gönderilirse,
 geçerli ayarı döndürür.
 - \*i2p.router.net.ssu.hostname -- \[String\] UDP taşıyıcısı için
 hangi sunucu adının kullanıldığı. Null gönderilirse, geçerli
 ayarı döndürür.
 - \*i2p.router.net.ssu.autoip -- \[String\] UDP taşıyıcısının IP
 adresini bulmak için hangi yöntemlerin kullanılması gerektiği.
 Null gönderilirse, geçerli ayarı döndürür.
 - \*i2p.router.net.ssu.detectedip -- \[null\] UDP taşıyıcısı
 tarafından hangi IP adresinin algılandığı.
 - \*i2p.router.net.upnp -- \[String\] UPnP etkin mi? Null
 gönderilirse, geçerli ayarı döndürür.
 - \*i2p.router.net.bw.share -- \[String\] Katkıda bulunulan
 tüneller için bant genişliğinin yüzde kaçının kullanılabilir
 olduğu. Null gönderilirse, geçerli ayarı döndürür.
 - \*i2p.router.net.bw.in -- \[String\] Kaç KB/sn geliş bant
 genişliğine izin verildiği. Null gönderilirse, geçerli ayarı
 döndürür.
 - \*i2p.router.net.bw.out -- \[String\] Kaç KB/sn gidiş bant
 genişliğine izin verildiği. Null gönderilirse, geçerli ayarı
 döndürür.
 - \*i2p.router.net.laptopmode -- \[String\] Dizüstü bilgisayar
 kipi etkin mi (IP değiştiğinde yöenltici kimliğini ve UDP
 bağlantı noktasını değiştirir). Null gönderilirse, geçerli ayarı
 döndürür.
 - Token -- \[String\] İstemcinin kimliğini doğrulamak için
 kullanılan kod. Sunucu tarafından \'Authenticate\' RPC yöntemi
 ile sağlanır. Null gönderilirse, geçerli ayarı döndürür.

- - Note: i2pd routers prior to version 2.41 returned some of these
 values as numbers. For compatibility, clients should handle both
 strings and numbers.
 - \*\*i2p.router.net.ntcp.port -- \[String\] İstenmişse, TCP
 taşıyıcısı için kullanılan bağlantı noktasını döndürür.
 - \*\*i2p.router.net.ntcp.hostname -- \[String\] İstenmişse, TCP
 taşıyıcısı için kullanılan sunucu adını döndürür.
 - \*\*i2p.router.net.ntcp.autoip -- \[String\] İstenmişse, TCP
 taşıyıcısı için IP adresinin otomatik olarak algılanması için
 kullanılan yöntemi döndürür.
 - \*\*i2p.router.net.ssu.port -- \[String\] İstenmişse, UDP
 taşıyıcısı için kullanılan bağlantı noktasını döndürür.
 - \*\*i2p.router.net.ssu.hostname -- \[String\] İstenmişse, UDP
 taşıyıcısı için kullanılan sunucu adını döndürür.
 - \*\*i2p.router.net.ssu.autoip -- \[String\] İstenmişse, UDP
 taşıyıcısının IP adresini algılamak için kullanılan yöntemleri
 döndürür.
 - \*\*i2p.router.net.ssu.detectedip -- \[String\] İstenmişse, UDP
 taşıyıcısı tarafından algılanan IP adresini döndürür.
 - \*\*i2p.router.net.upnp -- \[String\] İstenmişse, UPNP ayarını
 döndürür.
 - \*\*i2p.router.net.bw.share -- \[String\] İstenmişse, katkıda
 bulunulan tüneller için bant genişliğinin yüzde kaçının
 kullanılabilir olduğunu döndürür.
 - \*\*i2p.router.net.bw.in -- \[String\] İstenmişse, kaç KB/sn
 geliş bant genişliğine izin verildiğini döndürür.
 - \*\*i2p.router.net.bw.out -- \[String\] İstenmişse, kaç KB/sn
 gidiş bant genişliğine izin verildiğini döndürür.
 - \*\*i2p.router.net.laptopmode -- \[String\] İstenmişse, dizüstü
 bilgisayar kipini döndürür.
 - SettingsSaved -- \[boolean\] Belirtilen ayarlar kaydedildi mi.
 - RestartNeeded -- \[boolean\] Yeni ayarların etkin olması için
 yeniden başlatma gerekli mi?

```{=html}
<!-- -->
```
- - {\"setting-key\": \"setting-value\", \...} -- \[Map\]

- - {\"setting-key\": \"setting-value\", \...} -- \[Map\]

- - \"setting-key\" -- \[String\]

- 

\* isteğe bağlı bir değeri belirtir.

\*\* olası bir dönüş değerini belirtir

### Hata kodları

- -32700 -- JSON işleme hatası.
- -32600 -- İstek geçersiz.
- -32601 -- Yöntem bulunamadı.
- -32602 -- Parametreler geçersiz.
- -32603 -- İç sorun.

```{=html}
<!-- -->
```
- -32001 -- Belirtilen parola geçersiz.
- -32002 -- Herhangi bir kimlik doğrulama kodu belirtilmedi.
- -32003 -- Kimlik doğrulama kodu bulunamadı.
- -32004 -- Belirtilen kimlik doğrulama kodunun süresi dolmuş ve
 kaldırılacak.
- -32005 -- Kullanılan I2PControl API sürümü belirtilmemiş, ancak
 belirtilmesi gerekiyor.
- -32006 -- Belirtilen I2PControl API sürümü, I2PControl tarafından
 desteklenmiyor.


