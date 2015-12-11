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
requirements:
  - "python-bitcoinlib >= 0.5"
  - "bitcoind (bitcoin-core daemon)"
'''

EXAMPLES = '''
# Send 0.01 BTC to 1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF
- bitcoin: sendtoaddress=1xsb94c9AMkj8GzhqYEJkieCXBpCZPvaF amount=0.01
'''

import bitcoin
from bitcoin import rpc

#def send_transaction(sendtoaddress, amount):
#    r = proxy.sendtoaddress(sendtoaddress, amount)
#    return r

def main():

    bitcoin.SelectParams("testnet")
    proxy = rpc.Proxy()

    module = AnsibleModule(
        argument_spec = dict(
            sendtoaddress = dict(required=True, type='str'),
            amount = dict(required=True, type='str'),
        ),
        supports_check_mode = False
    )

    sendtoaddress = module.params['sendtoaddress']
    amount = module.params['amount']

    rc = None
    out = 'out'
    err = 'err'
    result = {}
    result['sendtoaddress'] = sendtoaddress
    result['amount'] = amount

    try:
        proxy.sendtoaddress(sendtoaddress, int(amount*100000000))
        #r = send_transaction(sendtoaddress, amount)
        result['changed'] = True
    except:
        module.fail_json(sendtoaddress=sendtoaddress, amount=amount, msg=err)
        result['changed'] = False

    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err

    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
