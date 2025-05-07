 Plugins Iunie 2012 0.9 

## Informație generală

The I2P network includes a plugin architecture to support both easy
development and installation of new plugins.

Acum sunt disponibile plugin-uri care acceptă e-mailuri distribuite,
bloguri, IRC clienți, stocare de fișiere distribuite, wikis-uri și multe
altele.

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

### Beneficii pentru utilizatorii i2p și dezvoltatorii de aplicații:

- Distribuirea ușoară a aplicațiilor
- Permite inovația și utilizarea bibliotecilor suplimentare fără să vă
 faceți griji creșterea dimensiunii `i2pupdate.sud`
- Sprijiniți aplicații cu scopuri mari sau cu scop special, care nu ar
 fi niciodată incluse cu instalarea I2P
- Aplicații semnate și verificate criptografic
- Actualizări automate ale aplicațiilor, la fel ca pentru router
- Separați pachetele de instalare și actualizare inițiale, dacă
 doriți, pentru descărcări de actualizări mai mici
- One-click installation of applications. No more asking users to
 modify `wrapper.config` or `clients.config`
- Izolați aplicațiile de baza de instalare `$I2P` de bază
- Verificarea automată a compatibilității pentru versiunea I2P,
 versiunea Java, Jetty versiunea și versiunea anterioară a aplicației
 instalate
- Adăugarea automată a legăturii în consolă
- Pornirea automată a aplicației, inclusiv modificarea traseului de
 clasă, fără a fi necesară repornirea
- Integrare automată și pornire de webapps în instanța Jetty a
 consolei
- Facilitate creation of \'app stores\' like the one at [](http://)
- Dezinstalare cu un singur clic
- Pachetele de limbă și temă pentru consolă
- Aduceți informații detaliate despre aplicația în consola routerului
- Sunt acceptate și aplicații non-java

### Versiunea necesară I2P

0.7.12 sau mai nou.

### Updating a Plugin

To update a plugin to the latest version, just click the update button
on [configclients.jsp](http://127.0.0.1:7657/configclients.jsp#plugin).
There is also a button to check if the plugin has a more recent version,
as well as a button to check for updates for all plugins. Plugins will
be checked for updates automatically when updating to a new I2P release
(not including dev builds).

![](/_static/images/plugins/plugin-update-0.png)

### Dezvoltare

See the latest [plugin specification]()

See also the sources for plugins developed by various people. Some
plugins, such as
[snowman](http:///plugins/snowman), were
developed specifically as examples.

### Noțiuni de bază

To create a plugin from an existing binary package you will need to get
makeplugin.sh from [the i2p.scripts repository in
git]().

### Probleme cunoscute

Rețineți că arhitectura pluginului routerului **NU** este actualmente
furnizat orice izolare suplimentară de securitate sau sandboxing de
plugin-uri.

- Actualizările unui plugin cu jars incluse (nu wars) nu vor fi
 recunoscute dacă pluginul a fost deja executat, deoarece necesită
 trucuri pentru încărcarea clasei pentru a spăla memoria cache; este
 necesar un restart complet al routerului.
- Butonul de oprire poate fi afișat chiar dacă nu există nimic de
 oprit.
- Plugin-urile care rulează într-un JVM separat creează un `logs/`
 director în `$CWD`
- Nu sunt prezente chei inițiale, cu excepția celor din jrandom și zzz
 (folosind aceleași chei ca pentru actualizarea routerului), deci
 prima cheie văzută pentru un semnatar este acceptat automat - nu
 există nicio autoritate cheie de semnare.
- La ștergerea unui plugin, directorul nu este întotdeauna șters, mai
 ales pe Windows.
- nstalarea unui plugin care necesită Java 1.6 pe o mașină Java 1.5 va
 avea ca rezultat un Mesajul \"plugin este corupt\" dacă se folosește
 compresia pack200 a fișierului plugin.
- Plugin-urile de temă și de traducere nu sunt testate.
- Dezactivarea pornirii automate nu funcționează întotdeauna.


