 BOB - Basic Open
Bridge 2022-06 

## Warning - Deprecated

Not for use by new applications. BOB supports the DSA-SHA1 signature
type only. BOB will not be extended to support new signature types or
other advanced features. New applications should use [SAM
V3]().

BOB is not supported in Java I2P new installs as of release 1.7.0
(2022-02). It will still work in Java I2P originally installed as
version 1.6.1 or earlier, even after updates, but it is unsupported and
may break at any time. BOB is still supported by i2pd as of 2022-06, but
applications should still migrate to SAMv3 for the reasons above.

At this point, most of the good ideas from BOB have been incorporated
into SAMv3, which has more features and more real-world use. BOB may
still work on some installations (see above), but it is not gaining the
advanced features available to SAMv3 and is essentially unsupported,
except by i2pd.

## Language libraries for the BOB API

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python -
 [i2py-bob](http:///w/i2py-bob.git)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## Обзор

`KEYS` = пара ключей public+private, в виде BASE64

`KEY` = public ключ, также BASE64

`ERROR` как и предполагается, возвращает сообщение
`"ERROR "+DESCRIPTION+"\n"`, где `DESCRIPTION` это описание проблемы.

`OK` возвращает `"OK"`, и если есть возвращаемые данные, они буду
расположены в этой же строке. `OK` означает, что команда выполнена.

Строка `DATA` содержит информацию, которую вы запросили. Может быть
несколько строк `DATA` на один запрос.

**Примечание:** Команда help - ЕДИНСТВЕННАЯ команда, для которой есть
исключения из правил\... Она может ничего не возвращать! Это сделано
намеренно, поскольку help это команда для ЧЕЛОВЕКА, а не для ПРИЛОЖЕНИЯ.

## Подключение и Версия

Весь вывод статуса BOB осуществляется по линиям. Линии могут быть \\n
или \\r\\n терминированными, в зависимости от системы. При подключении,
BOB выводит две линии:

 BOB version OK 

Текущая версия: 00.00.10

Обратите внимание, что предыдущие версии использовали шестнадцатеричные
цифры в верхнем регистре и не соответствовали стандартам версионности
I2P. Рекомендуется, чтобы в последующих версиях использовались только
0-9. 00.00.10

История версий

 Версия Версия роутера I2P Изменения
 --------------------- -------------------- ------------------------
 00.00.10 0.9.8 текущая версия
 00.00.00 - 00.00.0F   разрабатываемые версии

## Команды

**ПОЖАЛУЙСТА УЧТИТЕ:** Для получения АКТУАЛЬНЫХ подробностей по командам
ПОЖАЛУЙСТА используйте встроенную команду help. Просто подключитесь по
telnet к localhost 2827 и введите help, и вы получите полную
документацию по каждой команде.

Команды никогда не устаревают и не изменяются, тем не менее, новые
команды время от времени появляются.

 COMMAND OPERAND RETURNS help (optional
command to get help on) NOTHING or OK and description of the command
clear ERROR or OK getdest ERROR or OK and KEY getkeys ERROR or OK and
KEYS getnick tunnelname ERROR or OK inhost hostname or IP address ERROR
or OK inport port number ERROR or OK list ERROR or DATA lines and final
OK lookup hostname ERROR or OK and KEY newkeys ERROR or OK and KEY
option key1=value1 key2=value2\... ERROR or OK outhost hostname or IP
address ERROR or OK outport port number ERROR or OK quiet ERROR or OK
quit OK and terminates the command connection setkeys KEYS ERROR or OK
and KEY setnick tunnel nickname ERROR or OK show ERROR or OK and
information showprops ERROR or OK and information start ERROR or OK
status tunnel nickname ERROR or OK and information stop ERROR or OK
verify KEY ERROR or OK visit OK, and dumps BOB\'s threads to the
wrapper.log zap nothing, quits BOB 

После установки все необходимые TCP сокеты могут и будут заблокированы,
и нет необходимости в дополнительных сообщениях в/из канал команд. Это
позволяет маршрутизатору проходить поток без разрыва с OOM, в отличие от
SAM, который захлебывается при попытке впихнуть несколько потоков в или
из одного сокета \-- это не поддается масштабированию при наличии
большого числа подключений!

Есть еще одна замечательная вещь в этом специфическом интерфейсе -
написать что угодно, подключающееся к нему, намного проще, чем к SAM. Не
нужно делать ничего дополнительного после установки. Его настройка
настолько проста, что любое просто средство, как например nc (netcat),
можно использовать для указания на какое-то приложение. Смысле в том,
что можно запланировать время запуска и остановки приложения, и для
этого не нужно изменять его, или, даже, останавливать это приложение.
Вместо этого вы можете буквально \"вынуть\" пункт назначения, и
\"вставить\" снова. Поскольку для восстановления моста используются та
же пара IP/порт и ключи, то обычному приложению это не важно, и оно не
будет даже об этом знать. Оно просто будет обмануто \-- пункт назначения
недоступен, и ничего не поступает на вход.

## Примеры

В следующем примере мы установим очень простое закольцованное локальное
подключение с двумя пунктами назначения. Пунктом \"mouth\" будет служба
CHARGEN демона суперсервера INET. Пунктом \"ear\" будет локальный порт,
к которому вы можете подключиться по telnet и увидеть забавный тест с
символами ASCII.

 ПРИМЕР ДИАЛОГА СЕССИИ \-- простой telnet
127.0.0.1 2827 работает A = Application C = Ответ команда от BOB FROM TO
DIALOGUE C A BOB 00.00.10 C A OK A C setnick mouth C A OK Nickname set
to mouth A C newkeys C A OK
ZMPz1zinTdy3\~zGD\~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr\~0g2-l0vM7Y8nSqtFrSdMw\~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU\~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq\~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw\~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA


**ОБРАТИТЕ ВНИМАНИЕ НА КЛЮЧ НАЗНАЧЕНИЯ ВЫШЕ, ВАШ БУДЕТ ДРУГИМ!**

 FROM TO DIALOGUE A C outhost 127.0.0.1 C A
OK outhost set A C outport 19 C A OK outbound port set A C start C A OK
tunnel starting 

Пока что ошибки не было, пункт назначения с именем \"mouth\" установлен.
Когда вы подключаетесь к указанному пункту, вы на самом деле
соединяетесь со службой `CHARGEN` на порту `19/TCP`.

А теперь вторая половина, мы на самом деле подключаемся к пункту
назначения.

 FROM TO DIALOGUE C A BOB 00.00.10 C A OK A
C setnick ear C A OK Nickname set to ear A C newkeys C A OK
8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg\~3eXtL-7S-qU-wdP-6VF\~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J\~flAvF4wrbF-LfVpMdg\~tjtns6fA\~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f\~dzoRCapAGDDTTnvjXuLrZ-vN-orT\~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A C inhost 127.0.0.1 C A OK inhost set A C inport 37337 C A OK inbound
port set A C start C A OK tunnel starting A C quit C A OK Bye! 

Все, что нам теперь осталось сделать - подключиться по telnet к
127.0.0.1 на порт 37337, отправить ключ пункта назначения или адрес узла
из адресной книги, к которому мы хотим подключиться. В нашем случае, мы
хотим подключиться к \"mouth\", мы вставляем ключ и понеслась.

**ПРИМЕЧАНИЕ:** Команда \"quit\" в канале команд НЕ выполняет разрыв
соединения туннелей, как это делает SAM.

 \$ telnet 127.0.0.1 37337 Trying
127.0.0.1\... Connected to 127.0.0.1. Escape character is \'\^\]\'.
ZMPz1zinTdy3\~zGD\~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr\~0g2-l0vM7Y8nSqtFrSdMw\~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU\~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq\~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw\~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefg
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefgh
\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghi
#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghij
\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghijk
\... 

После пары виртуальных километров этой отрыжки нажмите `Control-]`

 \... cdefghijklmnopqrstuvwxyz{\|}\~
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{\|}\~
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{\|}\~ !\"#\$%&\'()\*+,-./0123456789:;\<= telnet\>
c Connection closed. 

И вот что произошло\...

 telnet -\> ear -\> i2p -\> mouth -\>
chargen -. telnet \<- ear \<- i2p \<- mouth \<\-\-\-\-\-\-\-\-\-\--\' 

Также вы не можете подключиться к I2P SITES!

 \$ telnet 127.0.0.1 37337 Trying
127.0.0.1\... Connected to 127.0.0.1. Escape character is \'\^\]\'.
i2host.i2p GET / HTTP/1.1 HTTP/1.1 200 OK Date: Fri, 05 Dec 2008
14:20:28 GMT Connection: close Content-Type: text/html Content-Length:
3946 Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT Accept-Ranges: bytes
\<html\> \<head\> \<title\>I2HOST\</title\> \<link rel=\"shortcut icon\"
href=\"favicon.ico\"\> \</head\> \... \<a
href=\"http://sponge.i2p/\"\>\--Sponge.\</a\>\</pre\> \<img
src=\"/counter.gif\" alt=\"!@\^7A76Z!#(\*&amp;%\"\> visitors. \</body\>
\</html\> Connection closed by foreign host. \$ 

Прикольно, правда? Если хотите, попробуйте другие известные I2P SITES,
несуществующие, и т.д., чтобы понять что можно ожидать на выходе в
различных ситуациях. По большей части предполагается что вы игнорируете
любые сообщения об ошибках. Они будут бессмысленными для приложения, и
выводятся только для отладки человеком.

Давайте теперь отключим наши пункты назначения, т.к. мы уже с ними
закончили.

Для начала посмотрим, какие имена пунктов у нас есть.

 FROM TO DIALOGUE A C list C A DATA
NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true
QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST:
127.0.0.1 C A DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING:
false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT:
not_set OUTHOST: localhost C A OK Listing done 

Отлично, вот и они. Сначала давайте уберем \"mouth\".

 FROM TO DIALOGUE A C getnick mouth C A OK
Nickname set to mouth A C stop C A OK tunnel stopping A C clear C A OK
cleared 

Теперь уберем \"ear\", и вот что происходит, когда вы печатаете слишком
быстро, также вы увидите, как выглядят типичные сообщения об ОШИБКАХ.

 FROM TO DIALOGUE A C getnick ear C A OK
Nickname set to ear A C stop C A OK tunnel stopping A C clear C A ERROR
tunnel is active A C clear C A OK cleared A C quit C A OK Bye! 

Я не стану показывать пример получателя моста, потому что это слишком
просто. Для него есть два доступных режима, и они переключаются командой
\"quiet\".

По умолчанию этот режим отключен, и первые данные, которые приходят на
ваш слушающий сокет - это пункт назначения, который к вам подключается.
Это одна строка, состоящая из BASE64 адреса, оканчивающаяся переводом
строки. Все остальное после нее предназначено для обработки приложением.

Тихий режим можно представить в виде обычного интернет-подключения.
Никаких дополнительных данных не приходит вовсе. Просто как будто вы
подключились к обычному интернету. Этот режим предоставляет такую же
форму прозрачности, какая доступна на странице настроек туннеля консоли
маршрутизатора, и поэтому вы можете использовать BOB, например, для
указания пункта назначения на веб-сервере, и вам совсем не нужно
изменять веб-сервер.

Преимущества использования BOB, как описано ранее. Вы можете
запланировать произвольное время работы приложения, перенаправить на
другую машину, и т.п. Одним из применений этого может быть желание
попробовать испортить оценку доступности канала
\"маршрутизатор\"-\"пункт назначения\". Вы можете опускать и поднимать
пункт назначения совершенно другим способом, чтобы выполнять
произвольную остановку и запуск службы. Таким методом вы будете только
отключать возможность подключения к такой службе и не будете вынуждены
останавливать и перезапускать ее. Вы можете перенаправить или указать на
другую машину в вашей LAN пока вы выполняете обновление, или указать на
набор запасных машин в зависимости от того, что запущено, и т.д. Ваши
возможности взаимодействия с BOB ограничены только вашим воображением.


