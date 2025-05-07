 SOCKS 

## SOCKS e proxies SOCKS

The SOCKS proxy is working as of release 0.7.1. SOCKS 4/4a/5 are
supported. Enable SOCKS by creating a SOCKS client tunnel in i2ptunnel.
Both shared-clients and non-shared are supported. There is no SOCKS
outproxy so it is of limited use. 

Muitos aplicativos vazam informações sensíveis que podem identificá-lo
na Internet. O I2P filtra apenas dados de conexão, mas se o programa que
você pretende executar enviar essas informações como conteúdo, o I2P não
tem como proteger seu anonimato. Por exemplo, alguns aplicativos de
e-mail enviarão o endereço IP da máquina em que estão sendo executados
para um servidor de e-mail. Não há como o I2P filtrar isso, portanto,
usar o I2P para \'socksify\' aplicativos existentes é possível, mas
extremamente perigoso.

E citando um email de 2005:

 ... há uma razão pela qual humanos e
 outros construíram e abandonaram os proxies SOCKS. Encaminhar
 tráfego arbitrário é simplesmente inseguro, e cabe a nós, como
 desenvolvedores de software de anonimato e segurança, ter a segurança de
 nossos usuários finais em primeiro lugar em nossas mentes.

Esperar que possamos simplesmente amarrar um cliente arbitrário em cima
do I2P sem auditar tanto seu comportamento quanto seus protocolos
expostos para segurança e anonimato é ingênuo. Praticamente \*todos\* os
aplicativos e protocolos violam o anonimato, a menos que tenham sido
projetados para isso especificamente, e mesmo assim, a maioria deles
também o faz. Essa é a realidade. Usuários finais são mais bem atendidos
com sistemas projetados para anonimato e segurança. Modificar sistemas
existentes para funcionar em ambientes anônimos não é pouca coisa,
ordens de magnitude mais funcionam do que simplesmente usar as APIs I2P
existentes.

O proxy SOCKS suporta nomes de catálogo de endereços padrão, mas não
destinos Base64. Hashes Base32 devem funcionar a partir da versão 0.7.
Ele suporta apenas conexões de saída, ou seja, um cliente I2PTunnel. O
suporte a UDP foi desativado, mas ainda não está funcionando. A seleção
de proxy de saída por número de porta foi desativada.

The notes for [Meeting 81]() and [Meeting
82]() in March 2004.

[Onioncat](http://www.abenteuerland.at/onioncat/)

[](http:///)

### Se você conseguir fazer algo funcionar

Por favor, nos avise. E por favor, forneça avisos substanciais sobre os
riscos dos proxies de meias. 
