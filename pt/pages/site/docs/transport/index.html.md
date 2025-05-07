 Visão geral do
transporte Junho de 2018 0.9.36 

## Transportes na I2P

Um \"transporte\" no I2P é um método para comunicação direta ponto a
ponto entre dois roteadores. Os transportes devem fornecer
confidencialidade e integridade contra adversários externos enquanto
autenticam que o roteador contatado é aquele que deve receber uma
determinada mensagem.

O I2P suporta múltiplos transportes simultaneamente. Existem três
transportes implementados atualmente:

Cada um fornece um paradigma de \"conexão\", com autenticação, controle
de fluxo , confirmações e retransmissão.

## Serviços de Transporte

O subsistema de transporte no I2P fornece os seguintes serviços:

- Reliable delivery of [I2NP]() messages.
 Transports support I2NP message delivery ONLY. They are not
 general-purpose data pipes.
- A entrega de mensagens em ordem NÃO é garantida por todos os
 transportes.
- Mantenha um conjunto de endereços de roteador, um ou mais para cada
 transporte, que o roteador publica como suas informações de contato
 globais (o RouterInfo). Cada transporte pode se conectar usando um
 desses endereços, que pode ser IPv4 ou (a partir da versão 0.9.8)
 IPv6.
- Seleção do melhor transporte para cada mensagem de saída
- Enfileiramento de mensagens de saída por prioridade
- Limitação de largura de banda, tanto de saída quanto de entrada, de
 acordo com a configuração do roteador
- Configuração e desmontagem de conexões de transporte
- Criptografia de comunicações ponto a ponto
- Manutenção dos limites de conexão para cada transporte,
 implementação de vários limites para esses limites, e comunicação do
 status do limite ao roteador para que ele possa fazer alterações
 operacionais com base no status
- Abertura de porta de firewall usando UPnP (Universal Plug and Play)
- Travessia cooperativa de NAT/Firewall
- Detecção de IP local por vários métodos, incluindo UPnP, inspeção de
 conexões de entrada e enumeração de dispositivos de rede
- Coordenação do status do firewall e IP local, e alterações em ambos,
 entre os transportes
- Comunicação do status do firewall e do IP local, e alterações em
 ambos, no roteador e na interface do usuário
- Determinação de um relógio de consenso, que é usado para atualizar
 periodicamente o relógio do roteador, como um backup para NTP
- Manutenção do status de cada par, incluindo se ele está conectado,
 se foi conectado recentemente, e se ele foi alcançável na última
 tentativa
- Qualificação de endereços IP válidos de acordo com um conjunto de
 regras locais
- Honrando as listas automatizadas e manuais de pares banidos mantidas
 pelo roteador, e recusando conexões de saída e entrada para esses
 pares

## Endereços de Transporte

O subsistema de transporte mantém um conjunto de endereços de roteador,
cada um dos quais lista um método de transporte, IP e porta. Esses
endereços constituem os pontos de contato anunciados e são publicados
pelo roteador no banco de dados da rede. Os endereços também podem
conter um conjunto arbitrário de opções adicionais.

Cada método de transporte pode publicar vários endereços de roteador.

Os cenários típicos são:

- Um roteador não tem endereços publicados, então ele é considerado
 \"oculto\" e não pode receber conexões de entrada
- A router is firewalled, and therefore publishes an SSU address which
 contains a list of cooperating peers or \"introducers\" who will
 assist in NAT traversal (see [the SSU spec]()
 for details)
- Um roteador não tem firewall ou suas portas NAT estão abertas; ele
 publica endereços NTCP e SSU contendo IPs e portas diretamente
 acessíveis.

## Seleção de Transporte

The transport system delivers [I2NP messages]()
only. The transport selected for any message is independent of the
upper-layer protocols and contents (router or client messages, whether
an external application was using TCP or UDP to connect to I2P, whether
the upper layer was using [the streaming
library]() streaming or
[datagrams](), datagrams etc.).

Para cada mensagem de saída, o sistema de transporte solicita \"lances\"
de cada transporte. O transporte que oferece o menor (melhor) valor
vence o lance e recebe a mensagem para entrega. Um transporte pode se
recusar a oferecer lances.

Se um transporte faz uma oferta e com qual valor, depende de vários
fatores:

- Configuração de preferências de transporte
- Se o transporte já está conectado ao peer
- O número de conexões atuais em comparação com vários limites de
 conexão
- Se as tentativas recentes de conexão com o peer falharam
- O tamanho da mensagem, pois diferentes transportes têm limites de
 tamanho diferentes
- Se o par pode aceitar conexões de entrada para esse transporte,
 conforme anunciado em seu RouterInfo
- Se a conexão seria indireta (exigindo apresentadores) ou direta
- A preferência de transporte do peer, conforme anunciado em seu
 RouterInfo

Em geral, os valores de lance são selecionados para que dois roteadores
sejam conectados apenas por um único transporte a qualquer momento. No
entanto, isso não é um requisito.

## Novos Transportes e Trabalho Futuro

Transportes adicionais podem ser desenvolvidos, incluindo:

- Um transporte semelhante ao TLS/SSH
- Um transporte \"indireto\" para roteadores que não podem ser
 alcançados por todos os outros roteadores (uma forma de \"rotas
 restritas\")
- Transportes plugáveis compatíveis com Tor

O trabalho continua no ajuste dos limites de conexão padrão para cada
transporte. O I2P é projetado como uma \"rede mesh\", onde se presume
que qualquer roteador pode se conectar a qualquer outro roteador. Essa
suposição pode ser quebrada por roteadores que excederam seus limites de
conexão e por roteadores que estão atrás de firewalls de estado
restritivo (rotas restritas).

Os limites de conexão atuais são maiores para SSU do que para NTCP, com
base na suposição de que os requisitos de memória para uma conexão NTCP
são maiores do que para SSU. No entanto, como os buffers NTCP estão
parcialmente no kernel e os buffers SSU estão no heap Java, essa
suposição é difícil de verificar.

Analyze [Breaking and Improving Protocol
Obfuscation]() and see how transport-layer padding
may improve things.


