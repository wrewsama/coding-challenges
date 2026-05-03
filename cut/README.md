# cut
https://codingchallenges.fyi/challenges/challenge-cut

## Usage

* 1st and 2nd field, `,`-delimited, from `testdata/fourchords.csv`
```shell
❯ ./cute -f1,2 -d, testdata/fourchords.csv | head
Song title	Artist
"10000 Reasons (Bless the Lord)"	Matt Redman and Jonas Myrin
"20 Good Reasons"	Thirsty Merc
"Adore You"	Harry Styles
"Africa"	Toto
"Aicha"	Cheb Khaled
"Ai Se Eu Te Pego"	Michel Teló
"All You Wanted"	Michelle Branch
"Almost"	Bowling for Soup
"Alone"	Alan Walker
```
> Yes the extra `e` is intentional because it was _cute_


* provide `-` or no file path to read from stdin
```shell
❯ tail -n5 fourchords.csv | ./cute -d, -f"1 2"
```

