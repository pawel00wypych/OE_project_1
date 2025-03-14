import random
import pandas as pd

class Chromosome:

    def __init__(self,
                 number_of_variables,
                 precision,
                 variables_ranges_list,
                 chromosome=None,
                 fitness=0):
        """variables_ranges_list - values ranges for all variables
           ex. for x,y,z -> variables = [(0,5),(-1,7),(2, 8)]
           x = (0,5), y = (-1,7), z = (2, 8)"""
        if chromosome is None:
            chromosome = []

        self.number_of_variables = number_of_variables
        self.variables_ranges_list = variables_ranges_list
        self.precision = precision
        self.ranges = []
        self.number_of_bits_variables = []
        self.number_of_bits_chromosome = 0
        self.chromosome = chromosome
        self.decoded_variables = []
        self.fitness = fitness

        self.calculate_ranges()
        self.calculate_number_of_bits()


    def calculate_ranges(self):
        """calculates ranges for all variables"""
        self.ranges = []  # Clear any previous ranges to avoid duplication
        for min_val, max_val in self.variables_ranges_list:
            if min_val < max_val:
                self.ranges.append(max_val - min_val)
            else:
                self.ranges.append(min_val - max_val)


    def calculate_number_of_bits(self):
        """We are calculating number of bits for chromosome and variables"""
        if not self.ranges:
            self.calculate_ranges()

        scaled_ranges =  [x * pow(10, self.precision) for x in self.ranges]
        self.number_of_bits_variables = [ len(bin(int(x))[2:]) for x in scaled_ranges]
        self.number_of_bits_chromosome = sum(self.number_of_bits_variables)

    def generate_chromosome(self):
        self.chromosome = [random.randint(0,1) for _ in range(self.number_of_bits_chromosome)]

    def convert_bin_to_decimal(self, list_of_bits):
        return sum(val*(2**idx) for idx, val in enumerate(reversed(list_of_bits)))

    def decode_variables(self):
        self.decoded_variables = []
        variables_list_series = pd.Series(self.variables_ranges_list)
        start_idx = 0

        for i in range(self.number_of_variables):
            min_val, max_val = variables_list_series[i]
            num_bits = self.number_of_bits_variables[i]

            if num_bits == 0:
                self.decoded_variables.append(min_val)
                continue

            # get proper chromosome segment (representing variable)
            end_idx = start_idx + num_bits
            segment = self.chromosome[start_idx:end_idx]

            # calculating segment as decimal value
            decimal_value = self.convert_bin_to_decimal(segment)

            # transforming into real value (scaled value)
            if min_val < max_val:
                scaled_value = min_val + (decimal_value * (max_val - min_val)) / (pow(2, num_bits) - 1)
            else:
                scaled_value = min_val - (decimal_value * (min_val - max_val)) / (pow(2, num_bits) - 1)

            if scaled_value < min_val:
                scaled_value = min_val
            elif scaled_value > max_val:
                scaled_value = max_val

            self.decoded_variables.append(scaled_value)
            start_idx = end_idx
