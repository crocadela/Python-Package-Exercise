# Replies to PEC4

# Libraries
from src.make_dataset import create_dataset
from src.make_dataset import to_csv

from src.clean_dataset import delete_nonyolo
from src.clean_dataset import bad_img

from src.data_visualization import draw_bonding_boxes
from src.data_visualization import graph_objects
from src.data_visualization import obj_distr
from src.data_visualization import car_city_year_graph

from src.data_analysis import count_objects
from src.data_analysis import filter_by_conf
from src.data_analysis import object_per_image
from src.data_analysis import popular_objects
from src.data_analysis import car_city_year


if __name__ == "__main__":

    # File paths
    path = "data/dataset_cities/"
    txt_path = path+"labels/"
    img_path = path+"images/"

    # Exercise 1
    print("EXERCISE 1\n\nThe dataset has been saved in the 'data_pec' variable.\n")
    data_pec = create_dataset(path, return_nulls=True)
    print("\nEl resumen del dataset:\n")
    print(data_pec.info())
    print("\nY las primeras 5 filas:\n",
          data_pec.head())

    # 1.2         
    print("\nEXERCISE 1.2\n First, I would reduce the number of columns in the dataset as much as possible",
      	  "and the characters of each value.\n I would probably do without elements such as object names",
          "and reduce the name of the image to a numeric code.\n Secondly, I would carry out an algorithms analysis",
          "to evaluate if our code is efficient.\n I would use tools such as the %time magic instruction or %lprun",
          "to evaluate if we can improve it, \n as every microsecond we gain and every loop we reduce counts when we talk",
          "about a large volume of data.\n Having done this, I would resort to using multithreading, in order to be able to",
          "distribute the workload across different CPUs.")

    # Exercise 2
	print("\nEXERCISE 2\n\nAlthough initially we were going to implement the function for reading the csv file,",
    	  "we have decided to do it directly in the files, \n since it is safer to check the original sources,",
      	  "for better error control.\n")

    yolo_data = delete_nonyolo(txt_path, data_pec)

    # Exercise 3
    # Specify the width and height of the original image
    W, H = 2048, 1024

	print("\nEXERCISE 3\nSee the bounding boxes for the images:")
    for e in yolo_data["city"].unique():
        first_row = yolo_data[yolo_data['city'] == e].iloc[0]['file_name'] + '.png'
        print("Image {}".format(first_row))
        draw_bonding_boxes(first_row, 2048, 1024, yolo_data)

    # Exercise 4
    print("\nEXERCISE 4\nFirst, we filter our database to only contain files that have",
          "passed the 'YOLO' filter and objects with a confidence greater than 0.4.",
          "\nIt is saved under the variable 'ycf_data' and is the dataset that will",
          "be used in the following exercises. \nWe present the first rows: \n")
          
	# Filtered dataset by confidence level
    ycf_data = filter_by_conf(yolo_data, 0.4)
    print(ycf_data.head())

    # Exercise 4.1
    print("\EXERCISE 4.1\n")

    # Graph visualization
    graph_objects(ycf_data)
    print("As we can see in the graph, there is a great difference between cars and",
          "the rest of the detected objects.\n")
    top_5 = count_objects(ycf_data).head(5)
	print("The five most common objects are:")
    print(top_5)


    # Exercise 4.2
    print("\EXERCISE 4.2\n")
    print("The average number of objects per image is {}.".format(object_per_image(ycf_data)))

    # Exercise 4.3
    print("\EXERCISE 4.3\n")
    print("The three objects that have been most popular in the images are:",
          list(popular_objects(ycf_data).items())[0:3])
          
	print("\nThis result matches the list of most popular objects in the dataset,",
		  "\nbut it doesn't necessarily have to be this way. If an object appears in few",
		   "images,  \nbut in large numbers, it can surpass another element in the dataset's",
		   "popular list, but not per image: \nfor example, if the camera captures groups",
		   "of cyclists in some images.")


    # Exercise 5
    print("\EXERCISE 5\n")

	print("The number of cars found per year, for each city is:\n",
          car_city_year(ycf_data))

    # Graph visualization
    car_city_year_graph(ycf_data)

    # Exercise 6
    print("\EXERCISE 6\n")
    print("The found images are:\n",
          bad_img(img_path, txt_path))
          
    print("\nAt first, I thought about using the popular images to analyze the strange objects,",
          "but it wasn't completely rigorous. \nThat's why I tried to find a way to capture",
          "the image metadata, since the image sizes were different in the bad images.",
          "\nMore filters could be included, but it's risky to think that there can't be",
          "images without cars, traffic lights,... \nThe image size or color code are much",
          "more reliable for filters than the elements that appear in each photograph.")


    # Exercise 7
    print("\EXERCISE 7\n")
    path = 'data/'
    file = 'processed_data.csv'
    print(to_csv(ycf_data, file, path, img_path, txt_path))
