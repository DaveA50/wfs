import logging
import os

import yaml


def setup_logging(path='logging.yaml', level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration.

    Uses logging.yaml for the default configuration.

    Args:
        path:
        level:
        env_key:
    """
    path = path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)
