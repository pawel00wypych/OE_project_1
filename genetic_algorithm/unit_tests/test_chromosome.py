import sys
import unittest
from unittest.mock import patch
from itertools import cycle

sys.path.append('../..')
from genetic_algorithm.chromosome import Chromosome

class TestChromosome(unittest.TestCase):

    def test_initialization(self):
        # Test for correct initialization
        variables = [(0, 5), (-1, 7), (2, 8)]
        precision = 2
        chromo = Chromosome(number_of_variables=3, precision=precision, variables_list=variables)

        # Check if variables are initialized correctly
        self.assertEqual(chromo.number_of_variables, 3)
        self.assertEqual(chromo.precision, 2)
        self.assertEqual(chromo.variables_list, variables)

    def test_calculate_ranges(self):
        # Test the range calculation
        variables = [(0, 5), (-1, 7), (2, 8)]
        chromo = Chromosome(number_of_variables=3, precision=2, variables_list=variables)

        chromo.calculate_ranges()

        # Check if ranges are calculated correctly
        self.assertEqual(chromo.ranges, [5, 8, 6])

    def test_calculate_number_of_bits(self):
        # Test the bit calculation based on ranges and precision
        variables = [(0, 5), (-1, 7), (2, 8)]
        precision = 2
        chromo = Chromosome(number_of_variables=3, precision=precision, variables_list=variables)

        chromo.calculate_number_of_bits()

        # Check the calculated number of bits for each variable
        expected_bits = [len(bin(int(range_val * pow(10, precision)))[2:]) for range_val in chromo.ranges]
        self.assertEqual(chromo.number_of_bits_variables, expected_bits)

        # Check the total number of bits for the chromosome
        self.assertEqual(chromo.number_of_bits_chromosome, sum(expected_bits))

    def test_empty_variables(self):
        # Test case with empty variables list
        chromo = Chromosome(number_of_variables=0, precision=2, variables_list=[])

        # Should handle gracefully, no ranges or bits
        self.assertEqual(chromo.ranges, [])
        self.assertEqual(chromo.number_of_bits_variables, [])
        self.assertEqual(chromo.number_of_bits_chromosome, 0)

    def test_single_variable(self):
        # Test case with a single variable range
        variables = [(0, 10)]
        precision = 2
        chromo = Chromosome(number_of_variables=1, precision=precision, variables_list=variables)

        chromo.calculate_number_of_bits()

        # Expected bit length for a range of 10, scaled by 10^2
        expected_bits = len(bin(int(10 * pow(10, precision)))[2:])
        self.assertEqual(chromo.number_of_bits_variables, [expected_bits])
        self.assertEqual(chromo.number_of_bits_chromosome, expected_bits)

    def test_negative_range(self):
        # Test case with negative ranges
        variables = [(-5, 5)]
        precision = 3
        chromo = Chromosome(number_of_variables=1, precision=precision, variables_list=variables)

        chromo.calculate_number_of_bits()

        # Expected bit length for a range of 10, scaled by 10^3
        expected_bits = len(bin(int(10 * pow(10, precision)))[2:])
        self.assertEqual(chromo.number_of_bits_variables, [expected_bits])
        self.assertEqual(chromo.number_of_bits_chromosome, expected_bits)

    def test_generate_chromosome(self):
        """Test the generation of a chromosome"""
        variables = [(0, 5), (-1, 7), (2, 8)]
        precision = 2
        chromo = Chromosome(number_of_variables=3, precision=precision, variables_list=variables)

        # Mocking random.randint to always return 0 or 1, for predictable test results
        with patch('random.randint', side_effect=cycle([0, 1])):  # Repeats 0, 1 infinitely
            chromo.generate_chromosome()

            # Check that the length of the chromosome matches the expected number of bits
            self.assertEqual(len(chromo.chromosome), chromo.number_of_bits_chromosome)

            # Check that the chromosome contains only 0s and 1s
            self.assertTrue(all(bit in [0, 1] for bit in chromo.chromosome))

if __name__ == "__main__":
    unittest.main()