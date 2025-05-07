 Ticket 1056 fix 

The issue described on this page only affects some Windows systems
upgrading from an earlier version to 0.9.8. Other operating systems are
not affected.

This issue has been corrected as of the [0.9.8.1
release]().

There are two possible ways to resolve this problem.

## Option 1

1. Stop I2P
2. Browser to `%APPDATA%\I2P` or wherever your I2P data dir is
3. Delete the files `router.info` and `router.keys`
4. Start I2P

## Option 2

Upgrade your I2P installation to to
[0.9.8.1](#update) by
following the instructions
[here](#update). 
