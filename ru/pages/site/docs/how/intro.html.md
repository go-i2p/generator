 Мягкое введение в
работу I2P 

I2P is a project to build, deploy, and maintain a network supporting
secure and anonymous communication. People using I2P are in control of
the tradeoffs between anonymity, reliability, bandwidth usage, and
latency. There is no central point in the network on which pressure can
be exerted to compromise the integrity, security, or anonymity of the
system. The network supports dynamic reconfiguration in response to
various attacks, and has been designed to make use of additional
resources as they become available. Of course, all aspects of the
network are open and freely available.

В отличие от многих других анонимизирующих сетей, I2P не пытается
обеспечить анонимность, скрывая отправителя некоторого сообщения, но не
получателя, или наоборот. I2P разработана для того, чтобы позволить
равным пользователям I2P общаться друг с другом анонимно --- и
отправитель, и получатель не идентифицируемы ни друг для друга, ни для
третьих лиц. Например, сегодня существуют как веб-сайты внутри I2P
(позволяющие анонимно публиковать / размещать информацию), так и
HTTP-прокси для обычного Интернета (позволяющие анонимно просматривать
веб-страницы). Возможность запуска серверов внутри I2P очень важна, так
как вполне вероятно, что любые исходящие прокси в обычный Интернет будут
отслеживаться, отключаться или даже захватываться для попыток более
злонамеренных атак.

The network itself is message oriented - it is essentially a secure and
anonymous IP layer, where messages are addressed to cryptographic keys
(Destinations) and can be significantly larger than IP packets. Some
example uses of the network include \"I2P Sites\" (webservers hosting
normal web applications within I2P), a BitTorrent client (\"I2PSnark\"),
or a distributed data store. With the help of the
[I2PTunnel]() application, we are able to
stream traditional TCP/IP applications over I2P, such as SSH, IRC, a
squid proxy, and even streaming audio. Most people will not use I2P
directly, or even need to know they\'re using it. Instead their view
will be of one of the I2P enabled applications, or perhaps as a little
controller app to turn on and off various proxies to enable the
anonymizing functionality.

An essential part of designing, developing, and testing an anonymizing
network is to define the [threat model](),
since there is no such thing as \"true\" anonymity, just increasingly
expensive costs to identify someone. Briefly, I2P\'s intent is to allow
people to communicate in arbitrarily hostile environments by providing
good anonymity, mixed in with sufficient cover traffic provided by the
activity of people who require less anonymity. This way, some users can
avoid detection by a very powerful adversary, while others will try to
evade a weaker entity, *all on the same network*, where each one\'s
messages are essentially indistinguishable from the others.

## Почему?

There are a multitude of reasons why we need a system to support
anonymous communication, and everyone has their own personal rationale.
There are many [other efforts]() working on
finding ways to provide varying degrees of anonymity to people through
the Internet, but we could not find any that met our needs or threat
model.

## Как?

The network at a glance is made up of a set of nodes (\"routers\") with
a number of unidirectional inbound and outbound virtual paths
(\"tunnels\", as outlined on the [tunnel
routing]() page). Each router is
identified by a cryptographic RouterIdentity which is typically long
lived. These routers communicate with each other through existing
transport mechanisms (TCP, UDP, etc), passing various messages. Client
applications have their own cryptographic identifier (\"Destination\")
which enables it to send and receive messages. These clients can connect
to any router and authorize the temporary allocation (\"lease\") of some
tunnels that will be used for sending and receiving messages through the
network. I2P has its own internal [network
database]() (using a modification of the Kademlia
algorithm) for distributing routing and contact information securely.

::: {.box style="text-align:center;"}
![Пример сетевой
топологии](images/net.png "Пример сетевой топологии")
:::

In the above, Alice, Bob, Charlie, and Dave are all running routers with
a single Destination on their local router. They each have a pair of
2-hop inbound tunnels per destination (labeled 1, 2, 3, 4, 5 and 6), and
a small subset of each of those router\'s outbound tunnel pool is shown
with 2-hop outbound tunnels. For simplicity, Charlie\'s inbound tunnels
and Dave\'s outbound tunnels are not shown, nor are the rest of each
router\'s outbound tunnel pool (typically stocked with a few tunnels at
a time). When Alice and Bob talk to each other, Alice sends a message
out one of her (pink) outbound tunnels targeting one of Bob\'s (green)
inbound tunnels (tunnel 3 or 4). She knows to send to those tunnels on
the correct router by querying the network database, which is constantly
updated as new leases are authorized and old ones expire.

If Bob wants to reply to Alice, he simply goes through the same
process - send a message out one of his outbound tunnels targeting one
of Alice\'s inbound tunnels (tunnel 1 or 2). To make things easier, most
messages sent between Alice and Bob are
[garlic]() wrapped, bundling the
sender\'s own current lease information so that the recipient can reply
immediately without having to look in the network database for the
current data.

To deal with a wide range of attacks, I2P is fully distributed with no
centralized resources - and hence there are no directory servers keeping
statistics regarding the performance and reliability of routers within
the network. As such, each router must keep and maintain profiles of
various routers and is responsible for selecting appropriate peers to
meet the anonymity, performance, and reliability needs of the users, as
described in the [peer selection]() page.

The network itself makes use of a significant number of [cryptographic
techniques and algorithms]() - a full
laundry list includes 2048bit ElGamal encryption, 256bit AES in CBC mode
with PKCS#5 padding, 1024bit DSA signatures, SHA256 hashes, 2048bit
Diffie-Hellman negotiated connections with station to station
authentication, and [ElGamal /
AES+SessionTag]().

Content sent over I2P is encrypted through three layers garlic
encryption (used to verify the delivery of the message to the
recipient), tunnel encryption (all messages passing through a tunnel is
encrypted by the tunnel gateway to the tunnel endpoint), and inter
router transport layer encryption (e.g. the TCP transport uses AES256
with ephemeral keys).

Сквозное (I2CP) шифрование (клиентское приложение к серверному
приложению) было отключено в релизе I2P 0.6; сквозное (чесночное)
шифрование (маршрутизатор клиента I2P к маршрутизатору сервера I2P) от
маршрутизатора Алисы \"a\" к маршрутизатору Боба \"h\" осталось.
Обратите внимание на разное использование терминов! Все данные от a до h
шифруются из конца в конец, но I2CP-соединение между маршрутизатором I2P
и приложениями не шифруется из конца в конец! A и h - это маршрутизаторы
Алисы и Боба, а Алиса и Боб на следующей схеме - это приложения,
работающие на I2P.

::: {.box style="text-align:center;"}
![Многоуровневое шифрование от конца до
конца](images/endToEndEncryption.png "Многоуровневое шифрование от конца до конца")
:::

The specific use of these algorithms are outlined
[elsewhere]().

Два основных механизма, позволяющих людям, которым нужна сильная
анонимность, использовать сеть, - это явно отложенные чесночные
маршрутизируемые сообщения и более полные туннели, включающие поддержку
объединения и смешивания сообщений. В настоящее время эти механизмы
запланированы на релиз 3.0, но уже существуют чесночные маршрутизируемые
сообщения без задержек и туннели FIFO. Кроме того, релиз 2.0 позволит
людям устанавливать и работать за ограниченными маршрутами (возможно, с
доверенными пирами), а также развертывать более гибкие и анонимные
транспорты.

Some questions have been raised with regards to the scalability of I2P,
and reasonably so. There will certainly be more analysis over time, but
peer lookup and integration should be bounded by `O(log(N))` due to the
[network database]()\'s algorithm, while end to
end messages should be `O(1)` (scale free), since messages go out K hops
through the outbound tunnel and another K hops through the inbound
tunnel, with K no longer than 3. The size of the network (N) bears no
impact.

## Когда?

I2P initially began in Feb 2003 as a proposed modification to
[Freenet](http://freenetproject.org) to allow it to use alternate
transports, such as [JMS](), then grew into its own
as an \'anonCommFramework\' in April 2003, turning into I2P in July,
with code being written in earnest starting in August \'03. I2P is
currently under development, following the
[roadmap]().

## Кто?

We have a small [team]() spread around several
continents, working to advance different aspects of the project. We are
very open to other developers who want to get involved and anyone else
who would like to contribute in other ways, such as critiques, peer
review, testing, writing I2P enabled applications, or documentation. The
entire system is open source - the router and most of the SDK are
outright public domain with some BSD and Cryptix licensed code, while
some applications like I2PTunnel and I2PSnark are GPL. Almost everything
is written in Java (1.5+), though some third party applications are
being written in Python and other languages. The code works on [Sun Java
SE](http://java.com/en/) and other Java Virtual Machines.

## Где?

Anyone interested should join us on the IRC channel #i2p-dev (hosted
concurrently on irc.freenode.net, irc.postman.i2p, irc.echelon.i2p,
irc.dg.i2p and irc.oftc.net). There are currently no scheduled
development meetings, however [archives are
available]().

The current source is available in [git]().

## Дополнительная информация

See [the Index to Technical Documentation]().


