from typing import Tuple
from my_exceptions import ConfigError
from pydantic import BaseModel, Field, NonNegativeInt, model_validator
from utils import is_42_cell


class Validator(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: Tuple[NonNegativeInt, NonNegativeInt]
    exit: Tuple[NonNegativeInt, NonNegativeInt]

    @model_validator(mode="after")
    def semantic_validation(self) -> 'Validator':
        w_entry, h_entry = self.entry
        w_exit, h_exit = self.exit
        if w_entry == w_exit and h_entry == h_exit:
            raise ConfigError(f"ENTRY and EXIT cannot be the same: "
                              f"{self.entry} and {self.exit}")

        if (
            w_entry < 0 or w_entry >= self.height
            or h_entry < 0 or h_entry >= self.width
        ):
            raise ConfigError(f"Invalid value for ENTRY: {self.entry}")

        if (
            w_exit < 0 or w_exit >= self.height
            or h_exit < 0 or h_exit >= self.width
        ):
            raise ConfigError(f"Invalid value for EXIT: {self.exit}")

        if is_42_cell(self.width, self.height, w_entry, h_entry):
            raise ConfigError(f"ENTRY cannot be in the 42 cell pattern: "
                              f"{self.entry}")

        if is_42_cell(self.width, self.height, w_exit, h_exit):
            raise ConfigError(f"EXIT cannot be in the 42 cell pattern: "
                              f"{self.exit}")

        return self
