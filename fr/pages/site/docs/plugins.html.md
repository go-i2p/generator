 Greffons Juin 2012 0.9 

## Information générale

The I2P network includes a plugin architecture to support both easy
development and installation of new plugins.

Les greffons proposés prennent maintenant en charge le courriel
distribué, les blogues, les clients IRC, le stockage distribué de
fichiers, les wikis et plus.

### Adding Plugins To Your I2P Router

I2P Plugins can be installed by copying the plugin download URL onto the
appropriate section on the [Router Console Plugin Configuration
Page](http://127.0.0.1:7657/configplugins).

Start by copying the plugin URL from the page where it is published.

![](/_static/images/plugins/plugin-step-0.png)

Then visit the plugin configuration page, which you can find linked on
the console homepage.

![](/_static/images/plugins/plugin-step-1.png)

Paste in the URL and click the \"Install Plugin\" button.

![](/_static/images/plugins/plugin-step-2.png)

### Avantages aux utilisateurs i2p et développeurs d'app :

- Distribution facile d'applications
- Permet l'innovation et l'utilisation de bibliothèques
 supplémentaires sans s'inquiéter de l'augmentation de la taille de
 `i2pupdate.sud`
- Prendre en charge les grandes applications ou les applications
 spécialisées qui ne seraient jamais offertes avec l'installation I2P
- Applications vérifiées et signées cryptographiquement
- Mises à jour automatiques d'applications, comme pour le routeur
- Sépare l'installation initiale et les paquets de mise à jour, si
 vous le souhaitez, pour de plus petits téléchargements de mise à
 jour
- Installation d'applications en un clic. Il n'est plus demandé aux
 utilisateurs de modifier `wrapper.config` ou `clients.config`
- Isole les applications de l'installation `$I2P` de base
- Vérification de compatibilité automatique de la version I2P, version
 Java, version Jetty, et de la version de l'application précédemment
 installée
- Addition automatique de lien dans la console
- Démarrage automatique de l'application, y compris modification
 classpath, sans exiger un redémarrage
- Intégration automatique et démarrage d'applisWeb dans l'instance
 Jetty de la console
- Facilitate creation of \'app stores\' like the one at [](http://)
- Désinstallation en un clic
- Packs de langue et de thème pour la console
- Amène des informations détaillées d'application à la console de
 routeur
- Applications non Java également prises en charge

### Version I2P requise

0.7.12 ou plus récente.

### Updating a Plugin

Pour mettre un greffon à jour vers la dernière version, cliquez
simplement sur le bouton de mise à jour sur
[configclients.jsp](http://127.0.0.1:7657/configclients.jsp#plugin).
Vous y trouverez aussi un bouton pour vérifier si une version plus
récente du greffon est proposée, ainsi qu'un bouton pour vérifier les
mises à jour de tous les greffons. Les mises à jour des greffons seront
vérifiées automatiquement lors de la mise à jour vers une nouvelle
version d'I2P (n'incluant pas les versions développement).

![](/_static/images/plugins/plugin-update-0.png)

### Développement

See the latest [plugin specification]()

See also the sources for plugins developed by various people. Some
plugins, such as
[snowman](http:///plugins/snowman), were
developed specifically as examples.

### Premier pas

To create a plugin from an existing binary package you will need to get
makeplugin.sh from [the i2p.scripts repository in
git]().

### Problèmes connus

Notez que l'architecture de greffon du routeur ne fournit actuellement
**PAS** de quelconque isolement de sécurité supplémentaire ni sandboxing
de greffons.

- Les mises à jour d'un greffon avec des jars (pas des wars) inclus ne
 seront pas reconnues si le greffon était déjà en cours d'exécution,
 car il exige que l'astuce de tromperie de classe chargeur vide la
 classe cache; une redémarrage complet du routeur est exigé.
- Le bouton d'arrêt peut être affiché même s'il n'y a rien à arrêter.
- Les greffons exécutés dans une JVM séparée créent un répertorie
 `logs/` dans `$CWD`.
- Aucune clés initiales ne sont présentes, à part celles de jrandom et
 de zzz (utilisant la même clé que pour la mise à jour de routeur),
 ainsi la première clé vue pour un signataire sera automatiquement
 acceptée---il n'y a aucune autorité de signature de clé.
- Lors de la suppression d'un greffon, le répertoire n'est pas
 toujours supprimé, en particulier sur Windows.
- Installer un greffon exigeant Java 1.6 sur une machine Java 1.5
 aboutira à au message \"le greffon est corrompu\" si le fichier est
 compressé en pack200.
- Le thèmes et des greffons de traduction ne sont pas testés.
- Désactiver le démarrage automatique ne marche pas toujours.


