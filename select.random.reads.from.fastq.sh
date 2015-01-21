#!/bin/bash


# Created on: Jan 21, 2015
# Usage: ./select.random.reads.from.fastq.sh
# Author: Javier Quilez (GitHub: jaquol)
# Goal: Loop over a directory with multiple FASTQ files and subset a random number of reads (sequence only) from each file

OUTDIR=/whre/to/output/sequences
mkdir $OUTDIR
outfile=$OUTDIR/random.reads.txt
rm $outfile
TRIMMED_READS=/my/directory/with/FASTQ/files
samples="sample1 sample2 sample3"
downsample=1000
sampled_reads=100

for sample in $samples; do

    # Select file for the sample
    echo $sample
    infile=`ls $TRIMMED_READS/*fastq.gz | grep $sample`

    # Select N random reads. This command sequentially does:
    # 1. Select header lines (starting with '@') plus the next line (the read itself)
    # 2. Get rid of the header and of the '--' added by the grep command to separate consecutive matches
    # 3. To make downstream calculations easier, only retain reads of length 100 nucleotides and add sample name
    # 4. Files are very big (millions of lines) so restrict to first 1,000 reads
    # 5. Random sorting and select the N first reads
    zcat $infile | grep -A 1 "@" | grep -v '@\|--' | awk -v sample=$sample '{if (length($0) == 100) print sample,$1}' | head -${downsample} | sort -R | head -${sampled_reads} >> $outfile

done
