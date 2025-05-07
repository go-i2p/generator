 Strict Countries 2024-07 

This implementation of I2P (the Java implementation distributed on this
site) includes a \"Strict Countries List\" which we use to decide how
routers should behave within regions where applications like I2P may be
limited by law. For example, while no countries that we know of prohibit
using I2P, some have broad prohibitions on participating in routing for
others. Routers that appear to be in the \"Strict\" countries will
automatically be placed into \"Hidden\" mode.

The Project relies on the research provided by civil and digital rights
organizations in order to make decisions that offer protections for its
users. In this case the ongoing research provided by [Freedom
House](https://freedomhouse.org/) has been referenced. General guidance
is to include countries with a Civil Liberties (CL) score of 16 or less
or an Internet Freedom score of 39 or less (not free).

#### Hidden Mode Summary

When a router is placed into hidden mode, three key things change about
its behavior. It will no longer publish a routerInfo to the NetDB, it
will no longer accept participating tunnels, and it will reject direct
connections to routers in the same country that it is in. These defenses
make the routers more difficult to enumerate reliably, and prevent them
from running afoul of restrictions on routing traffic for others.

#### Strict Countries List as of 2024

 /* Afghanistan */ "AF",
 /* Azerbaijan */ "AZ",
 /* Bahrain */ "BH",
 /* Belarus */ "BY",
 /* Brunei */ "BN",
 /* Burundi */ "BI",
 /* Cameroon */ "CM",
 /* Central African Republic */ "CF",
 /* Chad */ "TD",
 /* China */ "CN",
 /* Cuba */ "CU",
 /* Democratic Republic of the Congo */ "CD",
 /* Egypt */ "EG",
 /* Equatorial Guinea */ "GQ",
 /* Eritrea */ "ER",
 /* Ethiopia */ "ET",
 /* Iran */ "IR",
 /* Iraq */ "IQ",
 /* Kazakhstan */ "KZ",
 /* Laos */ "LA",
 /* Libya */ "LY",
 /* Myanmar */ "MM",
 /* North Korea */ "KP",
 /* Palestinian Territories */ "PS",
 /* Pakistan */ "PK",
 /* Rwanda */ "RW",
 /* Saudi Arabia */ "SA",
 /* Somalia */ "SO",
 /* South Sudan */ "SS",
 /* Sudan */ "SD",
 /* Eswatini (Swaziland) */ "SZ",
 /* Syria */ "SY",
 /* Tajikistan */ "TJ",
 /* Thailand */ "TH",
 /* Turkey */ "TR",
 /* Turkmenistan */ "TM",
 /* Venezuela */ "VE",
 /* United Arab Emirates */ "AE",
 /* Uzbekistan */ "UZ",
 /* Vietnam */ "VN",
 /* Western Sahara */ "EH",
 /* Yemen */ "YE"

[If you think a country should be added to the strict countries, file an
issue on the I2P gitlab.](https://i2pgit.org/i2p/i2p.i2p/)


