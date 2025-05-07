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

## Vue d'ensemble

`CLÉS` = paire de clés publique+privée, elles sont en Base64

`CLÉ` = clé publique, aussi en Base64

`ERROR` comme elle l'implique retourne le message
`"ERROR "+DESCRIPTION+"\n"`, où la `DESCRIPTION` est ce qui s'est mal
passé.

`Correct` retourne `« Correct »`, et si des données doivent être
retournée, elle seront sur la même ligne.`Correct` signifie que la
commande est terminée.

`DATA` ces lignes contiennent les informations que vous avez demandé. Il
peut y avoir de multiples lignes `DATA` par requête.

**NOTE :** la commande d'aide est la SEULE commande qui a une exception
aux règles ... elle peut en réalité ne rien retourner ! Ceci est
intentionnel, sachant que l'aide est un HUMAIN et pas une commande
d'APPLICATION.

## Connexion et version

All BOB status output is by lines. Lines may be \\n or \\r\\n
terminated, depending on the system. On connection, BOB outputs two
lines:

 BOB version OK 

La version actuelle est : 00.00.10

Note that previous versions used upper-case hex digits and did not
conform to I2P versioning standards. It is recommended that subsequent
versions use digits 0-9 only. 00.00.10

Historique des versions

 Version Version du routeur I2P Changements
 --------------------- ------------------------ ---------------------------
 00.00.10 0.9.8 version actuelle
 00.00.00 - 00.00.0F   versions de développement

## Commandes

**VEUILLEZ NOTER :** Pour des précisions À JOUR sur les commandes,
VEUILLEZ utiliser la commande d'aide incorporée. Connectez-vous
simplement par Telnet à l'hôte local 2827 et tapez « help ». Vous
obtiendrez ainsi la documentation complète de chaque commande.

Les commandes ne seront jamais obsolètes ni changées, cependant de
nouvelles commandes sont ajoutées de temps en temps.

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

Une fois configuré, tous les sockets TCP peuvent et vont bloquer comme
nécessaire, et il n'y a aucun besoin de messages supplémentaires
vers/depuis le canal de commande. Ceci permet au routeur de marcher à
pas mesurés le flux sans exploser avec OOM comme SAM le fait si il
s'étrangle en tentant de pousser beaucoup de flux dans ou hors d'un
socket \-- cela ne peut pas se mettre à l'échelle quand vous avez
beaucoup de connexions !

Ce qui est aussi agréable au sujet de cette interface particulière est
que écrire quoi que ce soit à l'interface, est beaucoup beaucoup plus
facile que SAM. Il n'y a aucun autre traitement à faire après la
configuration. Sa configuration est si simple, que des outils très
simples, comme nc (netcat) peuvent être utilisés pour pointer vers une
certaine application. La valeur est là que l'on pourrait prévoir en haut
et en bas pour une application, et ne pas avoir à changer l'application
pour le faire, ou même avoir à arrêter cette application. Au lieu de
cela, vous pouvez littéralement \"déconnecter\" la destination, et quand
vous rebrancherez de nouveau, l'application TCP normale ne s'en souciera
pas et ne le remarquera pas. Elle sera simplement trompée \-- les
destinations ne sont pas accessibles, et que rien n'entre.

## Exemples

Pour l'exemple suivant, nous ferons une configuration très simple de
connexion loopback, avec deux destinations. La destination \"bouche\"
sera le service CHARGEN depuis le démon superserveur INET. La
destination \"oreille\" sera un port local auquel vous pouvez vous
connecter via telnet, et observer le joli dégueulis de test d'ASCII.

 DIALOGUE DE SESSION D'EXEMPLE - un simple
telnet 127.0.0.1 2827 fonctionne A = Application C = La réponse de
commande de BOB. FROM TO DIALOGUE C A BOB 00.00.10 C A OK A C setnick
mouth C A OK Nickname set to mouth A C newkeys C A OK
ZMPz1zinTdy3\~zGD\~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr\~0g2-l0vM7Y8nSqtFrSdMw\~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU\~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq\~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw\~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA


**PRENEZ NOTE DE LA CLÉ DE DESTINATION CI-DESSUS, LA VÔTRE SERA
DIFFÉRENTE !**

 FROM TO DIALOGUE A C outhost 127.0.0.1 C A
OK outhost set A C outport 19 C A OK outbound port set A C start C A OK
tunnel starting 

À ce point, il n'y a pas eu d'erreur, une destination avec le surnom
\"bouche\" est configurée. Quand vous contactez la destination fournie,
vous vous connectez en réalité au service `CHARGEN` sur le `19/TCP`.

Maintenant pour l'autre moitié, afin que nous puissions réellement
contacter cette destination.

 FROM TO DIALOGUE C A BOB 00.00.10 C A OK A
C setnick ear C A OK Nickname set to ear A C newkeys C A OK
8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg\~3eXtL-7S-qU-wdP-6VF\~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J\~flAvF4wrbF-LfVpMdg\~tjtns6fA\~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f\~dzoRCapAGDDTTnvjXuLrZ-vN-orT\~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A C inhost 127.0.0.1 C A OK inhost set A C inport 37337 C A OK inbound
port set A C start C A OK tunnel starting A C quit C A OK Bye! 

Maintenant tout que nous avons à faire est d'utiliser telnet vers
127.0.0.1, port 37337 envoyer la clé de destination ou l'adresse d'hôte
du carnet d'adresses que nous voulons contacter. Dans ce cas, nous
voulons contacter la \"bouche\", tout ce que nous faisons est de coller
dedans la clé et c'est parti.

**NOTE :** la commande \"quit\" dans le canal de commande ne déconnecte
PAS les tunnels comme SAM.

 \$ telnet 127.0.0.1 37337 Trying
127.0.0.1\... Connected to 127.0.0.1. Escape character is \'\^\]\'.
ZMPz1zinTdy3\~zGD\~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr\~0g2-l0vM7Y8nSqtFrSdMw\~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU\~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq\~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw\~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefg
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefgh
\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghi
#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghij
\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\]\^\_\`abcdefghijk
\... 

Après quelques km virtuels de ce vomissement, pressez `Control-]`

 \... cdefghijklmnopqrstuvwxyz{\|}\~
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{\|}\~
!\"#\$%&\'()\*+,-./0123456789:;\<=\>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{\|}\~ !\"#\$%&\'()\*+,-./0123456789:;\<= telnet\>
c Connection closed. 

Voici ce qui est arrivé...

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

Allons poser nos destinations maintenant que nous avons terminé avec
elles.

D'abord, allons voir quels sont les surnoms de destination que nous
avons.

 FROM TO DIALOGUE A C list C A DATA
NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true
QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST:
127.0.0.1 C A DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING:
false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT:
not_set OUTHOST: localhost C A OK Listing done 

Bien, les voilà. D'abord, enlevons \"bouche\".

 FROM TO DIALOGUE A C getnick mouth C A OK
Nickname set to mouth A C stop C A OK tunnel stopping A C clear C A OK
cleared 

Maintenant enlevons \"oreille\", notez que c'est ce qui arrive quand
vous tapez trop vite, et vous affiche ce à quoi ressemble un message
ERROR typique.

 FROM TO DIALOGUE A C getnick ear C A OK
Nickname set to ear A C stop C A OK tunnel stopping A C clear C A ERROR
tunnel is active A C clear C A OK cleared A C quit C A OK Bye! 

Je vais m'abstenir de montrer un exemple de la partie réceptrice d'un
pont, car elle est très simple. Elle a deux paramètres possibles et ils
sont activées/désactivés avec la commande « quiet ».

La valeur par défaut n'est PAS « quiet » et les premières données à
entrer dans votre connecteur logiciel d'écoute sont la destination qui
établit le contact. C'est une seule ligne composée de l'adresse Base64
suivie par un saut de ligne. Tout ce qui arrive ensuite est en fait là
pour être consommé par l'application.

En mode « quiet », on pourrait le comparer à une connexion ordinaire à
Internet. Aucune donnée supplémentaire n'entre du tout. C'est comme si
vous étiez simplement connecté à l'Internet ordinaire. Ce mode permet
une forme de transparence assez semblable à ce qui est proposé sur les
pages de paramètres de tunnel de la console du routeur, afin que vous
puissiez utiliser BOB pour diriger une destination vers un serveur Web,
par exemple, et vous n'auriez pas du tout à modifier le serveur Web.

L'avantage avec l'utilisation de BOB pour ceci est comme discuté
précédemment. Vous pourriez planifier des périodes de fonctionnement
aléatoires pour l'application, rediriger vers une machine différente,
etc. Une utilisation de ceci peut être quelque chose comme vouloir
essayer de faire une gaffe router-to-destination upness guessing. Vous
pourriez arrêter et démarrer la destination avec un processus totalement
différent pour faire aléatoire des mises en service et hors service. De
cette façon vous arrêteriez seulement la capacité de contacter un tel
service, et ne pas avoir à se déranger à l'arrêter et le redémarrer.
Vous pourriez rediriger et pointer vers une machine différente sur votre
réseau local tandis que vous faites des mises à jour, ou pointez vers un
ensemble de machines de secours selon ce qui fonctionne, etc, etc. Seule
votre imagination limite ce que vous pourriez faire avec BOB.


