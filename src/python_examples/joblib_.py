import math
import time

import joblib
from tqdm import tqdm

n = 10_000
func = math.factorial


def func(i):
    time.sleep(0.3)
    return i


n = 20

start = time.time()
a = [func(i) for i in tqdm(range(n))]
print(time.time() - start)

start = time.time()
b = joblib.Parallel(n_jobs=-1)(joblib.delayed(func)(i) for i in range(n))
print(time.time() - start)

start = time.time()
with joblib.parallel_backend(backend="threading"):
    c = joblib.Parallel()(joblib.delayed(func)(i) for i in range(n))
print(time.time() - start)
