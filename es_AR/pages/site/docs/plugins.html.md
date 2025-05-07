 Complementos Junio de 2012 0.9 

## Información general

The I2P network includes a plugin architecture to support both easy
development and installation of new plugins.

Ahora hay plugins disponibles que soportan email distribuido, blogs,
clientes IRC, almacenamiento de ficheros distribuido, wikis y más.

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

### Los beneficios para los usuarios de I2P y los desarrolladores de aplicaciones son:

- Fácil distribución de aplicaciones
- Permite la innovación y el uso de librerías adicionales sin
 preocuparse por el incremento de tamaño de `i2pupdate.sud`
- Soporta aplicaciones grandes o de proposito-especial que nunca
 serían empaquetadas con la instalación de I2P
- Aplicaciones criptográficamente firmadas y verificadas
- Actualizaciones automáticas de aplicaciones, igual que para el
 router
- Paquetes separados para la instalación inicial y las
 actualizaciones, si se desea, para tener descargas de
 actualizaciones más pequeñas
- Instalación de aplicaciones en un-sólo-clic. Sin preguntar más al
 usuario para modificar `wrapper.config` o `clients.config`
- Aplicaciones aisladas desde la instalación base de `$I2P`
- Comprobación automática de compatibilidad para la versión de I2P, la
 versión de Java, la versión de Jetty, y versiones de la aplicación
 previamente instaladas
- Añadido automático de enlaces en la consola
- Inicio automático de la aplicación, incluyendo modificación de la
 ruta de clases (\`classpath\`), sin requerir un reinicio
- Integración automática e inicio de aplicaciones web en la instancia
 de consola Jetty
- Facilitate creation of \'app stores\' like the one at [](http://)
- Desinstalación en un-sólo-clic
- Paquetes de idioma y de temas para la consola
- Trae información detallada de la aplicación a la consola del router
- Las aplicaciones no-Java también están soportadas

### Versión de I2P requerida

0.7.12 o superior.

### Updating a Plugin

Para actualizar un plugin a la última versión, tan solo haga clic en el
botón de actualización sobre
[configclients.jsp](http://127.0.0.1:7657/configclients.jsp#plugin).
También hay un botón para comprobar si el plugin tiene una versión más
reciente, así como un botón para buscar actualizaciones para todos los
plugins. Se comprobará si hay actualizaciones para los plugins
automáticamente cuando se actualice a una nueva versión de I2P (sin
incluir las versiones de desarrollo).

![](/_static/images/plugins/plugin-update-0.png)

### Desarrollo

See the latest [plugin specification]()

See also the sources for plugins developed by various people. Some
plugins, such as
[snowman](http:///plugins/snowman), were
developed specifically as examples.

### Iniciar con Martus

To create a plugin from an existing binary package you will need to get
makeplugin.sh from [the i2p.scripts repository in
git]().

### Dificultades conocidas.

Observe que la arquitectura del plugin del router actualmente **NO**
proporciona seguridad adicional, aislamiento o sandboxing de plugins.

- Las actualizaciones de un plugin con jars (no wars) incluidos, no
 serán reconocidas si el plugin ya se está ejecutando, ya que
 requiere usar trucos en el cargador de clases (\'class\') para
 limpiar la caché de clases; se requiere un reinicio completo del
 router.
- El botón de parada podría mostarse incluso si no hay nada que parar.
- Los plugins ejecutandose en una JVM crean un directorio `logs/` en
 `$CWD`.
- No hay claves inciales presentes, excepto para aquellos de
 \`jrandom\` y \`zzz\` (que usan las mismas claves que para la
 actualización del router), por lo que la primera clave vista para un
 firmante es automáticamente aceptada---no hay autoridad de clave de
 firmado.
- Cuando se borra un plugin el directorio no siempre se borra,
 especialmente sobre Windows.
- Instalar un plugin que requiere Java 1.6 sobre una máquina Java 1.5
 resultará en un mensaje \"el plugin está corrupto\" si se usó la
 compresión pack200 en el fichero del plugin.
- Los plugins de temas y traducciones no están probados.
- Deshabilitar autoinicio no siempre funciona.


