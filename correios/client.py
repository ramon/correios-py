from decimal import Decimal
from typing import Union, List, Optional, Sequence

from correios.models.contract import Contract
from correios.models.package import Package
from correios.models.service import Service, ExtraService, EXTRA_SERVICE_MP, EXTRA_SERVICE_AR
from correios.utils import to_decimal, to_integer
from correios.webservices import Freight
from correios.webservices.freight import FreightResponse


class Client:

    def __init__(self, contract: Contract) -> None:
        self._contract = contract

        self.freight_client = Freight()
        self.freight = self.freight_client.service

    def calculate_freights(self,
                           services: List[Union[Service, int]],
                           from_zipcode: Union[int, str],
                           to_zipcode: Union[int, str],
                           package: Package,
                           value: Union[Decimal, float] = 0.00,
                           extra_services: Optional[Sequence[Union[ExtraService, int]]] = None
                           ) -> List:
        services = [Service.get(s) for s in services]

        if extra_services is None:
            extra_services = []
        else:
            extra_services = [ExtraService.get(es) for es in extra_services]

        response = self.freight.CalcPrecoPrazo(
            self._contract.administrative_code,
            self._contract._password,
            ",".join(str(s) for s in services),
            str(from_zipcode),
            str(to_zipcode),
            package.weight,
            package.package_type,
            package.length,
            package.height,
            package.width,
            package.diameter,
            "S" if EXTRA_SERVICE_MP in extra_services else "N",
            value,
            "S" if EXTRA_SERVICE_AR in extra_services else "N",
        )

        result = []

        for service in response.cServico:
            result.append(self._build_freight_response(service_data=service))

        return result

    def calculate_freight_messaage(self,
                           services: List[Union[Service, int]],
                           from_zipcode: Union[int, str],
                           to_zipcode: Union[int, str],
                           package: Package,
                           value: Union[Decimal, float] = 0.00,
                           extra_services: Optional[Sequence[Union[ExtraService, int]]] = None
                           ) -> List:
        services = [Service.get(s) for s in services]

        if extra_services is None:
            extra_services = []
        else:
            extra_services = [ExtraService.get(es) for es in extra_services]

        response = self.freight_client.create_message(self.freight, 'CalcPrecoPrazo',
            nCdEmpresa=self._contract.administrative_code,
            sDsSenha=self._contract._password,
            nCdServico=",".join(str(s) for s in services),
            sCepOrigem=str(from_zipcode),
            sCepDestino=str(to_zipcode),
            nVlPeso=package.weight,
            nCdFormato=package.package_type,
            nVlComprimento=package.length,
            nVlAltura=package.height,
            nVlLargura=package.width,
            nVlDiametro=package.diameter,
            sCdMaoPropria="S" if EXTRA_SERVICE_MP in extra_services else "N",
            nVlValorDeclarado=value,
            sCdAvisoRecebimento="S" if EXTRA_SERVICE_AR in extra_services else "N",
        )

        return response

    def _build_freight_response(self, service_data) -> FreightResponse:
        return FreightResponse(
            service=Service.get(service_data.Codigo),
            delivery_time=int(service_data.PrazoEntrega),
            value=to_decimal(service_data.ValorSemAdicionais),
            declared_value=to_decimal(service_data.ValorValorDeclarado),
            mp_value=to_decimal(service_data.ValorMaoPropria),
            ar_value=to_decimal(service_data.ValorAvisoRecebimento),
            saturday=service_data.EntregaSabado and service_data.EntregaSabado.lower() == "s" or False,
            home=service_data.EntregaDomiciliar and service_data.EntregaDomiciliar.lower() == "s" or False,
            error_code=to_integer(service_data.Erro) or 0,
            error_message=service_data.MsgErro or "",
        )
