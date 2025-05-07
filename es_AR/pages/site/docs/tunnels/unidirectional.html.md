 Túneles
unidireccionales Noviembre de
2016 0.9.27 

## Información general

Esta página describe los orígenes I2P y el diseño de los túneles
unidireccionales de I2P.

- [Página de la introducción al
 túnel]()
- [Especificación de
 túneles]()
- [Especificación de creación de
 túneles]()
- [Discusión sobre el diseño de
 túnel]()
- [Selección de Par
 (peer)]()
- [Reunión 125
 (\~13:12-13:30)]()

## Revisar

Aunque no estamos al tanto de investigación publicada alguna sobre las
ventajas de túneles unidireccionales, estos parece que hacen más difícil
detectar un patrón de solicitud/respuesta, lo cual es bastante posible
que se detecte sobre un túnel bidireccional. Varias aplicaciones y
protocolos, notablemente HTTP, transfieren datos de esta manera. Hacer
que el tráfico siga la misma ruta hacia su destino y de vuelta puede
ponerlo más fácil para un atacante que sólo disponga de datos tiempo y
de volumen de tráfico para inferir la ruta que está tomando un túnel.
Hacer que la respuesta vuelva a través de otra ruta es razonable que lo
haga más difícil.

Cuando tratamos con un adversario interno o con la mayoría de
adversarios externos, los túneles unidireccionales de I2P exponen como
mucho la mitad de los datos de tráfico que se expondrían con circuitos
bidireccionales simplemente observando los propios flujos - una
solicitud y respuesta HTTP seguiría la misma ruta en Tor, mientras que
en I2P los paquetes que componen la solicitud saldrían a través de uno o
más túneles de salida, y los paquetes que componen la respuesta
retornarían a traves de uno o más túneles de entrada diferentes.

La estrategia de usar dos túneles separados para la comunicación de
entrada y de salida no es la única técnica disponible, y tiene
implicaciones en el anonimato. En el lado positivo, al usar túneles
separados se reducen los datos de tráfico expuestos al análisis de los
participantes en un túnel - por ejemplo, los pares (\`peers´) en un
túnel de entrada desde un navegador web sólo verían el tráfico de un
HTTP GET, mientras que los pares en un túnel de entrada verían la carga
entregada a través del túnel. Con túneles bidireccionales, todos los
participantes tendrían acceso al hecho de que, por ejemplo, 1 KB fuera
enviado en una dirección, y después 100 KB en la otra. En el lado
negativo, usar túneles unidireccionales significa que hay dos conjuntos
de pares (\`peers\`) precisan ser perfilados y fiscalizados, y que se
debe tener una precaución adicional para afrontar el incremento de
velocidad que se ha producido en los ataques de predecesor. El proceso
de depositado (\`pooling\`) y erigido (selección de pares y estrategias
de ordenación) debería minimizar las preocupaciones por los ataques de
predecesor.

## Anonimato

A recent [paper by Hermann and Grothoff]() declared
that I2P\'s unidirectional tunnels \"seems to be a bad design
decision\".

The paper\'s main point is that deanonymizations on unidirectional
tunnels take a longer time, which is an advantage, but that an attacker
can be more certain in the unidirectional case. Therefore, the paper
claims it isn\'t an advantage at all, but a disadvantage, at least with
long-living I2P Sites.

Esta conclusión no está totalmente confirmada en el estudio. Los túneles
unidireccionales mitigan claramente otros ataques y no está claro si es
inteligente sacrificar el riesgo del ataque del estudio por los riesgos
de la arquitectura de túneles bidireccionales.

This conclusion is based on an arbitrary certainty vs. time weighting
(tradeoff) that may not be applicable in all cases. For example,
somebody could make a list of possible IPs then issue subpoenas to each.
Or the attacker could DDoS each in turn and via a simple intersection
attack see if the I2P Site goes down or is slowed down. So close may be
good enough, or time may be more important.

La conclusión está basada en una forma de medir específica de la
importancia de la certeza vs. el tiempo, y esa medida puede estar
equivocada, y es definitivamente discutible, especialmente en el mundo
real con citaciones, órdenes de registro y otros métodos disponibles.

Un análisis completo de las compensaciones de los túneles
unidireccionales vs. bidireccionales está claramente fuera del alcance
del estudio, y no se ha hecho en ningún sitio. Por ejemplo, ¿cómo se
compara este ataque con los numerosos posibles ataques publicados sobre
la red onion? Claramente los autores no han hecho ese análisis, si
pudiese ser posible hacerlo efectivamente.

Tor utiliza túneles bidireccionales y tiene mucha revisión académica.
I2P usa túneles unidireccionales y tiene muy poca revisión. ¿Significa
la falta de estudios defendiendo los túneles unidireccionales que son
una mala elección de diseño, o sólo necesita más estudio? Contra los
ataques de tiempo y los ataques distribuidos para I2P y tor es difícil
defenderse para ambos. El intento de diseño (vea las referencias arriba)
era que los túneles de diseño eran más resistentes a los ataques de
tiempo. Sin embargo, el estudio presenta un tipo diferente de ataque de
tiempo. ¿Es este ataque, innovador, suficiente para calificar la
arquitectura de túneles de I2P (y por lo tanto a I2P al completo) de un
\"mal diseño\", y por implicación, claramente inferior a Tor, o
simplemente es una alternativa de diseño que claramente necesita más
investigación y análisis? Hay otras razones para considerar a I2p
inferior a Tor y a otros proyectos (el pequeño tamaño de la red, falta
de fondos, falta de revisión) ¿pero son los túneles unidireccionales de
verdad una razón?

En resumen, la \"mala decisión de diseño\" parece (ya que el estudio no
califica a los túneles bidireccionales de \"malos\") otra forma de decir
que los túneles \"unidireccionales son inequívocamente inferiores a los
túneles bidireccionales\", aunque esta conclusión no está demostrada en
el estudio.


