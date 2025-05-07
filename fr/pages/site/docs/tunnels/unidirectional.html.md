 Tunnels
unidirectionels Novembre 2016 0.9.27 

## Vue d'ensemble

This page describes the origins and design of I2P\'s unidirectional
tunnels. For further information see:

- [Tunnel overview
 page]()
- [Tunnel
 specification]()
- [Tunnel creation
 specification]()
- [Tunnel design
 discussion]()
- [Sélection de
 pair]()
- [Meeting 125
 (\~13:12-13:30)]()

## Synthèse

While we aren\'t aware of any published research on the advantages of
unidirecdtional tunnels, they appear to make it harder to detect a
request/response pattern, which is quite possible to detect over a
bidirectional tunnel. Several apps and protocols, notably HTTP, do
transfer data in such manner. Having the traffic follow the same route
to its destination and back could make it easier for an attacker who has
only timing and traffic volume data to infer the path a tunnel is
taking. Having the response come back along a different path arguably
makes it harder.

When dealing with an internal adversary or most external adversaries,
I2P\'s undirectional tunnels expose half as much traffic data than would
be exposed with bidirectional circuits by simply looking at the flows
themselves - an HTTP request and response would follow the same path in
Tor, while in I2P the packets making up the request would go out through
one or more outbound tunnels and the packets making up the response
would come back through one or more different inbound tunnels.

The strategy of using two separate tunnels for inbound and outbound
communication is not the only technique available, and it does have
anonymity implications. On the positive side, by using separate tunnels
it lessens the traffic data exposed for analysis to participants in a
tunnel - for instance, peers in an outbound tunnel from a web browser
would only see the traffic of an HTTP GET, while the peers in an inbound
tunnel would see the payload delivered along the tunnel. With
bidirectional tunnels, all participants would have access to the fact
that e.g. 1KB was sent in one direction, then 100KB in the other. On the
negative side, using unidirectional tunnels means that there are two
sets of peers which need to be profiled and accounted for, and
additional care must be taken to address the increased speed of
predecessor attacks. The tunnel pooling and building process (peer
selection and ordering strategies) should minimize the worries of the
predecessor attack.

## Anonymat

A recent [paper by Hermann and Grothoff]() declared
that I2P\'s unidirectional tunnels \"seems to be a bad design
decision\".

The paper\'s main point is that deanonymizations on unidirectional
tunnels take a longer time, which is an advantage, but that an attacker
can be more certain in the unidirectional case. Therefore, the paper
claims it isn\'t an advantage at all, but a disadvantage, at least with
long-living I2P Sites.

Cette conclusion n'est pas entièrement soutenue par le papier. Les
tunnels unidirectionnels atténuent clairement d'autres attaques et il
n'est pas clair dans le papier sur la façon de négocier le risque
d'attaques dans une architecture de tunnels bidirectionnels.

This conclusion is based on an arbitrary certainty vs. time weighting
(tradeoff) that may not be applicable in all cases. For example,
somebody could make a list of possible IPs then issue subpoenas to each.
Or the attacker could DDoS each in turn and via a simple intersection
attack see if the I2P Site goes down or is slowed down. So close may be
good enough, or time may be more important.

La conclusion est basée sur une pondération spécifique de l'importance
de la certitude contre le temps, et que la pondération pourrait être
fausse, et c'est certainement discutable, particulièrement dans un monde
réel avec citations à comparaître, mandats de perquisition et autres
méthodes disponibles pour la confirmation finale.

Une analyse complète des compromis entre tunnels unidirectionnels et
tunnels bidirectionnels dépasse de toute évidence la portée du présent
article et ne peut pas être trouvée ailleurs. Par exemple, comment cette
attaque se compare-t-elle aux nombreuses attaques temporelles possibles
qui ont été publiées au sujet des réseaux avec routage en oignon ?
Manifestement, les auteurs n'ont pas effectué cette analyse, s'il est
même possible de la faire avec efficacité.

Tor utilise des tunnels bidirectionnels et a fait l'objet de nombreuses
évaluations universitaires. I2P utilise des tunnels unidirectionnels et
n'a été que peu évalué. Le manque d'articles de recherche qui défendent
les tunnels unidirectionnels signifie-t-il qu'ils sont un mauvais choix
de conception, ou plutôt qu'ils justifient plus d'étude? Il est
difficile de se défendre contre des attaques temporelles et contre des
attaques distribuées, autant dans I2P que dans Tor. L'objectif de
conception (voir les références ci-dessus) était que les tunnels
unidirectionnels résistent mieux aux attaques temporelles. Cependant,
l'article présente un type d'attaque temporelle quelque peu différente.
Cette attaque, aussi novatrice qu'elle soit, est-elle suffisante pour
établir que l'architecture de tunnels d'I2P (et par conséquent tout I2P)
est une « mauvaise conception » et donc nettement inférieure à Tor, ou
est-ce plutôt une autre conception qui doit de toute évidence faire
l'objet de recherches et d'analyses plus poussées ? Plusieurs autres
raisons permettraient de considérer I2P comme actuellement inférieur à
Tor et à d'autres projets (petite taille du réseau, manque de
financement, manque d'évaluation), mais les tunnels unidirectionnels
sont-ils vraiment une raison ?

En résumé, \"mauvaise décision de conception\" est apparemment (puisque
le papier n'étiquette pas comme \"mauvais\" les tunnels bidirectionnels)
un raccourci pour \"les tunnels unidirectionnels sont sans équivoque
inférieurs aux tunnels bidirectionnel\", pourtant cette conclusion n'est
pas soutenue par le papier.


