from typing import Optional
from abc import ABCMeta, abstractmethod
import json
import yaml
from pprint import pprint
from ._DictItem import DictItem


_DATA_LOAD_FUNC = {
    "json": json.load,
    "yaml": yaml.safe_load
}

_DATA_DUMP_FUNC = {
    "json": json.dump,
    "yaml": yaml.dump
}

_available_extensions = ("json", "yaml")


def _get_extension(filename: str):
    return filename.split(".")[-1]


class ConfigParser:
    def __init__(self):
        self.FILENAME = None
        self.EXT = None

    @staticmethod
    def load(filename: str, encoding="utf-8-sig") -> "ConfigParser":
        ext = _get_extension(filename)
        if not ext in _available_extensions:
            raise Exception("Please specify file extension json or yaml")

        data = _DATA_LOAD_FUNC[ext](open(filename, "r", encoding=encoding))
        config_parser = ConfigParser()
        config_parser.FILENAME = filename
        config_parser.EXT = ext

        for k, v in data.items():
            if isinstance(v, dict):
                config_parser.__dict__[k] = DictItem(v)
            else:
                config_parser.__dict__[k] = v

        return config_parser

    def as_dict(self) -> dict:
        result = {}
        for k, v in self.__dict__.items():
            if k in ("FILENAME", "EXT"):
                continue

            if isinstance(v, DictItem):
                result[k] = v.as_dict()
            else:
                result[k] = v

        return result

    def __str__(self):
        text = ""
        for k, v in self.__dict__.items():
            if isinstance(v, DictItem):
                text += f"{k} : {v.to_text(2)}\n"
            else:
                text += f"{k} : {v}\n"

        return text
     
    def write(self, filename: Optional[str] = None):
        assert not (self.FILENAME is None and filename is None)
        filename = self.FILENAME if filename is None else filename
        _DATA_DUMP_FUNC[_get_extension(filename)](self.as_dict(), open(filename, "w", encoding="utf-8-sig"))
