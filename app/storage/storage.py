from abc import ABCMeta, abstractmethod
from urllib.parse import ParseResult


class Storage(metaclass=ABCMeta):
    @abstractmethod
    def get_name(self):
        pass


class LightDbStorage(Storage):

    def __init__(self, connection_details: ParseResult, **kwargs):
        super().__init__(**kwargs)
        print(f'LightDbStorage INIT: {connection_details.geturl()}')

    def get_name(self):
        return 'LightDB'
