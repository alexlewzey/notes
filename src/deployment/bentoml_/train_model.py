import bentoml.xgboost
import pandas as pd
import xgboost as xgb

# Load and prep the data
data = pd.read_csv("data/data.csv")
X, y = data.drop("target", axis=1), data[["target"]]

# Create a DMatrıx
dtrain = xgb.DMatrix(X.values, label=y.values)

# Specify parameters for a binary classification problem
params = {
    "objective": "binary:logistic",
    "booster": "gbtree",
    "eval_metric": "auc",
}

# Train
booster = xgb.train(params=params, dtrain=dtrain)
bento_xgb = bentoml.xgboost.save_model("xgb_1", booster)
