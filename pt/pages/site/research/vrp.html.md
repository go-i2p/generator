 Vulnerability
Response Process 2023-04 vrp 

This process is subject to change. Please refer to this page for the
current VRP. 

Echelon is the trusted security point-of-contact. He forwards emails to
team members as appropriate.

## III. Incident Response

1. Researcher submits report via: security (at) geti2p.net
2. Response Team designates a Response Manager who is in charge of the
 particular report based on availability and/or knowledge-set.
3. In no more than working days, Response Team should respond
 to researcher using only encrypted methods.
4. Response Manager makes inquiries to satisfy any needed information
 and to confirm if submission is indeed a vulnerability.
 1. If submission proves to be vulnerable, proceed.
 2. If not vulnerable:
 1. Response Manager responds with reasons why submission is not
 a vulnerability.
 2. Response Manager moves discussion to a new or existing
 ticket on public Trac if necessary.
5. Affects network as a whole, has potential to break entire network or
 is on a scale of great catastrophe.
 MEDIUM
 Affects individual routers, or must be carefully exploited.
 LOW
 Is not easily exploitable.
6. Respond according to the severity of the vulnerability:
 1. HIGH severities must be notified on website and news feed within
 working days of classification.
 1. The notification should list appropriate steps for users to
 take, if any.
 2. The notification must not include any details that could
 suggest an exploitation path.
 3. The latter takes precedence over the former.
 2. MEDIUM and HIGH severities will require a Point Release.
 3. LOW severities will be addressed in the next Regular Release.
7. Response Team applies appropriate patch(es).
 1. Response Manager works on a patch LOCALLY, patches are shared by
 the response team via PGP-encrypted e-mail until such a time as
 it is safe to expose to the public.
 2. Patches are reviewed with the researcher.
 3. Any messages associated with PUBLIC commits during the time of
 review should not make reference to the security nature of the
 PRIVATE branch or its commits.
 4. Vulnerability announcement is drafted.
 1. Include severity of vulnerability.
 2. Include systems/apps effected.
 3. Include solutions (if any) if patch cannot be applied.
 5. Release date is discussed.
8. At release date, Response Team coordinates with developers to
 finalize update:
 1. Response Manager propagates the \"hotfix branch\" to trunk.
 2. Response Manager includes vulnerability announcement draft in
 release notes.
 3. Proceed with the Point or Regular Release. At this time, it is
 not possible to release an in-network update for only one
 operating system or architecture. In order that all affected
 products can be released as quickly as possible, the person
 responsible for that software should be able to perform
 necessary release processes in a timely manner. Importantly this
 should include consideration for package maintainers in Debian,
 Ubuntu and F-Droid.

## IV. Post-release Disclosure Process

1. Response Team has days to fulfill all points within
 section III.
2. If the Incident Response process in section III is successfully
 completed:
 1. Response Manager contacts researcher and asks if researcher
 wishes for credit.

 2. Finalize vulnerability announcement draft and include the
 following:
 1. Project name and URL.
 2. Versions known to be affected.
 3. Versions known to be not affected (for example, the
 vulnerable code was introduced in a recent version, and
 older versions are therefore unaffected).
 4. Versions not checked.
 5. Type of vulnerability and its impact.
 6. If already obtained or applicable, a CVE-ID.
 7. The planned, coordinated release date.
 8. Mitigating factors (for example, the vulnerability is only
 exposed in uncommon, non-default configurations).
 9. Workarounds (configuration changes users can make to reduce
 their exposure to the vulnerability).
 10. If applicable, credits to the original reporter.

 3. Release finalized vulnerability announcement on website and in
 news feed.

 4. 1. If the vulnerability may be exploited while the network is
 being upgraded, delay the announcement until the vulnerable
 routers are upgraded.
 2. After the update is successful, write the announcement for
 the news feed, send it for translation, and release it.
 3. When translations come in, news operators should pull in the
 translations and update their feeds.

 5. For HIGH severities, release finalized vulnerability
 announcement on well-known mailing lists:
 1. oss-security@lists.openwall.com
 2. bugtraq@securityfocus.com

 6. If applicable, developers request a CVE-ID.
 1. The commit that applied the fix is made reference too in a
 future commit and includes a CVE-ID.
3. If the Incident Response process in section III is \*not\*
 successfully completed:
 1. Response Team and developers organize an IRC meeting to discuss
 why/what points in section III were not resolved and how the
 team can resolve them in the future.
 2. Any developer meetings immediately following the incident should
 include points made in section V.
 3. If disputes arise about whether or when to disclose information
 about a vulnerability, the Response Team will publicly discuss
 the issue via IRC and attempt to reach consensus.
 4. If consensus on a timely disclosure is not met (no later than
 days), the researcher (after days) has every
 right to expose the vulnerability to the public.

## V. Incident Analysis

1. Isolate codebase
 1. Response Team and developers should coordinate to work on the
 following:
 1. Problematic implementation of classes/libraries/functions,
 etc.
 2. Focus on apps/distro packaging, etc.
 3. Operator/config error, etc.
2. Auditing
 1. Response Team and developers should coordinate to work on the
 following:
 1. Auditing of problem area(s) as discussed in point 1.
 2. Generate internal reports and store for future reference.
 3. If results are not sensitive, share with the public via IRC
 or public Trac.
3. Response Team has days following completion of section III
 to ensure completion of section V.

## VI. Resolutions

Any further questions or resolutions regarding the incident(s) between
the researcher and response + development team after public disclosure
can be addressed via the following:

1. Trac
2. IRC
3. Email
4. Twitter

## VII. Continuous Improvement

1. Response Team and developers should hold annual meetings to review
 the previous year\'s incidents.
2. Response Team or designated person(s) should give a brief
 presentation, including:
 1. Areas of I2P affected by the incidents.
 2. Any network downtime or monetary cost (if any) of the incidents.
 3. Ways in which the incidents could have been avoided (if any).
 4. How effective this process was in dealing with the incidents.
3. After the presentation, Response Team and developers should discuss:
 1. Potential changes to development processes to reduce future
 incidents.
 2. Potential changes to this process to improve future responses.


