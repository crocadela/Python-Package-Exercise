import pandas as pd


def filter_by_conf(data: pd.DataFrame, conf: float) -> pd.DataFrame:
    """Filters the dataset by confidence level.

          Parameters:
              data (pd.Dataframe): Dataframe to be filtered
              conf (int): Confidence level

          Returns:
              (pd.Dataframe): Filtered dataframe
        """
    return data[data['conf'] > conf]


def count_objects(data: pd.DataFrame) -> pd.DataFrame:
    """Counts the total number of objects by type,
       creates a new column with the results 'counts
       and returns the dataframe ordered from highest to lowest.

       Parameters:
           data (pd.Dataframe): Dataframe

       Returns:
           (pd.Dataframe): Filtered dataframe
        """
    # Count occurrences in a particular column
    objects_freq = data.groupby(['object_id', 'object']).size().sort_values(ascending=False)
    return objects_freq.reset_index(name='counts')


def object_per_image(data: pd.DataFrame) -> int:
    """Calculates the average number of total objects per image.

       Parameters:
           data (pd.Dataframe): Analyzed dataframe

       Returns:
           (int): Average
        """
    return round(data.groupby(['file_name']).size().mean())


def popular_objects(data: pd.DataFrame) -> dict:
    """Counts the number of objects by popularity, following these rules:
       1. If it has less than 3 objects or exactly 3 different objects
          we keep all those objects that appear.
       2. If it has more than 3 different objects:
            2.1) If the highest frequency appears in more than three objects,
                 we keep all those objects as the most popular
                 (in this case it can be more than three).
            2.2) If there is no tie between popularity between the 3rd and 4th most popular object
                 we keep the top 3 frequent objects.
            2.3) If the popularity tie occurs between the 3rd and 4th most frequent object
                 we do the following:
                    2.3.1) If the tie occurs between the third and fourth most frequent object
                           we only keep the two most popular objects.
                    2.3.2) If the frequency tie occurs between the second
                           and third most frequent objects we only keep the most popular object.

       Parameters:
           data (pd.Dataframe): Analyzed dataframe

       Returns:
           (dict): Dictionary with objects as 'keys' and the number of times it has been among
                   the three most popular objects as 'values'.
        """
    # Select the number of objects by class and image
    c_ob = data.groupby(['file_name', 'object']).size().reset_index(name='counts')
    # Sort the dataset
    counted_objects = c_ob.sort_values(by=['file_name', 'counts'], ascending=[True, False]).reset_index(drop=True)

    # Select the total number of different objects per image
    counted_images = counted_objects.groupby(['file_name']).size().reset_index(name='counts')

    # Select the images that have equal to or less than three objects
    counted_less = set(counted_images[counted_images['counts'] <= 3]['file_name'])
    # Dictionary to be filled
    pop_dict = dict()

    def dict_insert(object: str, dic: dict) -> dict:
        """Inserts values into the dictionary according to whether they were already in it
           and adds 1 for each time a value is found.

           Parameters:
               object (str): Object name
               dic (dict): Dictionary in which the objects will be inserted

           Returns:
               (dict): Dictionary with the object inserted.
        """
        if object not in dic:
            dic[object] = 1
        else:
            dic[object] += 1
        return dic

    # Case 1: Less than 3 different objects
    for i, row in counted_objects.iterrows():
        if row['file_name'] in counted_less:
            pop_dict = dict_insert(row['object'], pop_dict)

        else:
            # Case 2: More than 3 different objects
            # 2.1) The highest frequency appears in more than 3 objects
            # First row
            cond1 = row.equals(counted_objects.loc[0])
            # If not first row, it does not have to share the image name with its previous row
            if i != 0:
                cond2 = row['file_name'] != counted_objects.loc[i - 1][0]
            if cond1 or cond2:
                pop_dict = dict_insert(row['object'], pop_dict)
                max_value = row['counts']
            # Select the rows with the same value
            elif row['file_name'] == counted_objects.loc[i - 1][0]:
                if row['counts'] == max_value:
                    pop_dict = dict_insert(row['object'], pop_dict)
                # 2.2) If there is no tie between the popularity of the 3rd and 4th 
                # most popular object, we keep the 3 most frequent objects
                # The second one
                elif row['file_name'] != counted_objects.loc[i - 2][0]:
                    if row['counts'] == counted_objects.loc[i + 2][2]:
                        pass
                    else:
                        pop_dict = dict_insert(row['object'], pop_dict)
                # The third pne
                elif row['file_name'] != counted_objects.loc[i - 3][0]:
                    # 2.3.1) If the tie occurs between the third and fourth object
                    if row['counts'] == counted_objects.loc[i + 1][2]:
                        pass
                    else:
                    	# Finally, keep the third one in order to meet 2.2
                        pop_dict = dict_insert(row['object'], pop_dict)
                else:
                    pass
    # Sort the dictionary from highest to lowest value
    sorted_dict = dict(sorted(pop_dict.items(), key=lambda x: x[1], reverse=True))
    return sorted_dict


def car_city_year(data: pd.DataFrame) -> pd.DataFrame:
    """Counts the number of cars by city and year.

       Parameters:
           data (pd.Dataframe): Analyzed dataframe

       Returns:
           (pd.Dataframe): Dataframe with the number of cars by city and year.
        """
    # Create a copy to avoid the warning message
    data = data.copy(deep=True)
    # Create a column with the year of the date
    data['year'] = data['date'].dt.year

    # Count the number of cars by city and year
    cars = data[data['object'] == 'car'].groupby(['city', 'year']).size().reset_index(name='count')
    return cars
