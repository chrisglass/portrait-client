import os
import yaml


# The landscape client configuration file. This is expected to be yaml.
LANDSCAPE_CLIENT_CONF = "/etc/landscape/client.conf"

DEFAULTS = {
    "server": "landscape.canonical.com",
    "ping_interval": 15}


def load_config_file(config=LANDSCAPE_CLIENT_CONF):
    """
    Load the configuration file, and returned the parsed (from yaml) contents.
    """
    assert os.path.exists(config), "The configuration file is not found."

    contents = DEFAULTS.copy()  # Defaults is a global dict!
    with open(config, "r") as thefile:
        loaded = yaml.load(thefile.read())
        contents.update(loaded)

    return contents
