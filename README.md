# Ansible Bitcoin Module

Ansible module for automating Bitcoin transactions.

This is experimental code and should not be used to transfer money. Run bitcoin or bitcoind with the -testnet flag to use the testnet (or put testnet=1 in the bitcoin.conf file).

## Examples

```
# Send 0.01 BTC to 1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF
- bitcoin: sendtoaddress=1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF amount=0.01
```

## Requirements

- python-bitcoinlib >= 0.5
- bitcoind (bitcoin-core daemon)
