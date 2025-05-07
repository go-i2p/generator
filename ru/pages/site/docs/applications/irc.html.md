 Настройка ПО IRC 2020-11 0.9.47 

# IRC ПО

- [Clients](#clients)
- [Servers](#servers)

[]{#clients}

## Клиенты

There are many IRC clients that can be used with I2P. In fact, all IRC
clients can be connected to the Irc2P Service by connecting them to the
IRC Tunnel.

- [Pidgin(Windows, Linux) Adium(OSX)](#pidgin)
- [XChat(Windows, Linux) XChat Aqua(OSX)](#xchat)
- [Thunderbird(Windows, Linux, OSX)](#thunderbird)
- [Revolution IRC(Android)](#revolution)
- [Dispatch(Windows, Linux, OSX)(WebClient)](#dispatch)

### Check the IRC tunnel

Чтобы настроить любой IRC-клиент для чата на Irc2P, сначала убедитесь,
что ваш IRC-туннель доступен. Зайдите в [Менеджер спрятанных
сервисов](http://127.0.0.1:7657/i2ptunnel/) и найдите Irc2P в разделе
\"Туннели клиентов\". Если индикатор \"Статус\" с правой стороны желтый
или зеленый, ваш туннель Irc2P готов, и вам следует перейти к следующему
шагу.

![IRC Tunnel
Check](images/irc/tuncheck-irc-all.png "IRC Tunnel Check")

К этому IRC-туннелю можно подключить любой IRC-клиент, подробные
инструкции для нескольких популярных клиентов приведены ниже.

[]{#pidgin}

### Pidgin

Pidgin is a very popular Instant Messaging client with built-in IRC
support. It is also possible to use it with many other kinds of chat
service, and it supports using multiple accounts at once and has a
variety of plugin-ins. There is a similar application for OSX called
\"Adium.\" The instructions for Pidgin are similar in Adium.

![Open the
menu](images/irc/pidgin-irc-0.png "Pidgin Step One")

После запуска Pidgin у вас должно появиться окно \"Список друзей\". Из
этого окна откройте меню \"Учетные записи\" на панели инструментов.
Выберите \"Управление учетными записями\", чтобы начать настройку.

![Add the
account](images/irc/pidgin-irc-1.png "Pidgin Step Two")

Нажмите кнопку \"Добавить\". В открывшемся окне выберите \"IRC\" в
разделе \"Протокол\" и установите \"Хост\" на 127.0.0.1. Затем выберите
имя пользователя и пароль. IRC не требует регистрации псевдонима для
присоединения, но вы можете, если захотите, после того как подключитесь
к Irc2P.

![Configure username, hostname,
password](images/irc/pidgin-irc-2.png "Pidgin Step Three")

Перейдите на вкладку \"Дополнительно\" и установите в поле \"Порт\"
значение 6668 и убедитесь, что SSL *отключен*, так как ваш туннель имеет
шифрование, обеспечиваемое I2P.

![Configure
port](images/irc/pidgin-irc-3.png "Pidgin Step Four")
[]{#xchat}

### XChat

Откройте меню \"Список серверов\" в XChat и нажмите кнопку \"Добавить\".

![Add a
server](images/irc/xchat-irc-0.png "XChat Step One")

Create a new network named \"Irc2P\" to configure for I2P IRC. Click the
\"Edit\" button on the right-hand side. Make sure you disable TLS and
SSL inside I2P.

![Add a
server](images/irc/xchat-irc-1.png "XChat Step Two")

Change the value in \"Servers\" from the default to \`localhost/6668\`,
and configure the default channels you want to join. I suggest #i2p and
#i2p-dev

![Add a
server](images/irc/xchat-irc-2.png "XChat Step Three")

Закройте окно \"Редактировать сервер\", чтобы вернуться на страницу
Список Серверов и нажмите \"Подключить\", чтобы присоединиться к I2PRC.

![Add a
server](images/irc/xchat-irc-3.png "XChat Step Four")
[]{#thunderbird}

### Thunderbird

Нажмите кнопку \"Чат\" на панели инструментов в верхней части окна
Thunderbird.

![Add a
chat](images/irc/thunderbird-irc-0.png "Thunderbird Step One")

Нажмите кнопку \"Начать работу\", чтобы начать настройку Irc2P.

![Get
Started](images/irc/thunderbird-irc-1.png "Thunderbird Step Two")

На первом этапе выберите \"IRC\" в качестве типа сети.

![Pick
IRC](images/irc/thunderbird-irc-2.png "Thunderbird Step Three")

Выберите ник и установите ваш IRC-сервер на 127.0.0.1, но не
устанавливайте порт.

![Set username and
server](images/irc/thunderbird-irc-3.png "Thunderbird Step Four")

При желании установите пароль.

![Add a
server](images/irc/thunderbird-irc-4.png "Thunderbird Step Five")

Настройте IRC-сервер с псевдонимом \"Irc2P\" и установите порт на 6668.

![Add a
server](images/irc/thunderbird-irc-5.png "Thunderbird Step Six")

Если ваша сводка выглядит примерно так, значит, вы готовы к подключению
к Irc2P.

![Add a
server](images/irc/thunderbird-irc-6.png "Thunderbird Step Seven")
[]{#revolution}

### Revolution IRC

Revolution IRC - это простой в использовании IRC-клиент для Android. Он
способен работать с несколькими учетными записями на нескольких
сервисах, поэтому вы можете использовать его как для Irc2P, так и для
ваших не-I2P IRC сетей.

Нажмите кнопку \"Добавить сервер\" (в форме, как здесь: \`+\`) в углу,
чтобы начать настройку Revolution IRC для I2P.

![Add a
server](images/irc/revolution-irc-0.png "Revolution Step One")

Заполните имя сервера, измените адрес на \"127.0.0.1\" и порт на 6668.

![Configure it like
this](images/irc/revolution-irc-1.png "Revolution Step Two")

Дайте себе псевдоним и настройте некоторые каналы на автоматическое
присоединение.

![Open the
menu](images/irc/revolution-irc-2.png "Revolution Step Three")
[]{#dispatch}

### Dispatch

Dispatch - это стабильный, самостоятельно размещаемый IRC-клиент с
веб-интерфейсом. Он имеет встроенную I2P-конфигурацию, доступную при
общении через [SAM v3
API]().

Диспетчер конфигурируется с помощью файла \`config.toml\`, в котором
можно настроить общие параметры.

 # Defaults for the client connect form
 [defaults]
 name = "myinvisibleirc.i2p"
 host = "anircservergoeshere.b32.i2p"
 port = 6667
 channels = [
 "#i2p",
 "#i2p-dev"
 ]
 server_password = ""
 ssl = false

[]{#servers}

## Серверы

- [Eris(Windows, OSX, Linux)](#eris)

[]{#eris}

### Eris

Eris - это простой в настройке IRC-сервер с поддержкой самонастройки для
I2P. Если вы хотите запустить частный IRC-сервер, это один из самых
простых способов.

This is a valid configuration of the Eris IRC server, but it uses a
default password for the admin account(admin). You should change the
operator.admin.password and account.admin.password before deploying to a
real service.

 mutex: {}
 network:
 name: Local
 server:
 password: ""
 listen: []
 tlslisten: {}
 i2plisten:
 invisibleirc:
 i2pkeys: iirc
 samaddr: 127.0.0.1:7656
 log: ""
 motd: ircd.motd
 name: myinvisibleirc.i2p
 description: Hidden IRC Services
 operator:
 admin:
 password: JDJhJDA0JE1vZmwxZC9YTXBhZ3RWT2xBbkNwZnV3R2N6VFUwQUI0RUJRVXRBRHliZVVoa0VYMnlIaGsu
 account:
 admin:
 password: JDJhJDA0JGtUU1JVc1JOUy9DbEh1WEdvYVlMdGVnclp6YnA3NDBOZGY1WUZhdTZtRzVmb1VKdXQ5ckZD
 www: 
 listen: []
 tlslisten: {}
 i2plisten:
 i2pinfoirc:
 i2pkeys: iircwww
 samaddr: "127.0.0.1:7656"
 templatedir: lang


