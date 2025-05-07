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

I2PControl écoute par défaut sur https://localhost:7650

## API, version 1.

Les paramètres sont seulement fournis selon la façon nommée (maps).

#### Format JSON-RPC 2

Request: { \"id\": \"id\", \"method\":
\"Method-name\", \"params\": { \"Param-key-1\": \"param-value-1\",
\"Param-key-2\": \"param-value-2\", \"Token\": \"\*\*actual token\*\*\"
}, \"jsonrpc\": \"2.0\" } Response: { \"id\": \"id\", \"result\": { \"Result-key-1\":
\"result-value-1\", \"Result-key-2\": \"result-value-2\" }, \"jsonrpc\":
\"2.0\" } 

- - Param-key-1 -- Description
 - Param-key-2 -- Description
 - Token -- Le jeton utilisé pour authentifier chaque requête
 (excluant la méthode \'Authenticate\' de RPC)

- - Result-key-1 -- Description
 - Result-key-2 -- Description

#### Méthodes implémentées

- - API -- \[long\] La version de l'API I2PControl utilisée par le
 client.
 - Password -- \[String\] Le mot de passe utilisé pour authentifier
 envers le serveur distant.

- - API -- \[long\] La version d'API I2PControl primaire implémentée
 par le serveur.
 - Token -- \[String\] Le jeton utilisé pour une future
 communication.

```{=html}
<!-- -->
```
- - Echo -- \[String\] La valeur sera rendue en réponse.
 - Token -- \[String\] Jeton utilisé pour authentifier le client.
 Il est fournit par le serveur via la méthode RPC
 \'Authenticate\'.

- - Result -- \[String\] Valeur de la clé \'echo\' dans la requête.

```{=html}
<!-- -->
```
- - Stat -- \[String\] Determines which
 rateStat to fetch, see
 [ratestats]().
 - Period -- \[long\] Détermine durant quelle période une stat est
 récupérée. Mesuré en ms.
 - Token -- \[String\] Jeton utilisé pour authentifier le client.
 Il est fournit par le serveur via la méthode RPC
 \'Authenticate\'.

- - Result -- \[double\] Returns the average value for the requested
 rateStat and period.

```{=html}
<!-- -->
```
- - \*i2pcontrol.address -- \[String\] Met en place une nouvelle
 adresse d'écoute pour I2PControl (seules 127.0.0.1 et 0.0.0.0
 est actuellement mises en œuvre dans I2PControl).
 - \*i2pcontrol.password -- \[String\] Met un nouveau mot de passe
 à I2PControl, tous les jetons d'authentification seront
 révoqués.
 - \*i2pcontrol.port -- \[String\] Bascule le port sur lequel
 I2PControl écoutera les connexions.
 - Token -- \[String\] Jeton utilisé pour authentifier le client.
 Il est fournit par le serveur via la méthode RPC
 \'Authenticate\'.

- - \*\*i2pcontrol.address -- \[null\] Rendu si l'adresse a été
 changée
 - \*\*i2pcontrol.password -- \[null\] Rendu si le paramètre a été
 changé
 - \*\*i2pcontrol.port -- \[null\] Rendu si le paramètre a été
 changé
 - SettingsSaved -- \[Boolean\] Retourne vrai si un quelconque
 changement a été fait.
 - RestartNeeded -- \[Boolean\] Retourne vrai si un quelconque
 changement nécessitant un redémarrage pour prendre effet a été
 fait.

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
 - Token -- \[String\] Jeton utilisé pour authentifier le client.
 Il est fournit par le serveur via la méthode RPC
 \'Authenticate\'.

- - \*\*i2p.router.status -- \[String\] L'état du routeur. A
 free-format, translated string intended for display to the user.
 May include information such as whether the router is accepting
 participating tunnels. Content is implementation-dependent.
 - \*\*i2p.router.uptime -- \[long\] La durée d'activité du routeur
 en ms. Note: i2pd routers prior to version 2.41 returned this
 value as a string. For compatibility, clients should handle both
 string and long.
 - \*\*i2p.router.version -- \[String\] Quelle version d'I2P le
 routeur exécute.
 - \*\*i2p.router.net.bw.inbound.1s -- \[double\] La moyenne, en 1
 seconde, de bande passante entrante en Bps.
 - \*\*i2p.router.net.bw.inbound.15s -- \[double\] La moyenne, en
 15 secondes, de bande passante entrante en Bps.
 - \*\*i2p.router.net.bw.outbound.1s -- \[double\] La moyenne sur 1
 seconde de bande passante sortante en Bps.
 - \*\*i2p.router.net.bw.outbound.15s -- \[double\] La moyenne sur
 15 secondes de bande passante sortante en Bps.
 - \*\*i2p.router.net.status -- \[long\] L'état actuel du réseau.
 Selon l'énumération ci-dessous :
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
 - \*\*i2p.router.net.tunnels.participating -- \[long\] À combien
 de tunnels participons-nous sur le réseau I2P.
 - \*\*i2p.router.netdb.activepeers -- \[long\] Avec combien de
 pairs avons-nous communiqué récemment.
 - \*\*i2p.router.netdb.fastpeers -- \[long\] Combien de pairs sont
 considérés \'rapides\'.
 - \*\*i2p.router.netdb.highcapacitypeers -- \[long\] Le nombre de
 pairs considérés à « grande capacité ».
 - \*\*i2p.router.netdb.isreseeding -- \[boolean\] Le routeur
 réensemence-t-il des hôtes vers son NetDB ?
 - \*\*i2p.router.netdb.knownpeers -- \[long\] Combien de pairs
 nous sont connus (listés dans notre NetDB).

```{=html}
<!-- -->
```
- - \*FindUpdates -- \[n/a\] **Blocking**. Initiates a search for
 signed updates.
 - \*Reseed -- \[n/a\] Démarre un réensemencement du routeur, en
 récupérant des pairs dans notre NetDB depuis un hôte distant.
 - \*Restart -- \[n/a\] Redémarre le routeur.
 - \*RestartGraceful -- \[n/a\] Redémarre le routeur
 respectueusement (attend l'expiration des tunnels participants).
 - \*Shutdown -- \[n/a\] Arrête le routeur.
 - \*ShutdownGraceful -- \[n/a\] Éteint le routeur respectueusement
 (attend l'expiration des tunnels participants).
 - \*Update -- \[n/a\] Initiates a router update from signed
 sources.
 - Token -- \[String\] Jeton utilisé pour authentifier le client.
 Il est fournit par le serveur via la méthode RPC
 \'Authenticate\'.

- - \*\*FindUpdates -- \[boolean\] **Blocking**. Returns true iff a
 signed update has been found.
 - \*\*Reseed -- \[null\] Si demandé, vérifie qu'un réensemencement
 a démarré.
 - \*\*Restart -- \[null\] Si demandé, vérifie qu'un redémarrage a
 été amorcé.
 - \*\*RestartGraceful -- \[null\] Si demandé, vérifie qu'un
 redémarrage respectueux a été amorcé.
 - \*\*Shutdown -- \[null\] Si demandé, vérifie si une fermeture a
 été amorcée.
 - \*\*ShutdownGraceful -- \[null\] Si demandé, vérifie qu'une
 fermeture respectueuse a été amorcée.
 - \*\*Update -- \[String\] **Blocking**. If requested, returns the
 status of the the update

```{=html}
<!-- -->
```
- - \*i2p.router.net.ntcp.port -- \[String\] Quel port est utilisé
 pour le transport de TCP. Si nul est soumis, le paramètre actuel
 sera rendu.
 - \*i2p.router.net.ntcp.hostname -- \[String\] Quel nom d'hôte est
 utilisé pour le transport de TCP. Si nul est soumis, le
 paramètre courant sera rendu.
 - \*i2p.router.net.ntcp.autoip -- \[String\] Utilise l'IP détectée
 automatiquement pour le transport de TCP. Si une valeur nulle
 est soumise, c'est le paramètre actuel sera rendu.
 - \*i2p.router.net.ssu.port -- \[String\] Quel port est utilisé
 pour le transport d'UDP. Si une valeur nulle est soumise, c'est
 le paramètre actuel qui sera rendu.
 - \*i2p.router.net.ssu.hostname -- \[String\] Quel est lke nom
 d'hôte utilisé pour le transport d'UDP. Si une valeur nulle est
 soumise, c'est le paramètre actuel qui sera rendu.
 - \*i2p.router.net.ssu.autoip -- \[String\] Quelles sont les
 méthodes qui devraient être utilisées pour détecter l'adresse IP
 du transport UDP. Si une valeur nulle est soumise, c'est le
 paramètre actuel qui sera rendu.
 - \*i2p.router.net.ssu.detectedip -- \[null\] Quelle IP a été
 détectée par le transport UDP.
 - \*i2p.router.net.upnp -- \[String\] UPnP est-il permis. Si une
 valeur nulle est soumise, c'est le paramètre actuel qui sera
 rendu.
 - \*i2p.router.net.bw.share -- \[String\] Quel est le pourcentage
 de bande passante utilisable pour des tunnels de participation.
 Si une valeur nulle est soumise, c'est le paramètre courant qui
 sera rendu.
 - \*i2p.router.net.bw.in -- \[String\] Bande passante entrante
 autorisée en ko/s. Si une valeur nulle est envoyée, le paramètre
 actuel sera retourné.
 - \*i2p.router.net.bw.out -- \[String\] Bande passante sortante
 autorisée en ko/s. Si une valeur nulle est envoyée, le paramètre
 actuel sera retourné.
 - \*i2p.router.net.laptopmode -- \[String\] Le mode ordinateur
 portable est-il activé (changer l'identité du routeur et le port
 UDP si l'IP change) ? Si une valeur nulle est envoyée, le
 paramètre actuel sera retourné.
 - Token -- \[String\] Token used for authenticating the client. Is
 provided by the server via the \'Authenticate\' RPC method. If
 null is submitted, current setting will be returned.

- - Note: i2pd routers prior to version 2.41 returned some of these
 values as numbers. For compatibility, clients should handle both
 strings and numbers.
 - \*\*i2p.router.net.ntcp.port -- \[String\] Si demandé, retourne
 le port utilisé pour le transport TCP.
 - \*\*i2p.router.net.ntcp.hostname -- \[String\] If requested,
 returns the hostname used for the TCP transport.
 - \*\*i2p.router.net.ntcp.autoip -- \[String\] If requested,
 returns the method used for automatically detecting ip for the
 TCP transport.
 - \*\*i2p.router.net.ssu.port -- \[String\] Si demandé, retourne
 le port utilisé pour le transport UDP.
 - \*\*i2p.router.net.ssu.hostname -- \[String\] If requested,
 returns the hostname used for the UDP transport.
 - \*\*i2p.router.net.ssu.autoip -- \[String\] If requested,
 returns methods used for detecting the ip address of the UDP
 transport.
 - \*\*i2p.router.net.ssu.detectedip -- \[String\] If requested,
 returns what ip has been detected by the UDP transport.
 - \*\*i2p.router.net.upnp -- \[String\] Si demandé, retourne le
 paramètre UPnP.
 - \*\*i2p.router.net.bw.share -- \[String\] If requested, returns
 how many percent of bandwidth is usable for participating
 tunnels.
 - \*\*i2p.router.net.bw.in -- \[String\] If requested, returns how
 many KB/s of inbound bandwidth is allowed.
 - \*\*i2p.router.net.bw.out -- \[String\] If requested, returns
 how many KB/s of outbound bandwidth is allowed.
 - \*\*i2p.router.net.laptopmode -- \[String\] Si demandé, retourne
 le mode ordinateur portable.
 - SettingsSaved -- \[boolean\] Les paramètres fournis ont-ils été
 enregistrés
 - RestartNeeded -- \[boolean\] Is a restart needed for the new
 settings to be used.

```{=html}
<!-- -->
```
- - {\"setting-key\": \"setting-value\", \...} -- \[Map\]

- - {\"setting-key\": \"setting-value\", \...} -- \[Map\]

- - \"setting-key\" -- \[String\]

- 

\* denotes an optional value.

\*\* denotes a possibly occuring return value

### Codes d'erreur

- -32700 -- JSON erreur d'analyse syntaxique.
- -32600 -- Requête invalide.
- -32601 -- Méthode non trouvée.
- -32602 -- Paramètres invalides.
- -32603 -- Erreur interne.

```{=html}
<!-- -->
```
- -32001 -- Mot de passe fourni invalide.
- -32002 -- Aucun jeton d'identification présenté.
- -32003 -- Le jeton d'identification n'existe pas.
- -32004 -- The provided authentication token was expired and will be
 removed.
- -32005 -- The version of the I2PControl API used wasn\'t specified,
 but is required to be specified.
- -32006 -- The version of the I2PControl API specified is not
 supported by I2PControl.


