import glob
import pandas as pd 
import os
import shutil
import shlex
import sys
import subprocess as sp
import numpy as np
import argparse

vcfs = glob.glob("chr*.vcf")
cmd = shlex.split('bcftools concat --output results.vcf ' + ' '.join(vcfs))
sp.call(cmd)
