 How to Set up a
Reseed Server using a Docker Image 2023-01 

## Informație generală

These guidelines are based on idk\'s
[reseed-tools](https://i2pgit.org/idk/reseed-tools) server. They should
be very similar to the guidelines for DivaExchange\'s
[i2p-reseed](https://codeberg.org/diva.exchange/i2p-reseed) server.
These guidelines make use of Docker to manage the reseed server in lieu
of the initsystem. If you are not interested in using Docker they will
be of no use to you.

#### [To read the reseed policy, follow this link.](reseed-policy)

#### [Please see the general information for all reseed servers in addition to reading this section.](reseed)

## Installation from a Docker Image

To make it easier to deploy reseeds, it is possible to run the
reseed-tools as a Docker image. Because the software requires access to
a network database to host a reseed, you will need to mount the netDb as
a volume inside your docker container to provide access to it, and you
will need to run it as the same user and group inside the container as
I2P.

When you run a reseed under Docker in this fashion, it will
automatically generate a self-signed certificate for your reseed server
in a Docker volume named reseed-keys. *Back up this directory* , if it
is lost it is impossible to reproduce.

Additional flags can be passed to the application in the Docker
container by appending them to the command. Please note that Docker is
not currently compatible with .onion reseeds unless you pass the
--network=host tag.

## If I2P is running as your user, do this:

 docker run -itd \
 --name reseed \
 --publish 443:8443 \
 --restart always \
 --volume $HOME/.i2p/netDb:$HOME/.i2p/netDb:z \
 --volume reseed-keys:/var/lib/i2p/i2p-config/reseed \
 eyedeekay/reseed \
 --signer $YOUR_EMAIL_HERE

## If I2P is running as another user, do this:

 docker run -itd \
 --name reseed \
 --user $(I2P_UID) \
 --group-add $(I2P_GID) \
 --publish 443:8443 \
 --restart always \
 --volume /PATH/TO/USER/I2P/HERE/netDb:/var/lib/i2p/i2p-config/netDb:z \
 --volume reseed-keys:/var/lib/i2p/i2p-config/reseed \
 eyedeekay/reseed \
 --signer $YOUR_EMAIL_HERE

## **Debian/Ubuntu and Docker**

In many cases I2P will be running as the Debian system user ` i2psvc ` .
This is the case for all installs where Debian's Advanced Packaging
Tool(apt) was used to peform the task. If you used \"apt-get install\"
this command will work for you. In that case, just copy-and-paste:

 docker run -itd \
 --name reseed \
 --user $(id -u i2psvc) \
 --group-add $(id -g i2psvc) \
 --publish 443:8443 \
 --restart always \
 --volume /var/lib/i2p/i2p-config/netDb:/var/lib/i2p/i2p-config/netDb:z \
 --volume reseed-keys:/var/lib/i2p/i2p-config/reseed \
 eyedeekay/reseed \
 --signer $YOUR_EMAIL_HERE

The certificates themselves are available in ` reseed-keys ` . When you
are ready, you should copy the ` *.crt ` files from that volume and
share them with the I2P community on [` zzz.i2p `](http://zzz.i2p) .
These will allow I2P users to authenticate your reseed services and
secure the I2P network.

Contact us via email zzz at mail.i2p (alternatively, post in the reseed
section on the zzz.i2p forum) Provide us with details about your new
reseed server:

- Reseed website URL
- Public SSL certificate
- Public reseed su3 certificate
- Your contact email
- A statement that you agree to the privacy policy above


