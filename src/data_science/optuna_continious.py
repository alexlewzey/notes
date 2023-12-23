from __future__ import annotations

import optuna
import pandas as pd
from optuna import Trial

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)
pd.set_option("display.float_format", "{:.3f}".format)


def ground_truth(i):
    if i < 500:
        return 1
    else:
        return 0


study_name = "example-study"
study = optuna.create_study(
    direction="maximize",
    study_name=study_name,
    load_if_exists=True,
)
n_trials = 1000


def objective(study: Trial):
    i = study.suggest_int("i", 0, 10_000)
    return (ground_truth(i) * 10_000) + i


study.optimize(objective, n_trials=n_trials)

print(study.best_params)
