 Clientes
gerenciados Fevereiro de 2014 0.9.11 

## Visão geral

Clients may be started directly by the router when they are listed in
the [clients.config]() file. These clients
may be \"managed\" or \"unmanaged\". This is handled by the
ClientAppManager. Additionally, managed or unmanaged clients may
register with the ClientAppManager so that other clients may retrieve a
reference to them. There is also a simple Port Mapper facility for
clients to register an internal port that other clients may look up.

## Clientes gerenciados

A partir da versão 0.9.4, o roteador suporta clientes gerenciados. Os
clientes gerenciados são instanciados e iniciados pelo ClientAppManager.
O ClientAppManager mantém uma referência ao cliente e recebe
atualizações sobre o estado do cliente. Os clientes gerenciados são
preferidos, pois é muito mais fácil implementar o rastreamento de estado
e iniciar e parar um cliente. Também é muito mais fácil evitar
referências estáticas no código do cliente que podem levar ao uso
excessivo de memória após um cliente ser interrompido. Os clientes
gerenciados podem ser iniciados e interrompidos pelo usuário no console
do roteador, e são interrompidos no desligamento do roteador.

Os clientes gerenciados implementam a interface net.i2p.app.ClientApp ou
net.i2p.router.app.RouterApp. Os clientes que implementam a interface
ClientApp devem fornecer o seguinte construtor:

 public MyClientApp(I2PAppContext context, ClientAppManager listener, String[] args)

Os clientes que implementam a interface RouterApp devem fornecer o
seguinte construtor:

 public MyClientApp(RouterContext context, ClientAppManager listener, String[] args)

Os argumentos fornecidos são especificados no arquivo clients.config.

## Clientes não gerenciados

Se a classe principal especificada no arquivo clients.config não
implementar uma interface gerenciada, ela será iniciada com main() com
os argumentos especificados, e interrompida com main() com os argumentos
especificados. O roteador não mantém uma referência, pois todas as
interações são por meio do método main() estático. O console não pode
fornecer informações de estado precisas ao usuário.

## Clientes Registrados

Clientes, gerenciados ou não, podem se registrar no ClientAppManager
para que outros clientes possam recuperar uma referência a eles. O
registro é feito por nome. Os clientes registrados conhecidos são:

 console, i2ptunnel, Jetty, outproxy, update

## Mapeador de Portos

O roteador também fornece um mecanismo simples para clientes encontrarem
um serviço de socket interno, como o proxy HTTP. Isso é fornecido pelo
Port Mapper. O registro é por nome. Clientes que se registram geralmente
fornecem um socket emulado interno naquela porta.


