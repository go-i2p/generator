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

I2PControl is by default listening on https://localhost:7650

## API, Version 1.

Parameters are only provided in a named way (maps).

#### JSON-RPC 2-Format

Request: { \"id\": \"id\", \"method\":
\"Method-name\", \"params\": { \"Param-key-1\": \"param-value-1\",
\"Param-key-2\": \"param-value-2\", \"Token\": \"\*\*actual token\*\*\"
}, \"jsonrpc\": \"2.0\" } Response: { \"id\": \"id\", \"result\": { \"Result-key-1\":
\"result-value-1\", \"Result-key-2\": \"result-value-2\" }, \"jsonrpc\":
\"2.0\" } 

- - Param-key-1 -- Description
 - Param-key-2 -- Description
 - Token -- Token used for authenticating every request (excluding
 the \'Authenticate\' RPC method)

- - Result-key-1 -- Description
 - Result-key-2 -- Description

#### Implementierte Methoden

- - API -- \[long\] Die vom Client verwendete Version der
 I2PControl-API.
 - Password -- \[String\] The password used for authenticating
 against the remote server.

- - API -- \[long\] The primary I2PControl API version implemented
 by the server.
 - Token -- \[String\] The token used for further communication.

```{=html}
<!-- -->
```
- - Echo -- \[String\] Wert wird in der Antwort zurückgegeben.
 - Token -- \[String\] Token used for authenticating the client. Is
 provided by the server via the \'Authenticate\' RPC method.

- - Result -- \[String\] Value of the key \'echo\' in the request.

```{=html}
<!-- -->
```
- - Stat -- \[String\] Determines which
 rateStat to fetch, see
 [ratestats]().
 - Period -- \[long\] Determines which period a stat is fetched
 for. Measured in ms.
 - Token -- \[String\] Token used for authenticating the client. Is
 provided by the server via the \'Authenticate\' RPC method.

- - Result -- \[double\] Returns the average value for the requested
 rateStat and period.

```{=html}
<!-- -->
```
- - \*i2pcontrol.address -- \[String\] Sets a new listen address for
 I2PControl (only 127.0.0.1 and 0.0.0.0 are implemented in
 I2PControl currently).
 - \*i2pcontrol.password -- \[String\] Sets a new password for
 I2PControl, all Authentication tokens will be revoked.
 - \*i2pcontrol.port -- \[String\] Switches which port I2PControl
 will listen for connections on.
 - Token -- \[String\] Token used for authenticating the client. Is
 provided by the server via the \'Authenticate\' RPC method.

- - \*\*i2pcontrol.address -- \[null\] Returned if address was
 changed
 - \*\*i2pcontrol.password -- \[null\] Returned if setting was
 changed
 - \*\*i2pcontrol.port -- \[null\] Returned if setting was changed
 - SettingsSaved -- \[Boolean\] Returns true if any changes were
 made.
 - RestartNeeded -- \[Boolean\] Returns true if any changes
 requiring a restart to take effect were made.

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
 - Token -- \[String\] Token used for authenticating the client. Is
 provided by the server via the \'Authenticate\' RPC method.

- - \*\*i2p.router.status -- \[String\] What the status of the
 router is. A free-format, translated string intended for display
 to the user. May include information such as whether the router
 is accepting participating tunnels. Content is
 implementation-dependent.
 - \*\*i2p.router.uptime -- \[long\] What the uptime of the router
 is in ms. Note: i2pd routers prior to version 2.41 returned this
 value as a string. For compatibility, clients should handle both
 string and long.
 - \*\*i2p.router.version -- \[String\] What version of I2P the
 router is running.
 - \*\*i2p.router.net.bw.inbound.1s -- \[double\] The 1 second
 average inbound bandwidth in Bps.
 - \*\*i2p.router.net.bw.inbound.15s -- \[double\] The 15 second
 average inbound bandwidth in Bps.
 - \*\*i2p.router.net.bw.outbound.1s -- \[double\] The 1 second
 average outbound bandwidth in Bps.
 - \*\*i2p.router.net.bw.outbound.15s -- \[double\] The 15 second
 average outbound bandwidth in Bps.
 - \*\*i2p.router.net.status -- \[long\] What the current network
 status is. According to the below enum:
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
 - \*\*i2p.router.net.tunnels.participating -- \[long\] How many
 tunnels on the I2P net are we participating in.
 - \*\*i2p.router.netdb.activepeers -- \[long\] How many peers have
 we communicated with recently.
 - \*\*i2p.router.netdb.fastpeers -- \[long\] How many peers are
 considered \'fast\'.
 - \*\*i2p.router.netdb.highcapacitypeers -- \[long\] How many
 peers are considered \'high capacity\'.
 - \*\*i2p.router.netdb.isreseeding -- \[boolean\] Is the router
 reseeding hosts to its NetDB?
 - \*\*i2p.router.netdb.knownpeers -- \[long\] How many peers are
 known to us (listed in our NetDB).

```{=html}
<!-- -->
```
- - \*FindUpdates -- \[n/a\] **Blocking**. Initiates a search for
 signed updates.
 - \*Reseed -- \[n/a\] Initiates a router reseed, fetching peers
 into our NetDB from a remote host.
 - \*Restart -- \[n/a\] Startet den Router neu.
 - \*RestartGraceful -- \[n/a\] Restarts the router gracefully
 (waits for participating tunnels to expire).
 - \*Shutdown -- \[n/a\] Fährt den Router herunter.
 - \*ShutdownGraceful -- \[n/a\] Shuts down the router gracefully
 (waits for participating tunnels to expire).
 - \*Update -- \[n/a\] Initiates a router update from signed
 sources.
 - Token -- \[String\] Token used for authenticating the client. Is
 provided by the server via the \'Authenticate\' RPC method.

- - \*\*FindUpdates -- \[boolean\] **Blocking**. Returns true iff a
 signed update has been found.
 - \*\*Reseed -- \[null\] If requested, verifies that a reseed has
 been initiated.
 - \*\*Restart -- \[null\] If requested, verifies that a restart
 has been initiated.
 - \*\*RestartGraceful -- \[null\] If requested, verifies that a
 graceful restart has been initiated.
 - \*\*Shutdown -- \[null\] If requested, verifies that a shutdown
 has been initiated
 - \*\*ShutdownGraceful -- \[null\] If requested, verifies that a
 graceful shutdown has been initiated
 - \*\*Update -- \[String\] **Blocking**. If requested, returns the
 status of the the update

```{=html}
<!-- -->
```
- - \*i2p.router.net.ntcp.port -- \[String\] What port is used for
 the TCP transport. If null is submitted, current setting will be
 returned.
 - \*i2p.router.net.ntcp.hostname -- \[String\] What hostname is
 used for the TCP transport. If null is submitted, current
 setting will be returned.
 - \*i2p.router.net.ntcp.autoip -- \[String\] Use automatically
 detected ip for TCP transport. If null is submitted, current
 setting will be returned.
 - \*i2p.router.net.ssu.port -- \[String\] What port is used for
 the UDP transport. If null is submitted, current setting will be
 returned.
 - \*i2p.router.net.ssu.hostname -- \[String\] What hostname is
 used for the UDP transport. If null is submitted, current
 setting will be returned.
 - \*i2p.router.net.ssu.autoip -- \[String\] Which methods should
 be used for detecting the ip address of the UDP transport. If
 null is submitted, current setting will be returned.
 - \*i2p.router.net.ssu.detectedip -- \[null\] What ip has been
 detected by the UDP transport.
 - \*i2p.router.net.upnp -- \[String\] Is UPnP enabled. If null is
 submitted, current setting will be returned.
 - \*i2p.router.net.bw.share -- \[String\] How many percent of
 bandwidth is usable for participating tunnels. If null is
 submitted, current setting will be returned.
 - \*i2p.router.net.bw.in -- \[String\] How many KB/s of inbound
 bandwidth is allowed. If null is submitted, current setting will
 be returned.
 - \*i2p.router.net.bw.out -- \[String\] How many KB/s of outbound
 bandwidth is allowed. If null is submitted, current setting will
 be returned.
 - \*i2p.router.net.laptopmode -- \[String\] Is laptop mode enabled
 (change router identity and UDP port when IP changes ). If null
 is submitted, current setting will be returned.
 - Token -- \[String\] Token used for authenticating the client. Is
 provided by the server via the \'Authenticate\' RPC method. If
 null is submitted, current setting will be returned.

- - Note: i2pd routers prior to version 2.41 returned some of these
 values as numbers. For compatibility, clients should handle both
 strings and numbers.
 - \*\*i2p.router.net.ntcp.port -- \[String\] If requested, returns
 the port used for the TCP transport.
 - \*\*i2p.router.net.ntcp.hostname -- \[String\] If requested,
 returns the hostname used for the TCP transport.
 - \*\*i2p.router.net.ntcp.autoip -- \[String\] If requested,
 returns the method used for automatically detecting ip for the
 TCP transport.
 - \*\*i2p.router.net.ssu.port -- \[String\] If requested, returns
 the port used for the UDP transport.
 - \*\*i2p.router.net.ssu.hostname -- \[String\] If requested,
 returns the hostname used for the UDP transport.
 - \*\*i2p.router.net.ssu.autoip -- \[String\] If requested,
 returns methods used for detecting the ip address of the UDP
 transport.
 - \*\*i2p.router.net.ssu.detectedip -- \[String\] If requested,
 returns what ip has been detected by the UDP transport.
 - \*\*i2p.router.net.upnp -- \[String\] If requested, returns the
 UPNP setting.
 - \*\*i2p.router.net.bw.share -- \[String\] If requested, returns
 how many percent of bandwidth is usable for participating
 tunnels.
 - \*\*i2p.router.net.bw.in -- \[String\] If requested, returns how
 many KB/s of inbound bandwidth is allowed.
 - \*\*i2p.router.net.bw.out -- \[String\] If requested, returns
 how many KB/s of outbound bandwidth is allowed.
 - \*\*i2p.router.net.laptopmode -- \[String\] If requested,
 returns the laptop mode.
 - SettingsSaved -- \[boolean\] Have the provided settings been
 saved.
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

### Fehlercodes

- -32700 -- JSON parse error.
- -32600 -- Ungültige Anfrage
- -32601 -- Methode nicht gefunden.
- -32602 -- Ungültige Parameter.
- -32603 -- Interner Fehler.

```{=html}
<!-- -->
```
- -32001 -- Invalid password provided.
- -32002 -- No authentication token presented.
- -32003 -- Authentication token doesn\'t exist.
- -32004 -- The provided authentication token was expired and will be
 removed.
- -32005 -- The version of the I2PControl API used wasn\'t specified,
 but is required to be specified.
- -32006 -- The version of the I2PControl API specified is not
 supported by I2PControl.


