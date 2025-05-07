 I2PControl -
Remote Control Service 2022-01 0.9.52 

I2P enables a [JSONRPC2](http://en.wikipedia.org/wiki/JSON-RPC)
interface via the plugin [I2PControl](). The
aim of the interface is to provide simple way to interface with a
running I2P node. A client, itoopie, has been developed in parallel. The
JSONRPC2 implementation for the client as well as the plugin is provided
by the java libraries [JSON-RPC
2.0](http://software.dzhuvinov.com/json-rpc-2.0.html). A list of
implementations of JSON-RPC for various languages can be found at [the
JSON-RPC wiki](http://json-rpc.org/wiki/implementations).

O I2PControl está escutando por padrão em https://localhost:7650

## API, versão 1.

Os parâmetros são fornecidos apenas de forma nomeada (mapas).

#### formato JSON-RPC 2

Request: { \"id\": \"id\", \"method\":
\"Method-name\", \"params\": { \"Param-key-1\": \"param-value-1\",
\"Param-key-2\": \"param-value-2\", \"Token\": \"\*\*actual token\*\*\"
}, \"jsonrpc\": \"2.0\" } Response: { \"id\": \"id\", \"result\": { \"Result-key-1\":
\"result-value-1\", \"Result-key-2\": \"result-value-2\" }, \"jsonrpc\":
\"2.0\" } 

- - Param-key-1 -- Description
 - Param-key-2 -- Description
 - Token -- Token usado para autenticar cada solicitação (excluindo
 o método RPC \'Authenticate\')

- - Result-key-1 -- Description
 - Result-key-2 -- Description

#### Métodos implementados

- - API -- \[long\] A versão da API de I2PControl usada pelo
 cliente.
 - Password -- \[String\] A senha usada para autenticação no
 servidor remoto.

- - API -- \[long\] A versão primária da API de I2PControl
 implementada pelo servidor.
 - Token -- \[String\] O token usado para comunicação futura.

```{=html}
<!-- -->
```
- - Echo -- \[String\] Valor será retornado em resposta.
 - Token -- \[String\] Token usado para autenticar o cliente. É
 fornecido pelo servidor via método RPC \'Authenticate\'.

- - Result -- \[String\] Valor da chave \'echo\' na requisição.

```{=html}
<!-- -->
```
- - Stat -- \[String\] Determines which
 rateStat to fetch, see
 [ratestats]().
 - Period -- \[long\] Determina para qual período uma estatística é
 buscada. Medido em ms.
 - Token -- \[String\] Token usado para autenticar o cliente. É
 fornecido pelo servidor via método RPC \'Authenticate\'.

- - Result -- \[double\] Returns the average value for the requested
 rateStat and period.

```{=html}
<!-- -->
```
- - \*i2pcontrol.address -- \[String\] Define um novo endereço de
 escuta para I2PControl (somente 127.0.0.1 e 0.0.0.0 são
 implementados no I2PControl atualmente).
 - \*i2pcontrol.password -- \[String\] Define uma nova senha para
 I2PControl, todos os tokens de autenticação serão revogados.
 - \*i2pcontrol.port -- \[String\] Alterna em qual porta o
 I2PControl escutará as conexões.
 - Token -- \[String\] Token usado para autenticar o cliente. É
 fornecido pelo servidor via método RPC \'Authenticate\'.

- - \*\*i2pcontrol.address -- \[null\] Retornado se o endereço mudou
 - \*\*i2pcontrol.password -- \[null\] Retornado se as
 configurações mudaram
 - \*\*i2pcontrol.port -- \[null\] Retornado se as configurações
 mudaram
 - SettingsSaved -- \[Boolean\] Retorna verdadeiro se alguma
 alteração foi feita.
 - RestartNeeded -- \[Boolean\] Retorna verdadeiro se alguma
 alteração que exija uma reinicialização para entrar em vigor foi
 feita.

```{=html}
<!-- -->
```
- - \*i2p.router.status -- \[n/a\]
 - \*i2p.router.uptime -- \[n/a\]
 - \*i2p.router.version -- \[n/a\]
 - \*i2p.router.net.bw.inbound.1s -- \[n/a\]
 - \*i2p.router.net.bw.inbound.15s -- \[n/a\]
 - \*i2p.router.net.bw.outbound.1s -- \[n/a\]
 - \*i2p.router.net.bw.outbound.15s -- \[n/a\]
 - \*i2p.router.net.status -- \[n/a\]
 - \*i2p.router.net.tunnels.participating -- \[n/a\]
 - \*i2p.router.netdb.activepeers -- \[n/a\]
 - \*i2p.router.netdb.fastpeers -- \[n/a\]
 - \*i2p.router.netdb.highcapacitypeers -- \[n/a\]
 - \*i2p.router.netdb.isreseeding -- \[n/a\]
 - \*i2p.router.netdb.knownpeers -- \[n/a\]
 - Token -- \[String\] Token usado para autenticar o cliente. É
 fornecido pelo servidor via método RPC \'Authenticate\'.

- - \*\*i2p.router.status -- \[String\] Qual o status do roteador. A
 free-format, translated string intended for display to the user.
 May include information such as whether the router is accepting
 participating tunnels. Content is implementation-dependent.
 - \*\*i2p.router.uptime -- \[long\] Qual o tempo de operação do
 roteador em ms. Note: i2pd routers prior to version 2.41
 returned this value as a string. For compatibility, clients
 should handle both string and long.
 - \*\*i2p.router.version -- \[String\] Qual versão do I2P que o
 roteador está rodando.
 - \*\*i2p.router.net.bw.inbound.1s -- \[double\] A largura de
 banda de entrada média de 1 segundo em Bps.
 - \*\*i2p.router.net.bw.inbound.15s -- \[double\] A largura de
 banda de entrada média de 15 segundos em Bps.
 - \*\*i2p.router.net.bw.outbound.1s -- \[double\] A largura de
 banda média de saída de 1 segundo em Bps.
 - \*\*i2p.router.net.bw.outbound.15s -- \[double\] A largura de
 banda média de saída de 15 segundos em Bps.
 - \*\*i2p.router.net.status -- \[long\] Qual é o status atual da
 rede. De acordo com o enum abaixo:
 - 0 -- OK
 - 1 -- TESTING
 - 2 -- FIREWALLED
 - 3 -- HIDDEN
 - 4 -- WARN_FIREWALLED_AND_FAST
 - 5 -- WARN_FIREWALLED_AND_FLOODFILL
 - 6 -- WARN_FIREWALLED_WITH_INBOUND_TCP
 - 7 -- WARN_FIREWALLED_WITH_UDP_DISABLED
 - 8 -- ERROR_I2CP
 - 9 -- ERROR_CLOCK_SKEW
 - 10 -- ERROR_PRIVATE_TCP_ADDRESS
 - 11 -- ERROR_SYMMETRIC_NAT
 - 12 -- ERROR_UDP_PORT_IN_USE
 - 13 -- ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL
 - 14 -- ERROR_UDP_DISABLED_AND_TCP_UNSET
 - \*\*i2p.router.net.tunnels.participating -- \[long\] Em quantos
 túneis na rede I2P estamos participando?
 - \*\*i2p.router.netdb.activepeers -- \[long\] Com quantos colegas
 nos comunicamos recentemente?
 - \*\*i2p.router.netdb.fastpeers -- \[long\] Quantos pontos são
 considerados \'rápidos\'.
 - \*\*i2p.router.netdb.highcapacitypeers -- \[long\] Quantos
 pontos são considerados \'alta capacidade\'.
 - \*\*i2p.router.netdb.isreseeding -- \[boolean\] O roteador está
 repropagando hosts para seu NetDB?
 - \*\*i2p.router.netdb.knownpeers -- \[long\] Quantos pares são
 conhecidos por nós (listados em nosso NetDB).

```{=html}
<!-- -->
```
- - \*FindUpdates -- \[n/a\] **Bloqueio**. Inicia uma busca por
 atualizações assinadas.
 - \*Reseed -- \[n/a\] Inicia uma nova propagação do roteador,
 buscando pares em nosso NetDB a partir de um host remoto.
 - \*Restart -- \[n/a\] Reinicia o roteador.
 - \*RestartGraceful -- \[n/a\] Reinicia o roteador normalmente
 (aguarda a expiração dos túneis participantes).
 - \*Shutdown -- \[n/a\] Desliga o roteador.
 - \*ShutdownGraceful -- \[n/a\] Desliga o roteador normalmente
 (aguarda a expiração dos túneis participantes).
 - \*Update -- \[n/a\] Inicia uma atualização do roteador a partir
 de fontes assinadas.
 - Token -- \[String\] Token usado para autenticar o cliente. É
 fornecido pelo servidor via método RPC \'Authenticate\'.

- - \*\*FindUpdates -- \[boolean\] **Bloqueio**. Retorna verdadeiro
 se uma atualização assinada foi encontrada.
 - \*\*Reseed -- \[null\] Se solicitado, verifica se uma nova
 sementeira foi iniciada.
 - \*\*Restart -- \[null\] Se solicitado, verifica se uma
 reinicialização foi iniciada.
 - \*\*RestartGraceful -- \[null\] Se solicitado, verifica se uma
 reinicialização normal foi iniciada.
 - \*\*Shutdown -- \[null\] Se solicitado, verifica se um
 desligamento foi iniciado
 - \*\*ShutdownGraceful -- \[null\] Se solicitado, verifica se um
 desligamento normal foi iniciado
 - \*\*Update -- \[String\] **Bloqueio**. Se solicitado, retorna o
 status da atualização

```{=html}
<!-- -->
```
- - \*i2p.router.net.ntcp.port -- \[String\] Qual porta é usada para
 o transporte TCP. Se null for enviado, a configuração atual será
 retornada.
 - \*i2p.router.net.ntcp.hostname -- \[String\] Qual nome de host é
 usado para o transporte TCP. Se null for enviado, a configuração
 atual será retornada.
 - \*i2p.router.net.ntcp.autoip -- \[String\] Use ip detectado
 automaticamente para transporte TCP. Se null for enviado, a
 configuração atual será retornada.
 - \*i2p.router.net.ssu.port -- \[String\] Qual porta é usada para
 o transporte UDP. Se null for enviado, a configuração atual será
 retornada.
 - \*i2p.router.net.ssu.hostname -- \[String\] Qual nome de host é
 usado para o transporte UDP. Se null for enviado, a configuração
 atual será retornada.
 - \*i2p.router.net.ssu.autoip -- \[String\] Quais métodos devem
 ser usados para detectar o endereço IP do transporte UDP. Se
 null for enviado, a configuração atual será retornada.
 - \*i2p.router.net.ssu.detectedip -- \[null\] Qual IP foi
 detectado pelo transporte UDP.
 - \*i2p.router.net.upnp -- \[String\] O UPnP está habilitado. Se
 null for enviado, a configuração atual será retornada.
 - \*i2p.router.net.bw.share -- \[String\] Quantos por cento da
 largura de banda é utilizável para túneis participantes. Se null
 for enviado, a configuração atual será retornada.
 - \*i2p.router.net.bw.in -- \[String\] Quantos KB/s de largura de
 banda de entrada são permitidos. Se null for enviado, a
 configuração atual será retornada.
 - \*i2p.router.net.bw.out -- \[String\] Quantos KB/s de largura de
 banda de saída são permitidos. Se null for enviado, a
 configuração atual será retornada.
 - \*i2p.router.net.laptopmode -- \[String\] O modo laptop está
 habilitado (alterar identidade do roteador e porta UDP quando o
 IP muda). Se null for enviado, a configuração atual será
 retornada.
 - Token -- \[String\] Token usado para autenticar o cliente. É
 fornecido pelo servidor por meio do método RPC \'Authenticate\'.
 Se null for enviado, a configuração atual será retornada.

- - Note: i2pd routers prior to version 2.41 returned some of these
 values as numbers. For compatibility, clients should handle both
 strings and numbers.
 - \*\*i2p.router.net.ntcp.port -- \[String\] Se solicitado,
 retorna a porta usada para o transporte TCP.
 - \*\*i2p.router.net.ntcp.hostname -- \[String\] Se solicitado,
 retorna o nome do host usado para o transporte TCP.
 - \*\*i2p.router.net.ntcp.autoip -- \[String\] Se solicitado,
 retorna o método usado para detectar automaticamente o IP para o
 transporte TCP.
 - \*\*i2p.router.net.ssu.port -- \[String\] Se solicitado, retorna
 a porta usada para o transporte UDP.
 - \*\*i2p.router.net.ssu.hostname -- \[String\] Se solicitado,
 retorna o nome do host usado para o transporte UDP.
 - \*\*i2p.router.net.ssu.autoip -- \[String\] Se solicitado,
 retorna métodos usados para detectar o endereço IP do transporte
 UDP.
 - \*\*i2p.router.net.ssu.detectedip -- \[String\] Se solicitado,
 retorna qual IP foi detectado pelo transporte UDP.
 - \*\*i2p.router.net.upnp -- \[String\] Se solicitado, retorna a
 configuração UPNP.
 - \*\*i2p.router.net.bw.share -- \[String\] Se solicitado, retorna
 quantos por cento da largura de banda é utilizável para os
 túneis participantes.
 - \*\*i2p.router.net.bw.in -- \[String\] Se solicitado, retorna
 quantos KB/s de largura de banda de entrada são permitidos.
 - \*\*i2p.router.net.bw.out -- \[String\] Se solicitado, retorna
 quantos KB/s de largura de banda de saída são permitidos.
 - \*\*i2p.router.net.laptopmode -- \[String\] Se solicitado,
 retorna o modo laptop.
 - SettingsSaved -- \[boolean\] As configurações fornecidas foram
 salvas?
 - RestartNeeded -- \[boolean\] É necessário reiniciar para que as
 novas configurações sejam usadas?

```{=html}
<!-- -->
```
- - {\"setting-key\": \"setting-value\", \...} -- \[Map\]

- - {\"setting-key\": \"setting-value\", \...} -- \[Map\]

- - \"setting-key\" -- \[String\]

- 

\* denota um valor opcional.

\*\* denota um valor de retorno possivelmente ocorrendo

### Códigos de erro

- -32700 -- Erro de análise do JSON.
- -32600 -- Requisição inválida.
- -32601 -- Método não encontrado.
- -32602 -- Parâmetros inválidos.
- -32603 -- Erro interno.

```{=html}
<!-- -->
```
- -32001 -- Senha inserida inválida.
- -32002 -- Nenhum token de autenticação apresentado.
- -32003 -- Token de autenticação não existe.
- -32004 -- O token de autenticação fornecido expirou e será removido.
- -32005 -- A versão da API de I2PControl usada não foi especificada,
 mas requer-se que seja especificada.
- -32006 -- A versão da API de I2PControl não é suportada pela
 extensão I2PControl.


