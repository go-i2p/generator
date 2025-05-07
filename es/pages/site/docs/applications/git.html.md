 Setting up Gitlab
with I2P 2020-09 0.9.47 

# Git over I2P for Users

Tutorial for setting up git access through an I2P Tunnel. This tunnel
will act as your access point to a single git service on I2P.

**If you intend to use the service at i2pgit.org/git.idk.i2p, then you
probably already have a tunnel configured and much of this tutorial will
not apply to you.**

## First: Set up an account at a Git service

To create your repositories on a remote git service, sign up for a user
account at that service. Of course it's also possible to create
repositories locally and push them to a remote git service, but most
will require an account and for you to create a space for the repository
on the server. Gitlab has a very simple sign-up form:

These are generic instructions for any in-i2p Git instance with HTTP and
SSH gateways. If you intend to contribute to I2P, you should create an
account at the I2P gitlab, which is open to the community. Account
registration may take a few days to complete, as the admin needs to sort
through a large number of spam registrations. You can help this by
getting in touch with the admin to confirm you are human using the
instructions on the home page.

- **[Dentro de I2P - (http://git.idk.i2p)](http://git.idk.i2p)**
- **[Fuera de I2P - (https://i2pgit.org)](https://i2pgit.org)**

![Registration is easy!](/_static/images/git/register.png)

## Second: Create a project to test with

To make sure the setup process works, it helps to make a repository to
test with from the server, and for the sake of this tutorial, we're
going to use a fork of the I2P router. First, browse to the
i2p-hackers/i2p.i2p repository:

![Browse to i2p.i2p](/_static/images/git/explore.png)

![I2P Hackers i2p.i2p](/_static/images/git/i2p.png)

Then, fork it to your account.

![Roger is forking](/_static/images/git/fork.png)

![Roger is finished](/_static/images/git/forked.png)

## Third: Set up your git client tunnel

To have read-write access to my server, you'll need to set up a tunnel
for your SSH client. As an example, we're going to use the HTTP tunnel
instead, but if all you need is read-only, HTTP/S cloning, then you can
skip all this and just use the http_proxy environment variable to
configure git to use the pre-configured I2P HTTP Proxy. For example:

 http_proxy=http://localhost:4444 git clone http://gittest.i2p/i2p-developer/i2p.i2p

![Client tunnel](/_static/images/git/wizard1.png)

![Git over I2P](/_static/images/git/wizard2.png)

Then, add the address you will be pushing and pulling from. Note that
this example address is for Read-Only HTTP-over-I2P clones, if your
admin does not allow the git HTTP(Smart HTTP) protocol, then you will
need to get the SSH clone base32 from them. If you have an SSH clone
base32, substitute it for the base32 in this step, which will fail.

![gittest.i2p](/_static/images/git/wizard3.png)

Pick a port to forward the I2P service to locally.

![localhost:localport](/_static/images/git/wizard4.png)

I use it alot, so I start my client tunnel automatically, but it's up to
you.

![Auto Start](/_static/images/git/wizard5.png)

When you're all done, it should look alot like this.

![Review settings](/_static/images/git/wizard6.png)

## Fourth: Attempt a clone {#trans--fourth-attempt-a-clone--endtrans}

Now your tunnel is all set up, you can attempt a clone over SSH.

Git Privacy: Committing to git adds a timestamp to git commit messages,
which may be configured to reflect your local time zone. To enforce the
use of UTC for all commits, you are advised to use a git alias, such as:

 git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'

which will allow you to substitute

 git commit

para

 git utccommit

in order to obscure your local time zone.

 GIT_SSH_COMMAND="ssh -p 7442" \
 git clone git@127.0.0.1:i2p-developer/i2p.i2p

You might get an error where the remote end hangs up unexpectedly.
Unfortunately git still doesn't support resumable cloning. Until it
does, there are a couple fairly easy ways to handle this. The first and
easiest is to try and clone to a shallow depth:

 GIT_SSH_COMMAND="ssh -p 7442" \
 git clone --depth 1 git@127.0.0.1:i2p-developer/i2p.i2p

Once you've performed a shallow clone, you can fetch the rest resumably
by changing to the repo directory and running:

 git fetch --unshallow

At this point, you still don't have all your branches yet. You can get
them by running the following commands:

 git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
 git fetch origin

Which tells git to alter the repository configuration so that fetching
from origin fetches all branches.

If that doesn't work, you can try opening the tunnel configuration menu
and adding some backup tunnels.

![Backup Tunnels](/_static/images/git/tweak2.png)

If that doesn't work, then the next easy thing to try is to decrease the
tunnel length. Don't do this if you believe you are at risk of your
code-contribution activity being de-anonymized by a well-resourced
attacker seeking to run many malicious nodes and control your whole
path. If that sounds unlikely to you then you can probably do it safely.

![One-Hop Tunnels](/_static/images/git/tweak1.png)

## *Suggested Workflow for Developers!* {#trans--suggested-workflow-for-developers--endtrans}

Revision control can make your life easier, but it works best if you use
it well! In light of this, we strongly suggest a fork-first,
feature-branch workflow as many are familiar with from Github. In such a
workflow, the master branch is used as a sort of "Trunk" for updates and
is never touched by the programmmer, instead, all changes to the master
are merged from branches. In order to do set up your workspace for this,
take the following steps:

- **Never make changes to the Master Branch**. You will be using the
 master branch to periodially obtain updates to the official source
 code. All changes should be made in feature branches.

1. Set up a second remote in your local repository using the upstream
 source code.

 git remote add upstream git@127.0.0.1:i2p-hackers/i2p.i2p

2. Pull in any upstream changes on your current master:

 git pull upstream master

3. Before making any changes to the source code, check out a new
 feature branch to develop on:

 git checkout -b feature-branch-name

4. When you're done with your changes, commit them and push them to
 your branch

 git commit -am "I added an awesome feature!"
 git push origin feature-branch-name

5. Submit a merge request. When the merge request is approved and
 brought into the upstream master, check out the master locally and
 pull in the changes:

 git checkout master
 git pull upstream master

6. Whenever a change to the upstream master(i2p-hackers/i2p.i2p) is
 made, you can update your master code using this procedure as well.

 git checkout master
 git pull upstream master

The git utccommit alias solution to git timestamp issue was arrived at
from the information first published here:
[saebamini.com](https://saebamini.com/Git-commit-with-UTC-timestamp-ignore-local-timezone/).


