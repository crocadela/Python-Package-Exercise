import os

import pandas as pd
import re
from PIL import Image

from src.check_correct_path import check_path


def check_yolo(file_path: str) -> bool:
    """Checks if the files are YOLO formatted.

       Parameters:
           file_path (str):Path to the folder where the files are located.

       Returns:
           (bool): Returns True if the file is properly formatted.
    """

    # Check if the path is correct
    check_path(file_path)

    def not_int(element: str) -> bool:
        """Checks if an element is an integer between 0 and 79.

            Parameters:
                element (str): Element to check, probably str.

            Returns:
                (bool): Returns True if it is not an integer.
            """
        if element.isnumeric():
            try:
                int(element)
                return not 0 <= int(element) <= 79
            except ValueError:
                return True
        else:
            return True

    def not_float(element: str) -> bool:
        """Checks if an element is a numeric between 0 and 1.

           Parameters:
           element (str):Element to check, probably str.

           Returns:
           (bool): Returns True if it is not numeric.
        """
        return not 0 <= float(element) <= 1

    try:
        # Open the file
        with open(file_path, 'r') as file:
            # Read the lines of the file
            lines = file.readlines()

            for line in lines:
                # Split the line into elements
                elements = line.split()
                 # Check that the number of elements is 6
                if len(elements) != 6:
                    print("The file {} does not have the right number of columns".format(file_path))
                    return False
                # Check that the elements are numeric
                for element in elements:
                    if not element.replace('.', '').isnumeric():
                        print("{}, in row {} of file {}".format(element, elements, file_path),
                              "has the wrong format.")
                        return False
                    # Check that the first element is an integer between 0 and 79
                    if element == elements[0]:
                        if not_int(element):
                            print("{}, in row {} of file {}".format(element, elements, file_path),
                                  "has an the wrong format.")
                            return False
                    else:
                        # Check that the other elements are decimals between 0 and 1
                        if not_float(element):
                            print("{}, in row {} of file {}".format(element, elements, file_path),
                                  "has an the wrong format.")
                            return False
            return True
    except ValueError:
        return False


def non_yolo_list(txt_path: str) -> list:
    """Creates a list of filenames that are not YOLO formatted.

        Parameters:
            txt_path (str): Path to the folder of the files.

        Returns:
            (list): List with wrong files.
    """

    # Check if the path is right
    check_path(txt_path)
    # List of files with non-YOLO format
    invalid_files = []

    # Iterate through all files in the path
    for file in os.listdir(txt_path):
        file_path = os.path.join(txt_path, file)
        if os.path.isfile(file_path) and file.endswith(".txt"):
            # Check if file is in YOLO format
            if not check_yolo(file_path):
                invalid_files.append(file.replace('.txt', ''))

    # If the list is empty, display this message
    if not invalid_files:
        print("\nNo incompatible files found.")

    else:
        print("\nFiles with incorrect values are:", invalid_files,
              "\n\nWe proceed to delete them from the dataset.")

    return invalid_files


def delete_nonyolo(txt_path: str, data: pd.DataFrame, drop_nulls: bool = False) -> pd.DataFrame:
    """Deletes files that do not have YOLO format from the dataset.

       Parameters:
           txt_path (str): Path of the file folder.
           data (str): Dataframe to be deleted from.
           drop_nulls (bool): *Optional* Deletes null values from dataframe.

       Returns:
           (pd.DataFrame): Clean dataframe.
    """
    # Check if the path is correct
    check_path(txt_path)
    invalid_files = non_yolo_list(txt_path)
    # Store the list of image names that have the wrong format
    deleted = data['file_name'].isin(invalid_files)
    print("Se eliminan {} filas del dataset.".format(deleted.sum()))
    # Update the dataset without errors
    new_data = data[~deleted]
    # Total number of nulls
    nulls = new_data.isnull().sum().sum()
    if nulls > 0:
        print("\nThere are null values:\n", new_data.isnull().sum())
        # Option to delete nulls
        if drop_nulls is True:
            new_data = new_data.dropna()
            print("\nDeleting {} rows from the dataset due to null values.".format(nulls))
    else:
        print("\nThere are no null values.\n")
    return new_data


def bad_img(img_folder: str, txt_folder: str) -> set:
    """Detects images that have a different format than the images from the capture cameras.

       Parameters:
          img_folder (str): Path of the image folder.
          txt_folder (str): Path of the file folder.

      Returns:
          (set): List of type set with images that do not have the correct format.
    """

    # Check if the paths are correct
    paths = [img_folder, txt_folder]
    list(map(check_path, paths))

    bad_list = set()
    # Open the folder
    with os.scandir(img_folder) as img_list:
        for img in img_list:
            # Check that the file is an image
            if os.path.splitext(img.name)[1] not in {'.jpg',
                                                     '.jpeg',
                                                     '.png',
                                                     '.gif'
                                                     }:
                continue
            # Taken from https://www.thepythoncode.com/article/extracting-image-metadata-in-python
            # Read the image using PIL
            image = Image.open(img.path)
            info_dict = {
                    "Filename": image.filename,
                    "Image Size": image.size,
                    "Image Height": image.height,
                    "Image Width": image.width,
                    "Image Format": image.format,
                    "Image Mode": image.mode,
                    "Image is Animated": getattr(image, "is_animated", False),
                    "Frames in Image": getattr(image, "n_frames", 1)
                    }
            # Conditions for taking it as a bad image:
            # 1. If it's not in the file list
            cond1 = os.path.splitext(img.name)[0] + '.txt' not in os.listdir(txt_folder)
            # 2. If the image size is not the same as the others
            cond2 = info_dict['Image Size'] != (2048, 1024)
            # 3. If it's vertical
            cond3 = info_dict['Image Height'] != 1024
            # 4. If it's not PNG
            cond4 = info_dict['Image Format'] != 'PNG'
            # 5. If it doesn't have RGB color code
            cond5 = info_dict['Image Mode'] != 'RGB'

            if cond1 or cond2 or cond3 or cond4 or cond5:
                bad_list.add(img.name)

            image.close()

        if not bad_list:
            print("\nNo strange images have been found.")

        return bad_list


def is_in_city(image: str, img_folder: str, txt_folder: str) -> bool:
    """Returns a boolean for images that have a different format than
       the capture camera images.

       Parameters:
          image (str): Name of the analyzed image without the extension
          img_folder (str): Path of the image folder
          txt_folder (str): Path of the file folder

      Returns:
          (bool): Returns True if the image has the right format.
    """

    # Check if the paths are correct
    paths = [img_folder, txt_folder]
    list(map(check_path, paths))

    # Remove the extension with regex
    pattern = r'\.[a-zA-Z]+$'
    bad_imgs = bad_img(img_folder, txt_folder)
    bad_img_set = set(map(lambda x: re.sub(pattern, '', x), bad_imgs))
    # Check that the image is not in the file of images with poor format
    if image in bad_img_set:
        return False
    else:
        return True
