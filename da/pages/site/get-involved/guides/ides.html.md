 Using an IDE with
I2P 

The main I2P development branch (`i2p.i2p`) has been set up to enable
developers to easily set up two of the commonly-used IDEs for Java
development: Eclipse and NetBeans.

## Eclipse

The main I2P development branches (`i2p.i2p` and branches from it)
contain build.gradle to enable the branch to be easily set up in
Eclipse.

1. Make sure you have a recent version of Eclipse. Anything newer than
 2017 should do.
2. Check out the I2P branch into some directory (e.g.
 `$HOME/dev/i2p.i2p`).
3. Select \"File - Import\...\" and then under \"Gradle\" select
 \"Existing Gradle Project\".
4. For \"Project root directory:\" choose the directory that the I2P
 branch was checked out to.
5. In the \"Import Options\" dialog, select \"Gradle Wrapper\" and
 press continue.
6. In the \"Import Preview\" dialog you can review the project
 structure. Multiple projects should appear under \"i2p.i2p\". Press
 \"Finish.\"
7. Done! Your workspace should now contain all projects within the I2P
 branch, and their build dependencies should be correctly set up.

## NetBeans

The main I2P development branches (`i2p.i2p` and branches from it)
contain NetBeans project files.


