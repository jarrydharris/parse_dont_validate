from datetime import datetime
import random
from typing import Any

Record = dict[str, Any]


def simulate_api_call(num_records: int = 10) -> list[Record]:
    names = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", None, 123, "Grace"]
    invalid_dobs = [None, "not_a_date", 123456, "31-02-2020"]

    records = []

    for _ in range(num_records):
        year = random.randint(1950, 2020)
        month = random.randint(1, 12)
        day = random.randint(1, 28 if month == 2 else 30)
        valid_dob = datetime(year, month, day).strftime("%Y-%m-%d")
        record = {
            "name": random.choice(names),
            "dob": random.choice([valid_dob, random.choice(invalid_dobs)]),
        }
        records.append(record)

    return records
