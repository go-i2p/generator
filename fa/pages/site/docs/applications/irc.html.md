 Configuring IRC
Software 2020-11 0.9.47 

# IRC Software

- [Clients](#clients)
- [Servers](#servers)

[]{#clients}

## کلاینت ها

There are many IRC clients that can be used with I2P. In fact, all IRC
clients can be connected to the Irc2P Service by connecting them to the
IRC Tunnel.

- [Pidgin(Windows, Linux) Adium(OSX)](#pidgin)
- [XChat(Windows, Linux) XChat Aqua(OSX)](#xchat)
- [Thunderbird(Windows, Linux, OSX)](#thunderbird)
- [Revolution IRC(Android)](#revolution)
- [Dispatch(Windows, Linux, OSX)(WebClient)](#dispatch)

### Check the IRC tunnel

To configure any IRC client to chat on Irc2P, first, make sure that your
IRC tunnel is available. Visit the [Hidden Services
Manager](http://127.0.0.1:7657/i2ptunnel/) and look for Irc2P in your
\"Client Tunnels\" section. If the \"Status\" indicator on the
right-hand side is yellow or green, your Irc2P tunnel is ready and you
should proceed to the next step.

![IRC Tunnel
Check](images/irc/tuncheck-irc-all.png "IRC Tunnel Check")

Any IRC client can be connected to this IRC tunnel, but detailed
instructions for several popular clients are provided below.

[]{#pidgin}

### Pidgin

Pidgin is a very popular Instant Messaging client with built-in IRC
support. It is also possible to use it with many other kinds of chat
service, and it supports using multiple accounts at once and has a
variety of plugin-ins. There is a similar application for OSX called
\"Adium.\" The instructions for Pidgin are similar in Adium.

![Open the
menu](images/irc/pidgin-irc-0.png "Pidgin Step One")

After launching Pidgin, you should see a \"Buddy List\" window. From
that window, open the \"Accounts\" menu from the toolbar. Select
\"Manage Accounts\" to begin configuring your I2P account.

![Add the
account](images/irc/pidgin-irc-1.png "Pidgin Step Two")

Click the \"Add\" button. In the window that opens, select \"IRC\" under
\"Protocol,\" and set the \"Host\" to 127.0.0.1. Then pick a username
and password. IRC does not require you to register a nickname to join,
but you may if you wish, after you connect to Irc2P.

![Configure username, hostname,
password](images/irc/pidgin-irc-2.png "Pidgin Step Three")

Navigate to the \"Advanced\" tab and set the \"Port\" field to 6668 and
make sure that SSL is *disabled*, since your tunnel has encryption
provided by I2P.

![Configure
port](images/irc/pidgin-irc-3.png "Pidgin Step Four")
[]{#xchat}

### XChat

Open the Server List menu of XChat and click the \"Add\" button.

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

Close the \"Edit Server\" window from to return to the Server List page
and click \"Connect\" to join I2PRC.

![Add a
server](images/irc/xchat-irc-3.png "XChat Step Four")
[]{#thunderbird}

### Thunderbird

Click on the \"Chat\" button in the toolbar at the top of the
Thunderbird window.

![Add a
chat](images/irc/thunderbird-irc-0.png "Thunderbird Step One")

Click the get started button to begin setting up Irc2P.

![Get
Started](images/irc/thunderbird-irc-1.png "Thunderbird Step Two")

In the first step, select \"IRC\" for your network type.

![Pick
IRC](images/irc/thunderbird-irc-2.png "Thunderbird Step Three")

Choose a nickname and set your IRC Server to 127.0.0.1, but do not set a
port.

![Set username and
server](images/irc/thunderbird-irc-3.png "Thunderbird Step Four")

Set a password if you want.

![Add a
server](images/irc/thunderbird-irc-4.png "Thunderbird Step Five")

Configure the IRC Server with an alias like \"Irc2P\" and set the port
to 6668.

![Add a
server](images/irc/thunderbird-irc-5.png "Thunderbird Step Six")

If your summary looks like this, then you\'re ready to connect with
Irc2P.

![Add a
server](images/irc/thunderbird-irc-6.png "Thunderbird Step Seven")
[]{#revolution}

### Revolution IRC

Revolution IRC is an easy to use IRC client for Android. It\'s able to
handle multiple accounts on multiple services, so you can use it for
Irc2P and for your non-I2P IRC networks as well.

Click the \"Add Server\" button(Shaped like this: \`+\`) in the corner
to get started configuring Revolution IRC for I2P.

![Add a
server](images/irc/revolution-irc-0.png "Revolution Step One")

Fill in the server name, change the address to \"127.0.0.1\" and the
port to 6668.

![Configure it like
this](images/irc/revolution-irc-1.png "Revolution Step Two")

Give yourself a nickname and configure some channels to automatically
join.

![Open the
menu](images/irc/revolution-irc-2.png "Revolution Step Three")
[]{#dispatch}

### Dispatch

Dispatch is a stable, self-hosted IRC client with a web interface. It
has native I2P configuration available by communicating over the [SAM v3
API]().

Dispatch is configured with a file called \`config.toml\`, which you can
configure the common settings.

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

## سرورها

- [Eris(Windows, OSX, Linux)](#eris)

[]{#eris}

### Eris

Eris is an easy-to-configure IRC server with self-configuring support
for I2P. If you want to run a private IRC server it\'s one of the
easiest ways.

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


