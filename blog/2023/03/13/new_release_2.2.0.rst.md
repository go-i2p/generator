::: document
::: {#trans .section}
# {% trans -%}
:::

::: {#i2p-release-2-2-0 .section}
# I2P Release 2.2.0

{%- endtrans %} .. meta:

::: system-message
System Message: ERROR/3 (`<string>`{.docutils}, line 7)

Unexpected indentation.
:::

``` literal-block
:author: idk
:date: 2023-03-13
:category: release
:excerpt: DDoS Mitigations, New Release Maintainer
```

{% trans -%} We have elected to move forward the 2.2.0 release date,
which will be occurring today, March 13, 2023. This release includes a
changes across the NetDB, Floodfill, and Peer-Selection components which
improve the ability of the router to survive DDOS attacks. The attacks
are likely to continue, but the improvements to these systems will help
to mitigate the risk of DDOS attacks by helping the router identify and
de-prioritize routers that appear malicious. {%- endtrans %}

{% trans -%} This release also adds replay protection to the Streaming
subsystem, which prevents an attacker who can capture an encrypted
packet from being able to re-use it by sending it to unintended
recipients. This is a backward-compatible change, so older routers will
still be able to use the streaming capabilities of newer routers. This
issue was discovered and fixed internally, by the I2P development team,
and is not related to the DDOS attacks. We have never encountered a
replayed streaming packet in the wild and do not believe a streaming
replay attack has ever taken place against the I2P network at this time.
{%- endtrans %}

{% trans -%} As you may have noticed, these release notes and the
release itself have been signed by idk, and not zzz. zzz has chosen to
step away from the project and his responsibilities are being taken on
by other team members. As such, the project is working on replacing the
network statistics infrastructure and moving the development forum to
i2pforum.i2p. We thank zzz for providing these services for such a long
time. {%- endtrans %}

{% trans -%} As usual, we recommend that you update to this release. The
best way to maintain security and help the network is to run the latest
release. {%- endtrans %}

**DETAILS**

*Changes*

-   i2psnark: New search feature
-   i2psnark: New max files per torrent config
-   NetDB: Expiration improvements
-   NetDB: More restrictions on lookups and exploration
-   NetDB: Store handling improvements
-   NTCP2: Banning improvements
-   Profiles: Adjust capacity estimates
-   Profiles: Expiration improvements
-   Router: Initial support for congestion caps (proposal 162)
-   Transports: Add inbound connection limiting
-   Tunnels: Refactor and improve peer selection
-   Tunnels: Improve handling of \"probabalistic\" rejections
-   Tunnels: Reduce usage of unreachable and floodfill routers

*Bug Fixes*

-   Docker: Fix graphs not displaying
-   i2psnark: Fix torrents with \'#\' in the name
-   i2psnark standalone: Fix running from outside directory
-   i2psnark standalone: Remove \"Start I2P\" menu item from systray
-   i2ptunnel: Fix typo in HTTPS outproxy hostname
-   i2ptunnel: Interrupt tunnel build if stop button clicked
-   i2ptunnel: Return error message to IRC, HTTP, and SOCKS clients on
    failure to build tunnels
-   NTCP2: Ensure an IPv6 address is published when firewalled and IPv4
    is not
-   Ratchet: Don\'t bundle wrong leaseset with ack
-   Router: Fixes for symmetric NAT errors on \'full cone\' NAT
-   SAM: Interrupt tunnel build if client times out
-   SSU2: Fix rare peer test NPE
-   Sybil: Don\'t blame i2pd publishing ::1
-   Sybil: Memory usage and priority reduction
-   Transports: More IP checks

*Other*

-   Blocklist efficiency improvements
-   Bundles: Identify Win and Mac bundles in version info
-   Console: Identify service installs, revision, and build time in
    version info
-   Console: NetDB search form and tunnels page improvements (advanced
    only)
-   Router: Reduce stats memory usage
-   Tunnels: Reduce \"grace period\"
-   Translation updates

Full list of fixed bugs:
[http://git.idk.i2p/i2p-hackers/i2p.i2p/-/issues?scope=all&state=closed&milestone_title=2.2.0](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/issues?scope=all&state=closed&milestone_title=2.2.0){.reference
.external}
:::
:::
