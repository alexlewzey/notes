import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from pyod.models.auto_encoder import AutoEncoder
from pyod.utils.data import generate_data
from sklearn.decomposition import PCA
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

contamination = 0.1  # percentage of outliers
n_train = 500  # number of training points
n_test = 500  # number of testing points
n_features = 25  # Number of features
x_train, x_test, y_train, y_test = generate_data(
    n_train=n_train,
    n_test=n_test,
    n_features=n_features,
    contamination=contamination,
    random_state=1234,
)
print(x_train.shape, y_train.shape, x_test.shape)
x_train = pd.DataFrame(x_train)
x_test = pd.DataFrame(x_test)

# PREPROCESSING ########################################################################################################

ss = StandardScaler()
x_train = ss.fit_transform(x_train)
x_train = pd.DataFrame(x_train)
x_test = ss.transform(x_test)
x_test = pd.DataFrame(x_test)

pca = PCA(2)
x_train_pca = pca.fit_transform(x_train)
x_train_pca = pd.DataFrame(x_train_pca)
x_train_pca.columns = ["pc1", "pc2"]
x_train_pca["y"] = y_train.astype(str)

x_test_pca = pca.transform(x_test)
x_test_pca = pd.DataFrame(x_test_pca)
x_test_pca.columns = ["pc1", "pc2"]
x_test_pca["y"] = y_test.astype(str)

# SKLEARN NOVELTY DETECTION ############################################################################################

# m = IsolationForest()
m = LocalOutlierFactor(novelty=True)

m.fit(x_train[y_train == 0.0])
threshold = m.score_samples(x_train[y_train == 0.0]).min() * 1.00

x_train_pca["score"] = m.score_samples(x_train)
x_train_pca["pred"] = (x_train_pca["score"] < threshold).astype(str)

x_test_pca["score"] = m.score_samples(x_test)
x_test_pca["pred"] = (x_test_pca["score"] < threshold).astype(str)


fig = px.scatter(
    x_train_pca, "pc1", "pc2", color="pred", title=f"{m.__class__.__name__}: train"
)
plot(fig)

fig = px.histogram(
    x_train_pca,
    "score",
    color="pred",
    nbins=100,
    title=f"{m.__class__.__name__}: train",
)
fig.add_vline(threshold, line_dash="dash", line_color="red")
plot(fig)

fig = px.scatter(
    x_test_pca, "pc1", "pc2", color="pred", title=f"{m.__class__.__name__}: test"
)
plot(fig)

fig = px.histogram(
    x_test_pca, "score", color="pred", title=f"{m.__class__.__name__}: test", nbins=100
)
fig.add_vline(threshold, line_dash="dash", line_color="red")
plot(fig)

# AUTO-ENCODERS ########################################################################################################

# train
ae = AutoEncoder(hidden_neurons=[25, 2, 2, 25])
baseline = x_train[y_train == 0.0]
ae.fit(baseline)
scores = ae.decision_function(baseline)
min_, max_ = pd.Series(scores).agg(["min", "max"]).values.tolist()
buffer = np.abs(max_ - min_) * 0.1
min_ -= buffer
max_ += buffer

x_train_pca["score_ae"] = ae.decision_function(x_train)
x_train_pca["pred_ae"] = x_train_pca["score_ae"].between(min_, max_)

x_test_pca["score_ae"] = ae.decision_function(x_test)
x_test_pca["pred_ae"] = x_test_pca["score_ae"].between(min_, max_)

fig = px.scatter(
    x_train_pca, "pc1", "pc2", color="pred_ae", title="auto-encoders: train"
)
plot(fig)
fig = px.histogram(
    x_train_pca, "score_ae", color="pred_ae", title="auto-encoders: train", nbins=150
)
for i in [min_, max_]:
    fig.add_vline(i, line_dash="dash", line_color="red")
plot(fig)

# test

fig = px.scatter(x_test_pca, "pc1", "pc2", color="pred_ae", title="auto-encoders: test")
plot(fig)
fig = px.histogram(
    x_test_pca, "score_ae", color="pred_ae", title="auto-encoders: test", nbins=150
)
for i in [min_, max_]:
    fig.add_vline(i, line_dash="dash", line_color="red")
plot(fig)
