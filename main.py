import argparse
from os.path import join
from pandas_plink import read_plink, read_plink1_bin, get_data_folder
from tqdm import tqdm
import matplotlib.pyplot as plt
import pickle

from regression import createPvalue
# from utils.dataset import load_vcf
from utils.postprocess import merge_col, make_genotype_by_bed

def get_args_parser():
    parser = argparse.ArgumentParser('Default Argument', add_help=False)
    # dataset parameters
    parser.add_argument('--path', type=str, default='')
    parser.add_argument('--mode', default='linear')
    parser.add_argument('--file', default='bim')
    parser.add_argument('--nosave', default=False, action='store_true')
    parser.add_argument('--save_dir', default='logs')

    parser.add_argument('--full_dataset', default=False, action='store_true')
    parser.add_argument('--num_col', default=[5000], nargs='+')

    return parser

def make_xy(args, df):
    # pheno
    train_test_df = merge_col(
        df, join(args.path, f'dataset/{args.mode}_pheno.txt'), 'y'
    )
    return train_test_df


def main(args):
    bim, fam, bed = read_plink(join(args.path, 'dataset/data')) #bim, fam, bed
    id = [fam['fid'].tolist(), fam['iid'].tolist()]
    snpid = bim['snp'].tolist()

    print("Fit model: in progress...")
    # start = time.time()

    res = {}
    for num in tqdm(args.num_col):
        genotype_df = make_genotype_by_bed(args, bed.compute(), id, snpid, num)
        train_test_df = make_xy(args, genotype_df)    
    
        createPvalue(args, train_test_df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Arguments', parents=[get_args_parser()])
    args = parser.parse_args()
    main(args)