from typing import Union, List

from correios.models.service import Service


class Contract:
    services: List["Service"] = []

    def __init__(self, number: Union[int, str], administrative_code: Union[int, str], password: str) -> None:
        self.number = int(str(number).strip())
        self._administrative_code = int(str(administrative_code).strip())
        self._password = password

    @property
    def administrative_code(self):
        return "{:08}".format(self._administrative_code)

    def add_service(self, service: "Service") -> None:
        self.services.append(service)

    def __str__(self):
        return self.number

    def __repr__(self):
        return "<Contract number={!r}>".format(self.number)
