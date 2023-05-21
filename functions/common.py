import string
import random
from random import randint

def random_str_generate(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def random_number():
    return randint(100000, 999999)