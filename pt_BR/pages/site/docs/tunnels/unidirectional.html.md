 Túneis
unidirecionais Novembro de 2016 0.9.27 

## Visão geral

Esta página descreve as origens e o design dos túneis unidirecionais do
I2P. Para mais informações, consulte:

- [Página de visão geral do
 túnel]()
- [Especificação do
 Túnel]()
- [Especificação de criação de
 túnel]()
- [Discussão sobre o projeto do
 túnel]()
- [Seleção de
 pares]()
- [Encontro 125
 (\~13:12-13:30)]()

## Revisão

Embora não tenhamos conhecimento de nenhuma pesquisa publicada sobre as
vantagens dos túneis unidirecionais , eles parecem dificultar a detecção
de um padrão de solicitação/resposta, o que é bem possível de detectar
em um túnel bidirecional. Vários aplicativos e protocolos, notavelmente
HTTP, transferem dados dessa maneira. Ter o tráfego seguindo a mesma
rota para seu destino e de volta pode tornar mais fácil para um invasor
que tem apenas dados de tempo e volume de tráfego inferir o caminho que
um túnel está tomando. Ter a resposta retornando por um caminho
diferente, sem dúvida torna isso mais difícil.

Ao lidar com um adversário interno ou a maioria dos adversários
externos, os túneis unidirecionais do I2P expõem metade dos dados de
tráfego que seriam expostos com circuitos bidirecionais simplesmente
observando os fluxos em si - uma solicitação e resposta HTTP seguiriam o
mesmo caminho no Tor, enquanto no I2P os pacotes que compõem a
solicitação sairiam por um ou mais túneis de saída e os pacotes que
compõem a resposta retornariam por um ou mais túneis de entrada
diferentes.

A estratégia de usar dois túneis separados para comunicação de entrada e
saída não é a única técnica disponível, e tem implicações de anonimato .
No lado positivo, usar túneis separados diminui os dados de tráfego
expostos para análise aos participantes em um túnel - por exemplo, pares
em um túnel de saída de um navegador da web veriam apenas o tráfego de
um HTTP GET, enquanto os pares em um túnel de entrada veriam a carga
útil entregue ao longo do túnel. Com túneis bidirecionais, todos os
participantes teriam acesso ao fato de que, por exemplo, 1 KB foi
enviado em uma direção, então 100 KB na outra. No lado negativo, usar
túneis unidirecionais significa que há dois conjuntos de pares que
precisam ser perfilados e contabilizados, e cuidado adicional deve ser
tomado para lidar com a velocidade aumentada de ataques predecessores .
O processo de pooling e construção de túneis (estratégias de seleção e
ordenação de pares) deve minimizar as preocupações do ataque
predecessor.

## Anonimato

A recent [paper by Hermann and Grothoff]() declared
that I2P\'s unidirectional tunnels \"seems to be a bad design
decision\".

O ponto principal do artigo é que desanonimizações em túneis
unidirecionais levam mais tempo, o que é uma vantagem, mas que um
invasor pode ter mais certeza no caso unidirecional. Portanto, o artigo
afirma que não é uma vantagem, mas uma desvantagem, pelo menos com sites
I2P de longa duração.

Esta conclusão não é totalmente suportada pelo artigo. Túneis
unidirecionais claramente mitigam outros ataques e não está claro como
negociar o risco do ataque no artigo com ataques em uma arquitetura de
túnel bidirecional.

Esta conclusão é baseada em uma certeza arbitrária vs. ponderação de
tempo (tradeoff) que pode não ser aplicável em todos os casos. Por
exemplo, alguém poderia fazer uma lista de IPs possíveis e então emitir
intimações para cada. Ou o invasor poderia fazer DDoS em cada um deles e
por meio de um simples ataque de interseção ver se o Site I2P cai ou
fica mais lento. Então, fechar pode ser bom o suficiente, ou o tempo
pode ser mais importante.

A conclusão é baseada em uma ponderação específica da importância da
certeza vs. tempo, e essa ponderação pode estar errada, e é
definitivamente discutível, especialmente em um mundo real com
intimações, mandados de busca e outros métodos disponíveis para
confirmação final.

Uma análise completa das compensações de túneis unidirecionais vs.
bidirecionais está claramente fora do escopo do artigo e não foi feita
em nenhum outro lugar. Por exemplo, como esse ataque se compara aos
numerosos ataques de temporização possíveis publicados sobre redes
roteadas por onion? Claramente, os autores não fizeram essa análise, se
é que é possível fazê-la efetivamente.

Tor usa túneis bidirecionais e teve muita revisão acadêmica. I2P usa
túneis unidirecionais e teve muito pouca revisão. A falta de um artigo
de pesquisa defendendo túneis unidirecionais significa que é uma escolha
de design ruim ou apenas que precisa de mais estudo? Ataques de
temporização e ataques distribuídos são difíceis de se defender tanto no
I2P quanto no Tor. A intenção do design (veja as referências acima) era
que os túneis unidirecionais são mais resistentes a ataques de
temporização. No entanto, o artigo apresenta um tipo um pouco diferente
de ataque de temporização . Este ataque, inovador como é, é suficiente
para rotular a arquitetura de túnel do I2P (e, portanto, o I2P como um
todo) como um \"design ruim\" e, por implicação, claramente inferior ao
Tor, ou é apenas uma alternativa de design que claramente precisa de
mais investigação e análise? Existem várias outras razões para
considerar o I2P atualmente inferior ao Tor e outros projetos (tamanho
pequeno da rede , falta de financiamento, falta de revisão), mas os
túneis unidirecionais são realmente uma razão?

Em resumo, \"má decisão de projeto\" é aparentemente (já que o artigo
não rotula túneis bidirecionais como \"ruins\") uma abreviação para
\"túneis unidirecionais são inequivocamente inferiores aos túneis
bidirecionais\", mas esta conclusão não é apoiada pelo artigo.


