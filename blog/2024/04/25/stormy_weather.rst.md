::: document
::: {#trans .section}
# {% trans -%}
:::

::: {#stormy-weather .section}
# Stormy Weather

{%- endtrans %} .. meta:

::: system-message
System Message: ERROR/3 (`<string>`{.docutils}, line 7)

Unexpected indentation.
:::

``` literal-block
:author: idk
:date: 2024-04-25
:category: release
:excerpt: Stormy Weather
```

{% trans -%} The I2P network is currently under a Denial-of-Service
attack. This attack affects I2P and i2pd but in different ways and is
having a serious effect on network health. Reachability of I2P sites is
badly degraded. {%- endtrans %}

{% trans -%} If you are hosting a service inside I2P and it is hosted on
a Floodfill router, you should consider multihoming the service on a
Floodfill-disabled router to improve reachability. Other mitigations are
being discussed but a long-term, backward-compatible solution is still
being worked on. {%- endtrans %}
:::
:::
