from requests import Session
from zeep import Client, Transport
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin


class WebService(Client):
    base_uri = None

    def __init__(self, timeout: int = 30, **kwargs) -> None:
        session = Session()
        session.verify = False
        session.timeout = timeout
        session.headers.update({"Content-Type": "text/xml;charset=UTF-8"})

        self.history = HistoryPlugin()

        cache = SqliteCache(path='/tmp/correios-api-cache.db', timeout=60)

        transport = Transport(operation_timeout=timeout, session=session, cache=cache)

        kwargs.update({'plugins':[self.history]})

        super(WebService, self).__init__(wsdl=self.base_uri, transport=transport, **kwargs)
