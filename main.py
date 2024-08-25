from dataclasses import dataclass
from io import TextIOWrapper
from typing import Optional

class InvalidUpdateError(Exception):
    pass

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

    _valid_keys: list[str] = ["key_1", "key_2"]

    def __init__(self, text_io: TextIOWrapper) ->  None:

        updates = []
        
        for line in text_io.readlines():

            error = None
            comma_seperated_line = [element.strip() for element in line.split(",")]
            
            if not self._is_key_value_pair(comma_seperated_line):
                continue
            
            key, value = comma_seperated_line
            
            if not self._matches_predefined_keys(key):
                error = ValueError("Invalid key.")
            
            updates.append(UpdateField(key, value, error))

        self.updates = updates
    
    def parse_text_io(self, metadata: Metadata) -> None:

        errors = [update.error for update in self.updates]
        
        if any(errors):
            message = f"Unable to update field due to the following error(s): {errors}"
            raise InvalidUpdateError(message)
        
        if self._missing_keys():
            raise InvalidUpdateError(f"Missing required keys")

        for update in self.updates:
            setattr(metadata, update.name, update.value)

    def _matches_predefined_keys(self, key: str) -> bool:
        return key in self._valid_keys

    def _is_key_value_pair(self, split_line: list[str]) -> bool:
        return len(split_line) == 2
    
    def _missing_keys(self) -> bool:
        # TODO: check the model attributes, not predefined keys
        return len(set(self._valid_keys).intersection([update.name for update in self.updates])) < len(self._valid_keys)

        


