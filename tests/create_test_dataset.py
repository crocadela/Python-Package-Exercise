from src.make_dataset import create_dataset
from src.clean_dataset import delete_nonyolo


# Create test_dataset
path = "test_files/sample_data/"
txt_path = path + "labels/"
img_path = path + "images/"
data_pec = create_dataset(path, return_nulls=True)
test_data = delete_nonyolo(txt_path, data_pec)
test_data.to_csv(path + 'test_data.csv')
