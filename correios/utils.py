import os
import re
from decimal import Decimal
from pathlib import Path
from typing import Union

from datetime import datetime

import pkg_resources


def rreplace(string: str, old: str, new: str, count: int = 0) -> str:
    """
    Return a copy of string with all occurences of substring
    old replace by new starting from the right. If the optional
    argument count is given only the first count occurences are
    replaced.
    """

    reverse = string[::-1]
    if count:
        return reverse.replace(old[::-1], new[::-1], count)[::-1]

    return reverse.replace(old[::-1], new[::-1])[::-1]

def to_integer(number: Union[int, str]) -> int:
    return int(str(number).strip())


def to_datetime(date: Union[datetime, str], fmt="%Y-%m-%d %H:%M:%S%z") -> datetime:
    if isinstance(date, str):
        last_colon_pos = date.rindex(":")
        date = date[:last_colon_pos] + date[last_colon_pos + 1 :]  # noqa: E203
        return datetime.strptime(date, fmt)
    return date


def to_decimal(value: Union[Decimal, str, float], precision=2) -> Decimal:
    if not isinstance(value, Decimal):
        value = rreplace(str(value), ",", ".", 1)
        if "." in value:
            real, imag = value.rsplit(".", 1)
        else:
            real, imag = value, "0"
        real = re.sub("[,._]", "", real)
        value = Decimal("{}.{}".format(real, imag))

    quantize = Decimal("0." + "0" * precision)
    return value.quantize(quantize)

def get_resource_path(path) -> Path:
    resource_package = "correios"
    resource_path = os.path.join("data", path)
    return Path(pkg_resources.resource_filename(resource_package, resource_path))
