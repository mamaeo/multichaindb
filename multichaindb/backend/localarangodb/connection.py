
import logging
from pydoc import cli
from ssl import CERT_REQUIRED

import pyArango
from pyArango.connection import Connection

from multichaindb.backend.connection import Connection
from multichaindb.backend.exceptions import (
    OperationError,
    ConnectionError
)

from multichaindb.backend.utils import get_multichaindb_config_value
from multichaindb.common.exceptions import ConfigurationError
from multichaindb.utils import Lazy

logger = logging.getLogger(__name__)


class LocalArangoDBConnection(Connection):

    def __init__(self, replicaset=None, ssl=None, login=None, password=None,
                 ca_cert=None, certfile=None, keyfile=None,
                 keyfile_passphrase=None, crlfile=None, **kwargs):
        """Create a new Connection instance.

        Args:
            replicaset (str, optional): the name of the replica set to
                                        connect to.
            **kwargs: arbitrary keyword arguments provided by the
                configuration's ``database`` settings
        """

        super().__init__(**kwargs)
        self.replicaset = replicaset or get_multichaindb_config_value('replicaset')
        self.ssl = ssl if ssl is not None else get_multichaindb_config_value('ssl', False)
        self.login = login or get_multichaindb_config_value('login')
        self.password = password or get_multichaindb_config_value('password')
        self.ca_cert = ca_cert or get_multichaindb_config_value('ca_cert')
        self.certfile = certfile or get_multichaindb_config_value('certfile')
        self.keyfile = keyfile or get_multichaindb_config_value('keyfile')
        self.keyfile_passphrase = keyfile_passphrase or get_multichaindb_config_value('keyfile_passphrase')
        self.crlfile = crlfile or get_multichaindb_config_value('crlfile')

    @property
    def db(self):
        return self.conn[self.dbname]

    def query(self):
        return Lazy()

    def collection(self, name):
        """Return a lazy object that can be used to compose a query.

        Args:
            name (str): the name of the collection to query.
        """
        return self.query()[self.dbname][name]


    def run(self, query):
        try:
            try:
                return query.run(self.conn[self.dbname])
            except pyArango.theExceptions.ConnectionError:
                logger.warning('Lost connection to the database, '
                               'retrying query.')
                return query.run(self.conn[self.dbname])
        except pyArango.theExceptions.ArangoError as exc:
            raise ConnectionError from exc
        except pyArango.theExceptions.AQLFetchError as exc:
            print(f'DETAILS: {exc.message}')
            raise OperationError from exc


    def _connect(self):
        """Try to connect to the database.

        Raises:
            :exc:`~ConnectionError`: If the connection to the database
                fails.
            :exc:`~AuthenticationError`: If there is a OperationFailure due to
                Authentication failure after connecting to the database.
            :exc:`~ConfigurationError`: If there is a ConfigurationError while
                connecting to the database.
        """

        try:
            # FYI: the connection process might raise a
            # `ServerSelectionTimeoutError`, that is a subclass of
            # `ConnectionFailure`.
            # The presence of ca_cert, certfile, keyfile, crlfile implies the
            # use of certificates for TLS connectivity.
            if self.ca_cert is None or self.certfile is None or \
                self.keyfile is None or self.crlfile is None:

                url = 'http://{}:{}'.format(self.host, self.port)
                client = Connection(arangoURL=url, username=self.login, 
                    password=self.password)

            else:
                # NOTE! Must be implemented!!
                pass

            return client

        except pyArango.theExceptions.ConnectionError as exc:
            logger.info('Exception in _connect(): {}'.format(exc))
            raise ConnectionError(str(exc)) from exc
        except pyArango.theExceptions.ArangoError as exc:
            raise ConfigurationError from exc

