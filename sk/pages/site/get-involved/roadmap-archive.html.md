 Roadmap 2021-12 

This is an archive of the roadmap for I2P over the course of it\'s
history.

## 2016 - 2020 Releases {#2016}

## 0.9.24 {#v0.9.24}

**Released: January 27, 2016**

- SAM v3.2
- Require Java 7
- NetDB Family
- Remove commons-logging
- Use SSU Extended options to request introduction
- Experimental Sybil analysis tool
- Unit test improvements
- Complete transition to Ed25519 signatures for most routers
- Tunnel Bloom filter fixes
- Bug fixes, translation updates, geoip updates

## 0.9.25 {#v0.9.25}

**Released: March 22, 2016**

- SAM v3.3
- Sybil tool enhancements
- QR codes and identicons
- Crypto speedups
- Router family configuration UI
- Custom icons for non-webapp plugins
- Pure Java key pair generation
- Bug fixes, translation updates, geoip updates

## 0.9.26 {#v0.9.26}

**Released: June 7, 2016**

- New subscription protocol, addressbook support (proposal 112)
- Wrapper 3.5.29
- GMP 6.0 (Debian/Ubuntu packages, new installs)
- Certificate revocations in the news feed
- Debian/Ubuntu/Tails package improvements
- Bug fixes, translation updates, geoip updates

## 0.9.27 {#v0.9.27}

**Released: October 17, 2016**

- SSU IPv6 peer testing (proposal 126)
- Enable tray icon on Windows
- Add outproxy plugin support in SOCKS
- Hidden mode improvements
- SSU peer test fixes
- Initial work on NTCP2
- Initial work on New DH
- GMP 6.0 (In-net updates)

## 0.9.28 {#v0.9.28}

**Released: December 12, 2016**

- IPv6 improvements
- Increase IPv6 MTU (proposal 127)
- Blocklist enhancements (proposal 129)
- Sybil tool enhancements
- Bundled software updates: Jetty, JRobin, Tomcat, Wrapper, Zxing
- Fixes for Java 9
- Improved self-signed certificates
- Bug fixes, translation updates, geoip updates

## 0.9.29 {#v0.9.29}

**Released: February 27, 2017**

- More fixes for Java 9
- NTP hardening and IPv6 support
- Same-origin referer pass through
- BOB database refactor
- Preliminary Docker support
- Translated man pages
- I2PBote release 0.4.5
- stats.i2p accepts authentication strings (proposal #112)
- Streaming test harness
- Bug fixes, translation updates, geoip updates

## 0.9.30 {#v0.9.30}

**Released: May 3, 2017**

- Hidden service server sigtype migration (publish dual LS)
- Tomcat 8 / Jetty 9.2
- Stretch/Zesty support
- i2ptunnel authentication page improvements and fixes
- Introducer expiration (proposal #133)
- I2PBote release 0.4.6
- i2psnark-rpc plugin
- Bug fixes, translation updates, geoip updates

## 0.9.31 {#v0.9.31}

**Released: August 7, 2017**

- Console redesign phase 1 (\"refresh\") (ticket #738)
- Move /peers HTML code to console, remove from Android
- i2psnark ratings and comments
- Launch I2P Summer of Dev 2
- Bug fixes, translation updates, geoip updates

## 0.9.32 {#v0.9.32}

**Released: November 7, 2017**

- Ignore hostnames in router infos (proposal #141)
- UI fixes
- Bug fixes, translation updates, geoip updates

## 0.9.33 {#v0.9.33}

**Released: January 30, 2018**

- Reseed support for proxies
- Enable tray app on OSX
- Jetty 9.2.22, Tomcat 8.5.23, Wrapper 3.5.34
- Console CSS fixes and improvements
- Susimail fixes, improvements, refactoring part 1
- Streaming bug fixes
- Android fixes
- Bote fixes
- Debian packaging changes and improvements, dependency changes
- Bug fixes, translation updates, geoip updates

## 0.9.34 {#0.9.34}

**Released: April 10, 2018**

- Susimail fixes, improvements, refactoring part 2
- I2PControl plugin fixed
- UPnP support for IGD 2
- IPv6 address selection improvements
- Better tunnel peer selection for hidden and IPv6-only modes
- Prep for HTTPS console and I2P Site by default
- Prep for splitting up Debian package
- Mac OS X installer, dock, tray enhancements (research and initial
 work)
- Bug fixes, translation updates, geoip updates

## 0.9.35 {#0.9.35}

**Released: June 26, 2018**

- Jetty 9.2.24
- Tomcat 8.5.30
- Susimail folders, background sending
- Improved support for SSL console and I2P Site
- Bug fixes, translation updates, geoip updates
- Progress on proposal #111 (NTCP2)
- Progress on Mac OS X installer, dock, tray enhancements

## 0.9.36 {#0.9.36}

**Released: August 23, 2018**

- NTCP2 (disabled by default)
- Jetty 9.2.25
- Progress on proposal #123 (LS2 with multi-destination support)
- Initial research on ElGamal replacement (\"new crypto\" / proposal
 #142)
- Capacity improvements: discussions, research, preliminary
- Streaming improvements
- Performance improvements
- NTCP Pumper improvements
- EdDSA updates

## 0.9.37 {#0.9.37}

**Released: October 4, 2018**

- NTCP2 (enabled by default)
- Android i2ptunnel SSL crash fix

## 0.9.38 {#0.9.38}

**Released: January 22, 2019**

- New setup wizard with bandwidth testing
- Beta Mac OS X installer, dock, tray enhancements
- Signed Windows installer
- Signed Firefox profile installer
- Preliminary floodfill support for LS2
- Sybil tool background analysis
- Switch to Maxmind GeoLite2 GeoIP format
- Switch JSON lib to json-simple, add Debian dependency
- New light background
- Orchid plugin fixes
- AppArmor fixes
- Continue work on ECIES-X25519 support (proposal #144)

## 0.9.39 {#0.9.39}

**Released: March 21, 2019**

- Redesigned website home page
- Reduce themes (ticket #2272)
- Replacement icons for console home page
- Continue work on testnet
- Floodfill and client encrypted LS2 support (proposal #123)
- LS2 client-side support (proposal #123)
- Add option to disable NTCP1
- Bundle i2pcontrol
- AppArmor fixes
- starting investigation of zerodeps jre
- starting investigation of monolithic installer
- Have apt-transport-i2p and all of its dependencies on-track for
 inclusion in Debian (sam3 and gosam, the Go i2p application
 libraries), include in PPA/Project repo
- Write beginner application development guides for SAM applications
- Start community PPA and application development (sub)forums
- Write materials for newbies on Medium
- Complete preferences dialog on the OSX Launcher
- Feature for running devbuilds with OSX Launcher

## 0.9.40 {#0.9.40}

**Released: May 7, 2019**

- New icons
- I2CP and router support for decrypting LS2 (proposal #123)
- Router decryption of LS2 support (proposal #123)
- Router-side meta LS2 support (proposal #123)
- Continue work on ECIES-X25519 support (proposal #144)
- Start work on Network ID detection (proposal #147)
- Start work on BLAKE2b sig types (proposal #148)
- Implement base 32 for encrypted LS2 (proposal #149)
- Document protocol for meta LS2 backend (proposal #150)
- Disable NTCP1
- Signed Windows installer
- Scripted connection filter for streaming
- geti2p/i2p docker image available at our download page
- osx: theme selection
- osx: auto updater
- osx: upgrade to newer swift version
- Browser identity management UI WebExtension for i2p Browser build
- Browser tunnel identity management UI WebExtension for i2p Browser
 build
- Browser news/documentation inclusion WebExtension for i2p Browser
 build
- Onboarding improvements
- Self-installing client/service demos for nginx(server only),
 ssh/sshd, and Mattermost client/server using split i2ptunnel
 configuration and apt
- Port any maintainable, i2p-native bittorrent client to be apt-get
 installable in Debian, likely BiglyBT or XD
- Produce ISO for \"I2P Linux Distro Redux\" Project using these
 features
- Fix I2P-bote Android
- Fix I2P-bote seeds
- goSam - Up to SAM 3.2, better default signatures.
- sam3 - Up to SAM 3.2, better default signatures. Streaming,
 datagrams, and raw. General improvements.
- jsam - Further development
- Better support / encourage translation efforts
- Android fixes

## 0.9.41 {#0.9.41}

**Released: July 3, 2019**

- Redesigned website navigation menu
- New console icons and logos
- Router-side meta LS2 support (proposal #123)
- UI for per-client encrypted LS2 (proposal #123)
- Continue work on ECIES-X25519 support (proposal #144)
- Implement base 32 for encrypted LS2 (proposal #149)
- GMP 6.1.2 (ticket #1869), partial
- Wrapper 3.5.39
- Wrapper for armv7 and aarch64
- IzPack 5 for non-Windows installers
- browser: new release, upstream tor changes, minor changes
- Browser identity management UI WebExtension for i2p Browser build
- Browser news/documentation inclusion WebExtension for i2p Browser
 build
- Android GMP 6 and 64-bit jbigi
- Android fixes

## 0.9.42 {#0.9.42}

**Released: August 27, 2019**

- Browser web extensions
- Self-installing demos of popular apps/services
- ISO for Linux distro
- Translation efforts
- ECIES Proposal 144 (continuing)
- GMP 6.1.2
- Network ID detection Prop 147
- Split configuration
- Android fixes

## 0.9.43 {#0.9.43}

**Released: October 22, 2019**

- Docker image documentation and promotion to first-class product
- I2P browser: Embed router
- I2P browser: Delay the user dialog
- I2P browser: JSON-RPC2 client for router communication
- I2P browser: Fix NoScript
- I2P browser releases: beta 5, 6; v3.0 based on 68.1 ESR
- I2CP blinding info message
- Proxy page for encrypted LS2 credentials
- Android client library release
- ECIES Proposal 144 (continuing)
- Setup wizard improvements
- Revamped website navigation menu
- Android fixes
- Android battery permission

## 0.9.44 {#0.9.44}

**Released: December 1, 2019**

- Testnet k8s definitions
- ruby gem (ji2p, initial code to be used to control many routers in
 k8s)
- k8s internal communication test with routers using network impl.
 flannel
- k8s ingress definitions (how to make outside contact the router(s)
 inside k8s)
- I2P Browser: See [Browser roadmap](../browser/roadmap)
- IPv6 fixes
- SSU performance improvements
- Faster router startup
- Console improvements
- ECIES Proposal 144 initial implementation
- Donation page redesign and backend (development)

## 0.9.45 {#0.9.45}

**Released: February 25, 2020**

- Hidden mode fixes
- Bandwidth test fixes
- ECIES Proposal 144 testing, fixes
- Susimail login page improvements
- LibSam - deduplication, documentation, support
- Console theme modernization(Light and Dark)
- Consistency with modern themes for SusiDNS, SusiMail apps
- Leftover light theme nits
 - border colours that are still present
 - download sidebar status is still gradient filled
 - take out network status icons? Replace with colours from style
 guide?
 - go over icons on every page and evaluate
 - try I2P blue icons on /home
 - buttons / tabs consistency
- Dark Theme
 - Carry over tabs/ buttons decisions
 - decide on theme colour
- Susi Mail Light & Dark
 - Remove icon bloat
 - make buttons rounded
 - remove gradient on login page
 - add a product description to login page
 - \*\*change icon colours for themes

## 0.9.46 {#0.9.46}

**Released: May 25, 2020**

- Replace jrobin with rrd4j
- ECIES Proposal 144 testing, fixes, completion
- ECIES lookup replies
- i2ptunnel edit page redesign
- Streaming performance improvements
- Start migrating deb.i2p2.no
- Android fixes
- Long-term strategy for website
- Identity and Values Workshops
- Branding Foundations Work
- Information Architecture Sprint : Console and Website
- Console Interface Redesign prototypes
- Console Interface Usability Testing
- Reproducible build fix
- Streaming fixes
- UPnP fixes

## 0.9.47 {#0.9.47}

**Released: August 24, 2020**

- Require Java 8
- Jetty 9.3.x
- json-simple 2.3.0
- RRD4j 3.6
- ECIES enabled by default for some tunnels
- Increase streaming MTU for ECIES connections
- Enable Sybil analysis and blocking by default
- Begin transition to Git
- Improvements to the Bandwidth Setup/Welcome Wizard imagery and text
- Ongoing refinements to new dark and light theme
- Find and replace inconsistent icons from the router console
- Bug Fixes on Android versions later than 8.0
- Hide empty sections on router console home page
- Operators guides for reseed services
- Detailed install guide for the main I2P Java distribution
- Begin implementing Information Architecture improvements to
 geti2p.net
- Identify and Publish information about critical infrastructures(VCS,
 website, reseeds, repositories, mirrors)
- Publish log retention policy Recommendations and Guidelines for
 service admins
- In depth blog entries on: Site Hosting/Service operation, Project
 Services, Policy Recommendations
- Release(Tag)-time \"git bundle\" generation and distribution by
 either HTTP or Bittorrent.

## 0.9.48 {#0.9.48}

**Released: December 1, 2020**

- ECIES router tunnel build record
- Avoid old DSA-SHA1 routers
- Block same-country connections when in hidden mode
- Deprecate BOB
- Drop support for Xenial
- Ratchet efficiency improvements and memory reduction
- Randomize SSU intro key
- Enable system tray for Linux KDE and LXDE
- More SSU performance improvements
- Continue transition to Git
- Operators guides for reseed services
- Windows Installer \"Install as Windows Service\" bugfixes and
 improvements.
- Implement controlled vocabuary as part of Information Architecture
 improvements
- Alternate destination header/meta tag for web sites offering I2P
 mirrors
- Snark in the Browser: Use torrents as alternates sources for
 resources embedded in an I2P Site
- Snark in the Browser: Demo a torrent-backed web page
- finish ji2p-cluster which adds the k8s part of the code
- Publish reasonable contact information for infrastructure admins

## 0.9.49 {#0.9.49}

**Released: February 17, 2021**

- SSU send individual fragments
- SSU Westwood+
- SSU fast retransmit
- SSU fix partial acks
- ECIES router encrypted messages
- Start rekeying routers to ECIES
- Start work on new tunnel build message (proposal 157)
- More SSU performance improvements
- i2psnark webseed support
- Start work on i2psnark hybrid v2 support
- Move web resources to wars
- Move resources to jars
- Fix Gradle build
- Hidden mode fixes
- Change DoH to RFC 8484
- Fix \"Start on Boot\" support on Android
- Add support for copying b32 addresses from the tunnels panel on I2P
 for Android client
- Add SAMv3 Support to I2P for Android
- Revise CSS on the default I2P Site to resemble console Light theme
- Document setup/configuration of default I2P site on the project site
- Add icons and symbols used in I2P router console Light theme to
 router console Dark theme
- Complete transition to Git
- Donation page redesign and backend (deployment)
- Review and update information about VCS, Code Repositories, and
 Mirrors across the entire website.

## 0.9.50 {#0.9.50}

**Released: May 18, 2021**

- Accelerate rekeying routers to ECIES
- UPnP IPv6 support
- 4/6 router address caps (proposal 158)
- IPv6 introducers (proposal 158)
- NTP year 2036 fixes
- Continue work on new tunnel build message (proposal 157)
- Enable DoH for reseeding
- Docker improvements
- SSU IPv6 fixes
- Persist Sybil blocklist
- Tunnel bandwidth limiter fixes


