 I2P Software
Licenses 

As required by our [threat model]() (among
other reasons), the software developed to support the anonymous
communication network we call I2P must be freely available, open source,
and user modifiable. To meet these criteria, we make use of a variety of
legal and software engineering techniques so as to remove as many
barriers to entry for those considering making use of or contributing to
the I2P effort.

While the information below may be more confusing than just simply
stating \"I2P is BSD\", \"I2P is GPL\", or \"I2P is public domain\", the
short answer to the question \"How is I2P licensed?\" is this:

## All software bundled in the I2P distributions will allow:

1. use without fee
2. use with no restrictions on how, when, where, why, or by whom is
 running it
3. access to the source code without fee
4. modifications to the source

Most of the software guarantees much more - the ability of **anyone** to
distribute the modified source however they choose. However, not all of
the software bundled provides this freedom - the GPL restricts the
ability of developers who wish to integrate I2P with their own
applications that are not themselves open source applications. While we
applaud the noble goals of increasing the resources in the commons, I2P
is best served by removing any barriers that stand in the way of its
adoption - if a developer considering whether they can integrate I2P
with their application has to stop and check with their lawyer, or
conduct a code audit to make sure their own source can be released as
GPL-compatible, we lose out.

## Component licenses

The I2P distribution contains several resources, reflecting the
partitioning of the source code into components. Each component has its
own license, which all developers who contribute to it agree to - either
by explicitly declaring the release of code committed under a license
compatible with that component, or by implicitly releasing the code
committed under the component\'s primary license. Each of these
components has a lead developer who has the final say as to what license
is compatible with the component\'s primary license, and the I2P project
manager has the final say as to what licenses meet the above four
guarantees for inclusion in the I2P distribution.

 ------------------------------------------------------- -------------------- ------------------- -------------------------------------------------------- -------------------------------------------------------- -------------
 **Component** **Source path** **Resource** **Primary license** **Alternate licenses** **Lead
 developer**

 **I2P SDK** core i2p.jar [Public [BSD](http://opensource.org/licenses/bsd-license.php)\ zzz
 domain](https://en.wikipedia.org/wiki/Public_domain) [Cryptix](http://www.cryptix.org/LICENSE.TXT)\ 
 [MIT](http://opensource.org/licenses/mit-license.html) 

 **I2P Router** router router.jar [Public [BSD](http://opensource.org/licenses/bsd-license.php)\ zzz
 domain](https://en.wikipedia.org/wiki/Public_domain) [Cryptix](http://www.cryptix.org/LICENSE.TXT)\ 
 [MIT](http://opensource.org/licenses/mit-license.html) 

 **Ministreaming** apps/ministreaming mstreaming.jar [BSD](http://opensource.org/licenses/bsd-license.php) [Public zzz
 domain](https://en.wikipedia.org/wiki/Public_domain)\ 
 [Cryptix](http://www.cryptix.org/LICENSE.TXT)\ 
 [MIT](http://opensource.org/licenses/mit-license.html) 

 **Streaming** apps/streaming streaming.jar [Public [BSD](http://opensource.org/licenses/bsd-license.php)\ zzz
 domain](https://en.wikipedia.org/wiki/Public_domain) [Cryptix](http://www.cryptix.org/LICENSE.TXT)\ 
 [MIT](http://opensource.org/licenses/mit-license.html) 

 **I2PTunnel** apps/i2ptunnel i2ptunnel.jar [GPL + exception](#java_exception) [Public zzz
 domain](https://en.wikipedia.org/wiki/Public_domain)\ 
 [BSD](http://opensource.org/licenses/bsd-license.php)\ 
 [Cryptix](http://www.cryptix.org/LICENSE.TXT)\ 
 [MIT](http://opensource.org/licenses/mit-license.html) 

 **Routerconsole** apps/routerconsole routerconsole.war [Public   zzz
 domain](https://en.wikipedia.org/wiki/Public_domain) 

 **Address Book** apps/addressbook addressbook.war [MIT](http://opensource.org/licenses/mit-license.html) [Public  
 domain](https://en.wikipedia.org/wiki/Public_domain)\ 
 [Cryptix](http://www.cryptix.org/LICENSE.TXT)\ 
 [BSD](http://opensource.org/licenses/bsd-license.php) 

 **Susidns** apps/susidns susidns.war [GPL + exception](#java_exception)    

 **Susimail** apps/susimail susimail.war [GPL + exception](#java_exception)    

 **I2PSnark** apps/i2psnark i2psnark.jar [GPL + exception](#java_exception)   zzz

 **[BOB]() apps/BOB BOB.jar [WTFPL](https://en.wikipedia.org/wiki/WTFPL)   sponge
 Bridge** 

 **[SAM]() apps/sam sam.jar [Public [Cryptix](http://www.cryptix.org/LICENSE.TXT)\ zzz
 Bridge** domain](https://en.wikipedia.org/wiki/Public_domain) [BSD](http://opensource.org/licenses/bsd-license.php)\ 
 [MIT](http://opensource.org/licenses/mit-license.html) 

 **[SAM v1]() apps/sam/perl SAM.pm [GPL](https://www.gnu.org/licenses/gpl-2.0.html) [Public BrianR
 Perl library** domain](https://en.wikipedia.org/wiki/Public_domain)\ 
 [Cryptix](http://www.cryptix.org/LICENSE.TXT)\ 
 [BSD](http://opensource.org/licenses/bsd-license.php)\ 
 [MIT](http://opensource.org/licenses/mit-license.html) 

 **[SAM v1]() apps/sam/c libSAM [BSD](http://opensource.org/licenses/bsd-license.php) [Public Nightblade
 C library** domain](https://en.wikipedia.org/wiki/Public_domain)\ 
 [Cryptix](http://www.cryptix.org/LICENSE.TXT)\ 
 [MIT](http://opensource.org/licenses/mit-license.html) 

 **[SAM v1]() apps/sam/python i2p.py [Public [BSD](http://opensource.org/licenses/bsd-license.php)\ Connelly
 Python library** domain](https://en.wikipedia.org/wiki/Public_domain) [Cryptix](http://www.cryptix.org/LICENSE.TXT)\ 
 [MIT](http://opensource.org/licenses/mit-license.html) 

 **[SAM v1]() apps/sam/csharp/ n/a [Public [BSD](http://opensource.org/licenses/bsd-license.php)\ smeghead
 C# library** domain](https://en.wikipedia.org/wiki/Public_domain) [Cryptix](http://www.cryptix.org/LICENSE.TXT)\ 
 [MIT](http://opensource.org/licenses/mit-license.html) 

 **Other apps not mentioned** apps/ \... Probably [Public    
 domain](https://en.wikipedia.org/wiki/Public_domain) but 
 check the source 

 **Installer** installer install.jar, [Public [GPL + exception](#java_exception)\  
 guiinstall.jar domain](https//en.wikipedia.org/wiki/Public_domain) [BSD](http://opensource.org/licenses/bsd-license.php)\ 
 [Cryptix](http://www.cryptix.org/LICENSE.TXT)\ 
 [MIT](http://opensource.org/licenses/mit-license.html) 
 ------------------------------------------------------- -------------------- ------------------- -------------------------------------------------------- -------------------------------------------------------- -------------

### [GPL + java exception]{#java_exception}

While it may be redundant, just for clarity the
[GPL]()\'ed code included within I2PTunnel and
other apps must be released under the GPL with an additional
\"exception\" explicitly authorizing the use of Java\'s standard
libraries:

`In addition, as a special exception, XXXX gives permission to link the code of this program with the proprietary Java implementation provided by Sun (or other vendors as well), and distribute linked combinations including the two. You must obey the GNU General Public License in all respects for all of the code used other than the proprietary Java implementation. If you modify this file, you may extend this exception to your version of the file, but you are not obligated to do so. If you do not wish to do so, delete this exception statement from your version.`

All source code under each component will by default be licensed under
the primary license, unless marked otherwise in the code. All of the
above is summary of the license terms - please see the specific license
for the component or source code in question for authoritative terms.
Component source locations and resource packaging may be changed if the
repository is reorganized.

## [Website content]{#website}

[![Creative Commons
License](images/cc-by-sa-4.0.png){style="border-width:0"}](http://creativecommons.org/licenses/by-sa/4.0/){rel="license"}

Except where otherwise noted, content on this site is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International
License](http://creativecommons.org/licenses/by-sa/4.0/){rel="license"}.

## [Commit privileges]{#commit}

Developers may push changes to a distributed git repository if you
receive permission from the person running that repository. See the [Git
Page]() for details.

However, to have changes included in a release, developers must be
trusted by the release manager (currently zzz). In addition, they must
explicitly agree with the above terms to be trusted. That means that
they must send one of the release managers a signed message affirming
that:

- Unless marked otherwise, all code I commit is implicitly licensed
 under the component\'s primary license
- If specified in the source, the code may be explicitly licensed
 under one of the component\'s alternate licenses
- I have the right to release the code I commit under the terms I am
 committing it

If anyone is aware of any instances where the above conditions are not
met, please contact the component lead and/or an I2P release manager
with further information. [See developers\' license
agreements]().


