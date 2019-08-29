import argparse
import os.path
import re

# define functions
########################################################
def fixed_width_cols( rows, pad_len=2, delimiter="\t" ):
    """given an input array of strings, create a fixed-width column string"""

    # get number of columns
    cols = rows[0].split(delimiter)
    num_cols = len(cols)

    # get max column width for each column
    max_col_width = [0] * num_cols # init with all zeroes
    for i in range(len(rows)):
        cols = rows[i].split(delimiter)
        for j in range(num_cols):
            if len(cols[j]) > max_col_width[j]:
                   max_col_width[j] = len(cols[j])

    # create fixed-width string by right padding with spaces
    fw = ""
    for i in range(len(rows)):
        cols = rows[i].split(delimiter)
        for j in range(num_cols):
            fw += right_pad(cols[j], max_col_width[j] + pad_len)
        fw += "\n"

    return fw

########################################################

def right_pad( str, width ):
    """right pad the given string with spaces to the given length"""

    while(len(str)<width):
        str += ' '

    return str

########################################################

# parse input arguments
parser = argparse.ArgumentParser(description="List sequence names with count of regions, min & max coords, total number of regions, and total sum of regions (does not correct for overlap)")
parser.add_argument('-b', '--bed', required=True, help="input BED file", metavar="str")
parser.add_argument('-l', '--log', help="name of log file, which is output only if specified, default name is '%(default)s'", nargs='?', default="log.txt", metavar="str")
args = parser.parse_args()

# read and process input BED file
# open BED file, first checking that it exists
if not os.path.isfile(args.bed):
    print("File '{0}' does not exist.".format(args.bed))
    exit();
with open(args.bed, "r") as input_bed:
    regions_count = 0 # total count of regions in input file (does not resolve any overlap)
    total_sum = 0 # total nt sum across all regions (does not resolve any overlap)
    info_by_seq_name = {} # dictionary of info by seqname
    seq_names_by_input_order = [] # list of seqnames kept in input order
    re_hash = re.compile(r'^#')
    re_track = re.compile(r'^track')
    for line in input_bed:
        line = line.strip()

        # TO DO skip if line is blank or starts with '#' or start with 'track'
        if len(line) == 0: # skip blank lines
            continue
        if re.search(re_hash, line):
            continue
        if re.search(re_track, line):
            continue

        # split into component values
        seq_name = ""
        start = 0
        end = 0
        etc = []
        try:
            seq_name, start, end, *etc = line.split("\t")
        except ValueError:
            print("Error on following input line:\n'{0}'".format(line))
            next
        start = int(start)
        end = int(end)

        # swap if start and stop if backward
        if start > end:
            tmp = end
            end = start
            start = tmp
        
        # count total num of regions
        regions_count += 1

        # total sum of regions (does not correct for overlap)
        total_sum += (end - start)

        # build list of sequence names with count of regions, min, and max coords
        if seq_name not in info_by_seq_name:
            seq_names_by_input_order.append(seq_name) # add this seqname to the end of the list (preserve input order)
            info_by_seq_name[seq_name] = [1,start,end,end-start] # region_cnt, min_coord, max_coord, nt_sum
        else:
            [region_cnt, min_coord, max_coord, nt_sum] = info_by_seq_name[seq_name]
            region_cnt += 1
            if start < min_coord:
                min_coord = start
            if end > max_coord:
                max_coord = end
            nt_sum += (end - start)
            info_by_seq_name[seq_name] = [region_cnt, min_coord, max_coord, nt_sum] # update stored data

# output stats by region
rows = ["seq\tnum_regions\tmin_coord\tmax_coord\tmax_min_diff\tnt_sum"] # output header
for seq_name_src_feat in seq_names_by_input_order:
    (region_cnt, min_coord, max_coord, nt_sum) = info_by_seq_name[seq_name_src_feat]
    rows.append("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(seq_name_src_feat,region_cnt, min_coord, max_coord, (max_coord-min_coord), nt_sum))
print(fixed_width_cols(rows))

# output summary stats
print("Total number of regions: {0}".format(regions_count))
print("Total number of unique sequence names (chromosomes): {0}".format(len(seq_names_by_input_order)))
print("Total nucleotide sum: {0}".format(total_sum))
