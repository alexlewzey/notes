import numpy as np
import optuna
import pandas as pd
import plotly.express as px
from optuna import Trial
from plotly.offline import plot


class Bandit:
    def __init__(self, p):
        self.p = p

    def __repr__(self):
        return f"Bandit(p={self.p})"

    def pull(self):
        return 1 if np.random.rand() <= self.p else 0


bandits = [Bandit(p) for p in (0.2, 0.6, 0.7, 0.3)]
bandits = dict(zip("abcd", bandits))


def objective(trial: Trial):
    bandit_name = trial.suggest_categorical("bandit", ["a", "b", "c", "d"])
    result = bandits[bandit_name].pull()
    return result


study_name = "example-study"
storage_name = f"sqlite:///{study_name}.db"
study = optuna.create_study(
    direction="maximize",
    study_name=study_name,
    storage=storage_name,
    load_if_exists=True,
)
n_trials = 2000
study.optimize(objective, n_trials=n_trials)

print(study.best_params)

# distribution of categories by n trials
n_trials = range(0, n_trials, 200)
data = []
for n in n_trials:
    params = [trial.params["bandit"] for trial in study.trials[n : n + 100]]
    params = pd.Series(params).value_counts().to_frame("counts").reset_index()
    params["pct"] = params["counts"] / params["counts"].sum()
    params["n"] = n
    data.append(params)
data = pd.concat(data)
fig = px.bar(data, "n", "pct", color="index")
plot(fig)
