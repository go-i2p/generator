 I2PTunnel
migration 

### I2PTunnel migration

After upgrading to the new architecture, you\'ll have to do a little
work to get your old I2PTunnel-driven servers running. Lets walk through
a simple example. For an I2P Site with the old clientApp configuration,
you had:

 -e "server localhost 80 myWebPriv.dat"

To provide that same functionality on the new web architecture:

- For the private key file: `path to "myWebPriv.dat"`\
 (it is recommended to copy that .dat to your new install dir)
- Check the \"Start automatically?\" checkbox `[X]`
- Click `"Save"`

It will come back saying:\

 * Not overwriting existing private keys in /usr/home/jrandom/routers/i2p/myWebPriv.dat
 * Ready!

That\'s it! Creating a new I2PTunnel server works the same way too,
except you don\'t need to \"copy the old file\", obviously. Behind the
scenes, it is all driven by the `i2ptunnel.config` file, which you may
modify externally (if you do, hit \"Reload config\" on the I2PTunnel web
page, which will tear down all of your existing tunnels and rebuild new
ones)

Note that you WILL need to wait until your router is integrated into the
network before you are able to use the /i2ptunnel/ web interface. It
will say \"Please be patient\" if you try to beforehand, which means
that it is still trying to build the necessary I2PTunnel sessions it has
been configured to create.


