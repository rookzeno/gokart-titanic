import luigi

from titanickart.processing.download_data import DownloadData
from titanickart.processing.make_features import MakeFeatures
from titanickart.processing.model import PredictXGBoostModel
from titanickart.processing.submit import SubmitData
from titanickart.task_template import TitanicKart


class TitanicKartPipeline(TitanicKart):
    submit: bool = luigi.BoolParameter()

    username: str = luigi.Parameter()
    api_key: str = luigi.Parameter(significant=False)

    def requires(self):
        data = DownloadData(username=self.username, api_key=self.api_key)
        processed_data = MakeFeatures(data=data)
        submission = PredictXGBoostModel(data=processed_data)
        dummy = SubmitData(submission=submission, submit=self.submit)
        return dummy

    def run(self):
        self.dump('finished')
