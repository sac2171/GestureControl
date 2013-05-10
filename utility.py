import string
import random

def rand_string(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for x in range(size))