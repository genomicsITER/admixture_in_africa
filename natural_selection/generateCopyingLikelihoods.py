#!/usr/bin/python

############################################################
## THIS SCRIPT TAKES CHROMOPAINTER OUTPUT AND GENERATES  ##
## A MATRIX OF GENOTYPES THAT CAN BE USED IN THE NATURAL ##
## SELECTION PROGRAMS
############################################################
import gzip # for reading/writing gzipped files
from optparse import OptionParser # for command line options
import numpy as np


#file_root = "/mnt/kwiat/well/human/george/chromopainter2/output/FULAInolocalChrom"
#out_root = "/mnt/kwiat/data/bayes/users/george/popgen/analysis3/chromopainter/outputcopyprobs/FULAInolocalAllChroms"
############################################################
# get commandline arguments
usage = "usage: %prog [options] \n\n **This program takes in ChromoPainter *samples.out file root and generates a matrix of genome-wide paintings with n_haps columns and n_snps rows."
parser = OptionParser()
parser = OptionParser(usage=usage, version="%prog 1.0")
parser.add_option("-i", "--infile", dest="infile",
                  help="input file root: should be the bit pre *ChromXX.samples.out file from ChromoPainter", metavar="INFILE")
parser.add_option("-o", "--outfile", dest="outfile", 
                  help="output file (gzipped)", metavar="OUTROOT")
parser.add_option("-s", "--samps", dest="numsamps", default = 10,
                  help="the number of samples generated by ChromoPainter: default is 10", metavar="SAMPS")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")


(options, args) = parser.parse_args()
file_root = options.infile
n_samps = options.numsamps
out_file = options.outfile

file_suff  = "PP.samples.out"
n_samps = 10

   
############################################################
# PROGRAM #


for chrom in range(1,23):
    if chrom < 10:
        chrom = "0" + str(chrom)
    else:
	chrom = str(chrom)

    in_file = file_root + chrom + file_suff
    print(in_file)
############################################################
## FIND NUMBER OF SNPS
    f = open(in_file)
    for i, line in enumerate(f):
	if i == 2:
	    n_snps = len(line.split())-1
    print('chromosome ' + chrom + ' sample file has: ' + str(n_snps) + ' snps...')
############################################################
## FIND NUMBER OF HAPS
    f = open(in_file)
    l = [x for x in f.readlines() if x.startswith('HAP')]
    n_haps = len(l)
    print 'sample file has: ' + str(n_haps) + ' haplotypes...'
############################################################
## NOW READ IN ALL THE SAMPLES AND MAKE A n_haps * 10 by n_snps matrix
    mat = np.zeros(shape=(n_snps,n_haps*n_samps),dtype=object)
    i = 0
    for line in open(in_file):
	l = line.split()
	if l[0].isdigit():
	    mat[:,i] =  l[1:len(l)]
	    i = i + 1

  
## ADD TO MASTER MATRIX
    if chrom == "01":
	with gzip.open(out_file,'wb') as f_handle:
	    np.savetxt(f_handle,mat, fmt='%1s')
    else:
	with gzip.open(out_file,'ab') as f_handle:
	    np.savetxt(f_handle,mat, fmt='%1s')


