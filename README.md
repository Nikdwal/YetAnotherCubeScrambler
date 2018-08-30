**YASG**: Yet Another Scramble Generator
-------------------
YASG is a program that can generate scrambles for a variety of different methods to solve the Rubik's Cube. It was designed to be a command line program, but there is a minimal graphical wrapper for it. You can generate the type of scramble you need by calling the program with a variety of options (flags). If you use the graphical version of this program, these should be entered in the text box in the main window. A full list of options can be obtained by running the program with the ```-h``` or ```--help``` flag. A guide on how to use them is found below.

Dependencies: ```kociemba``` (required) and ```TKinter``` (if you want to use the graphical program). Both can bit installed with PIP.

Just running the program without any commands specified gives a random state. If you want to scramble for a specific cube state, enter the following options in the command line or text box.

### Options

```-s STEP``` or ```--step=STEP```

This is by far the most useful flag.. Many substeps are supported, including, but not limited to, OLL, PLL, COLL, EPLL, SB, ZZF2L, LS, EJLS etc. Use ```-h```  or ```--help``` for an exhaustive list.

##### *examples*
```-s PLL``` or ```--step=PLL```

*example result:* R2 D' R2 F2 U' F2 D R2 B2 U L R' U2 L' R'

![image](http://cube.crider.co.uk/visualcube.php?fmt=svg&alg=R2D'R2F2U'F2DR2B2ULR'U2L'R')

```-s ZZLS``` or ```--step=ZZLS```

*example result:* L2 D' L2 U2 F2 R2 U' L2 B2 L' R' U' R' U F2 L'

![image](http://cube.crider.co.uk/visualcube.php?fmt=svg&alg=L2D'L2U2F2R2U'L2B2L'R'U'R'UF2L')

-------------

```--co```, ```--cp```, ```--eo```, and ```--ep```

Specify the corners and edges that can be disoriented or permuted. This exists just in case any substep isn't supported yet.
You can either specify specific pieces or an entire (outer) layer. If you use a flag, but don't specifiy any pieces, no pieces will be affected (e.g. using ```--eo ""``` ensures none of the edges will be disoriented). If you omit one of these four flags, this is equivalent to using it with all pieces (e.g. if you don't use ```--ep```, all edge pieces may be permuted).

##### *examples*
<sub>(This is purely for illustrative purposes. You can just use the ```-s``` flag for common subsets.)</sub>

<u>ZZ Last Slot scrambler:</u>

```--co "U DFR" --cp "U DFR" --eo "" --ep "U FR"```
This disorients and permutes the corners in the U layer as well as the DFR corner. It leaves EO undisturbed and it permutes the edges in the U layer and the FR edge.

*example result:* F2 U2 R2 D2 L2 D' B2 D L2 B2 L' B2 D2 R' U2 R' U' F2

![image](http://cube.crider.co.uk/visualcube.php?fmt=svg&alg=F2U2R2D2L2D'B2DL2B2L'B2D2R'U2R'U'F2)


<u>F2L scrambler:</ul>

```--ep "U FR FL BR BL" --eo "U FR FL BR BL"```. This is basically the same spiel. CO and CP are scrambled for all corners, because the flags for both are not specified.

*example result*: F2 U' R2 U2 L2 U2 F2 D' F2 L U2 R' F R U R2 D' U' B2 L2

![image](http://cube.crider.co.uk/visualcube.php?fmt=svg&alg=F2U'R2U2L2U2F2D'F2LU2R'FRUR2D'U'B2L2)

--------

```-c OCLL, --ocll=OCLL```

This forces a specific corner case for the last layer. You can enter a single OCLL case or a list in quotation marks, in which case it will choose one randomly. The names of these OCLL cases are U, T, L, H, Pi (or Bruno), S (or Sune), and AS (or Antisune). You should probably use this in combination with other flags

##### *examples*
```-s CMLL -c "H Pi"``` or equivalently ```-step=CMLL -ocll="H Pi"```

*example result:* B2 L2 D U2 L2 D2 U' B2 D B U' R' U L2 F2 L2 R B' U2

![image](http://cube.crider.co.uk/visualcube.php?fmt=svg&alg=B2L2DU2L2D2U'B2DBU'R'UL2F2L2RB'U2)



----------
```-e``` or ```--badedges```

This is made specifically for ZZ users. It generates a scramble with a given number of bad edges. This is the only way to ensure that exactly *N* edges are disoriented, as opposed to *at most N*, which can be done to some extent with the ```--eo``` flag.

##### *examples*
```-e 12``` or ```--badedges 12```

*example result:* B2 L2 D U2 L2 D2 U' B2 D B U' R' U L2 F2 L2 R B' U2

![image](http://cube.crider.co.uk/visualcube.php?fmt=svg&alg=D'F2DR2UF2U2B2UB2F'L'R2U2B2LDB2U2B'F')
