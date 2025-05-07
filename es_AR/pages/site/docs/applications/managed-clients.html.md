 Clientes
gestionados Febrero de 2014 0.9.11 

## Información general

Clients may be started directly by the router when they are listed in
the [clients.config]() file. These clients
may be \"managed\" or \"unmanaged\". This is handled by the
ClientAppManager. Additionally, managed or unmanaged clients may
register with the ClientAppManager so that other clients may retrieve a
reference to them. There is also a simple Port Mapper facility for
clients to register an internal port that other clients may look up.

## Clientes gestionados

Desde la versión 0.9.4, el router I2P soporta clientes gestionados. Los
clientes gestionados son invocados e iniciados por el ClientAppManager.
El ClientAppManager mantiene una referencia hacia el cliente y recibe
actualizaciones sobre su estado. Se prefieren los clientes gestionados,
ya que es mucho más fácil implementar el rastreo del estado e iniciar y
detener un cliente. También es mucho más fácil evitar referencias
estáticas en el código del cliente que podrían llevar a un uso excesivo
de memoria después de que un cliente sea detenido. Los clientes
gestionados pueden ser iniciados y detenidos por el usuario en la
consola del router I2P, y son detenidos en el apagado del router.

Los clientes gestionados implementan o bien la interfaz
net.i2p.app.ClientApp o bien net.i2p.router.app.RouterApp . Los clientes
que implementan la interfaz ClientApp deben proporcionar el siguiente
constructor:

 public MyClientApp(I2PAppContext context, ClientAppManager listener, String[] args)

Los clientes que implementan la interfaz RouterApp deben proporcionar el
siguiente constructor:

 public MyClientApp(RouterContext context, ClientAppManager listener, String[] args)

Los argumentos proporcionados se especifican en el fichero
clients.config .

## Clientes no gestionados

Si la clase principal especificada en el fichero clients.config no
implementa una interfaz gestionada, será iniciada con main() con los
argumentos especificados, y detenida con main() con los argumentos
especificados. El router I2P no mantiene una referencia, ya que todas
las interacciones se realizan mediante el método main(). La consola no
puede proporcionar información de estado precisa al usuario.

## Clientes registrados

Los clientes, tanto si son gestionados como si no, pueden registrarse
con el ClientAppManger de forma que los demás clientes pueden obtener
una referencia hacia ellos. El registro es por nombre. Son clientes
registrados conocidos:

 console, i2ptunnel, Jetty, outproxy, update

## Mapeador de puertos

El router I2P también proporciona un mecanismo simple para que los
clientes encuentren un servicio de socket interno (conexión entre
procesos), como el proxy HTTP. Esto es proporcionado por el Mapeador de
Puertos. El registro es por nombre. Los clientes que se registran
generalmente proporcionan un socket emulado interno sobre ese puerto.


