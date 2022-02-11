

"""Query implementation for arangoDB"""


import json
from turtle import update
from pyArango.theExceptions import (
    CreationError
)

from multichaindb import backend
from multichaindb.backend.exceptions import DuplicateKeyError
from multichaindb.backend.utils import module_dispatch_registrar
from multichaindb.backend.localarangodb.connection import LocalArangoDBConnection
from multichaindb.common.transaction import Transaction

register_query = module_dispatch_registrar(backend.query)


@register_query(LocalArangoDBConnection)
def store_transactions(conn, signed_transactions):
    # Create list of documents
    return [conn.db['transactions']
            .createDocument(tx).save() for tx in signed_transactions]


@register_query(LocalArangoDBConnection)
def get_transaction(conn, transaction_id):
    return conn.collection('transactions')[transaction_id]


@register_query(LocalArangoDBConnection)
def get_transactions(conn, transaction_ids):
    pass


@register_query(LocalArangoDBConnection)
def store_metadatas(conn, metadata):
    pass


@register_query(LocalArangoDBConnection)
def get_metadata(conn, transaction_ids):
    pass


@register_query(LocalArangoDBConnection)
def store_asset(conn, asset):
    pass


@register_query(LocalArangoDBConnection)
def store_assets(conn, assets):
    pass


@register_query(LocalArangoDBConnection)
def get_asset(conn, asset_id):
    return conn.run(conn.collection('asset')[asset_id])


@register_query(LocalArangoDBConnection)
def get_assets(conn, asset_ids):
    pass


@register_query(LocalArangoDBConnection)
def get_spent(conn, transaction_id, output):
    pass


@register_query(LocalArangoDBConnection)
def get_latest_block(conn):
    res = (conn.db['blocks']
            .fetchFirstExample({ 'height': conn.db['blocks'].count() - 1 }))
    return next(res) if len(res) > 0 else None
    


@register_query(LocalArangoDBConnection)
def store_block(conn, block):
    try:
        return conn.run(conn.collection('blocks')
            .createDocument(block)
            .save())
    except CreationError:
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
        .createDocument(state)
        .save())


@register_query(LocalArangoDBConnection)
def get_pre_commit_state(conn):
    pass


# Non va bene
@register_query(LocalArangoDBConnection)
def store_validator_set(conn, validators_update):
    res = conn.db['validators'].fetchFirstExample({'height': validators_update['height']})
    doc = next(res) if len(res) > 0 else conn.db['validators'].createDocument()
    # Force document to update to new values whatever it is a new document 
    # or an existing one
    doc.set(validators_update)
    doc.save()
    return doc


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
    pass


@register_query(LocalArangoDBConnection)
def get_validator_set(conn, height=None):
    pass


@register_query(LocalArangoDBConnection)
def get_election(conn, election_id):
    pass


@register_query(LocalArangoDBConnection)
def get_asset_tokens_for_public_key(conn, asset_id, public_key):
    pass


@register_query(LocalArangoDBConnection)
def store_abci_chain(conn, height, chain_id, is_synced=True):
    res = conn.db['abci_chains'].fetchFirstExample({'height': height})
    doc = res[0] if len(res) > 0 else conn.db['abci_chains'].createDocument()
    doc.set({'height': height, 'chain_id': chain_id, 'is_synced': is_synced })
    doc.save()
    return doc


@register_query(LocalArangoDBConnection)
def delete_abci_chain(conn, height):
    return conn.run(conn.collection('abci_chains')
        .empty())


@register_query(LocalArangoDBConnection)
def get_latest_abci_chain(conn):
    res = (conn.db['abci_chains']
        .fetchFirstExample({'height': conn.db['abci_chains'].count() - 1}))
    return next(res) if len(res) > 0 else None

