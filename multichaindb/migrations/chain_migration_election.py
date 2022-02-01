import json

from multichaindb.common.schema import TX_SCHEMA_CHAIN_MIGRATION_ELECTION
from multichaindb.elections.election import Election


class ChainMigrationElection(Election):

    OPERATION = 'CHAIN_MIGRATION_ELECTION'
    CREATE = OPERATION
    ALLOWED_OPERATIONS = (OPERATION,)
    TX_SCHEMA_CUSTOM = TX_SCHEMA_CHAIN_MIGRATION_ELECTION

    def has_concluded(self, multichaindb, *args, **kwargs):
        chain = multichaindb.get_latest_abci_chain()
        if chain is not None and not chain['is_synced']:
            # do not conclude the migration election if
            # there is another migration in progress
            return False

        return super().has_concluded(multichaindb, *args, **kwargs)

    def on_approval(self, multichain, *args, **kwargs):
        multichain.migrate_abci_chain()


    def show_election(self, multichain):
        output = super().show_election(multichain)
        chain = multichain.get_latest_abci_chain()
        if chain is None or chain['is_synced']:
            return output

        output += f'\nchain_id={chain["chain_id"]}'
        block = multichain.get_latest_block()
        output += f'\napp_hash={block["app_hash"]}'
        validators = [
            {
                'pub_key': {
                    'type': 'tendermint/PubKeyEd25519',
                    'value': k,
                },
                'power': v,
            } for k, v in self.get_validators(multichain).items()
        ]
        output += f'\nvalidators={json.dumps(validators, indent=4)}'
        return output


    def on_rollback(self, multichain, new_height):
        multichain.delete_abci_chain(new_height)
