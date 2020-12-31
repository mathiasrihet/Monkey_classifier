'''
Contains utility functions and "glue" code
'''

import re
import numpy as np
import argparse
from functools import reduce

#Return true if the given color string is hexacolor: '#xxxxxx' (with lower case characters)
#Else return false
def check_hexacolor(color_str):
    if re.search("#[0-9, a-f]{6}", color_str):
        return re.search("#[0-9, a-f]{6}", color_str).group() == color_str
    else:
        return False

#Compute euclidean distance for two points on listed coordinates   
def euclidean_distance (a, b, norm, coordinates):
    d = ((a[axis]-b[axis])**2 for axis in coordinates)
    
    return np.sqrt(reduce(lambda acc, elem: acc + elem, d))

#Compute euclidean distance for two monkey objects on listed attributes (percent=True rescale attributes to give them approximatively all the same scale)
def euclidean_distance_monkey(m1, m2, attributes):
    d = ((m1.get(value, percent=True)-m2.get(value,percent=True))**2 for value in attributes)
    
    return np.sqrt(reduce(lambda acc, elem: acc + elem, d))

    
#Argparser for main() in monkey_classif.py
def get_cli_args():
    parser = argparse.ArgumentParser(description = 'Treat monkey dataframe')
    subparsers = parser.add_subparsers(dest = 'command', help = 'Two possible subcommands')
    
    
    parser_knn = subparsers.add_parser('knn', help = 'Compute knn function on a dataframe and save results')
    parser_knn.add_argument('indir', type=str, help='Input dir for original dataframe (including file name)')
    parser_knn.add_argument('outdir', type=str, help='Output dir for computed dataframe (including file name)')
    
    #Assure features >=2
    parser_knn.add_argument('features1', type=str, nargs=1, metavar='features' , choices = ['size', 'weight', 'bmi', 'fur_color', 'fur_color_red', 'fur_color_blue', 'fur_color_green', 'fur_color_intensity'], help='Attributes to use for the KNN algorithm (at least 2)' )
    parser_knn.add_argument('features2', type=str, nargs='+', metavar='features', choices = ['size', 'weight', 'bmi', 'fur_color', 'fur_color_red', 'fur_color_blue', 'fur_color_green', 'fur_color_intensity'], help=argparse.SUPPRESS )
    
    parser_visualize = subparsers.add_parser('visualize', help = 'Visualize values in a dataframe following two axis')
    parser_visualize.add_argument('indir', type=str, help='Input dir for dataframe')
    parser_visualize.add_argument('features', type=str, nargs = 2, metavar = 'features', choices = ['size', 'weight', 'fur_color'], help='Features to use as X and Y coordinates')
    
    
    
    args = parser.parse_args()
    
    return args


