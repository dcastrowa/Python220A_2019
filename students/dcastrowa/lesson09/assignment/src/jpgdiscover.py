"""Recursion program for discovering PNG files in nested dirs."""
import os


def list_jpg_files(directory):
    """
    Takes a directory and recurses through it to find .png files
    and returns a list of lists for the path the .png files were found
    and the files itself.
    :param directory str: directory to recurse through
    :return list of values including path where .png was found and
    list of items in that dir that match .png.
    :rtype list
    """
    list_of_paths = []
    for root, dirs, files in os.walk(directory):
        list_of_files = []
        for file in files:
            if '.png' in file:
                list_of_files.append(file)
        if list_of_files:
            list_of_paths.append(root)
            list_of_paths.append(list_of_files)
        for dire in dirs:
            list_jpg_files(dire)
    return list_of_paths


if __name__ == "__main__":
    JPGS = list_jpg_files(os.getcwd())
    for jpg in JPGS:
        print(jpg)
