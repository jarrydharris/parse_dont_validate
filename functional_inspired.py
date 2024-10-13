from dataclasses import dataclass
from datetime import date
from typing import Callable, Generic, TypeVar
from mock_api import Record, simulate_api_call

T = TypeVar("T")
U = TypeVar("U")


class InvalidUserError(Exception):
    pass


class InvalidNameError(Exception):
    pass


class InvalidDOBError(Exception):
    pass


@dataclass
class User:
    name: str
    dob: str


class ParseUser(Generic[T]):
    def __init__(self, value: T | Exception):
        self.value = value

    def map(self, func: Callable[[T], U]) -> "ParseUser[U]":
        if isinstance(self.value, Exception):
            return ParseUser[U](self.value)
        try:
            return ParseUser[U](func(self.value))
        except Exception as e:
            return ParseUser[U](e)

    def __repr__(self) -> str:
        return str(self.value)

    @classmethod
    def extract_fields(cls, record: Record) -> "ParseUser[User | Exception]":
        if not isinstance(record, dict):
            return ParseUser(TypeError("Expected dictionary"))

        name = record.get("name")
        dob = record.get("dob")

        if name and dob:
            new_user = User(name=record["name"], dob=record["dob"])
            return ParseUser(new_user)

        return ParseUser(InvalidUserError("Invalid fields: name or dob is missing"))


def validate_name(user: User | Exception) -> User | Exception:
    if isinstance(user, Exception):
        return user
    if isinstance(user.name, str) and user.name.strip():
        return user
    return InvalidNameError(f"Invalid name: '{user.name}' must be a non-empty string")


def validate_dob(user: User | Exception) -> User | Exception:
    if isinstance(user, Exception):
        return user
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
        parser_result = (
            ParseUser.extract_fields(record).map(validate_name).map(validate_dob)
        )
        if isinstance(parser_result.value, User):
            users.append(parser_result.value)
        else:
            invalid.append(parser_result.value)
    return users, invalid


def main() -> None:
    response = simulate_api_call()
    users, invalid = parse_response(response)

    print(invalid)
    print(users)


main()
