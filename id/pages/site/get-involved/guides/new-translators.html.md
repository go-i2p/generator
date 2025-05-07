 Panduan Penerjemah
Baru Here\'s a very quick guide to
getting started. Note that for both (website/console) there is an **easy
way** using a translation web-site (and requiring nothing else than to
use that) and the **other way** which requires you to set up a
build-environment (installing software etc.).

## How to Translate the Website

Translation of the website is done with .po files. The easiest way by
far to translate the website is to sign up for an account at
[Transifex]() and request to join a
translation team. Alternatively it can be done \"the old way\" as
outlined below.

1. **Preparation**
 1. Come to #i2p-dev on irc and talk to people. Claim the language -
 To make sure other coworkers don\'t bump onto the files you are
 working on, please update the translation status on [this wiki
 page]().
 2. Follow the [new developer\'s guide](),
 including the installation of git and the gettext tools. You
 will need the i2p.www repository. It is not required that you
 sign a dev agreement.
2. **Create files:** If the file for your language does not exist yet:
 1. Run \"`./extract-messages.sh`\" to generate a `messages.pot` in
 the base directory. Edit the header of this file, then run
 \"`./init-new-po.sh locale`\" to generate the file
 `i2p2www/translations/locale/LC_MESSAGES/messages.po`.
 \"`mtn add`\" this file.
 2. Edit `i2p2www/pages/global/lang.html` and add a line for your
 language (copy an existing line).
 3. Add a flag image file to `i2p2www/static/images/flags/` for the
 menu (copy from the router).
3. **Edit files:** Edit
 `i2p2www/translations/locale/LC_MESSAGES/messages.po`. To work with
 .po files efficiently, you may wish to use
 [POEdit](http://www.poedit.net/download.php)
4. **Git Workflow:** You can then add all new and changed files to your
 next commit using `git add .` (or specify which files instead of the
 dot). Please note the suggested workflow for git on our git-page.
5. Repeat. Check in often. Don\'t wait until it is perfect.

## How to Translate the Router Console

The easiest way by far to translate the router console is to sign up for
an account at [Transifex]() and request to
join a translation team. Alternatively it can be done \"the old way\" as
outlined below.

1. **Preparation**
 1. Come to #i2p-dev on irc and talk to people. Claim the language -
 To make sure other coworkers don\'t bump onto the files you are
 working on, please update the translation status on [this wiki
 page]().
 2. Follow the [new developer\'s guide](),
 including the installation of git and the gettext tools. You
 will need the i2p.i2p repository.
 3. Generate your own gpg key and sign the dev agreement.
2. Before starting a console translation, better help translate some
 i2p webpages first. At least an i2p homepage in your language would
 be great.
3. **What to translate:** There are about 15 files in the i2p.i2p
 branch that needs translation:
 - `installer/resources/readme/readme_xx.html`
 - `installer/resources/initialNews/initialNews_xx.xml`
 - `apps/routerconsole/locale/messages_xx.po`
 - `installer/resources/proxy/*_xx.ht` (about 9 files)
 - `apps/routerconsole/jsp/help_xx.jsp`
 - `installer/resources/I2P Site.help/help/index_xx.html`
 - `apps/i2ptunnel/locale/messages_xx.po`
 - `apps/i2psnark/locale/messages_xx.po`
 - `apps/susidns/locale/messages_xx.po`

 Where xx is your language code like fr/de/ch/zh/\... There may be or
 may not be files with your lang code. If not, you can create your
 own. by copying and renaming other language files you know with your
 own lang code.
4. **Create files:** If the file for your language does not exist yet,
 copy another language file to a new file `foo_xx.bar` for your
 language. Then \"`mtn add`\" the file. After creating a .po file,
 edit the headers. Then run \"`ant distclean poupdate`\".
5. **Start to work:** Edit the HTML files with any text editor. Be sure
 not to use an editor in HTML mode that reformats everything. To work
 with .po files efficiently, you may wish to use
 [POEdit](http://www.poedit.net/download.php)
6. **Git Workflow:** You can then add all new and changed files to your
 next commit using `git add .` (or specify which files instead of the
 dot). Please note the suggested workflow for git on our git-page.
7. Repeat. Check in often. Don\'t wait until it is perfect.

As you can see, it\'s not that difficult. If you have questions about
the meaning of the terms in the console, ask in `#i2p-dev` on IRC.

## FAQ

**Q: Why do I have to install git, Java, jsp, learn about .po files and
html, etc.? Why can\'t I just do a translation and email it to you?**

**A: You do not / Several reasons:**

- First of all: you don\'t have to, you can translate via Transifex
 (aka \"using a web-site to translate\"). Request to join a
 translation team [here](). Aside from
 that \...
- We don\'t have anybody who has time to accept manual contributions
 and submit them to our source control system on your behalf. Even if
 we did, it doesn\'t scale.
- Maybe you are thinking translation is a one-step process. It isn\'t.
 You can\'t do it all at once. You will make mistakes. You need to
 test it and tweak it to make it look right *before* you submit it.
 Developers will update or add to the English text, thus requiring a
 translation update.
- Having translators use a source control system directly provides
 authentication and accountablility - we know who is doing what, and
 we can track changes, and revert them if necessary.
- .po files are not difficult. If you don\'t want to work directly
 with them, we recommend \'poedit\'.
- HTML files are not difficult. Just ignore the html stuff and
 translate the text.
- Installing and using git is not that difficult. Several of the
 translators and other contributors to I2P are non-programmers, and
 they use git regularly. Git is simply a source control system, it is
 not about \"coding\".
- Our items to translate are not \"documents\". They are html files
 and po files, with a specific format and character encoding (UTF-8)
 that must be maintained, and not corrupted by email programs or
 other methods of transfer.
- We looked at \'pootle\' as a front-end for translators. It didn\'t
 work well, needed an administrator, and a pootle-based process would
 suffer from a number of the above flaws.

**In summary:** Yes, we know it is somewhat of a hurdle to get started.
It\'s really the only possible way we can do it. Give it a try, it
really isn\'t that hard.

## More Information

The #i2p-dev channel on IRC, or the [translation forum on ](http:///forums/14).


