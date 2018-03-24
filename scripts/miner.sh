#!/usr/bin/env bash
if [ "$#" -ne 2 ] ; then
    echo "Usage: $0 <blockchain_store> <block server port>" >&2
    exit 1
fi
source ../ENV/bin/activate
cd ../src
python -m blockchain.miner.main blockchain_store=${1}.json block_server_port=$2
