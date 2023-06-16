from abc import ABCMeta, abstractmethod


class Animal(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def num_legs(self):
        pass


class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)

    def num_legs(self):
        return 4


class Monkey(Animal):
    def __init__(self, name):
        super().__init__(name)

    def num_legs(self):
        return 2


m = Monkey("jim")
d = Dog("pete")

for i in [m, d]:
    print(i.num_legs())
