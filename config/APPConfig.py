from figgypy import Config, set_config, get_value


class APPConfig:
    def __init__(self):
        self.config = Config(config_file='config.yaml')
        set_config(self.config)

    @staticmethod
    def read(key):
        return get_value(key)
