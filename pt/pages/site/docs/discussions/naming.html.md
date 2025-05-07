 Discussão sobre
nomenclatura 

NOTE: The following is a discussion of the reasons behind the I2P naming
system, common arguments and possible alternatives. See [the naming
page]() for current documentation.

## Alternativas descartadas

A nomeação dentro do I2P tem sido um tópico frequentemente debatido
desde o início, comdefensores em todo o espectro de possibilidades. No
entanto, dada a demanda inerenteda I2P por comunicação segura e operação
descentralizada, o sistema de nomenclatura tradicional no estilo DNS
está claramente fora, assim como os sistemas devotação de \"regras da
maioria\".

No entanto, a I2P não promove o uso de serviços semelhantes ao DNS, pois
os danos causadospelo sequestro de um site podem ser tremendos - e
destinos inseguros nãotêm valor. O próprio DNSsec ainda recai sobre
registradores e autoridades de certificação, enquanto com o I2P, as
solicitações enviadas para um destino não podem ser interceptadas ou a
respostafalsificada, pois são criptografadas para as chaves públicas do
destino, e um destinoem si é apenas um par de chaves públicas e um
certificado. Os sistemas no estilo DNS, por outro lado,permitem que
qualquer um dos servidores de nomes no caminhode pesquisa monte ataques
simples de negação de serviço e falsificação. Adicionar um certificado
autenticando asrespostas como assinadas por alguma autoridade de
certificação centralizada resolveria muitos dos problemas hostis do
servidor de nomes, mas deixaria em aberto ataques de repetição, bem como
ataques hostis de autoridade decertificação.

A nomeação de estilo de votação também é perigosa, especialmente dada a
eficácia de ataques Sybil em sistemas anônimos - o invasor pode
simplesmente criar um número arbitrariamente alto de pares e \"votar\"
com cada um para assumir um determinado nome. Métodos de prova de
trabalho podem ser usados para tornar a identidade não livre, mas
conforme a rede cresce, a carga necessária para contatar todos para
conduzir a votação online é implausível, ou se a rede completa não for
consultada, diferentes conjuntos de respostas podem ser alcançáveis.

Assim como na Internet, no entanto, o I2P está mantendo o design e a
operação de um sistema de nomenclatura fora da camada de comunicação
(semelhante ao IP). A biblioteca de nomenclatura empacotada inclui uma
interface simples de provedor de serviços que [sistemas de nomenclatura
alternativos](#alternatives) podem conectar, permitindo que os usuários
finais conduzam que tipo de trocas de nomenclatura eles preferem.

## Discussion

Veja também [Nomes: Descentralizado, Seguro, Significativo para o ser
humano: Escolha dois](https://zooko.com/distnames.html).

### Comments by jrandom

(adaptado de uma postagem no antigo Syndie, 26 de novembro de 2005)

P: O que fazer se alguns hosts não concordarem com um endereço e se
alguns endereços estiverem funcionando, outros não? Quem é a fonte
correta de um nome?

R: Você não. Esta é, na verdade, uma diferença crítica entre nomes no
I2P e como DNS funciona - nomes no I2P são legíveis por humanos,
seguros, mas **não são globalmente únicos**. Isto é por design e uma
parte inerente da nossa necessidade de segurança.

Se eu pudesse de alguma forma convencê-lo a mudar o destino associado a
algum nome , eu \"assumiria\" o site com sucesso, e sob nenhuma
circunstância isso é aceitável. Em vez disso, o que fazemos é tornar os
nomes **localmente únicos**: eles são o que *você* usa para chamar um
site, assim como você pode chamar as coisas do que quiser quando as
adiciona aos favoritos do seu navegador ou à lista de amigos do seu
cliente de MI . Quem você chama de \"Chefe\" pode ser quem outra pessoa
chama de \"Sally\".

Os nomes nunca serão legíveis por humanos de forma segura e globalmente
únicos.

### Comments by zzz

O texto a seguir, do zzz, é uma análise de várias reclamações comuns
sobre o sistema de nomenclatura do I2P.

- **Ineficiência:** Todo o hosts.txt é baixado (se tiver sido
 alterado, já que o eepget usa o etag e os cabeçalhos da última
 modificação). São cerca de 400K agora para quase 800 hosts.

 Verdade, mas isso não é muito tráfego no contexto do i2p, que é
 extremamente ineficiente (bancos de dados de inundação, enorme
 sobrecarga de criptografia e preenchimento, roteamento garlic,
 etc.). Se você baixasse um arquivo hosts.txt de alguém a cada 12
 horas, a média seria de cerca de 10 bytes/seg.

 Como geralmente é o caso no i2p, há uma compensação fundamental aqui
 entre anonimato e eficiência. Alguns diriam que usar os cabeçalhos
 etag e last-modified é perigoso porque expõe quando você solicitou
 os dados pela última vez. Outros sugeriram solicitar apenas chaves
 específicas (semelhante ao que os serviços de salto fazem, mas de
 uma forma mais automatizada), possivelmente com um custo adicional
 em anonimato.

 Possible improvements would be a replacement or supplement to
 address book (see [p](http:///)), or something simple like
 subscribing to http://example.i2p/cgi-bin/recenthosts.cgi rather
 than http://example.i2p/hosts.txt. If a hypothetical recenthosts.cgi
 distributed all hosts from the last 24 hours, for example, that
 could be both more efficient and more anonymous than the current
 hosts.txt with last-modified and etag.

 A sample implementation is on stats.i2p at [](). This script returns an Etag with a
 timestamp. When a request comes in with the If-None-Match etag, the
 script ONLY returns new hosts since that timestamp, or 304 Not
 Modified if there are none. In this way, the script efficiently
 returns only the hosts the subscriber does not know about, in an
 address book-compatible manner.

 Portanto, a ineficiência não é um grande problema e há várias
 maneiras de melhorar as coisas sem mudanças radicais.

- **Não escalável:** O arquivo hosts.txt de 400K (com pesquisa linear)
 não é tão grande no momento e provavelmente podemos aumentar em 10x
 ou 100x antes que se torne um problema.

 Quanto ao tráfego de rede, veja acima. Mas, a menos que você vá
 fazer uma consulta lenta em tempo real pela rede para uma chave,
 você precisa ter todo o conjunto de chaves armazenado localmente, a
 um custo de cerca de 500 bytes por chave.

- **Requer configuração e \"confiança\":** O catálogo de endereços
 pronto para uso é assinado apenas em http://www.i2p2.i2p/hosts.txt,
 que raramente é atualizado, levando a uma experiência ruim para
 novos usuários.

 Isso é muito intencional. jrandom quer que um usuário \"confie\" em
 um provedor hosts.txt e, como ele gosta de dizer, \"confiança não é
 um booleano\". A etapa de configuração tenta forçar os usuários a
 pensar sobre questões de confiança em uma rede anônima.

 Como outro exemplo, a página de erro \"I2P Site Unknown\" no proxy
 HTTP lista alguns serviços de salto, mas não \"recomenda\" nenhum em
 particular, e cabe ao usuário escolher um (ou não). jrandom diria
 que confiamos nos provedores listados o suficiente para listá-los,
 mas não o suficiente para buscar automaticamente a chave deles.

 Não tenho certeza do sucesso disso. Mas deve haver algum tipo de
 hierarquia de confiança para o sistema de nomenclatura. Tratar todos
 igualmente pode aumentar o risco de sequestro.

- **Não é DNS**

 Infelizmente, pesquisas em tempo real via i2p tornariam a navegação
 na web significativamente mais lenta.

 Além disso, o DNS é baseado em pesquisas com cache limitado e tempo
 de vida, enquanto as chaves i2p são permanentes.

 Claro, poderíamos fazer funcionar, mas por quê? Não é um bom ajuste.

- **Não confiável:** Depende de servidores específicos para
 assinaturas de catálogo de endereços.

 Sim, depende de alguns servidores que você configurou. Dentro do
 i2p, servidores e serviços vêm e vão. Qualquer outro sistema
 centralizado (por exemplo, servidores raiz DNS) teria o mesmo
 problema. Um sistema completamente descentralizado (todos são
 autoritativos) é possível implementando uma solução \"todos são
 servidores DNS raiz\" ou algo ainda mais simples, como um script que
 adiciona todos em seu hosts.txt ao seu catálogo de endereços.

 No entanto, as pessoas que defendem soluções totalmente
 autoritativas geralmente não pensaram nas questões de conflitos e
 sequestros.

- **Estranho, não em tempo real:** É uma colcha de retalhos de
 provedores hosts.txt, provedores de formulários web de adição de
 chaves, provedores de serviços de jump, repórteres de status de
 sites I2P. Servidores de jump e assinaturas são um problema,
 deveriam funcionar como DNS.

 Veja as seções de confiabilidade e confiança.

Então, em resumo, o sistema atual não está terrivelmente quebrado,
ineficiente ou não escalável, e as propostas de \"apenas usar DNS\" não
são bem pensadas.

## Alternativas {#alternatives}

A fonte I2P contém vários sistemas de nomenclatura plugáveis e suporta
opções de configuração para permitir a experimentação com sistemas de
nomenclatura.

- **Meta** - chama dois ou mais outros sistemas de nomenclatura em
 ordem. Por padrão, chama PetName e depois HostsTxt.

- **PetName** - Procura em um arquivo petnames.txt. O formato deste
 arquivo NÃO é o mesmo que hosts.txt.

- **HostsTxt** - Procura nos seguintes arquivos, em ordem:

- 1. privatehosts.txt
 2. userhosts.txt
 3. hosts.txt

- **AddressDB** - Cada host é listado em um arquivo separado em um
 diretório addressDb/.

- **Eepget** - faz uma solicitação de pesquisa HTTP de um servidor
 externo - deve ser empilhado após a pesquisa HostsTxt com Meta. Isso
 pode aumentar ou substituir o sistema de salto. Inclui cache na
 memória.

- **Exec** - chama um programa externo para pesquisa, permite
 experimentação adicional em esquemas de pesquisa, independente de
 Java. Pode ser usado após HostsTxt ou como o único sistema de
 nomenclatura. Inclui cache na memória.

- **Dummy** - usado como fallback para nomes Base64, caso contrário
 falha.

O sistema de nomenclatura atual pode ser alterado com a opção de
configuração avançada \'i2p.naming.impl\' (reinicialização necessária).
Consulte core/java/src/net/i2p/client/naming para obter detalhes.

Qualquer novo sistema deve ser empilhado com HostsTxt, ou deve
implementar o armazenamento local e/ou as funções de assinatura do
catálogo de endereços, já que o catálogo de endereços só conhece os
arquivos hosts.txt e o formato.

## Certificados {#certificates}

Destinos I2P contêm um certificado, no entanto, no momento em que o
certificado é sempre nulo. Com um certificado nulo, destinos base64 são
sempre 516 bytes terminando em \"AAAA\", e isso é verificado no
mecanismo de mesclagem do catálogo de endereços e possivelmente em
outros lugares. Além disso, não há método disponível para gerar um
certificado ou adicioná-lo a um destino . Portanto, eles terão que ser
atualizados para implementar certificados.

One possible use of certificates is for [proof of
work](#hashcash).

Outra é que \"subdomínios\" (entre aspas porque não existe tal coisa,
i2p usa um sistema de nomenclatura simples) sejam assinados pelas chaves
do domínio de 2º nível.

Com qualquer implementação de certificado deve vir o método para
verificar os certificados . Presumivelmente isso aconteceria no código
de mesclagem do catálogo de endereços. Existe um método para vários
tipos de certificados ou vários certificados?

Adicionar um certificado autenticando as respostas como assinadas por
alguma autoridade de certificação centralizada resolveria muitos dos
problemas de servidores de nomes hostis, mas deixaria ataques de
repetição abertos, bem como ataques de autoridades de certificação
hostis.


