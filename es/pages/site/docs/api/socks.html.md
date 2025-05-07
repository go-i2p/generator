 SOCKS 

## Proxies SOCKS y SOCKS

The SOCKS proxy is working as of release 0.7.1. SOCKS 4/4a/5 are
supported. Enable SOCKS by creating a SOCKS client tunnel in i2ptunnel.
Both shared-clients and non-shared are supported. There is no SOCKS
outproxy so it is of limited use. 

Muchas aplicaciones filtran información sensible que podría
identificarle en Internet. I2P sólo filtra la conexión de datos, pero si
el programa que usted intenta ejecutar envía esta información como
contenido, I2P no tiene manera de proteger su anonimato. Por ejemplo,
algunas aplicaciones de correo enviarán la dirección IP de la máquina
sobre la que estén ejecutando el servidor de correo. No hay forma de I2P
filtre esto, por lo que usar I2P para socksificar (\'socksify\')
aplicaciones existentes es posible, pero extremadamente peligroso.

Y citando a un email de 2005:

 ... hay una razón por la que ambos, los humanos y otros, hemos construido 
 y abandonado los proxys SOCKS. Rebotar el tráfico arbitrario es simplemente 
 bastante inseguro, y nos corresponde a nosotros, como desarrolladores 
 de software de anonimato y seguridad, tener la seguridad de nuestros 
 usuarios finales entre nuestras prioridades.

Esperar que simplemente podamos adherir un cliente arbitrario sobre I2P
sin auditar la seguridad y anonimato tanto de su comportamiento como de
sus protocolos expuestos, es ingenuo. Casi cualquier aplicación y
protocolo viola el anonimato, a menos que fuera específicamente diseñado
para lo contrario, e incluso entonces la mayoría de aquellos también lo
hace. Esa es la realidad. Los usuarios finales están mejor servidos con
sistemas diseñados para el anonimato y la seguridad. Modificar sistemas
existentes para trabajar en entornos anónimos no es una cuestión banal,
supone varios órdenes de magnitud más de trabajo que simplemente usar
las APIs existentes de I2P.

El proxy SOCKS soporta los nombres de las libretas de direcciones
estándar, pero no los destinos Base64. Los hashes Base32 deberían
funcionar desde la versión \`0.7\`. Sólo soporta conexiones salientes,
es decir, se erradicó el soporte para un I2PTunnel de cliente. Se forzó
la inclusión del soporte UDP, pero no funciona aún. Se forzó la
inclusión de la selección mediante número de puerto de proxy externo
(\`outproxy\`).

The notes for [Meeting 81]() and [Meeting
82]() in March 2004.

[Onioncat](http://www.abenteuerland.at/onioncat/)

[](http:///)

### Si consigue que algo funcione

Por favor, permítanos saberlo. Y, por favor, proporcione advertencias
sustanciales acerca de los riesgos de los proxys SOCKS. 
