# Copyright © 2020 Interplanetary Database Association e.V.,
# BigchainDB and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0


class BaseValidationRules():
    """Base validation rules for MultiChainDB.

    A validation plugin must expose a class inheriting from this one via an entry_point.

    All methods listed below must be implemented.
    """

    @staticmethod
    def validate_transaction(multichaindb, transaction):
        """See :meth:`multichaindb.models.Transaction.validate`
        for documentation.
        """
        return transaction.validate(multichaindb)

    @staticmethod
    def validate_block(multichaindb, block):
        """See :meth:`multichaindb.models.Block.validate` for documentation."""
        return block.validate(multichaindb)
