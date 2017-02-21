from Entity.Key import KeySet
from Entity.Config import Config
from Service.KeyService import KeyService


class ConfigService(object):
    @staticmethod
    def init():
        ConfigService.read_config("Text/config.txt")
        ConfigService.read_key_list("Text/key_list.txt")
        ConfigService.read_code_list("Text/code_list.txt")

    @staticmethod
    def read_config(config_file_name):
        with open(config_file_name, 'r') as f:
            for line in f:
                line = line.strip('\n')
                key = line[:line.index(' = ')]
                value = line[line.index(' = ') + 3:]
                Config.get_config_field()[key] = value

    @staticmethod
    def read_key_list(key_list_file_name):
        with open(key_list_file_name, 'r') as f:
            for line in f:
                if line is not '\n':
                    field = line.strip('\n').split(',')
                    keyset = KeySet(field[0])
                    if len(field) == 3:
                        keyset.set_end(int(field[2]))
                    else:
                        keyset.set_end(1000)
                    if len(field) >= 2:
                        keyset.set_start(int(field[1]))
                    else:
                        KeyService.find_start(keyset)
                    keyset.set_download_path(Config.get_config_field()["download_dir"] + field[0] + '/')
                    Config.get_key_list().append(keyset)
                else:
                    break

    @staticmethod
    def read_code_list(code_list_file_name):
        with open(code_list_file_name, 'r') as f:
            for line in f:
                Config.get_code_list().append(line.strip('\n'))
