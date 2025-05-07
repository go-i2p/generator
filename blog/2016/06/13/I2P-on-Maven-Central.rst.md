::: document
::: {#trans .section}
# {% trans -%}
:::

::: {#i2p-on-maven-central .section}
# I2P on Maven Central

{%- endtrans %}

{% trans -%} We\'re nearly half-way into the APIs month of Summer Dev,
and making great progress on a number of fronts. I\'m happy to announce
that the first of these is complete: the I2P client libraries are now
available on Maven Central! {%- endtrans %}

{% trans -%} This should make it much simpler for Java developers to use
I2P in their applications. Instead of needing to obtain the libraries
from a current install, they can simply add I2P to their dependencies.
Upgrading to new versions will similarly be much easier. {%- endtrans %}

{% trans -%} How to use them =============== {%- endtrans %}

{% trans -%} There are two libraries that you need to know about: {%-
endtrans %}

-   `net.i2p:i2p`{.docutils .literal} - The core I2P APIs; you can use
    these to send individual datagrams.
-   `net.i2p.client:streaming`{.docutils .literal} - A TCP-like set of
    sockets for communicating over I2P.

{% trans -%} Add one or both of these to your project\'s dependencies,
and you\'re good to go! {%- endtrans %}

::: {#gradle .section}
## Gradle

``` literal-block
compile 'net.i2p:i2p:0.9.26'
compile 'net.i2p.client:streaming:0.9.26'
```
:::

::: {#maven .section}
## Maven

``` literal-block
<dependency>
    <groupId>net.i2p</groupId>
    <artifactId>i2p</artifactId>
    <version>0.9.26</version>
</dependency>
<dependency>
    <groupId>net.i2p.client</groupId>
    <artifactId>streaming</artifactId>
    <version>0.9.26</version>
</dependency>
```

{% trans -%} For other build systems, see the Maven Central pages for
the
[core](http://search.maven.org/#artifactdetails%7Cnet.i2p%7Ci2p%7C0.9.26%7Cjar){.reference
.external} and
[streaming](http://search.maven.org/#artifactdetails%7Cnet.i2p.client%7Cstreaming%7C0.9.26%7Cjar){.reference
.external} libraries. {%- endtrans %}

{% trans -%} Android developers should use the [I2P Android client
library](http://search.maven.org/#artifactdetails%7Cnet.i2p.android%7Cclient%7C0.8%7Caar){.reference
.external}, which contains the same libraries along with
Android-specific helpers. I\'ll be updating it soon to depend on the new
I2P libraries, so that cross-platform applications can work natively
with either I2P Android or desktop I2P. {%- endtrans %}

{% trans -%} Get hacking! ============ {%- endtrans %}

{% trans -%} See our [application
development](%7B%7Bsite_url('get-involved/develop/applications')%7D%7D#start){.reference
.external} guide for help getting started with these libraries. You can
also chat with us about them in #i2p-dev on IRC. And if you do start
using them, let us know what you\'re working on with the hashtag
[#I2PSummer](https://twitter.com/hashtag/I2PSummer){.reference
.external} on Twitter! {%- endtrans %}
:::
:::
:::
