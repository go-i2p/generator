 Incorporando I2P
em seu aplicativo 2023-01 2.1.0 

## Sinopse

Esta página é sobre agrupar todo o binário do roteador I2P com seu
aplicativo. Não se trata de escrever um aplicativo para trabalhar com
I2P (agrupado ou externo). However, many of the guidelines may be useful
even if not bundling a router.

Muitos projetos estão agrupando, ou falando sobre agrupar, I2P. Isso é
ótimo se feito corretamente. Se feito errado, pode causar danos reais à
nossa rede. O roteador I2P é complexo, e pode ser um desafio esconder
toda a complexidade dos seus usuários. Esta página discute algumas
diretrizes gerais.

Most of these guidelines apply equally to Java I2P or i2pd. However,
some guidelines are specific to Java I2P and are noted below.

### Fale conosco

Inicie um diálogo. Estamos aqui para ajudar. Os aplicativos que
incorporam I2P são as oportunidades mais promissoras - e empolgantes -
para que possamos expandir a rede e melhorar o anonimato para todos.

### Escolha seu roteador com sabedoria

Se seu aplicativo estiver em Java ou Scala, é uma escolha fácil - use o
roteador Java. Se estiver em C/C++, recomendamos o i2pd. O
desenvolvimento do i2pcpp foi interrompido. Para aplicativos em outras
linguagens, é melhor usar SAM ou BOB ou SOCKS e agrupar o roteador Java
como um processo separado. Alguns dos seguintes se aplicam apenas ao
roteador Java.

### Licenciamento

Certifique-se de atender aos requisitos de licença do software que você
está empacotando.

## Configuration

### Verificar pré-configuração

Uma configuração padrão correta é crucial. A maioria dos usuários não
alterará os padrões. Os padrões para seu aplicativo podem precisar ser
diferentes dos padrões para o roteador que você está empacotando.
Substitua os padrões do roteador, se necessário.

Alguns padrões importantes a serem revisados: largura de banda máxima,
quantidade e comprimento do túnel, número máximo de túneis
participantes. Muito disso depende da largura de banda esperada e dos
padrões de uso do seu aplicativo.

Configure largura de banda e túneis suficientes para permitir que seus
usuários contribuam com a rede. Considere desabilitar o I2CP externo,
pois você provavelmente não precisa dele e ele entraria em conflito com
qualquer outra instância I2P em execução. Veja também as configurações
para desabilitar a eliminação da JVM na saída, por exemplo.

### Considerações sobre o tráfego participante

Pode ser tentador desabilitar o tráfego participante. Há várias maneiras
de fazer isso (modo oculto, definir o máximo de túneis como 0, definir a
largura de banda compartilhada abaixo de 12 KBytes/seg). Sem tráfego
participante, você não precisa se preocupar com desligamento normal,
seus usuários não veem o uso de largura de banda não gerado por eles,
etc. No entanto, há muitos motivos pelos quais você deve permitir túneis
participantes.

Primeiro, o roteador não funciona tão bem se não tiver a chance de
\"integrar-se\" com a rede, o que é muito ajudado por outros construindo
túneis através de você.

Em segundo lugar, mais de 90% dos roteadores na rede atual permitem
tráfego participante. É o padrão no roteador Java. Se seu aplicativo não
rotear para outros e se tornar muito popular, então ele é um sanguessuga
na rede, e perturba o equilíbrio que temos agora. Se ficar muito grande,
então nos tornamos Tor e passamos nosso tempo implorando para que as
pessoas habilitem o retransmissão.

Em terceiro lugar, o tráfego participante é o tráfego de cobertura que
ajuda no anonimato dos seus usuários.

Não recomendamos fortemente que você desabilite o tráfego participante
por padrão. Se você fizer isso e seu aplicativo se tornar muito popular,
isso poderá danificar a rede.

### Persistência

You must save the router\'s data (netdb, configuration, etc.) between
runs of the router. I2P does not work well if you must reseed each
startup, and that\'s a huge load on our reseed servers, and not very
good for anonymity either. Even if you bundle router infos, I2P needs
saved profile data for best performance. Without persistence, your users
will have a poor startup experience.

There are two possibilities if you cannot provide persistence. Either of
these eliminates your project\'s load on our reseed servers and will
significantly improve startup time.

1\) Set up your own project reseed server(s) that serve much more than
the usual number of router infos in the reseed, say, several hundred.
Configure the router to use only your servers.

2\) Bundle one to two thousand router infos in your installer.

Also, delay or stagger your tunnel startup, to give the router a chance
to integrate before building a lot of tunnels.

### Configurabilidade

Dê aos seus usuários uma maneira de alterar a configuração das
configurações importantes. Entendemos que você provavelmente desejará
ocultar a maior parte da complexidade do I2P, mas é importante mostrar
algumas configurações básicas. Além dos padrões acima, algumas
configurações de rede, como UPnP, IP/porta, podem ser úteis.

### Considerações sobre aterro

Acima de uma certa configuração de largura de banda, e atendendo a
outros critérios de saúde, seu roteador se tornará floodfill, o que pode
causar um grande aumento nas conexões e no uso de memória (pelo menos
com o roteador Java). Pense se isso é OK. Você pode desabilitar o
floodfill, mas seus usuários mais rápidos não estão contribuindo com o
que poderiam. Também depende do tempo de atividade típico do seu
aplicativo.

### Ressemeando

Decida se você está agrupando informações do roteador ou usando nossos
hosts de reseed. A lista de hosts de reseed Java está no código-fonte,
então se você mantiver seu código-fonte atualizado, a lista de hosts
também estará. Esteja ciente de possíveis bloqueios por governos hostis.

### Use Shared Clients

Java I2P i2ptunnel supports shared clients, where clients may be
configured to use a single pool. If you require multiple clients, and if
consistent with your security goals, configure the clients to be shared.

### Limit Tunnel Quantity

Specify tunnel quantity explicitly with the options `inbound.quantity`
and `outbound.quantity`. The default in Java I2P is 2; the default in
i2pd is higher. Specify in the SESSION CREATE line using SAM to get
consistent settings with both routers. Two each in/out is sufficient for
most low-to-medium bandwidth and low-to-medium fanout applications.
Servers and high-fanout P2P applications may need more. See [this forum
post](http://zzz.i2p/topics/1584) for guidance on calculating
requirements for high-traffic servers and applications.

### Specify SAM SIGNATURE_TYPE

SAM defaults to DSA_SHA1 for destinations, which is not what you want.
Ed25519 (type 7) is the correct selection. Add SIGNATURE_TYPE=7 to the
DEST GENERATE command, or to the SESSION CREATE command for
DESTINATION=TRANSIENT.

### Limit SAM Sessions

Most applications will only need one SAM session. SAM provides the
ability to quickly overwhelm the local router, or even the broader
network, if a large number of sessions are created. If multiple
sub-services can use a single session, set them up with a PRIMARY
session and SUBSESSIONS (not currently supported on i2pd). A reasonable
limit to sessions is 3 or 4 total, or maybe up to 10 for rare
situations. If you do have multiple sessions, be sure to specify a low
tunnel quantity for each, see above.

In almost no situation should you require a unique session
per-connection. Without careful design, this could quickly DDoS the
network. Carefully consider if your security goals require unique
sessions. Please consult with the Java I2P or i2pd developers before
implementing per-connection sessions.

### Reduzir o uso de recursos de rede

Note that these options are not currently supported on i2pd. These
options are supported via I2CP and SAM (except delay-open, which is via
i2ptunnel only). See the I2CP documentation (and, for delay-open, the
i2ptunnel configuration documentation) for details.

Considere configurar os túneis do seu aplicativo para atrasar a
abertura, reduzir quando ocioso e/ou fechar quando ocioso. Isso é
simples se estiver usando o i2ptunnel, mas você terá que implementar
parte disso se estiver usando o I2CP diretamente. Veja o i2psnark para
obter o código que reduz a contagem de túneis e, em seguida, fecha o
túnel, mesmo na presença de alguma atividade DHT em segundo plano.

## Life Cycle

### Updatability

Tenha um recurso de atualização automática, se possível, ou pelo menos
notificação automática de uma nova versão. Nosso maior medo é um grande
número de roteadores que não podem ser atualizados. Temos cerca de 6 a 8
lançamentos por ano do roteador Java, e é essencial para a saúde da rede
que os usuários se mantenham atualizados. Geralmente temos mais de 80%
da rede na versão mais recente dentro de 6 semanas após o lançamento, e
gostaríamos de mantê-la assim. Você não precisa se preocupar em
desabilitar a função de atualização automática integrada do roteador,
pois esse código está no console do roteador, que você provavelmente não
está agrupando.

### Lançamento

Tenha um plano de implementação gradual. Não sobrecarregue a rede de uma
só vez. Atualmente, temos aproximadamente 25 mil usuários únicos por dia
e 40 mil únicos por mês. Provavelmente somos capazes de lidar com um
crescimento de 2 a 3 vezes por ano sem muitos problemas. Se você
antecipar um aumento mais rápido do que isso, OU a distribuição de
largura de banda (ou distribuição de tempo de atividade, ou qualquer
outra característica significativa) da sua base de usuários for
significativamente diferente da nossa base de usuários atual, realmente
precisamos ter uma discussão. Quanto maiores forem seus planos de
crescimento, mais importante será todo o resto nesta lista de
verificação.

### Projete e incentive longos períodos de atividade

Diga aos seus usuários que o I2P funciona melhor se continuar em
execução. Pode levar vários minutos após a inicialização para que ele
funcione bem, e ainda mais depois da primeira instalação. Se o seu tempo
de atividade médio for inferior a uma hora, o I2P provavelmente é a
solução errada.

## User Interface

### Mostrar status

Forneça alguma indicação ao usuário de que os túneis do aplicativo estão
prontos. Incentive a paciência.

### Desligamento elegante

Se possível, adie o desligamento até que seus túneis participantes
expirem. Não deixe que seus usuários quebrem os túneis facilmente, ou
pelo menos peça para eles confirmarem.

### Educação e Doação

Seria legal se você desse aos seus usuários links para aprender mais
sobre o I2P e fazer doações.

### Opção de roteador externo

Dependendo da sua base de usuários e aplicação, pode ser útil fornecer
uma opção ou um pacote separado para usar um roteador externo.

## Other Topics

### Uso de outros serviços comuns

Se você planeja usar ou vincular a outros serviços I2P comuns (feeds de
notícias, assinaturas hosts.txt, rastreadores, outproxies, etc.),
certifique-se de não sobrecarregá-los, e converse com as pessoas que os
executam para ter certeza de que está tudo bem.

### Problemas de tempo/NTP

Note: This section refers to Java I2P. i2pd does not include an SNTP
client.

O I2P inclui um cliente SNTP. O I2P requer o horário correto para
operar. Ele compensará um relógio de sistema distorcido, mas isso pode
atrasar a inicialização. Você pode desabilitar as consultas SNTP do I2P,
mas isso não é aconselhável a menos que seu aplicativo certifique-se de
que o relógio do sistema esteja correto.

### Escolha o que e como você deseja agrupar

Note: This section refers to Java I2P only.

No mínimo, você precisará de i2p.jar, router.jar, streaming.jar e
mstreaming.jar. Você pode omitir os dois jars de streaming para um
aplicativo somente de datagrama. Alguns aplicativos podem precisar de
mais, por exemplo, i2ptunnel.jar ou addressbook.jar. Não se esqueça do
jbigi.jar, ou de um subconjunto dele para as plataformas que você
suporta, para tornar a criptografia muito mais rápida. Java 7 ou
superior é necessário para compilar. Se você estiver compilando pacotes
Debian / Ubuntu, você deve exigir o pacote I2P do nosso PPA em vez de
agrupá-lo. Você quase certamente não precisa de susimail, susidns, o
console do roteador e i2psnark, por exemplo.

Os seguintes arquivos devem ser incluídos no diretório de instalação do
I2P, especificados com a propriedade \"i2p.dir.base\". Não se esqueça do
diretório certificates/, que é necessário para a nova propagação, e
blocklist.txt para validação de IP. O diretório geoip é opcional, mas
recomendado para que o roteador possa tomar decisões com base na
localização. Se incluir geoip, certifique-se de colocar o arquivo
GeoLite2-Country.mmdb nesse diretório (compacte-o em
installer/resources/GeoLite2-Country.mmdb.gz). O arquivo hosts.txt pode
ser necessário, você pode modificá-lo para incluir quaisquer hosts que
seu aplicativo use. Você pode adicionar um arquivo router.config ao
diretório base para substituir os padrões iniciais. Revise e edite ou
remova os arquivos clients.config e i2ptunnel.config.

Os requisitos de licença podem exigir que você inclua o arquivo
LICENSES.txt e o diretório de licenças.

- Você também pode querer agrupar um arquivo hosts.txt.
- Be sure to specify a bootclasspath if you are compiling Java I2P for
 your release, rather than taking our binaries.

### Considerações sobre Android

Note: This section refers to Java I2P only.

Nosso aplicativo de roteador Android pode ser compartilhado por vários
clientes. Se não estiver instalado, o usuário será avisado quando
iniciar um aplicativo cliente.

Alguns desenvolvedores expressaram preocupação de que esta seja uma
experiência ruim para o usuário, e desejam incorporar o roteador em seu
aplicativo. Temos uma biblioteca de serviços de roteador Android em
nosso roteiro, o que pode facilitar a incorporação. Mais informações
necessárias.

Se precisar de ajuda, entre em contato conosco.

### Potes Maven

Note: This section refers to Java I2P only.

Temos um número limitado de nossos jars no [Maven
Central](http://search.maven.org/#search%7Cga%7C1%7Cg%3A%22net.i2p%22).
Há vários tickets de rastreamento para resolvermos que melhorarão e
expandirão os jars lançados no Maven Central.

Se precisar de ajuda, entre em contato conosco.

### Considerações sobre datagrama (DHT)

Se seu aplicativo estiver usando datagramas I2P, por exemplo, para um
DHT, há muitas opções avançadas disponíveis para reduzir a sobrecarga e
aumentar a confiabilidade. Isso pode levar algum tempo e experimentação
para funcionar bem. Esteja ciente das compensações de
tamanho/confiabilidade. Fale conosco para obter ajuda. É possível - e
recomendado - usar datagramas e streaming no mesmo destino. Não crie
destinos separados para isso. Não tente armazenar seus dados não
relacionados nos DHTs de rede existentes (iMule, bote, bittorrent e
roteador). Crie o seu próprio. Se você estiver codificando nós de
semente, recomendamos que tenha vários.

### Outproxies

I2P outproxies to the clearnet are a limited resource. Use outproxies
only for normal user-initiated web browsing or other limited traffic.
For any other usage, consult with and get approval from the outproxy
operator.

### Co-marketing

Vamos trabalhar juntos. Não espere até que esteja pronto. Dê-nos seu
identificador do Twitter e comece a tuitar sobre isso, nós retribuiremos
o favor.

### Malware

Por favor, não use o I2P para o mal. Isso pode causar grandes danos à
nossa rede e à nossa reputação.

### Junte-se a nós

Isso pode ser óbvio, mas junte-se à comunidade. Execute o I2P 24/7.
Inicie um site I2P sobre seu projeto. Participe do IRC #i2p-dev. Poste
nos fóruns. Espalhe a palavra. Podemos ajudar você a obter usuários,
testadores, tradutores ou até mesmo codificadores.

## Examples

### Exemplos de aplicação

Talvez você queira instalar e brincar com o aplicativo I2P para Android
e observar seu código, para ver um exemplo de um aplicativo que agrupa o
roteador. Veja o que expomos ao usuário e o que ocultamos. Observe a
máquina de estado que usamos para iniciar e parar o roteador. Outros
exemplos são: Vuze, o aplicativo Nightweb para Android, iMule, TAILS,
iCloak e Monero.

### Exemplo de Código

Note: This section refers to Java I2P only.

Nenhum dos itens acima realmente informa como escrever seu código para
agrupar o roteador Java, então a seguir está um breve exemplo.

 import java.util.Properties;
 import net.i2p.router.Router;

 Properties p = new Properties();
 // add your configuration settings, directories, etc.
 // where to find the I2P installation files
 p.addProperty("i2p.dir.base", baseDir);
 // where to find the I2P data files
 p.addProperty("i2p.dir.config", configDir);
 // bandwidth limits in K bytes per second
 p.addProperty("i2np.inboundKBytesPerSecond", "50");
 p.addProperty("i2np.outboundKBytesPerSecond", "50");
 p.addProperty("router.sharePercentage", "80");
 p.addProperty("foo", "bar");
 Router r = new Router(p);
 // don't call exit() when the router stops
 r.setKillVMOnEnd(false);
 r.runRouter();

 ...

 r.shutdownGracefully();
 // will shutdown in 11 minutes or less

Este código é para o caso em que seu aplicativo inicia o roteador, como
em nosso aplicativo Android. Você também pode fazer com que o roteador
inicie o aplicativo por meio dos arquivos clients.config e
i2ptunnel.config, junto com os webapps Jetty, como é feito em nossos
pacotes Java. Como sempre, o gerenciamento de estado é a parte difícil.

See also: [the Router
javadocs](http:///net/i2p/router/Router.html).


