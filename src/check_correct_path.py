import os


def check_path(path: str) -> None:
    """Checks that the path is correct and returns an exception if it is not.

	   Parameters:
	   path (str): Analyzed path

	   Returns:
	   (None): Returns Exception if the path is incorrect."
    """
    if not os.path.exists(path):
        text = "The path '{}' does not exist. Please, check if it is correct or needs to be created."
        raise Exception(text.format(path))
