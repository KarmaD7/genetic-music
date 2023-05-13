import random
import logging
from functools import reduce
from fitness import dummy

M = 100
N = 10

LOW_PITCH = 1
HIGH_PITCH = 14


# TODO: encode chord

class GeneticRunner(object):
    def __init__(self, pcross: float, pmutation: float, music_len: int) -> None:
        self.pcross = 1
        self.pmutation = 0.01
        self.music_len = 5
        self.population_size = 2
        self.rosseta_prob = []
        self.now_population = [[1, 2, 7, 8, 9], [5, 6, 2, 3, 4]]
        self.next_population = []
        self.fitness = dummy # func, todo
        # the following variables are intermidiate variables in member functions.
        # we define them here to reduce the time for malloc.
        self.crossovered = [False, False]
        self.chosen_music = []

    def read_music(self) -> None:
        pass
        # self.now_population = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]

    def output_music(self) -> None:
        print(0)

    def rossetta(self) -> None:
        '''
        choose a new population of population_size
        '''
        self.chosen_music.clear()
        # logging.info(rosseta_prob)
        rosseta_prob = list(map(lambda x: self.fitness(x) / reduce(lambda x, y: self.fitness(x) + self.fitness(y), self.now_population), self.now_population))
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
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    runner = GeneticRunner(1, 0.01, 5)
    runner.read_music()
    for _ in range(M):
        if runner.step():
            break
    runner.output_music()
    #     print(i)