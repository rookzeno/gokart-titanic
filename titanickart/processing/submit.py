import gokart
import luigi
import pandas as pd

from titanickart.task_template import TitanicKart


class SubmitData(TitanicKart):
    submission = gokart.TaskInstanceParameter()
    submit = luigi.BoolParameter()

    def requires(self):
        return dict(submission=self.submission)

    def run(self):
        if self.submit:
            self.dump(self._run(self.load_data_frame('submission')))
        else:
            self.dump('not submitted')

    @staticmethod
    def _run(submission: pd.DataFrame) -> pd.DataFrame:
        from kaggle import KaggleApi  # because of an error in __init__.py
        api = KaggleApi()
        api.authenticate()

        submission.to_csv('titatic_submission.csv', index=False)
        csv_file_path = 'titatic_submission.csv'
        message = 'titanic submission'
        competition_id = 'titanic'
        api.competition_submit(csv_file_path, message, competition_id)
        return 'submitted'
