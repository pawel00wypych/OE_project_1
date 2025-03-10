import random
import pandas as pd

class Chromosome:


    def __init__(self,
                 number_of_variables,
                 precision,
                 variables_list):
        """variables_list - values ranges for all variables
           ex. for x,y,z -> variables = [(0,5),(-1,7),(2, 8)]
           x = (0,5), y = (-1,7), z = (2, 8)"""
        self.number_of_variables = number_of_variables
        self.variables_list = variables_list
        self.precision = precision
        self.ranges = []
        self.number_of_bits_variables = []
        self.number_of_bits_chromosome = 0
        self.chromosome = []
        self.decoded_variables = []

        self.calculate_ranges()
        self.calculate_number_of_bits()


    def calculate_ranges(self):
        """calculates ranges for all variables"""
        self.ranges = []  # Clear any previous ranges to avoid duplication
        for min_val, max_val in self.variables_list:
            self.ranges.append(abs(max_val - min_val))

    def calculate_number_of_bits(self):
        """We are calculating number of bits for chromosome and variables"""
        if not self.ranges:
            self.calculate_ranges()

        ranges_series = pd.Series(self.ranges)
        scaled_ranges = ranges_series * pow(10, self.precision)
        self.number_of_bits_variables = scaled_ranges.apply(lambda x: len(bin(int(x))[2:])).tolist()
        self.number_of_bits_chromosome = sum(self.number_of_bits_variables)

    def generate_chromosome(self):
        self.chromosome = [random.randint(0,1) for _ in range(self.number_of_bits_chromosome)]

    def decode_variables(self):
        variables_list_series = pd.Series(self.variables_list)
        start_idx = 0

        for i in range(self.number_of_variables):
            min_val, max_val = variables_list_series[i]
            num_bits = self.number_of_bits_variables[i]

            # get proper chromosome segment (representing variable)
            end_idx = start_idx + num_bits
            segment = self.chromosome[start_idx:end_idx]

            # calculating segment as decimal value
            decimal_value = int("".join(str(bit) for bit in segment), 2)

            # transforming into real value (scaled value)
            scaled_value = min_val + (decimal_value * (max_val - min_val)) / (pow(2, num_bits) - 1)
            self.decoded_variables.append(scaled_value)
            start_idx = end_idx
