 Extensões Junho de 2012 0.9 

## Informação geral

The I2P network includes a plugin architecture to support both easy
development and installation of new plugins.

Agora há plugins disponíveis que oferecem suporte a e-mail distribuído,
blogs, clientes IRC , armazenamento de arquivos distribuído, wikis e
muito mais.

### Adding Plugins To Your I2P Router

Os plugins I2P podem ser instalados copiando o URL de download do plugin
para a seção apropriada na [Página de configuração do plugin do console
do roteador](http://127.0.0.1:7657/configplugins).

Comece copiando a URL do plugin da página onde ele está publicado.

![](/_static/images/plugins/plugin-step-0.png)

Em seguida, visite a página de configuração do plugin, cujo link está na
página inicial do console.

![](/_static/images/plugins/plugin-step-1.png)

Cole a URL e clique no botão \"Instalar Plugin\".

![](/_static/images/plugins/plugin-step-2.png)

### Benefícios para os usuários da I2P e desenvolvedores de aplicações:

- Fácil distribuição de aplicativos
- Permite inovação e uso de bibliotecas adicionais sem se preocupar em
 aumentar o tamanho de `i2pupdate.sud`
- Suporta aplicações grandes ou de propósito especial que nunca seriam
 agrupadas com a instalação do I2P
- Aplicativos verificados e assinados com criptografia
- Atualizações automática de aplicações, tal como para o roteador
- Pacotes de instalação e atualização iniciais separados, se desejado,
 para downloads de atualização menores
- Instalação de aplicativos com um clique. Não é mais necessário pedir
 aos usuários para modificar `wrapper.config` ou `clients.config`
- Isolar aplicativos da instalação base `$I2P`
- Verificação automática de compatibilidade para versão I2P, versão
 Java, versão Jetty e versão anterior do aplicativo instalado
- Adição automática de link no console
- Inicialização automática do aplicativo, incluindo modificação do
 classpath, sem necessidade de reinicialização
- Integração automática e inicialização de webapps na instância do
 console Jetty
- Facilitate creation of \'app stores\' like the one at [](http://)
- Desinstalação em um clique.
- Pacotes de temas e idiomas para o painel
- Traga informações detalhadas do aplicativo para o console do
 roteador
- Aplicativos não-java também suportados

### Versão do roteador I2P necessária

0.7.12 ou mais recente.

### Atualizando um plugin

Para atualizar um plugin para a versão mais recente, basta clicar no
botão de atualização em
[configclients.jsp](http://127.0.0.1:7657/configclients.jsp#plugin). Há
também um botão para verificar se o plugin tem uma versão mais recente,
assim como um botão para verificar atualizações para todos os plugins.
Os plugins serão verificados para atualizações automaticamente ao
atualizar para uma nova versão I2P (não incluindo dev builds).

![](/_static/images/plugins/plugin-update-0.png)

### Desenvolvimento

See the latest [plugin specification]()

See also the sources for plugins developed by various people. Some
plugins, such as
[snowman](http:///plugins/snowman), were
developed specifically as examples.

### Primeiros passos

To create a plugin from an existing binary package you will need to get
makeplugin.sh from [the i2p.scripts repository in
git]().

### Problemas conhecidos

Observe que a arquitetura de plug-ins do roteador **NÃO** atualmente
fornece qualquer isolamento de segurança adicional ou sandbox de
plug-ins.

- Atualizações de um plugin com jars incluídos (não wars) não serão
 reconhecidas se o plugin já tiver sido executado, pois requer
 truques do carregador de classes para liberar o cache de classe ;
 uma reinicialização completa do roteador é necessária.
- O botão de parada pode ser exibido mesmo que não haja nada para
 parar.
- Extensões rodando em Máquina Virtual Java separada criam um
 diretório de `registros/` em `$CWD`.
- Nenhuma chave inicial está presente, exceto as de jrandom e zzz
 (usando as mesmas chaves da atualização do roteador), então a
 primeira chave vista para um signatário é aceita
 automaticamente---não há autoridade de chave de assinatura.
- Quando se apaga uma extensão, o diretório nem sempre é apagado,
 especialmente no Windows.
- Instalar um plugin que requer Java 1.6 em uma máquina Java 1.5
 resultará em uma mensagem \"plugin está corrompido\" se a
 compactação pack200 do arquivo de plugin for usada.
- Os plugins de tema e tradução não foram testados.
- Desativar a autoinicialização nem sempre funciona.


