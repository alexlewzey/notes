"""Training and saving tensorflow model for making predictions."""
import json

import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.models import Model

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)


def plotly_multicol_line(df: pd.DataFrame) -> go.Figure:
    """Plot time series where each column corresponds to a separate series and the index
    are the dates."""
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col))
    return fig


iris = sns.load_dataset("iris")

X = iris.iloc[:, :4]
y = iris.iloc[:, -1].astype("category")
mapping = dict(enumerate(y.cat.categories))
y = y.cat.codes
K = len(set(y))

i = Input(shape=(X.shape[1]))
x = Dense(200, activation="relu")(i)
x = Dense(50, activation="relu")(x)
x = Dense(K, activation="softmax")(x)

model = Model(i, x)
model.compile(
    optimizer="adam", loss=SparseCategoricalCrossentropy(), metrics=["accuracy"]
)
r = model.fit(X, y, epochs=100)

# results = pd.DataFrame(r.history)
# fig = plotly_multicol_line(results)
# plot(fig)

with open("mapping.json", "w") as f:
    json.dump(mapping, f)
model.save("flower_classifier")
