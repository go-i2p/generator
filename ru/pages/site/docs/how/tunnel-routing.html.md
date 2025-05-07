 Маршрутизация
туннелей Июль 2011 0.8.7 

## Обзор

Эта страница содержит обзор терминологии и функционирования I2P-туннелей
со ссылками на технические страницы, подробности и спецификации.

As briefly explained in the [introduction](), I2P
builds virtual \"tunnels\" - temporary and unidirectional paths through
a sequence of routers. These tunnels are classified as either inbound
tunnels (where everything given to it goes towards the creator of the
tunnel) or outbound tunnels (where the tunnel creator shoves messages
away from them). When Alice wants to send a message to Bob, she will
(typically) send it out one of her existing outbound tunnels with
instructions for that tunnel\'s endpoint to forward it to the gateway
router for one of Bob\'s current inbound tunnels, which in turn passes
it to Bob.

![Alice connecting through her outbound tunnel to Bob via his inbound
tunnel](images/tunnelSending.png "Alice connecting through her outbound tunnel to Bob via his inbound tunnel")

 A: Выходной шлюз (Alice)
 B: Выходной участник
 C: Выходная конечная точка
 D: Входной шлюз
 E: Входной участник
 F: Входная конечная точка (Bob)

## Tunnel vocabulary

- **Tunnel gateway** - the first router in a tunnel. For inbound
 tunnels, this is the one mentioned in the LeaseSet published in the
 [network database](). For outbound tunnels,
 the gateway is the originating router. (e.g. both A and D above)
- **Конечная точка туннеля** - последний маршрутизатор в туннеле.
 (например, оба варианта C и F выше)
- **Участник туннеля** - все маршрутизаторы в туннеле, кроме шлюза или
 конечной точки (например, оба B и E выше)
- **n-Hop tunnel** - туннель с определенным количеством межмаршрутных
 переходов, например:
 - **0-hop tunnel** - туннель, в котором шлюз также является
 конечной точкой
 - **1-hop tunnel** - туннель, в котором шлюз общается
 непосредственно с конечной точкой
 - **2-(или более)-хоп туннель** - туннель, в котором есть по
 крайней мере один промежуточный участник туннеля. (приведенная
 выше схема включает два 2-хоповых туннеля - один исходящий от
 Алисы и входящий к Бобу).
- **Tunnel ID** - A [4 byte
 integer](#type_TunnelId) different
 for each hop in a tunnel, and unique among all tunnels on a router.
 Chosen randomly by the tunnel creator.

## Информация о строительстве туннеля

Routers performing the three roles (gateway, participant, endpoint) are
given different pieces of data in the initial [Tunnel Build
Message]() to accomplish their tasks:

- **Туннельный шлюз получает:**
 - **tunnel encryption key** - an [AES private
 key](#type_SessionKey) for
 encrypting messages and instructions to the next hop
 - **tunnel IV key** - an [AES private
 key](#type_SessionKey) for
 double-encrypting the IV to the next hop
 - **reply key** - an [AES public
 key](#type_SessionKey) for
 encrypting the reply to the tunnel build request
 - **reply IV** - IV для шифрования ответа на запрос построения
 туннеля
 - **tunnel id** - целое число 4 байта (только для входящих шлюзов)
 - **next hop** - какой маршрутизатор является следующим на пути
 (если только это не 0-хоп туннель, и шлюз также является
 конечной точкой)
 - **next tunnel id** - Идентификатор туннеля в следующем хопе
- **Все участники промежуточного туннеля получают:**
 - **tunnel encryption key** - an [AES private
 key](#type_SessionKey) for
 encrypting messages and instructions to the next hop
 - **tunnel IV key** - an [AES private
 key](#type_SessionKey) for
 double-encrypting the IV to the next hop
 - **reply key** - an [AES public
 key](#type_SessionKey) for
 encrypting the reply to the tunnel build request
 - **reply IV** - IV для шифрования ответа на запрос построения
 туннеля
 - **tunnel id** - 4 byte integer
 - **next hop** - what router is the next one in the path
 - **next tunnel id** - Идентификатор туннеля в следующем хопе
- **The tunnel endpoint gets:**
 - **tunnel encryption key** - an [AES private
 key](#type_SessionKey) for
 encrypting messages and instructions to the the endpoint
 (itself)
 - **tunnel IV key** - an [AES private
 key](#type_SessionKey) for
 double-encrypting the IV to the endpoint (itself)
 - **reply key** - an [AES public
 key](#type_SessionKey) for
 encrypting the reply to the tunnel build request (outbound
 endpoints only)
 - **reply IV** - the IV for encrypting the reply to the tunnel
 build request (outbound endpoints only)
 - **tunnel id** - 4 byte integer (outbound endpoints only)
 - **reply router** - the inbound gateway of the tunnel to send the
 reply through (outbound endpoints only)
 - **reply tunnel id** - The tunnel ID of the reply router
 (outbound endpoints only)

Details are in the [tunnel creation
specification]().

## Tunnel pooling

Several tunnels for a particular purpose may be grouped into a \"tunnel
pool\", as described in the [tunnel
specification](#tunnel.pooling). This
provides redundancy and additional bandwidth. The pools used by the
router itself are called \"exploratory tunnels\". The pools used by
applications are called \"client tunnels\".

## Длина туннеля {#length}

As mentioned above, each client requests that their router provide
tunnels to include at least a certain number of hops. The decision as to
how many routers to have in one\'s outbound and inbound tunnels has an
important effect upon the latency, throughput, reliability, and
anonymity provided by I2P - the more peers that messages have to go
through, the longer it takes to get there and the more likely that one
of those routers will fail prematurely. The less routers in a tunnel,
the easier it is for an adversary to mount traffic analysis attacks and
pierce someone\'s anonymity. Tunnel lengths are specified by clients via
[I2CP options](#options). The maximum number of
hops in a tunnel is 7.

### 0-прыжковые туннели

При отсутствии удаленных маршрутизаторов в туннеле у пользователя есть
очень простой способ правдоподобного отрицания (поскольку никто не знает
наверняка, что отправивший ему сообщение пир не просто переслал его как
часть туннеля). Однако довольно легко провести статистическую атаку и
заметить, что сообщения, нацеленные на определенный адрес назначения,
всегда отправляются через один шлюз. Статистический анализ исходящих
0-hop туннелей более сложен, но может показать похожую информацию (хотя
это буде несколько сложнее сделать).

### 1-прыжковые туннели

With only one remote router in a tunnel, the user has both plausible
deniability and basic anonymity, as long as they are not up against an
internal adversary (as described on [threat
model]()). However, if the adversary ran a
sufficient number of routers such that the single remote router in the
tunnel is often one of those compromised ones, they would be able to
mount the above statistical traffic analysis attack.

### 2-прыжковые туннели

При наличии двух или более удаленных маршрутизаторов в туннеле затраты
на проведение атаки анализа трафика возрастают, поскольку для ее
проведения необходимо взломать множество удаленных маршрутизаторов.

### 3-прыжковые (или более) туннели

To reduce the susceptibility to [some attacks](), 3
or more hops are recommended for the highest level of protection.
[Recent studies]() also conclude that more than 3
hops does not provide additional protection.

### Длина туннеля по умолчанию

The router uses 2-hop tunnels by default for its exploratory tunnels.
Client tunnel defaults are set by the application, using [I2CP
options](#options). Most applications use 2 or 3
hops as their default.

## Проверка туннеля {#testing}

All tunnels are periodically tested by their creator by sending a
DeliveryStatusMessage out an outbound tunnel and bound for another
inbound tunnel (testing both tunnels at once). If either fails a number
of consecutive tests, it is marked as no longer functional. If it was
used for a client\'s inbound tunnel, a new leaseSet is created. Tunnel
test failures are also reflected in the [capacity rating in the peer
profile](#capacity).

## Создание туннелей

Tunnel creation is handled by [garlic
routing]() a Tunnel Build Message to a
router, requesting that they participate in the tunnel (providing them
with all of the appropriate information, as above, along with a
certificate, which right now is a \'null\' cert, but will support
hashcash or other non-free certificates when necessary). That router
forwards the message to the next hop in the tunnel. Details are in the
[tunnel creation specification]().

## Tunnel encryption

Multi-layer encryption is handled by [garlic
encryption]() of tunnel messages. Details
are in the [tunnel specification](). The IV
of each hop is encrypted with a separate key as explained there.

## Предстоящая работа

- Можно использовать другие методы испытания туннелей, такие как
 чесночная упаковка нескольких тестов в зубчики, тестирование
 отдельных участников туннеля, участников по отдельности и т.д.
- Переход к 3-хоповым исследовательским туннелям по умолчанию.
- В одном из будущих релизов могут быть реализованы опции,
 определяющие параметры объединения, смешивания и чаф генерации.
- В одном из будущих релизов могут быть введены ограничения на
 количество и размер сообщений, разрешенных во время жизни туннеля
 (например, не более 300 сообщений или 1 МБ в минуту).

## См. также

- [Спецификация
 туннеля]()
- [Спецификация создания
 туннеля]()
- [Всенаправленные
 туннели]()
- [Спецификация туннельных
 сообщений]()
- [Чесночная
 маршрутизация]()
- [ElGamal/AES+SessionTag]()
- [Настройки
 I2CP](#options)


