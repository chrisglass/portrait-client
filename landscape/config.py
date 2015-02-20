import yaml
import os


# The landscape client configuration file. This is expected to be yaml.
LANDSCAPE_CLIENT_CONF = "/etc/landscape/client.conf"


def load_config_file(config=LANDSCAPE_CLIENT_CONF):
    """
    Load the configuration file, and returned the parsed (from yaml) contents.
    """
    assert os.path.exists(config), "The configuration file is not found."

    contents = None
    with open(config, "r") as thefile:
        contents = yaml.load(thefile.read())

    assert contents, "The configuration file is empty."
    return contents
