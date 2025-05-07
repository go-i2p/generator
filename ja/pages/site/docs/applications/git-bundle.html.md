 Setting up Gitlab
with I2P 2020-09 0.9.47 

# gitバンドルを使ったI2Pソースコードの取得 {#using-a-git-bundle-to-fetch-the-i2p-source-code}

Cloning large software repositories over I2P can be difficult, and using
git can sometimes make this harder. Fortunately, it can also sometimes
make it easier. Git has a `git bundle` command which can be used to turn
a git repository into a file which git can then clone, fetch, or import
from a location on your local disk. By combining this capability with
bittorrent downloads, we can solve our remaining problems with
`git clone`.

## 始める前に {#before-you-start}

If you intend to generate a git bundle, you **must** already possess a
full copy of the **git** repository, not the mtn repository. You can get
it from github or from git.idk.i2p, but a shallow clone(a clone done to
--depth=1) *will not* *work*. It will fail silently, creating what looks
like a bundle, but when you try to clone it it will fail. If you are
just retrieving a pre-generated git bundle, then this section does not
apply to you.

## I2PソースをBitTorrent経由で取得 {#fetching-i2p-source-via-bittorrent}

Someone will need to supply you with a torrent file or a magnet link
corresponding to an existing `git bundle` that they have already
generated for you. A recent, correctly-generated bundle of the mainline
i2p.i2p source code as-of Wednesday, March 18, 2020, can be found inside
of I2P at my pastebin
[paste.idk.i2p/f/4hq37i](http://paste.idk.i2p/f/4h137i).

Once you have a bundle, you will need to use git to create a working
repository from it. If you're using GNU/Linux and i2psnark, the git
bundle should be located in \$HOME/.i2p/i2psnark or, as a service on
Debian, /var/lib/i2p/i2p-config/i2psnark. If you are using BiglyBT on
GNU/Linux, it is probably at "\$HOME/BiglyBT Downloads/" instead. The
examples here assume I2PSnark on GNU/Linux, if you use something else,
replace the path to the bundle with the download directory preferred by
your client and platform.

### Using `git clone`

gitバンドルからのクローンは簡単です。単に：

 git clone $HOME/.i2p/i2psnark/i2p.i2p.bundle

If you get the following error, try using git init and git fetch
manually instead.

 fatal: multiple updates for ref 'refs/remotes/origin/master' not allowed

### Using `git init` and `git fetch`

まず gitレポジトリとするためのi2p.i2pディレクトリを作成します。

 mkdir i2p.i2p && cd i2p.i2p

次に、更新取得にむけて空のgitレポジトリを初期化します。

 git init

最後に、バンドルからレポジトリを取得します。

 git fetch $HOME/.i2p/i2psnark/i2p.i2p.bundle

### バンドルリモートを上流リモートで置き換える {#replace-the-bundle-remote-with-the-upstream-remote}

バンドルを持っている今、リモートを上流レポジトリソースに設定することで更新に追従できます。

 git remote set-url origin git@127.0.0.1:i2p-hackers/i2p.i2p

## バンドルの生成 {#generating-a-bundle}

First, follow the [Git guide for Users](GIT.md) until you have a
successfully `--unshallow`ed clone of clone of the i2p.i2p repository.
If you already have a clone, make sure you run `git fetch --unshallow`
before you generate a torrent bundle.

取得できたら、対応するant targetを走らせるだけです：

 ant git-bundle

and copy the resulting bundle into your I2PSnark downloads directory.
For instance:

 cp i2p.i2p.bundle* $HOME/.i2p/i2psnark/

数分でI2PSnarkがそのトレントを拾います。
「開始」ボタンをクリックし、torrentのシードを始めてください。


