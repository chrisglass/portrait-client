import configparser
import os


# The portrait client configuration file. This is expected to be an INI file
# with a single section called "portrait".
LANDSCAPE_CLIENT_CONF = "/etc/portrait/client.conf"

DEFAULTS = {
    "server": "landscape.canonical.com",
    "ping_interval": "15",
    "computer_title": "My test portrait client",
    "main_store": "/var/lib/portrait/main_store.db"}


def load_config_file(config_file=LANDSCAPE_CLIENT_CONF, use_defaults=True):
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
