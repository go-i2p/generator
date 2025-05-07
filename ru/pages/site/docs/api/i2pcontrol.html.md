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

I2PControl по умолчанию слушает на https://localhost:7650

## API, версия 1.

Параметры предоставляются только именованным способом (карты).

#### Формат JSON-RPC 2

Request: { \"id\": \"id\", \"method\":
\"Method-name\", \"params\": { \"Param-key-1\": \"param-value-1\",
\"Param-key-2\": \"param-value-2\", \"Token\": \"\*\*actual token\*\*\"
}, \"jsonrpc\": \"2.0\" } Response: { \"id\": \"id\", \"result\": { \"Result-key-1\":
\"result-value-1\", \"Result-key-2\": \"result-value-2\" }, \"jsonrpc\":
\"2.0\" } 

- - Param-key-1 -- Description
 - Param-key-2 -- Description
 - Token -- Токен, использующийся для аутентификации каждого
 запроса (исключая метод \'Authenticate\')

- - Result-key-1 -- Description
 - Result-key-2 -- Description

#### Реализованные методы

- - API -- \[long\] Версия I2PControl API, используемая клиентом.
 - Password -- \[String\] Пароль, использующийся для авторизации на
 удалённом сервере.

- - API -- \[long\] Основная версия I2PControl API, реализованная
 сервером.
 - Token -- \[String\] Токен, используемый для последующего
 информационного обмена.

```{=html}
<!-- -->
```
- - Echo -- \[String\] Значение будет возвращено в ответе.
 - Token -- \[String\] Токен, использованный для аутентификации
 клиента. Предоставляется сервером при помощи RPC метода
 \'Authenticate\'.

- - Result -- \[String\] Значение ключа \'echo\' в запросе.

```{=html}
<!-- -->
```
- - Stat -- \[String\] Determines which
 rateStat to fetch, see
 [ratestats]().
 - Period -- \[long\] Определяет, за какой период будет получена
 статистика. Измеряется в мс.
 - Token -- \[String\] Токен, использованный для аутентификации
 клиента. Предоставляется сервером при помощи RPC метода
 \'Authenticate\'.

- - Result -- \[double\] Returns the average value for the requested
 rateStat and period.

```{=html}
<!-- -->
```
- - \*i2pcontrol.address -- \[String\] Задаёт новый адрес для
 прослушивания для I2PControl (на данный момент реализованы
 только 127.0.0.1 и 0.0.0.0 адреса).
 - \*i2pcontrol.password -- \[String\] Устанавливает новый пароль
 для I2PControl, все токены для аутентификации будут сброшены.
 - \*i2pcontrol.port -- \[String\] Устанавливает, какой порт будет
 использовать I2P для прослушивания входящих соединений.
 - Token -- \[String\] Токен, использованный для аутентификации
 клиента. Предоставляется сервером при помощи RPC метода
 \'Authenticate\'.

- - \*\*i2pcontrol.address -- \[null\] Возвращается, если адрес был
 изменён
 - \*\*i2pcontrol.password -- \[null\] Возвращается, если этот
 параметр был изменён
 - \*\*i2pcontrol.port -- \[null\] Возвращается, если этот параметр
 был изменён
 - SettingsSaved -- \[Boolean\] Возвращает \'true\', если были
 изменены какие-либо настройки.
 - RestartNeeded -- \[Boolean\] Возвращает \'true\', если были
 изменены какие-либо настройки, для применения которых требуется
 перезагрузка.

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
 - Token -- \[String\] Токен, использованный для аутентификации
 клиента. Предоставляется сервером при помощи RPC метода
 \'Authenticate\'.

- - \*\*i2p.router.status -- \[String\] Каков статус маршрутизатора
 I2P. A free-format, translated string intended for display to
 the user. May include information such as whether the router is
 accepting participating tunnels. Content is
 implementation-dependent.
 - \*\*i2p.router.uptime -- \[long\] Каково время с начала загрузки
 маршрутизатора в мс. Note: i2pd routers prior to version 2.41
 returned this value as a string. For compatibility, clients
 should handle both string and long.
 - \*\*i2p.router.version -- \[String\] I2P маршрутизатор какой
 версии запущен в данный момент.
 - \*\*i2p.router.net.bw.inbound.1s -- \[double\] Средний входящий
 трафик за 1 секунду в б/с.
 - \*\*i2p.router.net.bw.inbound.15s -- \[double\] Средний входящий
 трафик за 15 секунд в б/с.
 - \*\*i2p.router.net.bw.outbound.1s -- \[double\] Средний
 исходящий трафик за 1 секунду в б/с.
 - \*\*i2p.router.net.bw.outbound.15s -- \[double\] Средний
 исходящий трафик за 15 секунд в б/с.
 - \*\*i2p.router.net.status -- \[long\] Каков текущий статус сети.
 Согласно списку ниже:
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
 - \*\*i2p.router.net.tunnels.participating -- \[long\] Сколько
 туннелей в сети I2P участвуют в обмене.
 - \*\*i2p.router.netdb.activepeers -- \[long\] Между сколькими
 пирами недавно был обмен данными.
 - \*\*i2p.router.netdb.fastpeers -- \[long\] Сколько пиров
 считаются \'быстрыми\'.
 - \*\*i2p.router.netdb.highcapacitypeers -- \[long\] Сколько пиров
 считаются с \'высокой пропускной способностью\'.
 - \*\*i2p.router.netdb.isreseeding -- \[boolean\] Перезагружает ли
 маршрутизатор хосты в свою NetDB?
 - \*\*i2p.router.netdb.knownpeers -- \[long\] Сколько пиров
 известны нам (перечислены в нашей Сетевой БД).

```{=html}
<!-- -->
```
- - \*FindUpdates -- \[n/a\] **Блокировка**. Инициирует поиск
 подписанных обновлений.
 - \*Reseed -- \[n/a\] Инициирует ресид маршрутизатора, собирая
 пиров в нашу NetDB с удаленного узла.
 - \*Restart -- \[n/a\] Перезагружает I2P маршрутизатор.
 - \*RestartGraceful -- \[n/a\] \"Мягко\" перезагружает I2P
 маршрутизатор (ждёт, пока у участвующих в обмене туннелей
 истечёт время).
 - \*Shutdown -- \[n/a\] Выключает I2P маршрутизатор.
 - \*ShutdownGraceful -- \[n/a\] \"Мягко\" выключает I2P
 маршрутизатор (ждёт, пока у участвующих в обмене туннелей
 истечёт время).
 - \*Update -- \[n/a\] Инициирует обновление маршрутизатора из
 подписанных источников.
 - Token -- \[String\] Токен, использованный для аутентификации
 клиента. Предоставляется сервером при помощи RPC метода
 \'Authenticate\'.

- - \*\*FindUpdates -- \[boolean\] **Блокировка**. Возвращает true,
 если было найдено подписанное обновление.
 - \*\*Reseed -- \[null\] По запросу проверяет, был ли инициирован
 ресид.
 - \*\*Restart -- \[null\] Если запрошено, проверять, что
 перезагрузка уже начата.
 - \*\*RestartGraceful -- \[null\] Если запрошено, проверяет, был
 ли инициирован постепенный перезапуск.
 - \*\*Shutdown -- \[null\] По запросу проверяет, было ли
 инициировано отключение.
 - \*\*ShutdownGraceful -- \[null\] По запросу проверяет, было ли
 инициировано отключение
 - \*\*Update -- \[String\] **Блокировка**. По запросу возвращает
 статус обновления

```{=html}
<!-- -->
```
- - \*i2p.router.net.ntcp.port -- \[String\] Какой порт используется
 для TCP транспорта. Если передано пустое значение, то будет
 возвращено текущее значение.
 - \*i2p.router.net.ntcp.hostname -- \[String\] Какое имя хоста
 используется для TCP транспорта. Если передано пустое значение,
 то будет возвращено текущее значение.
 - \*i2p.router.net.ntcp.autoip -- \[String\] Использовать
 автоматически определённый IP адрес для TCP транспорта. Если
 передано пустое значение, то будет возвращено текущее значение.
 - \*i2p.router.net.ssu.port -- \[String\] Какой порт используется
 для UDP транспорта. Если передано пустое значение, то будет
 возвращено текущее значение.
 - \*i2p.router.net.ssu.hostname -- \[String\] Какое имя хоста
 используется для UDP транспорта. Если передано пустое значение,
 то будет возвращено текущее значение.
 - \*i2p.router.net.ssu.autoip -- \[String\] Какие методы следует
 использовать для определения IP адреса UDP транспорта. Если
 передано пустое значение, то будет возвращено текущее значение.
 - \*i2p.router.net.ssu.detectedip -- \[null\] IP адрес,
 автоматически определённый UDP транспортом.
 - \*i2p.router.net.upnp -- \[String\] Включен ли UPnP. Если
 передано пустое значение, то будет возвращено текущее значение.
 - \*i2p.router.net.bw.share -- \[String\] Процент ширины канала,
 доступный для обмена данными туннелей. Если передано пустое
 значение, то будет возвращено текущее значение.
 - \*i2p.router.net.bw.in -- \[String\] Разрешенный входящий трафик
 в Кб/с. Если передано пустое значение, то будет возвращено
 текущее значение.
 - \*i2p.router.net.bw.out -- \[String\] Разрешенный исходящий
 трафик в Кб/с. Если передано пустое значение, то будет
 возвращено текущее значение.
 - \*i2p.router.net.laptopmode -- \[String\] Включен ли режим
 лэптопа (изменяет ID маршрутизатора и UDP порт, когда меняется
 IP адрес). Если передано пустое значение, то будет возвращено
 текущее значение.
 - Token -- \[String\] Токен, используемый для аутентификации
 клиента. Предоставляется сервером при помощи RPC метода
 \'Authenticate\'. Если передано пустое значение, то будет
 возвращено текущее значение.

- - Note: i2pd routers prior to version 2.41 returned some of these
 values as numbers. For compatibility, clients should handle both
 strings and numbers.
 - \*\*i2p.router.net.ntcp.port -- \[String\] Если запрошено,
 возвращает порт, используемый TCP транспортом.
 - \*\*i2p.router.net.ntcp.hostname -- \[String\] Если запрошено,
 возвращает имя хоста, используемое TCP транспортом.
 - \*\*i2p.router.net.ntcp.autoip -- \[String\] Если запрошено,
 возвращает метод, используемый для автоматического определения
 IP адреса для TCP транспорта.
 - \*\*i2p.router.net.ssu.port -- \[String\] Если запрошено,
 возвращает порт, используемый UDP транспортом.
 - \*\*i2p.router.net.ssu.hostname -- \[String\] Если запрошено,
 возвращает имя хоста, используемое UDP транспортом.
 - \*\*i2p.router.net.ssu.autoip -- \[String\] Если запрошено,
 возвращает метод, используемый для автоматического определения
 IP адреса UDP транспорта.
 - \*\*i2p.router.net.ssu.detectedip -- \[String\] Если запрошено,
 возвращает IP адрес, определённый UDP транспортом.
 - \*\*i2p.router.net.upnp -- \[String\] Если запрошено, возвращает
 значение настройки UPnP.
 - \*\*i2p.router.net.bw.share -- \[String\] Если запрошено,
 возвращает процент ширины канала, доступный для использования
 туннелями.
 - \*\*i2p.router.net.bw.in -- \[String\] Если запрошено,
 возвращает, сколько КБ/с входящей пропускной способности
 разрешено.
 - \*\*i2p.router.net.bw.out -- \[String\] Если запрошено,
 возвращает, сколько КБ/с исходящей пропускной способности
 разрешено.
 - \*\*i2p.router.net.laptopmode -- \[String\] Если запрошено,
 возвращает значение настройки режима лэптопа.
 - SettingsSaved -- \[boolean\] Были ли сохранены заданные
 настройки.
 - RestartNeeded -- \[boolean\] Требуется ли перезапуск для
 вступления в силу новых настроек.

```{=html}
<!-- -->
```
- - {\"setting-key\": \"setting-value\", \...} -- \[Map\]

- - {\"setting-key\": \"setting-value\", \...} -- \[Map\]

- - \"setting-key\" -- \[String\]

- 

\* означает необязательный параметр

\*\* означает возможное возвращаемое значение

### Коды ошибок

- -32700 -- Ошибка разбора JSON.
- -32600 -- Некорректный запрос.
- -32601 -- Метод не найден.
- -32602 -- Некорректные параметры.
- -32603 -- Внутренняя ошибка.

```{=html}
<!-- -->
```
- -32001 -- Указан неверный пароль.
- -32002 -- Не предоставлен аутентификационный токен.
- -32003 -- Аутентификационный токен не существует.
- -32004 -- Время действия предоставленного аутентификационного токена
 истекло, и он будет удалён.
- -32005 -- Не указана используемая версия I2PControl API, необходимо
 её указать.
- -32006 -- Запрошенная версия I2PControl API не поддерживается
 I2PControl.


