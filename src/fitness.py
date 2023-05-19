def dummy(a: list) -> int:
    return sum(a)

class Fitness:
    tonality_intervals = [0, 2, 4, 5, 7, 9, 11]
    perfect_consonants = [0, 5, 7, 12]
    imperfect_consonants = [2, 4, 9, 11]
    seconds = [1, 2]
    sevenths = [10, 11]

    def __init__(self, mode : int, tempo : int, stop_tone : int, extend_tone : int, 
                 alpha: float, beta : float, garmma : float, reference_tone : list,
                 reference_prefix : int):
        self.mode : int = mode
        self.tempo : int = tempo
        self.stop_tone : int = stop_tone
        self.extend_tone : int = extend_tone
        self.alpha : float = alpha
        self.beta : float = beta
        self.garmma :float = garmma

        # TODO: zeta, eta
        self.zeta = [1.0, 1.0, 1.0, 1.0] 
        self.eta = [0.0, 0.2, 0.2, 0.0]

        # self.values = [1, 3, 1, 3, 5]
        self.values = [1, 2, 3, 3, 5]

        # self.reference_tone : list = reference_tone
        ref_intervals = self.get_intervals(reference_tone, reference_prefix)
        ref_values = self.intervals_value(ref_intervals)
        ref_mu, ref_sigma = self.calc_avg_sigma2(ref_values)
        self.ref_mu = ref_mu
        self.ref_sigma = ref_sigma
        
    def get_intervals(self, tone: list, prefix: int) -> list:
        last_tone = 0
        intervals = []
        if(prefix):
            bar_intervals = []
            for i in range(prefix):
                if(tone[i] == self.stop_tone or tone[i] == self.extend_tone):
                    continue
                if(last_tone == 0):
                    if(tone[i] != 0):
                        last_tone = tone[i]
                    continue
                bar_intervals.append(tone[i] - last_tone)
                last_tone = tone[i]
            if(len(bar_intervals)):
                intervals.append(bar_intervals)
        for i in range(prefix, len(tone), self.tempo):
            bar_intervals = []
            bar = tone[i:i + self.tempo]
            for each_tone in bar:
                if(each_tone == self.stop_tone or each_tone == self.extend_tone):
                    continue
                if(last_tone == 0):
                    if(each_tone != 0):
                        last_tone = each_tone
                    continue
                bar_intervals.append(each_tone - last_tone)
                last_tone = each_tone
            if(len(bar_intervals)):
                intervals.append(bar_intervals)
        return intervals
                
    def single_interval_value(self, interval: int):
        if(interval in self.perfect_consonants):
            return self.values[0]
        if(interval in self.imperfect_consonants):
            return self.values[1]
        if(interval in self.seconds):
            return self.values[2]
        if(interval in self.sevenths):
            return self.values[3]
        return self.values[4]
    
    def intervals_value(self, intervals: list):
        ret = []
        for each in intervals:
            val = []
            for tone in each:
                val.append(self.single_interval_value(abs(tone)))
            ret.append(val)
        return ret

    def stat_info_of_bar(self, bar_intervals: list):
        # interval_values = [abs(i) for i in intervals]
        avg = sum(bar_intervals) / len(bar_intervals)
        sigma2 = sum([(i - avg)**2 for i in bar_intervals]) / len(bar_intervals)
        return avg, sigma2
    
    def calc_avg_sigma2(self, intervals: list):
        avgs = []
        sigma2s = []
        for each in intervals:
            avg, sigma2 = self.stat_info_of_bar(each)
            avgs.append(avg)
            sigma2s.append(sigma2)
        return avgs, sigma2s

    def if_bad_tone(self, tone: int) -> bool:
        if tone == self.stop_tone or tone == self.extend_tone:
            return False
        interval = (tone - self.mode) % 12
        if interval in self.tonality_intervals:
            return False
        return True

    def badtone(self, a: list):
        return sum([self.if_bad_tone(a[i]) for i in range(len(a))]) + 1

    def interval_consonants(self, a: list) -> float:
        ret : float = 0.0
        for i in range(len(a)):
            ret += (self.ref_mu[i] - a[i]) * self.zeta[i]
        return ret

    def variance(self, b: list) -> float:
        ret : float = 0.0
        for i in range(len(b)):
            ret += (self.ref_sigma[i] - b[i]) * self.eta[i]
        return ret

    def fitness(self, tone: list, prefix: int) -> float:
        intervals = self.get_intervals(tone, prefix)
        intervals_values = self.intervals_value(intervals)
        avgs, sigma2s = self.calc_avg_sigma2(intervals_values)

        return self.alpha * self.interval_consonants(avgs) + self.beta * self.variance(sigma2s) + self.garmma / self.badtone(tone)

if __name__ == "__main__":
    a = [1, 3, 5, 6, 8, 10]
    f = Fitness(1, 4, 0, 0, 1.0, 1.0, 1.0, a, 0)
    print(f.fitness(a, 0))
