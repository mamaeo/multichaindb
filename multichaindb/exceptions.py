# Copyright © 2020 Interplanetary Database Association e.V.,
# BigchainDB and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0


class MultiChainDBError(Exception):
    """Base class for MultiChainDBError exceptions."""


class CriticalDoubleSpend(MultiChainDBError):
    """Data integrity error that requires attention"""
