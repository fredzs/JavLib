

class Config(object):
    config_field = dict()
    key_list = []
    code_list = list()

    @staticmethod
    def get_config_field():
        return Config.config_field

    @staticmethod
    def get_key_list():
        return Config.key_list

    @staticmethod
    def get_code_list():
        return Config.code_list

    @staticmethod
    def set_config_field(config_field):
        Config.config_field = config_field

    @staticmethod
    def set_key_list(key_list):
        Config.key_list = key_list

    @staticmethod
    def set_code_list(code_list):
        Config.code_list = code_list
