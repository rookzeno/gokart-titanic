import json
import os
import subprocess

import luigi
import pandas as pd

from titanickart.task_template import TitanicKart


class DownloadData(TitanicKart):
    username: str = luigi.Parameter()
    api_key: str = luigi.Parameter()

    def run(self):
        self.dump(self._run(self.username, self.api_key))

    @classmethod
    def _run(cls, username: str, api_key: str) -> pd.DataFrame:
        from kaggle import KaggleApi  # because of an error in __init__.py
        cls.init_on_kaggle(username, api_key)
        api = KaggleApi()
        api.authenticate()
        api.competition_download_file('titanic', 'train.csv', path='tmp_download')
        api.competition_download_file('titanic', 'test.csv', path='tmp_download')
        train = pd.read_csv('tmp_download/train.csv')
        test = pd.read_csv('tmp_download/test.csv')
        data = pd.concat([train, test])
        return data

    @staticmethod
    def init_on_kaggle(username, api_key):
        KAGGLE_CONFIG_DIR = os.path.join(os.path.expandvars('$HOME'), '.kaggle')
        try:
            os.makedirs(KAGGLE_CONFIG_DIR)
        except FileExistsError:
            return 0
        api_dict = {'username': username, 'key': api_key}
        with open(f'{KAGGLE_CONFIG_DIR}/kaggle.json', 'w', encoding='utf-8') as f:
            json.dump(api_dict, f)
        cmd = f'chmod 600 {KAGGLE_CONFIG_DIR}/kaggle.json'
        output = subprocess.check_output(cmd.split(' '))
        output = output.decode(encoding='UTF-8')
        return 0
