from dataclasses import dataclass
from datetime import date
from typing import Callable, Generic, TypeVar
from mock_api import Record, simulate_api_call
from validation_exceptions import InvalidDOBError, InvalidNameError, InvalidUserError

T = TypeVar("T")
U = TypeVar("U")


@dataclass
class User:
    name: str
    dob: str


class ParseUserResult(Generic[T]):
    def __init__(self, value: T | Exception):
        self.value = value

    def map(self, func: Callable[[T], U]) -> "ParseUserResult":
        if isinstance(self.value, Exception):
            return ParseUserResult[U](self.value)
        try:
            return ParseUserResult[U](func(self.value))
        except Exception as e:
            return ParseUserResult[U](e)

    def __repr__(self) -> str:
        return str(self.value)


def extract_fields(record: Record) -> User:
    if not isinstance(record, dict):
        raise TypeError("Expected dictionary")

    name = record.get("name")
    dob = record.get("dob")

    if name and dob:
        new_user = User(name=record["name"], dob=record["dob"])
        return new_user

    raise InvalidUserError("Invalid fields: name or dob is missing")


def validate_name(user: User) -> User:
    if isinstance(user.name, str) and user.name.strip():
        return user
    raise InvalidNameError(f"Invalid name: '{user.name}' must be a non-empty string")


def validate_dob(user: User) -> User:
    try:
        date.fromisoformat(user.dob)
        return user
    except ValueError:
        raise InvalidDOBError(f"Invalid dob: '{user.dob}' is not a valid ISO 8601 date")


def parse_response(response: list[Record]) -> tuple[list[User], list[Exception]]:
    invalid: list[Exception] = []
    users: list[User] = []
    for record in response:
        parser_result = (
            ParseUserResult(record)
            .map(extract_fields)
            .map(validate_name)
            .map(validate_dob)
        )
        if isinstance(parser_result.value, User):
            users.append(parser_result.value)
        else:
            invalid.append(parser_result.value)
    return users, invalid


def main() -> None:
    response = simulate_api_call()
    users, invalid = parse_response(response)
    print(users, invalid)


main()
