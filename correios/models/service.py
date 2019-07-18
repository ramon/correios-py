from decimal import Decimal
from typing import Union, Optional, Sequence, List, cast, Dict, Any

from correios.exceptions import MaximumDeclaredValueError, MinimumDeclaredValueError, InvalidExtraServiceError

EXTRA_SERVICE_CODE_SIZE = 2
EXTRA_SERVICES = {
    1: {"code": "AR", "name": "Aviso de Recebimento"},
    2: {"code": "MP", "name": "Mão Própria Nacional"},
    19: {"code": "VD", "name": "Valor Declarado (Encomendas)"},  # Sedex
    25: {"code": "RR", "name": "Registro Nacional"},
    64: {"code": "VD", "name": "Valor Declarado (Encomendas)"},  # PAC
}

EXTRA_SERVICE_AR = 1
EXTRA_SERVICE_MP = 2
EXTRA_SERVICE_VD_SEDEX = 19
EXTRA_SERVICE_RR = 25
EXTRA_SERVICE_VD_PAC = 64

SERVICES = {
    "40215": {
        "description": "SEDEX 10",
        "max_weight": 10000,
        "display_name": "SEDEX 10",
        "min_declared_value": Decimal("19.50"),
        "max_declared_value": Decimal("10000.00"),
    },
    "04162": {
        "description": "SEDEX CONTRATO AGENCIA",
        "max_weight": 30000,
        "display_name": "SEDEX",
        "default_extra_services": [EXTRA_SERVICE_RR],
        "min_declared_value": Decimal("19.50"),
        "max_declared_value": Decimal("10000.00"),
    },
    "04669": {
        "description": "PAC",
        "display_name": "PAC",
        "max_weight": 30000,
        "default_extra_services": [EXTRA_SERVICE_RR],
        "min_declared_value": Decimal("19.50"),
        "max_declared_value": Decimal("3000.00"),
    }
}


class Service:
    def __init__(self,
                 code: Union[int, str],
                 description: str,
                 display_name: Optional[str] = "",
                 max_weight: Optional[int] = None,
                 min_declared_value: Decimal = Decimal("0.00"),
                 max_declared_value: Decimal = Decimal("0.00"),
                 default_extra_services: Optional[Sequence[Union["ExtraService", int]]] = None
                 ) -> None:
        self.code = Service.sanitize_code(code)
        self.description = description.strip()
        self.display_name = display_name or self.description
        self.max_weight = max_weight
        self.min_declared_value = min_declared_value
        self.max_declared_value = max_declared_value

        if default_extra_services is None:
            self.default_extra_services = []  # type: List
        else:
            self.default_extra_services = [ExtraService.get(es) for es in default_extra_services]

    def __str__(self):
        return str(self.code)

    def __repr__(self):
        return "<Service code={!r}, name={!r}>".format(self.code, self.display_name)

    def __eq__(self, other):
        other = Service.get(other)
        return self.code == other.code

    def validate_declared_value(self, value: Union[Decimal, float]) -> bool:
        if value > self.max_declared_value:
            raise MaximumDeclaredValueError(
                "Declared value {!r} is greater than maximum "
                "{!r} for service {!r}".format(value, self.max_declared_value, self)
            )

        if value < self.min_declared_value:
            raise MinimumDeclaredValueError(
                "Declared value {!r} is less than minimum "
                "{!r} for service {!r}".format(value, self.min_declared_value, self)
            )

        return True

    @classmethod
    def sanitize_code(cls, code: Union[int, str]) -> str:
        code = int(str("".join(d for d in str(code) if d.isdigit())).strip())
        return "{:05}".format(code)

    @classmethod
    def get(cls, service: Union["Service", int, str]) -> "Service":
        if isinstance(service, cls):
            return service

        service = cast(Union[int, str], service)
        code = cls.sanitize_code(service)
        return cls(code=code, **SERVICES[code])


class ExtraService:
    def __init__(self, number: int, code: str, name: str) -> None:
        if not number:
            raise InvalidExtraServiceError("Invalid Extra Service Number {!r}".format(number))
        self.number = number

        if not code or len(code) != EXTRA_SERVICE_CODE_SIZE:
            raise InvalidExtraServiceError("Invalid Extra Service Code {!r}".format(code))
        self.code = code.upper()

        if not name:
            raise InvalidExtraServiceError("Invalid Extra Service Name {!r}".format(name))
        self.name = name


    def __repr__(self):
        return "<ExtraService number={!r}, code={!r}>".format(self.number, self.code)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.number == other

        return self.number == other.number

    def is_declared_value(self):
        return self in (EXTRA_SERVICE_VD_PAC, EXTRA_SERVICE_VD_SEDEX)

    @classmethod
    def get(cls, number: Union["ExtraService", str]) -> "ExtraService":
        if isinstance(number, cls):
            return number

        number = cast(int, number)
        attrs: Dict[str, Any] = EXTRA_SERVICES[number]
        return cls(number=number, **attrs)
