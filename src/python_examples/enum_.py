from enum import Enum


class Sauce(Enum):
    BARBEQUE = 1
    SWEET_CURRY = 2
    KETCHUP = 3


sauce = Sauce.BARBEQUE

if sauce == Sauce.BARBEQUE:
    print("Its barb!")
