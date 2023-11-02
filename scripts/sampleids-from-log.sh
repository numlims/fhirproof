# extract certain sampleids the from log, for example all samples failing BehealterCheck check.
# grep flags:
# -P perl mode (for regex)
# -o output
# ?<= positive look-behind. ?<! would negative look-behind, ?= and ?! positive and negative look-ahead

cat tmp.log | grep "BehealterCheck" | grep -P '(?<=sample )\d+' -o 
