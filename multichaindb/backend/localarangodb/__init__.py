
"""ArangoDB backend implementation.

Contains a ArangoDB-specific implementation of the
:mod:`~multichaindb.backend.schema` and :mod:`~multichaindb.backend.query` interfaces.

You can specify MultiChainDB to use ArangoDB as its database backend by either
setting ``database.backend`` to ``'localarangodb'`` in your configuration file, or
setting the ``MULTICHAINDB_DATABASE_BACKEND`` environment variable to
``'localarangodb'``.

ArangoDB is the default database backend for MultiChainDB.

If configured to use ArangoDB, MultiChainDB will automatically return instances
of :class:`~multichain.backend.localarangodb.LocalArangoDBConnection` for
:func:`~multichaindb.backend.connection.connect` and dispatch calls of the
generic backend interfaces to the implementations in this module.
"""

# Register the single dispatched modules on import.
from multichaindb.backend.localarangodb import schema, query # noqa

# ArangoDBConnection should always be accessed via
# ``multichaindb.backend.connect()``.
