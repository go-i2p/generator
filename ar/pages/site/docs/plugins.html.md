 الاضافات June 2012 0.9 

## المعلومات العامة

The I2P network includes a plugin architecture to support both easy
development and installation of new plugins.

There are now plugins available that support distributed email, blogs,
IRC clients, distributed file storage, wikis, and more.

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

### Benefits to i2p users and app developers:

- Easy distribution of applications
- Allows innovation and use of additional libraries without worrying
 about increasing the size of `i2pupdate.sud`
- Support large or special-purpose applications that would never be
 bundled with the I2P installation
- Cryptographically signed and verified applications
- Automatic updates of applications, just like for the router
- Separate initial install and update packages, if desired, for
 smaller update downloads
- One-click installation of applications. No more asking users to
 modify `wrapper.config` or `clients.config`
- Isolate applications from the base `$I2P` installation
- Automatic compatibility checking for I2P version, Java version,
 Jetty version, and previous installed application version
- Automatic link addition in console
- Automatic startup of application, including modifying classpath,
 without requiring a restart
- Automatic integration and startup of webapps into console Jetty
 instance
- Facilitate creation of \'app stores\' like the one at [](http://)
- One-click uninstall
- Language and theme packs for the console
- Bring detailed application information to the router console
- Non-java applications also supported

### Required I2P version

0.7.12 or newer.

### Updating a Plugin

To update a plugin to the latest version, just click the update button
on [configclients.jsp](http://127.0.0.1:7657/configclients.jsp#plugin).
There is also a button to check if the plugin has a more recent version,
as well as a button to check for updates for all plugins. Plugins will
be checked for updates automatically when updating to a new I2P release
(not including dev builds).

![](/_static/images/plugins/plugin-update-0.png)

### Development

See the latest [plugin specification]()

See also the sources for plugins developed by various people. Some
plugins, such as
[snowman](http:///plugins/snowman), were
developed specifically as examples.

### ابدء

To create a plugin from an existing binary package you will need to get
makeplugin.sh from [the i2p.scripts repository in
git]().

### مشاكل شائعة

Note that the router\'s plugin architecture does **NOT** currently
provide any additional security isolation or sandboxing of plugins.

- Updates of a plugin with included jars (not wars) won\'t be
 recognized if the plugin was already run, as it requires class
 loader trickery to flush the class cache; a full router restart is
 required.
- The stop button may be displayed even if there is nothing to stop.
- Plugins running in a separate JVM create a `logs/` directory in
 `$CWD`.
- No initial keys are present, except for those of jrandom and zzz
 (using the same keys as for router update), so the first key seen
 for a signer is automatically accepted---there is no signing key
 authority.
- When deleting a plugin, the directory is not always deleted,
 especially on Windows.
- Installing a plugin requiring Java 1.6 on a Java 1.5 machine will
 result in a \"plugin is corrupt\" message if pack200 compression of
 the plugin file is used.
- Theme and translation plugins are untested.
- Disabling autostart doesn\'t always work.


