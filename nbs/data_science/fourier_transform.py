import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import scipy
from plotly.offline import plot

plt.ioff()

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)
pd.options.display.float_format = "{:,.4f}".format


def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = np.sin((2 * np.pi) * frequencies)
    return x, y


# how many measurements per second
SAMPLE_RATE: int = 44_100
# how many seconds
DURATION: int = 5

_, nice_tone = generate_sine_wave(400, SAMPLE_RATE, DURATION)
_, noise_tone = generate_sine_wave(4000, SAMPLE_RATE, DURATION)
noise_tone = noise_tone * 0.3

mixed_tone = nice_tone + noise_tone
normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)

df = pd.DataFrame({"x": range(len(normalized_tone)), "y": normalized_tone})
fig = px.line(df, "x", "y", range_x=(0, 200))
plot(fig)

yf = scipy.fft.rfft(normalized_tone)
xf = scipy.fft.rfftfreq(df.shape[0], 1 / SAMPLE_RATE)
dff = pd.DataFrame({"yf": np.abs(yf), "xf": xf})
dff["pct"] = dff["yf"] / dff["yf"].sum()
fig = px.line(dff, "xf", "yf")
plot(fig)
points_per_freq = len(xf) / (SAMPLE_RATE / 2)
target_idx = int(points_per_freq * 4000)
print(points_per_freq, target_idx)
dff["yf_human"] = dff["yf"]
dff.iloc[target_idx, -1] = 0
df["y_human"] = scipy.fft.irfft(dff["yf_human"].values)

fig = px.line(df, "x", "y_human", range_x=(0, 200))
plot(fig)
