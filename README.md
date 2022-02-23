<!---
Copyright © 2022 Matteo Piacentini,
MultiChainDB.
SPDX-License-Identifier: (Apache-3.0 AND CC-BY-4.0)
Code is Apache-3.0 and docs are CC-BY-4.0
--->

# MultiChainDB Server

MultiChainDB è un noSql decentralizzato e scalabile con tutte le caratteristiche tipiche di una blockchain, garantendo l'efficienza nella gestione delle transazioni tipiche dei database e la sicurezza ed immutabilità garantite dagli elementi di crittografia. 
MultichainDB è una soluzione privata o permissioned che utilizza un protocollo di votazione per la gestione delle transazioni e validazione dei blocchi, oltre ad un protocollo molto efficiente per la replicazione attraverso la rete peer to peer chiamato Tendermint.

## Testare MultiChainDB 
Per eseguire e testare l'ultima versione di MultiChainDB è necessario munirsi della versione più recente di [Docker Compose](https://docs.docker.com/compose/install/). Una volta installato, basterà clonare questo repository attraverso il comando:
```text
git clone https://github.com/multichaindb/multichaindb.git
cd multichaindb
make run
```

MultiChainDB offre un servizio di API per interagire con il database raggiungibile attraverso la porta (di default) 9984.

I comandi eseguibili sono:

* `make start`: Esegui MultiChainDB in background (termina la sua esecuzione digitando `make stop`).
* `make stop`: Stop MultiChainDB.
* `make logs`: Aggancia i logs.
* `make clean`: Rimuove tutti gli artifatti Python generati con l'esecuzione.
* `make reset`: Termina e rimuove tutti i container Docker. Attenzione che perderai tutti i tuoi dati salvati

Eseguire make per visualizzare tutti i comandi disponibili.

## Legal

MultiChainDB è una fork di un'altra piattaforma chiamata BigChainDB che utilizza un database document-based come servizio noSql.
I file non modificati sono soggetti a CopyRight di BigChainDB.

* [Licenses](LICENSES.md) - open source & open content
* [Contact Me](matteo.piacentini3@studenti.unimi.it)
