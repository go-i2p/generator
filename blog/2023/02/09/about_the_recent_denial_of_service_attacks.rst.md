::: document
::: {#trans .section}
# {% trans -%}
:::

::: {#about-the-recent-denial-of-service-attacks .section}
# About the recent Denial of Service attacks

{%- endtrans %} .. meta:

::: system-message
System Message: ERROR/3 (`<string>`{.docutils}, line 7)

Unexpected indentation.
:::

``` literal-block
:author: idk,sadie
:date: 2023-02-09
:category: release
:excerpt: I2P remains intact with impaired performance
```

{% trans -%} The I2P network is currently being affected by a Denial of
Service attack. The floodfill function of the network has been affected,
resulting in responses being disrupted and tunnel build success rates
dropping. Participants in the network have experienced difficulties
connecting to I2P sites and using I2P services. Mitigation strategies
are being investigated and implemented gradually. {%- endtrans %}

{% trans -%} While the attack has degraded performance, the network
remains intact and usable. Java I2P routers appear to be handling the
issues better than i2pd routers for now. Various mitigations should
begin to appear in dev builds of both Java and C++ routers in the next
week. {%- endtrans %}
:::
:::
