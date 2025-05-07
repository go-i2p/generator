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

## Visão geral

`KEYS` = par de chaves pública+privada, que são BASE64

`KEY` = chave pública, também BASE64

`ERRO` como está implícito retorna a mensagem `"ERRO "+DESCRIÇÃO+"\n"`,
onde `DESCRIÇÃO` é o que deu errado.

`OK` retorna `"OK"`e, se os dados devem ser retornados, eles estão na
mesma linha. `OK` significa que o comando foi concluído.

`DATA` linhas contêm informações que você solicitou. Pode haver várias
`DATA` linhas por solicitação.

**NOTA:** O comando help é o ÚNICO comando que tem uma exceção às
regras\... ele pode realmente não retornar nada! Isso é intencional, já
que help é um comando HUMANO e não de APLICATIVO.

## Conexão e Versão

Todas as saídas de status do BOB são por linhas. As linhas podem ser
terminadas em \\n ou \\r\\n , dependendo do sistema. Na conexão, o BOB
emite duas linhas:

 BOB version OK 

A versão atual é: 00.00.10

Observe que versões anteriores usavam dígitos hexadecimais maiúsculos e
não estavam em conformidade com os padrões de controle de versão I2P. É
recomendado que versões subsequentes usem apenas dígitos de 0 a 9.
00.00.10

Histórico de versões

 Versão Versão do roteador I2P Modificações
 --------------------- ------------------------ ----------------------------
 00.00.10 0.9.8 versão atual
 00.00.00 - 00.00.0F   versões de desenvolvimento

## Comandos

**ATENÇÃO:** Para detalhes ATUAIS sobre os comandos, USE o comando help
integrado. Basta fazer telnet para o localhost 2827 e digitar help, e
você poderá obter a documentação completa sobre cada comando.

Os comandos nunca ficam obsoletos ou alterados, porém novos comandos são
adicionados de tempos em tempos.

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

Uma vez configurados, todos os soquetes TCP podem e irão bloquear
conforme necessário, e não há necessidade de nenhuma mensagem adicional
de/para o canal de comando. Isso permite que o roteador controle o fluxo
sem explodir com OOM como o SAM faz, pois ele engasga ao tentar empurrar
muitos fluxos para dentro ou para fora de um soquete \-- que não pode
ser dimensionado quando você tem muitas conexões!

O que também é legal sobre essa interface em particular é que escrever
qualquer coisa para a interface para ela é muito mais fácil do que SAM.
Não há nenhum outro processamento a ser feito após a configuração. Sua
configuração é tão simples que ferramentas muito simples, como nc
(netcat) podem ser usadas para apontar para algum aplicativo. O valor aí
é que alguém poderia agendar tempos de atividade e inatividade para um
aplicativo, e não ter que alterar o aplicativo para fazer isso, ou mesmo
ter para parar esse aplicativo. Em vez disso, você pode literalmente
\"desconectar\" o destino e \"conectá-lo\" novamente. Contanto que os
mesmos endereços IP/porta e chaves de destino sejam usados ao ativar a
ponte, o aplicativo TCP normal não se importará e não notará. Ele
simplesmente será enganado \-- os destinos não são alcançáveis e nada
está chegando.

## Exemplos

Para o exemplo a seguir, configuraremos uma conexão de loopback local
muito simples, com dois destinos. O destino \"mouth\" será o serviço
CHARGEN do daemon do superservidor INET. O destino \"ear\" será uma
porta local na qual você pode fazer telnet e assistir ao belo teste
ASCII vomitar.

 EXEMPLO DE DIÁLOGO DE SESSÃO \-- telnet
simples 127.0.0.1 2827 funciona A = Application C = Resposta do comando
do BOB. FROM TO DIALOGUE C A BOB 00.00.10 C A OK A C setnick mouth C A
OK Nickname set to mouth A C newkeys C A OK
ZMPz1zinTdy3\~zGD\~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr\~0g2-l0vM7Y8nSqtFrSdMw\~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU\~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq\~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw\~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA


**ANOTE A CHAVE DE DESTINO ACIMA, O SEU SERÁ DIFERENTE!**

 FROM TO DIALOGUE A C outhost 127.0.0.1 C A
OK outhost set A C outport 19 C A OK outbound port set A C start C A OK
tunnel starting 

Neste ponto, não houve erro, um destino com um apelido de \"boca\" é
configurado. Quando você contata o destino fornecido, você realmente
conecta ao serviço `CHARGEN` em `19/TCP`.

Agora, a outra metade, para que possamos realmente entrar em contato com
esse destino.

 FROM TO DIALOGUE C A BOB 00.00.10 C A OK A
C setnick ear C A OK Nickname set to ear A C newkeys C A OK
8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg\~3eXtL-7S-qU-wdP-6VF\~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J\~flAvF4wrbF-LfVpMdg\~tjtns6fA\~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f\~dzoRCapAGDDTTnvjXuLrZ-vN-orT\~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A C inhost 127.0.0.1 C A OK inhost set A C inport 37337 C A OK inbound
port set A C start C A OK tunnel starting A C quit C A OK Bye! 

Agora, tudo o que precisamos fazer é fazer telnet para 127.0.0.1, porta
37337, enviar a chave de destino ou o endereço do host do catálogo de
endereços que queremos contatar. Neste caso, queremos contatar
\"mouth\", tudo o que fazemos é colar a chave e pronto.

**NOTA:** O comando \"quit\" no canal de comando NÃO desconecta os
túneis como o SAM.

 \$ telnet 127.0.0.1 37337 Trying
127.0.0.1\... Connected to 127.0.0.1. Escape character is \'\^\]\'.
ZMPz1zinTdy3\~zGD\~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr\~0g2-l0vM7Y8nSqtFrSdMw\~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU\~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq\~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw\~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefg
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefgh
\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghi
#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghij
\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghijk
\... 

Depois de algumas milhas virtuais desse vômito, pressione `Control-]`

 \... cdefghijklmnopqrstuvwxyz{\|}\~
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{\|}\~
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{\|}\~ !\"#\$%&\'()\*+,-./0123456789:;\<= telnet\>
c Connection closed. 

Eis aqui o que acontece\...

 telnet -\> ear -\> i2p -\> mouth -\>
chargen -. telnet \<- ear \<- i2p \<- mouth \<\-\-\-\-\-\-\-\-\-\--\' 

Você também pode se conectar aos SITES I2P!

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

Muito legal, não é? Tente outros SITES I2P bem conhecidos, se quiser,
inexistentes, etc, para ter uma ideia de que tipo de saída esperar em
diferentes situações. Na maioria das vezes, é sugerido que você ignore
qualquer uma das mensagens de erro. Elas não teriam sentido para o
aplicativo e são apresentadas apenas para depuração humana.

Vamos anotar nossos destinos agora que já terminamos de conhecê-los.

Primeiro, vamos ver quais apelidos de destino temos.

 FROM TO DIALOGUE A C list C A DATA
NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true
QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST:
127.0.0.1 C A DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING:
false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT:
not_set OUTHOST: localhost C A OK Listing done 

Certo, aqui estão eles. Primeiro, vamos remover \"boca\".

 FROM TO DIALOGUE A C getnick mouth C A OK
Nickname set to mouth A C stop C A OK tunnel stopping A C clear C A OK
cleared 

Agora, para remover \"orelha\", observe que isso é o que acontece quando
você digita muito rápido, e mostra como são as mensagens de ERRO
típicas.

 FROM TO DIALOGUE A C getnick ear C A OK
Nickname set to ear A C stop C A OK tunnel stopping A C clear C A ERROR
tunnel is active A C clear C A OK cleared A C quit C A OK Bye! 

Não vou me incomodar em mostrar um exemplo da extremidade do receptor de
uma ponte porque é muito simples. Há duas configurações possíveis para
ela, e ela é alternada com o comando \"quiet\".

O padrão NÃO é quiet, e os primeiros dados a entrarem no seu soquete de
escuta são o destino que está fazendo o contato. É uma linha única
consistindo do endereço BASE64 seguido por uma nova linha. Tudo depois
disso é para o aplicativo realmente consumir.

No modo silencioso, pense nisso como uma conexão de Internet regular.
Nenhum dado extra entra. É como se você estivesse conectado à Internet
regular. Este modo permite uma forma de transparência muito parecida com
a disponível nas páginas de configurações do túnel do console do
roteador, para que você possa usar o BOB para apontar um destino para um
servidor web, por exemplo, e você não teria que modificar o servidor web
de forma alguma.

A vantagem de usar BOB para isso é como discutido anteriormente. Você
pode agendar tempos de atividade aleatórios para o aplicativo,
redirecionar para uma máquina diferente, etc. Um uso disso pode ser algo
como querer tentar estragar a adivinhação de atividade do roteador para
o destino. Você pode parar e iniciar o destino com um processo
totalmente diferente para criar tempos de atividade e inatividade
aleatórios em serviços. Dessa forma, você estaria apenas interrompendo a
capacidade de contatar tal serviço, e não teria que se preocupar em
desligá-lo e reiniciá-lo. Você pode redirecionar e apontar para uma
máquina diferente na sua LAN enquanto faz atualizações, ou apontar para
um conjunto de máquinas de backup dependendo do que está em execução,
etc., etc. Somente sua imaginação limita o que você pode fazer com o
BOB.


