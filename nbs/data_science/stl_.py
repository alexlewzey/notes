import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from statsmodels.nonparametric.smoothers_lowess import lowess

# create example time-series with noise
np.random.seed(123)
dates = pd.date_range(start="2022-01-01", end="2022-12-31", freq="D")
values = np.sin(np.linspace(0, 2 * np.pi, len(dates))) + np.random.normal(
    0, 0.2, len(dates)
)
ts = pd.Series(data=values, index=dates)

# apply lowess smoothing to the time-series
smooth_values = lowess(ts.values, ts.index.values, frac=0.1)

# create dataframe for plotting
df = pd.DataFrame(
    {"date": ts.index, "value": ts.values, "smoothed": smooth_values[:, 1]}
)

# plot the results
fig = px.line(
    df, x="date", y=["value", "smoothed"], labels={"date": "Date", "value": "Value"}
)
plot(fig)
