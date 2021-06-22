import os

RELATIVE_PATH = os.path.dirname(__file__) + '/'
data_path = RELATIVE_PATH + 'data/'
sample_data_dir = os.path.join(os.path.abspath(RELATIVE_PATH), 'data/sample_data')
generate_data_dir = os.path.join(os.path.abspath(RELATIVE_PATH), 'data/generate_data')