import sys
import unittest

sys.path.append('../..')
from genetic_algorithm.chromosome import Chromosome

class TestChromosome(unittest.TestCase):

    def test_initialization(self):
        variables = [(0, 5), (-1, 7), (2, 8)]
        precision = 2
        chromo = Chromosome(number_of_variables=3, precision=precision, variables_ranges_list=variables)

        self.assertEqual(chromo.number_of_variables, 3)
        self.assertEqual(chromo.precision, 2)
        self.assertEqual(chromo.variables_ranges_list, variables)

    def test_empty_variables(self):
        chromo = Chromosome(number_of_variables=0, precision=2, variables_ranges_list=[])

        self.assertEqual(chromo.ranges, [])
        self.assertEqual(chromo.number_of_bits_variables, [])
        self.assertEqual(chromo.number_of_bits_chromosome, 0)

    def test_single_variable(self):
        variables = [(0, 10)]
        precision = 2
        chromo = Chromosome(number_of_variables=1, precision=precision, variables_ranges_list=variables)

        chromo.calculate_number_of_bits()

        # Expected bit length for a range of 10, scaled by 10^2
        expected_bits = len(bin(int(10 * pow(10, precision)))[2:])
        self.assertEqual(chromo.number_of_bits_variables, [expected_bits])
        self.assertEqual(chromo.number_of_bits_chromosome, expected_bits)

    def test_negative_range(self):
        variables = [(-5, 5)]
        precision = 3
        chromo = Chromosome(number_of_variables=1, precision=precision, variables_ranges_list=variables)

        chromo.calculate_number_of_bits()

        expected_bits = len(bin(int(10 * pow(10, precision)))[2:])
        self.assertEqual(chromo.number_of_bits_variables, [expected_bits])
        self.assertEqual(chromo.number_of_bits_chromosome, expected_bits)

    def setUp(self):
        self.variables_list = [(0, 5), (-1, 7), (2, 8)]
        self.number_of_variables = len(self.variables_list)
        self.precision = 2
        self.chromosome_obj = Chromosome(self.number_of_variables, self.precision, self.variables_list)

    def test_calculate_ranges(self):
        self.chromosome_obj.calculate_ranges()
        expected_ranges = [5, 8, 6]
        self.assertEqual(self.chromosome_obj.ranges, expected_ranges)

    def test_calculate_number_of_bits(self):
        self.chromosome_obj.calculate_number_of_bits()
        self.assertEqual(self.chromosome_obj.number_of_bits_variables, [9, 10, 10])
        self.assertEqual(self.chromosome_obj.number_of_bits_chromosome, 29)

    def test_generate_chromosome(self):
        self.chromosome_obj.generate_chromosome()
        self.assertEqual(len(self.chromosome_obj.chromosome), self.chromosome_obj.number_of_bits_chromosome)
        self.assertTrue(all(bit in [0, 1] for bit in self.chromosome_obj.chromosome))

    def test_decode_variables(self):
        self.chromosome_obj.chromosome = [
            1,1,1,1,1,0,1,0,0,
            1,1,0,0,1,0,0,0,0,0,
            1,0,0,1,0,1,1,0,0,0
        ]
        self.chromosome_obj.decode_variables()
        expected_decoded_variables = [4.892, 5.256, 5.519]
        self.assertEqual([round(x,3) for x in self.chromosome_obj.decoded_variables], expected_decoded_variables)

    def test_decode_single_variable(self):
        self.chromosome_obj.number_of_variables = 1
        self.chromosome_obj.number_of_bits_variables = [5]
        self.chromosome_obj.chromosome = [1, 0, 0, 1, 1]
        self.chromosome_obj.decode_variables()
        expected_decoded_variable = [3.064516129032258]
        self.assertEqual(self.chromosome_obj.decoded_variables, expected_decoded_variable)

    def test_decode_negative_range(self):
        self.chromosome_obj.variables_ranges_list = [(-5, 5)]
        self.chromosome_obj.number_of_variables = 1
        self.chromosome_obj.number_of_bits_variables = [10]
        self.chromosome_obj.chromosome = [1,1,1,1,1,0,1,0,0,0]
        self.chromosome_obj.decode_variables()
        expected_decoded_variable = [4.775]
        self.assertEqual([round(x,3) for x in self.chromosome_obj.decoded_variables], expected_decoded_variable)


if __name__ == "__main__":
    unittest.main()