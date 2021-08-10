import yaml
from pprint import pprint
from ._ConfigParser import ConfigParserBase
from ._DictItem import DictItem


class YamlConfigParser(ConfigParserBase):
    """YamlConfigParser parses the YAML file and you can access the variable easily.

    Examples:
    ---------
        >>>
    """

    def __init__(self, yaml_filename: str):
        super().__init__(yaml_filename)

    def load(self):
        d = yaml.safe_load(open(self.FILENAME))
        for k, v in d.items():
            if isinstance(v, dict):
                self.__dict__[k] = DictItem(v)
            else:
                self.__dict__[k] = v

    def as_dict(self) -> dict:
        result = {}
        for k, v in self.__dict__.items():
            if isinstance(v, DictItem):
                result[k] = v.as_dict()
            else:
                result[k] = v

        del result["FILENAME"]
        return result

    def __str__(self):
        text = ""
        for k, v in self.__dict__.items():
            if isinstance(v, DictItem):
                text += f"{k} : {v.to_text(2)}\n"
            else:
                text += f"{k} : {v}\n"

        return text
