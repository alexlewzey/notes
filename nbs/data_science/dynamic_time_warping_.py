from __future__ import annotations

import pandas as pd
import plotly.express as px
from plotly.offline import plot
from sklearn import metrics
from tqdm import tqdm
from tslearn.clustering import TimeSeriesKMeans
from tslearn.datasets import UCR_UEA_datasets

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)
pd.set_option("display.float_format", "{:.3f}".format)

x, y_train, x_test, y_test = UCR_UEA_datasets().load_dataset("TwoPatterns")
x = x[..., 0]

data = []
for i in tqdm(range(5, 31, 5)):
    model = TimeSeriesKMeans(
        n_clusters=i, metric="dtw", max_iter=10, random_state=5, n_jobs=-1
    )
    model.fit(x)
    score = metrics.silhouette_score(x, model.labels_)
    data.append([i, score])
ts = (
    pd.DataFrame(data, columns=["score", "i"])
    .reset_index()
    .rename(columns={"index": "time"})
)
fig = px.line(ts, "time", "score")
plot(fig)

columns = [f"t{i}" for i in range(x.shape[1])]
df = pd.DataFrame(x, columns=columns).reset_index().rename(columns={"index": "series"})
df["label"] = model.labels_

melt = df.melt(id_vars=["series", "label"], var_name="time")
fig = px.line(melt, "time", "value", color="series")
plot(fig)
