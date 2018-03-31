# Minimum Viable Blockchain
This project contains a pair of Python applications which together satisfy the requirements for a [minimum viable blockchain](https://www.igvita.com/2014/05/05/minimum-viable-block-chain/#properties). The applications form a decentralised peer-to-peer network, that allows the formation of distributed consensus regarding the validity of transactions that take place within it. Any number of wallets or miners may join or leave the network at any time.

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

The operations are:

### new-address
Creates a new address, from which payments can be sent and received. Each address has an associated public/private key pair stored in a [.pem file](http://how2ssl.com/articles/working_with_pem_files/). These files are all that is required to access any funds associated with a payment address, and therefore should be kept secret, and backed-up securely. To create a new payment address first choose a name for it; the name must be locally unique (i.e. it must be different to all your other address names) but it doesn't matter if someone else on the network has chosen the same name for one of their addresses. 

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

Run the wallet supplying the `send` argument, followed by the sending address, the amount, and the receiving address, in that order.

For example, to send a payment of '10' from `robs-address` to the remote address `e699496067b860f1cadcb7a4c7cc502a4e758b42cf624ac7fb40c65a0aa1edce`, run the following command:
```
> python -m blockchain.wallet.main send robs-address 10 e699496067b860f1cadcb7a4c7cc502a4e758b42cf624ac7fb40c65a0aa1edce
```
The sending address can be specified using either the local address name, as in the example above, or the global address name as displayed by the `list-addresses` command.

The receiving address should use the global address name of the recipient, unless funds are being transferred between 2 local addresses, in which case the local name can be used instead.

When the send command is issued, information concerning the transaction is sent to the network via a UDP broadcast, and will be re-broadcast at intervals when synchronising (see below) until the transaction is added to the blockchain by a mining node. 

### sync
Synchronises the wallet with the network, this operation will continue until the user cancels it by pressing `Ctrl-C`.

Synchronisation is started by running the wallet with the `sync` argument, as shown:
```
> python -m blockchain.wallet.main sync
```

During synchronisation 2 tasks are performed:

1. The wallet listens for status broadcasts from mining nodes. These broadcasts announce the length of the blockchain currently held by the miner. If a wallet receives a broadcast claiming a longer blockchain than the one that the wallet currently holds, then the wallet will request the additional blocks from the miner.
2. The wallet re-broadcasts details of any payments that it has made, which have not yet been included in the blockchain. This ensures that payments are processed even if no miners were online when the payment was originally made.

## Miner Application




