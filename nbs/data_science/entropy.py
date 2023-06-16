import numpy as np

# logs #################################################################################################################

# understanding intercepts
np.log(np.e), np.log(1)
np.log2(2), np.log(1)


# entropy ##############################################################################################################
# Skewed Probability Distribution (unsurprising): Low entropy.
# Balanced Probability Distribution (surprising): High entropy.


def entropy(probs: np.ndarray) -> float:
    return -sum(probs * np.log2(probs))


coin = np.array([0.5, 0.5])
coin_bias = np.array([0.2, 0.8])
dice = np.ones(6) / 6
dice_8 = np.ones(8) / 8
lottery = np.ones(1_000_000) / 1_000_000

e_coin = round(entropy(coin), 2)
assert e_coin == -(0.5 * np.log2(0.5)) * 2
e_coin_bias = round(entropy(coin_bias), 2)
e_dice = round(entropy(dice), 2)
e_dice_8 = round(entropy(dice_8), 2)
e_lottery = round(entropy(lottery), 2)

print(f"entropy of coin: {e_coin}")
print(f"entropy of coin_bias: {e_coin_bias}")
print(f"entropy of dice: {e_dice}")
print(f"entropy of dice_8: {e_dice_8}")
print(f"entropy of lottery: {e_lottery}")

# 1 bit of information if reducing your uncertaintiy by half
# less information gain for knowing outcome of a know bias coin,
# ie it is less random for the reduction in uncertainity is lower
# higher information gain for knowing outcome of lottery
