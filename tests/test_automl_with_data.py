import unittest
import tempfile
import json
import numpy as np
import pandas as pd

from numpy.testing import assert_almost_equal
from sklearn import datasets
from supervised.automl import AutoML
from supervised.metric import Metric

import sklearn.model_selection
from sklearn.metrics import log_loss


class AutoMLTestWithData(unittest.TestCase):
    def test_fit_and_predict(self):
        seed = 1706 + 1
        for dataset_id in [31]:  # 720 # 31,44,737
            df = pd.read_csv("./tests/data/data/{0}.csv".format(dataset_id))
            x_cols = [c for c in df.columns if c != "target"]
            X = df[x_cols]
            y = df["target"]

            X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
                X, y, test_size=0.3, random_state=seed
            )
            automl = AutoML(
                total_time_limit=60 * 6000,
                algorithms=["LightGBM", "RF", "NN", "CatBoost", "Xgboost"],
                start_random_models=10,
                hill_climbing_steps=3,
                top_models_to_improve=3,
                train_ensemble=True,
                verbose=True,
            )
            automl.fit(X_train, y_train)

            response = automl.predict(X_test)
            # Compute the logloss on test dataset
            ll = log_loss(y_test, response)
            print("(*) Dataset id {} logloss {}".format(dataset_id, ll))

            for i, m in enumerate(automl._models):
                response = m.predict(X_test)
                ll = log_loss(y_test, response)
                print("{}) Dataset id {} logloss {}".format(i, dataset_id, ll))


if __name__ == "__main__":
    unittest.main()
