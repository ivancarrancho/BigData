import os


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ('TRUE', '1')

    return result


SECRET_KEY = 'issosecret'
DOMAIN = os.getenv("DOMAIN")
BIGDATA_PRIVATE_KEY = os.getenv('BIGDATA_PRIVATE_KEY')
