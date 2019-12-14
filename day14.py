import numpy as np
from collections import defaultdict

with open('/Users/relyea/data/input.txt') as input_file:
    inpfile = input_file.readlines()

# fill a dictionary with all the formulas
formuladict = {}
for line in inpfile:
    output = line.split(' => ')[1].strip()
    inputs = line.split(' => ')[0]
    inputlist = inputs.split(',')
    for theinput in inputlist:
        if output not in formuladict:
            formuladict[output] = [theinput.strip()]
        else:
            formuladict[output].append(theinput.strip())


class oreGetter(object):
    def __init__(self, formuladict):
        self.formuladict = formuladict
        self.reset_surplus()

    def reset_surplus(self):
        self.surplus = defaultdict()
        self.surplus['ORE'] = 0
        for key in formuladict:
            number, element  = self.get_number_and_element(key)
            self.surplus[element] = 0
    
    def get_formula_number(self, element: str):
        number_and_element_in_formula = [key for key in self.formuladict if element in key][0]
        return np.int(number_and_element_in_formula.split(' ')[0])

    def get_number_and_element(self, number_and_element):
        number, element = number_and_element.split(' ')
        number = np.int(number)
        return number, element
    
    def get_reactants(self, element):
        number_and_element_in_formula = [key for key in self.formuladict if element in key][0]
        return self.formuladict[number_and_element_in_formula]
    
    def get_num_ore(self, number_and_element):
        num_ore = 0
        number_needed, element_needed  = self.get_number_and_element(number_and_element)
        # print('REQUIREMENTS',element_needed, '\t', number_needed)
        
        # pull from surplus first
        if number_needed <= self.surplus[element_needed]:
            self.surplus[element_needed] -= number_needed
            # print('OVERSURPLUS EXISTS', num_ore)
            return num_ore # we need no additional ore because we already made this element
        elif self.surplus[element_needed] > 0:
            # print('HAD A SURPLUS', self.surplus[element_needed])
            number_needed -= self.surplus[element_needed]
            self.surplus[element_needed] = 0
        number_in_formula = self.get_formula_number(element_needed)
        # print('FORMULA',element_needed, '\t', number_in_formula)
        
        # deterine how many operations we need to get the required number of the element
        if number_needed // number_in_formula == number_needed / number_in_formula:
            extra = 0
            multiple = number_needed // number_in_formula
        else:
            multiple = number_needed // number_in_formula + 1
            extra = multiple * number_in_formula - number_needed
            self.surplus[element_needed] += extra
        # print('MULTIPLE AND EXTRA', multiple, ' ', extra)

        # figure out the ore for each of the necessary reactancts to create this element
        for reactant_and_number in self.get_reactants(element_needed):
            reactant_number, reactant = self.get_number_and_element(reactant_and_number)
            # print('REACTANT',reactant, '\t', reactant_number, '\t', reactant_number * multiple)
            if reactant == 'ORE':
                num_ore += reactant_number * multiple
                # print('JUST ORE', reactant_number * multiple, num_ore)
            else:
                new_ore = self.get_num_ore(str(multiple * reactant_number) + ' ' + reactant)
                num_ore += new_ore
                # print('GET MORE', reactant, new_ore, num_ore)
        return num_ore


ore_getter = oreGetter(formuladict)
ore_for_1_fuel = ore_getter.get_num_ore('1 FUEL')
# this produces 483766, which is correct

n_ore = 1e12
approxnum = int(n_ore // ore_for_1_fuel)
not_converged = True
while not_converged:
    ore_getter.reset_surplus()
    ore_needed = ore_getter.get_num_ore(str(approxnum)+' FUEL')
    approxnum = np.int(approxnum * 1e12/ore_needed)
    print(ore_needed, approxnum)
    aa = input()
    ore_getter.reset_surplus()
    ore_needed = ore_getter.get_num_ore(str(approxnum)+' FUEL')
