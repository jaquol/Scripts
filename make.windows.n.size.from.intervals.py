#!/usr/bin/python

# Created on: Nov 8th 2014
# Usage: python make.windows.n.size.from.intervals.py
# Goal: Merges genomic intervals (BED) format to make windows of a specified size


# Variable parameters
window_size = 1e6	# e.g. for 1 Mbps


# Paths
input_bed = 'test.bed'


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

		# Calculate additional bps to reach the required window size of callable
		offset = window_size - sum(total_lengths)
		#print chrom, min(start_coords), end, offset
		if offset < chunk_length:
			extra_bit = start + offset
			print chrom, '\t', min(start_coords), '\t', extra_bit, '\t', sum(total_lengths) + extra_bit - start
			total_lengths = []
			start_coords = []
			continue
		
		# New chromosome
		if current_chrom != chrom:
			total_lengths = []
			start_coords = []

		# Update values		 
		total_lengths = total_lengths + [chunk_length]
		start_coords = start_coords + [start]
		current_chrom = chrom
