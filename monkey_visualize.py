'''
Contains all the logic for producing visualizations
'''
import utils
import matplotlib.pyplot as plt
import pandas as pd

#Turn hexacolors strings into integers in order to display them correctly
def lookFor_hexa(value):
    if type(value) == str:
        if utils.check_hexacolor(value):
            return int(value[1:], 16)
    return value

#Display a scatter plot with values collored by labels and following X and Y axis 
def scatter_plot (X, Y, labels):
    data = pd.DataFrame({'X':X, 'Y':Y, 'labels':labels})
    data = data.applymap(lookFor_hexa)
    groups = data.groupby('labels')
    
    for name, group in groups:
        plt.scatter(group['X'], group['Y'], label=name)
        
    plt.legend()
    plt.show()