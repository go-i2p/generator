 Naming and Address
Book 2025-01 0.9.65 

## Prezentare generală {#overview}

I2P este livrat cu o bibliotecă de denumire generică și o implementare
de bază proiectata pentru a calcula un nume local la cartografierea
destinației, precum și o aplicație suplimentară numită [agenda de
adrese](#addressbook). I2P acceptă de asemenea [nume de gazdă
Base32](#base32) similare cu adresele .onion ale lui Tor.

The address book is a web-of-trust driven secure, distributed, and human
readable naming system, sacrificing only the call for all human readable
names to be globally unique by mandating only local uniqueness. While
all messages in I2P are cryptographically addressed by their
destination, different people can have local address book entries for
\"Alice\" which refer to different destinations. People can still
discover new names by importing published address books of peers
specified in their web of trust, by adding in the entries provided
through a third party, or (if some people organize a series of published
address books using a first come first serve registration system) people
can choose to treat these address books as name servers, emulating
traditional DNS.

NOTE: For the reasoning behind the I2P naming system, common arguments
against it and possible alternatives see the [naming
discussion]() page.

## Denumirea componentelor sistemului {#components}

În I2P nu există o autoritate de denumire centrală. Toate numele de
gazdă sunt locale.

Sistemul de denumire este destul de simplu și cea mai mare parte a
acestuia este implementată în aplicații externe routerului, dar incluse
în pachet distribuția I2P. Componentele sunt:

1. [Serviciul de denumire](#lookup) local care efectuează căutări de
 asemenea, se ocupă cu [numele de gazdă Base32](#base32).
2. [Proxy HTTP](#httpproxy) care solicită routerului căutări și puncte
 utilizatorul la serviciile de salt la distanță pentru a asista la
 căutările eșuate
3. [Formulare de adăugare de gazdă](#add-services) HTTP care permit
 utilizatorilor să adauge gazde la gazdele lor locale.txt
4. [Servicii de salt](#jump-services) HTTP care oferă propriile lor
 căutări și redirecționare.
5. [Aplicația de adrese](#addressbook) care se contopește extern liste
 de gazde, preluate prin HTTP, cu lista locală.
6. Aplicația [SusiDNS](#susidns), care este un simplu front-end web
 pentru configurarea agendei de adrese și vizualizarea listelor de
 gazdă locale.

## Naming Services {#lookup}

All destinations in I2P are 516-byte (or longer) keys. (To be more
precise, it is a 256-byte public key plus a 128-byte signing key plus a
3-or-more byte certificate, which in Base64 representation is 516 or
more bytes. Non-null
[Certificates](#certificates) are in
use now for signature type indication. Therefore, certificates in
recently-generated destinations are more than 3 bytes.

Dacă o aplicație (i2ptunnel sau proxy HTTP) dorește să acceseze o
destinație pe nume, routerul face o căutare locală foarte simplă pentru
a rezolva acest nume.

### Hosts.txt Naming Service

Hosts.txt Naming Service efectuează o simplă căutare liniară in fișiere
text. Acest serviciu de denumire a fost implicit până la lansarea 0.8.8
când a fost înlocuit de serviciul de numire Blockfile. Formatul
hosts.txt a devenit prea lent după ce fișierul a crescut la mii de
înregistrări.

It does a linear search through three local files, in order, to look up
host names and convert them to a 516-byte destination key. Each file is
in a simple [configuration file
format](), with hostname=base64, one per
line. The files are:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile Naming Service

Serviciul de denumire Blockfile stochează mai multe „adrese" într-un
singur fișier de bază de date numit hostsdb.blockfile. Acest serviciu de
denumire este implicit de la lansarea 0.8.8.

A blockfile is simply on-disk storage of multiple sorted maps (key-value
pairs), implemented as skiplists. The blockfile format is specified on
the [Blockfile page](). It provides fast
Destination lookup in a compact format. While the blockfile overhead is
substantial, the destinations are stored in binary rather than in Base
64 as in the hosts.txt format. In addition, the blockfile provides the
capability of arbitrary metadata storage (such as added date, source,
and comments) for each entry to implement advanced address book
features. The blockfile storage requirement is a modest increase over
the hosts.txt format, and the blockfile provides approximately 10x
reduction in lookup times.

On creation, the naming service imports entries from the three files
used by the hosts.txt Naming Service. The blockfile mimics the previous
implementation by maintaining three maps that are searched in-order,
named privatehosts.txt, userhosts.txt, and hosts.txt. It also maintains
a reverse-lookup map to implement rapid reverse lookups.

### Other Naming Service Facilities

The lookup is case-insensitive. The first match is used, and conflicts
are not detected. There is no enforcement of naming rules in lookups.
Lookups are cached for a few minutes. Base 32 resolution is [described
below](#base32). For a full description of the Naming Service API see
the [Naming Service Javadocs](). This API
was significantly expanded in release 0.8.7 to provide adds and removes,
storage of arbitrary properties with the hostname, and other features.

### Alternatives and Experimental Naming Services

The naming service is specified with the configuration property
`i2p.naming.impl=class`. Other implementations are possible. For
example, there is an experimental facility for real-time lookups (a la
DNS) over the network within the router. For more information see the
[alternatives on the discussion
page](#alternatives).

The HTTP proxy does a lookup via the router for all hostnames ending in
\'.i2p\'. Otherwise, it forwards the request to a configured HTTP
outproxy. Thus, in practice, all HTTP (I2P Site) hostnames must end in
the pseudo-Top Level Domain \'.i2p\'.

Dacă routerul nu reușește să rezolve numele de gazdă, proxy-ul HTTP
revine o pagină de eroare către utilizator cu link-uri către mai multe
servicii de „salt". Vezi mai jos pentru detalii.

## .i2p.alt Domain {#alt}

We previously [applied to reserve the .i2p
TLD](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/)
following the procedures specified in [RFC
6761](https://www.rfc-editor.org/rfc/rfc6761.html). However, this
application and all others were rejected, and RFC 6761 was declared a
\"mistake\".

After many years of work by the GNUnet team and others, the .alt domain
was reserved as a special-use TLD in [RFC
9476](https://www.rfc-editor.org/rfc/rfc9476.html) as of late 2023.
While there are no official registrars sanctioned by IANA, we have
registered the .i2p.alt domain with the primary unofficial registrar
[GANA](https://gana.gnunet.org/dot-alt/dot_alt.html). This does not
prevent others from using the domain, but it should help discourage it.

One benefit to the .alt domain is that, in theory, DNS resolvers will
not forward .alt requests once they update to comply with RFC 9476, and
that will prevent DNS leaks. For compatibility with .i2p.alt hostnames,
I2P software and services should be updated to handle these hostnames by
stripping off the .alt TLD. These updates are scheduled for the first
half of 2024.

At this time, there are no plans to make .i2p.alt the preferred form for
display and interchange of I2P hostnames. This is a topic for further
research and discussion.

## Carte de adrese {#addressbook}

### Abonamente primite și Fuziune

Aplicația de adrese periodice preia fișierele hosts.txt ale altor
utilizatori și fuzionează ei cu gazdele locale.txt, după mai multe
verificări. Conflictele de denumire sunt soluționate pentru un prim
servit primul venit bază.

Abonarea la fișierul hosts.txt al altui utilizator implică oferindu-le o
anumită încredere. Nu le doriți, de exemplu, „deturnează" un site nou
prin introducerea rapidă în propria cheie pentru un nou site înainte de
a trece noua intrare gazdă/cheie.

For this reason, the only subscription configured by default is
`http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`,
which contains a copy of the hosts.txt included in the I2P release.
Users must configure additional subscriptions in their local address
book application (via subscriptions.txt or [SusiDNS](#susidns)).

Some other public address book subscription links:

- [http:///cgi-bin/i2hostetag](http:///cgi-bin/i2hostetag)
- [http:///cgi-bin/newhosts.txt](http:///cgi-bin/newhosts.txt)

Operatorii acestor servicii pot avea diverse politici pentru listarea
gazdelor. Prezența pe această listă nu implică aprobare.

### Reguli de denumire

While there are hopefully not any technical limitations within I2P on
host names, the address book enforces several restrictions on host names
imported from subscriptions. It does this for basic typographical sanity
and compatibility with browsers, and for security. The rules are
essentially the same as those in RFC2396 Section 3.2.2. Any hostnames
violating these rules may not be propagated to other routers.

Reguli de denumire:

- Numele sunt convertite cu litere mici la import.
- Numele sunt verificate pentru a intra în conflict cu numele
 existente în userhosts.txt și hosts.txt existente (dar nu
 privatehosts.txt) după conversie în minuscule.
- Trebuie să conțină numai \[a-z\] \[0-9\] \'. \" și „-" după
 conversie în minuscule.
- Nu trebuie să încep cu \'.\' sau „-".
- Trebuie să se termine cu „.i2p".
- Maximum 67 de caractere, inclusiv „.i2p".
- Nu trebuie să conțină „..".
- Nu trebuie să conțină „.-" sau „-". (începând cu 0.6.1.33).
- Nu trebuie să conțină „-" decât în ​​„xn\--" pentru IDN.
- Numele de gazdă Base32 (\* .b32.i2p) sunt rezervate pentru
 utilizarea bazei 32 și astfel nu este permis să fie importate.
- Certain hostnames reserved for project use are not allowed
 (proxy.i2p, router.i2p, console.i2p, mail.i2p, \*.proxy.i2p,
 \*.router.i2p, \*.console.i2p, \*.mail.i2p, and others)
- Hostnames starting with \'www.\' are discouraged and are rejected by
 some registration services. Some addressbook implementations
 automatically strip \'www.\' prefixes from lookups. So registring
 \'www.example.i2p\' is unnecessary, and registering a different
 destination for \'www.example.i2p\' and \'example.i2p\' will make
 \'www.example.i2p\' unreachable for some users.
- Tastele sunt verificate pentru validitatea bazei 64.
- Cheile sunt verificate pentru a intra în conflict cu cheile
 existente în hosts.txt (dar nu privatehosts.txt).
- Lungimea minimă a cheii 516 octeți.
- Lungimea maximă a cheii 616 bytes (pentru a contabiliza certuri de
 până la 100 de octeți).

Orice nume primit prin abonament care trece toate verificările este
adăugat prin intermediul serviciului de denumire local.

Note that the \'.\' symbols in a host name are of no significance, and
do not denote any actual naming or trust hierarchy. If the name
\'host.i2p\' already exists, there is nothing to prevent anybody from
adding a name \'a.host.i2p\' to their hosts.txt, and this name can be
imported by others\' address book. Methods to deny subdomains to
non-domain \'owners\' (certificates?), and the desirability and
feasibility of these methods, are topics for future discussion.

Denumirile internaționale de domeniu (IDN) funcționează de asemenea în
i2p (folosind formularul punycode „xn\--" ). Pentru a vedea numele de
domeniu IDN .i2p redate corect în bara de locații Firefox, adaugati
\'network.IDN.whitelist.i2p (boolean) = true\' in about:config.

Întrucât aplicația pentru agenda de adrese nu utilizează deloc
privatehosts.txt, în practică acest fișier este singurul loc în care
este potrivit să plasați aliasuri private sau \"nume prietenesti\"
pentru site-urile care se află deja în hosts.txt.

### Formatul avansat de feed pentru abonamente

As of release 0.9.26, subscription sites and clients may support an
advanced hosts.txt feed protocol that includes metadata including
signatures. This format is backwards-compatible with the standard
hosts.txt hostname=base64destination format. See [the
specification](/spec/subscription) for details.

### Abonamente efectuate

Address Book will publish the merged hosts.txt to a location
(traditionally hosts.txt in the local I2P Site\'s home directory) to be
accessed by others for their subscriptions. This step is optional and is
disabled by default.

### Hosting and HTTP Transport Issues

Aplicația de adrese, împreună cu eepget, salvează Etag și / sau
Last-Modified informatii returnate de serverul web al abonamentului.
Acest lucru reduce considerabil lățimea de bandă necesară, așa cum va fi
serverul web întoarceți un „304 Not Modified" pe următoarea operațiune
dacă nu s-a schimbat nimic.

Totuși, întregul hosts.txt este descărcat dacă s-a schimbat. Vezi mai
jos pentru discuții pe această temă.

Gazde care servesc un hosts.txt static sau o aplicație CGI echivalentă
sunt încurajați să livreze un antet cu lungimea conținutului și un antet
Etag sau Ultima modificare. De asemenea, asigurați-vă că serverul
livrează un „304 Nemodificat" atunci când este cazul. Aceasta va reduce
dramatic lățimea de bandă a rețelei și reduce șansele de corupție.

## Servicii de adăugare de gazdă {#add-services}

Un serviciu de adăugare de gazdă este o aplicație CGI simplă care are ca
parametri un nume de gazdă și o cheie Base64 și adaugă asta la gazdele
sale locale.txt. Dacă alți routeri se abonează la acel hosts.txt, noul
nume / cheie gazdă va fi propagat prin rețea.

Se recomandă ca serviciile de adăugare de la gazdă să impună, cel puțin,
restricțiile impuse de aplicația din agenda de adrese menționată mai
sus. Serviciile de adăugare de gazdă pot impune restricții suplimentare
pentru nume de gazdă și chei, de exemplu:

- O limită a numărului de „subdomenii".
- Autorizarea „subdomeniilor" prin diferite metode.
- Certificări Hashcash sau semnate.
- Revizuire editorială a numelor de gazdă și / sau a conținutului.
- Categorizarea gazdelor după conținut.
- Rezervarea sau respingerea anumitor nume de gazdă.
- Restricții privind numărul de nume înregistrate într-o anumită
 perioadă de timp.
- Întârzieri între înregistrare și publicare.
- Cerința ca gazda să fie pregătită pentru verificare.
- Expirare și / sau revocare.
- Respingerea spoofului IDN.

## Servicii de salt {#jump-services}

A jump service is a simple CGI application that takes a hostname as a
parameter and returns a 301 redirect to the proper URL with a
`?i2paddresshelper=key` string appended. The HTTP proxy will interpret
the appended string and use that key as the actual destination. In
addition, the proxy will cache that key so the address helper is not
necessary until restart.

Note that, like with subscriptions, using a jump service implies a
certain amount of trust, as a jump service could maliciously redirect a
user to an incorrect destination.

Pentru a oferi cel mai bun serviciu, ar trebuie ca un serviciu de salt
sa fie abonat mai mulți furnizori de hosts.txt, astfel încât lista sa
gazdă locală să fie actuală.

## SusiDNS

SusiDNS is simply a web interface front-end to configuring address book
subscriptions and accessing the four address book files. All the real
work is done by the \'address book\' application.

Currently, there is little enforcement of address book naming rules
within SusiDNS, so a user may enter hostnames locally that would be
rejected by the address book subscription rules.

## Nume Base32 {#base32}

I2P supports Base32 hostnames similar to Tor\'s .onion addresses. Base32
addresses are much shorter and easier to handle than the full
516-character Base64 Destinations or addresshelpers. Example:
`ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

In Tor, the address is 16 characters (80 bits), or half of the SHA-1
hash. I2P uses 52 characters (256 bits) to represent the full SHA-256
hash. The form is {52 chars}.b32.i2p. Tor has a
[proposal](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013)
to convert to an identical format of {52 chars}.onion for their hidden
services. Base32 is implemented in the naming service, which queries the
router over I2CP to lookup the LeaseSet to get the full Destination.
Base32 lookups will only be successful when the Destination is up and
publishing a LeaseSet. Because resolution may require a network database
lookup, it may take significantly longer than a local address book
lookup.

Base32 addresses can be used in most places where hostnames or full
destinations are used, however there are some exceptions where they may
fail if the name does not immediately resolve. I2PTunnel will fail, for
example, if the name does not resolve to a destination.

## Extended Base32 Names {#newbase32}

Extended base 32 names were introduced in release 0.9.40 to support
encrypted lease sets. Addresses for encrypted leasesets are identified
by 56 or more encoded characters, not including the \".b32.i2p\" (35 or
more decoded bytes), compared to 52 characters (32 bytes) for
traditional base 32 addresses. See proposals 123 and 149 for additional
information.

Standard Base 32 (\"b32\") addresses contain the hash of the
destination. This will not work for encrypted ls2 (proposal 123).

You can\'t use a traditional base 32 address for an encrypted LS2
(proposal 123), as it contains only the hash of the destination. It does
not provide the non-blinded public key. Clients must know the
destination\'s public key, sig type, the blinded sig type, and an
optional secret or private key to fetch and decrypt the leaseset.
Therefore, a base 32 address alone is insufficient. The client needs
either the full destination (which contains the public key), or the
public key by itself. If the client has the full destination in an
address book, and the address book supports reverse lookup by hash, then
the public key may be retrieved.

So we need a new format that puts the public key instead of the hash
into a base32 address. This format must also contain the signature type
of the public key, and the signature type of the blinding scheme.

This section documents a new b32 format for these addresses. While we
have referred to this new format during discussions as a \"b33\"
address, the actual new format retains the usual \".b32.i2p\" suffix.

### Creation and encoding

Construct a hostname of {56+ chars}.b32.i2p (35+ chars in binary) as
follows. First, construct the binary data to be base 32 encoded:

 flag (1 byte)
 bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
 bit 1: 0 for no secret, 1 if secret is required
 bit 2: 0 for no per-client auth,
 1 if client private key is required
 bits 7-3: Unused, set to 0

 public key sigtype (1 or 2 bytes as indicated in flags)
 If 1 byte, the upper byte is assumed zero

 blinded key sigtype (1 or 2 bytes as indicated in flags)
 If 1 byte, the upper byte is assumed zero

 public key
 Number of bytes as implied by sigtype

Post-processing and checksum:

 Construct the binary data as above.
 Treat checksum as little-endian.
 Calculate checksum = CRC-32(data[3:end])
 data[0] ^= (byte) checksum
 data[1] ^= (byte) (checksum >> 8)
 data[2] ^= (byte) (checksum >> 16)

 hostname = Base32.encode(data) || ".b32.i2p"

Any unused bits at the end of the b32 must be 0. There are no unused
bits for a standard 56 character (35 byte) address.

### Decoding and Verification

 Strip the ".b32.i2p" from the hostname
 data = Base32.decode(hostname)
 Calculate checksum = CRC-32(data[3:end])
 Treat checksum as little-endian.
 flags = data[0] ^ (byte) checksum
 if 1 byte sigtypes:
 pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
 blinded sigtype = data[2] ^ (byte) (checksum >> 16)
 else (2 byte sigtypes) :
 pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
 blinded sigtype = data[3] || data[4]
 parse the remainder based on the flags to get the public key

### Secret and Private Key Bits

The secret and private key bits are used to indicate to clients,
proxies, or other client-side code that the secret and/or private key
will be required to decrypt the leaseset. Particular implementations may
prompt the user to supply the required data, or reject connection
attempts if the required data is missing.

### Notes

- XORing first 3 bytes with the hash provides a limited checksum
 capability, and ensures that all base32 chars at the beginning are
 randomized. Only a few flag and sigtype combinations are valid, so
 any typo is likely to create an invalid combination and will be
 rejected.
- In the usual case (1 byte sigtypes, no secret, no per-client auth),
 the hostname will be {56 chars}.b32.i2p, decoding to 35 bytes, same
 as Tor.
- Tor 2-byte checksum has a 1/64K false negative rate. With 3 bytes,
 minus a few ignored bytes, ours is approaching 1 in a million, since
 most flag/sigtype combinations are invalid.
- Adler-32 is a poor choice for small inputs, and for detecting small
 changes. We use CRC-32 instead. CRC-32 is fast and is widely
 available.
- While outside the scope of this specification, routers and/or
 clients must remember and cache (probably persistently) the mapping
 of public key to destination, and vice versa.
- Distinguish old from new flavors by length. Old b32 addresses are
 always {52 chars}.b32.i2p. New ones are {56+ chars}.b32.i2p
- Tor discussion thread [is
 here](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- Don\'t expect 2-byte sigtypes to ever happen, we\'re only up to 13.
 No need to implement now.
- New format can be used in jump links (and served by jump servers) if
 desired, just like b32.
- Any secret, private key, or public key longer than 32 bytes would
 exceed the DNS max label length of 63 chars. Browsers probably do
 not care.
- No backward compatibility issues. Longer b32 addresses will fail to
 be converted to 32-byte hashes in old software.


