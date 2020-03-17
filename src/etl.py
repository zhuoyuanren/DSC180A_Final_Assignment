import pandas as pd 
import os
import shutil
import shlex
import sys
import subprocess as sp
import numpy as np
import argparse
import matplotlib.pyplot as plt
import json
import seaborn as sns


def get_data(person, files, outpath, **kwargs):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    for i in person:
        for f in files:
            response = urllib.request.urlopen("ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/%s/sequence_read/%s"%(i,f))
            with open(i+f[:f.index('.')]+'.fastq', 'wb') as output:
                output.write(response.read())

def filter_recode(input_file, output_dir,output_filename, maf, geno, mind ):
    if not os.path.exists(output_dir):
        cmd = shlex.split("mkdir -p "+output_dir)
        sp.call(cmd)
    cmd = shlex.split('plink2 --vcf ' + input_file + '  --make-bed  --snps-only  --maf ' + str(maf) + '  --geno ' + str(geno) + ' --mind ' + str(mind) + ' --recode vcf  --out ' + output_dir + '/' + output_filename)
    sp.call(cmd)

def pca(filename = 'data/interim/chr22'):
    cmd = shlex.split('plink2 --bfile ' + filename + '  --pca  --out ' + filename)
    sp.call(cmd)

def remove_outlier(input = 'data/interim/chr22.eigenvec', graph_output1 = 'data/before_remove_outliers1.png', 
                   graph_output2 = 'data/before_remove_outliers2.png',
                   remove_output = 'data/outliers.txt',filename = 'data/interim/chr22'):
    temp = pd.read_table(input,header=None,sep=' ')
    country = pd.read_csv('sample_info.csv')
    temp = temp.merge(country, left_on = 0, right_on = 'Sample')
    plt.figure(figsize=(8, 6))
    ax = sns.scatterplot(x=2, y=3, hue='Population', data=temp)
    ax.set(xlabel='PC1', ylabel='PC2')
    ax.set(title = 'PC1 vs PC2 With Outlier')
    ax.figure.savefig(graph_output1)
    
    ax = sns.scatterplot(x=3, y=4, hue='Population', data=temp)
    ax.set(xlabel='PC2', ylabel='PC3')
    ax.set(title = 'PC2 vs PC3 With Outlier')
    ax.figure.savefig(graph_output2)
    
    std = temp.std()[2]
    temp['outlier'] = (temp[np.arange(2,12)].abs() < 2*std).apply(lambda x: 0 if sum(x) == 10 else 1, axis=1)
    outlier = temp[temp['outlier'] == 1]
    ols = outlier[[0,1]].values.tolist()
    with open(remove_output, 'w') as x:
        for sub_list in ols:
            for item in sub_list:    
                x.write(item + ' ')
            x.write("\n")
    cmd = shlex.split('plink2 --bfile '+filename+' --pca  --remove '+ remove_output +'  --out '+filename)
    sp.call(cmd)

def after_removal(input = 'data/interim/chr22.eigenvec',
                  graph_output1 = 'data/after_remove_outliers1.png',
                 graph_output2 = 'data/after_remove_outliers2.png'):
    temp = pd.read_table(input,header=None,sep=' ')
    country = pd.read_csv('sample_info.csv')
    temp = temp.merge(country, left_on = 0, right_on = 'Sample')
    plt.figure(figsize=(8, 6))
    ax = sns.scatterplot(x=2, y=3, hue='Population', data=temp)
    ax.set(xlabel='PC1', ylabel='PC2')
    ax.set(title = 'PC1 vs PC2 Without Outlier')
    ax.figure.savefig(graph_output1)
    
    ax = sns.scatterplot(x=3, y=4, hue='Population', data=temp)
    ax.set(xlabel='PC2', ylabel='PC3')
    ax.set(title = 'PC2 vs PC3 Without Outlier')
    ax.figure.savefig(graph_output2)
   