import random
import string

def string_generator(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))
