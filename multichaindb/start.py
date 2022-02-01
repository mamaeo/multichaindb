# Copyright © 2020 Interplanetary Database Association e.V.,
# BigchainDB and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

import logging
import setproctitle

from abci import TmVersion, ABCI

import multichaindb
from multichaindb.lib import MultiChainDB
from multichaindb.core import App
from multichaindb.parallel_validation import ParallelValidationApp
from multichaindb.web import server, websocket_server
from multichaindb.events import Exchange, EventTypes
from multichaindb.utils import Process


logger = logging.getLogger(__name__)

BANNER = """
****************************************************************************
*                                                                          *
*                             MultiChainDB 2.2.2                           *
*   codename "jumping sloth"                                               *
*   Initialization complete. MultiChainDB Server is ready and waiting.     *
*                                                                          *
*   You can send HTTP requests via the HTTP API documented in the          *
*   MultiChainDB Server docs at:                                           *
*    https://multichaindb.com/http-api                                     *
*                                                                          *
*   Listening to client connections on: {:<15}                             *
*                                                                          *
****************************************************************************
"""


def start(args):
    # Exchange object for event stream api
    logger.info('Starting MultiChainDB')
    exchange = Exchange()
    # start the web api
    app_server = server.create_server(
        settings=multichaindb.config['server'],
        log_config=multichaindb.config['log'],
        multichaindb_factory=MultiChainDB)
    p_webapi = Process(name='multichaindb_webapi', target=app_server.run, daemon=True)
    p_webapi.start()

    logger.info(BANNER.format(multichaindb.config['server']['bind']))

    # start websocket server
    p_websocket_server = Process(name='multichaindb_ws',
                                 target=websocket_server.start,
                                 daemon=True,
                                 args=(exchange.get_subscriber_queue(EventTypes.BLOCK_VALID),))
    p_websocket_server.start()

    p_exchange = Process(name='multichaindb_exchange', target=exchange.run, daemon=True)
    p_exchange.start()

    # We need to import this after spawning the web server
    # because import ABCIServer will monkeypatch all sockets
    # for gevent.
    from abci.server import ABCIServer

    setproctitle.setproctitle('multichaindb')

    # Start the ABCIServer
    abci = ABCI(TmVersion(multichaindb.config['tendermint']['version']))
    if args.experimental_parallel_validation:
        app = ABCIServer(
            app=ParallelValidationApp(
                abci=abci.types,
                events_queue=exchange.get_publisher_queue(),
            )
        )
    else:
        app = ABCIServer(
            app=App(
                abci=abci.types,
                events_queue=exchange.get_publisher_queue(),
            )
        )
    app.run()


if __name__ == '__main__':
    start()
