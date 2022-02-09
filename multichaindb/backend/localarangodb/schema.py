

import logging

import pyArango

from multichaindb import backend
from multichaindb.backend.localarangodb.connection import LocalArangoDBConnection
from multichaindb.backend.utils import module_dispatch_registrar

logger = logging.getLogger(__name__)
register_schema = module_dispatch_registrar(backend.schema)


INDEXES = {
    'transactions': [
        ('asset.id', dict(name='asset_id')),
        ('outputs.public_keys', dict(name='outputs')),
        (['inputs.fulfills.transaction_id',
            'inputs.fulfills.output_index'], dict(name='inputs'))
    ],
    # ArangoDB doesn't support wildcards indexes
    'blocks': [
        ('height', dict(name='height', unique=True))
    ],
    'utxos': [
        (['transaction_id', 'output_index'], 
            dict(name='utxo', unique=True))
    ],
    'pre_commit': [
        ('height', dict(name='height', unique=True))
    ], 
    'elections': [
        (['height', 'election_id'],
         dict(name='election_id_height', unique=True)),
    ],
    'validators': [
        ('height', dict(name='height', unique=True)),
    ],
    'abci_chains': [
        ('height', dict(name='height', unique=True)),
        ('chain_id', dict(name='chain_id', unique=True)),
    ],
}


@register_schema(LocalArangoDBConnection)
def create_database(conn, dbname):
    logger.info('Create database `%s`.', dbname)
    # TODO: read and write concerns can be declared here
    if not conn.conn.hasDatabase(dbname):
        conn.conn.createDatabase(dbname)



@register_schema(LocalArangoDBConnection)
def create_tables(conn, dbname):
    for table_name in backend.schema.TABLES:
        # create the table
        # TODO: read and write concerns can be declared here
        try:
            logger.info(f'Create `{table_name}` table.')
            conn.conn[dbname].createCollection(table_name)
        except pyArango.theExceptions.CreationError:
            logger.info(f'Collection {table_name} already exists.')
        create_indexes(conn, dbname, table_name, INDEXES[table_name])


def create_indexes(conn, dbname, collection, indexes):
    logger.info(f'Ensure secondary indexes for `{collection}`.')
    for fields, kwargs in indexes:
        conn.conn[dbname].ensureHashIndex(fields, **kwargs)


@register_schema(LocalArangoDBConnection)
def drop_database(conn, dbname):
    del(conn.conn[dbname])
