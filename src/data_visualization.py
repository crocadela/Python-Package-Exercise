from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
import pandas as pd
from src.data_analysis import car_city_year


def draw_bonding_boxes(img: str, img_width: int, img_height: int, df: pd.DataFrame) -> None:
    """Draws bounding boxes on the provided image.

       Parameters:
           img (str): Analyzed path
           img_width (int): Image width
           img_height (int): Image height
           df (pd.DataFrame): Dataset where image data is stored

       Returns:
           (None): Image with the drawn rectangles.
    """
    img_path = 'data/dataset_cities/images/' + img
    img_name = img.replace('.png', '')
    img_rows = df[df['file_name'] == img_name]

    # Image size
    W, H = img_width, img_height

    img = plt.imread(img_path)
    figure, ax = plt.subplots(1)
    ax.imshow(img)

    for i, row in img_rows.iterrows():
        # YOLO coordinates denormalization
        x, y = float(row['x']) * W, float(row['y']) * H

        # Define object dimensions
        w, h = float(row['w']) * W, float(row['h']) * H

        # Change coordinates
        x1 = x - w / 2
        y1 = y - h / 2

        # Create rectangle
        rect = Rectangle((x1, y1), w, h, linewidth=1, edgecolor='r', facecolor='none')

        ax.add_patch(rect)
    plt.show()


def graph_objects(data):
    """Plots the number of appearances by object.

       Parameters:
           data (pd.DataFrame): Dataset from where it extracts the data

       Returns:
           (None): Bar chart with the number of appearances by object.
    """
    objects = data[['object_id', 'object']]
    ax = sns.countplot(y=objects["object"], order=objects["object"].value_counts().index)
    sns.set(rc={'figure.figsize': (30, 15)})
    ax.bar_label(ax.containers[0], label_type='edge')
    plt.title("Número de apariciones por objeto", fontsize=20)
    plt.show()



def car_city_year_graph(data: pd.DataFrame) -> None:
    """Grafica el número de coches por ciudad y año.

       Parameters:
           data (pd.DataFrame): Dataset de donde extrae los datos

       Returns:
           (None): Gráfico con una línea por cada ciudad.
    """
    cars = car_city_year(data)
   # Create a line graph for each city
    for city in cars['city'].unique():
        by_city = cars[cars['city'] == city]
        plt.plot(by_city['year'], by_city['count'], label=city)

    # Add labels and title to the graph
    plt.xlabel('Año')
    plt.ylabel('Número de coches')
    plt.title('Número de coches por ciudad y año')

    plt.legend()

    plt.show()
