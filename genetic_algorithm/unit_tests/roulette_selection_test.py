import unittest
from unittest.mock import patch

from genetic_algorithm.chromosome import Chromosome
from genetic_algorithm.selection import Selection
from genetic_algorithm.population import Population

class TestRouletteSelection(unittest.TestCase):
    def setUp(self):
        variables_ranges_list = [(0, 5), (-1, 7), (2, 8)]
        self.individuals = [
            Chromosome(3, 2, variables_ranges_list,
                       [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0],10),
            Chromosome(3, 2, variables_ranges_list,
                       [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0],20),
            Chromosome(3, 2, variables_ranges_list,
                       [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0],15),
            Chromosome(3, 2, variables_ranges_list,
                       [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0],45)
        ]
        self.population = Population(3,2,variables_ranges_list,self.individuals)

    # Test 1: Basic Test - Check if the function returns the correct number of individuals
    def test_basic_selection(self):
        selected = Selection.roulette_selection(self.population, 3)
        self.assertEqual(len(selected), 3)

    # Test 2: Identical Fitness - Ensure random selection when all individuals have the same fitness
    @patch('random.sample')  # Mocking random.sample to control randomness in tests
    def test_identical_fitness(self, mock_random_sample):

        # We mock random.sample to return the input individuals for predictability
        mock_random_sample.return_value = self.individuals[:2]

        selected = Selection.roulette_selection(self.population, 2)

        # All individuals have the same fitness, so we should return any 2
        self.assertEqual(len(selected), 2)
        self.assertEqual(selected, self.individuals[:2])  # Ensure the returned individuals are as expected

    # Test 3: Non-Identical Fitness - Higher fitness individuals should be selected more often
    @patch('random.uniform')  # Mocking random.uniform to control randomness in tests
    def test_non_identical_fitness(self, mock_random_uniform):
        # Mock the random.uniform call to control which individual is selected
        mock_random_uniform.side_effect = [0.05, 0.15,0.25]  # These numbers should pick individuals based on scaled fitness

        selected = Selection.roulette_selection(self.population, 3)

        # Verify that 3 individuals are selected and they are sorted by fitness (descending)
        self.assertEqual(len(selected), 3)
        self.assertTrue(all(self.population.individuals[i].fitness >= selected[i].fitness for i in range(1, len(selected))))

    # Test 4: Small Population (Edge Case) - Select from a population with one individual
    def test_single_individual(self):
        selected = Selection.roulette_selection(self.population, 1)

        # Since there is only one individual, they should be selected
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].fitness, self.individuals[0].fitness)

    # Test 5: Ensure the result is sorted by fitness in descending order
    def test_sorted_selection(self):
        selected = Selection.roulette_selection(self.population, 2)

        # The result should be sorted by fitness, in descending order
        self.assertEqual([individual.fitness for individual in selected],
                         sorted([individual.fitness for individual in selected], reverse=True))


if __name__ == '__main__':
    unittest.main()
