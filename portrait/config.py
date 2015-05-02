import configparser
import os

from portrait.storage.main import DEFAULT_PORTRAIT_DB_PATH


# The portrait client configuration file. This is expected to be an INI file
# with a single section called "portrait".
PORTRAIT_CLIENT_CONF = "/etc/portrait/client.conf"

DEFAULTS = {
    "server": "landscape.canonical.com",
    "ping_interval": "15",
    "computer_title": "My test portrait client",
    "main_store": DEFAULT_PORTRAIT_DB_PATH}


def load_config_file(config_file=PORTRAIT_CLIENT_CONF, use_defaults=True):
    """
    Load the configuration file, and returned the parsed contents.
    """
    assert os.path.exists(config_file), "The configuration file is not found."

    contents = {}
    if use_defaults:
        contents.update(DEFAULTS)
    config = configparser.ConfigParser()
    config.read(config_file)

    assert "portrait" in config.sections()
    contents.update(dict(config["portrait"]))

    return contents
