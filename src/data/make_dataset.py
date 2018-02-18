# -*- coding: utf-8 -*-
import os
#import click
#import logging
#from dotenv import find_dotenv, load_dotenv
import numpy as np
import pandas as pd
import sklearn.preprocessing


def create_dummies(df,column):
    ndf = pd.get_dummies(df[column], prefix= column, dummy_na=True)
    df = df.drop(column, axis=1)
    df = df.join(ndf)
    return df

# @click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
def main(input_filepath=0, output_filepath=0):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    # logger = logging.getLogger(__name__)
    # logger.info('making final data set from raw data')
        
    train = load_df('train.csv')
    test = load_df('test.csv')
    train_test = pd.concat([train, test], axis=0)
    train_test.reset_index(drop=True, inplace=True)
    print(train.shape)
    print(test.shape)
    print(train_test.shape)
    train_test = create_dummies(train_test, 'MSSubClass')
    for column in train_test.select_dtypes(exclude = [np.number]).columns:
        train_test = create_dummies(train_test, column)
    train_test['2ndFlrSF'].fillna(0, inplace=True)
    imp = sklearn.preprocessing.Imputer()
    imp.fit_transform(train_test)
    # imputer tem que ser diferente no caso da área do segundo andar

    train = train_test.iloc[:train.index[-1]]
    test = train_test.iloc[train.index[-1]:]

    save_df(train, 'train.hdf5')
    save_df(test, 'test.hdf5')

def load_df(filename):
    """
    Loads train_df
    :return: Train DataFrame
    :rtype: pandas DataFrame
    """
    final_path = os.path.join(get_data_path(), 'raw/' + filename)
    return pd.read_csv(final_path)



def save_df(df, filename):
    """
    Saves DataFrame in hdf5 with name 'train.hdf5'

    :param df: DataFrame to be Saved
    """
    final_path = os.path.join(get_data_path(), 'processed')
    if not os.path.exists(final_path):
        os.mkdir(final_path)

    final_path = os.path.join(final_path, filename)

    df.to_hdf(final_path, 'processed_data')

def get_data_path():
    # Get current absolute path
    absolute_path = os.path.abspath(__file__)

    # Get parent path
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(absolute_path)))

    # Get final path (absolute path for '../../data/raw/'
    final_path = os.path.join(project_root, 'data/')

    return final_path

if __name__ == '__main__':
    # log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    # project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())

    main()

