 How to Upgrade
from 0.6.1.30 and Earlier 

• 2008-02-05: **Upgrading from 0.6.1.30 and Earlier Releases**

Since i2p\'s lead developer [has gone AWOL](),
we do not have his update signing key or access to www.i2p\[.net\] or
dev.i2p\[.net\]. Complication and zzz have generated new signing keys,
and they and Amiga are providing update file hosting. These changes must
be configured in your router to take effect.

Make the following configuration changes and your router will
automatically install the latest release.

We recommend the automated process as it will verify the key of the
signed update file. If you do not make these changes, you may manually
download the i2pupdate.zip file from [the download
page]().

1. On [configupdate.jsp](http://localhost:7657/configupdate.jsp):
 a. Change the News URL to: 
 b. Select ONE of the following new Update URLs at random and enter
 it into the Update URL box:\
 http://amiga.i2p/i2p/i2pupdate.sud\
 http://complication.i2p/i2p/i2pupdate.sud\
 http://stats.i2p/i2p/i2pupdate.sud
 c. Check the box \"Update through the eepProxy?\"
 d. Click \"Save\"
2. On [configadvanced.jsp](http://localhost:7657/configadvanced.jsp):
 a. Add the following line:\
 b. Click \"Apply\"
3. You are now ready to automatically receive the release update file,
 either by setting your update policy to \"download and install\" or
 by clicking on the \"update available\" link when it appears.

If you would like to verify the trusted update keys, they are also
[posted and signed here](). Thank you for your
support during this transition. For help please contact us on #i2p.

Amiga, Complication, welterde, zzz


