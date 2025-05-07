::: document
::: {#trans .section}
# {% trans -%}
:::

::: {#i2p-release-2-2-1 .section}
# I2P Release 2.2.1

{%- endtrans %} .. meta:

::: system-message
System Message: ERROR/3 (`<string>`{.docutils}, line 7)

Unexpected indentation.
:::

``` literal-block
:author: idk
:date: 2023-04-12
:category: release
:excerpt: Packaging Fixes
```

{% trans -%} After the I2P 2.2.0 release, which was moved forward to
accelerate mitigations for the DDOS attacks, we learned about a few
developing issues which made it necessary to build and release new
packages. This release fixes an issue within Ubuntu Lunar and Debian Sid
where the router console was inaccessible using an updated version of
the jakarta package. Docker packages were not reading arguments
correctly, resulting in inaccessible configuration files. This issue has
also been resolved. The docker container is now also compatible with
Podman. {%- endtrans %}

{% trans -%} This release syncs translations with transifex and updates
the GeoIP database. {%- endtrans %}

{% trans -%} As usual, we recommend that you update to this release. The
best way to maintain security and help the network is to run the latest
release. {%- endtrans %}

**DETAILS**

*Changes*

-   Fix missing Java options in docker/rootfs/startapp.sh
-   Detect when running in Podman instead of regular Docker
-   Update Tor Browser User-Agent String
-   Update local GeoIP database
-   Remove invalid signing keys from old installs
-   Update Tomcat version in Ubuntu Lunar and Debian Sid

Full list of fixed bugs:
[http://git.idk.i2p/i2p-hackers/i2p.i2p/-/issues?scope=all&state=closed&milestone_title=2.2.1](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/issues?scope=all&state=closed&milestone_title=2.2.1){.reference
.external}
:::
:::
