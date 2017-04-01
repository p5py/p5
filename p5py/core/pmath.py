import math
import random as rnd

def random(high=1, low=0):
    return rnd.uniform(low, high)

def random_seed(seed):
    return rnd.seed(seed)

def random_gaussian(mean=0, sdev=1):
    return rnd.gauss(mu=mean, sigma=sdev)
