import random


class Util:
    @staticmethod
    def shuffle_the_list(lst: list) -> list:
        random.shuffle(lst)
        return lst
