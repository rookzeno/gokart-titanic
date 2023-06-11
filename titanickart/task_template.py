from logging import getLogger

import gokart


class TitanicKart(gokart.TaskOnKart):
    task_namespace = 'TitanicKart'

    def __init__(self, *args, **kwargs):
        super(TitanicKart, self).__init__(*args, **kwargs)
        self.logger = getLogger(self.__module__)
