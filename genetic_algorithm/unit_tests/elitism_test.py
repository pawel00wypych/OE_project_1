import unittest

from genetic_algorithm.chromosome import Chromosome
from genetic_algorithm.elitism import Elitism


class TestElitism(unittest.TestCase):

    def setUp(self):
        """Setup the initial population for each test"""
        self.population = [Chromosome(number_of_variables=2,
                                      precision=2,
                                      variables_ranges_list=[(0, 10), (5, 15)],
                                      fitness=10),
                           Chromosome(number_of_variables=2,
                                      precision=2,
                                      variables_ranges_list=[(0, 10), (5, 15)],
                                      fitness=30),
                           Chromosome(number_of_variables=2,
                                      precision=2,
                                      variables_ranges_list=[(0, 10), (5, 15)],
                                      fitness=20),
                           Chromosome(number_of_variables=2,
                                      precision=2,
                                      variables_ranges_list=[(0, 10), (5, 15)],
                                      fitness=5),
                           Chromosome(number_of_variables=2,
                                      precision=2,
                                      variables_ranges_list=[(0, 10), (5, 15)],
                                      fitness=15)]
        self.elitism = Elitism(self.population)

    def test_choose_the_best_individuals(self):
        """Test if the best individuals are chosen correctly"""
        self.elitism.choose_the_best_individuals()
        self.assertEqual(self.elitism.best_fitness_val, 30)
        self.assertEqual(len(self.elitism.elite_individuals), self.elitism.number_of_elites)
        self.assertEqual(self.elitism.elite_individuals[0].fitness, 30)  # Best individual

    def test_configure_num_of_elite(self):
        """Test the number of elite individuals based on population size"""
        elitism_small_pop = Elitism([Chromosome(number_of_variables=2,
                                      precision=2,
                                      variables_ranges_list=[(0, 10), (5, 15)],
                                                fitness=1) for _ in range(10)])
        elitism_medium_pop = Elitism([Chromosome(number_of_variables=2,
                                      precision=2,
                                      variables_ranges_list=[(0, 10), (5, 15)],
                                                 fitness=1) for _ in range(50)])
        elitism_large_pop = Elitism([Chromosome(number_of_variables=2,
                                      precision=2,
                                      variables_ranges_list=[(0, 10), (5, 15)],
                                                fitness=1) for _ in range(200)])

        self.assertEqual(elitism_small_pop.number_of_elites, 1)
        self.assertEqual(elitism_medium_pop.number_of_elites, 2)  # 50 // 20
        self.assertEqual(elitism_large_pop.number_of_elites, 13)  # 200 // 15

    def test_set_new_population(self):
        """Test setting a new population"""
        new_population = [Chromosome(number_of_variables=2,
                                      precision=2,
                                      variables_ranges_list=[(0, 10), (5, 15)],
                                     fitness=50),
                          Chromosome(number_of_variables=2,
                                      precision=2,
                                      variables_ranges_list=[(0, 10), (5, 15)],
                                     fitness=100)]
        self.elitism.set_new_population(new_population)
        self.assertEqual(len(self.elitism.population), 2)
        self.assertEqual(self.elitism.population[0].fitness, 50)
        self.assertEqual(self.elitism.population[1].fitness, 100)

    def test_get_elite_list(self):
        """Test if the elite list is returned correctly"""
        self.elitism.choose_the_best_individuals()
        elite_list = self.elitism.get_elite_list()
        self.assertEqual(len(elite_list), self.elitism.number_of_elites)
        self.assertEqual(elite_list[0].fitness, 30)  # Best individual


if __name__ == '__main__':
    unittest.main()
