 Ministreaming
Library 

## Observera

The ministreaming library has been enhanced and extended by the \"full\"
[streaming library](). Ministreaming is
deprecated and is incompatible with today\'s applications. The following
documentation is old. Also note that streaming extends ministreaming in
the same Java package (net.i2p.client.streaming), so the current [API
documentation]() contains both. Obsolete
ministreaming classes and methods are clearly marked as deprecated in
the Javadocs.

## Ministreaming Library

The ministreaming library was written by mihi as a part of his
[I2PTunnel]() application and then factored
out and released under the BSD license. It is called the
\"mini\"streaming library because it makes some simplifications in the
implementation, while a more robust streaming library could be further
optimized for operation over I2P. The two main issues with the
ministreaming library are its use of the traditional TCP two phase
establishment protocol and the current fixed window size of 1. The
establishment issue is minor for long lived streams, but for short ones,
such as quick HTTP requests, the impact can be
[significant](). As for the window size, the
ministreaming library doesn\'t maintain any ID or ordering within the
messages sent (or include any application level ACK or SACK), so it must
wait on average twice the time it takes to send a message before sending
another.

Even with those issues, the ministreaming library performs quite well in
many situations, and its [API]() is both quite
simple and capable of remaining unchanged as different streaming
implementations are introduced. The library is deployed in its own
ministreaming.jar. Developers in Java who would like to use it can
access the API directly, while developers in other languages can use it
through [SAM]()\'s streaming support.


