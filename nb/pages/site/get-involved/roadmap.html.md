 Roadmap 2025-04 

This is the official project roadmap for the desktop and Android Java
I2P releases only. Some related tasks for resources such as the website
and plugins may be included.

For details and discussion on specific items, search on gitlab or
zzz.i2p. For contents of past releases, see the release notes. For other
project goals, see the meeting notes.

We do not maintain separate unstable and stable branches or releases. We
have a single, stable release path. Our typical release cycle is about
13 weeks.

Older releases are at the bottom of the page.

## 2.10.0 (API 0.9.67) {#2.10.0}

**Target release: Late August 2025**

- UDP tracker support (prop. 160)
- Implement LS service record parameter (prop. 167)
- Continue work on PQ (prop. 169); Start checking in MLKEM parts of PQ
 (prop. 169)
- Tunnel build bandwidth parameters (prop. 168) Part 2 (handling)
- Continue work on per-tunnel throttling
- Stat/graph subsystem cleanup and make prometheus-friendly
- Tomcat update

## 2.9.0 (API 0.9.66) {#2.9.0}

**Target release: June 3, 2025**

- Netdb map
- Implement Datagram2, Datagram3 (prop. 163)
- Start work on LS service record parameter (prop. 167)
- Start work on PQ (prop. 169)
- Continue work on per-tunnel throttling
- Tunnel build bandwidth parameters (prop. 168) Part 1 (sending)
- Use /dev/random for PRNG by default on Linux
- Remove redundant LS render code
- Display changelog in HTML
- Reduce HTTP server thread usage
- Fix auto-floodfill enrollment
- Wrapper update to 3.5.60

## 2.8.2 (API 0.9.65) {#2.8.2}

**Released: March 29, 2025**

- Fix SHA256 corruption bug

## 2.8.1 (API 0.9.65) {#2.8.1}

**Released: March 17, 2025**

- Fix installer failure on Java 21+
- Fix \"loopback\" bug
- Fix tunnel tests for outbound client tunnels
- Fix installing to paths with spaces
- Update outdated Docker container and container libraries
- Console notification bubbles
- SusiDNS sort-by-latest
- Use SHA256 pool in Noise
- Console dark theme fixes and improvements
- .i2p.alt support

## 2.8.0 (API 0.9.65) {#2.8.0}

**Released: February 3, 2025**

- RouterInfo publishing improvements
- Improve SSU2 ACK efficiency
- Improve SSU2 handling of dup relay messages
- Faster / variable lookup timeouts
- LS expiration improvements
- Change symmetric NAT cap
- Enforce POST in more forms
- SusiDNS dark theme fixes
- Bandwidth test cleanups
- New Gan Chinese translation
- Add Kurdish option to UI
- New Jammy build to handle Jetty API change
- Izpack 5.2.3
- rrd4j 3.10

## 2.7.0 (API 0.9.64) {#2.7.0}

**Released: October 8, 2024**

- i2ptunnel HTTP server reduce thread usage
- Generic UDP Tunnels in I2PTunnel
- Browser Proxy in I2PTunnel(Proposal 166)
- Website Migration
- Fix for tunnels going yellow
- Console /netdb refactoring

## 2.6.1 (API 0.9.63) {#2.6.1}

**Released: August 6, 2024**

- Fix iframe size issues in console
- Convert graphs to SVG
- Bundle translation status report in console

## 2.6.0 (API 0.9.63) {#2.6.0}

**Released: July 19, 2024**

- Reduce memory usage for netdb
- Continue removing SSU1 code
- Fix i2psnark temp file leaks and stalls
- More efficient PEX in i2psnark
- JS refresh of graphs in console
- Graph rendering improvements
- Susimail JS search
- More efficient handling of messages at OBEP
- More efficient lookup of local destinations in I2CP
- Fix JS variable scoping issues and concurrency

## 2.5.2 (API 0.9.62) {#2.5.2}

**Released: May 15, 2024**

- HTTP truncation fix
- Publish G cap if symmetric natted
- rrd4j 3.9.1-preview

## 2.5.1 (API 0.9.62) {#2.5.1}

**Released: May 6, 2024**

- NetDB DDoS mitigations
- Add Tor blocklist
- susimail fixes
- susimail search
- Continue removing SSU1 code
- Tomcat 9.0.88

## 2.5.0 (API 0.9.62) {#2.5.0}

**Released: April 8, 2024**

- Console iframe improvements
- Redesign i2psnark bandwidth limiter
- Javascript drag-and-drop for i2psnark and susimail
- i2ptunnel SSL error handling improvements
- i2ptunnel persistent HTTP connection support
- Start removing SSU1 code
- SSU2 relay tag request handling improvements
- SSU2 peer test fixes
- susimail initial loading speedup
- susimail javascript markdown for plain text emails
- susimail HTML email support
- susimail fixes and improvements
- tunnnel peer selection adjustments
- Update RRD4J to 3.9
- Update gradlew to 8.5

## 2.4.0 (API 0.9.61) {#2.4.0}

**Released: December 18, 2023**

- NetDB context management/Segmented NetDB
- Handle congestion capabilities by deprioritizing overloaded routers
- Revive Android helper library
- i2psnark local torrent file selector
- NetDB lookup handler fixes
- Disable SSU1
- Ban routers publishing in the future
- SAM fixes
- susimail fixes
- UPnP fixes

## 2.3.0 (API 0.9.59) {#2.3.0}

**Released: June 28, 2023**

- Tunnel peer selection improvements
- User-Configurable blocklist expiration
- Throttle fast bursts of lookup from same source
- Fix replay detection information leak
- NetDB fixes for multihomed leaseSets
- NetDB fixes for leaseSets which were received as a reply before
 being recieved as a store

## 2.2.1 (API 0.9.58) {#2.2.1}

**Released: April 12, 2023**

- Packaging fixes

## 2.2.0 (API 0.9.58) {#2.2.0}

**Released: March 13, 2023**

- Tunnel peer selection improvements
- Streaming replay fix

## 2.1.0 (API 0.9.57) {#2.1.0}

**Released: January 10, 2023**

- SSU2 fixes
- Tunnel build congestion fixes
- SSU peer test and symmetric NAT detction fixes
- Fix broken LS2 encrypted leasesets
- Option to disable SSU 1 (preliminary)
- Compressible padding (proposal 161)
- New console peers status tab
- Add torsocks support to SOCKS proxy and other SOCKS improvements and
 fixes

## 2.0.0 (API 0.9.56) {#2.0.0}

**Released: November 21, 2022**

- SSU2 connection migration
- SSU2 immediate acks
- Enable SSU2 by default
- SHA-256 digest proxy authentication in i2ptunnel
- Update Android build process to use modern AGP, end need of
 deprecated Maven plugin in Android build
- Cross-Platform(Desktop) I2P browser auto-configuration support

## 1.9.0 (API 0.9.55) {#1.9.0}

**Released: August 22, 2022**

- SSU2 peer test and relay implementation
- SSU2 fixes
- SSU MTU/PMTU improvements
- Enable SSU2 for a small portion of routers
- Add deadlock detector
- More certificate import fixes
- Fix i2psnark DHT restart after router restart

## 1.8.0 (API 0.9.54) {#1.8.0}

**Released: May 23, 2022**

- Router family fixes and improvements
- Soft restart fixes
- SSU fixes and performance improvements
- I2PSnark standalond fixes and improvements
- Avoid Sybil penalty for trusted families
- Reduce tunnel build reply timeout
- UPnP fixes
- Remove BOB source
- Certificate import fixes
- Tomcat 9.0.62
- Refactoring to support SSU2 (proposal 159)
- Initial implementation of SSU2 base protocol (proposal 159)
- SAM authorization popup for Android apps
- Improve support for custom directory installs in i2p.firefox

## 1.7.0 (API 0.9.53) {#1.7.0}

**Released: Feb. 21, 2022**

- Remove BOB
- New i2psnark torrent editor
- i2psnark standalone fixes and improvements
- NetDB reliability improvements
- Add popup messages in systray
- NTCP2 performance improvements
- Remove outbound tunnel when first hop fails
- Fallback to exploratory for tunnel build reply after repeated client
 tunnel build failures
- Restore tunnel same-IP restrictions
- Refactor i2ptunnel UDP support for I2CP ports
- Continue work on SSU2, start implementation (proposal 159)
- Create Debian/Ubuntu Package of I2P Browser Profile
- Create Plugin of I2P Browser Profile
- Document I2P for Android applications
- i2pcontrol improvements
- Plugin support improvements
- New local outproxy plugin
- IRCv3 message tag support

## 1.6.1 (API 0.9.52) {#1.6.1}

**Released: Nov. 29, 2021**

- Accelerate rekeying routers to ECIES
- SSU performance improvements
- Improve SSU peer test security
- Add theme selection to new-install wizard
- Continue work on SSU2 (proposal 159)
- Send new tunnel build messages (proposal 157)
- Include automatic browser configuration tool in IzPack installer
- Make Fork-and-Exec Plugins Managable
- Document jpackage install processes
- Complete, document Go/Java Plugin Generation Tools
- Reseed Plugin - Run a self-signed HTTPS reseed as a Java router
 plugin with no configuration.

## 1.5.0 (API 0.9.51) {#1.5.0}

**Released: Aug. 23, 2021**

- Accelerate rekeying routers to ECIES
- Start work on SSU2
- Implement new tunnel build messages (proposal 157)
- Support dmg and exe automatic updates
- New native OSX installer
- X-I2P-Location(alt-svc) locations for built-in I2P Site
- RRD4J 3.8
- Create C, CGo, SWIG bindings for libi2pd

#### [Looking for older releases? Check the roadmap archive by following this link.](roadmap-archive)


