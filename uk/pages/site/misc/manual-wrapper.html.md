 Manually
Installing the Java Wrapper 

# Manually Installing the Java Wrapper

The installation package for the [I2P
router]() comes with a Java wrapper for the
most common architectures. If your system is not supported by our
installer---or if you want to update the wrapper to a newer
version---the following steps describe installing the wrapper manually.

- Check Tanuki Software\'s [download
 page](http://wrapper.tanukisoftware.com/doc/english/download.jsp#stable)
 for your platform. Is your platform listed? If so, you\'re in luck!
 Download the most recent version of the Community Edition for your
 OS and CPU and move to [the next step](#packaged).
- If your platform does not have an already compiled wrapper
 available, you may be able to compile it yourself. If you are
 willing to have a go at it, move on to [compiling](#compiling) the
 wrapper for your system.

## Using existing binaries {#packaged}

In the steps below, \$I2P means *the location I2P was installed to*.

1. `tar xzf wrapper-*.tar.gz`
2. `cp wrapper*/bin/wrapper $I2P/i2psvc`
3. `cp wrapper*/lib/wrapper.jar $I2P/lib`
4. `cp wrapper*/lib/libwrapper.so $I2P/lib`
5. Try to start I2P using `$I2P/i2prouter start`
6. `tail -f /tmp/wrapper.log` and look for any problems.

If this did not work you\'ll need to use `runplain.sh` to start I2P.

## Compiling from source {#compiling}

These steps worked to compile the wrapper for use on a mipsel system
running Debian. The steps **will** need to be altered for your system.

1. Download the source archive for the community version of the wrapper
 from [wrapper download
 page](http://wrapper.tanukisoftware.com/downloads).
2. Extract the tarball\
     `tar xzf wrapper_3.5.13_src.tar.gz`
3. Set environment variables `ANT_HOME` and `JAVA_HOME`. For example,
 in Debian:\
     `export ANT_HOME=/usr/share/ant`\
     `export JAVA_HOME=/usr/lib/jvm/default-java`
4. Since there isn\'t a Makefile for Mipsel, we\'ll make a copy of an
 already existing makefile:\
     `cp src/c/Makefile-linux-x86-32.make src/c/Makefile-linux-mipsel-32.make`
5. Now we can attempt to compile the wrapper:\
     `./build32.sh` (use `./build64.sh` if you have a 64bit CPU and
 JVM)
6. Copy the wrapper into its proper place:
 - `cp bin/wrapper $I2P/i2psvc`
 - `cp lib/wrapper.jar $I2P/lib`
 - `cp lib/libwrapper.so $I2P/lib`
7. Try to start I2P using `$I2P/i2prouter start`
8. `tail -f /tmp/wrapper.log` and look for any problems.

If this did not work you\'ll need to use `runplain.sh` to start I2P.


