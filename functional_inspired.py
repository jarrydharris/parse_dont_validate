from dataclasses import dataclass
from datetime import date
from typing import Callable
from mock_api import Record, simulate_api_call
from validation_exceptions import InvalidDOBError, InvalidNameError, InvalidUserError


@dataclass
class User:
    name: str
    dob: str


class ParseUserResult:
    def __init__(self, value: User | Exception):
        self.value = value

    def map(self, func: Callable[[User], User | Exception]) -> "ParseUserResult":
        if isinstance(self.value, Exception):
            return ParseUserResult(self.value)

        return ParseUserResult(func(self.value))

    def __repr__(self) -> str:
        return str(self.value)


def parse_user(record: Record) -> ParseUserResult:
    if not isinstance(record, dict):
        return ParseUserResult(TypeError("Expected dictionary"))

    name = record.get("name")
    dob = record.get("dob")

    if isinstance(name, str) and isinstance(dob, str):
        new_user = ParseUserResult(User(name=record["name"], dob=record["dob"]))
        return new_user

    return ParseUserResult(InvalidUserError("Invalid fields: name or dob is missing"))


def validate_name(user: User) -> User | Exception:
    if isinstance(user.name, str) and user.name.strip():
        return user
    return InvalidNameError(f"Invalid name: '{user.name}' must be a non-empty string")


def validate_dob(user: User) -> User | Exception:
    try:
        date.fromisoformat(user.dob)
        return user
    except ValueError:
        return InvalidDOBError(
            f"Invalid dob: '{user.dob}' is not a valid ISO 8601 date"
        )


def parse_response(response: list[Record]) -> tuple[list[User], list[Exception]]:
    invalid: list[Exception] = []
    users: list[User] = []
    for record in response:
        parser_result = parse_user(record).map(validate_name).map(validate_dob)
        if isinstance(parser_result.value, User):
            users.append(parser_result.value)
        else:
            invalid.append(parser_result.value)
    return users, invalid


def main() -> None:
    response = simulate_api_call()
    users, invalid = parse_response(response)
    print(users, invalid, sep="\n\n")


main()
