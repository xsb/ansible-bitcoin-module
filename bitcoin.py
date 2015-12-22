#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: bitcoin
author: "Xavi S.B. @xavi_xsb"
short_description: automate bitcoin transactions
description:
  - Automates Bitcoin transactions using a Bitcoin Core full node running locally
options:
  sendtoaddress:
    description:
      - Public bitcoin address
    required: true
  amount:
    description:
      - Amount to transact
    required: true
  testnet:
    description:
      - Use testnet mode
    default: false
  service_url:
    description:
      - If not specified, the username and password are read out of the file
    default: None
  service_port:
    description:
      - The default port is set according to the chain parameters in use: mainnet, testnet
    default: None
  btc_conf_file:
    description:
      - If not specified "~/.bitcoin/bitcoin.conf" or equivalent is used by default.
    default: None
requirements:
  - "python-bitcoinlib >= 0.5.0"
  - "bitcoind (Bitcoin Core daemon) >= v0.11.0"
'''

EXAMPLES = '''
# Send 0.01 BTC to 1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF
- bitcoin: sendtoaddress=1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF amount=0.01

# Send a transaction using testnet
- bitcoin: sendtoaddress=1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF amount=0.01 testnet=true
'''

from bitcoin import SelectParams, rpc

def main():

    module = AnsibleModule(
        argument_spec = dict(
            sendtoaddress = dict(required=True, type='str'),
            amount = dict(required=True, type='str'),
            testnet = dict(default=False, type='bool'),
            service_url = dict(default=None, type='str'),
            service_port = dict(default=None, type='int'),
            btc_conf_file = dict(default=None, type='str'),
        ),
        supports_check_mode = True
    )

    if module.params['testnet']:
        SelectParams("testnet")
    else:
        SelectParams("mainnet")

    proxy = rpc.Proxy(
            module.params['service_url'],
            module.params['service_port'],
            module.params['btc_conf_file']
    )

    sendtoaddress = module.params['sendtoaddress']
    raw_amount = module.params['amount']
    amount = float(raw_amount)*100000000

    err = ''
    txid = ''
    result = {}
    result['sendtoaddress'] = sendtoaddress
    result['amount'] = raw_amount

    if not module.check_mode:
        try:
            txid = proxy.sendtoaddress(sendtoaddress, amount)
        except Exception as e:
            err = str(e)

    if err:
        module.fail_json(sendtoaddress=sendtoaddress, amount=raw_amount, msg=err)
        result['changed'] = False
    else:
        result['txid'] = txid.encode("hex")
        result['changed'] = True

    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
