

"""Query implementation for arangoDB"""

from arango.exceptions import (
    DocumentInsertError
)

from multichaindb import backend
from multichaindb.backend.exceptions import DuplicateKeyError
from multichaindb.backend.utils import module_dispatch_registrar
from multichaindb.backend.localarangodb.connection import LocalArangoDBConnection
from multichaindb.common.transaction import Transaction

register_query = module_dispatch_registrar(backend.query)


@register_query(LocalArangoDBConnection)
def store_transactions(conn, signed_transactions):
    return conn.run(conn.collection('transactions')
        .insert_many(signed_transactions))


@register_query(LocalArangoDBConnection)
def get_transaction(conn, transaction_id):
    return conn.run(conn.collection('transactions')
        .get(transaction_id))


@register_query(LocalArangoDBConnection)
def get_transactions(conn, transaction_ids):
    return conn.run(conn.collection('transactions')
        .get_many(transaction_ids))


@register_query(LocalArangoDBConnection)
def store_metadatas(conn, metadata):
    return conn.run(conn.collection('metadata')
        .insert_many(store_metadatas))


@register_query(LocalArangoDBConnection)
def get_metadata(conn, transaction_ids):
    return conn.run(conn.collection('metadata')
        .get_many(transaction_ids))


@register_query(LocalArangoDBConnection)
def store_asset(conn, asset):
    try:
        return conn.run(conn.collection('assets')
            .insert(asset))
    except DocumentInsertError:
        pass


@register_query(LocalArangoDBConnection)
def store_assets(conn, assets):
    return conn.run(conn.collection('assets')
        .insert_many(assets))


@register_query(LocalArangoDBConnection)
def get_asset(conn, asset_id):
    try:
        return conn.run(conn.collection('assets')
            .get(asset_id))
    except IndexError:
        pass


@register_query(LocalArangoDBConnection)
def get_assets(conn, asset_ids):
    return conn.run(conn.collection('assets')
        .get_many(asset_ids))


@register_query(LocalArangoDBConnection)
def get_spent(conn, transaction_id, output):
    pass


@register_query(LocalArangoDBConnection)
def get_latest_block(conn):
    return next(conn.run(conn.collection('blocks')
        .find({'height': conn.db['blocks'].count() - 1})), None)


@register_query(LocalArangoDBConnection)
def store_block(conn, block):
    try:
        return conn.run(conn.collection('blocks')
            .insert(block))
    except DocumentInsertError:
        pass


@register_query(LocalArangoDBConnection)
def get_txids_filtered(conn, asset_id, operation=None, last_tx=None):
    pass


@register_query(LocalArangoDBConnection)
def text_search(conn, search, *, language='english', case_sensitive=False,
                diacritic_sensitive=False, text_score=False, limit=0, table='assets'):
    pass


def _remove_text_score(asset):
    pass


@register_query(LocalArangoDBConnection)
def get_owned_ids(conn, owner):
    pass


@register_query(LocalArangoDBConnection)
def get_spending_transactions(conn, inputs):
    pass


@register_query(LocalArangoDBConnection)
def get_block(conn, block_id):
    pass


@register_query(LocalArangoDBConnection)
def get_block_with_transaction(conn, txid):
    pass


@register_query(LocalArangoDBConnection)
def delete_transactions(conn, txn_ids):
    pass


@register_query(LocalArangoDBConnection)
def store_unspent_outputs(conn, *unspent_outputs):
    pass


@register_query(LocalArangoDBConnection)
def delete_unspent_outputs(conn, *unspent_outputs):
    pass


@register_query(LocalArangoDBConnection)
def get_unspent_outputs(conn, *, query=None):
    pass


@register_query(LocalArangoDBConnection)
def store_pre_commit_state(conn, state):
    return conn.run(conn.collection('pre_commit')
        .insert(state, overwrite=True))


@register_query(LocalArangoDBConnection)
def get_pre_commit_state(conn):
    next(conn.run(conn.collection('pre_commit')
        .all(limit=1)), None)


# Non va bene
@register_query(LocalArangoDBConnection)
def store_validator_set(conn, validators_update):
    return conn.run(conn.collection('validators')
        .insert(validators_update, overwrite=True))


@register_query(LocalArangoDBConnection)
def delete_validator_set(conn, height):
    pass


@register_query(LocalArangoDBConnection)
def store_election(conn, election_id, height, is_concluded):
    pass


@register_query(LocalArangoDBConnection)
def store_elections(conn, elections):
    pass


@register_query(LocalArangoDBConnection)
def delete_elections(conn, height):
    return conn.run(conn.collection('elections')
        .delete_match({'height': height}))


@register_query(LocalArangoDBConnection)
def get_validator_set(conn, height=None):
    pass


@register_query(LocalArangoDBConnection)
def get_election(conn, election_id):
    return next(conn.run(conn.collection('elections')
        .find(filter={'election_id': election_id, 
            'height': conn.db['elections'].count() - 1})), None)


@register_query(LocalArangoDBConnection)
def get_asset_tokens_for_public_key(conn, asset_id, public_key):
    pass


@register_query(LocalArangoDBConnection)
def store_abci_chain(conn, height, chain_id, is_synced=True):
    return conn.run(conn.collection('abci_chains')
        .insert({'height': height, 'chain_id': chain_id, 'is_synced': is_synced}, 
            overwrite=True))


@register_query(LocalArangoDBConnection)
def delete_abci_chain(conn, height):
    return conn.run(conn.collection('abci_chains')
        .delete_match({'height': height}))


@register_query(LocalArangoDBConnection)
def get_latest_abci_chain(conn):
    return next(conn.run(conn.collection('abci_chains')
        .find({'height': conn.db['abci_chains'].count() - 1})), None)