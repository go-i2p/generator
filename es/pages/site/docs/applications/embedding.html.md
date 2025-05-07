 Incrustando I2P en
su aplicación 2023-01
2.1.0 

## Vista general

Esta página trata acerca del empaquetamiento del binario completo del
router I2P junto a su aplicación. No trata sobre escribir una aplicación
para que funcione con I2P (tanto empaquetándola como de forma externa).
However, many of the guidelines may be useful even if not bundling a
router.

Montones de proyectos están empaquetando, o discutiendo acerca de
empaquetar, I2P. Esto es estupendo si se hace bien. Si se hace mal,
podría causar un verdadero daño a su red. El router I2P es complejo, y
puede ser un reto ocultar toda la complejidad a sus usuarios. Esta
página trata algunas directrices técnicas.

Most of these guidelines apply equally to Java I2P or i2pd. However,
some guidelines are specific to Java I2P and are noted below.

### Hable con nosotros

Inicie un debate. Estamos aquí para ayudar. Las aplicaciones que
incrustan I2P son las oportunidades más prometedoras - y excitantes -
para nosotros, de hacer crecer la red y mejorar el anonimato para todos.

### Elija su router I2P sabiamente

Si su aplicación está escrita en Java o Scala, es una elección fácil -
use el router I2P Java. Si lo está en C/C++, recomendamos i2pd. El
desarrollo de i2pcpp se ha detenido. Para aplicaciones en otros idiomas,
lo mejor es usar SAM, o BOB, o SOCKS, y empaquetar el router I2P Java
como un proceso aparte. Algunas de las siguientes sólo se aplican al
router I2P Java.

### Licenciamiento

Asegúrese de cumplir con los requerimientos de la licencia del software
que está empaquetando.

## Configuration

### Verifique la configuración por defecto

Una configuración por defecto correcta es crucial. La mayoría de
usuarios no cambiará la configuración predeterminada.

Algunas configuraciones predeterminadas importantes a revisar: Ancho de
banda máximo, cantidad y longitud de túneles, número máximo de túneles
participantes. Esto depende en gran medida del ancho de banda esperado y
los patrones de uso de su aplicación.

Configure suficiente ancho de banda y túneles para permitir contribuir a
la red a sus usuarios. Considere deshabilitar I2CP (protocolo cliente de
I2P), ya que probablemente no lo necesitará y entraría en conflicto con
cualquier otra instancia de I2P en marcha. Mire también en la
configuración para deshabilitar la fulminación (kill) de la JVM al
salir, por ejemplo.

### Consideraciones de tráfico participante

Podría ser tentador para usted deshabilitar el tráfico partipante. Hay
varias formas de hacer esto (modo oculto, establecer el nº máximo de
túneles a 0, establecer el ancho de banda compartido por debajo de 12
KBytes/seg). Sin tráfico participante, no tiene que preocuparse por que
se efectúe un cierre ordenado, sus usuarios no ven el uso de ancho de
banda no generado por ellos mismos, etc. Sin embargo, hay montones de
razones por las que debería permitir túneles participantes.

Lo primero de todo, el router I2P no funciona tan bien si no tiene una
oportunidad de \"integrarse\" con la red, algo a lo que otros
contribuyen tremendamente estableciendo túneles a través de usted.

En segundo lugar, más del 90% de los routers I2P en la red actual
permiten tráfico participante. Es la configuración por defecto en el
router I2P Java. Si su aplicación no enruta para otros y se vuelve
realmente popular, entonces es una sanguijuela (leech) en la red, y
perturba el equilibrio que tenemos ahora. Si su impacto se vuelve
realmente grande, entonces nos convertimos en Tor, y pasamos nuestro
tiempo rogando a la gente que habilite la repetición de tráfico.

En tercer lugar, el tráfico participante es tráfico de cobertura y
contribuye al anonimato de sus usuarios.

Le recomendamos firmemente que no deshabilite el tráfico participante de
forma predeterminada. Si hace esto y su aplicación se vuelve
inmensamente popular, podría fracturar la red.

### Persistencia

You must save the router\'s data (netdb, configuration, etc.) between
runs of the router. I2P does not work well if you must reseed each
startup, and that\'s a huge load on our reseed servers, and not very
good for anonymity either. Even if you bundle router infos, I2P needs
saved profile data for best performance. Without persistence, your users
will have a poor startup experience.

There are two possibilities if you cannot provide persistence. Either of
these eliminates your project\'s load on our reseed servers and will
significantly improve startup time.

1\) Set up your own project reseed server(s) that serve much more than
the usual number of router infos in the reseed, say, several hundred.
Configure the router to use only your servers.

2\) Bundle one to two thousand router infos in your installer.

Also, delay or stagger your tunnel startup, to give the router a chance
to integrate before building a lot of tunnels.

### Configurabilidad

Proporcione a sus usuarios una forma de cambiar los valores de las
configuraciones importantes. Comprendemos que probablemente querrá
ocultar la mayoría de la complejidad de I2P, pero es importante mostrar
algunas configuraciones básicas. Además de las configuraciones por
defecto anteriores, algunas configuraciones de red tales como UPnP o
IP/puerto pueden ser útiles.

### Consideraciones de routers I2P de inundación (floodfill)

Por encima de un cierto valor de ancho de banda, y respondiendo a otros
criterios de salubridad, su router I2P se convertirá en router I2P de
inundación (floodfill), lo que puede causar un gran incremento del
número de conexiones y del uso de memoria (al menos con el router I2P
Java). Piense en si eso es aceptable. Puede deshabilitar la
característica floodfill, pero después sus usuarios más rápidos no
estarán contribuyendo todo lo que podrían. También depende de la tiempo
medio de ejecución continuada de su aplicación.

### Resembrado

Decida si va a empaquetar las informaciones de los routers I2P (router
infos) o si va a usar nuestros nodos de resembrado. La lista de nodos de
resembrado Java está en el código fuente, así que si se mantiene
actualizado, la lista de nodos también lo estará. Esté alerta ante un
posible bloqueo por parte de gobiernos hostiles.

### Use Shared Clients

Java I2P i2ptunnel supports shared clients, where clients may be
configured to use a single pool. If you require multiple clients, and if
consistent with your security goals, configure the clients to be shared.

### Limit Tunnel Quantity

Specify tunnel quantity explicitly with the options `inbound.quantity`
and `outbound.quantity`. The default in Java I2P is 2; the default in
i2pd is higher. Specify in the SESSION CREATE line using SAM to get
consistent settings with both routers. Two each in/out is sufficient for
most low-to-medium bandwidth and low-to-medium fanout applications.
Servers and high-fanout P2P applications may need more. See [this forum
post](http://zzz.i2p/topics/1584) for guidance on calculating
requirements for high-traffic servers and applications.

### Specify SAM SIGNATURE_TYPE

SAM defaults to DSA_SHA1 for destinations, which is not what you want.
Ed25519 (type 7) is the correct selection. Add SIGNATURE_TYPE=7 to the
DEST GENERATE command, or to the SESSION CREATE command for
DESTINATION=TRANSIENT.

### Limit SAM Sessions

Most applications will only need one SAM session. SAM provides the
ability to quickly overwhelm the local router, or even the broader
network, if a large number of sessions are created. If multiple
sub-services can use a single session, set them up with a PRIMARY
session and SUBSESSIONS (not currently supported on i2pd). A reasonable
limit to sessions is 3 or 4 total, or maybe up to 10 for rare
situations. If you do have multiple sessions, be sure to specify a low
tunnel quantity for each, see above.

In almost no situation should you require a unique session
per-connection. Without careful design, this could quickly DDoS the
network. Carefully consider if your security goals require unique
sessions. Please consult with the Java I2P or i2pd developers before
implementing per-connection sessions.

### Reduzca el uso de recursos de red

Note that these options are not currently supported on i2pd. These
options are supported via I2CP and SAM (except delay-open, which is via
i2ptunnel only). See the I2CP documentation (and, for delay-open, the
i2ptunnel configuration documentation) for details.

Considere configurar los túneles de su aplicación a retardar-apertura
(hasta necesitarlos), reducir-en-inactividad y/o cerrar-en-inactividad.
Esto es algo directo si está usando i2ptunnel, pero tendrá que
implementar algo de esto usted mismo si está usando I2CP directamente.
Vea i2psnark para código que reduzca el número de túneles y cierre
después el túnel, incluso en presencia de cierta actividad DHT (tabla de
hash distribuida) en segundo plano.

## Life Cycle

### Actualizabilidad

Incluya una característica de auto-actualización si de algún modo es
posible, o al menos de auto-notificación de nueva versión. Nuestro mayor
temor es un enorme número de routers I2P ahí fuera que no se puedan
actualizar. Tenemos en torno a 6-8 versiones al año del router I2P Java,
y es crítico para la salud de la red que los usuarios se mantengan al
día. Normalmente tenemos más del 80% de la red en la última versión tras
6 semanas de la publicación de la versión, y nos gustaría continuar así.
No tiene que preocuparse de deshabilitar la función integrada de
auto-actualización del router I2P, ya que ese código está en la consola
de este, la cual presumiblemente no está empaquetando.

### Despliegue

Elabore un plan de despliegue gradual. No empuje a toda la red a la vez.
Actualmente tenemos aproximadamente 25K usuarios únicos al día y 40K
únicos al mes. Probablemente podemos manejar un crecimiento de 2-3X por
año sin demasiados problemas. Si anticipa una escalada más rápida que
esa, - O - la distribución del ancho de banda (o la del tiempo de
actividad o cualquier otro rasgo relevante) de su base de usuarios es
significativamente diferente a la de nuestra base de usuarios actual,
verdaderamente debemos tener una charla. Cuanto más grandes sean sus
planes de crecimiento, más importantes serán el resto de cosas en esta
lista de comprobación.

### Diseñe por, e incite a, tiempos de actividad largos

Explique a sus usuarios que I2P logra su mejor funcionamiento si se
mantiene en ejecución. Pueden pasar varios minutos tras el inicio antes
de que funcione bien, e incluso más tras la primera instalación. Si su
tiempo medio en activo es menos de una hora, I2P probablemente es una
mala solución.

## User Interface

### Muestre el estado

Proporcione alguna indicación al usuario de que los túneles de la
aplicación están listos. Aliente a tener paciencia.

### Cierre ordenado

Si es posible, retrase el cierre hasta que sus túneles participantes
expiren. No deje que sus usuarios rompan los túneles fácilmente, o al
menos pídales que confirmen.

### Educación y Donación

Estaría bien si provee a sus usuarios enlaces para conocer más acerca de
I2P y para donar.

### Opción para router I2P externo

Dependiendo de su base de usarios y la aplicación, puede ser útil
proporcionar una opción o un paquete aparte para usar un router I2P
externo.

## Other Topics

### Uso de otros servicios comunes

Si planea usar un enlace a otros servicios comunes de I2P (suscripciones
(feeds) de noticias, suscripciones a hosts.txt, trackers (bittorrent),
proxys de salida, etc.), asegúrese de que no está sobrecargándolos, y
hable con la gente que los ejecuta para asegurarse de que no les está
perjudicando.

### Tiempo / Problemas NTP

Note: This section refers to Java I2P. i2pd does not include an SNTP
client.

I2P incluye un cliente SNTP. I2P requiere la hora correcta para operar.
Compensará un reloj de sistema desfasado, pero esto puede retrasar el
inicio. Puede deshabilitar las peticiones SNTP de I2P, pero no se
aconseja esto a menos que su aplicación se asegure de que el reloj de
sistema está correcto.

### Escoja Qué empaqueta y Cómo

Note: This section refers to Java I2P only.

At a minimum you will need i2p.jar, router.jar, streaming.jar, and
mstreaming.jar. You may omit the two streaming jars for a datagram-only
app. Some apps may need more, e.g. i2ptunnel.jar or addressbook.jar.
Don\'t forget jbigi.jar, or a subset of it for the platforms you
support, to make the crypto much faster. Java 7 or higher is required to
build. If you\'re building Debian / Ubuntu packages, you should require
the I2P package from our PPA instead of bundling it. You almost
certainly do not need susimail, susidns, the router console, and
i2psnark, for example.

The following files should be included in the I2P installation
directory, specified with the \"i2p.dir.base\" property. Don\'t forget
the certificates/ directory, which is required for reseeding, and
blocklist.txt for IP validation. The geoip directory is optional, but
recommended so the router can make decisions based on location. If
including geoip, be sure to put the file GeoLite2-Country.mmdb in that
directory (gunzip it from installer/resources/GeoLite2-Country.mmdb.gz).
The hosts.txt file may be necessary, you may modify it to include any
hosts your application uses. You may add a router.config file to the
base directory to override initial defaults. Review and edit or remove
the clients.config and i2ptunnel.config files.

Los condicionantes de la licencia pueden requerir que incluya el fichero
LICENSES.txt y el directorio de licencias.

- Puede que también quiera empaquetar un fichero hosts.txt.
- Be sure to specify a bootclasspath if you are compiling Java I2P for
 your release, rather than taking our binaries.

### Consideraciones sobre Android

Note: This section refers to Java I2P only.

Nuestra aplicación de router I2P para Android puede ser compartida por
múltiples clientes. Si no está instalada, se le indicará al usuario
cuando inicie una aplicación cliente.

Algunos desarrolladores han expresado preocupación acerca de que esto
supone una pobre experiencia de usuario, y que desean insertar el router
I2P en sus aplicaciones. Tenemos una librería de servicio del router I2P
para Android en nuestra hoja de ruta, que podría facilitar la inserción.
Se precisa más información.

Si requiere asistencia, por favor, contacte con nosostros.

### Jars de Maven

Note: This section refers to Java I2P only.

Tenemos un número limitado de nuestros jars en [Maven
Central](http://search.maven.org/#search%7Cga%7C1%7Cg%3A%22net.i2p%22).
Hay numerosos tickets de trac para que resolvamos, que mejorarán y
expandirán los jars publicados en Maven Central.

Si requiere asistencia, por favor, contacte con nosostros.

### Consideraciones de datagrama (DHT)

Si su aplicación está usando datagramas I2P, ej. para una DHT (tabla de
hashes distribuida), hay montones de opciones avanzadas disponibles para
reducir le tráfico de control e incrementar la fiabilidad. Esto puede
llevar algún tiempo y experimentación para lograr que funcione bien.
Tenga en cuenta los equilibrios tamaño/fiabilidad. Hable con nosotros
para obtener ayuda. Es posible - y está recomendado - usar datagramas y
transporte streaming para el mismo destino. No cree destinos separados
para esto. No trate de almacenar sus datos sin relación en los DHTs
existentes en la red (iMule, bote, bittorrent, y el router I2P).
Construya el suyo propio. Si está integrando nodos semilla en el código,
recomendamos que incluya varios.

### Outproxies

I2P outproxies to the clearnet are a limited resource. Use outproxies
only for normal user-initiated web browsing or other limited traffic.
For any other usage, consult with and get approval from the outproxy
operator.

### Marketing colaborativo

Trabajemos juntos. No espere hasta que esté hecho. Denos su
identificador de Twitter y comience a twitear acerca de ello,
devolveremos el favor.

### Malware

Por favor, no use I2P para el mal. Podría causar un gran daño tanto a
nuestra red como a nuestra reputación.

### Únase a nosotros

This may be obvious, but join the community. Run I2P 24/7. Start an I2P
Site about your project. Hang out in IRC #i2p-dev. Post on the forums.
Spread the word. We can help get you users, testers, translators, or
even coders.

## Examples

### Ejemplos de la aplicación

Puede que desee instalar y jugar con la aplicación I2P Android, y echar
un vistazo a su código en busca de un ejemplo de aplicación que
empaqueta el router I2P. Vea lo que exponemos al usuario y lo que
ocultamos. Mire la máquina de estado que usamos para iniciar y detener
el router I2P. Otros ejemplos son: Vuze, la aplicación Nightweb Android,
iMule, TAILS, iCloak, y Monero.

### Ejemplo de código

Note: This section refers to Java I2P only.

Nada de lo anterior le cuenta en realidad cómo escribir su código para
empaquetar el router I2P Java, así que a continuación tiene un breve
ejemplo.

 import java.util.Properties;
 import net.i2p.router.Router;

 Properties p = new Properties();
 // add your configuration settings, directories, etc.
 // where to find the I2P installation files
 p.addProperty("i2p.dir.base", baseDir);
 // where to find the I2P data files
 p.addProperty("i2p.dir.config", configDir);
 // bandwidth limits in K bytes per second
 p.addProperty("i2np.inboundKBytesPerSecond", "50");
 p.addProperty("i2np.outboundKBytesPerSecond", "50");
 p.addProperty("router.sharePercentage", "80");
 p.addProperty("foo", "bar");
 Router r = new Router(p);
 // don't call exit() when the router stops
 r.setKillVMOnEnd(false);
 r.runRouter();

 ...

 r.shutdownGracefully();
 // will shutdown in 11 minutes or less

Este código es para el caso en que su aplicación inicia el router I2P,
como en nuestra aplicación Android. También podría disponer que el
router I2P inicie la aplicación mediante los ficheros clients.config e
i2ptunnel.config, junto con las aplicaciones web Jetty, tal como se hizo
en nuestros paquetes Java. Como siempre, la gestión del estado es la
parte difícil.

See also: [the Router
javadocs](http:///net/i2p/router/Router.html).


