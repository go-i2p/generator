 Nommer et carnet
d\'adresse 2025-01 0.9.65 

## Vue d'ensemble {#overview}

I2P est livré avec une bibliothèque générique de nommage et une mise en
œuvre de base conçue pour marcher à partir d'un nom local vers la
cartographie de destination, ainsi qu'avec une application add-on
appelée le [carnet d'adresses](#addressbook). I2P permet aussi les [noms
d'hôtes en Base32](#base32) de façon similaire aux adresses en .onion de
Tor.

Le carnet d'adresses est conduit par Web de confiance sécurisé,
distribué, et système de nommage lisible par humain, sacrifiant
seulement l'appel pour tous les noms lisibles par humain qu'il soient
globalement uniques en mandatant seulement l'unicité locale. Tandis que
tous les messages dans I2P sont cryptographiquement adressés par leur
destination, des gens différents peuvent avoir des entrées de carnet
d'adresse locales pour \"Alice\" qui réfère aux destinations
différentes. Les gens peuvent toujours découvrir de nouveaux noms en
important les carnets d'adresses publiés de pairs indiqués dans leur Web
de confiance, ceci en ajoutant les entrées fournies par personne
interposée, ou (si quelques personnes organisent une série de carnets
d'adresses publiés utilisant un système d'enregistrement de type premier
arrivé premier servi) les gens peuvent vouloir traiter ces carnets
d'adresses comme des serveurs de nom, émulant un DNS traditionnel.

NOTE: For the reasoning behind the I2P naming system, common arguments
against it and possible alternatives see the [naming
discussion]() page.

## Composants système de nommage {#components}

Il n'y a aucune autorité centrale de nommage dans I2P. Tous les noms
d'hôtes sont locaux.

Le système de nommage est assez simple et la plupart de cela est mis en
œuvre dans des applications externes au routeur, mais empaquetées avec
la distribution I2P. Les composants sont :

1. Le [service de noms](#lookup) local qui assure les consultations et
 gère aussi les [noms d'hôtes Base32](#base32).
2. Le [mandataire HTTP](#httpproxy) qui demande au routeur des
 consultations et dirige l'utilisateur vers des services de saut
 distants afin de pallier les échecs de consultation.
3. [formulaires HTTP basés-hôte](#add-services) qui permettent aux
 utilisateurs d'ajouter des hôtes à leur hosts.txt local
4. [Services de saut](#jump-services) HTTP qui fournissent leurs
 propres consultations et redirection.
5. Le [carnet d'adresses](#addressbook) l'application qui mêle des
 listes d'hôtes externes, recouvrées via HTTP, avec la liste locale.
6. L'application [SusiDNS](#susidns) qui est qui est un simple frontal
 Web simple pour la configuration du carnet d'adresses et le
 visionnage des listes locales d'hôtes.

## Naming Services {#lookup}

All destinations in I2P are 516-byte (or longer) keys. (To be more
precise, it is a 256-byte public key plus a 128-byte signing key plus a
3-or-more byte certificate, which in Base64 representation is 516 or
more bytes. Non-null
[Certificates](#certificates) are in
use now for signature type indication. Therefore, certificates in
recently-generated destinations are more than 3 bytes.

Si une application (i2ptunnel ou le mandataire HTTP) souhaite accéder à
une destination par son nom, le routeur fait une très simple
consultation locale afin de résoudre ce nom.

### Hosts.txt Naming Service

Le service de noms hosts.txt effectue une simple recherche linéaire de
fichiers texte. Ce système de noms était celui par défaut jusqu'à la
version 0.8.8. Il fut alors remplacé par le système de noms Blockfile.
Le format hosts.txt était devenu trop lent après que le fichier a grossi
à plusieurs milliers d'entrées.

It does a linear search through three local files, in order, to look up
host names and convert them to a 516-byte destination key. Each file is
in a simple [configuration file
format](), with hostname=base64, one per
line. The files are:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile Naming Service

Le service de noms Blockfile enregistre plusieurs « carnets d'adresses »
dans un seul fichier de base de données nommé hostsdb.blockfile. Ce
système de noms est le système par défaut depuis la version 0.8.8.

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

Lors de la création, le service de noms importe des entrées des trois
fichiers utilisés par le service de noms hosts.txt. Le blockfile imite
la mise en œuvre précédente en maintenant trois cartes qui sont
consultées en ordre, nommées privatehosts.txt, userhosts.txt et
hosts.txt. Il maintient aussi une carte de consultation inversée pour
mettre en œuvre des consultations inversés rapides.

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

Si le routeur n'arrive pas à résoudre le nom d'hôte, le mandataire HTTP
retourne à l'utilisateur une page d'erreur avec des liens vers plusieurs
services de « saut ». Voir ci-dessous pour plus de précisions.

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

## Carnet d'adresses {#addressbook}

### Abonnements entrants et fusion

L'application carnet d'adresses récupère périodiquement les fichiers
hosts.txt d'autres utilisateurs et les mêle avec le hosts.txt local,
après plusieurs contrôles. Les conflits de nommage sont résolus sur une
base premier-arrivé premier-servi.

S'abonner au fichier hosts.txt d'un autre utilisateur implique de lui
accorder une certaine confiance. Vous ne voulez pas, par exemple, qu'ils
« détournent » un nouveau site en saisissant rapidement leur propre clé
pour un nouveau site avant de vous passer la nouvelle entrée d'hôte, de
clé.

Pour cette raison, le seul abonnement configuré par défaut est
`http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`
qui contient un exemplaire du hosts.txt inclus dans la version d'I2P.
Les utilisateurs doivent configurer les abonnements supplémentaires dans
leur application locale de carnet d'adresses (avec subscriptions.txt ou
[SusiDNS](#susidns)).

Some other public address book subscription links:

- [http:///cgi-bin/i2hostetag](http:///cgi-bin/i2hostetag)
- [http:///cgi-bin/newhosts.txt](http:///cgi-bin/newhosts.txt)

Les opérateurs de ces services peuvent avoir différentes politiques de
listage des hôtes. La présence dans cette liste n'implique pas une
approbation.

### Règles de nommage

Bien que nous espérions qu'il n'y a pas de restrictions techniques dans
I2P concernant les noms d'hôtes, le carnet d'adresses impose plusieurs
restrictions aux noms d'hôtes importés d'abonnements. Il le fait par
justesse typographique, compatibilité avec les navigateurs et sécurité.
Les règles sont essentiellement identiques à celles présentées par
RFC2396 section 3.2.2. Tout nom d'hôte enfreignant ces règles ne peut
pas être propagé à d'autres routeurs.

Règles de nommage:

- Les noms sont convertis en minuscule lors de l'importation.
- Les noms sont vérifiés contre le conflit avec des noms existants
 dans userhosts.txt existant et hosts.txt (mais pas privatehosts.txt)
 après conversion en minuscule.
- Doivent contenir seulement \[a-z\] \[0-9\] \'.\' et \'-\' après
 conversion en minuscules.
- Ne doivent pas commencer avec \'.\' ni \'-\'.
- Doivent terminer par \'i2p\'.
- 67 caractères au maximum, le \'.i2p\' compris.
- Ne doivent pas contenir \'..\'.
- Ne doivent pas contenir \'..\' ou \'-.\' (depuis la 0.6.1.33).
- Ne doivent pas contenir \'\--\' excepté dans \'xn\--\' pour IDN.
- Les noms d'hôte Base32 (\*.b32.i2p) sont réservés pour un usage
 Base32 et ne peuvent donc pas être importés.
- Certain hostnames reserved for project use are not allowed
 (proxy.i2p, router.i2p, console.i2p, mail.i2p, \*.proxy.i2p,
 \*.router.i2p, \*.console.i2p, \*.mail.i2p, and others)
- Hostnames starting with \'www.\' are discouraged and are rejected by
 some registration services. Some addressbook implementations
 automatically strip \'www.\' prefixes from lookups. So registring
 \'www.example.i2p\' is unnecessary, and registering a different
 destination for \'www.example.i2p\' and \'example.i2p\' will make
 \'www.example.i2p\' unreachable for some users.
- La validité Base64 des clés est vérifiée.
- Les clés sont vérifiées contre le conflit avec des clés existantes
 dans hosts.txt (mais pas privatehosts.txt).
- Longueur minimum de clé : 516 octets.
- Longueur maximum de clé : 616 octets (pour tenir compte des certs
 jusqu'à 100 octets).

Tout nom reçu par abonnement qui subit avec succès toutes les
vérifications est ajouté par le système local de noms.

Notez que les symboles \'.\' dans un nom hôte n'ont aucune signification
et ne dénotent pas de hiérarchie de nommage ni de confiance. Si le nom
\'host.i2p\' existe déjà, il n'y a rien pour empêcher quelqu'un
d'ajouter un nom \'a.host.i2p\' à son hosts.txt, et ce nom pourra être
importé par les carnets d'adresses d'autres personnes. Des méthodes pour
refuser des sous-domaines aux \'propriétaires\' de non-domaines (des
certificats ?) et la désirabilité et la faisabilité de ces méthodes sont
sujets de discussions futures.

Les noms de domaine internationaux (IDN) marchent aussi dans i2p
(utilisant le punycode de forme \'xn\--\'). Pour voir les noms de
domaine IDN .i2p rendus correctement dans la barre d'adresse de Firefox,
ajoutez \'network.IDN.whitelist.i2p (boolean) = true\' dans
about:config.

Comme l'application carnet d'adresses n'utilise pas du tout
privatehosts.txt, en pratique ce fichier est le seul endroit où il est
approprié de placer des alias privés ou \"pet names\" pour des sites
déjà présents dans hosts.txt.

### Format évolué de flux d'abonnement

As of release 0.9.26, subscription sites and clients may support an
advanced hosts.txt feed protocol that includes metadata including
signatures. This format is backwards-compatible with the standard
hosts.txt hostname=base64destination format. See [the
specification](/spec/subscription) for details.

### Abonnements sortants

Address Book will publish the merged hosts.txt to a location
(traditionally hosts.txt in the local I2P Site\'s home directory) to be
accessed by others for their subscriptions. This step is optional and is
disabled by default.

### Hosting and HTTP Transport Issues

L'application de carnet d'adresses, de concert avec eepget, enregistre
l'Etag ou les informations de dernière modification retournées par le
serveur Web de l'abonnement. Cela réduit grandement la bande passante
exigée, car le serveur Web retournera « 304 non modifié » lors de la
prochaine récupération si rien n'a été modifié.

Cependant hosts.txt est téléchargé en entier si il a changé. Voir
ci-dessous pour la discussion sur cette question.

Les hôtes servant un hosts.txt fixe ou une application CGI équivalente
sont fortement encouragés à livrer un en-tête de longueur de contenu et
soit une balise Etag, soit un en-tête de dernière modification. Cela
garantit aussi que le serveur livre un « 304 not modified » (304 non
modifié) si nécessaire. La bande passante du réseau sera
considérablement réduite et les risques de corruption seront aussi
réduits.

## Services d'ajout d'hôtes {#add-services}

Un service d'ajout d'hôte est une simple application CGI qui prend un
nom d'hôte et une clé en Base64 comme paramètres et ajoute cela à son
hosts.txt local. Si d'autres routeurs s'abonnent à ce hosts.txt, le
nouveau nom d'hôte ou clé seront propagés à travers le réseau.

Il est recommandé que les services de nom d'hôte imposent, au minimum,
les restrictions imposées par la l'application carnet d'adresses
inscrite ci--dessus. Les services d'ajout d'hôtes peuvent imposer des
restrictions supplémentaires de nom d'hôtes et de clés, par exemple :

- Une limite concernant le nombre de \'sous-domaines\'.
- Autorisation de \'sous-domaines\' à travers diverses méthodes.
- Certificats signés ou hashcash.
- Révision des noms d'hôte ou du contenu.
- Catégorisation par contenu des noms d'hôtes.
- Réservation ou refus de certains noms hôtes.
- Restrictions sur le nombre de noms enregistrés durant une période
 donnée.
- Retards entre enregistrement et publication.
- Exiger que l'hôte soit en ligne afin d'être vérifié.
- Expiration ou révocation.
- Refus d'usurpation IDN

## Services de saut {#jump-services}

Un service de saut est une simple application CGI qui prend un nom
d'hôte comme paramètre et retourne une redirection 301 vers l'URL
appropriée en ajoutant une chaîne `?i2paddresshelper=key`. Le mandataire
HTTP interprétera la chaîne ajoutée et utilisera cette clé comme
destination effective. De plus, le mandataire mettra cette clé en cache
afin que l'aide d'adresse ne soit plus nécessaire jusqu'au redémarrage.

Notez que, comme avec les abonnements, utiliser un service de saut
implique une certaine confiance, car un service de saut pourrait de
façon malveillante rediriger un utilisateur vers une destination
incorrecte.

Pour fournir le meilleur service, un service de saut devrait être abonné
à plusieurs fournisseurs hosts.txt afin que sa liste d'hôtes locaux soit
actuelle.

## SusiDNS

SusiDNS is simply a web interface front-end to configuring address book
subscriptions and accessing the four address book files. All the real
work is done by the \'address book\' application.

Currently, there is little enforcement of address book naming rules
within SusiDNS, so a user may enter hostnames locally that would be
rejected by the address book subscription rules.

## Noms Base32 {#base32}

I2P prend en charge les noms d'hôte en Base32 semblables aux adresses
.onion de Tor. Les adresses Base32 sont beaucoup plus courtes et plus
faciles à manipuler que les destinations complètes Base64 à 516
caractères ou que les aides d'adresse. Exemple :
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

Les adresses Base32 peuvent être utilisées dans la plupart des endroits
où noms d'hôte ou des destinations pleines sont utilisées, cependant il
y a quelques exceptions où elles peuvent échouer si le nom n'est pas
résolu immédiatement . I2PTunnel échouera, par exemple, si le nom ne
résout pas à une destination.

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


