# [Crypto++](http://www.cryptopp.com) 5.2.1 Benchmarks

Here are speed benchmarks for some of the most commonly used
cryptographic algorithms. All were coded in C++, compiled with Microsoft
Visual C++ .NET 2003 (whole program optimization, optimize for speed, P4
code generation), and ran on a Pentium 4 2.1 GHz processor under Windows
XP SP 1. 386 assembly routines were used for multiple-precision addition
and subtraction. SSE2 intrinsics were used for multiple-precision
multiplication.

Also available are [benchmarks that ran on an AMD Opteron 1.6 GHz
processor under Linux
2.4.21](http://www.eskimo.com.wstub.archive.org/~weidai/amd64-benchmarks.html).
Those were compiled with GCC 3.2.2 using -O2 optimization, and inline
assembly was used to access the 64-bit multiplication instruction.

Algorithm

Megabytes(2\^20 bytes) Processed

Time Taken

MB/Second

CRC-32

2.05e+003

6.399

320.050

Adler-32

4.1e+003

3.525

1161.986

MD2

16

4.006

3.994

MD5

1.02e+003

4.726

216.674

SHA-1

256

3.766

67.977

SHA-256

256

5.758

44.460

SHA-512

64

5.618

11.392

HAVAL (pass=3)

512

4.717

108.544

HAVAL (pass=4)

256

3.695

69.283

HAVAL (pass=5)

256

3.796

67.439

Tiger

128

3.364

38.050

RIPE-MD160

256

4.867

52.599

Panama Hash (little endian)

1.02e+003

3.375

303.407

Panama Hash (big endian)

1.02e+003

4.637

220.832

Whirlpool

64

5.288

12.103

MDC/MD5

256

5.377

47.610

Luby-Rackoff/MD5

64

4.307

14.860

DES

128

5.998

21.340

DES-XEX3

128

6.159

20.783

DES-EDE3

64

6.499

9.848

IDEA

64

3.375

18.963

RC2

64

5.548

11.536

RC5 (r=16)

256

4.286

59.729

Blowfish

256

3.976

64.386

3-WAY

128

3.665

34.789

TEA

128

5.378

23.801

SAFER (r=8)

128

6.279

20.385

GOST

128

3.505

36.519

SHARK (r=6)

128

3.826

33.455

CAST-128

256

5.988

42.752

CAST-256

128

5.889

21.735

Square

128

4.176

30.651

SKIPJACK

128

6.329

20.224

RC6

128

3.385

37.814

MARS

128

4.586

27.911

Rijndael (128-bit key)

256

4.196

61.010

Rijndael (192-bit key)

256

4.817

53.145

Rijndael (256-bit key)

256

5.308

48.229

Rijndael (128) CTR

256

4.436

57.710

Rijndael (128) OFB

256

4.837

52.925

Rijndael (128) CFB

256

5.378

47.601

Rijndael (128) CBC

256

4.617

55.447

Twofish

128

4.075

31.411

Serpent

128

6.069

21.091

ARC4

512

4.517

113.350

SEAL-3.0-BE

1.02e+003

3.485

293.831

SEAL-3.0-LE

2.05e+003

4.937

414.827

WAKE-CFB-BE

512

5.498

93.125

WAKE-CFB-LE

512

3.615

141.632

WAKE-OFB-BE

512

3.855

132.815

WAKE-OFB-LE

512

3.836

133.472

Panama Cipher (little endian)

1.02e+003

4.036

253.717

Panama Cipher (big endian)

1.02e+003

5.317

192.590

SHACAL-2 (128-bit key)

128

6.279

20.385

SHACAL-2 (512-bit key)

128

6.279

20.385

Camellia (128-bit key)

64

3.355

19.076

Camellia (192-bit key)

64

4.437

14.424

Camellia (256-bit key)

64

4.416

14.493

MD5-MAC

1.02e+003

5.528

185.239

XMACC/MD5

1.02e+003

5.999

170.695

HMAC/MD5

1.02e+003

4.726

216.674

Two-Track-MAC

256

4.817

53.145

CBC-MAC/Rijndael

256

4.447

57.567

DMAC/Rijndael

256

4.476

57.194

BlumBlumShub 512

0.25

3.585

0.070

BlumBlumShub 1024

0.125

4.096

0.031

BlumBlumShub 2048

0.0625

5.869

0.011

Operation

Iterations

Total Time

Milliseconds/Operation

RSA 1024 Encryption

27607

5.007

0.18

RSA 1024 Decryption

1050

5.007

4.77

Rabin 1024 Encryption

3008

5.007

1.66

Rabin 1024 Decryption

795

5.007

6.30

LUC 1024 Encryption

23544

5.008

0.21

LUC 1024 Decryption

634

5.007

7.90

DLIES 1024 Encryption

1159

5.007

4.32

DLIES 1024 Encryption with precomputation

1061

5.007

4.72

DLIES 1024 Decryption

350

5.008

14.31

LUCELG 512 Encryption

2433

5.007

2.06

LUCELG 512 Encryption with precomputation

2402

5.007

2.08

LUCELG 512 Decryption

2744

5.007

1.82

RSA 2048 Encryption

11022

5.007

0.45

RSA 2048 Decryption

177

5.028

28.41

Rabin 2048 Encryption

1254

5.007

3.99

Rabin 2048 Decryption

159

5.027

31.62

LUC 2048 Encryption

8756

5.007

0.57

LUC 2048 Decryption

110

5.037

45.79

DLIES 2048 Encryption

260

5.007

19.26

DLIES 2048 Encryption with precomputation

269

5.017

18.65

DLIES 2048 Decryption

60

5.027

83.78

LUCELG 1024 Encryption

532

5.008

9.41

LUCELG 1024 Encryption with precomputation

531

5.007

9.43

LUCELG 1024 Decryption

772

5.007

6.49

RSA 1024 Signature

1053

5.007

4.75

RSA 1024 Verification

27406

5.007

0.18

Rabin 1024 Signature

816

5.008

6.14

Rabin 1024 Verification

3117

5.007

1.61

RW 1024 Signature

951

5.007

5.26

RW 1024 Verification

55580

5.007

0.09

LUC 1024 Signature

644

5.007

7.77

LUC 1024 Verification

24321

5.008

0.21

NR 1024 Signature

2260

5.007

2.22

NR 1024 Signature with precomputation

4376

5.007

1.14

NR 1024 Verification

1964

5.007

2.55

NR 1024 Verification with precomputation

2738

5.007

1.83

DSA 1024 Signature

2301

5.008

2.18

DSA 1024 Signature with precomputation

4444

5.007

1.13

DSA 1024 Verification

2007

5.007

2.49

DSA 1024 Verification with precomputation

2795

5.007

1.79

LUC-HMP 512 Signature

2365

5.007

2.12

LUC-HMP 512 Signature with precomputation

2401

5.008

2.09

LUC-HMP 512 Verification

2312

5.007

2.17

LUC-HMP 512 Verification with precomputation

2269

5.007

2.21

ESIGN 1023 Signature

9837

5.007

0.51

ESIGN 1023 Verification

27679

5.007

0.18

ESIGN 1536 Signature

4898

5.008

1.02

ESIGN 1536 Verification

11940

5.007

0.42

RSA 2048 Signature

178

5.007

28.13

RSA 2048 Verification

11054

5.007

0.45

Rabin 2048 Signature

158

5.028

31.82

Rabin 2048 Verification

1294

5.007

3.87

RW 2048 Signature

176

5.017

28.51

RW 2048 Verification

24521

5.007

0.20

LUC 2048 Signature

110

5.007

45.52

LUC 2048 Verification

9072

5.008

0.55

NR 2048 Signature

511

5.007

9.80

NR 2048 Signature with precomputation

1530

5.007

3.27

NR 2048 Verification

454

5.007

11.03

NR 2048 Verification with precomputation

982

5.008

5.10

LUC-HMP 1024 Signature

522

5.007

9.59

LUC-HMP 1024 Signature with precomputation

527

5.007

9.50

LUC-HMP 1024 Verification

520

5.007

9.63

LUC-HMP 1024 Verification with precomputation

499

5.007

10.03

ESIGN 2046 Signature

4253

5.008

1.18

ESIGN 2046 Verification

11024

5.007

0.45

XTR-DH 171 Key-Pair Generation

2802

5.007

1.79

XTR-DH 171 Key Agreement

1360

5.007

3.68

XTR-DH 342 Key-Pair Generation

777

5.007

6.44

XTR-DH 342 Key Agreement

404

5.018

12.42

DH 1024 Key-Pair Generation

2283

5.007

2.19

DH 1024 Key-Pair Generation with precomputation

2072

5.007

2.42

DH 1024 Key Agreement

1298

5.007

3.86

DH 2048 Key-Pair Generation

512

5.007

9.78

DH 2048 Key-Pair Generation with precomputation

524

5.007

9.56

DH 2048 Key Agreement

368

5.027

13.66

LUCDIF 512 Key-Pair Generation

4688

5.007

1.07

LUCDIF 512 Key-Pair Generation with precomputation

4339

5.007

1.15

LUCDIF 512 Key Agreement

2880

5.008

1.74

LUCDIF 1024 Key-Pair Generation

1057

5.007

4.74

LUCDIF 1024 Key-Pair Generation with precomputation

1037

5.007

4.83

LUCDIF 1024 Key Agreement

776

5.017

6.47

MQV 1024 Key-Pair Generation

2311

5.007

2.17

MQV 1024 Key-Pair Generation with precomputation

4595

5.008

1.09

MQV 1024 Key Agreement

1224

5.007

4.09

MQV 2048 Key-Pair Generation

522

5.007

9.59

MQV 2048 Key-Pair Generation with precomputation

1572

5.007

3.19

MQV 2048 Key Agreement

282

5.017

17.79

ECIES over GF(p) 168 Encryption

759

5.008

6.60

ECIES over GF(p) 168 Encryption with precomputation

1327

5.007

3.77

ECIES over GF(p) 168 Decryption

1062

5.007

4.71

ECNR over GF(p) 168 Signature

1497

5.007

3.34

ECNR over GF(p) 168 Signature with precomputation

2629

5.007

1.90

ECNR over GF(p) 168 Verification

794

5.008

6.31

ECNR over GF(p) 168 Verification with precomputation

1618

5.007

3.09

ECDHC over GF(p) 168 Key-Pair Generation

1536

5.007

3.26

ECDHC over GF(p) 168 Key-Pair Generation with precomputation

2576

5.007

1.94

ECDHC over GF(p) 168 Key Agreement

1474

5.007

3.40

ECMQVC over GF(p) 168 Key-Pair Generation

1529

5.008

3.28

ECMQVC over GF(p) 168 Key-Pair Generation with precomputation

2588

5.007

1.93

ECMQVC over GF(p) 168 Key Agreement

746

5.007

6.71

ECIES over GF(2\^n) 155 Encryption

414

5.007

12.09

ECIES over GF(2\^n) 155 Encryption with precomputation

1071

5.008

4.68

ECIES over GF(2\^n) 155 Decryption

633

5.007

7.91

ECNR over GF(2\^n) 155 Signature

827

5.007

6.05

ECNR over GF(2\^n) 155 Signature with precomputation

2132

5.007

2.35

ECNR over GF(2\^n) 155 Verification

655

5.007

7.64

ECNR over GF(2\^n) 155 Verification with precomputation

1232

5.008

4.06

ECDHC over GF(2\^n) 155 Key-Pair Generation

806

5.007

6.21

ECDHC over GF(2\^n) 155 Key-Pair Generation with precomputation

2124

5.007

2.36

ECDHC over GF(2\^n) 155 Key Agreement

780

5.007

6.42

ECMQVC over GF(2\^n) 155 Key-Pair Generation

816

5.007

6.14

ECMQVC over GF(2\^n) 155 Key-Pair Generation with precomputation

2116

5.008

2.37

ECMQVC over GF(2\^n) 155 Key Agreement

660

5.017

7.60

## Notes

- Crypto++ 5.2.1 Benchmark Average for this platform: **135.54**. This
 number is computed by taking the geometric mean of the number of
 MB/second of each cipher, hash function, and MAC, and
 operations/second of each asymmetric operation listed above.
- RSA and LUC use 17 as the public exponent.
- DH and ElGamal encryption and decryption use short exponents to save
 time. The size of the secret exponents were chosen so that a
 meet-in-the-middle attack would be slower than the general discrete
 log algorithm (NFS). The sizes used were:
 modulus
 exponent
 512
 120
 1024
 164
 2048
 226
- EC means elliptic curve. Operations in GF(2\^n) are implemented
 using trinomial basis. Note that compared to other algorithms listed
 here, Crypto++\'s implementation of EC over GF(2\^n) is less
 optimized.
- All tests were done by repeating the crypto operations over small
 blocks of random data. In practice you will likely see slower speeds
 because time is needed to transfer data to and from memory.
- For the ciphers that specify big endian byte order, the timing data
 listed include time needed to convert to and from little endian
 order. For some ciphers (WAKE and SHA) this is a large fraction (up
 to 25%) of the total time.
- The RSA, RW, DH, MQV, and elliptic curve schemes come from the IEEE
 P1363 standard. For more info see
 <http://grouper.ieee.org/groups/1363/index.html>.
- Precomputation means using a table of 16 precomputed powers of each
 fixed base to speed up exponentiation.
- Tiger, SHARK, SHA-384, and SHA-512 are designed to take advantage of
 64-bit word operations. Their relatives speeds can be expected to be
 much higher if the benchmarks were done on a 64-bit CPU.
- Source code for these benchmarks is available as part of the
 [Crypto++](http://www.cryptopp.com) library.

------------------------------------------------------------------------

Written by: [Wei Dai](http://www.weidai.com) \<<webmaster@weidai.com>\>
Last modified: 7/23/2004
