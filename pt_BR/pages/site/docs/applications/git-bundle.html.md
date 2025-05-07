 Configurando o
Gitlab com o I2P 2020-09 0.9.47 

# Usando um pacote git para buscar o código-fonte I2P {#using-a-git-bundle-to-fetch-the-i2p-source-code}

Clonar grandes repositórios de software sobre I2P pode ser difícil, e
usar o git às vezes pode tornar isso mais difícil. Felizmente, às vezes
também pode tornar isso mais fácil. O Git tem um comando `git bundle`
que pode ser usado para transformar um repositório git em um arquivo que
o git pode então clonar, buscar ou importar de um local no seu disco
local. Ao combinar essa capacidade com downloads de bittorrent, podemos
resolver nossos problemas restantes com `git clone`.

## Antes de começar {#before-you-start}

Se você pretende gerar um pacote git, você **deve** já possuir uma cópia
completa do repositório **git** , não do repositório mtn. Você pode
obtê-lo do github ou do git.idk.i2p, mas um clone raso (um clone feito
para --depth=1) *não* *funcionará*. Ele falhará silenciosamente, criando
o que parece ser um pacote, mas quando você tentar cloná-lo, ele
falhará. Se você estiver apenas recuperando um pacote git pré-gerado,
esta seção não se aplica a você.

## Obtendo a fonte I2P via Bittorrent {#fetching-i2p-source-via-bittorrent}

Alguém precisará fornecer a você um arquivo torrent ou um link magnet
correspondente a um pacote git existente que eles já geraram para você.
Um pacote recente e corretamente gerado do código-fonte principal
i2p.i2p de quarta-feira, 18 de março de 2020, pode ser encontrado dentro
do I2P no meu pastebin
[paste.idk.i2p/f/4hq37i](http://paste.idk.i2p/f/4h137i).

Depois de ter um pacote, você precisará usar o git para criar um
repositório funcional a partir dele. Se estiver usando GNU/Linux e
i2psnark, o pacote git deve estar localizado em \$HOME/.i2p/i2psnark ou,
como um serviço no Debian, /var/lib/i2p/i2p-config/i2psnark. Se estiver
usando o BiglyBT no GNU/Linux, provavelmente ele estará em
"\$HOME/BiglyBT Downloads/". Os exemplos aqui assumem o I2PSnark no
GNU/Linux, se você usar outra coisa, substitua o caminho para o pacote
pelo diretório de download preferido pelo seu cliente e plataforma.

### Usando `git clone` {#using-git-clone}

A clonagem de um pacote git é fácil, basta:

 git clone $HOME/.i2p/i2psnark/i2p.i2p.bundle

Se você receber o seguinte erro, tente usar git init e git fetch
manualmente.

 fatal: multiple updates for ref 'refs/remotes/origin/master' not allowed

### Usando `git init` e `git fetch` {#using-git-init-and-git-fetch}

Primeiro, crie um diretório i2p.i2p para transformá-lo em um repositório
git.

 mkdir i2p.i2p && cd i2p.i2p

Em seguida, inicialize um repositório git vazio para buscar as
alterações novamente.

 git init

Por fim, busque o repositório do pacote.

 git fetch $HOME/.i2p/i2psnark/i2p.i2p.bundle

### Substitua o controle remoto do pacote pelo controle remoto upstream {#replace-the-bundle-remote-with-the-upstream-remote}

Agora que você tem um pacote, pode acompanhar as alterações configurando
o controle remoto para a origem do repositório upstream.

 git remote set-url origin git@127.0.0.1:i2p-hackers/i2p.i2p

## Gerando um pacote {#generating-a-bundle}

Primeiro, siga o guia do Git [para usuários](GIT.md) até que você tenha
um clone `--unshallow`editado com sucesso do clone do repositório
i2p.i2p. Se você já tem um clone, certifique-se de executar
`git fetch --unshallow` antes de gerar um pacote torrent.

Depois de ter isso, basta executar o alvo ant correspondente:

 ant git-bundle

e copie o pacote resultante para o seu diretório de downloads do
I2PSnark. Por exemplo:

 cp i2p.i2p.bundle* $HOME/.i2p/i2psnark/

Em um ou dois minutos, o I2PSnark vai pegar o torrent. Clique no botão
"Start" para começar a semear o torrent.


