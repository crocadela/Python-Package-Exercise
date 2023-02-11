import unittest

import pandas as pd

from src.make_dataset import create_dataset
from src.make_dataset import read_labels
from src.make_dataset import read_codes
from src.make_dataset import to_csv


class TestMakeDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Loading dataset")
        path = 'test_files/sample_data/'
        cls._df = create_dataset(path)

    def test_reading(self):
        print("Starting test_reading")
        path = 'test_files/sample_data/'
        self.assertEqual(len(read_labels(path)), 45)
        self.assertEqual(len(read_codes(path)), 80)

    def test_create_dataset(self):
        print("Starting test_create_dataset")
        self.assertEqual(self._df.shape[0], 45)
        self.assertEqual(self._df.shape[1], 10)
        # Types
        self.assertEqual(self._df['file_name'].dtype, 'O')
        self.assertEqual(self._df['city'].dtype, 'O')
        self.assertEqual(self._df['date'].dtype, 'datetime64[ns]')
        self.assertEqual(self._df['object_id'].dtype, 'int')
        self.assertEqual(self._df['x'].dtype, 'float')
        self.assertEqual(self._df['y'].dtype, 'float')
        self.assertEqual(self._df['w'].dtype, 'float')
        self.assertEqual(self._df['h'].dtype, 'float')
        self.assertEqual(self._df['conf'].dtype, 'float')
        self.assertEqual(self._df['object'].dtype, 'O')

    def test_to_csv(self):
        print("Starting test_to_csv")
        file = 'processed_data_test.csv'
        file2 = 'bad_processed_data_test.csv'
        path = 'test_files/sample_data/'
        invalid_path = 'path/to/invalid/folder/'
        img_folder = 'test_files/sample_data/images/'
        txt_folder = 'test_files/sample_data/labels/'
        result = to_csv(self._df, file, path, img_folder, txt_folder)
        text = "The file '{}' has been saved in '{}'. ¡Thanks for joining us in this PEC!"
        final_csv = pd.read_csv(path+file)
        expected_result = text.format(file, path)
        self.assertEqual(result, expected_result)
        self.assertRaises(Exception, to_csv, self._df, file2, invalid_path, img_folder, txt_folder)
        self.assertEqual(final_csv.shape[0], 8)
        self.assertEqual(final_csv.shape[1], 8)
        self.assertEqual(set(final_csv['year'].unique()), {2015, 2016, 2017, 2018, 2019})


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMakeDataset))
unittest.TextTestRunner(verbosity=2).run(suite)
