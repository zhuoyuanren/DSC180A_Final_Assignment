import sys
import json
import shutil
import argparse


sys.path.insert(0, 'src') # add library code to path
from etl import filter_recode
from etl import pca
from etl import remove_outlier
from etl import after_removal
from etl import get_data



#DATA_PARAMS = 'config/data-params.json'
#TEST_PARAMS = 'config/test-params.json'
conf = json.load(open('config/test-params.json'))  

parser = argparse.ArgumentParser(description='choose a process to run')

parser.add_argument('process', type = str, nargs = 1, help = "choose process to run")

args = parser.parse_args()
if args.process[0] == "filter":
    filter_recode(input_file=conf['input_file'], output_dir = conf['temp_path'], output_filename = conf['name'], maf = conf['maf'], geno = conf['geno'], mind = conf['mind'])
elif args.process[0] == "initial_pca":
    pca(filename = conf['temp_path'] + '/' + conf['name']) #'data/interim/chr22' 
elif args.process[0] == "remove_outlier_then_pca":
    remove_outlier(input = 'data/interim/chr22.eigenvec', graph_output1 = 'data/before_remove_outliers1.png', 
                   graph_output2 = 'data/before_remove_outliers2.png',
                   remove_output = 'data/outliers.txt',filename = conf['temp_path'] + '/' + conf['name'])
elif args.process[0] == "graph_after_remove_outlier":
    after_removal(input = 'data/interim/chr22.eigenvec',
                  graph_output1 = 'data/after_remove_outliers1.png',
                 graph_output2 = 'data/after_remove_outliers2.png')
elif args.process[0] == "test-project":
    filter_recode(input_file=conf['input_file'], output_dir = conf['temp_path'], output_filename = conf['name'], maf = conf['maf'], geno = conf['geno'], mind = conf['mind'])
    pca(filename = conf['temp_path'] + '/' + conf['name']) #'data/interim/chr22' 
    remove_outlier(input = 'data/interim/chr22.eigenvec', graph_output1 = 'data/before_remove_outliers1.png', 
                   graph_output2 = 'data/before_remove_outliers2.png',
                   remove_output = 'data/outliers.txt',filename = conf['temp_path'] + '/' + conf['name'])
    after_removal(input = 'data/interim/chr22.eigenvec',
                  graph_output1 = 'data/after_remove_outliers1.png',
                 graph_output2 = 'data/after_remove_outliers2.png')
elif args.process[0] == 'get_data':
    conf = json.load(open(DATA_PARAMS))  
    get_data(conf['person'],conf['files'],conf['config'])
    
