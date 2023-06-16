import matplotlib.pyplot as plt
import ruptures as rpt

# Generate some random data with two different means
n_samples, dim, sigma = 1000, 1, 1
n_bkps, sigma_noise = 2, 1
signal, bkps = rpt.pw_constant(n_samples, dim, n_bkps, noise_std=sigma_noise)

# Perform change point detection using the Pelt algorithm
algo = rpt.Pelt(model="rbf").fit(signal)
result = algo.predict(pen=10)

# Plot the results
rpt.display(signal, bkps, result)
plt.show()
