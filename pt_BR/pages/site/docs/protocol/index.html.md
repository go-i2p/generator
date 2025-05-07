 Pilha de
Protocolos 2024-01 0.9.61 

Here is the protocol stack for I2P. See also the [Index to Technical
Documentation]().

Cada uma das camadas na pilha fornece recursos extras. Os recursos estão
listados abaixo, começando na parte inferior da pilha de protocolos.

- **Camada de Internet:**\
 IP: Protocolo de Internet, permite endereçar hosts na Internet
 regular e rotear pacotes pela Internet usando entrega de melhor
 esforço.
- **Camada de transporte:**\
 TCP: Protocolo de Controle de Transmissão, permite a entrega
 confiável e ordenada de pacotes pela internet.\
 UDP: User Datagram Protocol, permite a entrega não confiável e fora
 de ordem de pacotes pela Internet.
- **Camada de Transporte I2P:** fornece conexões criptografadas entre
 2 roteadores I2P. Eles ainda não são anônimos, é estritamente uma
 conexão hop-to-hop. Dois protocolos são implementados para fornecer
 esses recursos. O NTCP2 é construído sobre o TCP, enquanto o SSU usa
 o UDP.\
 [NTCP2](): TCP baseado em NIO\
 [SSU](): UDP
 semi-confiável seguro
- **Camada de túnel I2P:** fornece conexões de túnel totalmente
 criptografadas.\
 [Tunnel messages](): tunnel messages
 are large messages containing encrypted I2NP (see below) messages
 and encrypted instructions for their delivery. The encryption is
 layered. The first hop will decrypt the tunnel message and read a
 part. Another part can still be encrypted (with another key), so it
 will be forwarded.\
 [I2NP messages](): I2P Network Protocol
 messages are used to pass messages through multiple routers. These
 I2NP messages are combined in tunnel messages.
- **Camada I2P Garlic:** fornece entrega de mensagens I2P
 criptografadas e anônimas de ponta a ponta.\
 [I2NP messages](): I2P Network Protocol
 messages are wrapped in each other and used to ensure encryption
 between two tunnels and are passed along from source to destination,
 keeping both anonymous.

As camadas a seguir, estritamente falando, não fazem mais parte da pilha
do protocolo I2P e não fazem parte da funcionalidade principal do
\"roteador I2P\". No entanto, cada uma dessas camadas adiciona
funcionalidade adicional para permitir que os aplicativos usem o I2P de
forma simples e conveniente.

**Camada de cliente I2P:** permite que qualquer cliente use a
funcionalidade I2P, sem exigir o uso direto da API do roteador.\
[I2CP](): I2P Client Protocol, allows secure and
asynchronous messaging over I2P by communicating messages over the I2CP
TCP socket.

**Camada de transporte ponta a ponta I2P:** permite funcionalidade
semelhante a TCP ou UDP sobre I2P.\
[Streaming Library](): an implementation of
TCP-like streams over I2P. This allows easier porting of existing
applications to I2P.\
[Datagram Library](): an implementation of
UDP-like messages over I2P. This allows easier porting of existing
applications to I2P.

**Camada de interface de aplicação I2P:** bibliotecas adicionais
(opcionais) que permitem implementações mais fáceis sobre I2P.\
[I2PTunnel]()\
[SAMv3]()

**Camada de proxy de aplicativo I2P:** sistemas proxy.\
Por fim, o que poderia ser considerado a **\'camada de aplicação
I2P\'**é um grande número de aplicações sobre I2P. Podemos ordenar isso
com base na camada de pilha I2P que eles usam.

- **Aplicações de streaming/datagrama**: i2psnark, Syndie, i2phex\...
- **Aplicações SAM**: IMule, i2p-bt\...
- **Other I2P
 applications**: Syndie, EepGet,
 [plugins]()\...
- **Aplicações regulares**: Jetty, Apache, Git, navegadores,
 e-mail\...

::: {.box style="text-align:center;"}
![I2P Network
stack](images/protocol_stack.png "I2P Network stack")\
\
Figura 1: As camadas na pilha de rede I2P.
:::

\

\* Observação: o SAM pode usar tanto a biblioteca de streaming quanto os
datagramas.


