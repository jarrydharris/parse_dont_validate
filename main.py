from dataclasses import dataclass
from io import TextIOWrapper
from typing import Optional

@dataclass(init=False)
class Metadata:
    key_1: str
    key_2: str

@dataclass
class UpdateField:
    name: str
    value: str
    error: Optional[BaseException]


class MetadataParser:
    def parse_text_io(self, text_io: TextIOWrapper) -> Metadata:
        new_metadata = Metadata()
        for line in text_io.readlines():
            key, value = (element.strip() for element in line.split(","))
            new_metadata.__setattr__(key, value)
        return new_metadata


def main():
    ...

main()