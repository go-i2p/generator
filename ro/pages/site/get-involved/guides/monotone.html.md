 Ghid Monoton 2021-01 

1. [Operating a Monotone client](#operating-a-monotone-client)
 1. [Generating Monotone keys](#generating-monotone-keys)
 2. [Trust and initializing your
 repository](#trust-and-initializing-your-repository)
 3. [Obtaining and deploying developers\'
 keys](#obtaining-and-deploying-developers-keys)
 4. [Setting up trust evaluation
 hooks](#setting-up-trust-evaluation-hooks)
 5. [Pulling the `i2p.i2p`, `i2p.www` and `i2p.syndie`
 branches](#pulling-the-i2p.i2p-i2p.www-and-i2p.syndie-branches)
 6. [Verifying that trust evaluation
 works](#verifying-that-trust-evaluation-works)
 7. [Checking out a working copy of the latest
 version](#checking-out-a-working-copy-of-the-latest-version)
 8. [Updating your working copy to the latest
 version](#updating-your-working-copy-to-the-latest-version)
2. [Operating a Monotone Server](#operating-a-monotone-server)
 1. [Obtaining and deploying developers' transport
 keys](#obtaining-and-deploying-developers-transport-keys)
 2. [Granting push and pull access](#granting-push-and-pull-access)
 3. [Running Monotone in server
 mode](#running-monotone-in-server-mode)
 4. [Differences under Debian
 GNU/Linux](#differences-under-debian-gnulinux)

 

**Note:** We are no longer using monotone. The project has migrated all
source repos to git.

*This is a revised version of [Complication\'s original
guide]() detailing the use of Monotone
in I2P development. For basic instructions see the [quick-start
guide]().*

I2P has a distributed development model. The source code is replicated
across independently administered [Monotone](http://www.monotone.ca/)
(\"MTN\") repositories. Developers with commit rights are able to push
their changes to the repository (a [license
agreement](#commit) needs to be signed before
commit rights are granted).

Some of Monotone\'s noteworthy qualities are: distributed version
control, cryptographic authentication, access control, its small size,
having few dependencies, storage of projects in a compressed SQLite
database file, and having the ability to resume interrupted
synchronization attempts.

## Operating a Monotone Client

### Generating Monotone keys

A transport key grants you the ability to push your changes to a
Monotone repository server. In order to commit code into Monotone (in
essence signing your code), a commit key is also needed. None of the
public Monotone servers on I2P currently require a key in order to read
(or pull) the source code.

Without a transport key, one cannot:

- pull code from a server which doesn\'t allow global read access
- push code to any server
- run a Monotone server

Without a commit key, one cannot:

- commit any code

If you only intend to retrieve code from MTN, feel free to skip to the
[next section](#trust-and-initializing-your-repository). If you want to
generate keys, read the following.

By convention keys are named like an e-mail addresses, but a
corresponding e-mail address does not need to exist. For example, your
keys might be named:

- yourname@mail.i2p
- yourname-transport@mail.i2p

Monotone stores keys under **`$HOME/.monotone/keys`** in text files
which are named identically to the keys. For example:

- `/home/complication/.monotone/keys/complication@mail.i2p`

To generate transport and commit keys, enter the following commands at a
prompt:

- `$ `**`mtn genkey yourname-transport@someplace`**
- `$ `**`mtn genkey yourname@someplace`**

Monotone will prompt you for a password to protect your keys. You are
very strongly encouraged to set a password for the commit key. Many
users will leave an empty password for the transport key, especially
those running a Monotone server.

### Trust, and initializing your repository

*Monotone\'s security model helps to ensure that nobody can easily
impersonate a developer without it being noticed. Since developers can
make mistakes and become compromised,only manual review can ensure
quality of code. Monotone\'s trust model will ensure that you read the
right diffs. It does not replace reading diffs.*

A Monotone repository is a single file (a compressed SQLite database)
which contains all of the project\'s source code and history.

After [importing the developers\' keys into
Monotone](#obtaining-and-deploying-developers-keys) and [setting up
trust evaluation hooks](#setting-up-trust-evaluation-hooks), Monotone
will prevent untrusted code from being checked out into your workspace.
There are commands available to clean untrusted code from your workspace
but in practice they\'ve not been needed due to the push access policies
in place.

A repository can hold many branches. For example, our repository holds
the following main branches:

- **i2p.i2p** --- The I2P router and associated programs
- **i2p.www** --- The I2P project website
- **i2p.syndie** --- Syndie, a distributed forums tool

By convention, the I2P Monotone repository is named `i2p.mtn`. Before
pulling source code from servers, a database for your repository will
need to be initialized. To initialize your local repository, change into
the directory that you want the `i2p.mtn` file and branch directories to
be stored and issue the following command:

- `$ `**`mtn --db="i2p.mtn" db init`**

### Obtaining and deploying developers\' keys

Keys which developers use to commit code are essential for trust
evaluation in Monotone. The other developers\' transport keys are only
required for Monotone server operators. 


Developers\' commit keys are provided GPG-signed [on another
page]().

To import developers\' keys after verifying their authenticity, copy
[all of the keys]() into a new file. Create
this file (e.g. **`keys.txt`**) in the same directory where `i2p.mtn` is
located. Import the keys with the command:

- `$ `**`mtn --db="i2p.mtn" read < keys.txt`**

**Note**: *Never* add keys to **`$HOME/.monotone/keys`** manually.

### Setting up trust evaluation hooks

The default Monotone trust policy is way too lax for our requirements:
every committer is trusted by default. That is not acceptable for I2P
development.

Change into the directory **`$HOME/.monotone`** and open the file
`monotonerc` with a text editor. Copy and paste the following two
functions into this file:



The first function determines an intersection between two sets, in our
case a revision\'s signers and trusted signers.

The second function determines trust in a given revision, by calling the
first function with \"signers\" and \"trusted\" as arguments. If the
intersection is null, the revision is not trusted. If the intersection
is not empty, the revision is trusted. Otherwise, the revision is not
trusted.

More information about Trust Evaluation Hooks can be found in the
[official Monotone
documentation](http://www.monotone.ca/docs/Hooks.html).

### Pulling the `i2p.i2p`, `i2p.www` and `i2p.syndie` branches

I2P is shipped with a pre-configured tunnel pointing to the project
Monotone server. Ensure that the tunnel has been started within
[I2PTunnel](http://127.0.0.1:7657/i2ptunnel) before attempting to pull
the source code from 127.0.0.1:8998.

Enter the directory where you initialized `i2p.mtn`. Depending on
whether you want only I2P sources, or also sources for the I2P website
and Syndie, you can perform the `pull` operation in different ways.

If you only want I2P sources:

- `$ `**`mtn --db="i2p.mtn" -k "" pull "mtn://127.0.0.1:8998?i2p.i2p"`**

If you want all branches:

- `$ `**`mtn --db="i2p.mtn" -k "" pull "mtn://127.0.0.1:8998?i2p.*"`**

If the transfer aborts before completing sucessfully, simply repeating
the pull command will resume the transfer.

Pulling in the above examples is done anonymously by specifying an empty
transport key. If everyone pulls anonymously it will be harder for an
attacker who gains control of the server to selectively provide some
people with tampered data.

### Verifying that trust evaluation works

To verify that trust evaluation works:

Make a backup of your `monotonerc` file.

Modify **`monotonerc`** by setting the trusted_signers variable in the
following way:

 local trusted_signers = {}
 

With **`monotonerc`** configured as above, Monotone will no longer trust
any committers. Confirm this by changing into the directory where
`i2p.mtn` was created and attempt a checkout of the I2P branch:

- `$ `**`mtn --db="i2p.mtn" co --branch="i2p.i2p"`**

A directory named `i2p.i2p` should **not** appear. You should encounter
many error messages like:

 mtn: warning: trust function disliked 1 signers
 of branch cert on revision 523c15f6f50cad3bb002f830111fc189732f693b
 mtn: warning: trust function disliked 1 signers
 of branch cert on revision 8ac13edc2919dbd5bb596ed9f203aa780bf23ff0
 mtn: warning: trust function disliked 1 signers
 of branch cert on revision 8c4dd8ad4053baabb102a01cd3f91278142a2cd1
 mtn: misuse: branch 'i2p.i2p' is empty
 

If you are satisfied with results, restore the backup of `monotonerc`
that was created above. If you didn\'t create a backup as advised,
re-read [Setting up trust evaluation
hooks](#setting-up-trust-evaluation-hooks).

### Checking out a working copy of the latest version

If you already have a branch checked out, skip to the [next
section](#updating-your-working-copy-to-the-latest-version).

Change into the directory where `i2p.mtn` is located. Over there issue:

- \$ **`mtn --db="i2p.mtn" co --branch="i2p.i2p"`**

The checkout should complete without error messages and a directory
named `i2p.i2p` should appear in the current directory. Congratulations!
You have successfully checked out the latest I2P sources, ready to be
compiled.

### Updating your working copy to the latest version

If you haven\'t done this already, pull fresh code from the server to
your local Monotone repository. To accomplish this, change into the
directory where `i2p.mtn` is located and issue:

- \$
 **`mtn --db="i2p.mtn" -k "" pull "mtn://127.0.0.1:8998?i2p.i2p"`**

Now change into your `i2p.i2p` directory, and over there issue:

- \$ **`mtn update`**

As long as there were no errors...Congratulations! You have successfully
updated to the latest I2P sources. They should be ready to compile.

## Operating a Monotone Server

### Obtaining and deploying developers\' transport keys

As a server operator you may want to grant push access to certain
developers.

### Granting push and pull access

By default the Monotone server denies all access.

To grant pull access to all clients, set the following in
`$HOME/.monotone/read-permissions`:

 pattern "*"
 allow "*"

No one will not be able to push code to your server without permission
being explicitly granted. To grant push access:

- Add the name of the user\'s transport key to
 `$HOME/.monotone/write-permissions`, such as

 zzz-transport@mail.i2p
 complication-transport@mail.i2p

 with one key per line.

- Import the transport key(s) into your database. The procedure for
 importing transport keys is the same as for importing commit keys,
 which is described in the section [Obtaining and deploying
 developers\' keys](#obtaining-and-deploying-developers-keys).

### Running Monotone in server mode

A separate database should be used for your Monotone server because
monotone will lock the database while it is served to others. Make a
copy of your development database, then start the server with:

- \$
 **`mtn serve --bind="127.0.0.1:8998" --db="i2p.mtn" --key "myserver-transport@mail.i2p"`**

If your key is protected with a passphrase, Monotone may request the
passphrase when the first client connects. You can work around this by
connecting making the first client connection to your server (or by
clearing the password for your transport key).

For your server to be accessible for others over I2P, you will need to
create a server tunnel for it. Use the \"Standard\" tunnel type and
\"Bulk\" profile.

### Differences under Debian GNU/Linux

Debian (amongst other distributions) has integrated Monotone into their
framework of daemons/services. Although Monotone servers can still be
run \"the ordinary way\" on Debian systems, doing it the \"Debian way\"
may be more straightforward.

Permissions are granted by editing the files
`/etc/monotone/read-permissions` and `/etc/monotone/write-permissions`.
You\'ll also need to edit `/etc/default/monotone` to enable monotone to
start at boot or to customize the host, port, or database location.


