import uuid
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (confusion_matrix, f1_score, precision_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)


def create_plot_path() -> str:
    plot_dir = Path().home() / ".plotly"
    plot_dir.mkdir(exist_ok=True)
    return (plot_dir / (str(uuid.uuid4()) + ".html")).as_posix()


def prediction_uncertainty(x, y, n_neighbors=21):
    nn = NearestNeighbors(n_neighbors=n_neighbors)
    nn.fit(x)
    distances, indices = nn.kneighbors(x)
    stds = []
    for i in range(indices.shape[0]):
        idxs = indices[i, 1:].tolist()
        std = y[idxs].std()
        stds.append(std)
    return stds


def random_forest_uncertainty(rf, x) -> np.ndarray:
    trees = np.array([tree.predict_proba(x)[:, -1] for tree in rf.estimators_]).T
    return trees.std(1)


def make_classification_data():
    """Synthetic binary classification dataset."""
    data, targets = datasets.make_classification(
        n_samples=100_000,
        n_features=20,
        n_informative=5,
        n_redundant=7,
        n_clusters_per_class=2,
        # weights=[0.95],
        weights=[0.6],
        flip_y=0.0,
        class_sep=2,
    )
    return data, targets


x, y = make_classification_data()
feature_columns = [f"f{i}" for i in range(x.shape[1])]
target_column = "y"
df = pd.DataFrame(x, columns=feature_columns)
df[target_column] = pd.Series(y)

# classification #######################################################################################################

train, test = train_test_split(df, test_size=0.3, random_state=42)
valid, test = train_test_split(test, test_size=0.5, random_state=42)
train["set"] = "train"
valid["set"] = "valid"
test["set"] = "test"
df = pd.concat([train, valid, test])
print(train.shape, valid.shape, test.shape)

predictions = []

fit_params = {
    "early_stopping_rounds": 10,
    "eval_set": (valid[feature_columns], valid[target_column]),
}
m = lgb.LGBMClassifier(n_estimators=500)
m.fit(train[feature_columns], train[target_column], **fit_params)

df["pred"] = m.predict(df[feature_columns])
df["prob"] = m.predict_proba(df[feature_columns])[:, 1]

# uncertainty
res = [
    m.predict_proba(df[feature_columns], start_iteration=i, num_iteration=1)[:, 1]
    for i in range(m.best_iteration_ + 1)
]
res = np.array(res).T
df["std"] = res.std(1)
df["p10"] = np.quantile(res, 0.1, axis=1)
df["p90"] = np.quantile(res, 0.9, axis=1)

# quantiles = [
#     ('75', 0.75),
#     ('25', 0.25),
# ]
# probs = ['prob'] + [f'prob{s}' for s, _ in quantiles]
# for s, v in quantiles:
#     m = lgb.LGBMClassifier(n_estimators=500, objective='quantile', metric='quantile', alpha=v)
#     m.fit(train[feature_columns], train[target_column], **fit_params)
#     df[f'pred{s}'] = m.predict(df[feature_columns])
#     df[f'prob{s}'] = m.predict_proba(df[feature_columns])[:, 1]
# df['prob_var'] = df[probs[-1]] - df[probs[1]]


norm = StandardScaler().fit_transform(df[feature_columns])
stds = prediction_uncertainty(norm, df["prob"].values)
df["stds"] = stds

# evaluation ###########################################################################################################

results = []
for set_ in ["train", "valid", "test"]:
    subset = df[df["set"] == set_]
    f1 = f1_score(subset[target_column], subset["pred"])
    precision = precision_score(subset[target_column], subset["pred"])
    recall = recall_score(subset[target_column], subset["pred"])
    tp, fp, fn, tn = confusion_matrix(subset[target_column], subset["pred"]).ravel()
    auc = roc_auc_score(subset[target_column], subset["prob"])
    eval_metrics = {
        "set": set_,
        "f1": f1,
        "precision": precision,
        "recall": recall,
        "auc": auc,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
    }
    results.append(eval_metrics)
results = pd.DataFrame(results)

# ys = ['y'] + probs
# for c in ys:
#     df[c] = df[c].astype(str)

# eda ##################################################################################################################

df["y"] = df["y"].astype(str)

pipe = Pipeline([("scale", StandardScaler()), ("pca", PCA(n_components=3))])

x_pca = pipe.fit_transform(x)
for i in range(x_pca.shape[1]):
    df[f"r{i}"] = x_pca[:, i]
pipe.named_steps["pca"].explained_variance_ratio_.sum()

fig = px.scatter(df, "r0", "r1", color="y")
plot(fig)

fig = px.scatter_3d(df, "r0", "r1", "r2", color="y")
fig.update_traces(marker=dict(size=3))
plot(fig)

# for c in ys:
#     fig = px.scatter(df, 'r0', 'r1', color=c, opacity=0.6, title=c)
#     fig.update_traces(marker={'size': 3})
#     plot(fig, filename=create_plot_path())

fig = px.scatter_3d(df.query('set == "test"'), "r0", "r1", "r2", color="y")
fig.update_traces(marker={"size": 2})
plot(fig, filename=create_plot_path())

fig = px.scatter_3d(df.query('set == "test"'), "r0", "r1", "r2", color="stds")
fig.update_traces(marker={"size": 2})
plot(fig, filename=create_plot_path())

fig = px.scatter_3d(df.query('set == "test"'), "r0", "r1", "r2", color="prob")
fig.update_traces(marker={"size": 2})
plot(fig, filename=create_plot_path())

# melt = df.melt(id_vars=['set'], value_vars=probs)
# fig = px.histogram(melt.query('set == "test"'), 'value', color='variable', barmode='overlay', opacity=0.6)
# plot(fig)

fig = px.histogram(df, "stds", color="set", barmode="overlay", opacity=0.6)
plot(fig)

df["correct"] = df["pred"] == df["y"]
gb = df.groupby(["set", "correct"])["stds"].mean().reset_index()
fig = px.bar(gb, "set", "stds", color="correct", barmode="group")
plot(fig)

fig = px.scatter(df, "prob", "stds", color="set")
plot(fig)

# random forest uncertainty

rf = RandomForestClassifier(n_jobs=-1)
rf.fit(train[feature_columns], train[target_column])

df["pred_rf"] = rf.predict(df[feature_columns])
df["prob_rf"] = rf.predict_proba(df[feature_columns])[:, -1]
df["stds_rf"] = random_forest_uncertainty(rf, df[feature_columns])

fig = px.scatter_3d(df.query('set == "test"'), "r0", "r1", "r2", color="stds_rf")
fig.update_traces(marker={"size": 2})
plot(fig, filename=create_plot_path())

df.query('set == "test"')[["prob", "stds", "stds_rf"]].corr()
