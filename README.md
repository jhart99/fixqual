# fixquals
## a utility to fix out of spec base qualities in a fastq

This small utility clips base quality scores that exceed specs down to
reasonable numbers.  I found that one batch of fastq files I had were causing
RSEM to choke and I wrote this to fix the bugged quality scores.

Runs in a very small amount of memory < 10 MB.  Uses 1 core fully.  In my
experience it runs at about 1 million reads in 40 sec.  Probably could get it
faster, but it seems sufficient.
