 Чесночная
маршрутизация Март 2014 0.9.12 

## Чесночная маршрутизация и \"Чесночная\" терминология

Термины \"чесночная маршрутизация\" и \"чесночное шифрование\" часто
используются довольно свободно, когда речь идет о технологии I2P. Здесь
мы объясняем историю терминов, различные значения и использование
\"чесночных\" методов в I2P.

Термин \"чесночная маршрутизация\" был впервые введен в обиход [Майклом
Дж. Фридманом](http://www.cs.princeton.edu/~mfreed/) в журнале Роджера
Дингледайна \"Free Haven\". [Магистерская
диссертация](http://www.freehaven.net/papers.html) Раздел 8.1.1 (июнь
2000 г.), как производное из [Луковой
маршрутизации](http://www.onion-router.net/).

Возможно, \"чеснок\" изначально использовался разработчиками I2P, потому
что I2P реализует форму комплектации, как описывает Фридман, или просто
чтобы подчеркнуть общие отличия от Tor. Конкретные причины образования
термина не сохранились. В целом, когда речь идет об I2P, термин
\"чеснок\" может означать одну из трех вещей:

1. Многоуровневое шифрование
2. Объединение вместе нескольких сообщений
3. Шифрование ElGamal/AES

К сожалению, использование I2P терминологии \"чеснок\" за последние семь
лет не всегда было точным, поэтому читатель должен быть внимателен при
взаимодействии с этим термином. Надеемся, что приведенное ниже
объяснение прояснит ситуацию.

### Многоуровневое шифрование

Луковая маршрутизация - это техника построения путей, или туннелей,
через серию пиров, а затем использование этого туннеля. Сообщения
многократно шифруются отправителем, а затем расшифровываются при каждом
прыжке. Во время фазы построения, только инструкции маршрутизации для
следующего прыжка доступны каждому пиру. На этапе эксплуатации сообщения
передаются через туннель, и сообщение и инструкции по его маршрутизации
доступны только для конечной точки туннеля.

This is similar to the way Mixmaster (see [network
comparisons]()) sends messages - taking a
message, encrypting it to the recipient\'s public key, taking that
encrypted message and encrypting it (along with instructions specifying
the next hop), and then taking that resulting encrypted message and so
on, until it has one layer of encryption per hop along the path.

В этом смысле \"чесночная маршрутизация\" как общая концепция идентична
\"луковой маршрутизации\". Конечно, в том виде, в котором она
реализована в I2P, есть несколько отличий от реализации в Tor; см. ниже.
Тем не менее, есть и существенные сходства, так что I2P получает пользу
от [большое количество академических исследований по луковой
маршрутизации](http://www.onion-router.net/Publications.html) , [Tor и
аналогичных сетей](http://freehaven.net/anonbib/topic.html).

### Упаковка нескольких сообщений

Майкл Фридман определил \"чесночную маршрутизацию\" как расширение
луковой маршрутизации, в которой несколько сообщений объединяются
вместе. Он назвал каждое сообщение \"луковицей\". Все сообщения, каждое
со своими инструкциями по доставке, открываются в конечной точке. Это
позволяет эффективно объединять \"ответный блок\" луковой маршрутизации
с исходным сообщением.

Эта концепция реализована в I2P, как описано ниже. Мы называем
\"луковицы\" чеснока \"зубчиками\". Может быть упаковано любое
количество сообщений может быть не только одно. Это существенное отличие
от луковой маршрутизации, реализованной в Tor. Однако это лишь одно из
многих значительных архитектурных различий между I2P и Tor; Возможно,
само по себе оно не является достаточным для того, чтобы оправдать
изменение терминологии.

Еще одно отличие от метода, описанного Фридманом заключается в том, что
путь однонаправленный: нет \"поворотной точки\", как это бывает в
луковой маршрутизации или ответных блоков mixmaster, что значительно
упрощает алгоритм и обеспечивает более гибкую и надежную доставку.

### Шифрование ElGamal/AES

In some cases, \"garlic encryption\" may simply mean
[ElGamal/AES+SessionTag]() encryption
(without multiple layers).

## \"Чесночные\" методы в I2P

Теперь, когда мы дали определение различным \"чесночным\" терминам, мы
можем сказать, что I2P использует чесночную маршрутизацию, упаковку и
шифрование в трех местах:

1. Для создания и маршрутизации через туннели (многоуровневое
 шифрование)
2. Для определения успеха или неудачи доставки сообщения до получателя
 (упаковка)
3. За публикацию некоторых записей сетевой базы данных (уменьшение
 вероятности успешной атаки для анализа трафика) (ElGamal/AES)

Существует также множество способов использования этой техники для
улучшения производительности сети, таких как использование компромиссов
между задержкой/пропускной способностью транспорта и разветвление данных
по избыточным путям для повышения надежности.

### Постройка и маршрутизация туннелей

В I2P туннели являются однонаправленными. Каждая сторона строит два
туннеля, один для исходящего и один для входящего трафика. Поэтому для
передачи одного сообщения и ответа в обе стороны требуется четыре
туннеля.

Tunnels are built, and then used, with layered encryption. This is
described on the [tunnel implementation
page](). Tunnel building details are defined
on [this page](). We use
[ElGamal/AES+SessionTag]() for the
encryption.

Tunnels are a general-purpose mechanism to transport all [I2NP
messages](), and [Garlic
Messages](#msg_Garlic) are not used to build
tunnels. We do not bundle multiple [I2NP
messages]() into a single [Garlic
Message](#msg_Garlic) for unwrapping at the
outbound tunnel endpoint; the tunnel encryption is sufficient.

### Объединение сквозных сообщений

At the layer above tunnels, I2P delivers end-to-end messages between
[Destinations](#struct_Destination).
Just as within a single tunnel, we use
[ElGamal/AES+SessionTag]() for the
encryption. Each client message as delivered to the router through the
[I2CP interface]() becomes a single [Garlic
Clove](#struct_GarlicClove) with its own
[Delivery
Instructions](#struct_GarlicCloveDeliveryInstructions),
inside a [Garlic Message](#msg_Garlic).
Delivery Instructions may specify a Destination, Router, or Tunnel.

Как правило, сообщение Garlic Message содержит только один зубчик..
Однако маршрутизатор будет периодически связывать два дополнительных
зубчика в Чесночное сообщение:

![Garlic Message
Cloves](/_static/images/garliccloves.png "Garlic Message Cloves"){style="text-align:center;"}

1. A [Delivery Status
 Message](#msg_DeliveryStatus), with
 [Delivery
 Instructions](#struct_GarlicCloveDeliveryInstructions)
 specifying that it be sent back to the originating router as an
 acknowledgment. This is similar to the \"reply block\" or \"reply
 onion\" described in the references. It is used for determining the
 success or failure of end to end message delivery. The originating
 router may, upon failure to receive the Delivery Status Message
 within the expected time period, modify the routing to the far-end
 Destination, or take other actions.
2. A [Database Store
 Message](#msg_DatabaseStore), containing a
 [LeaseSet](#struct_LeaseSet) for
 the originating Destination, with [Delivery
 Instructions](#struct_GarlicCloveDeliveryInstructions)
 specifying the far-end destination\'s router. By periodically
 bundling a LeaseSet, the router ensures that the far-end will be
 able to maintain communications. Otherwise the far-end would have to
 query a floodfill router for the network database entry, and all
 LeaseSets would have to be published to the network database, as
 explained on the [network database page]().

By default, the Delivery Status and Database Store Messages are bundled
when the local LeaseSet changes, when additional [Session
Tags](#type_SessionTag) are delivered,
or if the messages have not been bundled in the previous minute. As of
release 0.9.2, the client may configure the default number of Session
Tags to send and the low tag threshold for the current session. See the
[I2CP options specification](#options) for
details. The session settings may also be overridden on a per-message
basis. See the [I2CP Send Message Expires
specification](#msg_SendMessageExpires) for
details.

Очевидно, что в настоящее время дополнительные сообщения объединяются
для конкретных целей, и не являются частью схемы маршрутизации общего
назначения.

Начиная с версии 0.9.12, сообщение о статусе доставки заворачивается
отправителем в другое чесночное сообщение, чтобы содержимое было
зашифровано и не было видно маршрутизаторам на обратном пути.

### Хранение в базе данных сети наводнений

As explained on the [network database
page](#delivery), local
[LeaseSets](#struct_LeaseSet) are sent
to floodfill routers in a [Database Store
Message](#msg_DatabaseStore) wrapped in a
[Garlic Message](#msg_Garlic) so it is not
visible to the tunnel\'s outbound gateway.

## Предстоящая работа

The Garlic Message mechanism is very flexible and provides a structure
for implementing many types of mixnet delivery methods. Together with
the unused delay option in the [tunnel message Delivery
Instructions](#struct_TunnelMessageDeliveryInstructions),
a wide spectrum of batching, delay, mixing, and routing strategies are
possible.

В частности, существует потенциал для гораздо большей гибкости в
конечной точке исходящего туннеля. Сообщения могут быть направлены в
один из нескольких туннелей (таким образом, минимизируя соединения
\"точка-точка\"), или многоадресную рассылку в несколько туннелей для
избыточности, или потоковое аудио и видео.

Such experiments may conflict with the need to ensure security and
anonymity, such as limiting certain routing paths, restricting the types
of I2NP messages that may be forwarded along various paths, and
enforcing certain message expiration times.

As a part of [ElGamal/AES encryption](), a
garlic message contains a sender specified amount of padding data,
allowing the sender to take active countermeasures against traffic
analysis. This is not currently used, beyond the requirement to pad to a
multiple of 16 bytes.

Encryption of additional messages to and from the [floodfill
routers](#delivery).

## Ссылки

- The term garlic routing was first coined in Roger Dingledine\'s Free
 Haven [Master\'s thesis](http://www.freehaven.net/papers.html) (June
 2000), see Section 8.1.1 authored by [Michael J.
 Freedman](http://www.cs.princeton.edu/~mfreed/).
- [Публикации о луковой
 маршрутизации](http://www.onion-router.net/Publications.html)
- [Луковая маршрутизация в
 Википедии](http://en.wikipedia.org/wiki/Onion_routing)
- [Чесночная маршрутизация в
 Википедии](http://en.wikipedia.org/wiki/Garlic_routing)
- [I2P Meeting 58]() (2003) discussing the
 implementation of garlic routing
- [Tor](https://www.torproject.org/)
- [Публикации проекта Free
 Haven](http://freehaven.net/anonbib/topic.html)
- Луковая маршрутизация была впервые описана в работе [Hiding Routing
 Information](http://www.onion-router.net/Publications/IH-1996.pdf)
 Дэвида Голдшлага, Майкла Рида и Пола Сиверсона в 1996 году.


