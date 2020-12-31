'''
Contains all the object-oriented logic for contructing monkey representations
'''

import utils

#Class for monkey object
class Monkey:
    def __init__(self, size, weight, fur_color, species=''):
        if not utils.check_hexacolor(fur_color):
            raise ValueError('fur_color needs to be hexadecimal color string')
        
        
        self.fur_color = fur_color 
        self.size = size
        self.weight = weight
        self.species = species
        
    #More readable representation for monkey object    
    def __repr__(self):
        return '[{0} {1} {2} {3}]'.format(self.size, self.weight, self.fur_color, self.species)
    
    #Get an attribute of the monkey object by computing it. The optional argument 'percent' rescale attribute's value if True (see euclidean_distance_monkey in utils)
    def get(self, attribute, percent = False):
        value = getattr(self, ''.join(['compute_', attribute]))()
        if percent == True:
            norms = {'fur_color': int('ffffff', 16),
                     'size' : 2,
                     'weight' : 1,
                     'bmi' : 100,
                     'fur_color_red' : 255,
                     'fur_color_green' : 255,
                     'fur_color_blue' : 255,
                     'fur_color_intensity': 1
                     }
            if attribute in norms.keys():
                value = (value/norms[attribute])*100
        
        return value
    
    def compute_fur_color(self):
        return int(self.fur_color[1:], 16)
    
    def compute_size(self):
        return self.size
    
    def compute_weight(self):
        return self.weight
    
    def compute_species(self):
        return self.species
    
    def compute_bmi(self):
        return self.weight/(self.size)**2
    
    def compute_fur_color_red(self):
        return int(self.fur_color[1:3], 16)
    
    def compute_fur_color_green(self):
        return int(self.fur_color[3:5], 16)
    
    def compute_fur_color_blue(self):
        return int(self.fur_color[5:7], 16)
    
    def compute_fur_color_intensity(self):
        R = self.compute_fur_color_red()
        G = self.compute_fur_color_green()
        B = self.compute_fur_color_blue()
        
        Cmax = max(R, G, B)
        if Cmax == 0:
            return 0.0
        
        Cmin = min(R, G, B)
        d = Cmax - Cmin
        
        return d/Cmax
    
    

