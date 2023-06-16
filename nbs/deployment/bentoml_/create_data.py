from pathlib import Path

import pandas as pd
from sklearn.datasets import make_classification

root = Path(__file__).parent
dir_data = root / "data"
dir_data.mkdir(exist_ok=True)

# Generate the data
n_samples, n_features = 10000, 7
X, y = make_classification(n_samples=n_samples, n_features=n_features, n_informative=5)

# Save it as a CSV
feature_names = [f"feature_{i}" for i in range(n_features)]
df = pd.DataFrame(X, columns=feature_names)
df["target"] = y

df.to_csv(dir_data / "data.csv", index=False)
