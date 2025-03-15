import unittest

from genetic_algorithm.chromosome import Chromosome
from genetic_algorithm.mutation import Mutation


class TestMutation(unittest.TestCase):

    def setUp(self):
        self.population = [
            Chromosome(number_of_variables=2,
                       precision=2,
                       variables_ranges_list=[(0, 10), (5, 15)],
                       chromosome=[1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0])
        ]
        self.mutation_probability = 1.0

    def test_single_point_mutation(self):
        mutation = Mutation(self.population, mutation_probability=1.0)
        original_chromosome = self.population[0].chromosome.copy()

        mutated_population = mutation.single_point_mutation()
        mutated_chromosome = mutated_population[0].chromosome

        diff = [i for i in range(len(original_chromosome)) if original_chromosome[i] != mutated_chromosome[i]]
        # assertEqual(2,...) - because there are 2 variables in chromo and mut_probability = 1
        self.assertEqual(2, len(diff), "One-point mutation should change exactly one bit in variable bits")

    def test_two_point_mutation(self):
        mutation = Mutation(self.population, mutation_probability=1.0)
        original_chromosome = self.population[0].chromosome.copy()

        mutated_population = mutation.two_point_mutation()
        mutated_chromosome = mutated_population[0].chromosome

        diff = [i for i in range(len(original_chromosome)) if original_chromosome[i] != mutated_chromosome[i]]
        # assertEqual(4,...) - because there are 2 variables in chromo and mut_probability = 1 and
        # its two point mutation -> 2 x 2 = 4
        self.assertEqual(4, len(diff), "Two-point mutation should change exactly two bits in variable bits")

    def test_edge_mutation(self):
        mutation = Mutation(self.population, mutation_probability=1.0)
        original_chromosome = self.population[0].chromosome.copy()

        mutated_population = mutation.edge_mutation()
        mutated_chromosome = mutated_population[0].chromosome

        diff = [i for i in range(len(original_chromosome)) if original_chromosome[i] != mutated_chromosome[i]]

        expected_positions = [0, 9, 10, 19]  # edge indexes
        self.assertTrue(all(pos in expected_positions for pos in diff),
                        "edge mutation should change only edge bits")

    def test_mutation_probability(self):
        mutation = Mutation(self.population, mutation_probability=0.0)
        original_chromosome = self.population[0].chromosome.copy()

        mutated_population = mutation.single_point_mutation()
        mutated_chromosome = mutated_population[0].chromosome

        self.assertEqual(original_chromosome, mutated_chromosome,
                         "mutation_probability = 0 chromosome shoudn't change")


if __name__ == '__main__':
    unittest.main()
