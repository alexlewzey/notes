import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

pts1 = np.array([1, 2, 3])
pts2 = np.array([0, 5, 8])
pts3 = np.random.rand(3, 3)


# euclidean distance
eu_np = np.linalg.norm(pts2 - pts1)
eu_sk = euclidean_distances(pts1.reshape(1, -1), pts2.reshape(1, -1))

print(eu_np, eu_sk)


eu_np = np.linalg.norm(pts2 - pts1)
eu_sk = euclidean_distances(pts1.reshape(1, -1), pts3)

print(eu_np, eu_sk)

# cosine similarity
sim_np = pts1 @ pts2 / (np.sqrt(pts1 @ pts1) * np.sqrt(pts2 @ pts2))
sim_sk = cosine_similarity(pts1.reshape(1, -1), pts2.reshape(1, -1))

print(sim_np, sim_sk)
