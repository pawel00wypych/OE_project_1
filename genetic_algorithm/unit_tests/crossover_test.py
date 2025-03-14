import unittest
from genetic_algorithm.crossover import Crossover
from genetic_algorithm.chromosome import Chromosome
import random

class TestCrossover(unittest.TestCase):
    def setUp(self):
        variables_ranges_list = [(0, 5), (-1, 7), (2, 8)]
        self.population = [
            Chromosome(3, 2, variables_ranges_list,
                       [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0]),
            Chromosome(3, 2, variables_ranges_list,
                       [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0]),
            Chromosome(3, 2, variables_ranges_list,
                       [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0]),
            Chromosome(3, 2, variables_ranges_list,
                       [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0])
        ]
        self.crossover = Crossover(self.population, 0.8)

    def test_single_point_crossover(self):
        new_population = self.crossover.single_point_crossover()
        self.assertEqual(len(new_population), len(self.population))

    def test_two_point_crossover(self):
        new_population = self.crossover.two_point_crossover()
        self.assertEqual(len(new_population), len(self.population))

    def test_uniform_crossover(self):
        new_population = self.crossover.uniform_crossover()
        self.assertEqual(len(new_population), len(self.population))

    def test_granular_crossover(self):
        new_population = self.crossover.granular_crossover()
        self.assertEqual(len(new_population), len(self.population))

    def test_decide_to_crossover(self):
        random.seed(1)
        self.assertTrue(self.crossover.decide_to_crossover())

    def test_decide_not_to_crossover(self):
        crossover = Crossover(self.population, 0.0)
        self.assertFalse(crossover.decide_to_crossover())

    def test_cross_chromosomes(self):
        chromo1 = self.population[0]
        chromo2 = self.population[1]
        new_chromo1, new_chromo2 = self.crossover.cross_chromosomes(chromo1, chromo2, 1)
        self.assertEqual(new_chromo1.chromosome, [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0])
        self.assertEqual(new_chromo2.chromosome, [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0])


    def test_create_new_chromosomes(self):
        chromo1 = self.population[0]
        chromo2 = self.population[1]
        new_genes1 = [1, 1, 1]
        new_genes2 = [0, 0, 0]
        new_chromo1, new_chromo2 = self.crossover.create_new_chromosomes(chromo1, chromo2, new_genes1, new_genes2)
        self.assertEqual(new_chromo1.chromosome, new_genes1)
        self.assertEqual(new_chromo2.chromosome, new_genes2)

if __name__ == '__main__':


    unittest.main()
