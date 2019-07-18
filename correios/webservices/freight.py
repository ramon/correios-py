from datetime import timedelta
from decimal import Decimal
from typing import Union

from correios.models.service import Service
from correios.utils import to_decimal, get_resource_path
from correios.webservices.webservice import WebService


FREIGHT_ERROR_INITIAL_ZIPCODE_RESTRICTED = 9
FREIGHT_ERROR_FINAL_ZIPCODE_RESTRICTED = 10
FREIGHT_ERROR_INITIAL_AND_FINAL_ZIPCODE_RESTRICTED = 11


class Freight(WebService):
    base_uri = str(get_resource_path('wsdls') / 'CalcPrecoPrazo.xml')


class FreightResponse:
    restricted_address_error_code = (
        FREIGHT_ERROR_INITIAL_ZIPCODE_RESTRICTED,
        FREIGHT_ERROR_FINAL_ZIPCODE_RESTRICTED,
        FREIGHT_ERROR_INITIAL_AND_FINAL_ZIPCODE_RESTRICTED,
    )

    def __init__(self,
                 service: Union[Service, int],
                 delivery_time: Union[int, timedelta],
                 value: Union[Decimal, float, int, str],
                 declared_value: Union[Decimal, float, int, str] = 0.00,
                 mp_value: Union[Decimal, float, int, str] = 0.00,
                 ar_value: Union[Decimal, float, int, str] = 0.00,
                 saturday: bool = False,
                 home: bool = False,
                 error_code: int = 0,
                 error_message: str = "",
                 ) -> None:

        self.service = Service.get(service)

        if not isinstance(delivery_time, timedelta):
            delivery_time = timedelta(days=delivery_time)

        self.delivery_time = delivery_time

        if not isinstance(value, Decimal):
            value = to_decimal(value)
        self.value = value

        if not isinstance(declared_value, Decimal):
            declared_value = to_decimal(declared_value)
        self.declared_value = declared_value

        if not isinstance(mp_value, Decimal):
            mp_value = to_decimal(mp_value)
        self.mp_value = mp_value

        if not isinstance(ar_value, Decimal):
            ar_value = to_decimal(ar_value)
        self.ar_value = ar_value

        if not isinstance(saturday, bool):
            saturday = saturday == "S"
        self.saturday = saturday

        if not isinstance(home, bool):
            home = home == "S"

        self.home = home
        self.error_code = error_code
        self.error_message = error_message

    @property
    def total(self) -> Decimal:
        return self.value + self.declared_value + self.ar_value + self.mp_value

    def is_error(self):
        return self.error_code != 0

    def is_restricted_address(self):
        return self.error_code in self.restricted_address_error_code
