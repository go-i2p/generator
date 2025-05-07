 I2PControl -
Remote Control Service 2022-01 0.9.52 

I2P enables a [JSONRPC2](http://en.wikipedia.org/wiki/JSON-RPC)
interface via the plugin [I2PControl](). The
aim of the interface is to provide simple way to interface with a
running I2P node. A client, itoopie, has been developed in parallel. The
JSONRPC2 implementation for the client as well as the plugin is provided
by the java libraries [JSON-RPC
2.0](http://software.dzhuvinov.com/json-rpc-2.0.html). A list of
implementations of JSON-RPC for various languages can be found at [the
JSON-RPC wiki](http://json-rpc.org/wiki/implementations).

I2PControl por defecto está escuchando sobre https://localhost:7650

## API, versión 1.

Los parámetros sólo se proporcionan a través del nombre (mapas).

#### Formato JSON-RPC 2

Request: { \"id\": \"id\", \"method\":
\"Method-name\", \"params\": { \"Param-key-1\": \"param-value-1\",
\"Param-key-2\": \"param-value-2\", \"Token\": \"\*\*actual token\*\*\"
}, \"jsonrpc\": \"2.0\" } Response: { \"id\": \"id\", \"result\": { \"Result-key-1\":
\"result-value-1\", \"Result-key-2\": \"result-value-2\" }, \"jsonrpc\":
\"2.0\" } 

- - Param-key-1 -- Description
 - Param-key-2 -- Description
 - Token -- Muestra usada para autentificar cada petición
 (excluyendo el método RPC \'Authenticate\')

- - Result-key-1 -- Description
 - Result-key-2 -- Description

#### Métodos implemetados

- - API -- \[long\] La versión del API de I2PControl usada por el
 cliente.
 - Password -- \[String\] La contraseña usada para autentificarse
 en el servidor remoto.

- - API -- \[long\] Versión del API principal de I2PControl
 implementado por el servidor.
 - Token -- \[String\] La muestra usada para la posterior
 comunicación.

```{=html}
<!-- -->
```
- - Echo -- \[String\] Un valor será devuelto como respuesta.
 - Token -- \[String\] Token usado para autentificar el cliente. Es
 provisto por el servidor a través del método RPC
 \'Authenticate\'

- - Result -- \[String\] Valor de la clave \'echo\', clave eco, en
 la petición.

```{=html}
<!-- -->
```
- - Stat -- \[String\] Determines which
 rateStat to fetch, see
 [ratestats]().
 - Period -- \[long\] Determina para qué periodo de tiempo se
 obtendrá el stat. Se mide en ms.
 - Token -- \[String\] Token usado para autentificar el cliente. Es
 provisto por el servidor a través del método RPC
 \'Authenticate\'

- - Result -- \[double\] Returns the average value for the requested
 rateStat and period.

```{=html}
<!-- -->
```
- - \*i2pcontrol.address -- \[String\] Cambia la dirección donde
 escucha I2PControl (sólo se han implementado 127.0.0.1 y 0.0.0.0
 para I2PControl hasta ahora).
 - \*i2pcontrol.password -- \[String\] Cambia la contraseña para
 I2PControl, todos los tokens de autentificación serán revocados.
 - \*i2pcontrol.port -- \[String\] Cambia el puerto en el que
 I2PControl escuchará por conexiones.
 - Token -- \[String\] Token usado para autentificar el cliente. Es
 provisto por el servidor a través del método RPC
 \'Authenticate\'

- - \*\*i2pcontrol.address -- \[null\] Devuelto si la dirección fue
 cambiada
 - \*\*i2pcontrol.password -- \[null\] Devuelto si la configuración
 fue cambiada
 - \*\*i2pcontrol.port -- \[null\] Devuelto si la configuración fue
 cambiada
 - SettingsSaved -- \[Boolean\] Devuelve verdadero si se hizo algún
 cambio.
 - RestartNeeded -- \[Boolean\] Devuelve verdadero si se hizo algún
 cambio que necesite un reinicio para tener efecto.

```{=html}
<!-- -->
```
- - \*i2p.router.status -- \[n/a\]
 - \*i2p.router.uptime -- \[n/a\]
 - \*i2p.router.version -- \[n/a\]
 - \*i2p.router.net.bw.inbound.1s -- \[n/a\]
 - \*i2p.router.net.bw.inbound.15s -- \[n/a\]
 - \*i2p.router.net.bw.outbound.1s -- \[n/a\]
 - \*i2p.router.net.bw.outbound.15s -- \[n/a\]
 - \*i2p.router.net.status -- \[n/a\]
 - \*i2p.router.net.tunnels.participating -- \[n/a\]
 - \*i2p.router.netdb.activepeers -- \[n/a\]
 - \*i2p.router.netdb.fastpeers -- \[n/a\]
 - \*i2p.router.netdb.highcapacitypeers -- \[n/a\]
 - \*i2p.router.netdb.isreseeding -- \[n/a\]
 - \*i2p.router.netdb.knownpeers -- \[n/a\]
 - Token -- \[String\] Token usado para autentificar el cliente. Es
 provisto por el servidor a través del método RPC
 \'Authenticate\'

- - \*\*i2p.router.status -- \[String\] cuál es el estado del
 router. A free-format, translated string intended for display to
 the user. May include information such as whether the router is
 accepting participating tunnels. Content is
 implementation-dependent.
 - \*\*i2p.router.uptime -- \[long\] Cuánto tiempo lleva encendido
 el ruter en ms. Note: i2pd routers prior to version 2.41
 returned this value as a string. For compatibility, clients
 should handle both string and long.
 - \*\*i2p.router.version -- \[String\] Qué versión de I2P está
 ejecutando el ruter.
 - \*\*i2p.router.net.bw.inbound.1s -- \[double\] Media del ancho
 de banda de entrada durante 1 segundo, en Bps.
 - \*\*i2p.router.net.bw.inbound.15s -- \[double\] Media del ancho
 de banda de entrada durante 15 segundos, en Bps.
 - \*\*i2p.router.net.bw.outbound.1s -- \[double\] Media del ancho
 de banda de salida durante 1 segundo, en Bps.
 - \*\*i2p.router.net.bw.outbound.15s -- \[double\] Media del ancho
 de banda de salida durante 15 segundos, en Bps.
 - \*\*i2p.router.net.status -- \[long\] Cuál es el estado actual
 de la red. De acuerdo con la lista:
 - 0 -- OK
 - 1 -- TESTING
 - 2 -- FIREWALLED
 - 3 -- HIDDEN
 - 4 -- WARN_FIREWALLED_AND_FAST
 - 5 -- WARN_FIREWALLED_AND_FLOODFILL
 - 6 -- WARN_FIREWALLED_WITH_INBOUND_TCP
 - 7 -- WARN_FIREWALLED_WITH_UDP_DISABLED
 - 8 -- ERROR_I2CP
 - 9 -- ERROR_CLOCK_SKEW
 - 10 -- ERROR_PRIVATE_TCP_ADDRESS
 - 11 -- ERROR_SYMMETRIC_NAT
 - 12 -- ERROR_UDP_PORT_IN_USE
 - 13 -- ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL
 - 14 -- ERROR_UDP_DISABLED_AND_TCP_UNSET
 - \*\*i2p.router.net.tunnels.participating -- \[long\] En cuántos
 túneles estamos participando en la red I2p.
 - \*\*i2p.router.netdb.activepeers -- \[long\] Con cuántos túneles
 nos hemos comunicado recientemente.
 - \*\*i2p.router.netdb.fastpeers -- \[long\] Cuántos pares se
 consideran como \'rápidos\'.
 - \*\*i2p.router.netdb.highcapacitypeers -- \[long\] Cuántos pares
 se consideran de \'alta capacidad\'
 - \*\*i2p.router.netdb.isreseeding -- \[boolean\] ¿El router I2P
 está resembrando nodos en su NetDB?
 - \*\*i2p.router.netdb.knownpeers -- \[long\] Cuántos pares
 conocemos (listados en nuestra NetDB).

```{=html}
<!-- -->
```
- - \*FindUpdates -- \[n/a\] **Bloqueando**. Inicia una búsqueda
 para actualizaciones firmadas.
 - \*Reseed -- \[n/a\] Inicia el resembrado de un ruter, obteniendo
 los pares para nuestra NetDB desde un ordenador remoto.
 - \*Restart -- \[n/a\] Reinicia el router.
 - \*RestartGraceful -- \[n/a\] Reinicia el ruter con cuidado
 (espera a que expiren los túneles participantes).
 - \*Shutdown -- \[n/a\] Apaga el router.
 - \*ShutdownGraceful -- \[n/a\] Apaga el ruter con cuidado (espera
 a que expiren los túneles participantes).
 - \*Update -- \[n/a\] Inicia una actualización del router I2P
 desde fuentes firmadas.
 - Token -- \[String\] Token usado para autentificar el cliente. Es
 provisto por el servidor a través del método RPC
 \'Authenticate\'

- - \*\*FindUpdates -- \[boolean\] **Bloqueando**. Devuelve
 verdadero si se ha encontrado una actualización firmada.
 - \*\*Reseed -- \[null\] Si se ha requerido, verifica que el
 resembrado ha sido iniciado.
 - \*\*Restart -- \[null\] Si se ha requerido, verifica que el
 reinicio ha sido iniciado.
 - \*\*RestartGraceful -- \[null\] Si se ha requerido, verifica que
 el reinicio con cuidado ha sido iniciado.
 - \*\*Shutdown -- \[null\] Si se ha requerido, verifica que el
 apagado ha sido iniciado.
 - \*\*ShutdownGraceful -- \[null\] Si se ha requerido, verifica
 que el apagado con cuidado ha sido iniciado.
 - \*\*Update -- \[String\] **Bloqueando**. Si se solicita,
 devuelve el estado de la actualización

```{=html}
<!-- -->
```
- - \*i2p.router.net.ntcp.port -- \[String\] Qué puerto es usado
 para el transporte TCP. Si se ha enviado null, se devolverá la
 configuración actual.
 - \*i2p.router.net.ntcp.hostname -- \[String\] Qué nombre de
 dominio es usado para el transporte TCP. Si se ha enviado null,
 se devolverá la configuración actual.
 - \*i2p.router.net.ntcp.autoip -- \[String\] Usar la ip detectada
 automáticamente para el transporte TCP . Si se ha enciado null,
 se devolverá la configuración actual.
 - \*i2p.router.net.ssu.port -- \[String\] Qué puerto es usado para
 el transporte UDP. Si se ha enviado null, se devolverá la
 configuración actual.
 - \*i2p.router.net.ssu.hostname -- \[String\] Qué nombre de
 dominio es usado para el transporte UDP. Si se ha enviado null,
 se devolverá la configuración actual.
 - \*i2p.router.net.ssu.autoip -- \[String\] Qué métodos deben
 susarse para detectar la dirección ip del transporte UDP. Si se
 ha enviado null, se devolverá la configuración actual.
 - \*i2p.router.net.ssu.detectedip -- \[null\] Qué ip ha sido
 detectada para el transporte UDP.
 - \*i2p.router.net.upnp -- \[String\] Está UPnP activo. Si se ha
 enviado null, se devolverá la configuración actual.
 - \*i2p.router.net.bw.share -- \[String\] Qué tanto por ciento del
 ancho de banda es utilizable para los túneles participantes. Si
 se ha enviado null, se devolverá la configuración actual.
 - \*i2p.router.net.bw.in -- \[String\] Cuántos KB/s se permiten
 para el ancho de banda entrante. Si se ha enviado null, se
 devolverá la configuración actual.
 - \*i2p.router.net.bw.out -- \[String\] Cuántos KB/s se permiten
 para el ancho de banda de salida. Si se ha enviado null, se
 devolverá la configuración actual.
 - \*i2p.router.net.laptopmode -- \[String\] Si está el modo laptop
 activado (el cambio de la identidad del ruter cuando cambia la
 IP). Si se ha enviado null, se devolverá la configuración
 actual.
 - Token -- \[String\] El identificador (\`token\`) usado para la
 autentificación del cliente, es proporcionado por el servidor a
 través del método \'Authenticate\' (autentificar) de RPC. Si se
 envía vacío (\'null\'), se devolverá el valor de configuración
 actual.

- - Note: i2pd routers prior to version 2.41 returned some of these
 values as numbers. For compatibility, clients should handle both
 strings and numbers.
 - \*\*i2p.router.net.ntcp.port -- \[String\] Si se solicita,
 devuelve el puerto usado para el transporte TCP.
 - \*\*i2p.router.net.ntcp.hostname -- \[String\] Si se solicita,
 devuelve el nombre del servidor usado para el transporte TCP.
 - \*\*i2p.router.net.ntcp.autoip -- \[String\] Si se solicita,
 devuelve el método usado para detectar automáticamente la IP
 para el transporte TCP.
 - \*\*i2p.router.net.ssu.port -- \[String\] Si se solicita,
 devuelve el puerto usado para el transporte UDP.
 - \*\*i2p.router.net.ssu.hostname -- \[String\] Si se solicita,
 devuelve el nombre del servidor usado para el transporte UDP.
 - \*\*i2p.router.net.ssu.autoip -- \[String\] Si se solicita,
 devuelve los métodos usados para detectar la dirección IP del
 transporte UDP.
 - \*\*i2p.router.net.ssu.detectedip -- \[String\] Si se solicita,
 devuelve la IP que ha sido detectada por el transporte UDP.
 - \*\*i2p.router.net.upnp -- \[String\] Si se solicita, devuelve
 el valor de la configuración UPnP.
 - \*\*i2p.router.net.bw.share -- \[String\] Si se solicita,
 devuelve el porcentaje de ancho de banda disponible para los
 túneles participantes.
 - \*\*i2p.router.net.bw.in -- \[String\] Si se solicita, devuelve
 el número de KB/s de ancho de banda de entrada que están
 permitidos.
 - \*\*i2p.router.net.bw.out -- \[String\] Si se solicita, devuelve
 el número de KB/s de ancho de banda de salida que están
 permitidos.
 - \*\*i2p.router.net.laptopmode -- \[String\] Si se solicita,
 devuelve el valor del modo laptop (portátil).
 - SettingsSaved -- \[boolean\] Han sido guardadas las
 configuraciones proporcionadas.
 - RestartNeeded -- \[boolean\] Se necesita un reinicio para que
 las nuevas configuraciones se usen.

```{=html}
<!-- -->
```
- - {\"setting-key\": \"setting-value\", \...} -- \[Map\]

- - {\"setting-key\": \"setting-value\", \...} -- \[Map\]

- - \"setting-key\" -- \[String\]

- 

\* denota un valor opcional.

\*\* denota un valor de retorno que posiblemente ocurra

### Códigos de error

- -32700 -- Error de procesado JSON.
- -32600 -- Petición no válida.
- -32601 -- Método no encontrado.
- -32602 -- Parámetros no válidos.
- -32603 -- Error interno.

```{=html}
<!-- -->
```
- -32001 -- Se proporcionó una contraseña no válida.
- -32002 -- No se presentó la credencial (\`token\`) de
 autentificación.
- -32003 -- La credencial (\`token\`) de autentificación no existe
- -32004 -- La credencial (\`token\`) de identificación ha expirado y
 será eliminada.
- -32005 -- La versión de la API I2PControl usada no fue especificada,
 pero se requiere que sea especificada.
- -32006 -- La versión de la API I2PControl especificada no está
 soportada por I2PControl.


