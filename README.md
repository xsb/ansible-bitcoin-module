# Ansible Bitcoin Module

Ansible module for automating Bitcoin transactions.

This is experimental code and should not be used to transfer money. Run bitcoin or bitcoind with the -testnet flag to use the testnet (or put testnet=1 in the bitcoin.conf file).

## Examples

```
# Send 0.01 BTC to 1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF
- bitcoin: sendtoaddress=1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF amount=0.01

# Send a transaction using testnet
- bitcoin: sendtoaddress=1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF amount=0.01 testnet=true

# Specify service URL for connection to bitcoind
- bitcoin: sendtoaddress=1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF amount=0.01 service_url=http://user:password@127.0.0.1:8332

# Specify port and config file for bitoind client
- bitcoin: sendtoaddress=1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF amount=0.01 service_port=8332 btc_conf_file=/path/to/bitcoin.conf
```

## Requirements

- python-bitcoinlib >= 0.5.0
- bitcoind (Bitcoin Core daemon) >= v0.11.0
