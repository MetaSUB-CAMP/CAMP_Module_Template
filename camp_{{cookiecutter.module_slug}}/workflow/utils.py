'''Utilities.'''


# --- Workflow setup --- #


import gzip
import os
from os import makedirs, symlink
from os.path import abspath, exists, join
import pandas as pd
import shutil


def extract_from_gzip(p, out):
    ap = abspath(p)
    if open(ap, 'rb').read(2) == b'\x1f\x8b': # If the input is gzipped
        with gzip.open(ap, 'rb') as f_in, open(out, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    else: # Otherwise, symlink
        symlink(ap, out)


def ingest_samples(samples, tmp):
    df = pd.read_csv(samples, header = 0, index_col = 0) # name, ctgs, fwd, rev
    s = list(df.index)
    lst = df.values.tolist()
    for f in os.listdir(tmp):
        os.remove(join(tmp, f))
    for i,l in enumerate(lst):
        # Symlink your original data to the temporary directory
        # Example: symlink(abspath(l[0]), join(tmp, s[i] + '.fasta'))
        # Example: extract_from_gzip(abspath(l[1]), join(tmp, s[i] + '_1.fastq'))
        # Example: extract_from_gzip(abspath(l[2]), join(tmp, s[i] + '_2.fastq'))
    return s


class Workflow_Dirs:
    '''Management of the working directory tree.'''
    OUT = ''
    TMP = ''
    LOG = ''

    def __init__(self, work_dir, module):
        self.OUT = join(work_dir, '{{ cookiecutter.module_slug }}')
        self.TMP = join(work_dir, 'tmp') 
        self.LOG = join(work_dir, 'logs') 
        if not exists(self.OUT):
            makedirs(self.OUT)
            # Add custom subdirectories to organize intermediate files
            makedirs(join(self.OUT, 'final_reports'))
        if not exists(self.TMP):
            makedirs(self.TMP)
        if not exists(self.LOG):
            # Add custom subdirectories to organize rule logs
            makedirs(self.LOG)


# --- Workflow functions --- #


