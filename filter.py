import pandas as pd 
import os
import shutil
import shlex
import sys
import subprocess as sp
import numpy as np
import argparse
import matplotlib.pyplot as plt

filename_p1 = '/datasets/dsc180a-wi20-public/Genome/vcf/ALL.chr'
filename_p2 = '.shapeit2_integrated_v1a.GRCh38.20181129.phased.vcf.gz'

cmd = shlex.split('mkdir filtered')
sp.call(cmd)
for i in range(23):
    print(i)
    cmd = shlex.split('plink2 --vcf ' + filename_p1 + str(i) + filename_p2 + '  --make-bed  --snps-only  --maf 0.05  --geno 0.1  --mind 0.05  --recode vcf  --out filtered/chr' + str(i))
    sp.call(cmd)
