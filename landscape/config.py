import os
import yaml


# The landscape client configuration file. This is expected to be yaml.
LANDSCAPE_CLIENT_CONF = "/etc/landscape/client.conf"

DEFAULTS = {
    "server": "landscape.canonical.com",
    "ping_interval": 15,
    "computer_title": "My test portrait client"}


def load_config_file(config=LANDSCAPE_CLIENT_CONF, use_defaults=True):
    """
    Load the configuration file, and returned the parsed (from yaml) contents.
    """
    assert os.path.exists(config), "The configuration file is not found."

    contents = {}
    if use_defaults:
        contents.update(DEFAULTS)
    with open(config, "r") as thefile:
        loaded = yaml.safe_load(thefile.read())
        contents.update(loaded)

    return contents
