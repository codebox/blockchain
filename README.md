# Minimum Viable Blockchain
This project contains a pair of Python applications, referred to as the _Wallet_ and the _Miner_. Together, these applications satisfy the requirements for a [minimum viable blockchain](https://www.igvita.com/2014/05/05/minimum-viable-block-chain/#properties). The applications form a decentralised peer-to-peer network, that allows the formation of distributed consensus regarding the validity of transactions that take place within it. Any number of wallets or miners may join or leave the network at any time.

## Wallet Application
The wallet application is run as follows:
```
> python -m blockchain.wallet.main
``` 
Running the wallet without any arguments (as shown above) will display a list of the various operations which the wallet can perform:
```
INFO: Usage: python /Users/rob/code/github/blockchain/src/blockchain/wallet/main.py 
        (new-address <address name> | list-addresses | send <from address> <amount> <to address> | sync)
```
These operations are described in detail below.

### new-address
Creates a new address, from which payments can be sent and received. Each address has an associated public/private key pair stored in a [.pem file](http://how2ssl.com/articles/working_with_pem_files/). These files are all that is required to access any funds associated with a payment address, and therefore should be kept secret, and backed-up securely. When creating a new payment address, a name must be selected. The name must be locally unique (i.e. it must be different to all your other address names) but it doesn't matter if someone else on the network has chosen the same name for one of their addresses. 

Run the wallet supplying the `new-address` argument followed by the name, for example:
```
> python -m blockchain.wallet.main new-address robs-address
```
The wallet should display a message something like this:
```
INFO: Generated key [robs-address] with address 415d29e1529662a44148db9a83ae5e89f06395ab4c888aa578656ca31f01837a. 
Key saved in ./robs-address.pem
```

### list-addresses
Displays a list of all the local addresses that have been created, together with their current balances. 

Run the wallet supplying the `list-addresses` argument, as follows:
```
> python -m blockchain.wallet.main list-addresses
```
The wallet should display something like this:
```
Key Name         Balance      Pending      Address                                                         
---------------- ------------ ------------ ----------------------------------------------------------------
robs-address                0    +0.000000 415d29e1529662a44148db9a83ae5e89f06395ab4c888aa578656ca31f01837a

```
The _Balance_ column shows the confirmed balance associated with each address, this balance is calculated using all the incoming and outgoing payments for this address that have been added to the blockchain. The total of any payments issued from this address, but not yet added into the blockchain, is shown in the _Pending_ column. The long value shown in the _Address_ column is the globally unique name associated with this address. This name is generated automatically when a new address is created, and should be used by other wallets when making payments to this address.

### send
Sends a payment from one address to another. 

Run the wallet with the `send` argument, followed by the sending address, the amount, and the receiving address, in that order.

For example, to send a payment of '10' from `robs-address` to the remote address `e699496067b860f1cadcb7a4c7cc502a4e758b42cf624ac7fb40c65a0aa1edce`, run the following command:
```
> python -m blockchain.wallet.main send robs-address 10 e699496067b860f1cadcb7a4c7cc502a4e758b42cf624ac7fb40c65a0aa1edce
```
The sending address can be specified using either the local address name, as in the example above, or the global address name as displayed by the `list-addresses` command.

The receiving address should use the global address name of the recipient, unless funds are being transferred between 2 local addresses, in which case the local name can be used instead.

When the send command is issued, information concerning the transaction is sent to the network via a UDP broadcast, and will be re-broadcast at intervals when synchronising (see below) until the transaction is added to the blockchain by a mining node. 

### sync
Synchronises the wallet with the network. This operation will continue until the user cancels it by pressing `Ctrl-C`.

The synchronisation process is started by running the wallet with the `sync` argument, as shown:
```
> python -m blockchain.wallet.main sync
```

During synchronisation 2 tasks are performed:

1. The wallet listens for status broadcasts from mining nodes. These broadcasts announce the length of the blockchain currently held by the miner. If a wallet receives a broadcast claiming a longer blockchain than the one that the wallet currently holds, then the wallet will request the additional blocks from the miner.
2. The wallet re-broadcasts details of any payments that it has made, which have not yet been included in the blockchain. This ensures that payments are processed even if no miners were online when the payment was originally made.

## Miner Application
The miner application is run as follows:
```
> python -m blockchain.miner.main
``` 
The miner will run continuously until the user terminates it using `Ctrl-C`, status updates will be written to stdout.

The miner performs a number of tasks, described below

### Mining Blocks
This is the most important task that a miner performs. Miners listen for network broadcasts from wallets, containing details of new transactions that have been made. Miners collect these transactions into blocks, and when a block contains enough new transactions the miner attempts to 'mine' the block. Mining consists of performing a CPU-intensive, hash-based [proof-of-work calculation](https://en.wikipedia.org/wiki/Proof-of-work_system) which is difficult to complete, but simple to verify. Miners are incentivised to perform this work by the inclusion of a 'mining-reward' transaction in each new block. Before starting to mine a block the miner adds a new transaction into the list, paying the designated reward into an address that they control. If multiple miners are present on the network then they race to be the first to mine the new block. A mined block effectively forms a tamper-proof record of the transactions that are contained within it - any attempt to alter the contents of the block will require the proof-of-work calculation to be re-performed. Since blocks also include a reference to the previous block in the blockchain, attempting to alter an older block would require the proof-of-work calculation to be re-performed not only for that block, but for all subsequent blocks in the blockchain. In order to complete such an alteration successfully, an attacker would need to control more than 50% of the CPU power on the network.
 
### Sending/Receiving Status Broadcasts
Miners regularly broadcast the length of their copy of the blockchain. A miner who has just mined a new block will have a blockchain that is 1-block longer than anyone else on the network. As other participants on the network receive the broadcast informing them of the new block, they will request a copy of the block from the miner who created it. Any miner who was in the process of mining a new block will stop their current mining task, download the new block, and then begin mining again on top of that new block. It is of course possible that 2 miners both complete their mining at about the same time, and both start advertising their new (different) blocks to the network. This results in a temporary 'fork' in the blockchain, with some miners mining on top of one block, and some mining on top of the other. However, this situation will be automatically resolved when the next block is mined - the first branch of the fork to have an additional block mined on top of it will become the new longest blockchain, and all parties on the network will adopt this as the basis for further mining.

### Running a Block Server
Miners must be able to provide details of newly mined blocks to other wallets and miners on the network. When a miner mines a new block they will receive many requests for that block from their peers. As the new block is distributed among other miners, and those miners themselves begin to broadcast the new longer blockchain, the requests to download the new block will become distributed among all the miners who have already downloaded it, reducing the load on the originating miner. 

A block server may also receive requests for more than 1 block, from wallets or miners who have been inactive for long periods, during which time multiple new blocks have been mined. When a new miner or wallet joins the network for the first time, they will request the entire blockchain from one of the active mining nodes.

## Notes
### Configuration
There are various parameters used by the wallet and miner applications which can be configured to alter the characteristics of the network. These parameters are stored in the `config.py` file, details below:

####difficulty
Controls the difficulty of the proof-of-work calculation performed when mining a block. The numeric value corresponds to the number of 0-bits that must be present at the start of the SHA256 hash of the contents of a valid mined block. The task of mining consists of adding a numeric value (called a _nonce_) into a block, hashing the block, and checking whether the hash has this many 0-bits at the start of it. The nonce value is incremented until a satisfactory hash is obtained, at which point the block is considered to be mined. Increasing the difficulty by 1 will, on average, double the time it takes to mine blocks.  

####block_size
The number of transactions which must be present in a block before it can be mined.

####block_reward
The amount of funds that a miner is allowed to allocate to themselves if they successfully mine a new block.

####key_size
The number of bits in the cryptographic keys used to sign transactions. [Larger values increase security](https://crypto.stackexchange.com/questions/19655/what-is-the-history-of-recommended-rsa-key-sizes) but require more CPU processing time.

####status_broadcast_interval_seconds
The interval (in seconds) between status broadcasts issued by mining nodes.

####transaction_broadcast_interval_seconds
The interval (in seconds) between transaction broadcasts issued by wallets.

####status_broadcast_port
The UDP port number used by miners for sending status broadcasts. All members of the network must use the same value for this parameter.

####block_server_port
The TCP port used by a mining node for its block server. Each miner may use a different port number, allowing multiple miners to run on the same host. Miners include the port number of their block server in the status broadcast.

####transaction_port
The UDP port number used by wallets to announce new transactions to the network. All members of the network must use the same value for this parameter.
