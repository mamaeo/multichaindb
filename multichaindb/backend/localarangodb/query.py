

"""Query implementation for arangoDB"""

from arango.exceptions import (
    DocumentInsertError,
    DocumentGetError
)

from multichaindb import backend
from multichaindb.backend.exceptions import DuplicateKeyError, OperationError
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
    return next(conn.run(conn.aql.execute(
        'FOR tx IN transactions ' \
        'FILTER tx.id == @id RETURN UNSET(tx, "_id", "_key", "_rev")',
            bind_vars={'id': transaction_id})), None)


@register_query(LocalArangoDBConnection)
def get_transactions(conn, transaction_ids):
    return list(conn.run(conn.aql.execute(
        "FOR tx IN transactions " \
        'FILTER tx.transaction_id IN @ids RETURN UNSET(tx, "_id", "_key", "_rev")', 
            bind_vars={'ids': transaction_ids})))


@register_query(LocalArangoDBConnection)
def store_metadatas(conn, metadata):
    return conn.run(conn.collection('metadata')
        .insert_many(metadata))


@register_query(LocalArangoDBConnection)
def get_metadata(conn, transaction_ids):
    return list(conn.run(conn.aql.execute(
        "FOR meta IN metadata " \
        'FILTER meta.id IN @ids RETURN UNSET(meta, "_id", "_key", "_rev")',
            bind_vars={'ids': transaction_ids})))

@register_query(LocalArangoDBConnection)
def store_asset(conn, asset):
    return conn.run(conn.collection('assets')
        .insert(asset))


@register_query(LocalArangoDBConnection)
def store_assets(conn, assets):
    return conn.run(conn.collection('assets')
        .insert_many(assets))


@register_query(LocalArangoDBConnection)
def get_asset(conn, asset_id):
    return next(conn.run(conn.aql.execute(
        'FOR asset IN assets ' \
        'FILTER asset.id == @id RETURN UNSET(asset, "_id", "_key", "_rev")',
            bind_vars={'id': asset_id})), None)


@register_query(LocalArangoDBConnection)
def get_assets(conn, asset_ids):
    return conn.run(conn.aql.execute(
        "FOR asset in assets " \
        'FILTER asset.id IN @ids RETURN UNSET(asset, "_id", "_key", "_rev")',
            bind_vars={'ids': asset_ids}))


@register_query(LocalArangoDBConnection)
def get_spent(conn, transaction_id, output):
    pass


@register_query(LocalArangoDBConnection)
def get_latest_block(conn):
    return next(conn.run(conn.aql.execute(
        "FOR blk IN blocks " \
        'SORT blk.height DESC LIMIT 1 ' \
        'RETURN UNSET(blk, "_id", "_key", "_rev")')), None)


@register_query(LocalArangoDBConnection)
def store_block(conn, block):
    return conn.run(conn.aql.execute(
        "INSERT @blk INTO blocks OPTIONS {ignoreErrors: true}", 
            bind_vars={'blk': block}))


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
    return conn.run(conn.aql.execute(
        'UPSERT {height: @height} ' \
        'INSERT @state UPDATE @state IN pre_commit',
            bind_vars={'height': state['height'], 'state': state}))


@register_query(LocalArangoDBConnection)
def get_pre_commit_state(conn):
    try:
        next(conn.run(conn.collection('pre_commit')
            .all(limit=1)), None)   
    except DocumentGetError:
        return None


@register_query(LocalArangoDBConnection)
def store_validator_set(conn, validators_update):
    return conn.run(conn.aql.execute(
        "UPSERT {height: @height} " \
        "INSERT @update UPDATE @update IN validators",
            bind_vars={'height': validators_update['height'],
            'update': validators_update}))


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
    return next(conn.run(
        conn.aql.execute('FOR election IN elections ' \
            'SORT election.height DESC LIMIT 1 ' \
            'RETURN UNSET(election, "_id", "_key", "_rev")')), None)


@register_query(LocalArangoDBConnection)
def get_asset_tokens_for_public_key(conn, asset_id, public_key):
    pass


@register_query(LocalArangoDBConnection)
def store_abci_chain(conn, height, chain_id, is_synced=True):
    return conn.run(conn.aql.execute(
        'UPSERT { height: @height }' \
        "INSERT @blk UPDATE @blk IN abci_chains", 
            bind_vars={'height': height, 'blk': {'height': height, 'chain_id': chain_id, 
                'is_synced': is_synced}}))


@register_query(LocalArangoDBConnection)
def delete_abci_chain(conn, height):
    return conn.run(conn.collection('abci_chains')
        .delete_match({'height': height}))


@register_query(LocalArangoDBConnection)
def get_latest_abci_chain(conn):
    return next(conn.run(
        conn.aql.execute("FOR chain IN abci_chains " \
            "SORT chain.height DESC LIMIT 1 "
            'RETURN UNSET(chain, "_id", "_key", "_rev")')), None)