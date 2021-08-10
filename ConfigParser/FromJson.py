import json
from pprint import pprint
from ._ConfigParser import ConfigParserBase
from ._DictItem import DictItem


class JsonConfigParser(ConfigParserBase):
    """JsonConfigParser parses the JSON file and you can access the variable easily.

    Examples:
    ---------
        >>> cfg = JsonConfigParser("Test.json") # you can find the Test.json in examples.
        >>> cfg.val1
        1
        >>> cfg.val5.val1
        1
        >>> cfg.val5.val3.fuga.hoge
        1
    """

    def __init__(self, json_filename: str):
        super().__init__(json_filename)

    def load(self):
        d = json.load(open(self.FILENAME))
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


if __name__ == "__main__":
    cfg = JsonConfigParser("examples/Test.json")
    pprint(cfg.as_dict())
