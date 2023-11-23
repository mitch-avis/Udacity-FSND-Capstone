import configparser


def load_config():
    config = configparser.ConfigParser()
    config.read(".config")
    return config


auth_config = load_config()
