from typing import Union, Optional

import math

from correios.models.service import Service

IATA_COEFICIENT = 6.0

VOLUMETRIC_WEIGHT_THRESHOLD = 5000  # g

MIN_WIDTH, MAX_WIDTH = 11, 105  # cm
MIN_HEIGHT, MAX_HEIGHT = 2, 105  # cm
MIN_LENGTH, MAX_LENGTH = 16, 105  # cm
MIN_DIAMETER, MAX_DIAMETER = 5, 91  # cm
MIN_CYLINDER_LENGTH, MAX_CYLINDER_LENGTH = 18, 105  # cm
MIN_SIZE, MAX_SIZE = 29, 200  # cm
MIN_CYLINDER_SIZE, MAX_CYLINDER_SIZE = 28, 200  # cm


class Package:
    TYPE_BOX: int = 1
    TYPE_CYLINDER: int = 2
    TYPE_ENVELOPE: int = 3

    def __init__(self,
                 package_type: int = TYPE_BOX,
                 width: Union[float, int] = 0,
                 height: Union[float, int] = 0,
                 length: Union[float, int] = 0,
                 diameter: Union[float, int] = 0,
                 weight: Union[float, int] = 0,
                 service: Optional[Union[Service, str, int]] = None
                 ) -> None:
        if service:
            service = Service.get(service)

        self.package_type = package_type

        self._width = width
        self._height = height
        self._length = length
        self._diameter = diameter
        self._weight = weight

    @property
    def width(self) -> int:
        return max(MIN_WIDTH, int(math.ceil(self._weight)))

    @property
    def height(self) -> int:
        return max(MIN_HEIGHT, int(math.ceil(self._height)))

    @property
    def length(self) -> int:
        return max(MIN_LENGTH, int(math.ceil(self._length)))

    @property
    def diameter(self) -> int:
        if self.package_type != Package.TYPE_CYLINDER:
            return 0

        return max(MIN_DIAMETER, int(math.ceil(self._diameter)))

    @property
    def weight(self) -> int:
        return int(math.ceil(self._weight))

    @property
    def volumetric_weight(self) -> int:
        return Package.calculate_volumetric_weight(self.width, self.height, self.length)

    @classmethod
    def calculate_volumetric_weight(cls, width, height, length) -> int:
        return int(math.ceil((width * height * length) / IATA_COEFICIENT))
