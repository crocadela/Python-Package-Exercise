from src.clean_dataset import *
import unittest


class TestCheckYolo(unittest.TestCase):
    def test_correct_columns(self):
        print("Starting test_correct_columns")
        file_path = 'test_files/docs/good_txt/correct_columns.txt'
        with open(file_path, 'w') as f:
            f.write('1 0.5 0.5 0.5 0.5 0.5\n')
        self.assertTrue(check_yolo(file_path))

    def test_less_columns(self):
        print("Starting test_less_columns")
        file_path = 'test_files/docs/bad_txt/less_columns.txt'
        with open(file_path, 'w') as f:
            f.write('1 0.5 0.5 0.5 0.5 0.5\n')
            f.write('1 0.5 0.5 0.5\n')
        self.assertFalse(check_yolo(file_path))

    def test_more_columns(self):
        print("Starting test_more_columns")
        file_path = 'test_files/docs/bad_txt/more_columns.txt'
        with open(file_path, 'w') as f:
            f.write('1 0.5 0.5 0.5 0.5 0.5\n')
            f.write('1 0.5 0.5 0.5 0.5 0.5 0.5\n')
        self.assertFalse(check_yolo(file_path))

    def test_bad_int(self):
        print("Starting test_bad_int")
        file_path = 'test_files/docs/bad_txt/bad_int.txt'
        with open(file_path, 'w') as f:
            f.write('0.4 0.5 0.5 0.5 0.5 0.5\n')
            f.write('1 0.5 0.5 0.5 0.5 0.5 0.5\n')
        self.assertFalse(check_yolo(file_path))

    def test_bad_float(self):
        print("Starting test_bad_float")
        file_path = 'test_files/docs/bad_txt/bad_float.txt'
        with open(file_path, 'w') as f:
            f.write('1 0.5 0.5 0.5 0.5 0.5\n')
            f.write('1 0.5 0.5 0.5 f 0.5\n')
        self.assertFalse(check_yolo(file_path))

    def test_range(self):
        print("Starting test_range")
        file_path = 'test_files/docs/good_txt/int_range.txt'
        with open(file_path, 'w') as f:
            f.write('79 0 0.5 0.5 0.5 0.5\n')
            f.write('0 1 0.5 0.5 0.5 0.5\n')
        self.assertTrue(check_yolo(file_path))

    def test_out_range(self):
        print("Starting test_out_range")
        file_path = 'test_files/docs/bad_txt/int_out_range.txt'
        with open(file_path, 'w') as f:
            f.write('80 1.01 0.5 0.5 0.5 0.5\n')
            f.write('0 -0.01 0.5 0.5 0.5 0.5\n')
        self.assertFalse(check_yolo(file_path))


class TestNoYoloList(unittest.TestCase):
    def test_yolo_no_invalid(self):
        print("Starting test_yolo_no_invalid")
        txt_path = 'test_files/docs/good_txt/'
        expected = []
        self.assertEqual(non_yolo_list(txt_path), expected)

    def test_yolo_invalid(self):
        print("Starting test_yolo_invalid")
        txt_path = 'test_files/docs/bad_txt/'
        expected = ['less_columns',
                    'more_columns',
                    'bad_int',
                    'bad_float',
                    'int_out_range']
        self.assertEqual(set(non_yolo_list(txt_path)), set(expected))


class TestBadImg(unittest.TestCase):
    def test_bad_img(self):
        print("Starting test_good_img")
        img_folder = 'test_files/sample_data/images/'
        text_folder = 'test_files/sample_data/labels/'
        bad_images = bad_img(img_folder, text_folder)
        expected = {'berlin_000000_000010_leftImg8bit_20-10-2018_wrong_size.png',
                    'right_parameters.png',
                    'zurich_000101_000019_leftImg8bit_02-05-2019.png',
                    'zurich_000113_000019_leftImg8bit_16-02-2019.png',
                    'bonn_000015_000019_leftImg8bit_14-03-2016.jpg'}

        self.assertEqual(bad_images, expected)


class TestIsInCity(unittest.TestCase):

    def test_right_image(self):
        print("Starting test_right_image")
        img_path = 'test_files/sample_data/images/'
        txt_path = 'test_files/sample_data/labels/'
        image = 'berlin_000000_000019_leftImg8bit_20-10-2018'
        self.assertTrue(is_in_city(image, img_path, txt_path))

    def test_no_label(self):
        print("Starting test_no_label")
        img_path = 'test_files/sample_data/images/'
        txt_path = 'test_files/sample_data/labels/'
        image = 'right_parameters'
        self.assertFalse(is_in_city(image, img_path, txt_path))

    def test_wrong_extension(self):
        print("Starting test_wrong_extension")
        img_path = 'test_files/sample_data/images/'
        txt_path = 'test_files/sample_data/labels/'
        image = 'bonn_000015_000019_leftImg8bit_14-03-2016'
        self.assertFalse(is_in_city(image, img_path, txt_path))

    def test_bad_size(self):
        print("Starting test_bad_size")
        img_path = 'test_files/sample_data/images/'
        txt_path = 'test_files/sample_data/labels/'
        image = 'zurich_000101_000019_leftImg8bit_02-05-2019'
        self.assertFalse(is_in_city(image, img_path, txt_path))


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestCheckYolo))
suite.addTest(unittest.makeSuite(TestNoYoloList))
suite.addTest(unittest.makeSuite(TestBadImg))
suite.addTest(unittest.makeSuite(TestIsInCity))
unittest.TextTestRunner(verbosity=2).run(suite)
