from abc import ABCMeta, abstractmethod


class ConfigParserBase(metaclass=ABCMeta):
    def __init__(self, filename: str):
        self.FILENAME = filename
        self.load()

    @abstractmethod
    def load(self):
        ...

    @abstractmethod
    def as_dict(self) -> dict:
        ...
