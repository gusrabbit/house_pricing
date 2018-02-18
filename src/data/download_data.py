import os
from six.moves import urllib

HOUSING_ROOT = "https://raw.githubusercontent.com/joaoavf/misc/master/housing_raw_data/"
TRAIN = 'train.csv'
TEST = 'test.csv'
DESCRIPTION = 'data_description.txt'
SUBMISSION = 'sample_submission.csv'
FILES = [TRAIN, TEST, DESCRIPTION, SUBMISSION]



def fetch_raw_data(root_url, filename, path='data/raw/'):
    """
    Fetches raw daw from server and save to disk.

    :param root_url: URL from which the File will be download
    :param filename: File Name (Both in Server and Local)
    :param path: Local path to save file, cookie cutter standard is 'data/raw' for this case
    """

    # Check if path dir exists and if not creates new dir
    if not os.path.isdir(path):
        os.makedirs(path)

    # Create URL and file_path
    url = root_url + filename
    file_path = path + filename

    # Download file from 'url' and save to disk on 'file_path'
    urllib.request.urlretrieve(url, file_path)

    # Message that download was completed successfully
    print(filename, 'download completed successfully...')


def fetch_data_kaggle_titanic(HOUSING_ROOT, list_of_files, path='data/raw/'):
    """
    Downloads all relevant raw data from Titanic dataset from Kaggle.

    :param path: Local path to save file, cookie cutter standard is 'data/raw' for this case
    """
    # Started downloading message
    print('dataset download started...')

    # Downloads file by file
    [fetch_raw_data(HOUSING_ROOT, file, path) for file in list_of_files]

if __name__ == '__main__':
    # Get current absolute path
    absolute_path = os.path.abspath(__file__)

    # Get parent path
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(absolute_path)))

    # Get final path (absolute path for '../../data/raw/'
    final_path = os.path.join(project_root, 'data/raw/')

    # Fetch Titanic Data
    fetch_data_kaggle_titanic(HOUSING_ROOT, FILES, final_path)
