 jbigi August 2011 0.8.7 

## Áttekintés

Using JNI (Java Native Interface), a bit of C code (thanks ugha!), a
little manual work and a piece of chewing gum we have made several
cryptography operations quite a bit faster.

The speedup comes from the super-fast [GNU MP Bignum library
(libgmp)](). We use a single function from
libgmp - [mpz_powm()]() as a replacement for the
[Java Math library\'s BigInteger modPow()](). As
modPow() is a significant computational portion of many crypto
operations, this is of significant benefit.

The standard I2P installation includes about 20 versions of the library
for different platforms, each about 50KB, inside the jbigi.jar file. The
initialization of the JBigI library, including CPU identification,
selection, and extraction of the correct loadable module, is handled by
the [NativeBigInteger class](). If no
module is available for the current platform, the standard [Java Math
library\'s BigInteger modPow()]() is used.

## Rebuilding and Testing JBigI

Following are the instructions to build a new jbigi library for your own
platform and testing its performance.

### Requirements

This works on Linux, and with a few changes in build.sh probably also on
other platforms. FreeBSD has also been reported to work too. On Kaffee
the speedup is very small, because it already uses native BitInteger
internally. Blackdown seems to cause strange errors. Because you are
going to do compilation, you need JDK; JRE won\'t work.

The required code is available in monotone database and the latest
source tarball.

The GNU MP Bignum library (libgmp) needs to be installed, if it isn\'t
included in your OS / distribution or installed already, it can be
received from <http://gmplib.org/#DOWNLOAD>. Even if you have already
installed it as binary, it might still be worth a try to compile GMP
yourself, since then it will be able to use the specific instructions of
your processor. The latest GMP may also be used instead of GMP 5.0.2,
but it hasn\'t been tested by us.

### Step-by-step instructions

1. Look at [your running environment on the logs.jsp
 page](http://localhost:7657/logs.jsp). There should be one of two
 status messages for JBigI - either
 ` Locally optimized native BigInteger loaded from the library path `
 or ` Native BigInteger library jbigi not loaded - using pure java`.
 If the native BitInteger library was NOT loaded, you definitely need
 to compile your own. Certain platforms, such as OS X, OpenSolaris,
 and 64-bit systems, may require you to compile your own library. If
 the BigInteger library was loaded, do at least the next step to see
 what your performance is.

2. Look on <http://localhost:7657/stats.jsp> to see what the lifetime
 average values for `crypto.elGamal.decrypt` and
 `crypto.elGamal.encrypt` are. The numbers are times in milliseconds.
 Copy these somewhere so you can compare them later on. The network
 average for encrypt time is about 20ms. If your encrypt time is less
 than 50ms for a relatively new processor, or less than 100ms for an
 older processor, and the native BigInteger library was loaded, you
 are probably fine.

3. Get the latest released source code of I2P from [the download
 page](), or get the cutting-edge source
 out of the monotone database mtn.i2p2.de

4. Inside the source tree change directory to: `core/c/jbigi`

5. Read the README file. If you have a /usr/lib/libgmp.so file, you do
 not have to download GMP. Use the \'dynamic\' argument to build.sh.
 Otherwise, you must download GMP version 5.0.2 from from
 <http://gmplib.org/#DOWNLOAD>, saving it to gmp-5.0.2.tar.bz2. If
 you decide to use a newer version, change the VER= line in
 `core/c/jbigi/build.sh`.

6. Take a look at `build.sh`, if your `JAVA_HOME` environment variable
 is set and you are using Linux then it might just work. Otherwise
 change the settings. Remember, you need the Java SDK installed.

7. Run `build.sh` (if you downloaded GMP) or `build.sh dynamic` (if you
 have /usr/lib/libgmp.so).\
 Maybe the build spewed out some errors of missing jni.h and jni_md.h
 files. Either copy these files from your java install into the
 core/c/jbigi/jbigi/include/ directory, or fix \$JAVA_HOME.\
 You can run the `build.sh` from the `core/c/` directory which will
 build all available jbigi libs into a jbigi.jar. A file named
 `libjbigi.so` should be created in the current directory. If this
 doesn\'t happen and/or you get errors then please report them.

8. Follow the instructions in core/c/README to install the library and
 run the speed test. Read the final lines of the speed test\'s output
 for some additional info, it will be something like this:

 native run time: 5842ms ( 57ms each)
 java run time: 41072ms (406ms each)
 native = 14.223802103622907% of pure java time

 If the native is indeed 5-7x faster (or more) then it looks all
 good. If not, please report.

9. Copy `libjbigi.so` to your i2p directory

10. Restart your I2P programs.

11. On <http://localhost:7657/stats.jsp> the `crypto.elGamal.decrypt`
 and `crypto.elGamal.encrypt` should be a lot faster.


