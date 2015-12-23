# Ansible Bitcoin Module

Ansible module for automating Bitcoin transactions.

This is experimental code and should not be used to transfer money. Run bitcoin or bitcoind with the -testnet flag to use the testnet (or put testnet=1 in the bitcoin.conf file).

## Requirements

- python-bitcoinlib >= 0.5.0
- bitcoind (Bitcoin Core daemon) >= v0.11.0

## Options

Parameter       | Required | Default | Choices              | Comments
:-------------- | :------- | :------ | :------------------- | :-------
sendtoaddress   | no       |         |                      | Public bitcoin address
amount          | no       |         |                      | Amount to transact
getnewaddress   | no       | no      | yes, no              | Generate a new bitcoin address
getbalance      | no       | no      | confirmed, total, no | Get current wallet balance
testnet         | no       | no      | yes, no              | If `yes`, use *testnet* instead of *mainnet*
service_url     | no       |         |                      | If not specified, the username and password are read out of the file
service_port    | no       |         |                      | The default port is set according to the chain parameters in use: *mainnet*, *testnet*
btc_conf_file   | no       |         |                      | If not specified `~/.bitcoin/bitcoin.conf` or equivalent is used by default

## Examples

```yaml
# Send 0.01 BTC to 1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF
- bitcoin: sendtoaddress=1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF amount=0.01

# Send a transaction using testnet
- bitcoin: sendtoaddress=n1LzM8zxDvtsdTVbc4yeY4vixa2H2uF5Ev amount=0.01 testnet=yes

# Generate new bitcoin address
- bitcoin: getnewaddress=yes

# Get confirmed wallet balance
- bitcoin: getbalance=confirmed
```

## Return Values

Name       | Description         | Returned | Type   | Sample
:--------- | :------------------ | :------- | :----- | :-----
txid       | transaction id      | success  | string | `f5d8ee39a430901c91a5917b9f2dc19d6d1a0e9cea205b009ca73dd04470b9a6`
newaddress | new bitcoin address | success  | string | `17Y7ZaAZYF3Gz8Sa9c5UifciVuthWfxx7F`
balance    | wallet balance      | success  | float  | `1.23965164`
