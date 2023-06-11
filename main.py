import argparse
import logging
import sys
from logging import getLogger

import gokart

from titanickart.pipeline import TitanicKartPipeline

logger = getLogger(__name__)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--submit', action='store_true')
    args = parser.parse_args()

    gokart.add_config('./conf/base.ini')
    task = TitanicKartPipeline(submit=args.submit)
    gokart.build(task, log_level=logging.DEBUG)
    return 0


if __name__ == '__main__':
    sys.exit(main())
