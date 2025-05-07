 Bittorrent через
I2P 2024-11 0.9.64 

Существует несколько клиентов и трекеров bittorrent на I2P. Поскольку в
I2P-адресации используется адрес назначения вместо IP и порта, требуются
незначительные изменения в ПО трекера и клиента на I2P . Эти изменения
указаны ниже. Обратите внимание на рекомендации по совместимости со
старыми I2P клиентами и трекерами.

На этой странице указаны детали протокола, общие для всех клиентов и
трекеров. Конкретные клиенты и трекеры могут реализовывать другие
уникальные функции или протоколы.

Мы приветствуем дополнительные порты клиентских и трекерных программ на
I2P.

## General Guidance for Developers

Most non-Java bittorrent clients will connect to I2P via
[SAMv3](). SAM sessions (or
inside I2P, tunnel pools or sets of tunnels) are designed to be
long-lived. Most bittorrent clients will only need one session, created
at startup and closed on exit. I2P is different from Tor, where circuits
may be rapidly created and discarded. Think carefully and consult with
I2P developers before designing your application to use more than one or
two simultaneous sessions, or to rapidly create and discard them.
Bittorrent clients must not create a unique session for every
connection. Design your client to use the same session for announces and
client connections.

Also, please ensure your client settings (and guidance to users about
router settings, or router defaults if you bundle a router) will result
in your users contributing more resources to the network than they
consume. I2P is a peer-to-peer network, and the network cannot survive
if a popular application drives the network into permanent congestion.

Do not provide support for bittorrent through an I2P outproxy to the
clearnet as it will probably be blocked. Consult with outproxy operators
for guidance.

The Java I2P and i2pd router implementations are independent and have
minor differences in behavior, feature support, and defaults. Please
test your application with the latest version of both routers.

i2pd SAM is enabled by default; Java I2P SAM is not. Provide
instructions to your users on how to enable SAM in Java I2P (via
/configclients in the router console), and/or provide a good error
message to the user if the initial connect fails, e.g. \"ensure that I2P
is running and the SAM interface is enabled\".

The Java I2P and i2pd routers have different defaults for tunnel
quantities. The Java default is 2 and the i2pd default is 5. For most
low- to medium-bandwidth and low- to medium-connection counts, 3 is
sufficient. Please specify the tunnel quantity in the SESSION CREATE
message to get consistent performance with the Java I2P and i2pd
routers.

I2P supports multiple signature and encryption types. For compatibility,
I2P defaults to old and inefficient types, so all clients should specify
newer types.

If using SAM, the signature type is specified in the DEST GENERATE and
SESSION CREATE (for transient) commands. All clients should set
SIGNATURE_TYPE=7 (Ed25519).

The encryption type is specified in the SAM SESSION CREATE command or in
i2cp options. Multiple encryption types are allowed. Some trackers
support ECIES-X25519, some support ElGamal, and some support both.
Clients should set i2cp.leaseSetEncType=4,0 (for ECIES-X25519 and
ElGamal) so that they may connect to both.

DHT support requires SAM v3.3 PRIMARY and SUBSESSIONS for TCP and UDP
over the same session. This will require substantial development effort
on the client side, unless the client is written in Java. i2pd does not
currently support SAM v3.3. libtorrent does not currently support SAM
v3.3.

Without DHT support, you may wish to automatically announce to a
configurable list of known open trackers so that magnet links will work.
Consult with I2P users for information on currently-up open trackers and
keep your defaults up-to-date. Supporting the i2p_pex extension will
also help alleviate the lack of DHT support.

For more guidance to developers on ensuring your application uses only
the resources it needs, please see the [SAMv3
specification]() and [our
guide to bundling I2P with your
application]().
Contact I2P or i2pd developers for further assistance.

## Анонсы

Клиенты обычно включают в анонс фальшивый параметр port=6881 для
совместимости со старыми трекерами. Трекеры могут игнорировать параметр
порта и не должны его требовать.

The ip parameter is the base 64 of the client\'s
[Destination](#struct_Destination),
using the I2P Base 64 alphabet \[A-Z\]\[a-z\]\[0-9\]-\~.
[Destinations](#struct_Destination)
are 387+ bytes, so the Base 64 is 516+ bytes. Clients generally append
\".i2p\" to the Base 64 Destination for compatibility with older
trackers. Trackers should not require an appended \".i2p\".

Другие параметры такие же, как и в стандартном битторрент-трекере.

Текущие адреса назначения для клиентов составляют 387 или более байт
(516 или более в кодировке Base 64). Разумный максимум, который можно
принять на данный момент, - 475 байт. Поскольку трекер должен
декодировать Base64 для доставки компактных ответов (см. ниже), трекеру,
вероятно, следует декодировать и отклонять плохие Base64 при объявлении.

Тип ответа по умолчанию - некомпактный. Клиенты могут запросить
компактный ответ с помощью параметра compact=1. Трекер может, но не
обязан, вернуть компактный ответ по запросу. Note: All popular trackers
now support compact responses and at least one requires compact=1 in the
announce. All clients should request and support compact responses.

Разработчикам новых I2P клиентов настоятельно рекомендуется
реализовывать анонсы через собственный туннель, а не через клиентский
HTTP-прокси на порту 4444. Это и более эффективно, и позволяет
обеспечить соблюдение назначения трекером (см. ниже).

Не существует известных I2P клиентов или трекеров, которые в настоящее
время поддерживают UDP анонсы/ответы.

## Некомпактные ответы сервера

Некомпактный ответ - как в стандартном bittorrent, с I2P \"ip\". This is
a long base64-encoded \"DNS string\", probably with a \".i2p\" suffix.

Трекеры обычно включают ключ с фальшивым портом или используют порт из
анонса для совместимости со старыми клиентами. Клиенты должны
игнорировать параметр порта и не должны его требовать.

The value of the ip key is the base 64 of the client\'s
[Destination](#struct_Destination), as
described above. Trackers generally append \".i2p\" to the Base 64
Destination if it wasn\'t in the announce ip, for compatibility with
older clients. Clients should not require an appended \".i2p\" in the
responses.

Другие ключи и значения ответа такие же, как и в стандартном bittorrent.

## Компактные ответы сервера

In the compact response, the value of the \"peers\" dictionary key is a
single byte string, whose length is a multiple of 32 bytes. This string
contains the concatenated [32-byte SHA-256
Hashes](#type_Hash) of the binary
[Destinations](#struct_Destination) of
the peers. This hash must be computed by the tracker, unless destination
enforcement (see below) is used, in which case the hash delivered in the
X-I2P-DestHash or X-I2P-DestB32 HTTP headers may be converted to binary
and stored. The peers key may be absent, or the peers value may be
zero-length.

Хотя поддержка компактных ответов является необязательной как для
клиентов, так и для трекеров, она настоятельно рекомендуется, поскольку
она уменьшает номинальный размер ответа более чем на 90%.

## Исполнение назначения

Some, but not all, I2P bittorrent clients announce over their own
tunnels. Trackers may choose to prevent spoofing by requiring this, and
verifying the client\'s
[Destination](#struct_Destination)
using HTTP headers added by the I2PTunnel HTTP Server tunnel. The
headers are X-I2P-DestHash, X-I2P-DestB64, and X-I2P-DestB32, which are
different formats for the same information. These headers cannot be
spoofed by the client. A tracker enforcing destinations need not require
the ip announce parameter at all.

Поскольку несколько клиентов используют HTTP-прокси вместо собственного
туннеля для сообщений, усиление адреса назначения будет препятствовать
их использованию этими клиентами до тех пор, пока эти клиенты не будут
переведены на анонсирование по собственному туннелю.

К сожалению, по мере роста сети будет расти и количество вредоносных
действий, поэтому мы ожидаем, что все трекеры в конечном итоге будут
принудительно укреплять адреса назначений. И разработчики трекеров, и
разработчики клиентов должны это предвидеть.

## Объявление имен хоста

Announce URL host names in torrent files generally follow the [I2P
naming standards](). In addition to host names
from address books and \".b32.i2p\" Base 32 hostnames, the full Base 64
Destination (with \[or without?\] \".i2p\" appended) should be
supported. Non-open trackers should recognize their own host name in any
of these formats.

Чтобы сохранить анонимность, клиенты должны игнорировать URL-адреса, не
относящиеся к I2P, в торрент-файлах.

## Клиентские соединения

Соединения клиент-клиент используют стандартный протокол TCP. Нет
известных I2P-клиентов, поддерживающих uTP.

I2P uses 387+ byte
[Destinations](#struct_Destination)
for addresses, as explained above.

Если у клиента есть только хэш назначения (например, из компактного
ответа или PEX), он должен выполнить поиск кодируя его в Base 32,
добавляя \".b32.i2p\" и запрашивая Службу именования, которая вернет
полный адрес назначения, если он доступен.

Если у клиента есть полный адрес назначения пира, который он получил в
некомпактном ответе, он должен использовать его непосредственно при
установке соединения. Не преобразуйте адрес назначения обратно в хэш
Base 32 для поиска, это очень неэффективно.

## Предотвращение межсетевых запросов

Чтобы сохранить анонимность, I2P битторрент-клиенты обычно не
поддерживают анонсы или пиринговые соединения, не относящиеся к I2P. I2P
HTTP аутпрокси часто блокируют анонсы. Не существует известных
SOCKS-аутпрокси, поддерживающих трафик битторрента.

Чтобы предотвратить использование не I2P клиентами через HTTP inproxy,
I2P трекеры часто блокируют доступы или анонсы, содержащие
HTTP-заголовок X-Forwarded-For. Трекеры должны отклонять стандартные
сетевые анонсы с IPv4 или IPv6 IP, и не передавать их в ответах.

## PEX

I2P PEX is based on ut_pex. As there does not appear to be a formal
specification of ut_pex available, it may be necessary to review the
libtorrent source for assistance. It is an extension message, identified
as \"i2p_pex\" in [the extension
handshake](http://www.bittorrent.org/beps/bep_0010.html). It contains a
bencoded dictionary with up to 3 keys, \"added\", \"added.f\", and
\"dropped\". The added and dropped values are each a single byte string,
whose length is a multiple of 32 bytes. These byte strings are the
concatenated SHA-256 Hashes of the binary
[Destinations](#struct_Destination) of
the peers. This is the same format as the peers dictionary value in the
i2p compact response format specified above. The added.f value, if
present, is the same as in ut_pex.

## DHT

Поддержка DHT включена в клиент i2psnark начиная с версии 0.9.2..
Предварительные отличия от [BEP
5](http://www.bittorrent.org/beps/bep_0005.html) описаны ниже и могут
быть изменены. Свяжитесь с разработчиками I2P, если вы хотите
разработать клиент с поддержкой DHT.

В отличие от стандартного DHT, I2P DHT не использует бит в квитировании
опций или в сообщении PORT. Он рекламируется с помощью сообщения
расширения, идентифицируемого как \"i2p_dht\" в [the extension
handshake](http://www.bittorrent.org/beps/bep_0010.html). Он содержит
кодированный словарь с двумя ключами, \"port\" и \"rport\", оба целые
числа.



The UDP (datagram) port listed in the compact node info is used to
receive repliable (signed) datagrams. This is used for queries, except
for announces. We call this the \"query port\". This is the \"port\"
value from the extension message. Queries use
[I2CP]() protocol number 17.

In addition to that UDP port, we use a second datagram port equal to the
query port + 1. This is used to receive unsigned (raw) datagrams for
replies, errors, and announces. This port provides increased efficiency
since replies contain tokens sent in the query, and need not be signed.
We call this the \"response port\". This is the \"rport\" value from the
extension message. It must be 1 + the query port. Responses and
announces use [I2CP]() protocol number 18.

Информация о компактном пире составляет 32 байта (32-байтовый SHA256
хэш) вместо 4 байт IP + 2 байт порт. Порт пира отсутствует. В ответе
ключ \"values\" представляет собой список строк, каждая из которых
содержит одну компактную информацию о пире.

Информация о компактном узле составляет 54 байта (20 байт Node ID + 32
байта SHA256 Hash + 2 байта port) вместо 20 байт Node ID + 4 байта IP +
2 байта порт. В ответе ключ \"узлы\" представляет собой однобайтовую
строку с конкатенированной компактной информацией об узле.

Требование к идентификатору защищенного узла: Чтобы затруднить различные
атаки DHT, первые 4 байта идентификатора узла должны совпадать с первыми
4 байтами хэша назначения, а следующие два байта идентификатора узла
должны совпадать со следующими двумя байтами хэша назначения,
exclusive-ORed с портом.

В торрент-файле ключ \"узлов\" словаря безтрекерного торрента является
TBD. Это может быть список 32-байтовых двоичных строк (SHA256 хэшей)
вместо списка списков содержащий строку хоста и целое число порта.
Альтернативы: Однобайтовая строка с конкатенированными хэшами, или
только список строк.

## Дейтаграм (UDP) трекеры

Поддержка UDP-трекеров в клиентах и трекерах пока недоступна.
Предварительные отличия от [BEP
15](http://www.bittorrent.org/beps/bep_0015.html) описаны ниже и могут
быть изменены. Свяжитесь с разработчиками I2P, если вы хотите
разработать клиент или трекер, поддерживающий анонсы дейтаграмм.

See [Proposal 160]().

## Дополнительная информация

- I2P bittorrent standards are generally discussed on [](http:///).
- A chart of current tracker software capabilities is [also available
 there](http:///files/trackers.html).
- The [I2P bittorrent
 FAQ](http:///viewtopic.php?t=2068)
- [DHT on I2P discussion](http:///topics/812)


