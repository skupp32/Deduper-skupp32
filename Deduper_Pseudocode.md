## Problem Definition:
During PCR, sequences can be over or underrepresented based on duplication.  The goal of this code is to remove PCR duplicates to correct for this.  Using UMIs, the bit-flag, position, RNAME, and cigar string from a Sequence Alignment Map (SAM) we can determine the UMI, the chromosome, the strand, and adjust the position as necessary to remove all PCR Duplicates.


Input: SAM File, List of UMIs in text file
Output: Sequence Alignment File

##Pseudo Code
Accept command line options for input file, output file, umi file, and help message


Create data structure to store UMI and associated soft clipped adjusted position, chromosome, reverse complemented flag.

Read in UMI file and save the UMIs in a data structure

Loop over SAM file line by line
If the line starts with "@" write it to the designated output file

Use functions to extract UMI, Strand, Starting Position, and Chromosome

Check if UMI is in the data structure

if it is in the structure and the position, chromosome, and strand are also the same:
    move on to the next line in the SAM File

if the UMI is not in the dictionary:
    write the line to the output file


### Functions:

def find_umi(list: SAM File Line, list: UMIs from file) -> str:

    Input:  SAM File Line separated by tabs and a list of UMIs from the given file
    Output: The UMI string or None

    Pass in a line from a sam file separated into a list by tabs.

    Use regular expressions to extract the UMI from the QNAME.

    Check if UMI is in the list of UMIs from the given UMI File.

    If it is in the list:
        and the umi is in the sequence:
            return the UMI
    Else:
        return None

    Example:
    Input: 
    ['NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAA','16','2','8','36','2S1M1I1M','*','0','0','AAAAA','EEEEE']

    Output:
    if GAACAGGT in list of UMIs, returns 'AAA'
    else: return None

    Input:
    ['NS500451:154:HWKTMBGXX:1:11101:15364:1139:TTT','16','2','8','36','2S1M1I1M','*','0','0','AAAAA','EEEEE']

    Output:
    return None ('TTT' not in sequence)

def adj_position(list: SAM File Line,bool: Reverse Complement) -> int,int:

    Input: SAM File Line separated by tabs and a bool giving the strand (true = minus strand)
    Output: The position of the read after adjustments, the chromosome of the read

    Pass in a line from a sam file separated into a list by tabs.
    Find the position from POS
    Find the number of soft clipped bases using regular expressions to find the number before 's' in the Cigar String.
    Find the chromosome number from RNAME

    if on minus strand (reverse complement = True):
        find number of insertions and deletions using regular expressions on cigar string
        subtract #insertions from starting positon
        add #deletions to starting position

    return the position minus the number of soft clipped bases, return chromosome number

    Example:

    Input:
    ['NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAA','16','2','8','36','2S1M1I1M','*','0','0','AAAAA','EEEEE'], True

    Output:
    Position: 5 (8-2-1), Chromosome: 2

    Input:
    ['NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAA','0','2','8','36','2S1M1I1M','*','0','0','AAAAA','EEEEE'], False

    Output:
    Position: 6 (8-2), Chromosome: 2

def find_strand(list: SAM File Line) -> bool:

    Input: SAM File Line separated by tabs
    Output: Bool specifying the strand (true = minus strand, false = plus strand)

    Pass in a line from a sam file separated into a list by tabs.
    Extract the bitwise flag.
    Check if reverse complemented flag is true

    if true:
        rev_comp = True
    else:
        rev_comp = False
    
    return rev_comp

    Example:

    Input:
    ['NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAA','16','2','8','36','2S1M1I1M','*','0','0','AAAAA','EEEEE']

    Bit Flag = 16

    Output:
    return True

    Input:
    ['NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAA','0','2','8','36','2S1M1I1M','*','0','0','AAAAA','EEEEE']

    Bit Flag = 0

    Output:
    return False

