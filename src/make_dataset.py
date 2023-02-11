import pandas as pd
import os
import re

from src.clean_dataset import is_in_city
from src.check_correct_path import check_path


def read_labels(path: str) -> list:
    """Reads the files from the path and converts them into a list with one item per row.

       Parameters:
           path (str): Analyzed path

      Returns:
          (list): List with the values separated by row from the files.
        """
    # List to store the lines of each file
    lines = []
    txt_path = path+'/labels/'
    img_path = path+'/images/'

    # Check if paths are correct
    paths = [path, txt_path, img_path]
    list(map(check_path, paths))

    # Open the folder
    with os.scandir(txt_path) as label_list:
        for entry in label_list:
            if os.path.isfile(entry.path) and entry.name.endswith(".txt"):
                # Extract the file name without .txt
                label_name = os.path.splitext(entry.name)[0]
                img_name = label_name+'.png'
                img_file_path = os.path.join(img_path, img_name)
                # Confirm that it exists in the 'images' folder
                if not os.path.exists(img_file_path):
                    print("WARNING: Not image {} found in folder 'images'".format(label_name))
                    continue
                try:
                    with open(entry, 'r') as file:
                        # Get the city and date of the file
                        city, date = label_name.split("_")[0], label_name.split("_")[-1]
                        # Add the lines of the file to the list, along with 
                        # the full file name, city and date.
                        lines += [[line.strip(), label_name, city, date] for line in file.readlines()]
                except FileNotFoundError as e:
                    print(e)
    return lines


def read_codes(path: str) -> dict:
    """Reads the codes from the file and returns a dictionary with the code as the key
       and the name as the value.

       Parameters:
           path (str): Analyzed path

      Returns:
          (list): Dictionary with the code as the key and the name as the value.
        """
    # Check if the path is correct
    check_path(path)
    with open(path+'/class_name.txt', 'r') as inp:
        dict_codes = dict()
        pattern = re.compile(r"\d+\s(.+)")
        for line in inp:
            match = pattern.search(line)
            if match:
                dict_codes[line.split(" ")[0]] = match.group(1)
    return dict_codes
 
    
def create_dataset(path: str, return_nulls: bool = False) -> pd.DataFrame:
    """Organizes all the information collected by the read_labels() and
       read_codes() functions into a DataFrame.

       Parameters:
           path (str): Analyzed path
           return_nulls (bool): *Optional* Returns the information with the null
                                 values in the dataset.

      Returns:
              (pd.Dataframe): Dataframe with all the organized information.
        """
    # Check if path is correct
    check_path(path)
    labels = read_labels(path)
    codes = read_codes(path)
    data = pd.DataFrame(labels, columns=["raw", "file_name", "city", "date"])
    data[["object_id", "x", "y", "w", "h", "conf"]] = data["raw"].str.split(" ", expand=True)
    data = data.drop(columns=["raw"])
    # Extracted from https://stackoverflow.com/questions/29794959/pandas-add-new-column-to-dataframe-from-dictionary
    data["object"] = data["object_id"].map(codes)
    # Clean the dataset
    data = data.apply(lambda x: x.str.replace("\n", ""))
    # Convert columns to their corresponding type
    data['date'] = pd.to_datetime(data['date'], dayfirst=True, errors='coerce')
    # Convert multiple columns to float
    num_cols = ["object_id", "x", "y", "w", "h", "conf"]
    data[num_cols] = data[num_cols].apply(pd.to_numeric, errors='coerce')
    data = data.sort_values(by='file_name', ignore_index=True)
    if return_nulls is True:
        # Check null values
        if data.isnull().sum().sum() > 0:
            print("There are null values:\n", data.isnull().sum())
    return data


def to_csv(df: pd.DataFrame, file: str, path: str, img_folder: str, txt_folder: str):
    """Converts the dataframe into a csv with the name of the image, the city, the year
       and the number of cars, people and traffic lights.

       Parameters:
           df (pd.DataFrame): Analyzed dataframe
           file (str): Name of the final .csv
           path (str): Path where the .csv will be saved
           img_folder (str): Path of the image folder
           txt_folder (str): Path of the file folder

       Returns:
           (str): Saves the file and returns confirmation phrase.
    """

    # "Check if the paths are correct
    paths = [path, img_folder, txt_folder]
    list(map(check_path, paths))
    print("Starting to create the final dataset...")
    # Create a copy to avoid .loc message warning
    df = df.copy(deep=True)
    # Create a column with the year
    df['year'] = df['date'].dt.year
    final_data = df.groupby(['file_name', 'city', 'year']).size().reset_index()
    final_data = final_data[['file_name', 'city', 'year']]
    images = final_data['file_name']
    # Create columns for the objects
    objects = ['car', 'traffic light', 'person']
    for obj in objects:
        counts = []
        for img in images:
            count = df.loc[(df["file_name"] == img) & (df["object"] == obj), "object"].count()
            counts.append(count)
            in_city = is_in_city(img, img_folder, txt_folder)
            final_data.loc[final_data["file_name"] == img, "in_city"] = in_city
        final_data[obj] = counts

    print("Starting to create the .csv file..."")
    try:
        final_data.to_csv(path+file)
    except Exception as e:
        raise Exception("An error occurred while trying to save the csv file: {}".format(e))

    return "The file '{}' has been saved in '{}'. Thank you for joining us in this PEC!".format(file, path)
