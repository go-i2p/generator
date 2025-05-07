 How to Set up a
Reseed Server 2024-12


## Általános információ

Thank you for volunteering to run an I2P reseed server. \"Reseeding\" is
our term for bootstrapping new routers into the network. New routers
fetch a bundle of peer references, or \"router infos\", from one or more
of a hardcoded list of HTTPS URLs.

## Requirements

A reseed server must be reachable on the public internet. It must use
TLS, but it may use a self-signed TLS certificate if the reseed
administrator is in communication with the router development team. The
administrator of the reseed server should provide contact information in
order to respond to issues and be in touch with the I2P team.

## More Information

#### [To read the reseed policy, follow this link.](reseed-policy)

#### [Are you a Debian user? You can find Debian-Specific instructions here.](reseed-debian)

#### [Are you a Docker user? You can find Docker-Specific instructions here.](reseed-docker)

#### [To read the old instructions, follow this link.](reseed-old)

## Installation from Source Code

These guidelines are based on idk\'s
[reseed-tools](https://i2pgit.org/idk/reseed-tools) server. They should
be very similar to the guidelines for DivaExchange\'s
[i2p-reseed](https://codeberg.org/diva.exchange/i2p-reseed) server.

Reseed Tools is a pure Go application which can be built statically
without CGO. It makes use of Go Modules. A Makefile is provided with
some targets which are convenient helpers for generating binaries,
especially for production and release purposes.

**1.** Install the build dependencies

``` sh
sudo apt-get install go git make
```

**2.** Clone the source code

``` sh
git clone https://i2pgit.org/idk/reseed-tools ~/go/src/i2pgit.org/idk/reseed-tools
```

**3.** Generate the binaries using the ` make build ` command

``` sh
cd ~/go/src/i2pgit.org/idk/reseed-tools
make build
```

**4.** Install the binary and the config files

``` sh
sudo make install
```

## Running the Service

**1.** First, ensure that the I2P service is already running. The longer
the better, if you have to re-start the service, or if the service has
very few peers, allow it to run for 24 hours before advancing to step
**2.**

``` sh
sudo systemctl start i2p
# or, if you use sysvinit
sudo service i2p start
```

**2.** Once your I2P router is Well-Integrated, fill in your email in
`/etc/systemd/system/reseed.service.d/override.conf` and start the
reseed service. If you use sysvinit, fill in your email in
`/etc/default/reseed instead`.

``` sh
sudo systemctl start reseed
# or, if you use sysvinit
sudo service reseed start
```

Your reseed will auto-configure with a self-signed certificate on port
` :8443 ` . The certificates themselves are available in
` /var/lib/i2p/i2p-config/reseed ` . When you are ready, you should copy
the ` *.crt ` files from that directory and share them with the I2P
community on [` zzz.i2p `](http://zzz.i2p) . These will allow I2P users
to authenticate your reseed services and secure the I2P network.

Contact us via email zzz at mail.i2p. Provide us with details about your
new reseed server:

- Reseed website URL
- Public SSL certificate (only required if selfsigned)
- Public reseed su3 certificate
- Your contact email
- A statement that you agree to the privacy policy above


