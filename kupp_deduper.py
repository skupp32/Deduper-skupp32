import re
import argparse



def get_args():
    parser = argparse.ArgumentParser(description="A program to remove PCR Duplicates from a Sam File by storing and comparing UMI, Strand, Starting Position, and Chromosome/Scaffold.")
    parser.add_argument("-i","--input_sam",help = "The file path to a sorted .sam file",required=True)
    parser.add_argument("-o","--output_sam", help = "The file directory of the output, deduplicated .sam file", required = True)
    parser.add_argument("-u","--umi_file", help = "The file path to a text file containing the list of UMIs used.", required = True)
    return parser.parse_args()

args = get_args()
umi_file = args.umi_file
input_sam = args.input_sam
out_sam = args.output_sam


umi_list = set() #Actually a set

#Opens file with list of umis and adds them to a set
with open(umi_file,'r') as umi_file:
    for line in umi_file:
        umi = line.strip()
        umi_list.add(line.strip())

def find_umi(QNAME: str, umi_list: set)-> str:
    '''
    Given the the QNAME and a set containing all used UMIs, find the umi in the
    QNAME and check that it is in given list of umis. If in the list return the umi, otherwise return 
    "None".
    '''
    umi = QNAME.split(":")[-1]
    if umi in umi_list:
        return umi
    else:
        return "None"

def pos_adjust(pos: int,cigar_string: str, strand: str)-> int:

    '''
    Given the position and cigar string from a sam file and the strand from the bit flag, return adjusted position.
    The strand will be given as "+" or "-".
    '''

    num_s = 0
    num_d = 0
    num_m = 0
    num_n = 0

    #Plus Strand
    if strand == "+":
        "pos - #(1st)S"
        
        #Find all S
        s_list = re.findall(r"[0-9]+(?=S)",cigar_string)
        
        #If 2 S
        if len(s_list) == 2:
            num_s = int(s_list[0]) #grab the first

        #If 1 S
        elif len(s_list) == 1:
            if cigar_string[-1] != "S":
                num_s = int(s_list[0])
        

        pos = pos - num_s


    #Minus Strand
    elif strand == '-':
        "pos + #M + #D + #N +#(last)S"

        #Find all of the M's, D's, N's
        m_list = re.findall(r"[0-9]+(?=M)",cigar_string)
        for exp in m_list:
            num_m += int(exp)

        d_list = re.findall(r"[0-9]+(?=D)",cigar_string)
        for exp in d_list:
            num_d += int(exp)

        n_list = re.findall(r"[0-9]+(?=N)", cigar_string)
        for exp in n_list:
            num_n += int(exp)

        #If the last character is S
        if cigar_string[-1] == "S":
            num_s = int(re.findall(r"[0-9]+(?=S)", cigar_string)[-1])
        else:
            num_s = 0


        pos = pos + num_m + num_n + num_d + num_s

    return pos

def find_strand(bitflag: str)-> str:

    '''
    Given the bitflag from a sam file line find which strand the read is on with the 16 bit.  If (flag & 16) == 16
    return '-', otherwise return '+'.
    '''
    flag = int(bitflag)

    if (flag & 16) == 16:
        return '-'
    else:
        return '+'


#Initialize dictionary for reads where the key is the umi and the value is a set of sets where each set contains
# {starting position, strand, and chrom}
read_list = {}
# dictionary where the key is the chromosome/scaffold and the value is number of unique reads
chrom_list = {} 
num_dups = 0
num_no_umi = 0


#Open both files
with open(out_sam,'w') as out:
    with open(input_sam,'r') as in_sam:
        for line in in_sam:
            #Writes the header lines to the new file
            if line[0] == '@':
                out.write(line)
            
            else:
                line = line.strip()
                cols = line.split()


                #Grab necessary columns from SAM
                QNAME = cols[0]
                bit_flag = cols[1]
                chrom = cols[2]
                lmm_pos = int(cols[3]) #leftmost mapping position
                cigar_string = cols[5]

                if chrom not in chrom_list:
                    chrom_list[chrom] = 0
                    #read_list = {} ## Can uncomment if using a SAM file sorted by chromosome

                umi = find_umi(QNAME,umi_list)
                
                if umi == "None":
                    num_no_umi += 1
                    continue

                strand = find_strand(bit_flag)
                adj_pos = pos_adjust(lmm_pos,cigar_string,strand)


                line_info = (strand,adj_pos,chrom)
                if umi not in read_list:
                    read_list[umi] = set()

                #Check if everything is unique
                if line_info not in read_list[umi]:
                    read_list[umi].add(line_info)
                    out.write(line + "\n")
                    chrom_list[chrom] += 1
                else:
                    num_dups += 1

                    


print(f'There are {num_dups} duplicates')
print(f'There are {num_no_umi} umis not in the given list')
print(f'Chromosomes/Scaffold and number of unique reads:\n{chrom_list}')