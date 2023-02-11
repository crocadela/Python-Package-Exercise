from src.data_analysis import *
import unittest
import pandas as pd
import numpy as np


class TestDataAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Loading dataset")
        cls._df = pd.read_csv('test_files/sample_data/test_data.csv')
        
    def test_filter_by_conf(self):
        print("Starting test_filter_by_conf")
        conf = 0.5
        filtered_df = filter_by_conf(self._df, conf)
        self.assertTrue(filtered_df['conf'].min() > conf)

    def test_count_objects(self):
        print("Starting test_count_objects")
        objects_freq = count_objects(self._df)
        self.assertEqual(objects_freq.shape[0], 7)
        self.assertEqual(set(objects_freq.columns), {'object_id', 'object', 'counts'})
        self.assertEqual(objects_freq['counts'].dtype, 'int')
        self.assertEqual(objects_freq[objects_freq['object'] == 'car']['counts'].sum(), 23)

    def test_count_bad(self):
        print("Starting test_count_bad")
        objects_freq = count_objects(self._df)
        self.assertNotEqual(objects_freq['counts'].dtype, 'float')


class TestPopularObjects(unittest.TestCase):
    def setUp(self):
        print("Preparing dataset")
        files = ['A'] * 17 + ['B'] * 16 + ['C'] * 13 + ['D'] * 11 + ['E'] * 8
        obj_a = np.array(['gatos'] * 4 + ['perros'] * 4 + ['patos'] * 4 + ['ratas'] * 4 + ['paloma'] * 1)
        obj_b = np.array(['gatos'] * 5 + ['perros'] * 4 + ['patos'] * 4 + ['ratas'] * 2 + ['paloma'] * 1)
        obj_c = np.array(['gatos'] * 4 + ['perros'] * 4 + ['patos'] * 2 + ['ratas'] * 2 + ['paloma'] * 1)
        obj_d = np.array(['gatos'] * 4 + ['perros'] * 2 + ['patos'] * 2 + ['ratas'] * 2 + ['paloma'] * 1)
        obj_e = np.array(['gatos'] * 4 + ['perros'] * 2 + ['patos'] * 2)

        objects = np.concatenate([obj_a, obj_b, obj_c, obj_d, obj_e])
        # Create a DataFrame with a single column 'object'
        data = pd.DataFrame({'file_name': files, 'object': objects})
        self.df = data

    def test_vars(self):
        print("Starting test_vars")
        c_ob = self.df.groupby(['file_name', 'object']).size().reset_index(name='counts')
        counted_objects = c_ob.sort_values(by=['file_name', 'counts'], ascending=[True, False]).reset_index(drop=True)
        # Check if c_ob has the expected number of rows and columns and values
        # Expected rows
        self.assertEqual(c_ob.shape[0], 23)
        # Expected columns
        self.assertEqual(c_ob.shape[1], 3)
        self.assertEqual(counted_objects.iloc[0]['object'], 'gatos')

        # What we expect:
        # 4 gatos, 4 perros, 4 patos, 4 ratas, 1 paloma -> most popular objects: gato, perro, pato, rata
        # 5 gatos, 4 perros, 4 patos, 2 ratas, 1 paloma -> most popular objects: gato, perro, pato
        # 4 gatos, 4 perros, 2 patos, 2 ratas, 1 paloma -> most popular objects: gato, perro
        # 4 gatos, 2 perros, 2 patos, 2 ratas, 1 paloma -> most popular objects: gato
        # 4 gatos, 4 perros, 2 patos                    -> most popular objects: gato, perro, pato

        expected = {'gatos': 5, 'perros': 4, 'patos': 3, 'ratas': 1}
        self.assertEqual(popular_objects(self.df), expected)


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestDataAnalysis))
suite.addTest(unittest.makeSuite(TestPopularObjects))
unittest.TextTestRunner(verbosity=2).run(suite)
