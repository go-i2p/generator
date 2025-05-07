 I2PTunnel
services 

Below is quick copy of aum\'s I2P Site deployment guide.

**1. - Deploy a local server**

- For simplicity\'s sake, we will walk through the setup of a web
 server; however, this procedure is the same regardless what protocol
 of servers and/or clients you are setting up.
- I recommend the Tiny Httpd web server, thttpd, (windows version
 available on site) although you can use anything that you feel
 comfortable with.
- Another more robust option would be to use EasyPHP, which is also
 open source. It comes with PHP, PHPmyadmin, mySQL, and Apache web
 server. For newbies who have no experience setting up and hosting
 content over servers, see the hosting page for help.
- With the web server you\'ve chosen, configure it to listen on a port
 of your choice, and serve its documents from a directory of your
 choice. For this example, we\'ll assume port 10880.
- Make sure your firewall is set up so that you cannot receive
 incoming connections on this port (which would breach your
 anonymity).
- Test the webserver, by pointing your normal browser (the one with
 the \"direct connection\") at
 [http://localhost:10880](http://localhost:10880){target="_blank"}
 (changing the 10880 to the port number you have chosen).
- Once your webserver is working, and you can access it locally with
 your browser, continue to the next step.

I2P does not deal in IP addresses. To protect your anonymity, it deals
in unique addresses called destination keys.

A destination key works a lot like a regular IP address, except that it
can\'t be traced to your IP address or physical location. When users
place a request to speak with you, your gateways are the ones that
answer for you. So the requesting user can only know the IP address of
your gateways. However, gateways don\'t know your IP address, because
gateways are the last nodes on your tunnels, and you anonymously create
tunnels by way of garlic routing. (So gateways are like puppets that
can\'t see their masters, and everyone communicates through these
puppets)

To deploy a server on I2P, you create a destination keypair. You use the
private key to authenticate your server when connecting it to I2P, and
you make the public key (aka destination key) known publicly, so others
can connect to your server. (indirectly, through your gateways)

Each service you run on I2P requires a different keypair.

To generate your keypair, type the command:
`java -jar lib/i2ptunnel.jar -nogui -e "genkeys myWebPrivKey.dat myWebPubKey.dat"`
(all on one line)

In windows, to generate your keypair, type the command:
`java -jar lib/i2ptunnel.jar -nogui -e "genkeys myWebPrivKey.dat myWebPubKey.dat"`

The filenames `myWebPrivKey.dat` and `myWebPubKey.dat` are arbitrary -
choose whatever you want here, as long as you understand your own
choices.

We now need to export your public key into base64 format, which you will
share with others.

To convert your myWebPubKey.dat file into shareable base64, type the
command
`java -cp lib/i2p.jar net.i2p.data.Base64 encode myWebPubKey.dat > myWebPubKey.txt`
(all on one line).

This file you have just generated, `myWebPubKey.txt`, contains a long
base64 string (516 chars at last count), which we call a destination
key. All you need to know about this string for now is that it allows
remote clients to uniquely pinpoint and connect to your server, just the
same way as an IP address allows remote machines to pinpoint and connect
to your machine.

However, in contrast to an IP address, there is no way to trace your
machine\'s physical location - even though your server can be addressed
via I2P, your IP address cannot be traced or associated with this
destination key.

**3 - Open a \'Tunnel\' from I2P To Your Server**

- For clients elsewhere in I2P to be able to access your server, you
 must run a \'bridge\' or \'tunnel\', which takes connections from
 these clients and forwards them to your local server.
- To activate such a tunnel, type the command
 `java -jar lib/i2ptunnel.jar -nogui -e "server localhost 10880 myWebPrivKey.dat"`
 (all one line).
- If you used different filenames or port number earlier on, change
 these accordingly
- Windows users, remember to replace apostrophes with double quotes.
 Thus:
 `java -jar lib/i2ptunnel.jar -nogui -e "server localhost 10880 myWebPrivKey.dat"`
- Within a few seconds, the \'tunnel\' should now be active, and
 remote clients should be able to reach your server anonymously.
 Remember to let your router \"warm up\" before opening clients to
 it.

**4 - Update Your hosts.txt File**

- To test your own server locally, you\'ll need to create an entry in
 your hosts.txt file, so I2P can translate the simple URL you place
 in the browser\'s address bar into the full public key text needed
 to find your server.
- Edit your hosts.txt, and add the line myserver.i2p=blahblahblah,
 where myserver.i2p is an I2P \'domain\' you want to associate with
 your site, and the blahblahblah is the text of the base64 public key
 you created earlier in the file myWebPubKey.txt
- With this in place, you and others can reach your server with the
 simple domain name myserver.i2p in the browser\'s address bar.

**5 - Surf Your Site Within I2P**

- Using your secondary browser - the one you earlier configured to use
 localhost:4444 as a proxy - point this browser to the address
 [http://myserver.i2p](http://myserver.i2p){target="_blank"}
- You should see the main page of your webserver come up.

**6 - Create a Local Client Tunnel Connection**

- We now have to think beyond just web servers.
- As you grow into I2P and get more of a \'feel\' for it, you will
 want to use all manner of servers and clients.
- The beauty of I2P is that it allows standard Internet clients and
 servers for most protocols to be transparently \'tunneled\' through
 the anonymous network.
- You can run mailservers/clients, nameservers/clients,
 newsservers/clients - almost anything at all - perhaps even FTP in
 passive mode.
- Now, we\'ll create a client tunnel. This is like the server tunnel
 we created earlier, but works in reverse. It listens to a port on
 your local machine; your local client connects to this port; the
 connection gets forwarded through I2P to the service on the other
 end.
- To open your client tunnel for your server, type the command
 `java -jar lib/i2ptunnel.jar -nogui -e "config localhost 7654" -e "client 10888 textofbase64key"`
 (all one line).
- The port 10888 is arbitrary - it just needs to be something other
 than the physical port your server is listening on.
- textofbase64key is simply the contents of the public key text file
 myWebPubKey.txt, reproduced fully on one line (alternately, instead
 of textofbase64key, you can specify the name from your hosts.txt -
 e.g. myserver.i2p)
- Within a minute or two of launching this command, the client tunnel
 from your local machine into I2P will be open and ready for use.
- Point your regular web browser (ie, not the one you configured to
 use localhost:4444), and point it to
 [http://localhost:10888](http://localhost:10888){target="_blank"}
- Verify that the main page of your server eventually comes up in your
 browser.
- You use the same procedure for using any local client program to
 access a remote I2P server - just get the base64 public key (called
 destination key) of the remote server, choose a local port to
 connect to the remote server, open the tunnel, and just connect with
 your client to your heart\'s content.

**7 - Share your server details with others**

- Using an anonymous medium (eg the one of the I2P IRC servers or
 ugha\'s wiki), post your domain name (eg
 [www.mynick.i2p](http://www.mynick.i2p){target="_blank"} as well as
 your destination key. Others will then be able to reach your server
 remotely, without either of you jeopardizing your anonymity.
- Remember, you can go to What\'s on I2P and find the latest public
 keys linked to their URL. You should also post your own public key
 and URL their. However, you will want to do this anonymously, of
 course. Drupal.i2p.net is currently, as of this writing, only
 accessible from the net. So, to access the outside WWW anonymously
 from inside of I2P, you will need to start up your script called
 startSquid. Do it the same way you have been doing these other
 scripts. Reconfigure your browser to proxy on localhost:5555, as
 defined in the script, and when the script has generated it\'s keys,
 you can access the squid proxy. Put any WWW URL (such as Google or
 this i2p site) into your browser\'s address bar and you will be
 surfing the World Wide Web anonymously. Now you can safely post your
 public key, and no one can detect your IP address.

**8 - Write Some Scripts To Handle All This Menial Nonsense**

- It would drive most people crazy, going through all these steps
 every time one sets up an I2P server, and/or deploys a client.
- Aum\'s website
 [http://www.freenet.org.nz/i2p/](http://www.freenet.org.nz/i2p/){target="_blank"}
 has a script called setupServer.py which automates all this nonsense
 into one simple command line . But I respect that people\'s tastes
 in user interfaces differ, and trying to write something which
 satisfies everyone\'s needs usually results in something so complex
 that it turns into newbie-repellent.
- So please feel free to use and/or customize setupServer.py to taste,
 or write your own in Python or another language.
- Also, you may want to write a script which handles the startup of
 the I2P Router, the eepProxy, plus any and all tunnels you are
 using. I\'ve got such a script called startEverything.sh, which gets
 launched at system startup. (Be sure to search this site for
 template scripts to automate your I2P commands. If I create a page
 for one, I\'ll try to remember to link it here.
- Exercise for Windows users - port setupServer.py into a MS-DOS .BAT
 file.


