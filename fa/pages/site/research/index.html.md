 Academic
Research May 2018 

## Introduction

### Research on the I2P Network

Research plays a key role in both maintaining the security and integrity
of the I2P network, as well as opening doors for more impactful future
development.

A list of known published papers about I2P is available
[here]().

This page outlines the most needed fields of research, notes to
potential researchers, general safety guidelines as well as an expanding
list of open research questions.

## Notes to Researchers:

### Defensive Research

While all research on the I2P network is beneficial and appreciated,
there are certain areas that are more in need than others. Most research
focuses on testing offensives against anonymous software, and this is
further reinforced by the incentives in academic institutions. The
project would appreciate research and testing that will support
fortifying the I2P network.

### Offensive and Analytic Tests

If you\'ve decided on a research topic that aims to hands-on investigate
the I2P network or solve a problem of large proportions we ask you to
**please** [communicate your ideas]() to the
development team, the sooner the better. I2P is under constant
development and a significant amount of roadmapping occurs, therefore
your problem may have already been identified and flagged for update or
patch. In the unlikely event you are conducting testing that overlaps
with / would be of interest to another research project already in
motion, we are also able to make you aware of this (with their
permission, of course), and possibly open the door for collaboration.
There is also a chance that the test itself may significantly harm the
network or regular users, and the team may have ideas or suggestions to
mitigate that risk and increase the safety of your testing.

## Research Ethics & Testing the Network

### General Guidelines

1. Consider the benefits and risks - is there any doubt that the
 research provides more value than danger?
2. If the research can be done on a test network then that is the
 preferred method
3. If you must operate on the live network, the safest route is only
 collecting data about yourself
4. If you need \'bigger data\', It is recommended to first see if you
 can use data sets from previous experiments or other third party
 resources is recommended
5. If you must collect data on the live network, ensure it is safe for
 publication and collect as little as possible
6. After testing and before publish, review that all data which is to
 be published publicly is ***not*** intended to be private by the
 originator

### Using a Test Network to Attack I2P

I2P can be run as a separate test network by controlling the locations
that a new router reseeds from so that it only finds other test routers.
The standard mode of operation is to have one JVM per router instance;
hence running multiple copies of I2P on a single machine is inadvisable,
both due to the potential resource drain and the certain port conflicts.
To better facilitate setting up small test networks, I2P has a
multirouter mode which enables multiple distinct routers to be run in
the same JVM. MultiRouter can be started from the i2p base directory by
running the below command.

 env CLASSPATH=$(find lib/ -name *.jar | paste -s -d ':') java net.i2p.router.MultiRouter 25

Additionally, I2P can be started in a virtual network mode. This mode
disables all transports, allowing the router to be tested in isolation
without network traffic. To enable this mode, add
`i2p.vmCommSystem=true` to the router.config before starting.

### Testing on the Live I2P Network

As stated above in the researcher notes, please [contact
us]() before you commence your testing. While
we do not discourage researchers from responsibly testing their ideas on
the live network, if an attack becomes apparent and we don\'t have any
line of communication then we will end up taking countermeasures which
could interfere with the test.

### Router Family Configuration

As of release 0.9.25, I2P supports a router family configuration. This
provides researchers who run multiple routers with the means to publicly
identify those routers. In turn, this helps the I2P project understand
that these routers are not running an attack on the network. It also
will prevent other routers from including multiple routers of the family
in a single tunnel, which could lead to deanonymization. Routers that
appear to be colluding but do not have a declared family may be assumed
to be an attack on the network, and may be blocked. The best way to
ensure the success of your research project is to work with us directly.

A router family shares a private key so that participation in the family
cannot be spoofed. To configure a router family, click on the \'I2P
Internals\' link in the router console, and then on the \'Family\' tab.
Follow the instructions there to generate the private key for the first
router in the family. Then, export the key from that router, and import
it to other members of the family.


