 Determinação de
perfis e seleção de pares 2024-02 0.9.62 

## NOTE

This page describes the Java I2P implementation of peer profiling and
selection as of 2010. While still broadly accurate, some details may no
longer be correct. We continue to evolve banning, blocking, and
selection strategies to address newer threats, attacks, and network
conditions. The current network has multiple router implementations with
various versions. Other I2P implementations may have completely
different profiling and selection strategies, or may not use profiling
at all.

## Visão geral

### Criação de perfil de pares

**Peer profiling** is the process of collecting data based on the
**observed** performance of other routers or peers, and classifying
those peers into groups. Profiling does **not** use any claimed
performance data published by the peer itself in the [network
database]().

Os perfis são usados para duas finalidades:

1. Selecionando pares para retransmitir nosso tráfego, o que é
 discutido abaixo
2. Choosing peers from the set of floodfill routers to use for network
 database storage and queries, which is discussed on the [network
 database]() page

### Seleção de Pares

**Seleção de pares** é o processo de escolher quais roteadores na rede
queremos retransmitir nossas mensagens para passar (quais pares iremos
pedir para se juntarem aos nossos túneis). Para fazer isso, nós
monitoramos como cada par se desempenha (o \"perfil\" do par) e usamos
esses dados para estimar quão rápidos eles são, com que frequência eles
serão capazes de aceitar nossas solicitações e se eles parecem estar
sobrecarregados ou de outra forma incapazes de executar o que eles
concordam de forma confiável.

Unlike some other anonymous networks, in I2P, claimed bandwidth is
untrusted and is **only** used to avoid those peers advertising very low
bandwidth insufficient for routing tunnels. All peer selection is done
through profiling. This prevents simple attacks based on peers claiming
high bandwidth in order to capture large numbers of tunnels. It also
makes [timing attacks](#timing) more
difficult.

A seleção de pares é feita com bastante frequência, pois um roteador
pode manter um grande número de túneis de cliente e exploratórios, e a
vida útil de um túnel é de apenas 10 minutos.

### Mais informações

For more information see the paper [Peer Profiling and Selection in the
I2P Anonymous Network]() presented at [PET-CON
2009.1](). See [below](#notes) for notes on minor
changes since the paper was published.

## Perfis

Each peer has a set of data points collected about them, including
statistics about how long it takes for them to reply to a network
database query, how often their tunnels fail, and how many new peers
they are able to introduce us to, as well as simple data points such as
when we last heard from them or when the last communication error
occurred. The specific data points gathered can be found in the
[code]().

Os perfis são bem pequenos, alguns KB. Para controlar o uso da memória,
o tempo de expiração do perfil diminui conforme o número de perfis
cresce. Os perfis são mantidos na memória até o desligamento do
roteador, quando são gravados no disco. Na inicialização, os perfis são
lidos para que o roteador não precise reinicializar todos os perfis,
permitindo assim que um roteador se reintegre rapidamente à rede após a
inicialização.

## Resumos de pares

Embora os perfis em si possam ser considerados um resumo do desempenho
de um peer , para permitir uma seleção eficaz de peers, dividimos cada
resumo em quatro valores simples, representando a velocidade do peer,
sua capacidade, quão bem integrado ele está na rede e se ele está
falhando.

### Velocidade

O cálculo de velocidade simplesmente percorre o perfil e estima quantos
dados podemos enviar ou receber em um único túnel através do peer em um
minuto. Para esta estimativa, ele apenas olha para o desempenho de no
minuto anterior.

### Capacidade {#capacity}

O cálculo de capacidade simplesmente percorre o perfil e estima quantos
túneis o peer concordaria em participar em um determinado período de
tempo. Para essa estimativa, ele analisa quantas solicitações de
construção de túnel o peer aceitou, rejeitou e descartou, e quantos dos
túneis acordados falharam posteriormente. Embora o cálculo seja
ponderado pelo tempo para que a atividade recente conte mais do que a
atividade posterior, estatísticas de até 48 horas podem ser incluídas.

Reconhecer e evitar pares não confiáveis e inacessíveis é extremamente
importante. Infelizmente, como a construção e o teste do túnel exigem a
participação de vários pares, é difícil identificar positivamente a
causa de uma solicitação de construção descartada ou falha de teste. O
roteador atribui uma probabilidade de falha a cada um dos pares e usa
essa probabilidade no cálculo de capacidade. Descartas e falhas de teste
são ponderadas muito mais do que rejeições.

## Organização de pares

Conforme mencionado acima, analisamos o perfil de cada peer para chegar
a alguns cálculos importantes e, com base neles, organizamos cada peer
em três grupos - rápido, alta capacidade e padrão.

Os agrupamentos não são mutuamente exclusivos nem são independentes:

- Um par é considerado de \"alta capacidade\" se seu cálculo de
 capacidade atende ou excede a mediana de todos os pares.
- Um peer é considerado \"rápido\" se já tiver \"alta capacidade\" e
 seu cálculo de velocidade atender ou exceder a mediana de todos os
 peers.
- Um par é considerado \"padrão\" se não for de \"alta capacidade\"

These groupings are implemented in the router\'s
[ProfileOrganizer]().

### Limites de tamanho do grupo

O tamanho dos grupos pode ser limitado.

- O grupo rápido é limitado a 30 pares. Se houver mais, apenas aqueles
 com a maior classificação de velocidade serão colocados no grupo.
- O grupo de alta capacidade é limitado a 75 pares (incluindo o grupo
 rápido) Se houver mais, apenas aqueles com a maior classificação de
 capacidade serão colocados no grupo.
- O grupo padrão não tem limite fixo, mas é um pouco menor que o
 número de RouterInfos armazenados no banco de dados da rede local.
 Em um roteador ativo na rede atual, pode haver cerca de 1000
 RouterInfos e 500 perfis de pares (incluindo aqueles nos grupos de
 alta e rápida capacidade)

## Recálculo e Estabilidade

Os resumos são recalculados e os pares são reunidos em grupos a cada 45
segundos.

Os grupos tendem a ser bastante estáveis, ou seja, não há muita
\"rotatividade\" nas classificações a cada recálculo. Pares nos grupos
rápido e de alta capacidade obtêm mais túneis construídos através deles,
o que aumenta suas classificações de velocidade e capacidade, o que
reforça sua presença no grupo.

## Seleção de Pares

O roteador seleciona pares dos grupos acima para construir túneis.

### Seleção de pares para túneis de clientes

Os túneis de cliente são usados para tráfego de aplicativos, como
proxies HTTP e servidores web.

Para reduzir a suscetibilidade a [alguns
ataques](http://blog.torproject.org/blog/one-cell-enough), e aumentar o
desempenho, pares para construir túneis de cliente são escolhidos
aleatoriamente do menor grupo, que é o grupo \"rápido\". Não há
preconceito em selecionar pares que já foram participantes de um túnel
para o mesmo cliente.

### Seleção de pares para túneis exploratórios

Túneis exploratórios são usados para fins administrativos do roteador,
como tráfego de banco de dados de rede e testes de túneis de cliente.
Túneis exploratórios também são usados para contatar roteadores
anteriormente desconectados, e é por isso que eles são chamados de
\"exploratórios\". Esses túneis geralmente são de baixa largura de
banda.

Os pares para construção de túneis exploratórios geralmente são
escolhidos aleatoriamente do grupo padrão. Se a taxa de sucesso dessas
tentativas de construção for baixa em comparação com a taxa de sucesso
de construção do túnel do cliente, o roteador selecionará uma média
ponderada de pares aleatoriamente do grupo de alta capacidade. Isso
ajuda a manter uma taxa de sucesso de construção satisfatória mesmo
quando o desempenho da rede é ruim. Não há preconceito em relação à
seleção de pares que foram participantes anteriores de um túnel
exploratório.

Como o grupo padrão inclui um subconjunto muito grande de todos os pares
que o roteador conhece, túneis exploratórios são essencialmente
construídos por meio de uma seleção aleatória de todos os pares, até que
a taxa de sucesso da construção se torne muito baixa.

### Restrições

Para evitar alguns ataques simples, e por questão de desempenho, há as
seguintes restrições:

- Dois pares do mesmo espaço IP /16 não podem estar no mesmo túnel.
- Um peer pode participar de no máximo 33% de todos os túneis criados
 pelo roteador.
- Pares com largura de banda extremamente baixa não são utilizados.
- Os pares para os quais uma tentativa de conexão recente falhou não
 são usados.

### Ordenação de pares em túneis

Peers are ordered within tunnels to to deal with the [predecessor
attack]() [(2008
update)](). More information is on the [tunnel
page](#ordering).

## Trabalho futuro

- Continue analisando os cálculos de velocidade e capacidade de ajuste
 conforme necessário
- Implemente uma estratégia de ejeção mais agressiva, se necessário,
 para controlar o uso da memória à medida que a rede cresce
- Avalie os limites de tamanho do grupo
- Usar dados de GeoIP para incluir ou excluir determinados pares,
 quando configurado

## Notas {#notes}

For those reading the paper [Peer Profiling and Selection in the I2P
Anonymous Network](), please keep in mind the
following minor changes in I2P since the paper\'s publication:

- O cálculo de integração ainda não é utilizado
- No artigo, "grupos" são chamados de "camadas"
- O nível \"Falha\" não é mais usado
- O nível \"Não falhando\" agora é chamado de \"Padrão\"

## Referências

- [Determinação de perfis e seleção de pares na Rede anônima
 I2P](pdf/I2P-PET-CON-2009.1.pdf)
- [Uma célula é o
 suficiente](http://blog.torproject.org/blog/one-cell-enough)
- [Guardas de entrada do
 Tor](https://wiki.torproject.org/noreply/TheOnionRouter/TorFAQ#EntryGuards)
- [Artigo de Murdoch
 2007](http://freehaven.net/anonbib/#murdoch-pet2007)
- [Ajuste para
 Tor](http://www.crhc.uiuc.edu/~nikita/papers/tuneup-cr.pdf)
- [Ataques de roteamento de poucos recursos contra
 Tor](http://cs.gmu.edu/~mccoy/papers/wpes25-bauer.pdf)


