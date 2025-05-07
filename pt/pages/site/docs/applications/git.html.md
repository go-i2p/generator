 Configurando o
Gitlab com o I2P 2020-09 0.9.47 

# Git over I2P for Users

Tutorial para configurar acesso git por meio de um túnel I2P. Este túnel
atuará como seu ponto de acesso a um único serviço git no I2P.

**Se você pretende usar o serviço em i2pgit.org/git.idk.i2p,
provavelmente já tem um túnel configurado e grande parte deste tutorial
não se aplicará a você.**

## Primeiro: crie uma conta em um serviço Git {#first-set-up-an-account-at-a-git-service}

Para criar seus repositórios em um serviço git remoto, inscreva-se para
uma conta de usuário naquele serviço. Claro que também é possível criar
repositórios localmente e enviá-los para um serviço git remoto, mas a
maioria exigirá uma conta e que você crie um espaço para o repositório
no servidor. O Gitlab tem um formulário de inscrição muito simples:

Estas são instruções genéricas para qualquer instância Git in-i2p com
gateways HTTP e SSH. Se você pretende contribuir para o I2P, você deve
criar uma conta no gitlab do I2P, que é aberto para a comunidade . O
registro da conta pode levar alguns dias para ser concluído, pois o
administrador precisa classificar um grande número de registros de spam.
Você pode ajudar entrando em contato com o administrador para confirmar
que você é humano usando as instruções na página inicial.

- **[Dentro do I2P - (http://git.idk.i2p)](http://git.idk.i2p)**
- **[Fora do I2P - (https://i2pgit.org)](https://i2pgit.org)**

![Registration is easy!](/_static/images/git/register.png)

## Second: Create a project to test with

Para garantir que o processo de configuração funcione, ajuda criar um
repositório para testar com o servidor e, para o propósito deste
tutorial, usaremos um fork do roteador I2P. Primeiro, navegue até o
repositório i2p-hackers/i2p.i2p:

![Browse to i2p.i2p](/_static/images/git/explore.png)

![I2P Hackers i2p.i2p](/_static/images/git/i2p.png)

Depois, bifurque-o para sua conta.

![Roger is forking](/_static/images/git/fork.png)

![Roger is finished](/_static/images/git/forked.png)

## Third: Set up your git client tunnel

Para ter acesso de leitura e gravação ao meu servidor, você precisará
configurar um túnel para seu cliente SSH. Como exemplo, usaremos o túnel
HTTP, mas se tudo o que você precisa é somente leitura, clonagem HTTP/S,
então você pode pular tudo isso e usar apenas a variável de ambiente
http_proxy para configurar o git para usar o Proxy HTTP I2P
pré-configurado. Por exemplo:

 http_proxy=http://localhost:4444 git clone http://gittest.i2p/i2p-developer/i2p.i2p

![Client tunnel](/_static/images/git/wizard1.png)

![Git over I2P](/_static/images/git/wizard2.png)

Em seguida, adicione o endereço do qual você fará push e pull. Observe
que este endereço de exemplo é para clones HTTP-over-I2P somente
leitura, se seu administrador não permitir o protocolo git HTTP (Smart
HTTP), então você precisará obter o clone SSH base32 deles. Se você
tiver um clone SSH base32, substitua-o pelo base32 nesta etapa, o que
falhará.

![gittest.i2p](/_static/images/git/wizard3.png)

Escolha uma porta para encaminhar o serviço I2P localmente.

![localhost:localport](/_static/images/git/wizard4.png)

Eu o uso muito, então inicio meu túnel de cliente automaticamente, mas
fica a seu critério.

![Auto Start](/_static/images/git/wizard5.png)

Quando terminar, deve ficar parecido com isso.

![Review settings](/_static/images/git/wizard6.png)

## Quarto: Tente um clone {#trans--fourth-attempt-a-clone--endtrans}

Agora que seu túnel está configurado, você pode tentar uma clonagem via
SSH.

Privacidade do Git: Comprometer-se com o git adiciona um timestamp às
mensagens de commit do git, que podem ser configuradas para refletir seu
fuso horário local. Para impor o uso do UTC para todos os commits, é
aconselhável usar um alias do git, como:

 git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'

que lhe permitirá substituir

 git commit

durante

 git utccommit

para ocultar seu fuso horário local.

 GIT_SSH_COMMAND="ssh -p 7442" \
 git clone git@127.0.0.1:i2p-developer/i2p.i2p

Você pode receber um erro em que o terminal remoto desliga
inesperadamente. Infelizmente, o git ainda não suporta clonagem
retomável. Até que isso aconteça, há algumas maneiras bem fáceis de
lidar com isso. A primeira e mais fácil é tentar clonar para uma
profundidade rasa:

 GIT_SSH_COMMAND="ssh -p 7442" \
 git clone --depth 1 git@127.0.0.1:i2p-developer/i2p.i2p

Depois de executar uma clonagem superficial, você pode buscar o restante
de forma contínua, alterando para o diretório do repositório e
executando:

 git fetch --unshallow

Neste ponto, você ainda não tem todos os seus branches. Você pode
obtê-los executando os seguintes comandos:

 git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
 git fetch origin

O que diz ao git para alterar a configuração do repositório para que a
busca na origem busque todos os branches.

Se isso não funcionar, você pode tentar abrir o menu de configuração do
túnel e adicionar alguns túneis de backup.

![Backup Tunnels](/_static/images/git/tweak2.png)

Se isso não funcionar, a próxima coisa fácil a tentar é diminuir o
comprimento do túnel. Não faça isso se você acredita que corre o risco
de sua atividade de contribuição de código ser desanonimizada por um
invasor bem-recursos buscando executar muitos nós maliciosos e controlar
todo o seu caminho. Se isso parece improvável para você, então você
provavelmente pode fazer isso com segurança.

![One-Hop Tunnels](/_static/images/git/tweak1.png)

## *Fluxo de trabalho sugerido para desenvolvedores!* {#trans--suggested-workflow-for-developers--endtrans}

O controle de revisão pode facilitar sua vida, mas funciona melhor se
você usá-lo bem! Em vista disso, sugerimos fortemente um fluxo de
trabalho fork-first, feature-branch, como muitos estão familiarizados no
Github. Em tal fluxo de trabalho, o branch master é usado como uma
espécie de "Trunk" para atualizações e nunca é tocado pelo programador,
em vez disso, todas as alterações no master são mescladas dos branches.
Para configurar seu espaço de trabalho para isso, siga os seguintes
passos:

- **Nunca faça alterações no Master Branch**. Você usará o master
 branch para obter atualizações periódicas do código-fonte oficial.
 Todas as alterações devem ser feitas em feature branches.

1. Configure um segundo controle remoto no seu repositório local usando
 o código-fonte upstream.

 git remote add upstream git@127.0.0.1:i2p-hackers/i2p.i2p

2. Puxe quaisquer alterações upstream no seu master atual:

 git pull upstream master

3. Antes de fazer qualquer alteração no código-fonte, confira um novo
 branch de recurso para desenvolver:

 git checkout -b feature-branch-name

4. Quando terminar suas alterações, confirme-as e envie-as para sua
 ramificação

 git commit -am "I added an awesome feature!"
 git push origin feature-branch-name

5. Envie uma solicitação de mesclagem. Quando a solicitação de
 mesclagem for aprovada e trazida para o master upstream, faça
 check-out do master localmente e puxe as alterações:

 git checkout master
 git pull upstream master

6. Sempre que uma alteração no master upstream (i2p-hackers/i2p.i2p)
 for feita, você também pode atualizar seu código master usando este
 procedimento.

 git checkout master
 git pull upstream master

A solução do alias git utccommit para o problema do git timestamp foi
obtida a partir das informações publicadas aqui:
[saebamini.com](https://saebamini.com/Git-commit-with-UTC-timestamp-ignore-local-timezone/).


