import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy


class FourierTransformer:
    one_day_frequency = 1 / (60 * 60 * 24)

    def __init__(self, window_size: int, n_harmonics: int = 5):
        self.window_size = window_size
        self.seconds_per_window = self.window_size * 60
        self.n_harmonics = n_harmonics
        self.human_frequencies: list[float] = None
        self.human_frequency_idxs: list[int] = None
        self.dff: pd.DataFrame = None

    @staticmethod
    def _find_idx_of_nearest_value(array: np.ndarray, value: float) -> int:
        return np.argmin(np.abs(array - value))

    def fit_predict(self, x: np.ndarray) -> np.ndarray:
        rows_per_day = (24 * 60) / self.window_size
        remainder = x.shape[0] % rows_per_day
        assert remainder == 0, (
            f"fft requires complete cycles i.e. no. of rows must be multiple"
            f" of {rows_per_day:.0f}. Current remainder={remainder}"
        )

        yf = np.fft.rfft(x)
        xf = np.fft.rfftfreq(x.shape[0], self.seconds_per_window)
        self.dff = pd.DataFrame({"xf": xf, "yf_abs": np.abs(yf), "yf": yf})

        self.human_frequencies = [
            self.one_day_frequency * i for i in range(self.n_harmonics)
        ]
        self.human_frequency_idxs = [
            self._find_idx_of_nearest_value(self.dff["xf"].values, f)
            for f in self.human_frequencies
        ]
        self.dff["y_pred"] = np.where(
            self.dff.index.isin(self.human_frequency_idxs), self.dff["yf"], 0j
        )
        y_pred = scipy.fft.irfft(self.dff["y_pred"].values)
        return y_pred

    def plot_power_spectrum(self) -> go.Figure:
        title = "power spectrum (with 24 hour frequency harmonics)"
        fig = px.line(self.dff, "xf", "yf_abs", title=title)
        for f in self.human_frequencies:
            fig.add_vline(f, line_dash="dash", line_color="red")
        return fig
