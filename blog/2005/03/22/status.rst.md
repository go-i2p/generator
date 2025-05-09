::: {#i2p-status-notes-for-2005-03-22 .document}
# I2P STATUS NOTES FOR 2005-03-22 {.title}

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    Hi y'all, quick status update

    * Index
    1) 0.5.0.3
    2) batching
    3) updating
    4) ???

    * 0.5.0.3

    The new release is out and about, and most of y'all have upgraded
    fairly quickly - thanks!  There were some bugfixes to various
    issues, but nothing revolutionary - the biggest part was dropping
    0.5 and 0.5.0.1 users off the net.  I've been tracking the net's
    behavior since then, digging through what's going on, and while
    there has been some improvement, there are still some things that
    need to get sorted out.

    There'll be a new release in the next day or two with a bugfix for
    an issue that no one has run into yet, but that breaks the new
    batching code.  There will also be some tools for automating the
    update process according to the user's preferences, along with other
    minor things.

    * batching

    As I mentioned in my blog, there's room for dramatically reducing
    the bandwidth and message count required on the net by doing some
    very simple batching of tunnel messages - rather than putting each
    I2NP message, regardless of size, in a tunnel message of its own,
    by adding in a brief delay we can bundle up to 15 or more within
    a single tunnel message.  The biggest gains there will occur with
    services that use small messages (such as IRC), while large file
    transfers will not be affected by this much.  The code to perform
    the batching has been implemented and tested, but unfortunately
    there's a bug on the live net which would cause all but the first
    I2NP message within a tunnel message to be lost.  Thats why we're
    going to have an interim release with that fix in it, followed by
    the batching release a week or so after that.

    * updating

    In this interim release, we're going to be shipping some of the
    oft discussed 'autoupdate' code.  We've got the tools to
    periodically check for authentic update announcements, download
    the update either anonymously or not, and then either install it
    or simply display a notice on the router console telling you that
    its ready and waiting for installation.  The update itself will
    now use smeghead's new signed update format which is essentially
    the update plus a DSA signature.  The keys used to verify that
    signature will be bundled with I2P, as well as configurable on
    the router console.

    The default behavior will be to simply periodically check for update
    announcements but not to act on them - just to display a one-click
    "Update now" feature on the router console.  There will be lots of
    other scenarios for different user needs, but they'll hopefully all
    be accounted for through a new configuration page.

    * ???

    I'm feeling a bit under the weather, so the above doesn't really go
    into all the detail about whats up.  Swing on by the meeting and
    fill in the gaps :)

    Oh, as an aside, I'll be pushing out a new PGP key for myself in the
    next day or two as well (since this one expires shortly...), so keep
    an eye out.

    =jr
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1.2.4 (GNU/Linux)

    iD8DBQFCQIW+GnFL2th344YRAj03AKCAwDNl6Dr/4Xi6l9x4kOhw8YIkEwCglfFc
    98JQv3aXNdaBiA65c5DP8c8=
    =qfoJ
    -----END PGP SIGNATURE-----
:::
