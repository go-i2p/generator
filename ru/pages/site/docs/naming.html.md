 Именование и
адресная книга 2025-01 0.9.65 

## Обзор {#overview}

I2P поставляется с общей библиотекой именования, основное ее применение
рассчитано на отображение локальных имен в катологах, также поставляется
дополнительное приложение [addressbook](#addressbook). Также I2P
поддерживает [Base32 hostnames](#base32), похожие на адреса .onion
Tor\'а.

\"Адресная книга\" - это сеть доверия, представляющая собой безопасную,
распределенную, удобочитаемую систему имен, в которой взамен глобальной
уникальности имен гарантируется только локальная уникальность. Несмотря
на то, что все сообщения в I2P криптографически адресуются по их
каталогам, у разных людей могут быть записи в локальной адресной книге
для \"Alice\", указывающие на разные катологи. Также люди могут узнавать
о новых именах, импортируя опубликованные адресные книги узлов,
перечисленных в их сети доверия, добавляя новые записи, предоставленные
третьей стороной, или (если кто-то организует серию опубликованных
адресных книг, используя систему регистрации первый пришел - первый
обслужен) люди могут использовать эти адресные книги в качестве серверов
имен, эмулирующих традиционные DNS.

NOTE: For the reasoning behind the I2P naming system, common arguments
against it and possible alternatives see the [naming
discussion]() page.

## Компоненты системы имён {#components}

Не существует централизованной системы авторизации имен в I2P. Все имена
узлов являются локальными.

Система имен довольно проста и большей частью представлена внешними, по
отношению к маршрутизатору, приложениями, но поставляющимися с
дистрибутивом I2P. Эти компоненты:

1. Локальный [сервис имен](#lookup), который осуществляет поиск и
 обрабатывает [Base32 имена узлов](#base32).
2. [HTTP proxy](#httpproxy), которое запрашивает поиск у
 маршрутизатора, и направляет пользователя в службы удаленных
 переходов в случае ошибок поиска.
3. HTTP [формы добавления узлов](#add-services), позволяющие
 пользователям добавлять узлы в их локальный hosts.txt
4. HTTP [службы переходов](#jump-services), предоставляющие собственный
 поиск и перенаправление.
5. Приложение [адресная книга](#addressbook), выполняющая слияние
 внешних списков узлов, полученных по HTTP, с локальным списком.
6. Приложение [SusiDNS](#susidns), являющееся простым веб-интерфейсом
 для настройки адресной книги и просмотра локального списка узлов.

## Naming Services {#lookup}

All destinations in I2P are 516-byte (or longer) keys. (To be more
precise, it is a 256-byte public key plus a 128-byte signing key plus a
3-or-more byte certificate, which in Base64 representation is 516 or
more bytes. Non-null
[Certificates](#certificates) are in
use now for signature type indication. Therefore, certificates in
recently-generated destinations are more than 3 bytes.

Когда приложение (i2ptunnel или HTTP-прокси) запрашивает доступ к адресу
назначения по имени, то маршрутизатор проводит очень простой локальный
поиск для разрешения этого имени.

### Hosts.txt Naming Service

Сервис имён hosts.txt производит простой линейный поиск в текстовых
файлах. Этот сервис имён использовался по умолчанию до версии 0.8.8,
когда его заменил сервис Blockfile. Формат hosts.txt становился очень
медленным, когда файл разрастался до тысяч записей.

It does a linear search through three local files, in order, to look up
host names and convert them to a 516-byte destination key. Each file is
in a simple [configuration file
format](), with hostname=base64, one per
line. The files are:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile Naming Service

Служба Blockfile Naming Service хранит несколько \"адресных книг\" в
одном файле базы данных с именем hostsdb.blockfile. Эта служба
используется по умолчанию начиная с версии 0.8.8.

A blockfile is simply on-disk storage of multiple sorted maps (key-value
pairs), implemented as skiplists. The blockfile format is specified on
the [Blockfile page](). It provides fast
Destination lookup in a compact format. While the blockfile overhead is
substantial, the destinations are stored in binary rather than in Base
64 as in the hosts.txt format. In addition, the blockfile provides the
capability of arbitrary metadata storage (such as added date, source,
and comments) for each entry to implement advanced address book
features. The blockfile storage requirement is a modest increase over
the hosts.txt format, and the blockfile provides approximately 10x
reduction in lookup times.

При создании, служба именования импортирует записи из трех файлов,
используемые системой идентификации имён hosts.txt. Блок-файл имитирует
предыдущую реализацию, поддерживая три карты, которые которые ищутся по
порядку и называются privatehosts.txt, userhosts.txt и hosts.txt.. Он
также поддерживает карту обратного поиска для осуществления быстрого
обратного поиска.

### Other Naming Service Facilities

The lookup is case-insensitive. The first match is used, and conflicts
are not detected. There is no enforcement of naming rules in lookups.
Lookups are cached for a few minutes. Base 32 resolution is [described
below](#base32). For a full description of the Naming Service API see
the [Naming Service Javadocs](). This API
was significantly expanded in release 0.8.7 to provide adds and removes,
storage of arbitrary properties with the hostname, and other features.

### Alternatives and Experimental Naming Services

The naming service is specified with the configuration property
`i2p.naming.impl=class`. Other implementations are possible. For
example, there is an experimental facility for real-time lookups (a la
DNS) over the network within the router. For more information see the
[alternatives on the discussion
page](#alternatives).

HTTP-прокси выполняет поиск через маршрутизатор всех имен хостов,
заканчивающихся на \'.i2p\'. В противном случае он направляет запрос на
настроенный HTTP outproxy. Т.о., на практике все имена хостов HTTP (I2P
Site) должны заканчиваться на псевдо-домен верхнего уровня \'.i2p\'.

Если маршрутизатор не может разрешить имя узла, то HTTP прокси
возвращает пользователю страницу с ошибкой и ссылками на несколько служб
\"переходов\". Подробнее смотри ниже.

## .i2p.alt Domain {#alt}

We previously [applied to reserve the .i2p
TLD](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/)
following the procedures specified in [RFC
6761](https://www.rfc-editor.org/rfc/rfc6761.html). However, this
application and all others were rejected, and RFC 6761 was declared a
\"mistake\".

After many years of work by the GNUnet team and others, the .alt domain
was reserved as a special-use TLD in [RFC
9476](https://www.rfc-editor.org/rfc/rfc9476.html) as of late 2023.
While there are no official registrars sanctioned by IANA, we have
registered the .i2p.alt domain with the primary unofficial registrar
[GANA](https://gana.gnunet.org/dot-alt/dot_alt.html). This does not
prevent others from using the domain, but it should help discourage it.

One benefit to the .alt domain is that, in theory, DNS resolvers will
not forward .alt requests once they update to comply with RFC 9476, and
that will prevent DNS leaks. For compatibility with .i2p.alt hostnames,
I2P software and services should be updated to handle these hostnames by
stripping off the .alt TLD. These updates are scheduled for the first
half of 2024.

At this time, there are no plans to make .i2p.alt the preferred form for
display and interchange of I2P hostnames. This is a topic for further
research and discussion.

## Адресная книга {#addressbook}

### Входящие Подписки и Слияние

Приложение адресной книги периодически запрашивает файлы hosts.txt
других пользователей и после нескольких проверок производит их слияние с
локальным hosts.txt. Конфликты имен разрешаются по принципу первый
пришел - первый обслужен.

Подписка на файл hosts.txt другого пользователя означает, что мы ему
доверяем в этой части отношений. Вы не хотите чтобы он, к примеру,
\'взломал\' новый сайт, быстро введя свой ключ для нового сайта до того
как передать новую пару узел/ключ вам.

По этой причине единственная подписка, настроенная по по умолчанию - это
`http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`,
она содержит копию файла hosts.txt, включенного в релиз I2P.
Пользователи должны настроить дополнительные подписки в своем локальном
приложении адресной книги (через subscriptions.txt или
[SusiDNS](#susidns)).

Ссылки на некоторые другие подписки публичных адресных книг:

- [http:///cgi-bin/i2hostetag](http:///cgi-bin/i2hostetag)
- [http:///cgi-bin/newhosts.txt](http:///cgi-bin/newhosts.txt)

У операторов этих служб могут быть различные политики для просмотра
списка узлов. В соответствии с этим список может быть не одобрен.

### Правила Именования

К счастью, нет никаких технических ограничений на имена узлов в I2P, но
адресная книга накладывает некоторые ограничения на имена узлов,
импортированные из подписок. Это делается для соблюдения основных правил
именования, совместимости с браузерами и с целью безопасности. Эти
правила в сущности такие же, как описанные в Разделе 3.2.2 RFC2396.
Любые имена узлов, нарушающие эти правила, не должны распространяться на
другие маршрутизаторы.

Правила Именования:

- При импорте имена приводятся к нижнему регистру.
- После приведения к нижнему регистру имена проверяются на конфликты с
 имеющимися именами в userhosts.txt и hosts.txt (но не в
 privatehosts.txt).
- После приведения к нижнему регистру должны содержать только \[a-z\]
 \[0-9\] \'.\' и \'-\'.
- Не должны начинаться с \'.\' или \'-\'.
- Должны оканчиваться на \'.i2p\'.
- Максимум 67 символов, включая \'.i2p\'.
- Не должны содержать \'..\'.
- Не должны содержать \'.-\' или \'-.\' (как в 0.6.1.33).
- Не должны содержать \'\--\', исключение - \'xn\--\' для IDN.
- Имена узлов Base32 (\*.b32.i2p) зарезервированы для использования
 base32 и не разрешены к импортированию.
- Certain hostnames reserved for project use are not allowed
 (proxy.i2p, router.i2p, console.i2p, mail.i2p, \*.proxy.i2p,
 \*.router.i2p, \*.console.i2p, \*.mail.i2p, and others)
- Hostnames starting with \'www.\' are discouraged and are rejected by
 some registration services. Some addressbook implementations
 automatically strip \'www.\' prefixes from lookups. So registring
 \'www.example.i2p\' is unnecessary, and registering a different
 destination for \'www.example.i2p\' and \'example.i2p\' will make
 \'www.example.i2p\' unreachable for some users.
- Ключи проверяются на соответствие base64.
- Ключи проверяются на конфликты с существующими ключами в hosts.txt
 (но не в privatehosts.txt).
- Минимальный размер ключа 516 байт.
- Максимальный размер ключа 616 байт (для нужд сертификатов до 100
 байт).

Каждое имя, полученное по подписке и прошедшее все проверки, добавляется
через локальную службу именования.

Учтите, что символ \'.\' в имени узла не имеет особого смысла и не
говорит о фактической иерархии имен или доверия. Если имя \'host.i2p\'
уже существует, ничто не мешает кому-нибудь добавить имя \'a.host.i2p\'
в свой hosts.txt, и это имя может быть импортировано в другие адресные
книги. Методы запрета заведения субдоменов не \"владельцами\" домена
(сертификата?), целесообразность и осуществимость этих методов - это
предмет для будущих обсуждений.

Также в I2P работают интернационализованные доменные имена (IDN)
(используя форму punycode \'xn\--\'). Чтобы IDN имена домена .i2p
корректно отображались в адресной строке Firefox, добавьте
\'network.IDN.whitelist.i2p (boolean) = true\' в about:config.

Поскольку приложение адресной книги совсем не использует
privatehosts.txt, то на практике этот файл - единственно верное место,
куда стоит поместить личные синонимы или \"клички\" для сайтов, которые
уже есть в hosts.txt.

### Формат расширенной подписки

As of release 0.9.26, subscription sites and clients may support an
advanced hosts.txt feed protocol that includes metadata including
signatures. This format is backwards-compatible with the standard
hosts.txt hostname=base64destination format. See [the
specification](/spec/subscription) for details.

### Исходящие Подписки

Адресная книга публикует объединенный hosts.txt с местоположении
(традиционно hosts.txt в домашнем каталоге локального сайта I2P),
доступном другим по их подпискам. Этот шаг необязателен и по умолчанию
отключен.

### Hosting and HTTP Transport Issues

Приложение адресной книги, совместно с eepget, сохраняет Etag и/или
информацию о последнем изменении, полученную веб-сервером по подписке.
Это существенно снижает требования к полосе пропускания, т.к. веб-сервер
вернет \'304 Not Modified\' при следующем получении, если изменений не
было.

Тем не менее, содержимое hosts.txt загружается, если он был изменен.
Обсуждение этой темы смотри ниже.

Узлу, обслуживающему статичный hosts.txt, или эквивалентному приложению
CGI настоятельно рекомендуется отправлять заголовок Content-Length, либо
Etag или заголовок Last-Modified. Убедитесь также, что сервер по
необходимости выдает \'304 Not Modified\'. Это существенно уменьшит
пропускную способность сети и уменьшит вероятность повреждения.

## Службы Добавления Узла {#add-services}

Служба добавления узла - это простое приложение CGI, которое принимает
имя узла и Base64 ключ в качестве параметров, и добавляет их в локальный
hosts.txt. Если другие маршрутизаторы подписаны на этот hosts.txt, то
новая пара имя узла/ключ будет передана по сети.

На службу добавления узла, как минимум, рекомендуется наложить
ограничения, совпадающие с ограничениями приложения адресной книги,
описанными выше. На службу добавления узла могут быть наложены
дополнительные ограничения на имя узла и ключ, например:

- Ограничение количества \'поддоменов\'.
- Различные методы авторизации для \'поддоменов\'.
- Hashcash или подписанные сертификаты.
- Экспертная оценка имен узлов и/или содержимого.
- Категоризация узлов по содержимому.
- Резервирование или исключение определенных имен узлов.
- Ограничение количества имен, регистрируемых за определенный период
 времени.
- Задержка между регистрацией и публикацией.
- Необходимость доступности узла для его верификации.
- Истечение срока и/или аннулирование.
- Предотвращение IDN-спуфинга.

## Службы перехода {#jump-services}

Служба перехода - это простое CGI приложение, которое получает имя узла
в качестве параметра, и возвращает перенаправление 301 на правильный URL
с добавлением строки `?i2paddresshelper=key`. HTTP прокси интерпретирует
добавленную строку и использует этот ключ как актуальный пункт
назначения. Кроме того, прокси кеширует этот ключ, так что address
helper не нужен до перезапуска.

Учтите, что как и с подписками, использование службы перехода требует
части доверия, так как служба перехода может злонамеренно перенаправить
пользователя в некорректный пункт назначения.

Для предоставления лучшего уровня сервиса служба перехода должна быть
подписана на несколько провайдеров hosts.txt, т.о., локальный список
узлов будет актуальным.

## SusiDNS

SusiDNS - это просто веб-интерфейс для настройки подписок адресной книги
и для доступа к четырем ее файлам. Вся настоящая работа выполняется
приложением \'адресная книга\'.

На данный момент в SusiDNS реализовано мало правил ограничения
именования адресной книги, так что пользователь может локально ввести
имя узла, которое будет отвергнуто в соответствии с правилами подписки
адресной книги.

## Base32 Имена {#base32}

I2P поддерживает Base32 имена узлов по аналогии с .onion адресами Tor.
Base32 адреса гораздо короче и их проще обрабатывать, чем полные
516-символьные Base64 пункты назначения или addresshelper-ы. Пример:
`ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

В Tor - адрес из 16 символов (80 бит), или половины хэша SHA-1. I2P
использует 52 символа (256 бит) для представления полного хэша SHA-256.
Форма - {52 chars}.b32.i2p. У Tor есть
[предложение](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013)
перейти на идентичный формат {52 chars}.onion для своих скрытых служб.
Base32 реализован в службе именования, которая запрашивает
маршрутизатор  по протоколу I2CP для поиска LeaseSet, чтобы получить
полный адрес пункта назначения. Поиск по Base32 будет успешным только,
если место назначения работает и публикует LeaseSet. Из-за этого для
разрешения может потребоваться поиск в сетевой базе данных, это может
занять значительно больше времени, чем поиск в локальной адресной книге.

Base32 адреса могут быть использованы в большинстве случаев, где
используются имена узлов или полные пункты назначения, тем не менее есть
несколько исключений, когда это может вызвать ошибку, если имя не может
быть преобразовано в адрес. Например, в I2PTunnel возникнет ошибка, если
имя не разрешается в пункт назначения.

## Extended Base32 Names {#newbase32}

Extended base 32 names were introduced in release 0.9.40 to support
encrypted lease sets. Addresses for encrypted leasesets are identified
by 56 or more encoded characters, not including the \".b32.i2p\" (35 or
more decoded bytes), compared to 52 characters (32 bytes) for
traditional base 32 addresses. See proposals 123 and 149 for additional
information.

Standard Base 32 (\"b32\") addresses contain the hash of the
destination. This will not work for encrypted ls2 (proposal 123).

You can\'t use a traditional base 32 address for an encrypted LS2
(proposal 123), as it contains only the hash of the destination. It does
not provide the non-blinded public key. Clients must know the
destination\'s public key, sig type, the blinded sig type, and an
optional secret or private key to fetch and decrypt the leaseset.
Therefore, a base 32 address alone is insufficient. The client needs
either the full destination (which contains the public key), or the
public key by itself. If the client has the full destination in an
address book, and the address book supports reverse lookup by hash, then
the public key may be retrieved.

So we need a new format that puts the public key instead of the hash
into a base32 address. This format must also contain the signature type
of the public key, and the signature type of the blinding scheme.

This section documents a new b32 format for these addresses. While we
have referred to this new format during discussions as a \"b33\"
address, the actual new format retains the usual \".b32.i2p\" suffix.

### Creation and encoding

Construct a hostname of {56+ chars}.b32.i2p (35+ chars in binary) as
follows. First, construct the binary data to be base 32 encoded:

 flag (1 byte)
 bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
 bit 1: 0 for no secret, 1 if secret is required
 bit 2: 0 for no per-client auth,
 1 if client private key is required
 bits 7-3: Unused, set to 0

 public key sigtype (1 or 2 bytes as indicated in flags)
 If 1 byte, the upper byte is assumed zero

 blinded key sigtype (1 or 2 bytes as indicated in flags)
 If 1 byte, the upper byte is assumed zero

 public key
 Number of bytes as implied by sigtype

Post-processing and checksum:

 Construct the binary data as above.
 Treat checksum as little-endian.
 Calculate checksum = CRC-32(data[3:end])
 data[0] ^= (byte) checksum
 data[1] ^= (byte) (checksum >> 8)
 data[2] ^= (byte) (checksum >> 16)

 hostname = Base32.encode(data) || ".b32.i2p"

Any unused bits at the end of the b32 must be 0. There are no unused
bits for a standard 56 character (35 byte) address.

### Decoding and Verification

 Strip the ".b32.i2p" from the hostname
 data = Base32.decode(hostname)
 Calculate checksum = CRC-32(data[3:end])
 Treat checksum as little-endian.
 flags = data[0] ^ (byte) checksum
 if 1 byte sigtypes:
 pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
 blinded sigtype = data[2] ^ (byte) (checksum >> 16)
 else (2 byte sigtypes) :
 pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
 blinded sigtype = data[3] || data[4]
 parse the remainder based on the flags to get the public key

### Secret and Private Key Bits

The secret and private key bits are used to indicate to clients,
proxies, or other client-side code that the secret and/or private key
will be required to decrypt the leaseset. Particular implementations may
prompt the user to supply the required data, or reject connection
attempts if the required data is missing.

### Notes

- XORing first 3 bytes with the hash provides a limited checksum
 capability, and ensures that all base32 chars at the beginning are
 randomized. Only a few flag and sigtype combinations are valid, so
 any typo is likely to create an invalid combination and will be
 rejected.
- In the usual case (1 byte sigtypes, no secret, no per-client auth),
 the hostname will be {56 chars}.b32.i2p, decoding to 35 bytes, same
 as Tor.
- Tor 2-byte checksum has a 1/64K false negative rate. With 3 bytes,
 minus a few ignored bytes, ours is approaching 1 in a million, since
 most flag/sigtype combinations are invalid.
- Adler-32 is a poor choice for small inputs, and for detecting small
 changes. We use CRC-32 instead. CRC-32 is fast and is widely
 available.
- While outside the scope of this specification, routers and/or
 clients must remember and cache (probably persistently) the mapping
 of public key to destination, and vice versa.
- Distinguish old from new flavors by length. Old b32 addresses are
 always {52 chars}.b32.i2p. New ones are {56+ chars}.b32.i2p
- Tor discussion thread [is
 here](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- Don\'t expect 2-byte sigtypes to ever happen, we\'re only up to 13.
 No need to implement now.
- New format can be used in jump links (and served by jump servers) if
 desired, just like b32.
- Any secret, private key, or public key longer than 32 bytes would
 exceed the DNS max label length of 63 chars. Browsers probably do
 not care.
- No backward compatibility issues. Longer b32 addresses will fail to
 be converted to 32-byte hashes in old software.


