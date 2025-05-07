 Perfilado y
selección de pares 2024-02 0.9.62 

## NOTE

This page describes the Java I2P implementation of peer profiling and
selection as of 2010. While still broadly accurate, some details may no
longer be correct. We continue to evolve banning, blocking, and
selection strategies to address newer threats, attacks, and network
conditions. The current network has multiple router implementations with
various versions. Other I2P implementations may have completely
different profiling and selection strategies, or may not use profiling
at all.

## Vista general

### Perfiles de los pares

**Peer profiling** is the process of collecting data based on the
**observed** performance of other routers or peers, and classifying
those peers into groups. Profiling does **not** use any claimed
performance data published by the peer itself in the [network
database]().

Los perfiles se usan con dos fines:

1. Para seleccionar pares para enviar nuestro tráfico a través, lo que
 se discute más abajo.
2. Choosing peers from the set of floodfill routers to use for network
 database storage and queries, which is discussed on the [network
 database]() page

### Selección de pares

La **selección de pares** es el proceso de escoger qué routers de la red
queremos para pasar nuestros mensajes a través (o a cuales pares les
pedimos permiso para unir nuestros túneles). Para llevar esto acabo,
llevamos el seguimiento de como funciona cada par (el \"perfil\" del
par) y usamos estos datos para estimar cómo son de rápidos, cuando serán
capaces de aceptar nuestras peticiones y de saber cuando están
sobrecargados o cuando no son capaces de hacer con fiabilidad lo que
acordaron.

Unlike some other anonymous networks, in I2P, claimed bandwidth is
untrusted and is **only** used to avoid those peers advertising very low
bandwidth insufficient for routing tunnels. All peer selection is done
through profiling. This prevents simple attacks based on peers claiming
high bandwidth in order to capture large numbers of tunnels. It also
makes [timing attacks](#timing) more
difficult.

La selección de pares se hace frecuentemente, ya que el ruter mantiene
un gran número de túneles clientes y exploratorios, y la vida de un
túnel es de sólo 10 minutos.

### Información futura

For more information see the paper [Peer Profiling and Selection in the
I2P Anonymous Network]() presented at [PET-CON
2009.1](). See [below](#notes) for notes on minor
changes since the paper was published.

## Perfiles

Each peer has a set of data points collected about them, including
statistics about how long it takes for them to reply to a network
database query, how often their tunnels fail, and how many new peers
they are able to introduce us to, as well as simple data points such as
when we last heard from them or when the last communication error
occurred. The specific data points gathered can be found in the
[code]().

Los perfiles son bastante pequeños, unos pocos KB. Para controlar el uso
de la memoria usada, el tiempo de expiración de los perfiles disminuye
cuando el número de perfiles aumenta. Los perfiles se mantienen en la
memoria hasta que el ruter se apaga, entonces se escriben al disco duro.
Al inicio, los perfiles son leídos para que el ruter no necesite
reiniciar todos los perfiles, permitiendo al ruter integrarse
rápidamente en la red después del arranque.

## Resúmenes de los pares

Aunque los perfiles por sí mismos puede considerarse un resumen del
rendimiento de los pares, para tener una selección efectiva de los pares
partimos cada resumen en cuatro valores simples, indicando la velocidad
del par, su capacidad, cómo de bien está integrado en la red y cuándo
fallan.

### Velocidad

El cálculo de la velocidad se hace simplemente mirando el perfil y
calculando cuantos datos podemos enviar o recibir a través de túnel de
un par durante un minuto. Para esta estimación simplemente mira el
rendimiento en el minuto anterior.

### Capacidad {#capacity}

El cálculo de la capacidad simplemente mira en el perfil y estima el
número de túneles en los que aceptará participar en un periodo de tiempo
dado. Para esta estimación mira cuantos peticiones de construcción de
túneles ha aceptado, denegado y tirado, y cuantos túneles de los
aceptados han fallado después. Las actividades recientes importan más
que las demás, pueden ser incluidas hasta estadísticas de hasta 48 horas
de viejas.

Reconocer y evitar los pares no fiables e inalcanzables es de
importancia crítica. Desafortunadamente, ya que la creación de los
túneles requiere la participación de varios pares, es difícil
identificar positivamente la causa de una petición caída o un fallo en
la prueba. El router asigna una probabilidad de fallo a cada par, y usa
esa probabilidad en el cálculo de la capacidad. Las caídas y los fallos
de prueba pesan mucho más que las denegaciones.

## Organización de los pares

Como se ha mencionado arriba, nos sumergimos en el perfil de cada par
para hacer unos pocos cálculos, y basado en esos cálculos, organizamos
cada par dentro de estos tres grupos - rápido, con capacidad y estándar.

Los grupos no se excluyen mutuamente, y están relacionados entre ellos:

- Un par es considerado de \"alta capacidad\" si los cálculos cumplen
 o exceden la media de todos los pares.
- Un par es considerado \"rápido\" si ya es de \"alta capacidad\", y
 los cálculos de velocidad cumplen o exceden la media de todos los
 pares.
- Un par es considerado \"estándar/normal\" si no es de \"alta
 capacidad\"

These groupings are implemented in the router\'s
[ProfileOrganizer]().

### Límites del tamaño de los grupos

El tamaño de los grupos puede estar limitado.

- El grupo rápido está limitado a 30 pares. Si hubiese más, sólo los
 que tuviesen las mayores velocidades permanecerían en el grupo.
- El grupo de alta capacidad está limitado a 75 pares (incluido el
 grupo rápido). Si hubiese más, sólo los que tuviesen las mayores
 capacidades permanecerían en el grupo.
- El grupo estándar no tiene un límite fijado, pero de alguna forma es
 menor que el número de RouterInfos almacenados en la base de datos
 de la red local. En un ruter activo de la red actual, puede haber
 como 1000 RouterInfoes y 500 perfiles de pares (incluyendo auqellos
 en los grupos rápidos y de alta capacidad)

## Nuevos cálculos y estabilidad

Cada 45 segundos, los resúmenes son re-calculados, y los pares son
recolocados en grupos.

Los grupos tienden a ser bastante estables, esto es, no hay mucha
\"agitación\" en las clasificaciones tras cada nuevo cálculo.

## Selección de pares

Los ruters seleccionan pares de los grupos anteriores para construir
túneles a través de ellos.

### Selección de pares para los túneles cliente

Los túneles cliente se usan para el tráfico de las aplicaciones, como
los proxies HTTP y los servidores web.

Para reducir la propensión a [algunos
ataques](http://blog.torproject.org/blog/one-cell-enough), e incrementar
el rendimiento, los pares para la construcción de los túneles cliente se
eligen aleatoriamente del grupo más pequeño, el cual es el grupo
\"rápido\". No existe una tendencia hacia la selección de pares que
anteriormente hayan participado en un túnel para el mismo cliente.

### Selección de pares para los túneles exploratorios

Los túneles exploratorios son usados para propósitos administrativos del
ruter, como el tráfico de la base de datos de la red y los túneles
cliente de prueba. También son usados para contactar con ruters
anteriormente no contactados, que es por lo que se llaman
\"exploratorios\". Estos túneles son normalmente de bajo ancho de banda.

Los pares para construir los túneles exploratorios son elegidos
normalmente aleatoriamente del grupo estándar. En su lugar, si la tasa
de éxito de esos intentos de construcción es baja comparada con la tasa
de éxito exitosa de construcción, el ruter seleccionará un promedio
balanceado aleatoriamente de pares del grupo de alta capacidad.

Ya que el grupo estándar incluye una gran parte de todos los pares que
el ruter conoce, los túneles exploratorios son construidos esencialmente
a través de una selección aleatoria de todos los pares, hasta que la
tasa de éxito de construcción sea demasiada baja.

### Restricciones

Para prevenir algunos ataques simples, y para mejorar el rendimiento,
existen las siguientes restricciones:

- Dos pares en el mismo espacio de IPs /16 no deben estar en el mismo
 túnel.
- Un par (\`peer\`) puede participar en un máximo de 33% de todos los
 túneles creados por el router.
- Los pares con el ancho de banda extremadamente bajo no son usados.
- Los pares para los que un intento de conexión reciente ha fallado no
 son usados.

### Orden de los pares en los túneles

Peers are ordered within tunnels to to deal with the [predecessor
attack]() [(2008
update)](). More information is on the [tunnel
page](#ordering).

## Trabajo futuro

- Continuar analizando y afinando los cálculos de capacidad y
 velocidad según las necesidades.
- Implementar una estrategia de expulsión más agresiva si se necesita
 para controlar el uso de memoria según crezca la red.
- Evaluar el tamaño de los límites de los grupos
- Usar datos GeoIP para incluir o excluir ciertos pares, si se
 configura

## Notas {#notes}

For those reading the paper [Peer Profiling and Selection in the I2P
Anonymous Network](), please keep in mind the
following minor changes in I2P since the paper\'s publication:

- Todavía no se usa el cálculo de integración
- En el estudio, a los \"grupos\" se les llama \"tiers\"/\"niveles\"
- El nivel \"Fallando\" no se usa más.
- El nivel \"no fallando\" se llama ahora \"estándar\"

## Referencias

- [Perfiles y selección de pares en la red anónima
 I2P](pdf/I2P-PET-CON-2009.1.pdf)
- [Una célula basta](http://blog.torproject.org/blog/one-cell-enough)
- [Entry Guards de
 Tor](https://wiki.torproject.org/noreply/TheOnionRouter/TorFAQ#EntryGuards)
- [Estudio Murdoch
 2007](http://freehaven.net/anonbib/#murdoch-pet2007)
- [Ajustes para
 Tor](http://www.crhc.uiuc.edu/~nikita/papers/tuneup-cr.pdf)
- [Ataques de enrutado de bajo recurso contra
 Tor](http://cs.gmu.edu/~mccoy/papers/wpes25-bauer.pdf)


