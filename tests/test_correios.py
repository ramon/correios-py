import unittest

from correios.client import Client
from correios.models.contract import Contract
from correios.models.package import Package
from correios.models.service import Service


class CorreiosTest(unittest.TestCase):
    def setUp(self) -> None:
        self.services = [Service(4162, 'SEDEX'), Service(4669, 'PAC')]
        self.contract = Contract(123, '08082650', '564321')
        for service in self.services: self.contract.add_service(service)
        self.instance = Client(self.contract)

    def test_calc(self):
        package = Package(weight=10)

        responses = self.instance.calculate_freights(
            self.services,
            41180710,
            5512200,
            package,
            29.90
        )

        self.assertTrue(len(responses) > 0)
        for response in responses:
            self.assertFalse(response.is_error())
            self.assertEqual(response.error_message, "")
            self.assertGreaterEqual(response.value, 0)
            self.assertGreaterEqual(response.total, 0)
