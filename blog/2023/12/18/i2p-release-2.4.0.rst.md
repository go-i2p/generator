::: document
::: {#trans .section}
# {% trans -%}
:::

::: {#i2p-2-4-0-release-with-congestion-and-netdb-security-improvements .section}
# I2P 2.4.0 Release with Congestion and NetDB Security improvements

{%- endtrans %} .. meta:

::: system-message
System Message: ERROR/3 (`<string>`{.docutils}, line 7)

Unexpected indentation.
:::

``` literal-block
:author: idk
:date: 2023-12-18
:category: release
:excerpt:
```

{% trans -%} Update details {%- endtrans %}
============================================

{% trans -%} This release, I2P 2.4.0, continues our effort to improve
the security and stability of the I2P network. It contains significant
improvements to the Network Database, an essential structure within the
I2P network used for disovering your peers. {%- endtrans %}

{% trans -%} The congestion handling changes will improve network
stability by giving routers the ability to relieve congested peers by
avoiding them. This will help the network limit the effect of tunnel
spam. It will also help the network heal during and after DDoS attacks.
{%- endtrans %}

{% trans -%} The NetDb changes also help secure individual routers and
the applications that use them. Routers can now defend against attackers
by separating the NetDB into multiple \"Sub-DB\'s\" which we use to
prevent information leaks between applications and the router. This also
improves the information available to Java routers about their NetDB
activity and simplifies our support for multihoming applications. {%-
endtrans %}

{% trans -%} Also included are a number of bug fixes and enhancements
across the I2PSnark and SusiMail applications. {%- endtrans %}

{% trans -%} As usual, we recommend that you update to this release. The
best way to maintain security and help the network is to run the latest
release. {%- endtrans %}

**RELEASE DETAILS**

**Changes**

-   i2psnark: Uncomment and fix local torrent file picker
-   NetDB: Lookup handler/throttler fixes
-   Router: Restructure netDb to isolate data recieved as a client from
    data recieved as a router
-   Router: Implement handling and penalties for congestion caps
-   Router: Temporarily ban routers publishing in the future
-   Transports: Disable SSU 1

**Bug Fixes**

-   Addressbook: Workaround for i2p-projekt.i2p etag bug (Gitlab #454)
-   Console: Clear out \"proxy must be running\" status after success
-   Console: Don\'t lose tabs in log messages
-   Console: Fix sidebar not immediately showing results of manual
    update check
-   Console: Fix visibility of radio/checkboxes (light theme)
-   Console: Prevent overflow of sidebar status
-   Debian: Change JRE dependency order (Gitlab #443, Debian #1024461)
-   i2psnark: Increase comment bucket size to reduce duplicates
-   i2psnark: Prevent start-all from within search results erroring
    (Gitlab #445)
-   i2ptunnel: Exempt tunnel name from XSS filter (Gitlab #467)
-   i2ptunnel: Fix gzip footer check in GunzipOutputStream (Gitlab #458)
-   i2ptunnel: Remove nonstandard Proxy-Connection headers (Gitlab #452)
-   NTCP2: Fix updating address on transition to firewalled (Gitlab
    #435)
-   SAM: Fix accept after soft restart (Gitlab #399)
-   SAM: Reset incoming socket if no subsession is matched (Gitlab #456)
-   SSU2: Fix uncaught IAE caused by itags with zero values (Gitlab
    #415)
-   SSU2: Prevent rare IAE in peer test timer (Gitlab #433)
-   Susimail: Dark theme fixes
-   Susimail: Fix binary content-encoding
-   Susimail: Fix incorrect \"previous\" icons
-   Susimail: Fix setting encoding for attachments
-   Susimail: Flush output to fix truncated mails
-   Sybil: Don\'t ban NAT64 addresses
-   Transport: Fix NPE during soft restart (Gitlab #437)
-   UPnP: Fix handing of multiple IGDs
-   UPnP: Fix missing port in Host header causing failures on
    libupnp-based devices

**Other**

-   API 0.9.61
-   Translation updates

[Full list of fixed
bugs](http://%7B%7Bi2pconv('git.idk.i2p')%7D%7D/i2p-hackers/i2p.i2p/-/issues?scope=all&state=closed&milestone_title=2.4.0){.reference
.external}

**SHA256 Checksums:**

``` literal-block
d08db62457d4106ca0e36df3487bdf6731cbb81045b824a003cde38c7e1dfa27  i2pinstall_2.4.0_windows.exe
ef5f3d0629fec292aae15d027f1ecb3cc7f2432a99a5f7738803b453eaad9cad  i2pinstall_2.4.0.jar
30ef8afcad0fffafd94d30ac307f86b5a6b318e2c1f44a023005841a1fcd077c  i2psource_2.4.0.tar.bz2
97be217bf07319a50b6496f932700c3f3c0cceeaf1e0643260d38c9e6e139b53  i2pupdate_2.4.0.zip
8f4a17a8cbadb2eabeb527a36389fd266a4bbcfd9d634fa4f20281f48c486e11  i2pupdate.su3
```
:::
:::
