 BOB - Basic Open
Bridge 2022-06 

## Warning - Deprecated

Not for use by new applications. BOB supports the DSA-SHA1 signature
type only. BOB will not be extended to support new signature types or
other advanced features. New applications should use [SAM
V3]().

BOB is not supported in Java I2P new installs as of release 1.7.0
(2022-02). It will still work in Java I2P originally installed as
version 1.6.1 or earlier, even after updates, but it is unsupported and
may break at any time. BOB is still supported by i2pd as of 2022-06, but
applications should still migrate to SAMv3 for the reasons above.

At this point, most of the good ideas from BOB have been incorporated
into SAMv3, which has more features and more real-world use. BOB may
still work on some installations (see above), but it is not gaining the
advanced features available to SAMv3 and is essentially unsupported,
except by i2pd.

## Language libraries for the BOB API

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python -
 [i2py-bob](http:///w/i2py-bob.git)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## Información general

`CLAVES` = par de claves pública+privada, estas son BASE64

`CLAVE` = clave pública, también BASE64

`ERROR` como está implícito, devuelve el mensaje
`"ERROR "+DESCRIPCIÓN+"\n"`, donde la `DESCRIPCIÓN` es lo que fue mal.

`OK` devuelve `"OK"`, y si se van a devolver datos, se hará en la misma
línea. `OK` significa que el comando ha finalizado.

`DATOS` líneas conteniendo la información que usted solicitó. Puede
haber múltiples líneas de `DATOS` por solicitud.

**NOTA:** El comando \`help\` es el ÚNICO comando que tiene una
excepción a las reglas\... actualmente puede devolver ¡nada! Es
intencionado, dado que \`help\` es un HUMANO y no un comando de
APLICACIÓN.

## Conexión y versión

Toda la salida de estado de BOB es por líneas. Las líneas pueden
terminar en \\n o \\r\\n, dependiendo del sistema. En conexión, BOB
produce una salida en dos líneas:

 BOB version OK 

La versión actual es: 00.00.10

Observe que las versiones anteriores usaban dígitos hexadecimales con
letras mayúsculas y no cumplían los estándares de versionado de I2P. Se
recomienda que las versiones subsiguientes sólo usen dígitos decimales
0-9. 00.00.10

Historial de la versión

 Versión Versión del router I2P Cambios
 --------------------- ------------------------ -------------------------
 00.00.10 0.9.8 versión actual
 00.00.00 - 00.00.0F   versiones de desarrollo

## Comandos

**POR FAVOR OBSERVE QUE:** Para detalles ACTUALES de los comandos POR
FAVOR use el comando interno \`help\`. Tan sólo haga telnet al localhost
2827, teclee \`help\` y podrá obtener la documentación completa para
cada comando.

Los comandos nunca cambian o se vuelven obsoletos, sin embargo nuevos
comandos son añadidos de cuando en cuando.

 COMMAND OPERAND RETURNS help (optional
command to get help on) NOTHING or OK and description of the command
clear ERROR or OK getdest ERROR or OK and KEY getkeys ERROR or OK and
KEYS getnick tunnelname ERROR or OK inhost hostname or IP address ERROR
or OK inport port number ERROR or OK list ERROR or DATA lines and final
OK lookup hostname ERROR or OK and KEY newkeys ERROR or OK and KEY
option key1=value1 key2=value2\... ERROR or OK outhost hostname or IP
address ERROR or OK outport port number ERROR or OK quiet ERROR or OK
quit OK and terminates the command connection setkeys KEYS ERROR or OK
and KEY setnick tunnel nickname ERROR or OK show ERROR or OK and
information showprops ERROR or OK and information start ERROR or OK
status tunnel nickname ERROR or OK and information stop ERROR or OK
verify KEY ERROR or OK visit OK, and dumps BOB\'s threads to the
wrapper.log zap nothing, quits BOB 

Una vez configurado, todos los sockets TCP pueden y bloquearán según se
necesite, y no hay necesidad de mensaje adicional alguno hacia/desde el
canal de comandos. Esto permite al router marcar el paso del stream sin
reventar con un OOM (out of memory/agotamiento de memoria) como lo hace
SAM al ahogarse intentando empujar varios streams dentro o fuera de un
socket \-- ¡que no puede crecer cuando tiene muchas conexiones!

Lo que también es agradable acerca de esta interfaz en particular es que
escribir algo para la interfaz, es mucho mucho más fácil que para SAM.
No hay ningún otro proceso que realizar después de configurarla. Su
configuración es tan simple, que muchas aplicaciones sencillas, tales
como nc (netcat) se pueden usar para apuntar a alguna aplicación. El
valor ahí es que uno puede programar periodos de actividad e inactividad
para una aplicación, sin tener que cambiar la aplicación para hacer eso,
o incluso sin tener que detener esa aplicación. En su lugar, puede
literalmente \"desenchufar\" el destino, y \"enchufarlo\" de nuevo.
Mientras las mismas direcciones IP/puerto y claves de destino sean
usadas al levantar la pasarela, a las aplicaciones TCP normales no les
importará, y no lo notarán. Simplemente serán engañadas \-- los destinos
no son alcanzables, y así nada va a recibirse.

## Ejemplos

Para el siguiente ejemplo, estableceremos un conexión loopback local muy
simple, con dos destinos. El destino \"boca\" será el servicio CHARGEN
desde el demonio superservidor INET. El destino \"oido\" será un puerto
local sobre el que podrá hacer telnet, y observar el precioso ASCII de
prueba vomitado.

 DIÁLOGO DE SESIÓN DE EJEMPLO \-- un simple
\`telnet 127.0.0.1 2827\` funciona A = Application C = Respuesta al
comando de BOB. FROM TO DIALOGUE C A BOB 00.00.10 C A OK A C setnick
mouth C A OK Nickname set to mouth A C newkeys C A OK
ZMPz1zinTdy3\~zGD\~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr\~0g2-l0vM7Y8nSqtFrSdMw\~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU\~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq\~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw\~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA


**ANOTE LA CLAVE DE DESTINO ANTERIOR, ¡LA SUYA SERÁ DIFERENTE!**

 FROM TO DIALOGUE A C outhost 127.0.0.1 C A
OK outhost set A C outport 19 C A OK outbound port set A C start C A OK
tunnel starting 

En este punto no hubo error, un destino con un apodo de \"boca\" está
establecido. Cuando contacte con el destino proporcionado, en realidad
conectará con el servicio `CHARGEN` sobre `19/TCP`.

Ahora para la otra mitad, para que realmente podamos contactar con este
destino.

 FROM TO DIALOGUE C A BOB 00.00.10 C A OK A
C setnick ear C A OK Nickname set to ear A C newkeys C A OK
8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg\~3eXtL-7S-qU-wdP-6VF\~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J\~flAvF4wrbF-LfVpMdg\~tjtns6fA\~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f\~dzoRCapAGDDTTnvjXuLrZ-vN-orT\~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A C inhost 127.0.0.1 C A OK inhost set A C inport 37337 C A OK inbound
port set A C start C A OK tunnel starting A C quit C A OK Bye! 

Ahora todo lo que necesitamos es hacer telnet a 127.0.0.1, puerto 37337,
enviar la clave destino o la dirección del servidor de la libreta de
direcciones con la que queramos contactar. En este caso, queremos
contactar con \"boca\", todo lo que haremos es pegar la clave e irá.

**NOTA:** El comando \"quit\" en el canal de comandos NO desconecta los
túneles como SAM.

 \$ telnet 127.0.0.1 37337 Trying
127.0.0.1\... Connected to 127.0.0.1. Escape character is \'\^\]\'.
ZMPz1zinTdy3\~zGD\~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr\~0g2-l0vM7Y8nSqtFrSdMw\~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU\~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq\~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw\~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefg
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefgh
\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghi
#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghij
\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghijk
\... 

Después de unas pocas millas virtuales de esta eyección, presione
`Control-]`

 \... cdefghijklmnopqrstuvwxyz{\|}\~
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{\|}\~
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{\|}\~ !\"#\$%&\'()\*+,-./0123456789:;\<= telnet\>
c Connection closed. 

Aquí está lo que sucedió\...

 telnet -\> ear -\> i2p -\> mouth -\>
chargen -. telnet \<- ear \<- i2p \<- mouth \<\-\-\-\-\-\-\-\-\-\--\' 

You can connect to I2P SITES too!

 \$ telnet 127.0.0.1 37337 Trying
127.0.0.1\... Connected to 127.0.0.1. Escape character is \'\^\]\'.
i2host.i2p GET / HTTP/1.1 HTTP/1.1 200 OK Date: Fri, 05 Dec 2008
14:20:28 GMT Connection: close Content-Type: text/html Content-Length:
3946 Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT Accept-Ranges: bytes
\<html\> \<head\> \<title\>I2HOST\</title\> \<link rel=\"shortcut icon\"
href=\"favicon.ico\"\> \</head\> \... \<a
href=\"http://sponge.i2p/\"\>\--Sponge.\</a\>\</pre\> \<img
src=\"/counter.gif\" alt=\"!@\^7A76Z!#(\*&amp;%\"\> visitors. \</body\>
\</html\> Connection closed by foreign host. \$ 

Pretty cool isn\'t it? Try some other well known I2P SITES if you like,
nonexistent ones, etc, to get a feel for what kind of output to expect
in different situations. For the most part, it is suggested that you
ignore any of the error messages. They would be meaningless to the
application, and are only presented for human debugging.

Desactivemos nuestros destinos ahora que hemos terminado del todo con
ellos.

Primero, veamos que apodos de destino tenemos.

 FROM TO DIALOGUE A C list C A DATA
NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true
QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST:
127.0.0.1 C A DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING:
false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT:
not_set OUTHOST: localhost C A OK Listing done 

De acuerdo, ahí las tiene. Primero, eliminemos \"boca\" (\`mouth\`).

 FROM TO DIALOGUE A C getnick mouth C A OK
Nickname set to mouth A C stop C A OK tunnel stopping A C clear C A OK
cleared 

Ahora para eliminar \"oido\" (\`ear\`), note que esto es lo que ocurre
cuando teclea demasiado rápido, y le muestra el aspecto de los típicos
mensajes de ERROR.

 FROM TO DIALOGUE A C getnick ear C A OK
Nickname set to ear A C stop C A OK tunnel stopping A C clear C A ERROR
tunnel is active A C clear C A OK cleared A C quit C A OK Bye! 

No le molestaré mostrando un ejemplo de un receptor final de una
pasarela (\`bridge\`) porque es muy simple. Hay dos posibles
configuraciones para ello, y se accionan con el comando \"quiet\"
(silenciar).

La configuración por defecto es NO silenciado, a y los primeros datos en
llegar a su socket de escucha es el destiono que está estableciendo el
contacto. Es una sola línea consistente en una dirección BASE64 seguida
de una nueva línea. Todo lo que viene después de aquello es en realidad
para consumo de la aplicación.

En modo silencioso, piense en él como en una conexión regular a
Internet. No hay dato extra entrante alguno. Es tan solo como si
estuviera conectado normalmente al Internet regular. Este modo permite
una forma de transparencia muy parecida a la que está disponible en las
páginas de configuración del túnel de la consola del router, así que
usted puede, por ejemplo, usar BOB para apuntar hacia un destino en un
servidor web, y no tendría que modificar para nada el servidor web.

La ventaja de usar BOB para esto es la que fue discutida previamente.
Puede programar periodos de actividad aleatorios para la aplicación,
redirigirla a una máquina diferente, etc. Un uso de esto puede ser algo
parecido a tratar de confundir acciones de estimación de la conectividad
router-destino. Puede detener e iniciar el destino con un proceso
totalmente diferente para establecer periodos aleatorios de actividad e
inactividad para los servicios. De ese modo sólo se estaría deteniendo
la capacidad de contactar con tal servicio, sin tener que preocuparse
cerrándolo y reiniciándolo. Podría redirigir y apuntar a una máquina
diferente de su LAN, mientras hace actualizaciones, o apuntar a un
conjunto de máquinas de respaldo dependiendo de lo que se esté
ejecuntando, etc, etc. Sólo su imaginación limita lo que podría hacer
con BOB.


