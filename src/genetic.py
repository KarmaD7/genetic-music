import random
import logging
from music21 import *
from functools import reduce
from fitness import dummy
from musicio import get_music_lists, write_musicxml

M = 100
N = 10

LOW_PITCH = 1
HIGH_PITCH = 48
ALPHA = 4000

# TODO: encode chord

class GeneticRunner(object):
    def __init__(self, pcross: float, pmutation: float, music_len: int) -> None:
        self.pcross = 1
        self.pmutation = 0.01
        self.music_len = 32
        self.population_size = 10
        self.rosseta_prob = []
        # self
        self.now_population = get_music_lists()
        self.next_population = []
        self.best_id = -1
        self.fitness = dummy # func, todo
        # the following variables are intermidiate variables in member functions.
        # we define them here to reduce the time for malloc.
        self.crossovered = [False, False]
        self.chosen_music = []

    def read_music(self) -> list:
        return get_music_lists()
        # self.now_population = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]

    def output_music(self) -> None:
        # logging.info(f"choose idx {self.best_id} music {self.now_population[self.best_id]}")
        # step 2. output
        print("output")
        print(sum(self.now_population[self.best_id]))
        write_musicxml(self.now_population[self.best_id])

    def find_max_fitness(self) -> int:
        population_fitness = list(map(self.fitness, self.now_population))
        max_fitness = max(population_fitness)
        self.best_id = population_fitness.index(max_fitness)
        logging.info(f"choose idx {self.best_id} music {self.now_population[self.best_id]} max fitness {max_fitness}")
        return max_fitness

    def rossetta(self) -> None:
        '''
        choose a new population of population_size
        '''
        self.chosen_music.clear()
        # logging.info(rosseta_prob)
        # print(self.now_population)
        fitness_sum = sum(map(lambda x: self.fitness(x), self.now_population))
        # print(fitness_sum)
        rosseta_prob = list(map(lambda x: self.fitness(x) / fitness_sum, self.now_population))
        logging.info(rosseta_prob)
        # Maybe TODO: more pythonic
        for _ in range(self.population_size):
            r = random.random()
            prefix_prob = 0
            for music, prob in zip(self.now_population, rosseta_prob):
                if prefix_prob < r < prefix_prob + prob:
                    self.chosen_music.append(music[:])
                    break
                prefix_prob += prob

    def crossover(self, a: list, b: list) -> None:
        '''
        cross over a and b in place.
        '''
        cross_pos = random.randint(1, self.music_len - 1) # [cross_pos, music_len - 1] will be crossed
        logging.info("cross pos is {}".format(cross_pos))
        a[cross_pos:], b[cross_pos:] = b[cross_pos:], a[cross_pos:]
        return
        # pass

    def mutation(self, a: list) -> None:
        '''
        mutation on a in place.
        '''
        mutation_pos = random.randint(0, self.music_len - 1)
        logging.info("mutation pos is {}".format(mutation_pos))
        a[mutation_pos] = random.randint(LOW_PITCH, HIGH_PITCH)

    def translate(self, a: list) -> None:
        pass

    def reflect(self, a: list) -> None:
        pass

    def reverse(self, a: list) -> None:
        pass

    def step(self) -> bool:
        '''
        A step will generate the next generation.
        Return value: if a good music exists
        '''
        # step 1: choose
        self.rossetta()
        # step 2: crossover
        self.next_population.clear()
        self.crossovered =  [False] * len(self.chosen_music)
        for i, music in enumerate(self.chosen_music):
            logging.info("i {} music {}".format(i, music))
            # logging.info(self.chosen_music)
            if self.crossovered[i]:
                continue

            r = random.random()
            if r < self.pcross:
                # TODO: 
                mate = random.randint(i + 1, self.population_size - 1)
                while self.crossovered[mate]:
                    mate = random.randint(i + 1, self.population_size - 1)
                self.crossover(self.chosen_music[i], self.chosen_music[mate])
                self.crossovered[i], self.crossovered[mate] = True, True
                self.next_population.append(self.chosen_music[i])
                self.next_population.append(self.chosen_music[mate])
            else:
                self.next_population.append(self.chosen_music[i])
        # step 3: mutation (or other transforms)
        for music in self.next_population:
            r = random.random()
            if r < self.pmutation:
                self.mutation(music)
        logging.info("next generation: {}".format(self.next_population))
        self.now_population = self.next_population[:]
        return self.find_max_fitness() >= ALPHA

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    runner = GeneticRunner(1, 0.01, 5)
    runner.read_music()
    for i in range(M):
        logging.warning(f"epoch {i}")
        if runner.step():
            break
    runner.output_music()
    #     print(i)