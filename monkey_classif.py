'''
Responsible for running the classification algorithm
'''
import pandas as pd
import numpy as np
import utils
import monkey_model as model
import monkey_visualize as visual
from collections import Counter
from utils import get_cli_args

########################
##Read monkeys dataframe
########################

#Convert hexadecimal color string '#xxxxxx' into an integer.
def hexa_to_int(hexa_color_str):
    return int(hexa_color_str[1:], 16)

#Set all values which are not hexadecimal color string to None in a column of a dataframe.  
def drop_nonhexa(value):
    value = str(value)
    if utils.check_hexacolor(value):
        return value
    else:
        return None

#Set all values which are <0 to None in a column of a dataframe. 
def drop_negative(value):
    if value >=0:
        return value
    else:
        return None
    
#Produce a dataframe of monkeys as required in Exercise 2
def read_monkeys_from_csv(csv_path, strict = False):
    data = pd.read_csv(csv_path)
    
    #Raise ValueError if wrong headers
    err = "Headers must be 'species', 'size', 'weight' and 'fur_color'"
    if len(data.columns)!=4:
        raise ValueError(err)
    
    for col in data.columns:
        if col not in ['species', 'size', 'weight', 'fur_color']:
            raise ValueError(err)
    if strict:
        if len(data.dropna()) != len(data):
            raise ValueError('Dataframe contains missing values')
    
    #Clean data (the dict map each column with a cleaning function)
    clean_dict = {'size':drop_negative, 'weight':drop_negative, 'fur_color':drop_nonhexa}
    for key, value in clean_dict.items():
        data[key] = data[key].apply(value)
    data = data.dropna(subset= clean_dict.keys())
    

    #Add monkey column
    data = np.round(data, 10) #reaches calculation limits otherwise
    data['monkey'] = data[['size', 'weight', 'fur_color', 'species']].apply(lambda x: model.Monkey(*x), axis=1)
    
    #Add fur_color_int column
    data['fur_color_int'] = data['fur_color'].apply(hexa_to_int)
    
    #Add bmi column
    data['bmi'] = data['monkey'].apply(lambda x: x.compute_bmi())
    
    return data   

##########################################
##knn algorithm with simple plurality vote
##########################################

#Infer species attribute of a monkey object based on a simple plurality vote among it k neighbors.
#Axis of the multidimensional space are given by 'attributes'
def class_a_monkey(m, label_list, k, attributes):
    
    neighbors = sorted(label_list, key = lambda x: utils.euclidean_distance_monkey(x, m, attributes))[:k]
    neighbors_species = (m.get('species') for m in neighbors)
    m.species = Counter(neighbors_species).most_common(1)[0][0]

#Infer species for each unlabelled monkey in the dataframe
#Written in a functional programming style as required for Exercise#3 bonus#1
def compute_knn(dataframe, attributes, k=5):
    
    labelled = dataframe[dataframe.species.isnull()==False]
    unlabelled = dataframe[dataframe.species.isnull()]
    
    unlabelled['monkey'].apply(lambda x: class_a_monkey(x, labelled['monkey'], k, attributes))
    dataframe['species'] = dataframe['monkey'].apply(lambda x: x.get('species'))

    return dataframe


############################################
##knn algorithm with weighted plurality vote
############################################

#Give a weight to each neighbor in k neighbors based on: euclidean_distance(monkey, neighbor)/euclidean_distance(monkey, k+1 neighbor)
#It assures that 0 <= weight <= 1
def distance_to_weight(x, m, norm, attributes):
    normalized_distance = utils.euclidean_distance_monkey(x, m, attributes)/utils.euclidean_distance_monkey(norm, m, attributes)
    weight = 1-normalized_distance
    
    return x.species, weight

#Sum labelled weights of each neighbors in a dict with labels as keys.
def group_species(gen):
    d = {}
    
    for elem in gen: 
        if elem[0] in d.keys():
            d[elem[0]] += elem[1]
        else:
            d[elem[0]] = elem[1]
    
    return d

#Infer species attribute of a monkey object based on a weighted plurality vote among it k neighbors.
#Axis of the multidimensional space are given by 'attributes'
def class_a_monkey_weighted(m, label_list, k, attributes):
    
    neighbors = sorted(label_list, key = lambda x: utils.euclidean_distance_monkey(x, m, attributes))[:k+1]
    neighbors_weight = map(lambda x: distance_to_weight(x, m, neighbors[-1],attributes), neighbors[:-1])
    out = group_species(neighbors_weight)
    m.species = max(out)

#Infer species for each unlabelled monkey in the dataframe
def compute_knn_weighted(dataframe, attributes, k=5):
    
    labelled = dataframe[dataframe.species.isnull()==False]
    unlabelled = dataframe[dataframe.species.isnull()]
    
    unlabelled['monkey'].apply(lambda x: class_a_monkey_weighted(x, labelled['monkey'], k, attributes))
    dataframe['species'] = dataframe['monkey'].apply(lambda x: x.get('species'))

    return dataframe


################
##Save dataframe
################

def save_to_csv(dataframe, path):
    dataframe.to_csv(path_or_buf =path, columns = ['species', 'fur_color', 'size', 'weight'], index = False)


#############################
##Main function with argparse
#############################

#Depends on the subcommand
def main():
    args = get_cli_args()
    
    #Compute knn on an input dataframe and save it as a csv file 
    if args.command == 'knn':
        dataframe = read_monkeys_from_csv(args.indir)
        attributes = args.features1 + args.features2
        #this way knn can be computed for any number>=2 of features required in Exercise#3 bonus#2
        dataframe = compute_knn(dataframe, attributes)
        save_to_csv(dataframe, args.outdir)
     
    #Display a scatterplot of values from an input dataframe following two axis  
    if args.command == 'visualize':
        dataframe = read_monkeys_from_csv(args.indir, strict =  True)
        X, Y = args.features
        labels = 'species'
        visual.scatter_plot(dataframe[X], dataframe[Y], dataframe[labels])
        


main()