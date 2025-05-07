 Протокол потоковой
передачи 2024-09 0.9.64 

## Обзор

The streaming library is technically part of the \"application\" layer,
as it is not a core router function. In practice, however, it provides a
vital function for almost all existing I2P applications, by providing a
TCP-like streams over I2P, and allowing existing apps to be easily
ported to I2P. The other end-to-end transport library for client
communication is the [datagram library]().

The streaming library is a layer on top of the core [I2CP
API]() that allows reliable, in-order, and
authenticated streams of messages to operate across an unreliable,
unordered, and unauthenticated message layer. Just like the TCP to IP
relationship, this streaming functionality has a whole series of
tradeoffs and optimizations available, but rather than embed that
functionality into the base I2P code, it has been factored off into its
own library both to keep the TCP-esque complexities separate and to
allow alternative optimized implementations.

Учитывая относительно высокую стоимость сообщений, протокол потоковой
библиотеки для планирования и доставки этих сообщений был оптимизирован
таким образом, чтобы отдельные передаваемые сообщения содержали столько
информации, сколько доступно. Например, небольшая транзакция HTTP,
проксируемая через потоковую библиотеку, может быть завершена за один
цикл - первые сообщения содержат SYN, FIN небольшую полезную нагрузку
HTTP запроса, а ответ содержит SYN, FIN, ACK и полезную нагрузку HTTP
ответа. Чтобы сообщить HTTP-серверу о получении SYN/FIN/ACK, необходимо
передать дополнительный ACK, а локальный HTTP-прокси часто может
немедленно доставить полный ответ браузеру.

Потоковая библиотека очень похожа на абстракцию TCP, с его скользящими
окнами, алгоритмами контроля перегрузки (медленный старт и
предотвращение перегрузки) и общим поведением пакетов (ACK, SYN, FIN,
RST, вычисление rto и т.д.).

Потоковая библиотека является надежной библиотекой, которая
оптимизирована для работы через I2P. Она имеет однофазную настройку, и
содержит полную реализацию оконного режима.

## API

The streaming library API provides a standard socket paradigm to Java
applications. The lower-level [I2CP]() API is
completely hidden, except that applications may pass [I2CP
parameters](#options) through the streaming
library, to be interpreted by I2CP.

The standard interface to the streaming lib is for the application to
use the [I2PSocketManagerFactory]() to create
an [I2PSocketManager](). The application then
asks the socket manager for an [I2PSession](),
which will cause a connection to the router via
[I2CP](). The application can then setup
connections with an [I2PSocket]() or receive
connections with an [I2PServerSocket]().

Here are the [full streaming library Javadocs]().

Хорошие примеры использования вы можете найти, взглянув на код i2psnark.

### Опции и настройки по умолчанию {#options}

The options and current default values are listed below. Options are
case-sensitive and may be set for the whole router, for a particular
client, or for an individual socket on a per-connection basis. Many
values are tuned for HTTP performance over typical I2P conditions. Other
applications such as peer-to-peer services are strongly encouraged to
modify as necessary, by setting the options and passing them via the
call to
[I2PSocketManagerFactory]().createManager(\_i2cpHost,
\_i2cpPort, opts). Time values are in ms.

Note that higher-layer APIs, such as [SAM](),
[BOB](), and
[I2PTunnel](), may override these defaults
with their own defaults. Also note that many options only apply to
servers listening for incoming connections.

Начиная с версии 0.9.1, большинство, но не все, опции могут быть
изменены на активном менеджере сокетов или сессии. Подробности см. в
javadocs.

 Option Default Notes
 --------------------------------------------------- ------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 i2cp.accessList null Разделенный запятыми или пробелами список пиринговых хэшей Base64, используются для списка доступа или черного списка. As of release .
 i2cp.destination.sigType DSA_SHA1 Используйте список доступа в качестве белого списка для входящих соединений. Имя или номер типа подписи для переходного пункта назначения. As of release .
 i2cp.enableAccessList false Используйте список доступа в качестве белого списка для входящих соединений. As of release .
 i2cp.enableBlackList false Используйте список доступа в качестве черного списка для входящих соединений. As of release .
 i2p.streaming.answerPings true Отвечать ли на входящие ping-запросы
 i2p.streaming.blacklist null Список пиринговых хэшей Base64, разделенных запятыми или пробелами должны быть в черном списке для входящих соединений со ВСЕМИ пунктами назначения в контексте. Эта опция должна быть установлена в свойствах контекста, а НЕ в аргументе опций createManager(). Обратите внимание, что установка этого параметра в контексте маршрутизатора не повлияет на клиентов за пределами маршрутизатора в отдельной JVM и контексте. As of release .
 i2p.streaming.bufferSize 64K Сколько данных передачи (в байтах) будет принято, которые еще не были записаны.
 i2p.streaming.congestionAvoidanceGrowthRateFactor 1 Когда мы находимся в режиме предотвращения перегрузки, мы увеличиваем размер окна со скоростью `1/(windowSize*factor)`. В стандартном TCP, размер окна указывается в байтах, а в I2P - в сообщениях. Большее число означает более медленный рост.
 i2p.streaming.connectDelay -1 Как долго нужно ждать после инстанцирования нового con перед попыткой подключения. Если это значение \<= 0, соединение происходит немедленно без начальных данных. Если больше 0, подождите, пока выходной поток не будет очищен, буфер не заполнится или пока не пройдет много миллисекунд, и включите любые начальные данные в SYN.
 i2p.streaming.connectTimeout 5\*60\*1000 Сколько блокировать при подключении, в миллисекундах. Отрицательное значение означает бесконечно. По умолчанию - 5 минут.
 i2p.streaming.disableRejectLogging false Отключать ли предупреждения в журналах, когда входящее соединение отклоняется из-за ограничений соединения. As of release .
 i2p.streaming.dsalist null Список разделенных запятыми или пробелами хэшей пиров Base64 или имен хостов, с будет связан, используя альтернативное место назначения DSA. Применимо, только если включена мультисессия и основная сессия не является DSA (обычно только для общих клиентов). Этот параметр должен быть установлен в свойствах контекста, а не в аргументе опций createManager(). Обратите внимание, что установка этого параметра в контексте маршрутизатора не повлияет на клиентов вне маршрутизатора в отдельной JVM и контексте. As of release .
 i2p.streaming.enforceProtocol true Слушая ли только потоковый протокол. Установка значения true запрещает взаимодействие с Каталогами, выпущенными ранее версии 0.7.1 (выпущена в марте 2009 года). Установите значение true, если на этом Каталоге несколько протоколов. As of release . Default true as of release 0.9.36.
 i2p.streaming.inactivityAction 2 (send) (0=отказ, 1=разъединение). Что делать при неактивном таймауте - ничего, отключиться или послать дубликат ack.
 i2p.streaming.inactivityTimeout 90\*1000 Время простоя перед отправкой keepalive
 i2p.streaming.initialAckDelay 750 Задержка перед отправкой запроса
 i2p.streaming.initialResendDelay 1000 Начальное значение поля задержки повторной отправки в заголовке пакета, умноженное на 1000. Реализовано не полностью; см. ниже.
 i2p.streaming.initialRTO 9000 Начальный тайм-аут (при отсутствии [данных совместного доступа](#sharing)). As of release .
 i2p.streaming.initialRTT 8000 Первоначальная оценка времени поездки туда и обратно (если нет [данных о совместном использовании](#sharing)). Отключено в версии 0.9.8; используется фактическое RTT.
 i2p.streaming.initialWindowSize 6 (при отсутствии [данных совместного доступа](#sharing)) В стандартном TCP размер окна - в байтах, а в I2P размер окна - в сообщениях.
 i2p.streaming.limitAction reset What action to take when an incoming connection exceeds limits. Valid values are: reset (reset the connection); drop (drop the connection); or http (send a hardcoded HTTP 429 response). Any other value is a custom response to be sent. backslash-r and backslash-n will be replaced with CR and LF. As of release .
 i2p.streaming.maxConcurrentStreams -1 (0 или отрицательное значение означает неограниченность) Это общий лимит для входящих и исходящих данных вместе взятых.
 i2p.streaming.maxConnsPerMinute 0 Лимит входящих соединений (для каждого пира; 0 означает отключено) As of release .
 i2p.streaming.maxConnsPerHour 0 (для каждого пира; 0 означает отключено) As of release .
 i2p.streaming.maxConnsPerDay 0 (для каждого пира; 0 означает отключено) As of release .
 i2p.streaming.maxMessageSize 1730 Максимальный размер полезной нагрузки, т.е. MTU в байтах.
 i2p.streaming.maxResends 8 Максимально количество повторных передач перед отказом.
 i2p.streaming.maxTotalConnsPerMinute 0 Лимит входящих соединений (для всех узлов; 0 снимает лимит) As of release .
 i2p.streaming.maxTotalConnsPerHour 0 (все пиры; 0 означает отключен). Будьте осторожны, так как превышение этого значения может отключить сервер на длительное время. As of release .
 i2p.streaming.maxTotalConnsPerDay 0 (все пиры; 0 означает отключен). Будьте осторожны, так как превышение этого значения может отключить сервер на длительное время. As of release .
 i2p.streaming.maxWindowSize 128 
 i2p.streaming.profile 1 (bulk) 1=bulk; 2=interactive; see important notes [below](#profile).
 i2p.streaming.readTimeout -1 Сколько блокировать чтение, в миллисекундах. Отрицательное значение означает неопределенно долго.
 i2p.streaming.slowStartGrowthRateFactor 1 Когда мы в режиме медленного запуска, мы увеличиваем размер окна со скоростью 1/(коэффициент). В стандартном TCP размер окна выражается в байтах, а в I2P - в сообщениях. Большее число означает более медленный рост.
 i2p.streaming.tcbcache.rttDampening 0.75 Ссылка: RFC 2140. Значение с плавающей точкой. Может быть установлено только через свойства контекста, но не через параметры соединения. As of release .
 i2p.streaming.tcbcache.rttdevDampening 0.75 Ссылка: RFC 2140. Значение с плавающей точкой. Может быть установлено только через свойства контекста, но не через параметры соединения. As of release .
 i2p.streaming.tcbcache.wdwDampening 0.75 Ссылка: RFC 2140. Значение с плавающей точкой. Может быть установлено только через свойства контекста, но не через параметры соединения. As of release .
 i2p.streaming.writeTimeout -1 Сколько блокировать запись/сброс, в миллисекундах. Отрицательное значение означает бесконечно.

## Спецификация протокола

[Ознакомьтесь со страницей Спецификации стриминговой
библиотеки.]()

## Детали реализации

### Установка

Инициатор посылает пакет с установленным флагом SYNCHRONIZE. Этот пакет
может содержать также начальные данные. Пир отвечает пакетом с
установленным флагом SYNCHRONIZE. Этот пакет может содержать также
начальные данные ответа.

Инициатор может отправлять дополнительные пакеты данных, вплоть до
размера начального окна, до получения ответа SYNCHRONIZE.. В этих
пакетах поле идентификатора потока отправки также будет установлено на
0. Получатели должны буферизировать пакеты, полученные по неизвестным
потокам, в течение короткого периода времени, поскольку они могут
приходить не по порядку, до пакета SYNCHRONIZE.

### Выбор и согласование MTU

Максимальный размер сообщения (также называемый MTU / MRU)
согласовывается с меньшим значением, поддерживаемым обоими пирами.
Поскольку туннельные сообщения имеют размер 1 КБ, неправильный выбор MTU
приведет к большим накладным расходам. MTU задается опцией
i2p.streaming.maxMessageSize. Текущий MTU по умолчанию 1730 был выбран
для того, чтобы точно уложиться в два туннельных сообщения I2NP размером
1K, включая накладные расходы для типичного случая. Note: This is the
maximum size of the payload only, not including the header.

Note: For ECIES connections, which have reduced overhead, the
recommended MTU is 1812. The default MTU remains 1730 for all
connections, no matter what key type is used. Clients must use the
minimum of the sent and received MTU, as usual. See proposal 155.

Первое сообщение в соединении включает 387 байт (типично) места
назначения, добавляемое потоковым уровнем, и обычно 898 байт (типично)
LeaseSet, а также ключи сессии, объединенные маршрутизатором в сообщение
Garlic. (LeaseSet и ключи сессии не будут включены, если сессия ElGamal
была установлена ранее). Поэтому цель вместить полный HTTP-запрос в одно
сообщение I2NP размером 1 КБ не всегда достижима. Однако выбор MTU, а
также тщательная реализация стратегий фрагментации и пакетирования в
процессоре туннельного шлюза являются важными факторами пропускной
способности сети, задержки, надежности и эффективности, особенно для
долгоживущих соединений.

### Целостность данных

Data integrity is assured by the gzip CRC-32 checksum implemented in
[the I2CP layer](#format). There is no checksum
field in the streaming protocol.

### Инкапсуляция пакета

Each packet is sent through I2P as a single message (or as an individual
clove in a [Garlic Message]()). Message
encapsulation is implemented in the underlying
[I2CP](), [I2NP](), and
[tunnel message]() layers. There is no
packet delimiter mechanism or payload length field in the streaming
protocol.

### Опциональная задержка

Пакеты данных могут включать необязательное поле задержки, определяющее
запрашиваемую задержку в мс, прежде чем приемник должен подтвердить
пакет. Допустимые значения от 0 до 60000 включительно. Значение 0
запрашивает немедленное подтверждение. Это только рекомендация, и
приемники должны немного задержаться, чтобы дополнительные пакеты могли
быть подтверждены одним ack. Некоторые реализации могут включать в это
поле рекомендательное значение (измеренный RTT / 2). Для ненулевых
необязательных значений задержки, приемники должны ограничить
максимальную задержку перед отправкой ack не более нескольких секунд.
Значения необязательной задержки более 60000 указывают на затор, см.
ниже.

### Приемное окно и затор

Заголовки TCP включают окно приема в байтах. Потоковый протокол не
содержит окна приема, он использует только простую индикацию
choke/unchoke . Каждая конечная точка должна поддерживать свою
собственную оценку окна приема на дальнем конце, либо в байтах, либо в
пакетах. Рекомендуемый минимальный размер буфера для реализации
приемника составляет 128 пакетов или 217 КБ (приблизительно 128x1730).
Из-за задержек в сети I2P, падений пакетов и возникающего контроля за
перегрузками, буфер такого размера редко заполняется. Однако
переполнение может произойти при высокоскоростных соединениях \"local
loopback\" (тот же маршрутизатор).

Для быстрой индикации и плавного восстановления после переполнения в
потоковом протоколе существует простой механизм отталкивания. Если
получен пакет с необязательным полем задержки со значением 60001 или
выше, это указывает на \"choking\" или нулевое окно приема. Пакет с
необязательным полем задержки, имеющим значение 60000 или меньше,
указывает на \"unchoking\". Пакеты без дополнительного поля задержки не
влияют на состояние \"choke/unchoke\".

После choke не следует отправлять больше никаких пакетов с данными до
тех пор, пока передатчик не будет разблокирован, за исключением
случайных \"пробных\" пакетов данных, чтобы компенсировать возможную
потерю пакетов без развязки. Choked конечная точка должна запустить
\"таймер сохранения\" для управления зондированием как в TCP. Unchoking
конечная точка, которая разблокирует, следует отправить несколько
пакетов с установленным полем, или продолжать периодически отправлять
их, пока пакеты данных не будут получены снова. Максимальное время
ожидания разблокировки зависит от реализации. Размер окна передатчика и
стратегия управления перегрузкой после разблокировки зависят от
реализации.

### Контроль перегрузок

В потоковой передаче используется стандартный медленный старт
(экспоненциальный рост окна) и предотвращение перегрузок (линейный рост
окна) фазы, с экспоненциальным отступлением. Окно и подтверждение
используют подсчет пакетов, а не байтов.

### Закрыть

В любом пакете, включая пакет с установленным флагом SYNCHRONIZE, может
быть также отправлен флаг CLOSE. Соединение не закрывается, пока пир не
ответит флагом CLOSE. Пакеты CLOSE могут также содержать данные.

### Ping / Pong

Функция ping отсутствует на уровне I2CP (эквивалент ICMP echo) или в
дейтаграммах. Эта функция предусмотрена в потоковой передаче. Pings и
pongs не могут быть объединены со стандартным потоковым пакетом; если
установлена опция ECHO, то большинство других флагов, опций, ackThrough,
sequenceNum, NACKs и т.д. игнорируются.

Пакет ping должен иметь установленные флаги ECHO, SIGNATURE_INCLUDED и
FROM_INCLUDED. SendStreamId должен быть больше нуля, а receiveStreamId
игнорируется. SendStreamId может соответствовать или не соответствовать
существующему соединению.

Пакет pong должен иметь установленный флаг ECHO. SendStreamId должен
быть нулевым, а receiveStreamId - это sendStreamId из ping. До версии
0.9.18 пакет pong не включал полезную нагрузку, которая содержалась в
ping.

Начиная с версии 0.9.18, pings и pongs могут содержать полезную
нагрузку. Полезная нагрузка в ping, максимум 32 байта, возвращается в
pong.

Потоковая передача может быть настроена на отключение отправки pongs с
помощью конфигурации i2p.streaming.answerPings=false.

### i2p.streaming.profile Notes {#profile}

This option supports two values; 1=bulk and 2=interactive. The option
provides a hint to the streaming library and/or router as to the traffic
pattern that is expected.

\"Bulk\" means to optimize for high bandwidth, possibly at the expense
of latency. This is the default. \"Interactive\" means to optimize for
low latency, possibly at the expense of bandwidth or efficiency.
Optimization strategies, if any, are implementation-dependent, and may
include changes outside of the streaming protocol.

Through API version 0.9.63, Java I2P would return an error for any value
other than 1 (bulk) and the tunnel would fail to start. As of API
0.9.64, Java I2P ignores the value. Through API version 0.9.63, i2pd
ignored this option; it is implemented in i2pd as of API 0.9.64.

While the streaming protocol includes a flag field to pass the profile
setting to the other end, this is not implemented in any known router.

### Совместное использование блоков управления {#sharing}

Потоковая библиотека поддерживает совместное использование блока
управления \"TCP\". При этом разделяются три важных параметра потоковой
библиотеки (размер окна, время обхода, дисперсия времени обхода) между
соединениями с одним и тем же удаленным аналогом. Что используется для
\"временного\" совместного использования во время открытия/закрытия
соединения, а не \"ансамблевого\" совместного использования во время
соединения (см. [RFC 2140](http://www.ietf.org/rfc/rfc2140.txt)).
Существует отдельный ресурс для каждого ConnectionManager (т.е. для
локального пункта назначения) чтобы не было утечки информации в другие
пункты назначения на одном и том же маршрутизаторе. Срок действия данных
совместного доступа для данного аналога истекает через несколько минут.
Следующие параметры совместного использования управляющих блоков могут
быть установлены для каждого маршрутизатора:

- RTT_DAMPENING = 0.75
- RTTDEV_DAMPENING = 0.75
- WINDOW_DAMPENING = 0.75

### Прочие параметры {#other}

Следующие параметры закодированы, но могут представлять интерес для
анализа:

- MIN_RESEND_DELAY = 100 ms (minimum RTO)
- MAX_RESEND_DELAY = 45 sec (maximum RTO)
- MIN_WINDOW_SIZE = 1
- TREND_COUNT = 3
- MIN_MESSAGE_SIZE = 512 (minimum MTU)
- INBOUND_BUFFER_SIZE = maxMessageSize \* (maxWindowSize + 2)
- INITIAL_TIMEOUT (valid only before RTT is sampled) = 9 sec
- \"alpha\" ( RTT dampening factor as per RFC 6298 ) = 0.125
- \"beta\" ( RTTDEV dampening factor as per RFC 6298 ) = 0.25
- \"K\" ( RTDEV multiplier as per RFC 6298 ) = 4
- PASSIVE_FLUSH_DELAY = 175 ms
- Maximum RTT estimate: 60 sec

### История

Потоковая библиотека органично росла для I2P - сначала mihi реализовал
\"мини библиотеку потоковой передачи\" как часть I2PTunnel, которая была
ограничена окном размером в 1 сообщение (требующее ACK перед отправкой
следующего), а затем она была рефакторингом в общий потоковый интерфейс
(зеркальное отображение TCP сокетов) и полная потоковая реализация была
развернута с протоколом скользящего окна и оптимизациями, учитывающими
высокое произведение пропускной способности и задержки. Отдельные потоки
могут регулировать максимальный размер пакета и другие параметры. По
умолчанию размер сообщения выбран таким образом, чтобы точно уместиться
в двух туннельных сообщениях I2NP размером 1K, и является разумным
компромиссом между стоимостью пропускной способности повторной передачи
потерянных сообщений, а также задержкой и накладными расходами на
передачу нескольких сообщений.

## Предстоящая работа {#future}

Поведение потоковой библиотеки оказывает глубокое влияние на
производительность на уровне приложения, и поэтому является важной
областью для дальнейшего анализа.

- Может понадобиться дополнительная настройка параметров стриминговой
 библиотеки.
- Another area for research is the interaction of the streaming lib
 with the NTCP and SSU transport layers. See [the NTCP discussion
 page]() for details.
- Взаимодействие алгоритмов маршрутизации с потоковой библиотекой
 сильно влияет на производительность. В частности, случайное
 распределение сообщений по нескольким туннелям в пуле приводит к
 высокой степени неупорядоченной доставки, что приводит к меньшим
 размерам окон чем в противном случае. В настоящее время
 маршрутизатор направляет сообщения для одной пары от/до пункта
 назначения через последовательный набор туннелей, пока не истечет
 срок действия туннеля или не произойдет сбой доставки. Алгоритмы
 маршрутизатора, алгоритмы отказа и выбора туннеля следует
 пересмотреть на предмет возможных усовершенствования.
- Данные в первом SYN-пакете могут превышать MTU приемника.
- Поле DELAY_REQUESTED можно было бы использовать больше.
- Дублирующие начальные пакеты SYNCHRONIZE на короткоживущих потоках
 могут быть не распознаны и не удалены.
- Не отправляйте MTU при повторной передаче.
- Данные отправляются до тех пор, пока исходящее окно не будет
 заполнено. (т.е. no-Nagle или TCP_NODELAY). Вероятно, для этого
 должна быть опция конфигурации.
- zzz добавил код отладки в потоковую библиотеку для регистрации
 пакетов в формате, совместимом с wireshark (pcap); используйте это
 для дальнейшего анализа производительности. Формат может нуждаться в
 усовершенствовании для сопоставления большего количества параметров
 потоковой библиотеки с полями TCP.
- Есть предложения заменить потоковую библиотеку стандартным TCP (или,
 возможно, нулевым уровнем вместе с сырыми сокетами). К сожалению,
 это будет несовместимо с потоковой библиотекой, но было бы неплохо
 сравнить их производительность.


