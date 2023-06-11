import gokart
import pandas as pd

from titanickart.task_template import TitanicKart


class MakeFeatures(TitanicKart):

    data = gokart.TaskInstanceParameter()

    USE_COLUMNS = ['PassengerId', 'Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked_C', 'Embarked_Q', 'Embarked_S']

    def requires(self):
        return dict(data=self.data)

    def run(self):
        data = self.load_data_frame('data')
        self.dump(self._make_features(data, self.USE_COLUMNS))

    @staticmethod
    def _make_features(data: pd.DataFrame, use_columns: list) -> pd.DataFrame:
        data['Sex'] = data['Sex'].apply(lambda x: x == 'male').astype(int)
        data = pd.get_dummies(data=data, columns=['Embarked'])
        return data[use_columns]
