 Configurando o
Gitlab com o I2P 2020-09 0.9.47 

# Configuração do Gitlab sobre I2P {#gitlab-over-i2p-setup}

::: {.meta author="idk" date="2020-03-16" excerpt="Espelhe repositórios Git I2P e Bridge Non-private internet.repositories para outros."}
:::

Este é o processo de configuração que eu uso para configurar o Gitlab e
o I2P, com o Docker instalado para gerenciar o serviço em si. O Gitlab é
muito fácil de hospedar no I2P dessa forma, ele pode ser administrado
por uma pessoa sem muita dificuldade. Na minha configuração, eu uso uma
VM Debian para hospedar contêineres docker e um roteador I2P, em um
sistema Debian Host, no entanto, isso pode ser mais do que necessário
para algumas pessoas. Essas instruções devem funcionar em qualquer
sistema baseado em Debian, independentemente de estar em uma VM ou não,
e devem ser facilmente traduzidas para qualquer sistema onde o Docker e
um roteador I2P estejam disponíveis. Este guia começa no Docker e não
assume nenhuma VM abaixo.

## Dependências e Docker {#dependencies-and-docker}

Como o Gitlab roda em um contêiner, precisamos instalar apenas as
dependências necessárias para o contêiner em nosso sistema principal.
Convenientemente, você pode instalar tudo o que precisa com:

 sudo apt install docker.io

em um sistema Debian não modificado, ou se você adicionou o repositório
Debian "Community" do próprio Docker, você pode usar:

 sudo apt install docker-ce

em vez de.

### Obter os contêineres do Docker {#fetch-the-docker-containers}

Depois de instalar o docker, você pode buscar os contêineres do docker
necessários para o gitlab. *Não os execute ainda.*

 docker pull gitlab/gitlab-ce

Para aqueles que estão preocupados, a imagem Docker gitlab-ce é
construída usando apenas imagens Docker do Ubuntu como pai, que são
construídas a partir de imagens do zero. Como não há imagens de
terceiros envolvidas aqui, as atualizações devem vir assim que estiverem
disponíveis nas imagens do host. Para revisar o Dockerfile por si mesmo,
visite o [código-fonte do
Gitlab](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile).

## Configurar um proxy HTTP I2P para uso do Gitlab (informações importantes, etapas opcionais) {#set-up-an-i2p-http-proxy-for-gitlab-to-useimportant-information-optional-steps}

Os servidores Gitlab dentro do I2P podem ser executados com ou sem a
capacidade de interagir com servidores na internet fora do I2P. No caso
em que o servidor Gitlab *não tem permissão* para interagir com
servidores fora do I2P, eles não podem ser desanonimizados clonando um
repositório git de um servidor git na internet fora do I2P. Eles podem,
no entanto, exportar e espelhar repositórios de outros serviços git
dentro do I2P.

No caso em que o servidor Gitlab tem *permissão* para interagir com
servidores fora do I2P, ele pode atuar como uma "Ponte" para os
usuários, que podem usá-lo para espelhar conteúdo fora do I2P para uma
fonte acessível ao I2P, no entanto, ele *não é anônimo* neste caso. Os
serviços Git na internet não anônima serão conectados diretamente.

**Se você quiser ter uma instância Gitlab não anônima e em ponte com
acesso a** **repositórios web,** nenhuma modificação adicional é
necessária.

**Se você quiser ter uma instância Gitlab somente I2P sem acesso aos
repositórios somente Web** , você precisará configurar o Gitlab para
usar um proxy HTTP I2P. Como o proxy HTTP I2P padrão escuta apenas em
`127.0.0.1`, você precisará configurar um novo para o Docker que escuta
no endereço Host/Gateway da rede Docker, que geralmente é `172.17.0.1`.
Eu configuro o meu na porta `4446`.

## Inicie o contêiner localmente {#start-the-container-locally}

Depois de configurar isso, você pode iniciar o contêiner e publicar sua
instância do Gitlab localmente.

 docker run --detach \
 --env HTTP_PROXY=http://172.17.0.1:4446 \
 --publish 127.0.0.1:8443:443 --publish 127.0.0.1:8080:80 --publish 127.0.0.1:8022:22 \
 --name gitlab \
 --restart always \
 --volume /srv/gitlab/config:/etc/gitlab:Z \
 --volume /srv/gitlab/logs:/var/log/gitlab:Z \
 --volume /srv/gitlab/data:/var/opt/gitlab:Z \
 gitlab/gitlab-ce:latest

Visite sua instância do Gitlab local e configure sua conta de
administrador. Escolha uma senha forte e configure os limites da conta
de usuário para corresponder aos seus recursos.

## Modifique gitlab.rb (opcional, mas uma boa ideia para hosts "Bridged non-anonymous") {#modify-gitlab.rboptional-but-a-good-idea-for-bridged-non-anonymous-hosts}

Também é possível aplicar suas configurações de Proxy HTTP de uma forma
mais granular, para que você possa permitir que usuários espelhem
repositórios somente dos domínios que você escolher. Como o domínio é
presumivelmente operado por uma organização, você pode usar isso para
garantir que repositórios que são espelháveis sigam um conjunto razoável
de políticas. Afinal, há muito mais conteúdo abusivo na internet não
anônima do que no I2P, não gostaríamos de tornar muito fácil introduzir
conteúdo abusivo de um lugar tão nefasto.

Adicione as seguintes linhas ao seu arquivo gitlab.rb dentro do
contêiner /src/gitlab/config. Essas configurações entrarão em vigor
quando você reiniciar em um momento.

 gitlab_rails['env'] = {
 "http_proxy" => "http://172.17.0.1:4446",
 "https_proxy" => "http://172.17.0.1:4446",
 "no_proxy" => ".github.com,.gitlab.com"
 }
 gitaly['env'] = {
 "http_proxy" => "http://172.17.0.1:4446",
 "https_proxy" => "http://172.17.0.1:4446",
 "no_proxy" => "unix,.github.com,.gitlab.com"
 }
 gitlab_workhorse['env'] = {
 "http_proxy" => "http
 "https_proxy" => "http://172.17.0.1:4446",
 "no_proxy" => "unix,.github.com,.gitlab.com"
 }

### Configure seus túneis de serviço e inscreva-se para um nome de host {#set-up-your-service-tunnels-and-sign-up-for-a-hostname}

Depois que você tiver o Gitlab configurado localmente, vá para o console
do I2P Router. Você precisará configurar dois túneis de servidor, um
levando à interface web (HTTP) do Gitlab na porta TCP 8080, e um para a
interface SSH do Gitlab na porta TCP 8022.

#### Interface Web (HTTP) do Gitlab {#gitlab-webhttp-interface}

Para a interface Web, use um túnel de servidor "HTTP". De
<http://127.0.0.1:7657/i2ptunnelmgr> inicie o "New Tunnel Wizard" e
insira os seguintes valores em cada etapa:

1. Selecione "Túnel do Servidor"
2. Selecione "Servidor HTTP"
3. Preencha "Gitlab Web Service" ou descreva o túnel de outra forma
4. Preencha `127.0.0.1` para o host e `8080` para a porta.
5. Selecione "Iniciar túnel automaticamente quando o roteador iniciar"
6. Confirme suas seleções.

##### Registre um nome de host (opcional) {#register-a-hostnameoptional}

Os serviços da Web no I2P podem registrar nomes de host para si mesmos
fornecendo uma sequência de autenticação para um provedor de serviços de
salto como [stats.i2p](http://stats.i2p). Para fazer isso, abra o
<http://127.0.0.1:7657/i2ptunnelmgr> novamente e clique no item "Gitlab
Web Service" que você acabou de configurar. Role até o final da seção
"Edit Server Settings" e clique em Registration Authentication. Copie o
campo que diz "Authentication for adding Hostname" e visite
[stats.i2p](http://stats.i2p/i2p/addkey.html) para adicionar seu nome de
host. Observe que se você quiser usar um subdomínio (como git.idk.i2p),
você terá que usar a sequência de autenticação correta para seu
subdomínio, o que é um pouco mais complicado e merece suas próprias
instruções.

#### Interface SSH do Gitlab {#gitlab-ssh-interface}

Para a interface SSH, use um túnel de servidor "Standard". De
<http://127.0.0.1:7657/i2ptunnelmgr> inicie o "New Tunnel Wizard" e
insira os seguintes valores em cada etapa:

1. Selecione "Túnel do Servidor"
2. Selecione "Servidor Padrão"
3. Preencha "Gitlab SSH Service" ou descreva o túnel de outra forma
4. Preencha `127.0.0.1` para o host e `8022` para a porta.
5. Selecione "Iniciar túnel automaticamente quando o roteador iniciar"
6. Confirme suas seleções.

## Reinicie o serviço Gitlab com o novo nome de host {#re-start-the-gitlab-service-with-the-new-hostname}

Por fim, se você modificou `gitlab.rb` ou registrou um nome de host,
será necessário reiniciar o serviço gitlab para que as configurações
entrem em vigor.

 docker stop gitlab
 docker rm gitlab
 docker run --detach \
 --hostname your.hostname.i2p \
 --hostname thisisreallylongbase32hostnamewithfiftytwocharacters.b32.i2p \
 --env HTTP_PROXY=http://172.17.0.1:4446 \
 --publish 127.0.0.1:8443:443 --publish 127.0.0.1:8080:80 --publish 127.0.0.1:8022:22 \
 --name gitlab \
 --restart always \
 --volume /srv/gitlab/config:/etc/gitlab:Z \
 --volume /srv/gitlab/logs:/var/log/gitlab:Z \
 --volume /srv/gitlab/data:/var/opt/gitlab:Z \
 gitlab/gitlab-ce:latest


