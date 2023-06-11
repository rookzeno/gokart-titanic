import gokart
import luigi
import pandas as pd
import xgboost
from sklearn.model_selection import train_test_split

from titanickart.task_template import TitanicKart


class TrainXGBoostModel(TitanicKart):

    data = gokart.TaskInstanceParameter()
    random_seed: int = luigi.IntParameter(default=42)

    def requires(self):
        return dict(data=self.data)

    def run(self):
        data = self.load_data_frame('data')
        self.dump(self._train_xgb_model(data, self.random_seed))

    @staticmethod
    def _train_xgb_model(data: pd.DataFrame, random_seed: int) -> xgboost.Booster:
        train = data[data['Survived'].notnull()]
        X_train, X_valid, y_train, y_valid = train_test_split(train.drop(['PassengerId', 'Survived'], axis=1),
                                                              train['Survived'],
                                                              test_size=0.2,
                                                              random_state=random_seed)
        dtrain = xgboost.DMatrix(X_train, label=y_train)
        dvalid = xgboost.DMatrix(X_valid, label=y_valid)
        params = {'objective': 'binary:logistic'}
        model = xgboost.train(
            params=params,
            dtrain=dtrain,
            num_boost_round=200,
            evals=[(dtrain, 'train'), (dvalid, 'valid')],
            verbose_eval=50,
        )
        return model


class PredictXGBoostModel(TitanicKart):
    data = gokart.TaskInstanceParameter()

    def requires(self):
        model = TrainXGBoostModel(data=self.data)
        return dict(data=self.data, model=model)

    def run(self):
        data = self.load_data_frame('data')
        model = self.load('model')
        self.dump(self._predict_xgb_model(data, model))

    @staticmethod
    def _predict_xgb_model(data: pd.DataFrame, model=xgboost.Booster) -> pd.DataFrame:
        test = data[data['Survived'].isnull()]
        dtest = xgboost.DMatrix(test.drop(['PassengerId', 'Survived'], axis=1))
        test['Survived'] = model.predict(dtest)
        test['Survived'] = test['Survived'].apply(lambda x: 1 if x > 0.5 else 0)
        return test[['PassengerId', 'Survived']]
