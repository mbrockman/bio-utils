# bio-utils
Repository for general bioinformatics utility scripts

### length:
- return the character length of the input string
- written in Perl
- usage statement: length -h or length
- basic usage: length <string>

### mlength:
- return the character length of multiple input strings
- written in Perl
- usage statement: mlength -h or mlength
- basic usage: mlength <filename|->
- accepts streamed input on the commandline with '-' as input: mlength -

### bed_stats.py
- return BED file region summary stats
- written in Python3
- usage statement: python bed_stats.py or python bed_stats.py -h
- basic usage: python bed_stats.py -b <input BED file>
