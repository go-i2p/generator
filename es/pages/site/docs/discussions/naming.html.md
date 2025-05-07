 Discusión de
nombres 

NOTE: The following is a discussion of the reasons behind the I2P naming
system, common arguments and possible alternatives. See [the naming
page]() for current documentation.

## Alternativas descartadas

Los nombres dentro de I2P han sido un tema a menudo debatido desde el
principio mismo, con defensores de todas las posibilidades del espectro.
Sin embargo, dada la demanda inherente a I2P de comunicaciones seguras y
operaciones descentralizadas, el sistema de nombres tradicional
estilo-DNS está claramente desestimado, ya que son sistemas de voto
donde la \"mayoría manda\".

I2P no promociona el uso de servicios tipo-DNS, ya que el daño hecho al
secuestrar un sitio puede ser tremedo - y los destinos inseguros no
tienen valor. El propio DNSsec aún se respalda sobre los registradores y
las autoridades de certificados, mientras que con I2P las solicitudes
enviadas a un destino no pueden ser interceptadas, o la respuesta
falseada (\`spoofed\`), ya que están cifradas hasta recibir las claves
públicas del destino, y un destino en si mismo es sólo un par de claves
públicas y un certificado. Por otra parte, los sistemas estilo-DNS
permiten a cualquiera de los servidores de nombres en la ruta de la
consulta, montar sencillos ataques de denegación de servicio (DoS) y de
falsificación (\`spoofing\`). Añadir un certificado autentificando las
respuestas como firmadas por alguna autoridad centralizada de
certificados podría solventar muchos de los problemas con servidores de
nombres hostiles, pero también dejaría abiertos los ataques de respuesta
así como los ataques de autoridades de certificados hostiles.

El estilo de voto de nombres también es peligroso, especialmente dada la
efectividad de ataques Sybil en sistemas anónimos - el atacante
simplemente puede crear arbitrariamente un alto número de pares
(\`peers\`) y \"votar\" con cada uno para conquistar un determinado
nombre. Métodos prueba-de-trabajo pueden usarse para hacer la identidad
no-gratuita, pero al crecer la red, la carga necesaria para contactar
con todos para realizar una votación en línea no es plausible, o si no
se consulta a la red completa diferentes grupos de respuestas pueden ser
alcanzables.

Sin embargo, como sucede con Internet, I2P está manteniendo el diseño y
las operaciones de un sistema de nombres fuera de la capa de
comunicación (al estilo-IP). La librería de nombres empaquetada incluye
una interfaz sencilla de proveedor de servicios a la que los [sistemas
de nombres alternativos](#alternatives) pueden enchufarse, permitiendo a
los usuarios finales dirigir la clase de compromisos de equilibrio con
los nombres que ellos prefieran.

## Discussion

Vea también [Nombres: descentralizados, seguros, con-significado-humano:
escoja
dos](http://wayback.archive.org/web/20120204172516/http://zooko.com/distnames.html).

### Comments by jrandom

(adaptado desde un post en el antiguo Syndie, 26 de noviembre de 2005)

P: ¿Qué hacer si algunos servidores no están de acuerdo con una de las
direcciones, y si algunas de las direcciones están funcionando y otras
no? ¿Quién es la fuente correcta de un nombre?

R: Tú no. En realidad esta es una diferencia crítica entre los nombres
en I2P y como funciona DNS - los nombres en I2P son legibles por
humanos, seguros, pero **no globalmente únicos**. Esto es así por
diseño, y una parte inherente de nuestra necesidad de seguridad.

Si yo pudiese convencerle de alguna forma de cambiar la destinación
asociada a algún nombre, yo habría \"tomado control\" de la web, y esto
no es aceptable bajo ninguna circunstancia. En su lugar, lo que hacemos
es hacer que los nombres sean **únicos localmente**: son lo que *usted*
normalmente llamaría un web, al igual que puede llamar a las cosas como
desea cuando las añade los favoritos de su navegador, o a su lista de
amigos de su cliente de mensajería. Aquél al que llama \"jefe\" puede
ser alguien llamado \"Sally\".

Los nombres no serán, nunca, legibles por humanos con-total-certeza, ni
globalmente únicos.

### Comments by zzz

Lo siguiente, desde el sitio de zzz, es un compendio de varias quejas
comunes acerca del sistema de nombres de I2P.

- **Ineficiencia:** El fichero hosts.txt completo se descarga (si ha
 cambiado, ya que eepget usa la ETag (etiqueta de entidad HTTP) y las
 últimas cabeceras modificadas). Ahora ocupa alrededor de 400KB para
 casi 800 servidores.

 Cierto, pero esto no es mucho tráfico en el contexto de I2P, que en
 si mismo es salvajemente ineficiente (bases de datos inundadas,
 enorme tráfico de control por la encriptación y tráfico por esquemas
 de relleno, enrutado ajo (\`garlic\`), etc.). Si usted descargó un
 fichero hosts.txt desde alguien cada 12 horas, esto hace una media
 de unos 10 bytes/s.

 Tal y como habitualmente es el caso en I2P, aquí hay un equilibrio
 fundamental entre anonimato y eficiencia. Alguien diría que usar las
 cabeceras (HTTP) ETag y de última modificación es arriesgado porque
 expone la última vez que solicitó los datos. Otros han sugerido
 pedir sólo claves específicas (de forma similar a lo que hacen los
 servicios de salto (jump, de direccionamiento distribuido), pero de
 un modo más automatizado), posiblemente a un coste superior en
 anonimato.

 Possible improvements would be a replacement or supplement to
 address book (see [p](http:///)), or something simple like
 subscribing to http://example.i2p/cgi-bin/recenthosts.cgi rather
 than http://example.i2p/hosts.txt. If a hypothetical recenthosts.cgi
 distributed all hosts from the last 24 hours, for example, that
 could be both more efficient and more anonymous than the current
 hosts.txt with last-modified and etag.

 A sample implementation is on stats.i2p at [](). This script returns an Etag with a
 timestamp. When a request comes in with the If-None-Match etag, the
 script ONLY returns new hosts since that timestamp, or 304 Not
 Modified if there are none. In this way, the script efficiently
 returns only the hosts the subscriber does not know about, in an
 address book-compatible manner.

 Así que la ineficiencia no es un gran problema y hay varias formas
 de mejorar las cosas sin un cambio radical.

- **No escalable:** El fichero hosts.txt de 400KB (con búsqueda
 lineal) no es tan grande de momento, y probablemente podamos crecer
 por un factor de 10x o 100x antes de que sea un problema.

 En cuanto al tráfico de red, vea más arriba. Pero a no ser que vaya
 a hacer una petición a tiempo real lenta sobre la red para obtener
 una clave, necesita tener todo el grupo de claves almacenadas
 localmente, con el coste de unos 500 bytes por clave.

- **Requiere configuración y \"confianza\":** La libreta de
 direcciones lista para usar sólo está suscrita a
 http://www.i2p2.i2p/hosts.txt, la cual raramente se actualiza,
 creando una experiencia pobre para los principiantes.

 Esto es intencionado. jrandom quiere que un usuario \"confíe\" en un
 proveedor de host.txt, y como a él le gusta decir, \"la confianza no
 es una variable binaria\". Los pasos de configuración intenta
 obligar a los usuarios a pensar sobre los problemas de confianza en
 una red anónima.

 As another example, the \"I2P Site Unknown\" error page in the HTTP
 Proxy lists some jump services, but doesn\'t \"recommend\" any one
 in particular, and it\'s up to the user to pick one (or not).
 jrandom would say we trust the listed providers enough to list them
 but not enough to automatically go fetch the key from them.

 ¿Cómo es de exitoso este sistema?. No estoy seguro. Pero tiene que
 haber algún tipo de jerarquía de confianza en el sistema de
 nombres/dominios. El tratar a todo el mundo igual puede aumentar el
 riesgo de secuestro de dominios.

- **No es DNS**

 Desafortunadamente, las búsquedas en tiempo real sobre I2P
 relentizarían significativamente la navegación web.

 Además, DNS está basado en búsquedas con caché y tiempo de vida
 limitados, mientras que las claves de i2p son permanentes.

 Seguro, podríamos hacerlo funcionar, pero ¿para qué? Sería un mal
 apaño.

- **Not reliable:** It depends on specific servers for address book
 subscriptions.

 Si, depende de los pocos servidores que ha configurado. Dentro de
 i2p, los servidores y los servicios van y vienen. Cualquier otros
 sistema centralizado (por ejemplo servidores raíz DNS) tendrían los
 mismos problemas. Un sistema descentralizado completamente (todo el
 mundo es una autoridad) es posible implementando una solución tipo
 \"todo el mundo es un servidor raíz DNS\", o con algo incluso más
 simple, con un script que añada a todos los que estén en su
 hosts.txt a su libreta de direcciones.

 La gente que defiende la solución de todos-son-autoridad
 generalmente no han pensado en los conflictos y en los secuestros de
 dominios.

- **Awkward, not real-time:** It\'s a patchwork of hosts.txt
 providers, key-add web form providers, jump service providers, I2P
 Site status reporters. Jump servers and subscriptions are a pain, it
 should just work like DNS.

 Vea las secciones de fiabilidad y confianza.

En resumen, el sistema actual no está terriblemente roto, no es
ineficiente, o no es escalable, y las propuestas de \"simplemente usemos
DNS\" no están bien pensadas.

## Alternativas {#alternatives}

El código de I2P contiene varios sistemas de dominios listos para
enchufar, y soporta opciones de configuración para permitir experimentar
con sistemas de nombres.

- **Meta** - llama a uno o más sistemas de nombres en orden. Por
 defecto llama a PetName y después a Hosts Txt.

- **PetName** - busca en el archivo petnames.txt. El formato de este
 archivo NO es el mismo que el de

- **HostsTxt** - Busca en los siguentes archivos en orden:

- 1. privatehosts.txt
 2. userhosts.txt
 3. hosts.txt

- **AddressDB** - Cada host es listado en un archivo separado en el
 directorio addressDb/.

- **Eepget** - hace una búsqueda HTTP en un servidor externo - por
 orden de realización debe colocarse después de la búsqueda en
 HostsTxt con Meta. Esto podría complementar o reemplazar al sistema
 de servicios de salto (jump, direccionamiento distribuido). Incluye
 cacheado en-memoria.

- **Exec** - llama a un programa externo para las búsquedas, permite
 experimentación adicional en los esquemas de búsquedas,
 independientemente de java. Puede ser usado después de HostsTxt o
 como un sistema de nombres en solitario. Incluye caché en-memoria.

- **Dummy** - usado como apoyo para los nombres BAse64, do otra forma
 falla.

El sistema actual de dominios puede ser cambiado en la configuración
avanzada \'i2p.naming.impl\' (se necesita reiniciar). Vea
core/java/src/net/i2p/client/naming para más detalles.

Any new system should be stacked with HostsTxt, or should implement
local storage and/or the address book subscription functions, since
address book only knows about the hosts.txt files and format.

## Certificados {#certificates}

Las destinaciones I2P contiene un certificado, aunque hasta el momento
ese certificado es siempre vacío, null. Con un certificado nulo, las
destinaciones base64 son siempre de 516 bytes y terminan en \"AAAA\", y
esto es comprobado en el mecanismo de unión de la libreta de
direcciones, y posiblemente en otros sitios. Además, no hay ningún
método disponible para generar un certificado o añadirlo a la
destinación. Con lo que este debe ser actualizado para implementar los
certificados.

One possible use of certificates is for [proof of
work](#hashcash).

Otro es para que los \"subdominios\" (entre comillas porque realmente no
existe tal cosa, I2P utiliza un sistema de dominios plano) sean firmados
por las claves de dominio de segundo nivel .

Con cualquier tipo de implementación de certificados tiene que venir
algún método para verificar los certificados. Probablemente esto debería
en al código de unión de la libreta de direcciones. ¿Hay un método para
múltiples tipos de certificados, o múltiples certificados?

Añadiendo sobre un certificado, autentificando la respuesta como firmada
por alguna autoridad certificada centralizada podría solucionar muchos
de los problemas con los servidores de nombres hostiles, pero lo dejaría
abierto a ataques de respuesta, al igual que a los ataques desde una
autoridad de certificados hostil.


