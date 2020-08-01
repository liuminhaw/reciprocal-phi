# -*- coding:UTF-8 -*-


# Standard library imports
# import standard libraries here
import json


class Config:
    
    def __init__(self, config_file):
        """
        Params:
            config_file - json configuration file (conf.json)
        Errors:
            configError - configuration error
        """
        self.config_file = config_file
        with open(self.config_file, 'r') as json_file:
            configs = json.load(json_file)
            self.ingredients = self._key_error(configs, 'Ingredients')
            self.pick = self._key_error(configs, 'Pick')

    def _key_error(self, configs, key):
        """
        Params:
            configs - json data block
            key - parsing key value
            msg - output message if KeyError raised
        Return:
            parsed data value
        """
        try:
            config_value = configs[key]
        except KeyError:
            msg = '{} not found in config file'.format(key)
            raise configError(msg)
        else:
            return config_value

# Exceptions
class configError(Exception):
    """
    Base class of config exception
    """
    pass