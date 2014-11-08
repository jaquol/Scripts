#!/usr/bin/python

# Created on: Nov 8th 2014
# Usage: python make.windows.n.size.from.intervals.py
# Goal: Merges genomic intervals (BED) format to make windows of a specified size


import sys


# Variable parameters
input_bed, window_size, output_bed  = sys.argv[1:4]
window_size = int(window_size)


outfile = open(output_bed, 'w')


# Variables to store coordinates
current_chrom = ''
start_coords = []
end_coords = []
total_lengths = []


# Read in file 
with open(input_bed) as f:
        
        for line in f:

                # Get genomic coordinates
                chrom, start, end  = line.strip().split('\t')
                start = int(start)
                end = int(end)
                chunk_length = end - start

                # Initialize list: min() is applied to non-empty lists
                if len(start_coords) == 0:
                        start_coords = start_coords + [start]
                
                # Initialize current_chrom:
                if current_chrom == '':
                        current_chrom = chrom
                        print chrom

                # Calculate additional bps to reach the required window size of callable
                offset = window_size - sum(total_lengths)
                #print chrom, min(start_coords), end, offset
                if offset < chunk_length:
                        extra_bit = start + offset
                        line_to_print = [str(i) for i in [chrom, min(start_coords), extra_bit, sum(total_lengths) + extra_bit - start]]
                        outfile.write("\t".join(line_to_print) +  "\n")
                        total_lengths = []
                        start_coords = []
                        print chrom, min(start_coords), extra_bit, sum(total_lengths) + extra_bit - start
                        continue
                
                # New chromosome
                if current_chrom != chrom:
                        print chrom
                        total_lengths = []
                        start_coords = []

                # Update values          
                total_lengths = total_lengths + [chunk_length]
                start_coords = start_coords + [start]
                current_chrom = chrom


f.close()
outfile.close()