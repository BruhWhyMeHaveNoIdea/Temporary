def get_chance(percent):
    import random

    rand = random.random()
    perc = percent / 100
    result = rand < perc
    return result


def print_delay(text, delay=0.02):
    import time

    for char in str(text):
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # перенос строки
