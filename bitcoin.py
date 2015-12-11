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
        ),
        supports_check_mode = False
    )

    if module.params['testnet']:
        SelectParams("testnet")
    else:
        SelectParams("mainnet")
    proxy = rpc.Proxy()

    sendtoaddress = module.params['sendtoaddress']
    raw_amount = module.params['amount']
    amount = float(raw_amount)*100000000

    err = ''
    result = {}
    result['sendtoaddress'] = sendtoaddress
    result['amount'] = raw_amount

    try:
        txid = proxy.sendtoaddress(sendtoaddress, amount)
    except:
        err = "Error sending transaction"

    if err:
        module.fail_json(sendtoaddress=sendtoaddress, amount=raw_amount, msg=err)
        result['changed'] = False
    else:
        result['txid'] = txid
        result['changed'] = True

    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
