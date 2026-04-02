

from __future__ import annotations
from abc import ABC, abstractmethod
from string import ascii_letters

dirty_string = "!@#!@sa!%!#n;'k$!!e^!#$t w()#!a#!@#g%!!@h*&*#@"

class Stage(ABC):
    
    @abstractmethod
    def process(self, data: str) -> str:
        ...

class StripExclamation(Stage):

    def process(self, data: str) -> str:
        return "".join([chr for chr in data if chr != "!"])

class StripOtherCharacters(Stage):

    def process(self, data: str) -> str:
        return "".join([chr for chr in data if chr in ascii_letters + " "   ])

class Pipeline:
    
    def __init__(self) -> None:
        self._stages : list[Stage] = []

    def add_stage(self, stage: Stage) -> Pipeline:
        self._stages.append(stage)
        return self

    def execute(self, data: str) -> str:
        result = data
        for stage in self._stages:
            result = stage.process(result)
        return result

if __name__ == "__main__": 
    
    dirty_string = "!@#!@sa!%!#n;'k$!!e^!#$t w()#!a#!@#g%!!@h*&*#@"
    print(dirty_string)
    pipeline = Pipeline()
    pipeline.add_stage(StripExclamation()).add_stage(StripOtherCharacters())
    result = pipeline.execute(dirty_string)
    print(result)

    