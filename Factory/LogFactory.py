import logging
from time import strftime

from Entity.Config import Config


class LogFactory(object):
    @staticmethod
    def init():
        logging.basicConfig(level=logging.INFO,
                            filename=Config.get_config_field()['log_dir'] + strftime("%Y-%m-%d %H.%M.%S") + '.log',
                            filemode='a',
                            format='[%(levelname)s][%(asctime)s][%(filename)s][line:%(lineno)d] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(levelname)s][%(filename)s][line:%(lineno)d] %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
