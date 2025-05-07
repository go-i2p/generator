 Configurando o
software IRC 2020-11
0.9.47 

# Software IRC

- [Clients](#clients)
- [Servers](#servers)

[]{#clients}

## Clientes

There are many IRC clients that can be used with I2P. In fact, all IRC
clients can be connected to the Irc2P Service by connecting them to the
IRC Tunnel.

- [Pidgin(Windows, Linux) Adium(OSX)](#pidgin)
- [XChat(Windows, Linux) XChat Aqua(OSX)](#xchat)
- [Thunderbird(Windows, Linux, OSX)](#thunderbird)
- [Revolution IRC(Android)](#revolution)
- [Dispatch(Windows, Linux, OSX)(WebClient)](#dispatch)

### Check the IRC tunnel

Para configurar qualquer cliente IRC para conversar no Irc2P, primeiro,
certifique-se de que seu túnel IRC esteja disponível. Visite o [Hidden
Services Manager](http://127.0.0.1:7657/i2ptunnel/) e procure por Irc2P
na sua seção \"Client Tunnels\". Se o indicador \"Status\" no lado
direito estiver amarelo ou verde, seu túnel Irc2P está pronto e você
deve prosseguir para a próxima etapa.

![IRC Tunnel
Check](images/irc/tuncheck-irc-all.png "IRC Tunnel Check")

Qualquer cliente IRC pode ser conectado a este túnel IRC, mas instruções
detalhadas para vários clientes populares são fornecidas abaixo.

[]{#pidgin}

### Pidgin

Pidgin is a very popular Instant Messaging client with built-in IRC
support. It is also possible to use it with many other kinds of chat
service, and it supports using multiple accounts at once and has a
variety of plugin-ins. There is a similar application for OSX called
\"Adium.\" The instructions for Pidgin are similar in Adium.

![Open the
menu](images/irc/pidgin-irc-0.png "Pidgin Step One")

Após iniciar o Pidgin, você deverá ver uma janela \"Buddy List\". A
partir de essa janela, abra o menu \"Accounts\" na barra de ferramentas.
Selecione \"Manage Accounts\" para começar a configurar sua conta I2P.

![Add the
account](images/irc/pidgin-irc-1.png "Pidgin Step Two")

Clique no botão \"Adicionar\". Na janela que se abre, selecione \"IRC\"
em \"Protocolo\" e defina o \"Host\" para 127.0.0.1. Em seguida, escolha
um nome de usuário e uma senha. O IRC não exige que você registre um
apelido para entrar, mas você pode, se desejar, depois de você se
conectar ao Irc2P.

![Configure username, hostname,
password](images/irc/pidgin-irc-2.png "Pidgin Step Three")

Navegue até a aba \"Avançado\" e defina o campo \"Porta\" como 6668 e
certifique-se de que o SSL esteja *desabilitado*, já que seu túnel tem
criptografia fornecida pelo I2P.

![Configure
port](images/irc/pidgin-irc-3.png "Pidgin Step Four")
[]{#xchat}

### XChat

Abra o menu Lista de Servidores do XChat e clique no botão
\"Adicionar\".

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

Feche a janela \"Editar servidor\" para retornar à página Lista de
servidores e clique em \"Conectar\" para ingressar no I2PRC.

![Add a
server](images/irc/xchat-irc-3.png "XChat Step Four")
[]{#thunderbird}

### Thunderbird

Clique no botão \"Bate-papo\" na barra de ferramentas na parte superior
da janela do Thunderbird.

![Add a
chat](images/irc/thunderbird-irc-0.png "Thunderbird Step One")

Clique no botão começar para começar a configurar o Irc2P.

![Get
Started](images/irc/thunderbird-irc-1.png "Thunderbird Step Two")

No primeiro passo, selecione \"IRC\" para seu tipo de rede.

![Pick
IRC](images/irc/thunderbird-irc-2.png "Thunderbird Step Three")

Escolha um apelido e defina seu servidor IRC como 127.0.0.1, mas não
defina uma porta.

![Set username and
server](images/irc/thunderbird-irc-3.png "Thunderbird Step Four")

Defina uma senha se desejar.

![Add a
server](images/irc/thunderbird-irc-4.png "Thunderbird Step Five")

Configure o servidor IRC com um alias como \"Irc2P\" e defina a porta
como 6668.

![Add a
server](images/irc/thunderbird-irc-5.png "Thunderbird Step Six")

Se o seu resumo for parecido com este, então você está pronto para
conectar com Irc2P.

![Add a
server](images/irc/thunderbird-irc-6.png "Thunderbird Step Seven")
[]{#revolution}

### Revolution IRC

Revolution IRC é um cliente IRC fácil de usar para Android. Ele é capaz
de lidar com múltiplas contas em múltiplos serviços, então você pode
usá-lo para Irc2P e para suas redes IRC não-I2P também.

Clique no botão \"Adicionar servidor\" (com o formato assim: \`+\`) no
canto para começar a configurar o Revolution IRC para I2P.

![Add a
server](images/irc/revolution-irc-0.png "Revolution Step One")

Preencha o nome do servidor, altere o endereço para \"127.0.0.1\" e a
porta para 6668.

![Configure it like
this](images/irc/revolution-irc-1.png "Revolution Step Two")

Dê a si mesmo um apelido e configure alguns canais para entrarem
automaticamente .

![Open the
menu](images/irc/revolution-irc-2.png "Revolution Step Three")
[]{#dispatch}

### Dispatch

Dispatch é um cliente IRC estável e auto-hospedado com uma interface
web. Ele tem configuração I2P nativa disponível por comunicação através
do [SAM v3 API]().

O Dispatch é configurado com um arquivo chamado \`config.toml\`, que
você pode configurar as configurações comuns.

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

## Servidores

- [Eris(Windows, OSX, Linux)](#eris)

[]{#eris}

### Eris

Eris é um servidor IRC fácil de configurar com suporte de
autoconfiguração para I2P. Se você quer rodar um servidor IRC privado,
essa é uma das maneiras mais fáceis.

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


