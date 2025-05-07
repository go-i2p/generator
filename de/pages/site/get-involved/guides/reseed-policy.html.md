 I2P Reseed Server
Policy Requirements and Guidelines 2023-01 

## Reseed Policy Information

### Requirements

Requirements for running a public reseed server:

- Well integrated running I2P router @ 24/7
- Server with static IPv4 (2 cpu/ 2GB ram is fine)
- Unix to run the golang solution
- Own domain, sub-domain or an anonymous third-level domain
- A self-signed SSL certificate, or an SSL certificate from [Let\'s
 Encrypt](https://letsencrypt.org){target="_blank"}
- Enough bandwidth and traffic volume - Around 15 GB/month as of
 December 2016
- Up-to-date web server (Apache/nginx), HTTPS ONLY with TLS 1.2 and
 good ciphers

Optional:

- fail2ban to protect you from botnets
- GnuPG/PGP for signed/encrypted emails
- IPv6

### Information Required

When your setup is complete and ready for testing, we will need the
HTTPS URL, the SSL public key certificate (only if selfsigned), and the
su3 public key certificate. After testing is complete, these will be
added to the hardcoded entries in the Java and C++ routers in the next
release, and you will start seeing traffic. We also will need your email
address so we may continue to contact you about reseed administration
issues. The email will not be made public but will be known to the other
reseed operators. You should expect that your nick or name and its
association with that URL or IP will become public.

### Privacy Policy

A reseed operator is a trusted role in the network. While we do not yet
have a formal privacy policy, you must ensure the privacy of our users
by not publicizing logs or IPs found in those logs, except as necessary
to discuss administration issues with the I2P reseed team.

### Financial Support

Modest financial support may be available to those running reseed
servers. This support would be in partial reimbursement for your server
costs. Support will not be paid in advance and will probably not cover
all your expenses. Support is only available to those who have been
running reseed servers in good standing for several months, and is based
on actual need.

If you would like to discuss support, please contact echelon and CC: zzz


