import abc
import typing

class BaseAgent(abc.ABC):

    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def run(self)->None:
        pass
    @abc.abstractmethod
    def root_agent(self)->None:
        pass
